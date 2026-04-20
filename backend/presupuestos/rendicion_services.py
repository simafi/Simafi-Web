# -*- coding: utf-8 -*-
"""
Cálculos de ejecución presupuestaria para informes de rendición de cuentas.
Reutiliza la misma lógica jerárquica que los informes de ingresos; parametrizada por tipo.
"""
from decimal import Decimal

from django.db.models import Sum

from .models import (
    Compromiso,
    CuentaPresupuestaria,
    EjecucionPresupuestaria,
    Fondo,
    OperacionManual,
    OrdenPago,
    OrdenPagoDetalle,
    PresupuestoAnual,
    ProyectoInversion,
    ReformaPresupuestaria,
)

def forma07_cuenta_tesoreria(empresa, ejercicio, fecha_hasta=None, ajustes=None):
    """
    Forma 07 (TSC) - Cuenta de Tesorería.
    Implementación basada en datos disponibles en Tesorería (cobros/pagos/depositos/notas/conciliación).
    Nota: la distinción Presupuestario vs Extrapresupuestario requiere clasificación; aquí se infiere
    parcialmente (pagos vinculados a OrdenPago = presupuestario). Para cobros y depósitos se asume
    presupuestario salvo que el municipio lleve un catálogo separado.
    """
    from datetime import date
    from django.db.models import Q
    from tesoreria.models import (
        CuentaTesoreria,
        PagoTesoreria,
        PagoDetalleOrden,
        DepositoTesoreria,
        NotaTesoreria,
        ConciliacionBancaria,
        DetalleConciliacion,
        CobroCaja,
    )
    from core.models import Municipio

    inicio = ejercicio.fecha_inicio
    fin = fecha_hasta or ejercicio.fecha_fin
    anio = int(ejercicio.anio)
    mes_corte = int(fin.month)

    municipio = None
    try:
        municipio = Municipio.objects.filter(codigo=empresa).first()
    except Exception:
        municipio = None

    # --- A. EFECTIVO Y BANCOS ---
    # Cobros en caja (efectivo) dentro del ejercicio
    cobros_efectivo = (
        CobroCaja.objects.filter(empresa=empresa, fecha__range=[inicio, fin])
        .aggregate(t=Sum("total_cobrado"))["t"]
        or Decimal("0")
    )

    # Depósitos (bancos) dentro del ejercicio
    depositos_banco = (
        DepositoTesoreria.objects.filter(empresa=empresa, fecha__range=[inicio, fin])
        .aggregate(t=Sum("monto"))["t"]
        or Decimal("0")
    )

    pagos_qs = PagoTesoreria.objects.filter(empresa=empresa, fecha__range=[inicio, fin]).exclude(estado="ANULADO")

    # Presupuestario: si el pago tiene al menos un detalle enlazado a OrdenPago
    pagos_pres_ids = set(
        PagoDetalleOrden.objects.filter(pago__in=pagos_qs).values_list("pago_id", flat=True)
    )

    pagos_pres_qs = pagos_qs.filter(id__in=pagos_pres_ids)
    pagos_extra_qs = pagos_qs.exclude(id__in=pagos_pres_ids)

    pagos_pres_total = pagos_pres_qs.aggregate(t=Sum("monto_total"))["t"] or Decimal("0")
    pagos_extra_total = pagos_extra_qs.aggregate(t=Sum("monto_total"))["t"] or Decimal("0")

    # Separación efectivo/bancos en pagos: efectivo si tipo_pago EFECTIVO o cuenta CAJA_GENERAL
    pagos_pres_efectivo = (
        pagos_pres_qs.filter(Q(tipo_pago="EFECTIVO") | Q(cuenta_tesoreria__tipo="CAJA_GENERAL"))
        .aggregate(t=Sum("monto_total"))["t"]
        or Decimal("0")
    )
    pagos_pres_banco = pagos_pres_total - pagos_pres_efectivo

    pagos_extra_efectivo = (
        pagos_extra_qs.filter(Q(tipo_pago="EFECTIVO") | Q(cuenta_tesoreria__tipo="CAJA_GENERAL"))
        .aggregate(t=Sum("monto_total"))["t"]
        or Decimal("0")
    )
    pagos_extra_banco = pagos_extra_total - pagos_extra_efectivo

    # Ajustes manuales extrapresupuestarios (captura por ejercicio)
    if ajustes:
        try:
            pagos_extra_efectivo += Decimal(str(getattr(ajustes, "pagos_extra_efectivo", 0) or 0))
            pagos_extra_banco += Decimal(str(getattr(ajustes, "pagos_extra_bancos", 0) or 0))
        except Exception:
            pass

    # Entradas: por ahora consideramos cobros caja como presupuestario efectivo y depósitos como presupuestario banco.
    entradas_pres_efectivo = cobros_efectivo
    entradas_pres_banco = depositos_banco
    entradas_extra_efectivo = Decimal("0")
    entradas_extra_banco = Decimal("0")

    if ajustes:
        try:
            entradas_extra_efectivo += Decimal(str(getattr(ajustes, "entradas_extra_efectivo", 0) or 0))
            entradas_extra_banco += Decimal(str(getattr(ajustes, "entradas_extra_bancos", 0) or 0))
        except Exception:
            pass

    # Saldos iniciales: desde conciliación de diciembre del año anterior si existe (saldo_libro consolidado)
    # Saldo inicial: conciliación FINALIZADA del mes anterior al corte (o diciembre del año anterior)
    if mes_corte > 1:
        conc_prev = ConciliacionBancaria.objects.filter(
            empresa=empresa, anio=anio, mes=mes_corte - 1, estado="FINALIZADA"
        )
    else:
        conc_prev = ConciliacionBancaria.objects.filter(
            empresa=empresa, anio=anio - 1, mes=12, estado="FINALIZADA"
        )
    saldo_inicial_bancos = conc_prev.aggregate(t=Sum("saldo_libro"))["t"] or Decimal("0")
    saldo_inicial_efectivo = Decimal("0")  # depende de arqueos (Formas 05 y 06)

    disponible_efectivo = saldo_inicial_efectivo + entradas_pres_efectivo + entradas_extra_efectivo
    disponible_bancos = saldo_inicial_bancos + entradas_pres_banco + entradas_extra_banco
    disponible_total = disponible_efectivo + disponible_bancos

    pagos_efectivo = pagos_pres_efectivo + pagos_extra_efectivo
    pagos_banco = pagos_pres_banco + pagos_extra_banco
    pagos_total = pagos_efectivo + pagos_banco

    saldo_final_efectivo = disponible_efectivo - pagos_efectivo
    saldo_final_bancos = disponible_bancos - pagos_banco
    saldo_final_total = saldo_final_efectivo + saldo_final_bancos

    # --- B. EXISTENCIAS EN CAJA ---
    # No existe aún módulo de arqueos (Formas 05 y 06); mostrar 0 y advertir.
    existencia_caja = Decimal("0")

    # --- C. SALDO DE BANCOS SEGÚN CONSTANCIA ---
    # Debe ser consistente con la conciliación bancaria (D): el saldo según constancia
    # es el saldo_banco de la conciliación FINALIZADA del mes 12 por cuenta.
    cuentas_banco = CuentaTesoreria.objects.filter(empresa=empresa, tipo__in=["BANCO", "CHEQUERA"]).order_by("codigo")
    constancias = []
    total_constancias = Decimal("0")
    cuentas_sin_conc = []

    for ct in cuentas_banco:
        # Para rendición trimestral/fecha, usar la última conciliación FINALIZADA <= mes de corte.
        conc = (
            ConciliacionBancaria.objects.filter(
                empresa=empresa,
                cuenta_tesoreria=ct,
                anio=anio,
                mes__lte=mes_corte,
                estado="FINALIZADA",
            )
            .order_by("-mes", "-id")
            .first()
        )
        if not conc:
            cuentas_sin_conc.append(ct)
        saldo = (conc.saldo_banco if conc else Decimal("0")) or Decimal("0")
        constancias.append(
            {
                "banco": ct.nombre or ct.codigo,
                "cuenta_numero": ct.codigo,
                "tipo_cuenta": ct.get_tipo_display(),
                # TSC: columna Fondo (11, 12, 26…); completar cuando exista vínculo explícito cuenta–fondo en datos.
                "fondo_display": None,
                "saldo": saldo,
                "tiene_conciliacion": True if conc else False,
                "mes_conciliacion": conc.mes if conc else None,
            }
        )
        total_constancias += saldo

    # --- D. CONCILIACIÓN BANCARIA CONSOLIDADA ---
    # Consolidar usando conciliaciones FINALIZADAS hasta mes de corte
    conc_dic = ConciliacionBancaria.objects.filter(empresa=empresa, anio=anio, mes__lte=mes_corte, estado="FINALIZADA")
    saldo_libros = conc_dic.aggregate(t=Sum("saldo_libro"))["t"] or Decimal("0")
    saldo_bancos = conc_dic.aggregate(t=Sum("saldo_banco"))["t"] or Decimal("0")

    # Cheques no cobrados: pagos cheque emitidos <= fin sin evidencia de conciliación al 31/12
    pagos_cheque = PagoTesoreria.objects.filter(empresa=empresa, tipo_pago="CHEQUE", fecha__lte=fin).exclude(estado="ANULADO")
    pagos_conciliados_ids = set(
        DetalleConciliacion.objects.filter(
            conciliacion__empresa=empresa,
            conciliacion__anio=anio,
            conciliacion__mes__lte=mes_corte,
            conciliacion__estado="FINALIZADA",
            pago__isnull=False,
            fecha_banco__lte=fin,
        ).values_list("pago_id", flat=True)
    )
    cheques_no_cobrados_qs = pagos_cheque.exclude(id__in=pagos_conciliados_ids)
    cheques_no_cobrados = list(
        cheques_no_cobrados_qs.order_by("fecha", "numero_referencia").values(
            "fecha", "numero_referencia", "beneficiario", "monto_total"
        )
    )
    total_cheques_no_cobrados = cheques_no_cobrados_qs.aggregate(t=Sum("monto_total"))["t"] or Decimal("0")

    # Depósitos en tránsito: depósitos <= fin no conciliados
    depositos_transito_qs = DepositoTesoreria.objects.filter(empresa=empresa, fecha__lte=fin, is_reconciled=False).order_by(
        "fecha", "numero_referencia"
    )
    depositos_transito = list(depositos_transito_qs.values("fecha", "numero_referencia", "monto"))
    total_depositos_transito = depositos_transito_qs.aggregate(t=Sum("monto"))["t"] or Decimal("0")

    # Notas: crédito/débito sin contabilizar (no conciliadas)
    notas_credito = (
        NotaTesoreria.objects.filter(empresa=empresa, tipo="CREDITO", fecha__lte=fin, is_reconciled=False)
        .aggregate(t=Sum("monto"))["t"]
        or Decimal("0")
    )
    notas_debito = (
        NotaTesoreria.objects.filter(empresa=empresa, tipo="DEBITO", fecha__lte=fin, is_reconciled=False)
        .aggregate(t=Sum("monto"))["t"]
        or Decimal("0")
    )

    error_libros = Decimal("0")
    error_bancos = Decimal("0")

    saldo_conciliado_libros = saldo_libros + notas_credito - notas_debito + error_libros
    saldo_conciliado_bancos = saldo_bancos - total_cheques_no_cobrados + total_depositos_transito + error_bancos

    warnings = []
    if saldo_inicial_efectivo == 0:
        warnings.append("Saldo inicial en efectivo no calculable sin arqueos (Formas 05 y 06).")
    if not conc_dic.exists():
        warnings.append("No hay conciliación bancaria FINALIZADA hasta el mes de corte para generar constancias y conciliación consolidada.")
    if cuentas_sin_conc:
        warnings.append(
            "Faltan conciliaciones FINALIZADAS (diciembre) para estas cuentas: "
            + ", ".join((c.codigo for c in cuentas_sin_conc))
        )
    # Validación: el total de constancias (C) debe coincidir con saldo_bancos (D)
    # porque ambos provienen del saldo_banco de conciliaciones FINALIZADAS hasta el mes de corte.
    if conc_dic.exists() and total_constancias != saldo_bancos:
        warnings.append(
            "Advertencia: el total de 'Saldo de Bancos según constancia' no coincide con el 'Saldo en bancos' consolidado. "
            "Revise conciliaciones FINALIZADAS por cuenta hasta el mes de corte."
        )

    def _first_non_empty(*vals):
        for v in vals:
            if v is None:
                continue
            s = str(v).strip()
            if s:
                return s
        return ""

    return {
        "periodo": {"desde": inicio, "hasta": fin},
        "a": {
            "saldo_inicial": {"efectivo": saldo_inicial_efectivo, "bancos": saldo_inicial_bancos},
            "entradas": {
                "presupuestario": {"efectivo": entradas_pres_efectivo, "bancos": entradas_pres_banco},
                "extrapresupuestario": {"efectivo": entradas_extra_efectivo, "bancos": entradas_extra_banco},
            },
            "disponible": {"efectivo": disponible_efectivo, "bancos": disponible_bancos, "total": disponible_total},
            "pagos": {
                "presupuestario": {"efectivo": pagos_pres_efectivo, "bancos": pagos_pres_banco},
                "extrapresupuestario": {"efectivo": pagos_extra_efectivo, "bancos": pagos_extra_banco},
                "totales": {"efectivo": pagos_efectivo, "bancos": pagos_banco, "total": pagos_total},
            },
            "saldo_final": {"efectivo": saldo_final_efectivo, "bancos": saldo_final_bancos, "total": saldo_final_total},
        },
        "b": {"existencia_caja": existencia_caja},
        "c": {"constancias": constancias, "total": total_constancias},
        "d": {
            "saldo_libros": saldo_libros,
            "notas_credito": notas_credito,
            "notas_debito": notas_debito,
            "error_libros": error_libros,
            "saldo_conciliado_libros": saldo_conciliado_libros,
            "saldo_bancos": saldo_bancos,
            "cheques_no_cobrados_total": total_cheques_no_cobrados,
            "depositos_transito_total": total_depositos_transito,
            "error_bancos": error_bancos,
            "saldo_conciliado_bancos": saldo_conciliado_bancos,
            "anexos": {"depositos_transito": depositos_transito, "cheques_no_cobrados": cheques_no_cobrados},
        },
        "warnings": warnings,
        "firmas": {
            # Por defecto catálogo Municipio; ajustes Forma 07 solo si se capturan (sobrescriben).
            "alcalde_nombre": _first_non_empty(
                getattr(municipio, "alcalde", None) if municipio else None,
                getattr(ajustes, "alcalde_nombre", None) if ajustes else None,
            ),
            "tesorero_nombre": _first_non_empty(
                getattr(municipio, "tesorero", None) if municipio else None,
                getattr(municipio, "tesorera", None) if municipio else None,
                getattr(ajustes, "tesorero_nombre", None) if ajustes else None,
            ),
            "contador_nombre": _first_non_empty(
                getattr(municipio, "contador", None) if municipio else None,
                getattr(ajustes, "contador_nombre", None) if ajustes else None,
            ),
        },
    }

def _safe_pct(delta, base):
    try:
        b = Decimal(base or 0)
        if b == 0:
            return Decimal("0")
        return (Decimal(delta or 0) / b) * Decimal("100")
    except Exception:
        return Decimal("0")


def totales_ingresos_egresos(empresa, ejercicio_id):
    """
    Totales consolidados del ejercicio:
    - ingresos_recaudados: suma de ejecución + operaciones manuales tipo INGRESO
    - egresos_ejecutados: suma de ejecución + operaciones manuales tipo EGRESO
    """
    ing = (
        EjecucionPresupuestaria.objects.filter(
            empresa=empresa,
            ejercicio_id=ejercicio_id,
            cuenta_presupuestaria__tipo_presupuesto="INGRESO",
        ).aggregate(t=Sum("monto"))["t"]
        or Decimal("0")
    )
    eg = (
        EjecucionPresupuestaria.objects.filter(
            empresa=empresa,
            ejercicio_id=ejercicio_id,
            cuenta_presupuestaria__tipo_presupuesto="EGRESO",
        ).aggregate(t=Sum("monto"))["t"]
        or Decimal("0")
    )
    om_ing = (
        OperacionManual.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, tipo="INGRESO", is_active=True)
        .aggregate(t=Sum("monto"))["t"]
        or Decimal("0")
    )
    om_eg = (
        OperacionManual.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, tipo="EGRESO", is_active=True)
        .aggregate(t=Sum("monto"))["t"]
        or Decimal("0")
    )
    ingresos_recaudados = ing + om_ing
    egresos_ejecutados = eg + om_eg
    return {
        "ingresos_recaudados": ingresos_recaudados,
        "egresos_ejecutados": egresos_ejecutados,
        "superavit_deficit": ingresos_recaudados - egresos_ejecutados,
    }


def forma04_liquidacion_presupuesto(empresa, ejercicio_id, ajustes=None):
    """
    Forma 04 TSC — Liquidación del Presupuesto (resultado presupuestario).
    Ingresos devengados/recaudados (ejecución presupuestaria + OM ingreso) menos obligaciones contraídas en el año
    (órdenes de pago aprobadas y pagadas). Ajustes por ingreso/egreso opcionales.
    """
    t = totales_ingresos_egresos(empresa, ejercicio_id)
    ingresos_devengados = t["ingresos_recaudados"]

    ing_ep = (
        EjecucionPresupuestaria.objects.filter(
            empresa=empresa,
            ejercicio_id=ejercicio_id,
            cuenta_presupuestaria__tipo_presupuesto="INGRESO",
        ).aggregate(t=Sum("monto"))["t"]
        or Decimal("0.00")
    )

    obligaciones_contraidas = (
        OrdenPagoDetalle.objects.filter(
            orden_pago__empresa=empresa,
            orden_pago__ejercicio_id=ejercicio_id,
        )
        .exclude(orden_pago__estado="ANULADA")
        .filter(orden_pago__estado__in=["APROBADA", "PAGADA"])
        .aggregate(t=Sum("monto"))["t"]
        or Decimal("0.00")
    )

    resultado = ingresos_devengados - obligaciones_contraidas

    ai = Decimal("0.00")
    ae = Decimal("0.00")
    if ajustes is not None:
        try:
            ai = Decimal(str(getattr(ajustes, "ajuste_por_ingreso", 0) or 0)).quantize(Decimal("0.01"))
        except Exception:
            ai = Decimal("0.00")
        try:
            ae = Decimal(str(getattr(ajustes, "ajuste_por_egreso", 0) or 0)).quantize(Decimal("0.01"))
        except Exception:
            ae = Decimal("0.00")

    resultado_ajustado = resultado + ai - ae

    return {
        "ingresos_devengados": ingresos_devengados,
        "ingresos_solo_ejecucion_presupuestaria": ing_ep,
        "obligaciones_contraidas_anio": obligaciones_contraidas,
        "resultado_presupuestario": resultado,
        "ajuste_por_ingreso": ai,
        "ajuste_por_egreso": ae,
        "resultado_presupuestario_ajustado": resultado_ajustado,
        "egresos_ejecutados_presupuesto_referencia": t["egresos_ejecutados"],
    }


def _sub100_letras_es(n):
    """Convierte 0-99 a palabras (español)."""
    if n < 0 or n > 99:
        return str(n)
    if n < 10:
        return ("cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve")[n]
    if n < 20:
        return (
            "diez",
            "once",
            "doce",
            "trece",
            "catorce",
            "quince",
            "dieciséis",
            "diecisiete",
            "dieciocho",
            "diecinueve",
        )[n - 10]
    d, u = divmod(n, 10)
    dec = ("", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa")
    veinti = {
        1: "veintiuno",
        2: "veintidós",
        3: "veintitrés",
        4: "veinticuatro",
        5: "veinticinco",
        6: "veintiséis",
        7: "veintisiete",
        8: "veintiocho",
        9: "veintinueve",
    }
    if d == 2:
        return veinti[u] if u else "veinte"
    if u == 0:
        return dec[d]
    return f"{dec[d]} y {_sub100_letras_es(u)}"


def _hasta_999_letras_es(n):
    """Convierte 0-999 a palabras."""
    if n == 0:
        return ""
    if n < 0 or n > 999:
        return str(n)
    if n == 100:
        return "cien"
    centenas = (
        "",
        "ciento",
        "doscientos",
        "trescientos",
        "cuatrocientos",
        "quinientos",
        "seiscientos",
        "setecientos",
        "ochocientos",
        "novecientos",
    )
    c, r = divmod(n, 100)
    parts = []
    if c:
        parts.append(centenas[c] if r else ("cien" if c == 1 else centenas[c]))
    if r:
        parts.append(_sub100_letras_es(r))
    return " ".join(parts)


def _entero_a_letras_es(n: int) -> str:
    if n == 0:
        return "cero"
    if n < 0:
        return "menos " + _entero_a_letras_es(-n)
    if n >= 10**9:
        return f"{n:,}"
    parts = []
    mm = n // 10**6
    n %= 10**6
    if mm:
        parts.append("un millón" if mm == 1 else f"{_hasta_999_letras_es(mm)} millones")
    miles = n // 1000
    n %= 1000
    if miles:
        if miles == 1:
            parts.append("mil")
        else:
            parts.append(f"{_hasta_999_letras_es(miles)} mil")
    if n:
        parts.append(_hasta_999_letras_es(n))
    return " ".join(parts).replace("uno mil", "mil").strip()


def _monto_a_letras_es(monto):
    try:
        d = Decimal(str(monto)).quantize(Decimal("0.01"))
    except Exception:
        return "—"
    ent = int(d)
    cent = int((d - Decimal(ent)) * 100)
    t = _entero_a_letras_es(ent)
    if cent:
        return f"{t} lempiras con {cent}/100"
    return f"{t} lempiras"


def forma05_arqueo_caja_general(empresa, ejercicio, fecha_hasta=None, ajustes_f05=None, salidas_manuales_qs=None):
    """
    Forma 05 TSC — Arqueo de Caja General.
    Salidas de efectivo desde cuenta de tesorería «Caja General»; sumatoria de cheques (pagos tipo cheque);
    disponibilidad estimada: entradas en efectivo (cobros caja) menos salidas de efectivo en el periodo.
    `ajustes_f05` y `salidas_manuales_qs` complementan lo capturado en Presupuestos (informe alimentado manualmente).
    """
    try:
        from tesoreria.models import CobroCaja, CobroCajaMetodo, CuentaTesoreria, PagoTesoreria
    except Exception:
        fin = fecha_hasta or ejercicio.fecha_fin
        if fin < ejercicio.fecha_inicio:
            fin = ejercicio.fecha_inicio
        if fin > ejercicio.fecha_fin:
            fin = ejercicio.fecha_fin
        inicio = ejercicio.fecha_inicio
        ex = (ajustes_f05.extra_entradas_efectivo if ajustes_f05 else None) or Decimal("0.00")
        es_adj = (ajustes_f05.extra_salidas_efectivo if ajustes_f05 else None) or Decimal("0.00")
        ec = (ajustes_f05.extra_cheques if ajustes_f05 else None) or Decimal("0.00")
        filas_m = []
        if salidas_manuales_qs is not None:
            for m in salidas_manuales_qs:
                if inicio <= m.fecha <= fin:
                    filas_m.append(
                        {
                            "descripcion": (m.descripcion or "").strip(),
                            "valor": m.monto or Decimal("0.00"),
                            "valor_en_letras": _monto_a_letras_es(m.monto),
                            "fecha": m.fecha,
                            "documento": (m.documento or "").strip(),
                            "es_manual": True,
                        }
                    )
        sum_lineas = sum((f["valor"] for f in filas_m), Decimal("0.00"))
        sum_sal = sum_lineas + es_adj
        disp = ex - sum_sal
        return {
            "salidas_efectivo": sorted(filas_m, key=lambda r: (r["fecha"], r["documento"] or "")),
            "sumatoria_salidas_efectivo": sum_sal,
            "sumatoria_salidas_solo_lineas": sum_lineas,
            "sumatoria_cheques": ec,
            "sumatoria_cheques_sistema": Decimal("0.00"),
            "entradas_efectivo_caja": ex,
            "entradas_efectivo_sistema": Decimal("0.00"),
            "disponibilidad_estimada": disp,
            "fecha_inicio": inicio,
            "fecha_fin": fin,
            "warnings": ["No se pudo cargar el módulo Tesorería (modelos o migraciones pendientes)."],
            "extras": {"entradas": ex, "salidas": es_adj, "cheques": ec},
        }

    inicio = ejercicio.fecha_inicio
    fin = fecha_hasta or ejercicio.fecha_fin
    if fin < inicio:
        fin = inicio
    if fin > ejercicio.fecha_fin:
        fin = ejercicio.fecha_fin

    warnings = []
    cuenta_ids_caja = list(
        CuentaTesoreria.objects.filter(empresa=empresa, tipo="CAJA_GENERAL", is_active=True).values_list("id", flat=True)
    )

    if cuenta_ids_caja:
        salidas_qs = (
            PagoTesoreria.objects.filter(
                empresa=empresa,
                fecha__range=[inicio, fin],
                cuenta_tesoreria_id__in=cuenta_ids_caja,
                tipo_pago="EFECTIVO",
            )
            .exclude(estado="ANULADO")
            .select_related("cuenta_tesoreria")
            .order_by("fecha", "id")
        )
    else:
        salidas_qs = (
            PagoTesoreria.objects.filter(empresa=empresa, fecha__range=[inicio, fin], tipo_pago="EFECTIVO")
            .exclude(estado="ANULADO")
            .select_related("cuenta_tesoreria")
            .order_by("fecha", "id")
        )
        warnings.append(
            "No hay cuenta de tesorería tipo «Caja General» configurada; se listan todos los pagos en efectivo del periodo."
        )

    filas = []
    for p in salidas_qs:
        desc = (p.beneficiario or "").strip()
        if p.concepto:
            desc = f"{desc} — {(p.concepto or '')[:200]}" if desc else (p.concepto or "")[:200]
        if not desc:
            desc = f"Pago efectivo {p.numero_referencia or p.id}"
        filas.append(
            {
                "descripcion": desc,
                "valor": p.monto_total or Decimal("0.00"),
                "valor_en_letras": _monto_a_letras_es(p.monto_total),
                "fecha": p.fecha,
                "documento": p.numero_referencia or "",
                "es_manual": False,
            }
        )

    if salidas_manuales_qs is not None:
        for m in salidas_manuales_qs:
            if inicio <= m.fecha <= fin:
                filas.append(
                    {
                        "descripcion": (m.descripcion or "").strip(),
                        "valor": m.monto or Decimal("0.00"),
                        "valor_en_letras": _monto_a_letras_es(m.monto),
                        "fecha": m.fecha,
                        "documento": (m.documento or "").strip(),
                        "es_manual": True,
                    }
                )

    filas.sort(key=lambda r: (r["fecha"], r["es_manual"], r["documento"] or ""))

    sum_lineas = sum((f["valor"] for f in filas), Decimal("0.00"))
    extra_s = (ajustes_f05.extra_salidas_efectivo if ajustes_f05 else None) or Decimal("0.00")
    extra_e = (ajustes_f05.extra_entradas_efectivo if ajustes_f05 else None) or Decimal("0.00")
    extra_c = (ajustes_f05.extra_cheques if ajustes_f05 else None) or Decimal("0.00")
    sum_salidas = sum_lineas + extra_s

    sum_cheques_sistema = (
        PagoTesoreria.objects.filter(empresa=empresa, fecha__range=[inicio, fin], tipo_pago="CHEQUE")
        .exclude(estado="ANULADO")
        .aggregate(t=Sum("monto_total"))["t"]
        or Decimal("0.00")
    )
    sum_cheques = sum_cheques_sistema + extra_c

    cobros_ids = CobroCaja.objects.filter(empresa=empresa, fecha__range=[inicio, fin]).values_list("id", flat=True)
    entradas_ef_base = (
        CobroCajaMetodo.objects.filter(cobro_id__in=cobros_ids, forma_pago="EFECTIVO").aggregate(t=Sum("monto"))["t"]
        or Decimal("0.00")
    )
    if not cobros_ids:
        entradas_ef_base = Decimal("0.00")
    entradas_ef = entradas_ef_base + extra_e

    disponibilidad = entradas_ef - sum_salidas

    return {
        "salidas_efectivo": filas,
        "sumatoria_salidas_efectivo": sum_salidas,
        "sumatoria_salidas_solo_lineas": sum_lineas,
        "sumatoria_cheques": sum_cheques,
        "sumatoria_cheques_sistema": sum_cheques_sistema,
        "entradas_efectivo_caja": entradas_ef,
        "entradas_efectivo_sistema": entradas_ef_base,
        "disponibilidad_estimada": disponibilidad,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
        "warnings": warnings,
        "extras": {"entradas": extra_e, "salidas": extra_s, "cheques": extra_c},
    }


def balance_general_a_fecha(empresa, ejercicio_id, fecha_hasta):
    """
    Balance general a la fecha usando Contabilidad (LibroMayor) por grupos:
    1=Activo, 2=Pasivo, 3=Patrimonio.
    """
    from decimal import Decimal as D
    from django.db.models import OuterRef, Subquery
    from contabilidad.models import CuentaContable, LibroMayor

    def _por_grupo(codigo_grupo):
        libro_subq = LibroMayor.objects.filter(
            empresa=empresa,
            cuenta_id=OuterRef("pk"),
            periodo__ejercicio_id=ejercicio_id,
            periodo__fecha_fin__lte=fecha_hasta,
        ).order_by("-periodo__numero").values("saldo_final")[:1]

        cuentas = (
            CuentaContable.objects.filter(empresa=empresa, grupo__codigo=codigo_grupo, is_active=True)
            .annotate(saldo=Subquery(libro_subq))
            .order_by("codigo")
        )
        filas = []
        total = D("0.00")
        for c in cuentas:
            s = c.saldo if c.saldo is not None else D("0.00")
            filas.append({"codigo": c.codigo, "nombre": c.nombre, "saldo": s})
            total += s
        return filas, total

    activos, total_act = _por_grupo("1")
    pasivos, total_pas = _por_grupo("2")
    patrimonio, total_pat = _por_grupo("3")
    return {
        "activos": activos,
        "pasivos": pasivos,
        "patrimonio": patrimonio,
        "totales": {"activos": total_act, "pasivos": total_pas, "patrimonio": total_pat},
    }


def balance_general_comparativo(empresa, ejercicio_actual, ejercicio_anterior, fecha_hasta_actual, fecha_hasta_anterior):
    """
    Comparativo de balance general (monetario y % sobre año anterior).
    Retorna totales por rubro y filas comparativas por cuenta (según cuentas del año actual).
    """
    actual = balance_general_a_fecha(empresa, ejercicio_actual.id, fecha_hasta_actual)
    anterior = balance_general_a_fecha(empresa, ejercicio_anterior.id, fecha_hasta_anterior)

    def _merge_rows(rows_actual, rows_prev):
        prev_by = {r["codigo"]: r for r in rows_prev}
        out = []
        for r in rows_actual:
            sa = r["saldo"] or Decimal("0")
            sp = (prev_by.get(r["codigo"], {}).get("saldo")) or Decimal("0")
            delta = sa - sp
            out.append(
                {
                    "codigo": r["codigo"],
                    "nombre": r["nombre"],
                    "actual": sa,
                    "anterior": sp,
                    "variacion": delta,
                    "variacion_pct": _safe_pct(delta, sp),
                }
            )
        return out

    comp = {
        "activos": _merge_rows(actual["activos"], anterior["activos"]),
        "pasivos": _merge_rows(actual["pasivos"], anterior["pasivos"]),
        "patrimonio": _merge_rows(actual["patrimonio"], anterior["patrimonio"]),
        "totales": {
            "actual": actual["totales"],
            "anterior": anterior["totales"],
            "variacion": {
                "activos": actual["totales"]["activos"] - anterior["totales"]["activos"],
                "pasivos": actual["totales"]["pasivos"] - anterior["totales"]["pasivos"],
                "patrimonio": actual["totales"]["patrimonio"] - anterior["totales"]["patrimonio"],
            },
            "variacion_pct": {
                "activos": _safe_pct(actual["totales"]["activos"] - anterior["totales"]["activos"], anterior["totales"]["activos"]),
                "pasivos": _safe_pct(actual["totales"]["pasivos"] - anterior["totales"]["pasivos"], anterior["totales"]["pasivos"]),
                "patrimonio": _safe_pct(actual["totales"]["patrimonio"] - anterior["totales"]["patrimonio"], anterior["totales"]["patrimonio"]),
            },
        },
    }
    return comp


def calcular_ejecucion_presupuestaria(
    empresa,
    ejercicio_id,
    tipo_presupuesto,
    fecha_desde=None,
    fecha_hasta=None,
    solo_nivel_2=False,
):
    """
    tipo_presupuesto: 'INGRESO' | 'EGRESO'
    Retorna lista de dicts con aprobado, reformas, ejecutado (recaudado/devengado según tipo).
    """
    tipo_om = "INGRESO" if tipo_presupuesto == "INGRESO" else "EGRESO"
    cuentas = CuentaPresupuestaria.objects.filter(
        empresa=empresa,
        tipo_presupuesto=tipo_presupuesto,
        is_active=True,
    ).order_by("codigo")

    data_map = {}
    for c in cuentas:
        data_map[c.id] = {
            "aprobado": Decimal("0.00"),
            "reformas": Decimal("0.00"),
            "ejecutado": Decimal("0.00"),
            "ejecutado_periodo": Decimal("0.00"),
        }

    pa_qs = PresupuestoAnual.objects.filter(
        empresa=empresa,
        ejercicio_id=ejercicio_id,
        cuenta__tipo_presupuesto=tipo_presupuesto,
    )
    for pa in pa_qs:
        if pa.cuenta_id in data_map:
            data_map[pa.cuenta_id]["aprobado"] = pa.monto_inicial
            data_map[pa.cuenta_id]["reformas"] = pa.monto_reformas

    exec_qs = EjecucionPresupuestaria.objects.filter(
        empresa=empresa,
        ejercicio_id=ejercicio_id,
        cuenta_presupuestaria__tipo_presupuesto=tipo_presupuesto,
    )
    if fecha_desde and fecha_hasta:
        exec_periodo = exec_qs.filter(fecha__range=[fecha_desde, fecha_hasta])
        res_periodo = exec_periodo.values("cuenta_presupuestaria_id").annotate(total=Sum("monto"))
        for r in res_periodo:
            cid = r["cuenta_presupuestaria_id"]
            if cid in data_map:
                data_map[cid]["ejecutado_periodo"] = r["total"] or Decimal("0.00")

    if fecha_hasta:
        exec_qs = exec_qs.filter(fecha__lte=fecha_hasta)

    res_total = exec_qs.values("cuenta_presupuestaria_id").annotate(total=Sum("monto"))
    for r in res_total:
        cid = r["cuenta_presupuestaria_id"]
        if cid in data_map:
            data_map[cid]["ejecutado"] = r["total"] or Decimal("0.00")

    op_qs = OperacionManual.objects.filter(
        empresa=empresa,
        ejercicio_id=ejercicio_id,
        tipo=tipo_om,
    )
    if fecha_desde and fecha_hasta:
        op_periodo = (
            op_qs.filter(fecha__range=[fecha_desde, fecha_hasta])
            .values("cuenta_id")
            .annotate(total=Sum("monto"))
        )
        for r in op_periodo:
            if r["cuenta_id"] in data_map:
                data_map[r["cuenta_id"]]["ejecutado_periodo"] += r["total"] or Decimal("0.00")

    if fecha_hasta:
        op_qs = op_qs.filter(fecha__lte=fecha_hasta)

    op_total = op_qs.values("cuenta_id").annotate(total=Sum("monto"))
    for r in op_total:
        if r["cuenta_id"] in data_map:
            data_map[r["cuenta_id"]]["ejecutado"] += r["total"] or Decimal("0.00")

    cuentas_sorted = sorted(cuentas, key=lambda x: x.nivel, reverse=True)
    for c in cuentas_sorted:
        if c.cuenta_padre_id and c.cuenta_padre_id in data_map:
            p_id = c.cuenta_padre_id
            data_map[p_id]["aprobado"] += data_map[c.id]["aprobado"]
            data_map[p_id]["reformas"] += data_map[c.id]["reformas"]
            data_map[p_id]["ejecutado"] += data_map[c.id]["ejecutado"]
            data_map[p_id]["ejecutado_periodo"] += data_map[c.id]["ejecutado_periodo"]

    resultados = []
    for c in cuentas:
        d = data_map[c.id]
        if solo_nivel_2 and c.nivel > 2:
            continue
        total_aprobado = d["aprobado"] + d["reformas"]
        por_ejecutar = total_aprobado - d["ejecutado"]
        pct = (d["ejecutado"] / total_aprobado * 100) if total_aprobado > 0 else 0
        resultados.append(
            {
                "codigo": c.codigo,
                "nombre": c.nombre,
                "nivel": c.nivel,
                "tipo": c.tipo_cuenta,
                "aprobado": d["aprobado"],
                "reformas": d["reformas"],
                "total_aprobado": total_aprobado,
                "ejecutado": d["ejecutado"],
                "ejecutado_periodo": d["ejecutado_periodo"],
                "saldo_por_ejecutar": por_ejecutar,
                "porcentaje": pct,
            }
        )
    return resultados


def totales_por_fondo(empresa, ejercicio_id, tipo_presupuesto):
    """Suma presupuesto vigente y ejecución por fondo."""
    fondos = Fondo.objects.filter(empresa=empresa, is_active=True).order_by("codigo")
    filas = []
    for f in fondos:
        pa = PresupuestoAnual.objects.filter(
            empresa=empresa,
            ejercicio_id=ejercicio_id,
            fondo=f,
            cuenta__tipo_presupuesto=tipo_presupuesto,
        )
        vigente = sum((p.monto_inicial + p.monto_reformas) for p in pa)
        ejec = EjecucionPresupuestaria.objects.filter(
            empresa=empresa,
            ejercicio_id=ejercicio_id,
            fondo=f,
            cuenta_presupuestaria__tipo_presupuesto=tipo_presupuesto,
        ).aggregate(t=Sum("monto"))["t"] or Decimal("0")
        om_tipo = "INGRESO" if tipo_presupuesto == "INGRESO" else "EGRESO"
        om = OperacionManual.objects.filter(
            empresa=empresa,
            ejercicio_id=ejercicio_id,
            fondo=f,
            tipo=om_tipo,
        ).aggregate(t=Sum("monto"))["t"] or Decimal("0")
        ejecutado = ejec + om
        filas.append(
            {
                "fondo_codigo": f.codigo,
                "fondo_nombre": f.nombre,
                "presupuesto_vigente": vigente,
                "ejecutado": ejecutado,
                "saldo": vigente - ejecutado,
            }
        )
    return filas


def reformas_por_tipo(empresa, ejercicio_id, tipo_presupuesto):
    """Listado de reformas que afectan cuentas del tipo indicado."""
    qs = (
        ReformaPresupuestaria.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True)
        .filter(cuenta_destino__tipo_presupuesto=tipo_presupuesto)
        .select_related("cuenta_destino", "cuenta_origen", "fondo")
        .order_by("fecha", "referencia")
    )
    return list(qs)


def reformas_ampliaciones(empresa, ejercicio_id):
    return list(
        ReformaPresupuestaria.objects.filter(
            empresa=empresa, ejercicio_id=ejercicio_id, tipo="AMPLIACION", is_active=True
        )
        .select_related("cuenta_destino", "cuenta_origen", "fondo")
        .order_by("fecha", "referencia")
    )


def reformas_reducciones_y_traspasos(empresa, ejercicio_id):
    return list(
        ReformaPresupuestaria.objects.filter(
            empresa=empresa, ejercicio_id=ejercicio_id, is_active=True, tipo__in=["REDUCCION", "TRASPASO"]
        )
        .select_related("cuenta_destino", "cuenta_origen", "fondo")
        .order_by("fecha", "referencia")
    )


def reformas_ampliaciones_disminuciones_detalle(empresa, ejercicio_id, tipo_presupuesto):
    """
    Filas detalladas de reformas para INGRESO o EGRESO (ampliaciones / disminuciones).
    Los traspasos se reflejan en origen (disminución) y destino (ampliación) solo si la cuenta corresponde al tipo.
    Retorna (lista_ampliaciones, lista_disminuciones) con dicts: tipo, fecha, referencia, cuenta, fondo, monto, concepto.
    """
    tp = tipo_presupuesto

    def _match(cuenta):
        return cuenta is not None and getattr(cuenta, "tipo_presupuesto", None) == tp

    disminuciones_rows = []
    ampliaciones_rows = []

    for r in reformas_ampliaciones(empresa, ejercicio_id):
        if _match(r.cuenta_destino):
            ampliaciones_rows.append(
                {
                    "tipo": "AMPLIACIÓN",
                    "fecha": r.fecha,
                    "referencia": r.referencia,
                    "cuenta": r.cuenta_destino,
                    "fondo": r.fondo,
                    "monto": r.monto,
                    "concepto": r.concepto,
                }
            )

    for r in reformas_reducciones_y_traspasos(empresa, ejercicio_id):
        t = getattr(r, "tipo", "") or ""
        if t == "REDUCCION" and _match(r.cuenta_destino):
            disminuciones_rows.append(
                {
                    "tipo": "REDUCCIÓN",
                    "fecha": r.fecha,
                    "referencia": r.referencia,
                    "cuenta": r.cuenta_destino,
                    "fondo": r.fondo,
                    "monto": r.monto,
                    "concepto": r.concepto,
                }
            )
        elif t == "TRASPASO":
            if _match(r.cuenta_origen):
                disminuciones_rows.append(
                    {
                        "tipo": "TRASPASO (origen)",
                        "fecha": r.fecha,
                        "referencia": r.referencia,
                        "cuenta": r.cuenta_origen,
                        "fondo": r.fondo,
                        "monto": r.monto,
                        "concepto": r.concepto,
                    }
                )
            if _match(r.cuenta_destino):
                ampliaciones_rows.append(
                    {
                        "tipo": "TRASPASO (destino)",
                        "fecha": r.fecha,
                        "referencia": r.referencia,
                        "cuenta": r.cuenta_destino,
                        "fondo": r.fondo,
                        "monto": r.monto,
                        "concepto": r.concepto,
                    }
                )

    disminuciones_rows.sort(key=lambda x: (x["fecha"], x["referencia"] or ""))
    ampliaciones_rows.sort(key=lambda x: (x["fecha"], x["referencia"] or ""))
    return ampliaciones_rows, disminuciones_rows


def listado_reformas_todas(empresa, ejercicio_id):
    """Todas las reformas del ejercicio (ampliaciones, reducciones y traspasos)."""
    return list(
        ReformaPresupuestaria.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True)
        .select_related("cuenta_destino", "cuenta_origen", "fondo")
        .order_by("fecha", "referencia")
    )


def listado_compromisos(empresa, ejercicio_id):
    return list(
        Compromiso.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True).order_by(
            "-fecha", "-numero"
        )
    )


def listado_ordenes_pago(empresa, ejercicio_id):
    return list(
        OrdenPago.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True).order_by(
            "-fecha", "-numero"
        )
    )


def listado_proyectos(empresa, ejercicio_id):
    return list(
        ProyectoInversion.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True).order_by(
            "codigo"
        )
    )


def operaciones_manuales_todas(empresa, ejercicio_id):
    return list(
        OperacionManual.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True)
        .select_related("cuenta", "fondo")
        .order_by("-fecha", "-id")
    )


def tabla_ejecucion_mensual(empresa, ejercicio, tipo_presupuesto):
    """Filas por cuenta con 12 meses + total (misma lógica que informe mensual ingresos)."""
    tipo_om = "INGRESO" if tipo_presupuesto == "INGRESO" else "EGRESO"
    cuentas = CuentaPresupuestaria.objects.filter(
        empresa=empresa, tipo_presupuesto=tipo_presupuesto, nivel__lte=2, is_active=True
    ).order_by("codigo")

    resultado_final = []
    for c in cuentas:
        fila = {"codigo": c.codigo, "nombre": c.nombre, "nivel": c.nivel, "meses": []}
        total_anio = Decimal("0.00")
        hijos_ids = CuentaPresupuestaria.objects.filter(
            empresa=empresa, codigo__startswith=c.codigo
        ).values_list("id", flat=True)

        for mes in range(1, 13):
            monto = EjecucionPresupuestaria.objects.filter(
                empresa=empresa,
                ejercicio=ejercicio,
                cuenta_presupuestaria_id__in=hijos_ids,
                fecha__month=mes,
            ).aggregate(total=Sum("monto"))["total"] or Decimal("0.00")

            monto += (
                OperacionManual.objects.filter(
                    empresa=empresa,
                    ejercicio=ejercicio,
                    tipo=tipo_om,
                    cuenta_id__in=hijos_ids,
                    fecha__month=mes,
                ).aggregate(total=Sum("monto"))["total"]
                or Decimal("0.00")
            )

            fila["meses"].append(monto)
            total_anio += monto

        fila["total"] = total_anio
        resultado_final.append(fila)
    return resultado_final


def _ids_arbol_cuenta(empresa, cuenta):
    """IDs de la cuenta presupuestaria y todas sus subcuentas."""
    ids = set()
    stack = [cuenta.id]
    while stack:
        cid = stack.pop()
        if cid in ids:
            continue
        ids.add(cid)
        for ch in CuentaPresupuestaria.objects.filter(empresa=empresa, cuenta_padre_id=cid).values_list(
            "id", flat=True
        ):
            stack.append(ch)
    return ids


def _fondo_bucket_f11_f12_otros(fondo):
    """Clasifica fondo municipal típico 11 / 12 / otros (por código numérico)."""
    if not fondo:
        return "otros"
    c = (fondo.codigo or "").strip()
    try:
        n = int(c)
        if n == 11:
            return "f11"
        if n == 12:
            return "f12"
    except ValueError:
        pass
    return "otros"


def _triple_fondo():
    return {"f11": Decimal("0.00"), "f12": Decimal("0.00"), "otros": Decimal("0.00")}


def _quad_fondo():
    return {"f11": Decimal("0.00"), "f12": Decimal("0.00"), "erp": Decimal("0.00"), "otros": Decimal("0.00")}


def _fondo_bucket_f11_f12_erp_otros(fondo):
    """
    Clasifica fondo municipal: 11, 12, ERP (código/nombre con «ERP» o numérico 13), u otros.
    """
    if not fondo:
        return "otros"
    c_raw = (fondo.codigo or "").strip()
    nombre = (fondo.nombre or "").upper()
    c_up = c_raw.upper()
    if "ERP" in c_up or "ERP" in nombre:
        return "erp"
    try:
        n = int(c_raw)
        if n == 11:
            return "f11"
        if n == 12:
            return "f12"
        if n == 13:
            return "erp"
    except ValueError:
        pass
    return "otros"


def _sumar_triple(target, add):
    for k in target:
        target[k] += add.get(k, Decimal("0.00"))


def forma02_liquidacion_egresos_por_programa(empresa, ejercicio_id):
    """
    Forma 02 TSC — Liquidación del presupuesto de egresos por programa.
    Columnas: clasificación Funcionamiento/Inversión, presupuesto inicial, modificaciones (ampliación,
    disminución, traspasos), presupuesto definitivo, obligaciones contraídas / pagadas / pendientes por fondo 11, 12 y otros.
    """
    programas_raiz = CuentaPresupuestaria.objects.filter(
        empresa=empresa, tipo_presupuesto="EGRESO", nivel=1, is_active=True
    ).order_by("codigo")

    filas = []
    totales = {
        "presupuesto_inicial": Decimal("0.00"),
        "modificaciones_aprobadas": Decimal("0.00"),
        "traspasos": Decimal("0.00"),
        "ampliacion": Decimal("0.00"),
        "disminucion": Decimal("0.00"),
        "presupuesto_definitivo": Decimal("0.00"),
        "obl_contraidas": {**_triple_fondo(), "de_mas": Decimal("0.00"), "de_menos": Decimal("0.00")},
        "obl_pagadas": _triple_fondo(),
        "obl_pendientes": _triple_fondo(),
    }

    todas_reformas = list(
        ReformaPresupuestaria.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True).select_related(
            "cuenta_destino", "cuenta_origen"
        )
    )

    for prog in programas_raiz:
        ids = _ids_arbol_cuenta(empresa, prog)
        cod = (prog.codigo or "").strip()

        pa_agg = PresupuestoAnual.objects.filter(
            empresa=empresa, ejercicio_id=ejercicio_id, cuenta_id__in=ids
        ).aggregate(ini=Sum("monto_inicial"), net_ref=Sum("monto_reformas"))
        inicial = pa_agg["ini"] or Decimal("0.00")
        modificaciones_aprobadas = pa_agg["net_ref"] or Decimal("0.00")
        definitivo = inicial + modificaciones_aprobadas

        ampliacion = Decimal("0.00")
        disminucion = Decimal("0.00")
        trasp_entrada = Decimal("0.00")
        trasp_salida = Decimal("0.00")

        for r in todas_reformas:
            t = r.tipo or ""
            if t == "AMPLIACION" and r.cuenta_destino_id and r.cuenta_destino_id in ids:
                ampliacion += r.monto or Decimal("0.00")
            elif t == "REDUCCION" and r.cuenta_destino_id and r.cuenta_destino_id in ids:
                disminucion += r.monto or Decimal("0.00")
            elif t == "TRASPASO":
                if r.cuenta_destino_id and r.cuenta_destino_id in ids:
                    trasp_entrada += r.monto or Decimal("0.00")
                if r.cuenta_origen_id and r.cuenta_origen_id in ids:
                    trasp_salida += r.monto or Decimal("0.00")

        traspasos_net = trasp_entrada - trasp_salida

        base_det = OrdenPagoDetalle.objects.filter(
            orden_pago__empresa=empresa,
            orden_pago__ejercicio_id=ejercicio_id,
            cuenta_presupuestaria_id__in=ids,
        ).exclude(orden_pago__estado="ANULADA")

        def agg_por_estados(estados):
            trip = _triple_fondo()
            qs = base_det.filter(orden_pago__estado__in=estados).select_related("fondo")
            for det in qs:
                b = _fondo_bucket_f11_f12_otros(det.fondo)
                key = b if b in ("f11", "f12") else "otros"
                trip[key] += det.monto or Decimal("0.00")
            return trip

        obl_contra = agg_por_estados(["APROBADA", "PAGADA"])
        obl_pag = agg_por_estados(["PAGADA"])
        obl_pend = agg_por_estados(["APROBADA"])

        cod3 = cod[:3] if len(cod) >= 3 else cod
        es_func = cod3.startswith("1")
        es_inv = cod3.startswith("2") or cod3.startswith("3")

        filas.append(
            {
                "codigo": cod,
                "descripcion": prog.nombre,
                "es_funcionamiento": es_func,
                "es_inversion": es_inv,
                "presupuesto_inicial": inicial,
                "modificaciones_aprobadas": modificaciones_aprobadas,
                "traspasos": traspasos_net,
                "ampliacion": ampliacion,
                "disminucion": disminucion,
                "presupuesto_definitivo": definitivo,
                "obl_contraidas": {
                    "de_mas": Decimal("0.00"),
                    "de_menos": Decimal("0.00"),
                    **obl_contra,
                },
                "obl_pagadas": obl_pag,
                "obl_pendientes": obl_pend,
            }
        )

        totales["presupuesto_inicial"] += inicial
        totales["modificaciones_aprobadas"] += modificaciones_aprobadas
        totales["traspasos"] += traspasos_net
        totales["ampliacion"] += ampliacion
        totales["disminucion"] += disminucion
        totales["presupuesto_definitivo"] += definitivo
        _sumar_triple(totales["obl_contraidas"], obl_contra)
        _sumar_triple(totales["obl_pagadas"], obl_pag)
        _sumar_triple(totales["obl_pendientes"], obl_pend)

    egreso_simple = calcular_ejecucion_presupuestaria(empresa, ejercicio_id, "EGRESO")
    por_codigo = {str(r.get("codigo") or ""): r for r in egreso_simple if r.get("nivel") == 1}
    for f in filas:
        r0 = por_codigo.get(f["codigo"], {})
        f["ejecutado_op"] = r0.get("ejecutado") or Decimal("0.00")
        f["porcentaje_ejec"] = r0.get("porcentaje") or 0

    return {"filas": filas, "totales": totales}


def forma01_liquidacion_ingresos(empresa, ejercicio_id):
    """
    Forma 01 TSC — Liquidación del presupuesto de ingresos.
    Por línea de cuenta: presupuesto inicial; modificaciones aprobadas (detalle ampliación, disminución, traspasos neto);
    presupuesto definitivo; ingresos devengados (solo ejecución presupuestaria); ingresos recaudados (EP + operaciones manuales);
    ingresos pendientes de cobro.
    """
    base = calcular_ejecucion_presupuestaria(empresa, ejercicio_id, "INGRESO")
    todas_reformas = list(
        ReformaPresupuestaria.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True).select_related(
            "cuenta_destino", "cuenta_origen"
        )
    )

    totales = {
        "presupuesto_inicial": Decimal("0.00"),
        "modificaciones_aprobadas": Decimal("0.00"),
        "ampliacion": Decimal("0.00"),
        "disminucion": Decimal("0.00"),
        "traspasos": Decimal("0.00"),
        "presupuesto_definitivo": Decimal("0.00"),
        "ingresos_devengados": Decimal("0.00"),
        "ingresos_recaudados": Decimal("0.00"),
        "ingresos_pendientes": Decimal("0.00"),
    }

    filas = []
    for r in base:
        cod = str(r.get("codigo") or "").strip()
        cuenta = CuentaPresupuestaria.objects.filter(
            empresa=empresa, codigo=cod, tipo_presupuesto="INGRESO", is_active=True
        ).first()
        if not cuenta:
            continue

        ids = _ids_arbol_cuenta(empresa, cuenta)

        pa_agg = PresupuestoAnual.objects.filter(
            empresa=empresa, ejercicio_id=ejercicio_id, cuenta_id__in=ids
        ).aggregate(ini=Sum("monto_inicial"), net_ref=Sum("monto_reformas"))
        inicial = pa_agg["ini"] or Decimal("0.00")
        modificaciones_aprobadas = pa_agg["net_ref"] or Decimal("0.00")
        definitivo = inicial + modificaciones_aprobadas

        ampliacion = Decimal("0.00")
        disminucion = Decimal("0.00")
        trasp_entrada = Decimal("0.00")
        trasp_salida = Decimal("0.00")

        for rf in todas_reformas:
            t = rf.tipo or ""
            if t == "AMPLIACION" and rf.cuenta_destino_id and rf.cuenta_destino_id in ids:
                ampliacion += rf.monto or Decimal("0.00")
            elif t == "REDUCCION" and rf.cuenta_destino_id and rf.cuenta_destino_id in ids:
                disminucion += rf.monto or Decimal("0.00")
            elif t == "TRASPASO":
                if rf.cuenta_destino_id and rf.cuenta_destino_id in ids:
                    trasp_entrada += rf.monto or Decimal("0.00")
                if rf.cuenta_origen_id and rf.cuenta_origen_id in ids:
                    trasp_salida += rf.monto or Decimal("0.00")

        traspasos_net = trasp_entrada - trasp_salida

        ep = (
            EjecucionPresupuestaria.objects.filter(
                empresa=empresa, ejercicio_id=ejercicio_id, cuenta_presupuestaria_id__in=ids
            ).aggregate(t=Sum("monto"))["t"]
            or Decimal("0.00")
        )
        om = (
            OperacionManual.objects.filter(
                empresa=empresa, ejercicio_id=ejercicio_id, tipo="INGRESO", cuenta_id__in=ids
            ).aggregate(t=Sum("monto"))["t"]
            or Decimal("0.00")
        )
        recaudados = ep + om
        devengados = ep
        pendientes = definitivo - recaudados

        filas.append(
            {
                "codigo": cod,
                "nombre": r.get("nombre") or "",
                "nivel": r.get("nivel") or 1,
                "presupuesto_inicial": inicial,
                "modificaciones_aprobadas": modificaciones_aprobadas,
                "ampliacion": ampliacion,
                "disminucion": disminucion,
                "traspasos": traspasos_net,
                "presupuesto_definitivo": definitivo,
                "ingresos_devengados": devengados,
                "ingresos_recaudados": recaudados,
                "ingresos_pendientes": pendientes,
                "porcentaje": r.get("porcentaje") or 0,
            }
        )

        totales["presupuesto_inicial"] += inicial
        totales["modificaciones_aprobadas"] += modificaciones_aprobadas
        totales["ampliacion"] += ampliacion
        totales["disminucion"] += disminucion
        totales["traspasos"] += traspasos_net
        totales["presupuesto_definitivo"] += definitivo
        totales["ingresos_devengados"] += devengados
        totales["ingresos_recaudados"] += recaudados
        totales["ingresos_pendientes"] += pendientes

    return {"filas": filas, "totales": totales}


def forma03_liquidacion_egresos_consolidado(empresa, ejercicio_id):
    """
    Forma 03 TSC — Liquidación del presupuesto de egresos consolidado (grupos 100, 200, 300, otros).
    Por grupo: presupuesto vigente y ejecución por fondo 11, 12, ERP y otros;
    obligaciones contraídas (De más / De menos reservados + detalle por fondo), pagadas y pendientes.
    """
    programas = liquidacion_egresos_por_programa(empresa, ejercicio_id)
    labels = {
        "100": "Grupo 100",
        "200": "Grupo 200",
        "300": "Grupo 300",
        "OTROS": "Otros",
    }
    grupos_order = ("100", "200", "300", "OTROS")

    filas = []
    totales = {
        "total_vigente": Decimal("0.00"),
        "ejecutado": Decimal("0.00"),
        "saldo": Decimal("0.00"),
        "vigente": _quad_fondo(),
        "ejecutado_por_fondo": _quad_fondo(),
        "obl_contraidas": {**_quad_fondo(), "de_mas": Decimal("0.00"), "de_menos": Decimal("0.00")},
        "obl_pagadas": _quad_fondo(),
        "obl_pendientes": _quad_fondo(),
    }

    for gkey in grupos_order:
        ids = set()
        for p in programas:
            cod = str(p.get("codigo") or "")
            pref = cod[:3] if len(cod) >= 3 else cod
            key = pref if pref in ("100", "200", "300") else "OTROS"
            if key != gkey:
                continue
            cuenta = CuentaPresupuestaria.objects.filter(
                empresa=empresa, codigo=cod.strip(), tipo_presupuesto="EGRESO", is_active=True
            ).first()
            if cuenta:
                ids |= _ids_arbol_cuenta(empresa, cuenta)

        vigente_quad = _quad_fondo()
        if ids:
            for pa in PresupuestoAnual.objects.filter(
                empresa=empresa, ejercicio_id=ejercicio_id, cuenta_id__in=ids
            ).select_related("fondo"):
                m = (pa.monto_inicial or Decimal("0.00")) + (pa.monto_reformas or Decimal("0.00"))
                b = _fondo_bucket_f11_f12_erp_otros(pa.fondo)
                vigente_quad[b] += m

        ejecutado_quad = _quad_fondo()
        if ids:
            for ep in EjecucionPresupuestaria.objects.filter(
                empresa=empresa, ejercicio_id=ejercicio_id, cuenta_presupuestaria_id__in=ids
            ).select_related("fondo"):
                b = _fondo_bucket_f11_f12_erp_otros(ep.fondo)
                ejecutado_quad[b] += ep.monto or Decimal("0.00")
            for om in OperacionManual.objects.filter(
                empresa=empresa, ejercicio_id=ejercicio_id, tipo="EGRESO", cuenta_id__in=ids
            ).select_related("fondo"):
                b = _fondo_bucket_f11_f12_erp_otros(om.fondo)
                ejecutado_quad[b] += om.monto or Decimal("0.00")

        total_vigente = sum(vigente_quad.values())
        total_ejecutado = sum(ejecutado_quad.values())
        saldo = total_vigente - total_ejecutado
        pct = (total_ejecutado / total_vigente * 100) if total_vigente > 0 else 0

        base_det = OrdenPagoDetalle.objects.filter(
            orden_pago__empresa=empresa,
            orden_pago__ejercicio_id=ejercicio_id,
            cuenta_presupuestaria_id__in=ids,
        ).exclude(orden_pago__estado="ANULADA")

        def agg_quad_estados(estados):
            q = _quad_fondo()
            qs = base_det.filter(orden_pago__estado__in=estados).select_related("fondo")
            for det in qs:
                b = _fondo_bucket_f11_f12_erp_otros(det.fondo)
                q[b] += det.monto or Decimal("0.00")
            return q

        ac = agg_quad_estados(["APROBADA", "PAGADA"])
        obl_contraidas = {
            "de_mas": Decimal("0.00"),
            "de_menos": Decimal("0.00"),
            **ac,
        }
        obl_pagadas = agg_quad_estados(["PAGADA"])
        obl_pendientes = agg_quad_estados(["APROBADA"])

        filas.append(
            {
                "grupo": gkey,
                "nombre": labels[gkey],
                "total_vigente": total_vigente,
                "vigente_por_fondo": vigente_quad,
                "ejecutado": total_ejecutado,
                "ejecutado_por_fondo": ejecutado_quad,
                "saldo": saldo,
                "porcentaje": pct,
                "obl_contraidas": obl_contraidas,
                "obl_pagadas": obl_pagadas,
                "obl_pendientes": obl_pendientes,
            }
        )

        totales["total_vigente"] += total_vigente
        totales["ejecutado"] += total_ejecutado
        totales["saldo"] += saldo
        for k in vigente_quad:
            totales["vigente"][k] += vigente_quad[k]
        for k in ejecutado_quad:
            totales["ejecutado_por_fondo"][k] += ejecutado_quad[k]
        totales["obl_contraidas"]["de_mas"] += obl_contraidas["de_mas"]
        totales["obl_contraidas"]["de_menos"] += obl_contraidas["de_menos"]
        for k in ("f11", "f12", "erp", "otros"):
            totales["obl_contraidas"][k] += obl_contraidas[k]
            totales["obl_pagadas"][k] += obl_pagadas[k]
            totales["obl_pendientes"][k] += obl_pendientes[k]

    return {"filas": filas, "totales": totales}


def liquidacion_egresos_por_programa(empresa, ejercicio_id):
    """
    Liquidación de egresos por cada 'programa'.
    En ausencia de un catálogo explícito de programas, se interpreta como las cuentas EGRESO de nivel 1
    (estructura organizacional) y se agregan montos de sus subcuentas.
    """
    egresos = calcular_ejecucion_presupuestaria(empresa, ejercicio_id, "EGRESO")
    programas = [r for r in egresos if r.get("nivel") == 1]
    return programas


def liquidacion_egresos_consolidado_por_grupo(empresa, ejercicio_id):
    """
    Resumen consolidado de programas por grupo: 100, 200, 300 y otros.
    Se agrupa usando el prefijo del código presupuestario a 3 dígitos.
    """
    programas = liquidacion_egresos_por_programa(empresa, ejercicio_id)
    buckets = {
        "100": {"grupo": "100", "nombre": "Grupo 100", "total_vigente": Decimal("0.00"), "ejecutado": Decimal("0.00")},
        "200": {"grupo": "200", "nombre": "Grupo 200", "total_vigente": Decimal("0.00"), "ejecutado": Decimal("0.00")},
        "300": {"grupo": "300", "nombre": "Grupo 300", "total_vigente": Decimal("0.00"), "ejecutado": Decimal("0.00")},
        "OTROS": {"grupo": "OTROS", "nombre": "Otros", "total_vigente": Decimal("0.00"), "ejecutado": Decimal("0.00")},
    }
    for p in programas:
        codigo = str(p.get("codigo") or "")
        pref = codigo[:3]
        key = pref if pref in ("100", "200", "300") else "OTROS"
        buckets[key]["total_vigente"] += p.get("total_aprobado") or Decimal("0.00")
        buckets[key]["ejecutado"] += p.get("ejecutado") or Decimal("0.00")

    filas = []
    for key in ("100", "200", "300", "OTROS"):
        fila = buckets[key]
        fila["saldo"] = fila["total_vigente"] - fila["ejecutado"]
        fila["porcentaje"] = (fila["ejecutado"] / fila["total_vigente"] * 100) if fila["total_vigente"] > 0 else 0
        filas.append(fila)
    return filas


def detalle_op_con_montos(empresa, ejercicio_id):
    ops = OrdenPago.objects.filter(empresa=empresa, ejercicio_id=ejercicio_id, is_active=True).order_by(
        "-fecha"
    )
    out = []
    for op in ops:
        dets = OrdenPagoDetalle.objects.filter(orden_pago=op).select_related(
            "cuenta_presupuestaria", "fondo"
        )
        out.append({"orden": op, "detalles": list(dets)})
    return out

# -*- coding: utf-8 -*-
"""Vistas del paquete de rendición de cuentas (14 formas)."""
from datetime import date

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.db.utils import ProgrammingError, OperationalError

from contabilidad.models import EjercicioFiscal
from core.models import Municipio

from .rendicion_registry import (
    FORMAS_IAIP,
    FORMAS_RENDICION,
    get_forma_by_index,
    get_iaip_by_index,
)
from .rendicion_services import (
    calcular_ejecucion_presupuestaria,
    balance_general_a_fecha,
    balance_general_comparativo,
    detalle_op_con_montos,
    forma01_liquidacion_ingresos,
    forma02_liquidacion_egresos_por_programa,
    forma03_liquidacion_egresos_consolidado,
    forma04_liquidacion_presupuesto,
    forma05_arqueo_caja_general,
    liquidacion_egresos_por_programa,
    listado_proyectos,
    forma07_cuenta_tesoreria,
    tabla_ejecucion_mensual,
    totales_ingresos_egresos,
    totales_por_fondo,
    reformas_ampliaciones,
    reformas_ampliaciones_disminuciones_detalle,
    reformas_reducciones_y_traspasos,
)
from .views import get_empresa, verificar_sesion


def _firmas_forma04(empresa, ajustes_f04=None):
    """Nombres para firmas: por defecto tabla Municipio (alcalde, tesorero/tesorera, contador); ajustes solo sobrescriben si se capturan."""
    try:
        m = Municipio.objects.filter(codigo=(empresa or "").strip()).first()
    except Exception:
        m = None

    def pick(*vals):
        for v in vals:
            if v is not None and str(v).strip():
                return str(v).strip()
        return ""

    return {
        "alcalde": pick(
            getattr(m, "alcalde", None) if m else None,
            getattr(ajustes_f04, "alcalde_nombre", None) if ajustes_f04 else None,
        ),
        "tesorero": pick(
            getattr(m, "tesorero", None) if m else None,
            getattr(m, "tesorera", None) if m else None,
            getattr(ajustes_f04, "tesorero_nombre", None) if ajustes_f04 else None,
        ),
        "contador": pick(
            getattr(m, "contador", None) if m else None,
            getattr(ajustes_f04, "contador_nombre", None) if ajustes_f04 else None,
        ),
    }


def _empresa_label(codigo):
    codigo = (codigo or "").strip()
    if not codigo:
        return ""
    try:
        m = Municipio.objects.filter(codigo=codigo).first()
        if m and m.descripcion:
            return f"{m.descripcion.strip()} ({codigo})"
    except Exception:
        pass
    return codigo


def rendicion_cuentas_hub(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    empresa = get_empresa(request)
    empresa_label = _empresa_label(empresa)
    ejercicios = EjercicioFiscal.objects.all().order_by("-anio")
    ejercicio_id = request.GET.get("ejercicio") or (str(ejercicios.first().id) if ejercicios.exists() else "")
    # Agrupar formas por categoría interna
    categorias = {}
    for f in FORMAS_RENDICION:
        categorias.setdefault(f["categoria"], []).append(f)

    return render(
        request,
        "presupuestos/rendicion/hub.html",
        {
            "modulo": "Rendición de cuentas",
            "descripcion": "Rendición TSC y transparencia IAIP (referencia Honduras)",
            "titulo": "Rendición de cuentas y transparencia",
            "empresa": empresa,
            "empresa_label": empresa_label,
            "usuario": request.session.get("nombre", ""),
            "ejercicios": ejercicios,
            "ejercicio_id": ejercicio_id,
            "formas": FORMAS_RENDICION,
            "formas_iaip": FORMAS_IAIP,
            "categorias": categorias,
            "hoy": date.today(),
            "nota_normativa": (
                "Las presentaciones oficiales ante el Tribunal Superior de Cuentas (TSC) y las obligaciones de "
                "transparencia ante el IAIP deben ajustarse a formatos, circulares y plazos vigentes. Los informes "
                "de la Contraloría General de la República (CGR) están en el módulo Contabilidad. "
                "Este apartado genera informes a partir de los catálogos y movimientos registrados en SIMAFI."
            ),
        },
    )


def rendicion_forma(request, num: int):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    forma = get_forma_by_index(num)
    if not forma:
        raise Http404("Forma no disponible")

    ejercicio_id = request.GET.get("ejercicio")
    if not ejercicio_id:
        messages.warning(request, "Seleccione un ejercicio fiscal para generar la forma.")
        return redirect("presupuestos:rendicion_cuentas_hub")

    ejercicio = get_object_or_404(EjercicioFiscal, pk=ejercicio_id)
    empresa = get_empresa(request)
    empresa_label = _empresa_label(empresa)

    # Captura/actualización de ajustes para Forma 07 (extrapresupuestarios + firmas)
    if num == 7 and request.method == "POST":
        from decimal import Decimal
        from .models import RendicionForma07Ajuste

        def _dec(val):
            try:
                return Decimal(str(val or "0")).quantize(Decimal("0.01"))
            except Exception:
                return Decimal("0.00")

        RendicionForma07Ajuste.objects.update_or_create(
            empresa=empresa,
            ejercicio=ejercicio,
            defaults={
                "entradas_extra_efectivo": _dec(request.POST.get("entradas_extra_efectivo")),
                "entradas_extra_bancos": _dec(request.POST.get("entradas_extra_bancos")),
                "pagos_extra_efectivo": _dec(request.POST.get("pagos_extra_efectivo")),
                "pagos_extra_bancos": _dec(request.POST.get("pagos_extra_bancos")),
                "alcalde_nombre": (request.POST.get("alcalde_nombre") or "").strip()[:200] or None,
                "tesorero_nombre": (request.POST.get("tesorero_nombre") or "").strip()[:200] or None,
                "contador_nombre": (request.POST.get("contador_nombre") or "").strip()[:200] or None,
            },
        )
        messages.success(request, "Ajustes de Forma 07 guardados.")
        return redirect("presupuestos:rendicion_forma", num=7)

    if num == 4 and request.method == "POST":
        from decimal import Decimal
        from django.urls import reverse

        from .models import RendicionForma04Ajuste

        def _dec(val):
            try:
                return Decimal(str(val or "0")).quantize(Decimal("0.01"))
            except Exception:
                return Decimal("0.00")

        try:
            RendicionForma04Ajuste.objects.update_or_create(
                empresa=empresa,
                ejercicio=ejercicio,
                defaults={
                    "ajuste_por_ingreso": _dec(request.POST.get("ajuste_por_ingreso")),
                    "ajuste_por_egreso": _dec(request.POST.get("ajuste_por_egreso")),
                    "alcalde_nombre": (request.POST.get("alcalde_nombre") or "").strip()[:200] or None,
                    "tesorero_nombre": (request.POST.get("tesorero_nombre") or "").strip()[:200] or None,
                    "contador_nombre": (request.POST.get("contador_nombre") or "").strip()[:200] or None,
                },
            )
            messages.success(request, "Datos de la Forma 04 guardados.")
        except (ProgrammingError, OperationalError):
            messages.warning(
                request,
                "No existe la tabla de ajustes de la Forma 04. Ejecute migraciones de Presupuestos (presu_rendicion_f04_ajuste).",
            )
        url = reverse("presupuestos:rendicion_forma", kwargs={"num": 4}) + f"?ejercicio={ejercicio.id}"
        return redirect(url)

    if num == 5 and request.method == "POST":
        from decimal import Decimal
        from django.urls import reverse

        from .models import RendicionForma05Ajuste, RendicionForma05SalidaManual

        def _dec(val):
            try:
                return Decimal(str(val or "0")).quantize(Decimal("0.01"))
            except Exception:
                return Decimal("0.00")

        def _redirect_f05():
            fc = parse_date(request.POST.get("fecha_hasta_redirect") or "") or ejercicio.fecha_fin
            if fc < ejercicio.fecha_inicio:
                fc = ejercicio.fecha_inicio
            if fc > ejercicio.fecha_fin:
                fc = ejercicio.fecha_fin
            url = (
                reverse("presupuestos:rendicion_forma", kwargs={"num": 5})
                + f"?ejercicio={ejercicio.id}&fecha_hasta={fc.isoformat()}"
            )
            return redirect(url)

        action = (request.POST.get("action") or "").strip()
        try:
            if action == "save_f05_ajustes":
                RendicionForma05Ajuste.objects.update_or_create(
                    empresa=empresa,
                    ejercicio=ejercicio,
                    defaults={
                        "extra_entradas_efectivo": _dec(request.POST.get("extra_entradas_efectivo")),
                        "extra_salidas_efectivo": _dec(request.POST.get("extra_salidas_efectivo")),
                        "extra_cheques": _dec(request.POST.get("extra_cheques")),
                        "alcalde_nombre": (request.POST.get("alcalde_nombre") or "").strip()[:200] or None,
                        "tesorero_nombre": (request.POST.get("tesorero_nombre") or "").strip()[:200] or None,
                        "contador_nombre": (request.POST.get("contador_nombre") or "").strip()[:200] or None,
                    },
                )
                messages.success(request, "Captura de Forma 05 guardada.")
                return _redirect_f05()
            if action == "add_f05_linea":
                fd = parse_date(request.POST.get("linea_fecha") or "")
                if not fd:
                    messages.error(request, "Indique la fecha del documento.")
                    return _redirect_f05()
                desc = (request.POST.get("linea_descripcion") or "").strip()
                if not desc:
                    messages.error(request, "Indique la descripción de la salida.")
                    return _redirect_f05()
                monto = _dec(request.POST.get("linea_monto"))
                if monto <= 0:
                    messages.error(request, "El monto debe ser mayor a cero.")
                    return _redirect_f05()
                RendicionForma05SalidaManual.objects.create(
                    empresa=empresa,
                    ejercicio=ejercicio,
                    fecha=fd,
                    descripcion=desc[:500],
                    documento=(request.POST.get("linea_documento") or "").strip()[:80],
                    monto=monto,
                )
                messages.success(request, "Salida manual agregada al informe.")
                return _redirect_f05()
            if action == "delete_f05_linea":
                lid = request.POST.get("line_id")
                if lid:
                    RendicionForma05SalidaManual.objects.filter(
                        pk=lid, empresa=empresa, ejercicio=ejercicio
                    ).delete()
                    messages.success(request, "Línea eliminada.")
                return _redirect_f05()
        except (ProgrammingError, OperationalError):
            messages.warning(
                request,
                "No existe la tabla de captura Forma 05. Ejecute migraciones de Presupuestos (presu_rendicion_f05_*).",
            )
            return _redirect_f05()

    if num == 6 and request.method == "POST":
        from django.urls import reverse

        from .models import RendicionForma06Captura

        if (request.POST.get("action") or "").strip() == "save_f06_captura":
            fd = parse_date(request.POST.get("fecha_arqueo") or "")
            try:
                RendicionForma06Captura.objects.update_or_create(
                    empresa=empresa,
                    ejercicio=ejercicio,
                    defaults={
                        "municipal_arqueo_nombre": (request.POST.get("municipal_arqueo_nombre") or "").strip()[:200],
                        "empleado_municipal_nombre": (request.POST.get("empleado_municipal_nombre") or "").strip()[:200],
                        "responsable_nombre": (request.POST.get("responsable_nombre") or "").strip()[:200],
                        "numero_arqueo": (request.POST.get("numero_arqueo") or "").strip()[:50] or None,
                        "fecha_arqueo": fd,
                    },
                )
                messages.success(request, "Datos de la Forma 06 guardados.")
            except (ProgrammingError, OperationalError):
                messages.warning(
                    request,
                    "No existe la tabla de captura Forma 06. Ejecute migraciones de Presupuestos (presu_rendicion_f06_captura).",
                )
            url = reverse("presupuestos:rendicion_forma", kwargs={"num": 6}) + f"?ejercicio={ejercicio.id}"
            return redirect(url)

    ctx = {
        "modulo": forma["codigo"] + " — " + forma["titulo"][:48],
        "descripcion": forma.get("normativa", "")[:120],
        "forma": forma,
        "forma_num": num,
        "ejercicio": ejercicio,
        "empresa": empresa,
        "empresa_label": empresa_label,
        "usuario": request.session.get("nombre", ""),
        "hoy": date.today(),
    }

    if num == 1:
        # Forma 01: Liquidación del Presupuesto de Ingresos (formato TSC)
        ctx["forma01"] = forma01_liquidacion_ingresos(empresa, ejercicio.id)
    elif num == 2:
        # Forma 02: Liquidación del Presupuesto de Egresos por cada Programa (formato TSC)
        ctx["forma02"] = forma02_liquidacion_egresos_por_programa(empresa, ejercicio.id)
        ctx["programas_egreso"] = liquidacion_egresos_por_programa(empresa, ejercicio.id)
    elif num == 3:
        # Forma 03: Liquidación del Presupuesto de Egresos Consolidado (formato TSC)
        ctx["forma03"] = forma03_liquidacion_egresos_consolidado(empresa, ejercicio.id)
        cemp = (empresa or "").strip()
        ctx["forma03_codigo_partes"] = [cemp[:2], cemp[2:4]] if len(cemp) >= 4 else [cemp, ""]
    elif num == 4:
        # Forma 04: Liquidación del Presupuesto (resultado presupuestario — TSC)
        from .models import RendicionForma04Ajuste

        try:
            ajustes_f04 = RendicionForma04Ajuste.objects.filter(empresa=empresa, ejercicio=ejercicio).first()
        except (ProgrammingError, OperationalError):
            ajustes_f04 = None
            messages.warning(
                request,
                "No existe la tabla de ajustes de la Forma 04. Ejecute migraciones de Presupuestos (presu_rendicion_f04_ajuste).",
            )
        ctx["forma04"] = forma04_liquidacion_presupuesto(empresa, ejercicio.id, ajustes=ajustes_f04)
        ctx["ajustes_f04"] = ajustes_f04
        ctx["forma04_firmas"] = _firmas_forma04(empresa, ajustes_f04)
        cemp = (empresa or "").strip()
        ctx["forma04_codigo_partes"] = [cemp[:2], cemp[2:4]] if len(cemp) >= 4 else [cemp, ""]
    elif num == 5:
        # Forma 05: Arqueo de Caja General (TSC) + captura manual
        from .models import RendicionForma05Ajuste, RendicionForma05SalidaManual

        fecha_corte = parse_date(request.GET.get("fecha_hasta") or "") or ejercicio.fecha_fin
        if fecha_corte < ejercicio.fecha_inicio:
            fecha_corte = ejercicio.fecha_inicio
        if fecha_corte > ejercicio.fecha_fin:
            fecha_corte = ejercicio.fecha_fin
        ctx["fecha_hasta"] = fecha_corte
        try:
            ajustes_f05 = RendicionForma05Ajuste.objects.filter(empresa=empresa, ejercicio=ejercicio).first()
            salidas_manuales = RendicionForma05SalidaManual.objects.filter(
                empresa=empresa, ejercicio=ejercicio
            ).order_by("orden", "fecha", "id")
        except (ProgrammingError, OperationalError):
            ajustes_f05 = None
            salidas_manuales = []
            messages.warning(
                request,
                "No existe la tabla de captura Forma 05. Ejecute migraciones de Presupuestos (presu_rendicion_f05_*).",
            )
        ctx["ajustes_f05"] = ajustes_f05
        ctx["f05_salidas_manuales_todas"] = salidas_manuales
        ctx["forma05"] = forma05_arqueo_caja_general(
            empresa,
            ejercicio,
            fecha_hasta=fecha_corte,
            ajustes_f05=ajustes_f05,
            salidas_manuales_qs=salidas_manuales,
        )
        ctx["forma05_firmas"] = _firmas_forma04(empresa, ajustes_f05)
        cemp = (empresa or "").strip()
        ctx["forma05_codigo_partes"] = [cemp[:2], cemp[2:4]] if len(cemp) >= 4 else [cemp, ""]
    elif num == 6:
        # Forma 06: Arqueo de Caja Chica o Fondo Rotatorio (declaración y firmas TSC)
        from .models import RendicionForma06Captura

        try:
            forma06_captura = RendicionForma06Captura.objects.filter(empresa=empresa, ejercicio=ejercicio).first()
        except (ProgrammingError, OperationalError):
            forma06_captura = None
            messages.warning(
                request,
                "No existe la tabla de captura Forma 06. Ejecute migraciones de Presupuestos (presu_rendicion_f06_captura).",
            )
        ctx["forma06_captura"] = forma06_captura
        cemp = (empresa or "").strip()
        ctx["forma06_codigo_partes"] = [cemp[:2], cemp[2:4]] if len(cemp) >= 4 else [cemp, ""]
    elif num == 7:
        # Forma 07: Cuenta de Tesorería (TSC)
        from .models import RendicionForma07Ajuste

        try:
            ajustes = RendicionForma07Ajuste.objects.filter(empresa=empresa, ejercicio=ejercicio).first()
        except (ProgrammingError, OperationalError):
            ajustes = None
            messages.warning(
                request,
                "No existe la tabla de ajustes de la Forma 07. Ejecute migraciones de Presupuestos para habilitar "
                "captura de extrapresupuestarios y firmas (presu_rendicion_f07_ajuste).",
            )
        ctx["ajustes_f07"] = ajustes
        fecha_corte = parse_date(request.GET.get("fecha_hasta") or "") or ejercicio.fecha_fin
        if fecha_corte < ejercicio.fecha_inicio:
            fecha_corte = ejercicio.fecha_inicio
        if fecha_corte > ejercicio.fecha_fin:
            fecha_corte = ejercicio.fecha_fin
        ctx["fecha_hasta"] = fecha_corte
        ctx["forma07"] = forma07_cuenta_tesoreria(empresa, ejercicio, fecha_hasta=fecha_corte, ajustes=ajustes)
    elif num == 8:
        # Forma 08: Control de Financiamiento (pendiente de captura/datos)
        ctx["pendiente_manual"] = True
    elif num == 9:
        # Forma 09: Control de Bienes Muebles e Inmuebles
        # En este sistema la fuente oficial está en el módulo de Activos (Contabilidad → Activos Fijos).
        from django.urls import reverse
        url = reverse("contabilidad:activos_fijos")
        return redirect(url)
    elif num == 10:
        # Forma 10: Informe Anual de Proyectos (usa catálogo de proyectos existente)
        ctx["proyectos"] = listado_proyectos(empresa, ejercicio.id)
    elif num == 11:
        # Forma 11 (oficial): Estado de Ingresos y Egresos
        ctx["estado_ie"] = totales_ingresos_egresos(empresa, ejercicio.id)
    elif num == 12:
        # Forma 12 (oficial): Balance General (al 31 de diciembre)
        fecha_corte = ejercicio.fecha_fin
        ctx["fecha_corte"] = fecha_corte
        ctx["balance"] = balance_general_a_fecha(empresa, ejercicio.id, fecha_corte)
    elif num == 13:
        # Forma 13 (oficial): Estado de Ingresos y Egresos Comparativos (año actual vs anterior)
        ejercicio_anterior = EjercicioFiscal.objects.filter(empresa=empresa, anio=ejercicio.anio - 1).first()
        ctx["ejercicio_anterior"] = ejercicio_anterior
        actual = totales_ingresos_egresos(empresa, ejercicio.id)
        anterior = totales_ingresos_egresos(empresa, ejercicio_anterior.id) if ejercicio_anterior else None
        delta_ing = (actual["ingresos_recaudados"] or 0) - ((anterior or {}).get("ingresos_recaudados") or 0)
        delta_eg = (actual["egresos_ejecutados"] or 0) - ((anterior or {}).get("egresos_ejecutados") or 0)
        delta_net = (actual["superavit_deficit"] or 0) - ((anterior or {}).get("superavit_deficit") or 0)
        ctx["comparativo_ie"] = {
            "actual": actual,
            "anterior": anterior or {"ingresos_recaudados": 0, "egresos_ejecutados": 0, "superavit_deficit": 0},
            "variacion": {"ingresos": delta_ing, "egresos": delta_eg, "neto": delta_net},
        }
        if not ejercicio_anterior:
            messages.warning(request, "No se encontró el ejercicio fiscal anterior para comparación.")
    elif num == 14:
        # Forma 14 (oficial): Balances Generales Comparativos (monetario y %)
        ejercicio_anterior = EjercicioFiscal.objects.filter(empresa=empresa, anio=ejercicio.anio - 1).first()
        ctx["ejercicio_anterior"] = ejercicio_anterior
        if ejercicio_anterior:
            fecha_corte_actual = ejercicio.fecha_fin
            fecha_corte_anterior = ejercicio_anterior.fecha_fin
            ctx["fecha_corte"] = fecha_corte_actual
            ctx["fecha_corte_anterior"] = fecha_corte_anterior
            ctx["balance_comp"] = balance_general_comparativo(
                empresa, ejercicio, ejercicio_anterior, fecha_corte_actual, fecha_corte_anterior
            )
        else:
            messages.warning(request, "No se encontró el ejercicio fiscal anterior para comparación.")
    else:
        raise Http404()

    return render(request, "presupuestos/rendicion/forma_detalle.html", ctx)


def _ejercicio_o_redirect(request):
    ejercicio_id = request.GET.get("ejercicio")
    if not ejercicio_id:
        messages.warning(request, "Seleccione un ejercicio fiscal para generar la forma.")
        return None, redirect("presupuestos:rendicion_cuentas_hub")
    ejercicio = get_object_or_404(EjercicioFiscal, pk=ejercicio_id)
    return ejercicio, None


def rendicion_iaip_forma(request, num: int):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    forma = get_iaip_by_index(num)
    if not forma:
        raise Http404("Formato IAIP no disponible")

    ejercicio, redir = _ejercicio_o_redirect(request)
    if redir:
        return redir
    empresa = get_empresa(request)
    empresa_label = _empresa_label(empresa)
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    ctx = {
        "modulo": forma["codigo"] + " — " + forma["titulo"][:42],
        "descripcion": forma.get("normativa", "")[:120],
        "paquete": "iaip",
        "forma": forma,
        "forma_num": num,
        "ejercicio": ejercicio,
        "empresa": empresa,
        "empresa_label": empresa_label,
        "usuario": request.session.get("nombre", ""),
        "hoy": date.today(),
    }

    if num == 1:
        ctx["es_portada"] = True
    elif num == 2:
        ctx["ingresos"] = calcular_ejecucion_presupuestaria(empresa, ejercicio.id, "INGRESO", solo_nivel_2=True)
        ctx["egresos"] = calcular_ejecucion_presupuestaria(empresa, ejercicio.id, "EGRESO", solo_nivel_2=True)
    elif num == 3:
        # Traspasos: se muestran en ambos criterios:
        # - como disminución en la cuenta ORIGEN
        # - como ampliación en la cuenta DESTINO
        ampliaciones = list(reformas_ampliaciones(empresa, ejercicio.id))
        red_y_tras = list(reformas_reducciones_y_traspasos(empresa, ejercicio.id))

        disminuciones_rows = []
        ampliaciones_rows = []

        for r in ampliaciones:
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

        for r in red_y_tras:
            if getattr(r, "tipo", "") == "REDUCCION":
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
            elif getattr(r, "tipo", "") == "TRASPASO":
                # Disminución en origen
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
                # Ampliación en destino
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

        # Ordenar por fecha/ref para lectura
        disminuciones_rows.sort(key=lambda x: (x["fecha"], x["referencia"] or ""))
        ampliaciones_rows.sort(key=lambda x: (x["fecha"], x["referencia"] or ""))

        ctx["reformas_ampliaciones"] = ampliaciones_rows
        ctx["reformas_disminuciones"] = disminuciones_rows
    elif num == 4:
        ctx["fondos_ingreso"] = totales_por_fondo(empresa, ejercicio.id, "INGRESO")
        ctx["fondos_egreso"] = totales_por_fondo(empresa, ejercicio.id, "EGRESO")
    elif num == 5:
        ctx["ordenes"] = detalle_op_con_montos(empresa, ejercicio.id)
    elif num == 6:
        ctx["proyectos"] = listado_proyectos(empresa, ejercicio.id)
    elif num == 7:
        ctx["operaciones"] = operaciones_manuales_todas(empresa, ejercicio.id)
    elif num == 8:
        ctx["es_indice"] = True
    else:
        raise Http404()

    ctx["meses_nombres"] = meses
    return render(request, "presupuestos/rendicion/transparencia_paquete.html", ctx)


def redirect_cgr_a_contabilidad(request, num: int):
    """Redirección: los informes CGR pasaron al módulo Contabilidad."""
    from django.urls import reverse

    url = reverse("contabilidad:cgr_informe_forma", kwargs={"num": num})
    q = request.GET.urlencode()
    if q:
        url += "?" + q
    return redirect(url)

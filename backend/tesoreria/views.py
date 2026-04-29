from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from decimal import Decimal
from datetime import date, datetime
import json
import csv
import io
import base64
import logging
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Trim
from django.db import transaction, connection

from contabilidad.models import CuentaContable
from .models import (
    CuentaTesoreria,
    PagoTesoreria,
    PagoDetalleOrden,
    DepositoTesoreria,
    NotaTesoreria,
    ConciliacionBancaria,
    DetalleConciliacion,
    CobroCaja,
    CobroCajaMetodo,
)
from .forms import CuentaTesoreriaForm, PagoTesoreriaForm, DepositoTesoreriaForm, NotaTesoreriaForm, ConciliacionBancariaForm
from presupuestos.models import OrdenPago
from tributario.models import PagoVariosTemp, NoRecibos, TransaccionesIcs, TransaccionesBienesInmuebles, Negocio
from core.pg_sequence import sync_postgres_serial_to_max_id
import qrcode

logger = logging.getLogger(__name__)


def _safe_decimal(value, default="0.00"):
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal(default)


def _empresa_codigo_transacciones(empresa: str) -> str:
    """`transaccionesics` y `transaccionesbienesinmuebles` almacenan empresa en 4 chars; sesión/pagovariostemp puede traer más."""
    e = (empresa or "").strip()
    return e[:4] if e else ""


def _norm_rubro_caja(rubro: str) -> str:
    return (rubro or "").strip().upper()[:6]


def _table_exists(table_name):
    try:
        return table_name in connection.introspection.table_names()
    except Exception:
        return False


def _create_cobro_caja_with_id_fallback(**payload):
    """Si en Postgres falta DEFAULT/seq en `teso_cobro_caja.id`, asignar id manualmente."""
    try:
        return CobroCaja.objects.create(**payload)
    except Exception as exc:
        err = str(exc).lower()
        if "null value" in err and "id" in err and "teso_cobro_caja" in err:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM teso_cobro_caja")
                    next_id = int(cursor.fetchone()[0])
                payload = {**payload, "id": next_id}
                obj = CobroCaja.objects.create(**payload)
            logger.warning(
                "Fallback teso_cobro_caja.id manual (%s) — ejecute migración 0006 o repare secuencia en BD.",
                next_id,
            )
            return obj
        raise


def _create_cobro_caja_metodo_with_id_fallback(**payload):
    """Si en Postgres falta DEFAULT/seq en `teso_cobro_caja_metodo.id`, asignar id manualmente."""
    try:
        return CobroCajaMetodo.objects.create(**payload)
    except Exception as exc:
        err = str(exc).lower()
        if "null value" in err and "id" in err and "teso_cobro_caja_metodo" in err:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM teso_cobro_caja_metodo")
                    next_id = int(cursor.fetchone()[0])
                payload = {**payload, "id": next_id}
                obj = CobroCajaMetodo.objects.create(**payload)
            logger.warning(
                "Fallback teso_cobro_caja_metodo.id manual (%s) — ejecute migración 0006 o repare secuencia en BD.",
                next_id,
            )
            return obj
        raise


def _ensure_cobro_vinculo_table():
    """
    Tabla de vínculo CobroCaja <-> negocio/bienes.
    Permite consultar historial por RTM/EXPE sin depender de textos en observación.
    """
    if _table_exists("teso_cobro_caja_vinculo"):
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS teso_cobro_caja_vinculo (
                  id BIGSERIAL PRIMARY KEY,
                  cobro_id BIGINT NOT NULL,
                  empresa VARCHAR(10) NOT NULL,
                  tipo CHAR(1) NOT NULL,
                  rtm VARCHAR(20) NULL,
                  expe VARCHAR(12) NULL,
                  cocata1 VARCHAR(20) NULL,
                  created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_teso_cobro_vinculo_negocio ON teso_cobro_caja_vinculo (empresa, tipo, rtm, expe)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_teso_cobro_vinculo_bienes ON teso_cobro_caja_vinculo (empresa, tipo, cocata1)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_teso_cobro_vinculo_cobro ON teso_cobro_caja_vinculo (cobro_id)"
            )
    except Exception:
        # Si falla por permisos/DB, no bloquear cobro
        return


def _build_qr_base64(payload_text):
    """
    Genera QR en SVG para evitar dependencia de PIL/_imaging.
    Retorna un data URI listo para usar en <img src="...">.
    """
    try:
        from qrcode.image.svg import SvgPathImage

        img = qrcode.make(payload_text, image_factory=SvgPathImage, box_size=8, border=2)
        buff = io.BytesIO()
        img.save(buff)
        svg_data = buff.getvalue()
        svg_b64 = base64.b64encode(svg_data).decode("utf-8")
        return f"data:image/svg+xml;base64,{svg_b64}"
    except Exception:
        # Fallback seguro si falla la generación del QR
        fallback_svg = (
            "<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
            "<rect width='220' height='220' fill='white' stroke='black'/>"
            "<text x='20' y='100' font-size='14' fill='black'>QR no disponible</text>"
            "<text x='20' y='125' font-size='11' fill='black'>Recibo generado</text>"
            "</svg>"
        )
        svg_b64 = base64.b64encode(fallback_svg.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{svg_b64}"


def _insert_pagovarios_desde_temp(pago, empresa, usuario, numero_recibo):
    """
    Inserta en tabla pagovarios si existe, usando columnas disponibles dinámicamente.
    """
    if not _table_exists("pagovarios"):
        return False, "La tabla pagovarios no existe en la base de datos."

    payload = {
        "empresa": empresa,
        "recibo": pago.recibo,
        "rubro": (pago.rubro or "")[:6],
        "codigo": (pago.codigo or "")[:16],
        "fecha": date.today(),
        "identidad": (pago.identidad or "")[:31],
        "nombre": (pago.nombre or "")[:150],
        "descripcion": (pago.descripcion or "")[:200],
        "valor": _safe_decimal(pago.valor),
        "comentario": (pago.comentario or "")[:500],
        "oficina": (pago.oficina or "")[:20],
        "facturadora": (pago.facturadora or "")[:45],
        "aplicado": "1",
        "traslado": (pago.traslado or "0")[:1],
        "solvencia": _safe_decimal(pago.solvencia, "0"),
        "cantidad": _safe_decimal(pago.cantidad, "1"),
        "vl_unit": _safe_decimal(pago.vl_unit, "0"),
        "deposito": _safe_decimal(pago.deposito, "0"),
        "cajero": (usuario or "")[:20],
        "usuario": (usuario or "")[:30],
        "referencia": str(numero_recibo)[:20],
        "banco": (pago.banco or "")[:3],
        "Tipofa": "O",
        "Rtm": (pago.Rtm or "")[:20],
        "expe": (str(pago.expe or "0"))[:12],
        "pagodia": _safe_decimal(numero_recibo, "0"),
        "rcaja": _safe_decimal(pago.valor),
        "Rfechapag": date.today(),
        "permiso": _safe_decimal(pago.permiso, "0"),
        "Fechavence": pago.Fechavence,
        "direccion": (pago.direccion or " ")[:100],
        "prima": (pago.prima or "")[:1],
        "categoria": (pago.categoria or "")[:2],
        "sexo": (pago.sexo or "")[:1],
        "rtn": (pago.rtn or "")[:20],
    }

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pagovarios LIMIT 0")
        col_names = [col[0] for col in cursor.description]

        cols = [c for c in payload.keys() if c in col_names]
        if not cols:
            return False, "No se pudieron mapear columnas para pagovarios."

        placeholders = ", ".join(["%s"] * len(cols))
        fields = ", ".join(cols)
        values = [payload[c] for c in cols]
        cursor.execute(f"INSERT INTO pagovarios ({fields}) VALUES ({placeholders})", values)

    return True, ""


def _registrar_resumen_factura(
    *,
    numero_recibo,
    empresa,
    nombre,
    metodo_pago,
    valor_pagado,
    descripcion,
    comentario,
    usuario,
):
    """
    Registra resumen en tablas facturas y pagos_factura si existen.
    """
    now = datetime.now()
    warnings = []
    valor = _safe_decimal(valor_pagado).quantize(Decimal("0.01"))

    observacion_resumen = (
        f"empresa={empresa}; nombre={nombre}; metodo_pago={metodo_pago}; "
        f"valor_pagado={valor:.2f}; descripcion={descripcion}; comentario={comentario}"
    )

    # Evitar duplicate PK en id tras importaciones (secuencia desfasada respecto a MAX(id)).
    if connection.vendor == "postgresql":
        if _table_exists("facturas"):
            sync_postgres_serial_to_max_id("facturas")
        if _table_exists("pagos_factura"):
            sync_postgres_serial_to_max_id("pagos_factura")

    if _table_exists("facturas"):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM facturas LIMIT 0")
                cols_fact = [d[0] for d in cursor.description]
                payload_fact = {
                    "numero_factura": str(numero_recibo)[:20],
                    "fecha_emision": date.today(),
                    "fecha_vencimiento": date.today(),
                    "subtotal": valor,
                    "impuestos": Decimal("0.00"),
                    "total": valor,
                    "estado": "PAGADA",
                    "observaciones": observacion_resumen[:2000],
                    "usuario_creacion": (usuario or "SISTEMA")[:50],
                    "fecha_creacion": now,
                    "fecha_modificacion": now,
                }
                cols = [c for c in payload_fact.keys() if c in cols_fact]
                if cols:
                    values = [payload_fact[c] for c in cols]
                    placeholders = ", ".join(["%s"] * len(cols))
                    cursor.execute(
                        f"INSERT INTO facturas ({', '.join(cols)}) VALUES ({placeholders})",
                        values,
                    )
        except Exception as exc:
            warnings.append(f"No se pudo registrar resumen en facturas: {exc}")
    else:
        warnings.append("No existe tabla facturas para registrar resumen.")

    if _table_exists("pagos_factura"):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM pagos_factura LIMIT 0")
                cols_pago = [d[0] for d in cursor.description]
                payload_pago = {
                    "numero_recibo": str(numero_recibo)[:20],
                    "fecha_pago": date.today(),
                    "monto": valor,
                    "forma_pago": (metodo_pago or "EFECTIVO")[:15],
                    "referencia": str(empresa)[:50],
                    "observaciones": observacion_resumen[:2000],
                    "usuario_pago": (usuario or "SISTEMA")[:50],
                    "fecha_creacion": now,
                }
                cols = [c for c in payload_pago.keys() if c in cols_pago]
                if cols:
                    values = [payload_pago[c] for c in cols]
                    placeholders = ", ".join(["%s"] * len(cols))
                    cursor.execute(
                        f"INSERT INTO pagos_factura ({', '.join(cols)}) VALUES ({placeholders})",
                        values,
                    )
        except Exception as exc:
            warnings.append(f"No se pudo registrar resumen en pagos_factura: {exc}")
    else:
        warnings.append("No existe tabla pagos_factura para registrar forma de pago.")

    return warnings


def verificar_sesion(request):
    """Verifica si el usuario tiene sesión activa (como en otros módulos)."""
    return request.session.get("user_id") is not None


def get_empresa(request):
    """Obtiene la empresa del usuario en sesión."""
    return request.session.get("empresa", "")


def tesoreria_login(request):
    """Login del módulo Tesorería (usa el login centralizado del sistema)."""
    if verificar_sesion(request):
        return redirect("tesoreria:tesoreria_menu_principal")
    return redirect("modules_core:login_principal")


def tesoreria_logout(request):
    """Vista de logout del módulo Tesorería"""
    messages.success(request, "Sesión cerrada correctamente")
    return redirect("modules_core:menu_principal")


def tesoreria_menu_principal(request):
    """Menú principal del módulo Tesorería"""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    return render(
        request,
        "tesoreria/menu_principal.html",
        {
            "modulo": "Tesorería",
            "descripcion": "Gestión de tesorería y caja",
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
            "tot_pagos": PagoTesoreria.objects.filter(empresa=empresa, is_active=True).count(),
        },
    )


def caja_cobros(request):
    """Pantalla de cobros en caja basada en transacciones de pagovariostemp."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    usuario = request.session.get("usuario", "") or request.session.get("nombre", "")
    criterio = (request.GET.get("q") or "").strip()
    recibos_seleccionados = [r.strip() for r in request.GET.getlist("selected") if r and r.strip()]

    if request.method == "POST":
        accion = (request.POST.get("accion") or "cobrar").strip().lower()
        recibos_seleccionados = request.POST.getlist("recibos")

        if accion == "eliminar":
            motivo = (request.POST.get("motivo_eliminacion") or "").strip()
            if not recibos_seleccionados:
                messages.error(request, "Debe seleccionar al menos una transacción para eliminar.")
                return redirect("tesoreria:caja_cobros")
            if not motivo:
                messages.error(request, "Debe indicar un motivo para la eliminación manual.")
                return redirect("tesoreria:caja_cobros")

            # Solo permitir eliminar transacciones pendientes (aplicado=0) del municipio actual.
            pendientes_qs = PagoVariosTemp.objects.filter(
                empresa=empresa,
                aplicado="0",
                recibo__in=recibos_seleccionados,
            )

            # Bloquear si alguno de los recibos ya tiene registros aplicados u otra empresa.
            ya_aplicadas = (
                PagoVariosTemp.objects.filter(empresa=empresa, recibo__in=recibos_seleccionados)
                .exclude(aplicado="0")
                .exists()
            )
            if ya_aplicadas:
                messages.error(
                    request,
                    "No se puede eliminar: al menos una transacción seleccionada ya fue aplicada.",
                )
                return redirect("tesoreria:caja_cobros")

            count = pendientes_qs.count()
            if count <= 0:
                messages.warning(request, "No se encontraron transacciones pendientes para eliminar.")
                return redirect("tesoreria:caja_cobros")

            with transaction.atomic():
                pendientes_qs.delete()

            logger.warning(
                "Eliminación manual de transacciones en caja. empresa=%s usuario=%s recibos=%s motivo=%s",
                empresa,
                usuario,
                ",".join([str(r) for r in recibos_seleccionados]),
                motivo,
            )
            messages.success(request, f"Transacciones eliminadas: {count}.")
            return redirect("tesoreria:caja_cobros")

        formas = request.POST.getlist("forma_pago[]")
        montos = request.POST.getlist("monto_pago[]")
        referencias = request.POST.getlist("referencia_pago[]")
        efectivo_recibido_texto = (request.POST.get("efectivo_recibido") or "0").replace(",", ".").strip()

        if not recibos_seleccionados:
            messages.error(request, "Debe seleccionar al menos una transacción para cobrar.")
            return redirect("tesoreria:caja_cobros")

        pagos_qs = PagoVariosTemp.objects.filter(
            empresa=empresa,
            aplicado="0",
            recibo__in=recibos_seleccionados,
        )
        total = (pagos_qs.aggregate(total=Sum("valor")).get("total") or Decimal("0.00")).quantize(Decimal("0.01"))
        if total <= 0:
            messages.error(request, "No se encontraron valores pendientes para los recibos seleccionados.")
            return redirect("tesoreria:caja_cobros")

        detalles_metodo = []
        total_formas = Decimal("0.00")
        monto_efectivo = Decimal("0.00")

        for idx, forma in enumerate(formas):
            forma_val = (forma or "").strip().upper()
            if forma_val not in {"EFECTIVO", "POS", "CHEQUE", "COMPENSACION"}:
                continue

            monto_texto = (montos[idx] if idx < len(montos) else "0")
            monto_texto = (monto_texto or "0").replace(",", ".").strip()
            try:
                monto = Decimal(monto_texto or "0").quantize(Decimal("0.01"))
            except Exception:
                monto = Decimal("0.00")

            if monto <= 0:
                continue

            referencia = (referencias[idx] if idx < len(referencias) else "").strip()
            detalles_metodo.append(
                {
                    "forma_pago": forma_val,
                    "monto": monto,
                    "referencia": referencia[:80] if referencia else "",
                }
            )
            total_formas += monto
            if forma_val == "EFECTIVO":
                monto_efectivo += monto

        try:
            efectivo_recibido = Decimal(efectivo_recibido_texto or "0").quantize(Decimal("0.01"))
        except Exception:
            efectivo_recibido = Decimal("0.00")

        if detalles_metodo:
            if total_formas < total:
                messages.error(
                    request,
                    f"La suma de formas de pago (L. {total_formas:.2f}) no cubre el total seleccionado (L. {total:.2f}).",
                )
                return redirect("tesoreria:caja_cobros")
            vuelto = (total - total_formas).quantize(Decimal("0.01"))
        else:
            if efectivo_recibido < total:
                messages.error(request, f"Monto insuficiente. Total a pagar: L. {total:.2f}.")
                return redirect("tesoreria:caja_cobros")
            # Si no se ingresa forma combinada, se asume cobro 100% en efectivo
            detalles_metodo = [
                {
                    "forma_pago": "EFECTIVO",
                    "monto": total,
                    "referencia": "ASUMIDO-SIN-DETALLE",
                }
            ]
            monto_efectivo = total
            total_formas = total
            vuelto = (efectivo_recibido - total).quantize(Decimal("0.01"))

        warnings = []
        with transaction.atomic():
            numero_recibo_impreso = NoRecibos.obtener_siguiente_numero_por_empresa(empresa)
            if _table_exists("teso_cobro_caja"):
                cobro = _create_cobro_caja_with_id_fallback(
                    empresa=empresa,
                    fecha=date.today(),
                    cajero=usuario[:50] if usuario else "",
                    total_cobrado=total,
                    fuente="CAJA",
                    recibos_json=json.dumps(recibos_seleccionados),
                    referencia=f"R-{numero_recibo_impreso}",
                )
                if _table_exists("teso_cobro_caja_metodo"):
                    for det in detalles_metodo:
                        _create_cobro_caja_metodo_with_id_fallback(
                            cobro=cobro,
                            forma_pago=det["forma_pago"],
                            monto=det["monto"],
                            referencia=det["referencia"],
                        )
                else:
                    warnings.append("No existe tabla teso_cobro_caja_metodo: se omitió detalle de métodos.")
            else:
                warnings.append("No existe tabla teso_cobro_caja: se procesó cobro sin guardar corte de caja.")

            pagos_lista = list(pagos_qs)
            nombres_set = set()
            descripciones = []
            comentarios = []
            detalle_recibo_items = []
            ids_pagovariostemp_cobrados = []
            es_recibo_negocio = False
            negocio_rtm = ""
            negocio_expe = ""
            negocio_nombre = ""
            direccion_negocio = ""
            es_recibo_bienes = False
            clave_catastral = ""
            propietario = ""
            direccion_inmueble = ""
            ics_por_rubro = {}
            bienes_por_rubro = {}
            for pago in pagos_lista:
                tipofa = (pago.Tipofa or "").strip().upper()
                valor_pago = _safe_decimal(pago.valor)
                rubro = _norm_rubro_caja(pago.rubro or "")
                rtm = (pago.Rtm or "").strip()
                expe = (str(pago.expe or "")).strip()
                fecha_mov = date.today()
                if tipofa == "N":
                    es_recibo_negocio = True
                    if not negocio_rtm and rtm:
                        negocio_rtm = rtm
                    if not negocio_expe and expe:
                        negocio_expe = expe
                    if not negocio_nombre and pago.facturadora:
                        negocio_nombre = (pago.facturadora or "").strip()
                    if not direccion_negocio and pago.direccion:
                        direccion_negocio = (pago.direccion or "").strip()
                    # Para reflejar el cobro en "control tributario", se debe rebajar el saldo real
                    # de `transaccionesics` (que se calcula por `monto__gt=0`).
                    # Los descuentos llegan como líneas negativas; para saldar el rubro usamos solo el monto positivo.
                    if valor_pago > 0 and rubro:
                        ics_por_rubro[rubro] = (ics_por_rubro.get(rubro) or Decimal("0.00")) + valor_pago
                elif tipofa == "B":
                    es_recibo_bienes = True
                    # Para BI, el flujo envía `cocata1` normalmente en Rtm.
                    if not clave_catastral and rtm:
                        clave_catastral = str(rtm).strip()
                    if not propietario and pago.nombre:
                        propietario = (pago.nombre or "").strip()
                    if not direccion_inmueble and pago.direccion:
                        direccion_inmueble = (pago.direccion or "").strip()
                    # Acumular por rubro para rebajar cuotas BI reales (evita doble cobro)
                    if valor_pago > 0 and rubro:
                        bienes_por_rubro[rubro] = (bienes_por_rubro.get(rubro) or Decimal("0.00")) + valor_pago
                ids_pagovariostemp_cobrados.append(pago.id)
                detalle_recibo_items.append(
                    {
                        "rubro": rubro or "-",
                        "codigo": (pago.codigo or "").strip() or "-",
                        "descripcion": (pago.descripcion or "").strip() or "-",
                        "valor": valor_pago,
                    }
                )
                if pago.nombre:
                    nombres_set.add(str(pago.nombre).strip())
                if pago.descripcion:
                    descripciones.append(str(pago.descripcion).strip())
                if pago.comentario:
                    comentarios.append(str(pago.comentario).strip())

                if tipofa == "O":
                    ok, warn = _insert_pagovarios_desde_temp(
                        pago=pago,
                        empresa=empresa,
                        usuario=usuario or "SISTEMA",
                        numero_recibo=numero_recibo_impreso,
                    )
                    if not ok and warn:
                        warnings.append(warn)

            # Guardar referencia de "origen" para historial (negocios / bienes) si existe teso_cobro_caja.
            # Esto permite filtrar historial por RTM/EXPE o por Clave Catastral sin depender de pagovariostemp.
            try:
                if _table_exists("teso_cobro_caja") and "cobro" in locals() and cobro:
                    obs_parts = []
                    if es_recibo_negocio and negocio_rtm and negocio_expe:
                        obs_parts.append(f"tipo=N;rtm={negocio_rtm};expe={negocio_expe}")
                    if es_recibo_bienes and clave_catastral:
                        obs_parts.append(f"tipo=B;cocata1={clave_catastral}")
                    if obs_parts:
                        cobro.observacion = " | ".join(obs_parts)[:2000]
                        cobro.save(update_fields=["observacion"])
            except Exception:
                pass

            # Insertar vínculo estructurado (si la DB lo permite)
            try:
                if _table_exists("teso_cobro_caja") and "cobro" in locals() and cobro:
                    _ensure_cobro_vinculo_table()
                    if _table_exists("teso_cobro_caja_vinculo"):
                        with connection.cursor() as cursor:
                            if es_recibo_negocio and negocio_rtm and negocio_expe:
                                cursor.execute(
                                    """
                                    INSERT INTO teso_cobro_caja_vinculo (cobro_id, empresa, tipo, rtm, expe)
                                    VALUES (%s, %s, %s, %s, %s)
                                    """,
                                    [cobro.id, empresa, "N", negocio_rtm[:20], str(negocio_expe)[:12]],
                                )
                            if es_recibo_bienes and clave_catastral:
                                cursor.execute(
                                    """
                                    INSERT INTO teso_cobro_caja_vinculo (cobro_id, empresa, tipo, cocata1)
                                    VALUES (%s, %s, %s, %s)
                                    """,
                                    [cobro.id, empresa, "B", str(clave_catastral)[:20]],
                                )
            except Exception:
                pass

            # Reflejar cobro en Control Tributario: rebajar saldo en `transaccionesics` (monto__gt=0)
            emp_trib = _empresa_codigo_transacciones(empresa)
            if es_recibo_negocio and negocio_rtm and negocio_expe and ics_por_rubro and emp_trib:
                for rubro_codigo, monto_rubro in ics_por_rubro.items():
                    restante = (monto_rubro or Decimal("0.00")).quantize(Decimal("0.01"))
                    if restante <= 0:
                        continue

                    trans_qs = (
                        TransaccionesIcs.objects.annotate(
                            _rtm_t=Trim("rtm"),
                            _ex_t=Trim("expe"),
                            _rb_t=Trim("rubro"),
                        )
                        .filter(
                            empresa=emp_trib,
                            _rtm_t=negocio_rtm[:16].strip(),
                            _ex_t=str(negocio_expe)[:12].strip(),
                            _rb_t=_norm_rubro_caja(rubro_codigo),
                            monto__gt=0,
                        )
                        .order_by("ano", "mes", "id")
                    )
                    for trans in trans_qs:
                        if restante <= 0:
                            break
                        saldo = _safe_decimal(trans.monto)
                        if saldo <= 0:
                            continue
                        aplicar = saldo if saldo <= restante else restante
                        trans.monto = (saldo - aplicar).quantize(Decimal("0.01"))
                        trans.usuario = (usuario or "SISTEMA")[:50]
                        trans.fechasys = datetime.now()
                        trans.save(update_fields=["monto", "usuario", "fechasys"])
                        restante = (restante - aplicar).quantize(Decimal("0.01"))

                    if restante > 0:
                        warnings.append(
                            f"No se pudo aplicar el pago completo del rubro {rubro_codigo}. Pendiente: L. {restante:.2f}"
                        )

            # Reflejar cobro en Bienes Inmuebles: rebajar cuotas reales en `transaccionesbienesinmuebles`
            # La pantalla de BI lista `estado='A'`, así que si una cuota queda en 0 se marca como pagada.
            if es_recibo_bienes and clave_catastral and bienes_por_rubro and emp_trib:
                norm_cc = str(clave_catastral).strip()[:20]
                for rubro_codigo, monto_rubro in bienes_por_rubro.items():
                    restante = (monto_rubro or Decimal("0.00")).quantize(Decimal("0.01"))
                    if restante <= 0:
                        continue

                    qs_bi = (
                        TransaccionesBienesInmuebles.objects.annotate(
                            _cc_t=Trim("cocata1"),
                            _rb_t=Trim("rubro"),
                        )
                        .filter(
                            empresa=emp_trib,
                            _cc_t=norm_cc,
                            _rb_t=_norm_rubro_caja(rubro_codigo),
                            estado__iexact="A",
                        )
                        .order_by("ano", "mes", "id")
                    )
                    for tbi in qs_bi:
                        if restante <= 0:
                            break
                        saldo = _safe_decimal(tbi.monto)
                        if saldo <= 0:
                            # Si ya no tiene saldo, marcar como pagada para ocultarla del listado legacy
                            tbi.estado = "P"
                            tbi.usuario = (usuario or "SISTEMA")[:50]
                            tbi.fechasys = datetime.now()
                            tbi.save(update_fields=["estado", "usuario", "fechasys"])
                            continue

                        aplicar = saldo if saldo <= restante else restante
                        nuevo_saldo = (saldo - aplicar).quantize(Decimal("0.01"))
                        tbi.monto = nuevo_saldo
                        tbi.usuario = (usuario or "SISTEMA")[:50]
                        tbi.fechasys = datetime.now()
                        if nuevo_saldo <= 0:
                            tbi.estado = "P"
                            tbi.save(update_fields=["monto", "estado", "usuario", "fechasys"])
                        else:
                            tbi.save(update_fields=["monto", "usuario", "fechasys"])
                        restante = (restante - aplicar).quantize(Decimal("0.01"))

                    if restante > 0:
                        warnings.append(
                            f"No se pudo aplicar el pago completo BI del rubro {rubro_codigo}. Pendiente: L. {restante:.2f}"
                        )

            # Eliminar de pagovariostemp los registros ya cobrados
            # En algunos esquemas legacy el PK puede no coincidir con `id` o venir inconsistente.
            # Para asegurar que el recibo cobrado desaparezca de la lista, eliminamos por recibo/empresa/aplicado=0.
            if recibos_seleccionados:
                # Normalizar recibos para compatibilidad (a veces recibo es numérico/decimal).
                recibos_norm = [r.strip() for r in recibos_seleccionados if r and str(r).strip()]
                recibos_decimal = []
                for r in recibos_norm:
                    try:
                        recibos_decimal.append(Decimal(str(r)))
                    except Exception:
                        continue

                base_qs = PagoVariosTemp.objects.filter(empresa=empresa)
                antes = base_qs.filter(recibo__in=recibos_norm).count()
                if recibos_decimal:
                    antes = max(antes, base_qs.filter(recibo__in=recibos_decimal).count())

                borrados = 0
                # Intento 1: borrar solo pendientes (lo esperado)
                borrados += base_qs.filter(aplicado="0", recibo__in=recibos_norm).delete()[0]
                if recibos_decimal:
                    borrados += base_qs.filter(aplicado="0", recibo__in=recibos_decimal).delete()[0]

                # Fallback: si no borró nada pero sí existen filas del recibo, marcar como aplicado
                # para que desaparezcan del listado (que filtra aplicado="0").
                if borrados == 0 and antes > 0:
                    actualizados = base_qs.filter(aplicado="0", recibo__in=recibos_norm).update(aplicado="1")
                    if recibos_decimal:
                        actualizados += base_qs.filter(aplicado="0", recibo__in=recibos_decimal).update(aplicado="1")
                    if actualizados:
                        warnings.append(
                            f"Se marcaron como aplicadas {actualizados} transacciones (no se pudieron borrar físicamente)."
                        )
                elif borrados:
                    warnings.append(f"Se eliminaron {borrados} transacciones temporales cobradas.")

            formas_set = {d["forma_pago"] for d in detalles_metodo if d.get("forma_pago")}
            if not formas_set:
                metodo_resumen = "EFECTIVO"
            elif len(formas_set) == 1:
                metodo_resumen = next(iter(formas_set))
            else:
                metodo_resumen = "MIXTO"

            nombres_resumen = ", ".join(sorted([n for n in nombres_set if n]))[:300] or "CONTRIBUYENTE"
            descripcion_resumen = " | ".join([d for d in descripciones if d][:5])[:500]
            comentario_resumen = " | ".join([c for c in comentarios if c][:3])[:500]

        # Registrar resumen fuera del bloque principal para evitar romper la transacción de cobro
        try:
            warnings.extend(
                _registrar_resumen_factura(
                    numero_recibo=f"R-{numero_recibo_impreso}",
                    empresa=empresa,
                    nombre=nombres_resumen,
                    metodo_pago=metodo_resumen,
                    valor_pagado=total,
                    descripcion=descripcion_resumen,
                    comentario=comentario_resumen,
                    usuario=usuario or "SISTEMA",
                )
            )
        except Exception as e_resumen:
            warnings.append(f"No se pudo registrar resumen de factura: {str(e_resumen)}")

        qr_payload = (
            f"Empresa: {empresa}\n"
            f"Recibo: R-{numero_recibo_impreso}\n"
            f"Fecha: {date.today().isoformat()}\n"
            f"Total: {total:.2f}\n"
            f"Usuario: {usuario or 'SISTEMA'}"
        )
        qr_data_uri = _build_qr_base64(qr_payload)

        negocio_info = {}
        if es_recibo_negocio:
            negocio_db = None
            if negocio_rtm and negocio_expe:
                negocio_db = Negocio.objects.filter(
                    empresa=empresa,
                    rtm=negocio_rtm[:16],
                    expe=negocio_expe[:12],
                ).first()
            negocio_info = {
                "rtm": negocio_rtm or (negocio_db.rtm if negocio_db else ""),
                "expe": negocio_expe or (negocio_db.expe if negocio_db else ""),
                "nombre_negocio": (negocio_db.nombrenego if negocio_db else negocio_nombre) or "",
                "comerciante": (negocio_db.comerciante if negocio_db else "") or "",
                "direccion": (negocio_db.direccion if negocio_db else direccion_negocio) or "",
            }

        bienes_info = {}
        if es_recibo_bienes:
            bienes_info = {
                "clave_catastral": clave_catastral or "-",
                "propietario": propietario or nombres_resumen or "-",
                "direccion": direccion_inmueble or "-",
            }

        return render(
            request,
            "tesoreria/recibo_caja.html",
            {
                "empresa": empresa,
                "usuario": request.session.get("nombre", ""),
                "numero_recibo": f"R-{numero_recibo_impreso}",
                "fecha": date.today(),
                "total": total,
                "efectivo_recibido": efectivo_recibido,
                "vuelto": vuelto,
                "metodos": detalles_metodo,
                "nombres_resumen": nombres_resumen,
                "detalle_items": detalle_recibo_items,
                "es_recibo_negocio": es_recibo_negocio,
                "negocio_info": negocio_info,
                "es_recibo_bienes": es_recibo_bienes,
                "bienes_info": bienes_info,
                "warnings": warnings,
                "qr_data_uri": qr_data_uri,
            },
        )

    base_transacciones_qs = PagoVariosTemp.objects.filter(empresa=empresa, aplicado="0")
    transacciones_qs = base_transacciones_qs
    if criterio:
        filtros = (
            Q(Rtm__icontains=criterio)
            | Q(expe__icontains=criterio)
            | Q(identidad__icontains=criterio)
            | Q(nombre__icontains=criterio)
        )
        try:
            criterio_num = Decimal(criterio)
            filtros = filtros | Q(recibo=criterio_num) | Q(solvencia=criterio_num)
        except Exception:
            pass
        transacciones_qs = base_transacciones_qs.filter(filtros)

    if recibos_seleccionados:
        recibos_decimal = []
        for recibo in recibos_seleccionados:
            try:
                recibos_decimal.append(Decimal(recibo))
            except Exception:
                continue
        if recibos_decimal:
            transacciones_qs = (
                transacciones_qs | base_transacciones_qs.filter(recibo__in=recibos_decimal)
            ).distinct()

    transacciones = list(
        transacciones_qs.values("recibo", "solvencia", "Rtm", "expe", "identidad", "nombre")
        .annotate(total=Sum("valor"))
        .order_by("recibo")
    )

    for item in transacciones:
        item["recibo"] = str(item.get("recibo") or "")
        item["solvencia"] = str(item.get("solvencia") or "")
        item["Rtm"] = (item.get("Rtm") or "").strip()
        item["expe"] = str(item.get("expe") or "").strip()
        item["identidad"] = (item.get("identidad") or "").strip()
        item["nombre"] = (item.get("nombre") or "").strip()
        item["total"] = float(item.get("total") or 0)

    recibos = [t["recibo"] for t in transacciones]
    detalles_raw = (
        PagoVariosTemp.objects.filter(empresa=empresa, aplicado="0", recibo__in=recibos)
        .values("recibo", "codigo", "descripcion", "valor")
        .order_by("-recibo", "codigo")
    )
    detalles_por_recibo = {}
    for det in detalles_raw:
        recibo = str(det.get("recibo") or "")
        if recibo not in detalles_por_recibo:
            detalles_por_recibo[recibo] = []
        detalles_por_recibo[recibo].append(
            {
                "codigo": (det.get("codigo") or "").strip(),
                "descripcion": (det.get("descripcion") or "").strip(),
                "valor": float(det.get("valor") or 0),
            }
        )

    return render(
        request,
        "tesoreria/caja_cobros.html",
        {
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
            "criterio": criterio,
            "recibos_seleccionados": recibos_seleccionados,
            "transacciones": transacciones,
            "detalles_json": json.dumps(detalles_por_recibo),
            "formas_pago": [
                {"codigo": "EFECTIVO", "nombre": "Efectivo"},
                {"codigo": "POS", "nombre": "POS"},
                {"codigo": "CHEQUE", "nombre": "Cheque"},
                {"codigo": "COMPENSACION", "nombre": "Compensación"},
            ],
        },
    )


def cierre_diario_caja(request):
    """Cierre diario de recaudación por cajero y consolidado incluyendo webservice."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    fecha_param = (request.GET.get("fecha") or "").strip()
    try:
        fecha_cierre = datetime.strptime(fecha_param, "%Y-%m-%d").date() if fecha_param else date.today()
    except Exception:
        fecha_cierre = date.today()

    if _table_exists("teso_cobro_caja"):
        cobros_caja = (
            CobroCaja.objects.filter(empresa=empresa, fecha=fecha_cierre, fuente="CAJA", is_active=True)
            .prefetch_related("metodos")
            .order_by("cajero", "id")
        )
    else:
        cobros_caja = []

    por_cajero = {}
    total_caja = Decimal("0.00")
    totales_metodos = {
        "EFECTIVO": Decimal("0.00"),
        "POS": Decimal("0.00"),
        "CHEQUE": Decimal("0.00"),
        "COMPENSACION": Decimal("0.00"),
    }

    for cobro in cobros_caja:
        cajero = (cobro.cajero or "SIN_CAJERO").strip() or "SIN_CAJERO"
        if cajero not in por_cajero:
            por_cajero[cajero] = {
                "cajero": cajero,
                "total": Decimal("0.00"),
                "cantidad_cobros": 0,
                "metodos": {
                    "EFECTIVO": Decimal("0.00"),
                    "POS": Decimal("0.00"),
                    "CHEQUE": Decimal("0.00"),
                    "COMPENSACION": Decimal("0.00"),
                },
            }
        por_cajero[cajero]["total"] += cobro.total_cobrado or Decimal("0.00")
        por_cajero[cajero]["cantidad_cobros"] += 1
        total_caja += cobro.total_cobrado or Decimal("0.00")

        if _table_exists("teso_cobro_caja_metodo"):
            for met in cobro.metodos.all():
                forma = (met.forma_pago or "").upper()
                if forma not in por_cajero[cajero]["metodos"]:
                    continue
                monto = met.monto or Decimal("0.00")
                por_cajero[cajero]["metodos"][forma] += monto
                totales_metodos[forma] += monto

    # Cobros aplicados sin cajero: se asumen provenientes de webservice/integraciones
    total_webservice = (
        PagoVariosTemp.objects.filter(
            empresa=empresa,
            aplicado="1",
            Rfechapag=fecha_cierre,
        )
        .filter(Q(cajero__isnull=True) | Q(cajero__exact=""))
        .aggregate(total=Sum("valor"))
        .get("total")
        or Decimal("0.00")
    )

    consolidado = {
        "fecha": fecha_cierre,
        "total_caja": total_caja,
        "total_webservice": total_webservice,
        "total_general": total_caja + total_webservice,
    }

    return render(
        request,
        "tesoreria/cierre_diario.html",
        {
            "empresa": empresa,
            "usuario": request.session.get("nombre", ""),
            "fecha_cierre": fecha_cierre.strftime("%Y-%m-%d"),
            "por_cajero": list(por_cajero.values()),
            "totales_metodos": totales_metodos,
            "consolidado": consolidado,
            "usa_tabla_cobro_caja": _table_exists("teso_cobro_caja"),
        },
    )


def _parse_observacion_resumen(raw_obs):
    data = {
        "empresa": "",
        "nombre": "",
        "metodo_pago": "",
        "valor_pagado": "",
        "descripcion": "",
        "comentario": "",
        "tipo": "",
        "rtm": "",
        "expe": "",
        "cocata1": "",
    }
    texto = (raw_obs or "").strip()
    if not texto:
        return data

    # Permite formatos: "k=v; k2=v2" y también bloques separados por "|".
    for chunk in texto.split("|"):
        for part in chunk.split(";"):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            key = k.strip()
            val = v.strip()
            if key in data:
                data[key] = val
    return data


def resumen_facturas_caja(request):
    """Resumen de facturas emitidas desde caja con filtros y exportación."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    fecha_desde = (request.GET.get("fecha_desde") or "").strip()
    fecha_hasta = (request.GET.get("fecha_hasta") or "").strip()
    cajero = (request.GET.get("cajero") or "").strip()
    metodo = (request.GET.get("metodo") or "").strip().upper()
    exportar = (request.GET.get("exportar") or "").strip().lower()

    if not _table_exists("teso_cobro_caja"):
        return render(
            request,
            "tesoreria/resumen_facturas_caja.html",
            {
                "empresa": empresa,
                "usuario": request.session.get("nombre", ""),
                "rows": [],
                "total_general": Decimal("0.00"),
                "filtros": {
                    "fecha_desde": fecha_desde,
                    "fecha_hasta": fecha_hasta,
                    "cajero": cajero,
                    "metodo": metodo,
                },
                "usa_tabla_cobro_caja": False,
            },
        )

    qs = CobroCaja.objects.filter(empresa=empresa, fuente="CAJA", is_active=True).prefetch_related("metodos")
    if fecha_desde:
        qs = qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        qs = qs.filter(fecha__lte=fecha_hasta)
    if cajero:
        qs = qs.filter(cajero__icontains=cajero)
    if metodo and metodo != "MIXTO":
        qs = qs.filter(metodos__forma_pago=metodo)

    qs = qs.order_by("-fecha", "-id").distinct()
    cobros = list(qs)

    referencias = [str(c.referencia or "").strip() for c in cobros if c.referencia]
    observaciones_map = {}
    if referencias and _table_exists("pagos_factura"):
        placeholders = ", ".join(["%s"] * len(referencias))
        sql = (
            f"SELECT numero_recibo, observaciones FROM pagos_factura "
            f"WHERE numero_recibo IN ({placeholders})"
        )
        with connection.cursor() as cursor:
            cursor.execute(sql, referencias)
            for numero_recibo, observacion in cursor.fetchall():
                observaciones_map[str(numero_recibo)] = observacion or ""

    rows = []
    total_general = Decimal("0.00")
    vinculos_by_cobro_id = {}
    try:
        if cobros and _table_exists("teso_cobro_caja_vinculo"):
            cobro_ids = [c.id for c in cobros if getattr(c, "id", None)]
            if cobro_ids:
                placeholders = ", ".join(["%s"] * len(cobro_ids))
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                        SELECT cobro_id, tipo, rtm, expe, cocata1
                        FROM teso_cobro_caja_vinculo
                        WHERE cobro_id IN ({placeholders})
                        """,
                        cobro_ids,
                    )
                    for cobro_id, tipo, rtm_v, expe_v, cocata1_v in cursor.fetchall():
                        vinculos_by_cobro_id[int(cobro_id)] = {
                            "tipo": (tipo or "").strip(),
                            "rtm": (rtm_v or "").strip(),
                            "expe": (expe_v or "").strip(),
                            "cocata1": (cocata1_v or "").strip(),
                        }
    except Exception:
        vinculos_by_cobro_id = {}

    for c in cobros:
        metodos = sorted({(m.forma_pago or "").upper() for m in c.metodos.all() if m.forma_pago})
        metodo_txt = " + ".join(metodos) if metodos else "EFECTIVO"
        if metodo == "MIXTO" and len(metodos) <= 1:
            continue
        obs_pf = _parse_observacion_resumen(observaciones_map.get(str(c.referencia or ""), ""))
        obs_cobro = _parse_observacion_resumen(c.observacion or "")
        obs = {**obs_pf, **{k: v for k, v in obs_cobro.items() if v}}
        v = vinculos_by_cobro_id.get(int(c.id)) if getattr(c, "id", None) else None
        if v:
            if v.get("rtm") and not obs.get("rtm"):
                obs["rtm"] = v.get("rtm")
            if v.get("expe") and not obs.get("expe"):
                obs["expe"] = v.get("expe")
            if v.get("cocata1") and not obs.get("cocata1"):
                obs["cocata1"] = v.get("cocata1")
        row = {
            "numero_recibo": str(c.referencia or ""),
            "empresa": obs.get("empresa") or c.empresa,
            "nombre": obs.get("nombre") or "",
            "metodo_pago": obs.get("metodo_pago") or metodo_txt,
            "valor_pagado": c.total_cobrado or Decimal("0.00"),
            "descripcion": obs.get("descripcion") or "",
            "comentario": obs.get("comentario") or "",
            "fecha": c.fecha,
            "cajero": c.cajero or "",
            "rtm": obs.get("rtm") or "",
            "expe": obs.get("expe") or "",
            "cocata1": obs.get("cocata1") or "",
        }
        rows.append(row)
        total_general += row["valor_pagado"]

    if exportar == "csv":
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="resumen_facturas_caja.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Numero Recibo",
                "Empresa",
                "RTM",
                "EXPE",
                "Cocata1",
                "Nombre",
                "Metodo de Pago",
                "Valor Pagado",
                "Descripcion",
                "Comentario",
                "Fecha",
                "Cajero",
            ]
        )
        for r in rows:
            writer.writerow(
                [
                    r["numero_recibo"],
                    r["empresa"],
                    r["rtm"],
                    r["expe"],
                    r["cocata1"],
                    r["nombre"],
                    r["metodo_pago"],
                    f"{r['valor_pagado']:.2f}",
                    r["descripcion"],
                    r["comentario"],
                    r["fecha"],
                    r["cajero"],
                ]
            )
        return response

    return render(
        request,
        "tesoreria/resumen_facturas_caja.html",
        {
            "empresa": empresa,
            "usuario": request.session.get("nombre", ""),
            "rows": rows,
            "total_general": total_general,
            "filtros": {
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
                "cajero": cajero,
                "metodo": metodo,
            },
            "usa_tabla_cobro_caja": True,
        },
    )


def cuentas_tesoreria(request):
    """Listado y filtro de cuentas configuradas (caja/banco/chequera)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    q = (request.GET.get("q") or "").strip()

    qs = CuentaTesoreria.objects.filter(empresa=empresa, is_active=True)
    if q:
        qs = qs.filter(Q(codigo__icontains=q) | Q(nombre__icontains=q) | Q(tipo__icontains=q))

    cuentas = qs.order_by("tipo", "codigo")
    return render(
        request,
        "tesoreria/cuentas_tesoreria.html",
        {
            "cuentas": cuentas,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
            "q": q,
            "titulo": "Cuentas de Tesorería",
        },
    )


def cuenta_tesoreria_crear(request):
    """Crear cuenta de tesorería (configurar enlace con cuenta contable)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    if request.method == "POST":
        form = CuentaTesoreriaForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.empresa = empresa
            cuenta.save()
            messages.success(request, "Cuenta de Tesorería creada correctamente.")
            return redirect("tesoreria:cuentas_tesoreria")
    else:
        form = CuentaTesoreriaForm(initial={"empresa": empresa})

    # Solo cuentas del catálogo de Activo (grupo 1) suelen aplicarse a Caja/Bancos.
    form.fields["cuenta_contable"].queryset = (
        CuentaContable.objects.filter(
            empresa=empresa,
            is_active=True,
            grupo__codigo="1",
        )
        .order_by("codigo")
    )

    return render(
        request,
        "tesoreria/cuenta_tesoreria_form.html",
        {
            "form": form,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
            "titulo": "Nueva Cuenta de Tesorería",
        },
    )


def cuenta_tesoreria_editar(request, pk):
    """Editar cuenta de tesorería (enlace con cuenta contable)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    cuenta = get_object_or_404(CuentaTesoreria, pk=pk, empresa=empresa)

    if request.method == "POST":
        form = CuentaTesoreriaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta de Tesorería actualizada correctamente.")
            return redirect("tesoreria:cuentas_tesoreria")
    else:
        form = CuentaTesoreriaForm(instance=cuenta, initial={"empresa": empresa})

    form.fields["cuenta_contable"].queryset = (
        CuentaContable.objects.filter(
            empresa=empresa,
            is_active=True,
            grupo__codigo="1",
        )
        .order_by("codigo")
    )

    return render(
        request,
        "tesoreria/cuenta_tesoreria_form.html",
        {
            "form": form,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
            "titulo": f"Editar Cuenta de Tesorería: {cuenta.codigo}",
        },
    )


def pagos_tesoreria(request):
    """Emisión de pagos (cheques/transferencia) vinculando órdenes de pago presupuestarias."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    # Cuentas bancarias o cajas para realizar pagos
    cuentas = CuentaTesoreria.objects.filter(
        empresa=empresa,
        is_active=True,
    ).order_by("tipo", "codigo")

    # Órdenes de pago que están listas para ser pagadas
    ordenes = OrdenPago.objects.filter(
        empresa=empresa,
        is_active=True,
        estado="APROBADA",
    ).order_by("-fecha", "-numero")

    if request.method == "POST":
        form = PagoTesoreriaForm(request.POST)
        form.fields["cuenta_tesoreria"].queryset = cuentas
        if form.is_valid():
            pago = form.save(commit=False)
            pago.empresa = empresa

            op_ids = request.POST.getlist("ordenes_pago")
            ops = OrdenPago.objects.filter(id__in=op_ids, empresa=empresa, is_active=True)
            
            if not ops.exists():
                messages.error(request, "Debe seleccionar al menos una orden de pago.")
            else:
                monto_total = Decimal("0.00")
                for op in ops:
                    monto_total += op.total or Decimal("0.00")
                
                pago.monto_total = monto_total
                pago.save()

                # Crear detalles y actualizar presupuesto
                for op in ops:
                    PagoDetalleOrden.objects.create(
                        pago=pago,
                        orden_pago=op,
                        monto=op.total or Decimal("0.00")
                    )
                    # Cambiar estado a PAGADA
                    op.estado = "PAGADA"
                    op.save(update_fields=["estado"])

                messages.success(request, f"Pago {pago.numero_referencia} registrado por L. {monto_total:.2f}.")
                return redirect("tesoreria:pagos_tesoreria")
    else:
        form = PagoTesoreriaForm(initial={"empresa": empresa})
        form.fields["cuenta_tesoreria"].queryset = cuentas

    return render(
        request,
        "tesoreria/pagos_tesoreria.html",
        {
            "form": form,
            "ordenes": ordenes[:150],
            "pagos": PagoTesoreria.objects.filter(empresa=empresa, is_active=True).order_by("-fecha", "-numero_referencia")[:100],
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def gestionar_cheques(request):
    """Control de entrega y anulación de cheques."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    q = request.GET.get("q", "")
    cheques = PagoTesoreria.objects.filter(empresa=empresa, tipo_pago="CHEQUE", is_active=True)
    
    if q:
        cheques = cheques.filter(Q(numero_referencia__icontains=q) | Q(beneficiario__icontains=q))

    if request.method == "POST":
        pago_id = request.POST.get("pago_id")
        accion = request.POST.get("accion")
        pago = get_object_or_404(PagoTesoreria, id=pago_id, empresa=empresa)

        if accion == "entregar":
            pago.is_delivered = True
            pago.fecha_entrega = request.POST.get("fecha_entrega")
            pago.save()
            messages.success(request, f"Cheque {pago.numero_referencia} marcado como entregado.")
        elif accion == "anular":
            pago.estado = "ANULADO"
            pago.save()
            # Opcional: Liberar órdenes de pago
            for det in pago.detalles_ordenes.all():
                op = det.orden_pago
                op.estado = "APROBADA"
                op.save()
            messages.warning(request, f"Cheque {pago.numero_referencia} anulado y órdenes de pago liberadas.")
        
        return redirect("tesoreria:gestionar_cheques")

    return render(
        request,
        "tesoreria/cheques_control.html",
        {
            "cheques": cheques.order_by("-fecha", "-numero_referencia"),
            "q": q,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
        },
    )


def depositos_tesoreria(request):
    """Gestión de depósitos bancarios."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    if request.method == "POST":
        form = DepositoTesoreriaForm(request.POST)
        if form.is_valid():
            dep = form.save(commit=False)
            dep.empresa = empresa
            dep.save()
            messages.success(request, "Depósito registrado correctamente.")
            return redirect("tesoreria:depositos_tesoreria")
    else:
        form = DepositoTesoreriaForm(initial={"empresa": empresa})

    items = DepositoTesoreria.objects.filter(empresa=empresa, is_active=True).order_by("-fecha")
    return render(
        request,
        "tesoreria/depositos.html",
        {"form": form, "items": items, "empresa": empresa}
    )


def notas_tesoreria(request):
    """Gestión de Notas de Crédito y Débito."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    if request.method == "POST":
        form = NotaTesoreriaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.empresa = empresa
            nota.save()
            messages.success(request, "Nota registrada correctamente.")
            return redirect("tesoreria:notas_tesoreria")
    else:
        form = NotaTesoreriaForm(initial={"empresa": empresa})

    items = NotaTesoreria.objects.filter(empresa=empresa, is_active=True).order_by("-fecha")
    return render(
        request,
        "tesoreria/notas.html",
        {"form": form, "items": items, "empresa": empresa}
    )


def conciliacion_bancaria(request):
    """Listado de conciliaciones y creación de nuevas."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    if request.method == "POST":
        form = ConciliacionBancariaForm(request.POST)
        if form.is_valid():
            con = form.save(commit=False)
            con.empresa = empresa
            con.save()
            return redirect("tesoreria:detalle_conciliacion", pk=con.id)
    else:
        form = ConciliacionBancariaForm(initial={"empresa": empresa})

    items = ConciliacionBancaria.objects.filter(empresa=empresa, is_active=True).order_by("-anio", "-mes")
    return render(
        request,
        "tesoreria/conciliacion.html",
        {"form": form, "items": items, "empresa": empresa}
    )


def detalle_conciliacion(request, pk):
    """Proceso de conciliación (matching)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    
    empresa = get_empresa(request)
    conciliacion = get_object_or_404(ConciliacionBancaria, pk=pk, empresa=empresa)
    
    # Aquí iría la lógica para buscar pagos/depósitos no conciliados
    return render(
        request,
        "tesoreria/conciliacion_detalle.html",
        {"conciliacion": conciliacion, "empresa": empresa}
    )


def consultar_ordenes_pago(request):
    """Consulta de órdenes de pago desde Tesorería."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")

    empresa = get_empresa(request)
    q = request.GET.get("q", "")
    items = OrdenPago.objects.filter(empresa=empresa, is_active=True)
    if q:
        items = items.filter(Q(numero__icontains=q) | Q(beneficiario__icontains=q))

    return render(
        request,
        "tesoreria/ordenes_pago_consulta.html",
        {"items": items.order_by("-fecha"), "q": q, "empresa": empresa}
    )

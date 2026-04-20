# -*- coding: utf-8 -*-
from datetime import date
from decimal import Decimal
from functools import wraps

from django.contrib import messages
from django.db import transaction
from django.db.models import Max, Prefetch, Sum
from django.shortcuts import get_object_or_404, redirect, render
from contabilidad.models import EjercicioFiscal, Inventario
from presupuestos.models import CuentaPresupuestaria

from .forms import (
    OrdenCompraDetalleFormSet,
    OrdenCompraForm,
    OrdenCompraNuevaForm,
    RequisicionDetalleFormSet,
    RequisicionForm,
    RequisicionNuevaForm,
    label_inventario_catalogo,
)
from .models import OrdenCompra, Requisicion, RequisicionDetalle, SolicitudCotizacion


def compras_require_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("modules_core:login_principal")
        return view_func(request, *args, **kwargs)

    return wrapper


def _empresa(request):
    return (request.session.get("empresa") or "").strip()


def _ctx(request):
    return {
        "usuario": request.session.get("nombre"),
        "empresa": _empresa(request),
        "es_aprobador": _usuario_es_aprobador(request),
    }


def _usuario_es_aprobador(request):
    """
    Verifica si el usuario en sesión tiene el rol de 'Aprobador de Compras'
    o es superusuario.
    """
    if request.session.get("es_superusuario"):
        return True
    
    uid = request.session.get("user_id")
    if not uid:
        return False
    
    from usuarios.models import UsuarioRol
    return UsuarioRol.objects.filter(
        usuario_id=uid,
        rol__nombre__icontains="Aprobador",
        is_active=True
    ).exists()

def _usuario_es_comprador(request):
    if request.session.get("es_superusuario"):
        return True
    uid = request.session.get("user_id")
    if not uid: return False
    from usuarios.models import UsuarioRol
    return UsuarioRol.objects.filter(usuario_id=uid, rol__nombre__icontains="Comprador", is_active=True).exists()

def _usuario_es_solicitante(request):
    if request.session.get("es_superusuario"):
        return True
    uid = request.session.get("user_id")
    if not uid: return False
    from usuarios.models import UsuarioRol
    return UsuarioRol.objects.filter(usuario_id=uid, rol__nombre__icontains="Solicitante", is_active=True).exists()


def _ejercicio_fiscal_actual(empresa: str):
    """
    Ejercicio fiscal vigente: preferir abierto con fechas que incluyen hoy;
    luego abierto del año calendario; luego el abierto más reciente;
    si no hay abiertos, el ejercicio del año en curso (aunque esté cerrado).
    """
    hoy = date.today()
    qs = EjercicioFiscal.objects.filter(empresa=empresa, estado="ABIERTO").order_by("-anio")
    for ej in qs:
        if ej.fecha_inicio <= hoy <= ej.fecha_fin:
            return ej
    ej = qs.filter(anio=hoy.year).first()
    if ej:
        return ej
    ej = qs.first()
    if ej:
        return ej
    return EjercicioFiscal.objects.filter(empresa=empresa, anio=hoy.year).order_by("-anio").first()


def _siguiente_correlativo_y_numero_requisicion(empresa: str, ej: EjercicioFiscal) -> tuple[int, str]:
    """Siguiente correlativo y texto de número REQ-{año}-{correlativo:04d} (llamar dentro de transaction.atomic + select_for_update del ejercicio)."""
    max_c = (
        Requisicion.objects.filter(empresa=empresa, ejercicio=ej).aggregate(m=Max("correlativo"))["m"] or 0
    )
    next_c = max_c + 1
    return next_c, f"REQ-{ej.anio}-{next_c:04d}"


def _filtrar_querysets_detalle(formset, empresa: str):
    if not empresa:
        return
    inv_qs = Inventario.objects.filter(empresa=empresa, is_active=True).order_by(
        "tipo_inventario__orden", "tipo_inventario__nombre", "codigo"
    )
    cpu_qs = CuentaPresupuestaria.objects.filter(empresa=empresa, is_active=True).order_by("codigo")
    for frm in formset.forms:
        frm.fields["inventario"].queryset = inv_qs
        frm.fields["inventario"].label_from_instance = label_inventario_catalogo
        frm.fields["cuenta_presupuestaria"].queryset = cpu_qs
        frm.fields["inventario"].required = False
        frm.fields["cuenta_presupuestaria"].required = False


def _requisicion_stock_rows(formset, empresa: str):
    """Existencia en bodega (Inventario.cantidad) y faltante = max(0, pedido - existencia)."""
    rows = []
    for f in formset.forms:
        ex = falt = None
        inv_obj = None
        cant = None
        if f.is_bound and getattr(f, "cleaned_data", None) and f.cleaned_data and not f.cleaned_data.get("DELETE"):
            inv_obj = f.cleaned_data.get("inventario")
            cant = f.cleaned_data.get("cantidad")
        if inv_obj is None and f.is_bound:
            raw_inv = f.data.get(f.add_prefix("inventario"))
            raw_cant = f.data.get(f.add_prefix("cantidad"))
            if raw_inv:
                inv_obj = Inventario.objects.filter(pk=raw_inv, empresa=empresa).first()
            if raw_cant not in (None, ""):
                try:
                    cant = Decimal(str(raw_cant).replace(",", "."))
                except Exception:
                    cant = None
        if inv_obj is None and f.instance.pk and f.instance.inventario_id:
            inv_obj = f.instance.inventario
            cant = f.instance.cantidad
        if inv_obj is not None and cant is not None:
            ex = inv_obj.cantidad
            falt = max(Decimal(0), cant - ex)
        rows.append({"existencia": ex, "faltante": falt})
    return rows


def _ejercicio_fiscal_vigente(empresa: str):
    """
    Ejercicio fiscal abierto más reciente para la empresa.
    Si no hay ninguno en estado ABIERTO, usa el ejercicio activo más reciente por año.
    """
    emp = (empresa or "").strip()
    if not emp:
        return None
    ej = (
        EjercicioFiscal.objects.filter(empresa=emp, is_active=True, estado="ABIERTO")
        .order_by("-anio")
        .first()
    )
    if ej:
        return ej
    return EjercicioFiscal.objects.filter(empresa=emp, is_active=True).order_by("-anio").first()


def _siguiente_numero_orden_compra(empresa: str) -> str:
    year = date.today().year
    prefix = f"OC-{year}-"
    ultimos = (
        OrdenCompra.objects.filter(empresa=empresa, numero__startswith=prefix)
        .order_by("-numero")
        .values_list("numero", flat=True)[:1]
    )
    if not ultimos:
        return f"{prefix}0001"
    try:
        n = int(ultimos[0].replace(prefix, "")) + 1
    except (ValueError, IndexError):
        n = 1
    return f"{prefix}{n:04d}"


def _filtrar_querysets_oc_detalle(formset, empresa: str):
    if not empresa:
        return
    inv_qs = Inventario.objects.filter(empresa=empresa, is_active=True).order_by(
        "tipo_inventario__orden", "tipo_inventario__nombre", "codigo"
    )
    cpu_qs = CuentaPresupuestaria.objects.filter(empresa=empresa, is_active=True).order_by("codigo")
    for frm in formset.forms:
        frm.fields["inventario"].queryset = inv_qs
        frm.fields["inventario"].label_from_instance = label_inventario_catalogo
        frm.fields["cuenta_presupuestaria"].queryset = cpu_qs
        frm.fields["inventario"].required = False
        frm.fields["cuenta_presupuestaria"].required = False


@compras_require_auth
def compras_menu_principal(request):
    emp = _empresa(request)
    ctx = _ctx(request)
    ctx.update(
        {
            "modulo": "Compras y abastecimiento",
            "sin_empresa": not bool(emp),
            "count_req": Requisicion.objects.filter(empresa=emp).count() if emp else 0,
            "req_pendientes": Requisicion.objects.filter(empresa=emp, estado__in=["BORRADOR", "ENVIADA"]).count() if emp else 0,
            "count_oc": OrdenCompra.objects.filter(empresa=emp).count() if emp else 0,
            "oc_abiertas": OrdenCompra.objects.filter(empresa=emp, estado__in=["BORRADOR", "APROBADA"]).count() if emp else 0,
            "count_sc": SolicitudCotizacion.objects.filter(empresa=emp).count() if emp else 0,
            "sc_abiertas": SolicitudCotizacion.objects.filter(empresa=emp, estado__in=["BORRADOR", "PUBLICADA"]).count() if emp else 0,
            "monto_oc_mes": OrdenCompra.objects.filter(empresa=emp, fecha__month=date.today().month, ejercicio__anio=date.today().year).aggregate(s=Sum("monto_total"))["s"] or 0 if emp else 0,
        }
    )
    return render(request, "compras/menu_principal.html", ctx)


@compras_require_auth
def requisicion_list(request):
    emp = _empresa(request)
    ctx = _ctx(request)
    if not emp:
        ctx["sin_empresa"] = True
        ctx["object_list"] = []
        return render(request, "compras/requisicion_list.html", ctx)
    qs = Requisicion.objects.filter(empresa=emp).select_related("ejercicio").order_by("-fecha", "-id")
    ctx["object_list"] = qs
    return render(request, "compras/requisicion_list.html", ctx)


@compras_require_auth
def requisicion_create(request):
    if not (_usuario_es_solicitante(request) or _usuario_es_comprador(request) or _usuario_es_aprobador(request)):
        messages.error(request, "No tiene permisos para crear requisiciones. Debe tener rol de Solicitante.")
        return redirect("compras:requisicion_list")

    emp = _empresa(request)
    if not emp:
        messages.error(
            request,
            "Su sesión no tiene empresa/municipio. Inicie sesión con un usuario municipal o asigne empresa.",
        )
        return redirect("compras:compras_menu_principal")

    if request.method == "POST":
        form = RequisicionNuevaForm(request.POST, empresa=emp)
        if form.is_valid():
            ej = _ejercicio_fiscal_actual(emp)
            if not ej:
                messages.error(
                    request,
                    "No hay ejercicio fiscal abierto vigente para su empresa. Defínalo en Contabilidad.",
                )
            else:
                req = form.save(commit=False)
                req.empresa = emp
                req.ejercicio = ej
                req.estado = "BORRADOR"
                with transaction.atomic():
                    EjercicioFiscal.objects.select_for_update().filter(pk=ej.pk).first()
                    corr, num = _siguiente_correlativo_y_numero_requisicion(emp, ej)
                    req.correlativo = corr
                    req.numero = num
                    req.save()
                messages.success(request, f"Requisición {req.numero} creada. Agregue líneas en editar.")
                return redirect("compras:requisicion_edit", pk=req.pk)
    else:
        form = RequisicionNuevaForm(empresa=emp, initial={"fecha": date.today()})
    ctx = _ctx(request)
    ctx["form"] = form
    ctx["titulo"] = "Nueva requisición"
    return render(request, "compras/requisicion_form_nueva.html", ctx)


@compras_require_auth
def requisicion_edit(request, pk):
    if not (_usuario_es_solicitante(request) or _usuario_es_comprador(request) or _usuario_es_aprobador(request)):
        messages.error(request, "No tiene permisos para modificar requisiciones.")
        return redirect("compras:requisicion_list")

    emp = _empresa(request)
    if not emp:
        messages.error(request, "Se requiere empresa en sesión.")
        return redirect("compras:compras_menu_principal")

    req = get_object_or_404(
        Requisicion.objects.select_related("ejercicio").prefetch_related(
            Prefetch(
                "detalles",
                queryset=RequisicionDetalle.objects.select_related("inventario", "cuenta_presupuestaria"),
            )
        ),
        pk=pk,
        empresa=emp,
    )
    if request.method == "POST":
        form = RequisicionForm(request.POST, instance=req, empresa=emp)
        fs = RequisicionDetalleFormSet(request.POST, instance=req)
        _filtrar_querysets_detalle(fs, emp)
        if form.is_valid() and fs.is_valid():
            with transaction.atomic():
                form.save()
                fs.save()
            for row in _requisicion_stock_rows(fs, emp):
                if row["faltante"] is not None and row["faltante"] > 0:
                    messages.warning(
                        request,
                        "Hay líneas con cantidad superior a la existencia en bodega (faltante); "
                        "podrá gestionarse como compra u otro abastecimiento.",
                    )
                    break
            messages.success(request, "Requisición guardada.")
            return redirect("compras:requisicion_list")
    else:
        form = RequisicionForm(instance=req, empresa=emp)
        fs = RequisicionDetalleFormSet(instance=req)
        _filtrar_querysets_detalle(fs, emp)

    ctx = _ctx(request)
    ctx.update(
        {
            "form": form,
            "formset": fs,
            "requisicion": req,
            "titulo": f"Editar {req.numero}",
            "detalle_lineas": list(zip(fs.forms, _requisicion_stock_rows(fs, emp))),
        }
    )
    return render(request, "compras/requisicion_form.html", ctx)


@compras_require_auth
def requisicion_cambiar_estado(request, pk, nuevo_estado):
    emp = _empresa(request)
    if not emp:
        return redirect("compras:compras_menu_principal")
    req = get_object_or_404(Requisicion, pk=pk, empresa=emp)
    
    # Seguridad: solo aprobadores pueden cambiar a ciertos estados
    if nuevo_estado in ["APROBADA", "RECHAZADA"] and not _usuario_es_aprobador(request):
        messages.error(request, "🚫 No tiene permisos de aprobador para realizar esta acción.")
        return redirect("compras:requisicion_edit", pk=pk)

    # Validar que el estado destino sea válido
    if nuevo_estado in [choice[0] for choice in Requisicion.ESTADO_CHOICES]:
        req.estado = nuevo_estado
        req.save(update_fields=["estado"])
        messages.success(request, f"Estatus de requisición {req.numero} actualizado a: {req.get_estado_display()}")
    else:
        messages.error(request, "Estado no válido.")
    return redirect("compras:requisicion_edit", pk=pk)


@compras_require_auth
def orden_compra_list(request):
    emp = _empresa(request)
    ctx = _ctx(request)
    if not emp:
        ctx["sin_empresa"] = True
        ctx["object_list"] = []
        return render(request, "compras/orden_compra_list.html", ctx)
    qs = OrdenCompra.objects.filter(empresa=emp).select_related("ejercicio").order_by("-fecha", "-id")
    ctx["object_list"] = qs
    return render(request, "compras/orden_compra_list.html", ctx)


@compras_require_auth
def orden_compra_cambiar_estado(request, pk, nuevo_estado):
    emp = _empresa(request)
    if not emp:
        messages.error(request, "No tiene empresa asignada.")
        return redirect("compras:orden_compra_list")

    oc = get_object_or_404(OrdenCompra, pk=pk, empresa=emp)

    if nuevo_estado == "APROBADA":
        if not _usuario_es_aprobador(request):
            messages.error(request, "Solo un aprobador puede autorizar la orden de compra.")
            return redirect("compras:orden_compra_edit", pk=oc.pk)
        
        # Integración presupuestaria (creación del Compromiso Automático)
        with transaction.atomic():
            detalles = oc.detalles.select_related('cuenta_presupuestaria').all()
            total_afectable = sum(d.subtotal for d in detalles if d.cuenta_presupuestaria)
            
            if total_afectable > 0:
                from presupuestos.models import Compromiso
                from django.db.models import Max
                
                # Buscar el fondo por defecto o el asignado. Usaremos un fondo por defecto (el primero activo) por simplicidad en este MVP
                # En un caso más complejo, el fondo vendría seleccionado en el detalle de la OC.
                from presupuestos.models import Fondo
                fondo = Fondo.objects.filter(empresa=emp).first()
                
                if not oc.compromiso:
                    # Generar un correlativo para el compromiso
                    max_c = Compromiso.objects.filter(empresa=emp, ejercicio=oc.ejercicio).count()
                    next_c = max_c + 1
                    num_compromiso = f"COMP-{oc.ejercicio.anio}-{next_c:04d}"
                    
                    compromiso = Compromiso.objects.create(
                        empresa=emp,
                        numero=num_compromiso,
                        fecha=oc.fecha,
                        ejercicio=oc.ejercicio,
                        favorecido=oc.proveedor.razon_social,
                        concepto=f"Compromiso generado auto por Orden de Compra {oc.numero}",
                        total=total_afectable,
                        estado="COMPROMETIDO",
                        fondo=fondo
                    )
                    oc.compromiso = compromiso
                else:
                    oc.compromiso.total = total_afectable
                    oc.compromiso.estado = "COMPROMETIDO"
                    oc.compromiso.save()

    elif nuevo_estado == "ANULADA":
        if not (_usuario_es_aprobador(request) or _usuario_es_comprador(request)):
            messages.error(request, "No tiene permisos para anular la orden de compra.")
            return redirect("compras:orden_compra_edit", pk=oc.pk)
            
        with transaction.atomic():
            if oc.compromiso:
                oc.compromiso.estado = "ANULADO"
                oc.compromiso.save()

    oc.estado = nuevo_estado
    oc.save(update_fields=["estado", "compromiso"])
    messages.success(request, f"Estado cambiado a {oc.get_estado_display()}")
    
    return redirect("compras:orden_compra_list")


@compras_require_auth
def orden_compra_create(request):
    if not (_usuario_es_comprador(request) or _usuario_es_aprobador(request)):
        messages.error(request, "No tiene permisos para crear Órdenes de Compra. Debe tener rol de Comprador.")
        return redirect("compras:orden_compra_list")

    emp = _empresa(request)
    if not emp:
        messages.error(
            request,
            "Su sesión no tiene empresa/municipio. Inicie sesión con un usuario municipal o asigne empresa.",
        )
        return redirect("compras:compras_menu_principal")

    if request.method == "POST":
        form = OrdenCompraNuevaForm(request.POST, empresa=emp)
        if form.is_valid():
            vig = _ejercicio_fiscal_vigente(emp)
            if not vig:
                messages.error(
                    request,
                    "No hay ejercicio fiscal vigente (abierto) para su empresa. "
                    "Regístrelo en Contabilidad — Ejercicios fiscales.",
                )
            else:
                oc = form.save(commit=False)
                oc.empresa = emp
                oc.ejercicio = vig
                oc.numero = _siguiente_numero_orden_compra(emp)
                oc.estado = "BORRADOR"
                oc.monto_total = 0
                oc.save()
                messages.success(request, f"Orden de compra {oc.numero} creada. Agregue líneas en editar.")
                return redirect("compras:orden_compra_edit", pk=oc.pk)
    else:
        form = OrdenCompraNuevaForm(empresa=emp, initial={"fecha": date.today()})
    ctx = _ctx(request)
    ctx["form"] = form
    ctx["titulo"] = "Nueva orden de compra"
    ctx["ejercicio_vigente"] = _ejercicio_fiscal_vigente(emp)
    return render(request, "compras/orden_compra_form_nueva.html", ctx)


@compras_require_auth
def orden_compra_edit(request, pk):
    if not (_usuario_es_comprador(request) or _usuario_es_aprobador(request)):
        messages.error(request, "No tiene permisos para modificar Órdenes de Compra.")
        return redirect("compras:orden_compra_list")

    emp = _empresa(request)
    if not emp:
        messages.error(request, "Se requiere empresa en sesión.")
        return redirect("compras:compras_menu_principal")

    oc = get_object_or_404(
        OrdenCompra.objects.select_related("proveedor", "ejercicio", "requisicion", "solicitud_cotizacion"),
        pk=pk,
        empresa=emp,
    )
    if request.method == "POST":
        form = OrdenCompraForm(request.POST, instance=oc, empresa=emp)
        fs = OrdenCompraDetalleFormSet(request.POST, instance=oc)
        _filtrar_querysets_oc_detalle(fs, emp)
        if form.is_valid() and fs.is_valid():
            vig = _ejercicio_fiscal_vigente(emp)
            if not vig:
                messages.error(
                    request,
                    "No hay ejercicio fiscal vigente (abierto) para su empresa. "
                    "Regístrelo en Contabilidad — Ejercicios fiscales.",
                )
            else:
                with transaction.atomic():
                    form.save()
                    fs.save()
                    OrdenCompra.objects.filter(pk=oc.pk).update(ejercicio_id=vig.pk)
                messages.success(
                    request,
                    "Orden de compra guardada. Puede imprimirla o volver al listado desde la vista de impresión.",
                )
                return redirect("compras:orden_compra_imprimir", pk=oc.pk)
    else:
        form = OrdenCompraForm(instance=oc, empresa=emp)
        fs = OrdenCompraDetalleFormSet(instance=oc)
        _filtrar_querysets_oc_detalle(fs, emp)

    ctx = _ctx(request)
    ctx.update(
        {
            "form": form,
            "formset": fs,
            "orden": oc,
            "titulo": f"Editar {oc.numero}",
            "ejercicio_vigente": _ejercicio_fiscal_vigente(emp),
        }
    )
    return render(request, "compras/orden_compra_form.html", ctx)


@compras_require_auth
def orden_compra_imprimir(request, pk):
    """Vista imprimible de la orden de compra (cabecera + líneas)."""
    emp = _empresa(request)
    if not emp:
        messages.error(request, "Se requiere empresa en sesión.")
        return redirect("compras:compras_menu_principal")

    oc = get_object_or_404(
        OrdenCompra.objects.select_related(
            "proveedor",
            "ejercicio",
            "requisicion",
            "solicitud_cotizacion",
            "compromiso",
        ),
        pk=pk,
        empresa=emp,
    )
    detalles = oc.detalles.select_related("inventario", "cuenta_presupuestaria").order_by("nro_linea", "id")
    ctx = _ctx(request)
    ctx.update(
        {
            "orden": oc,
            "detalles": detalles,
            "titulo": f"Orden de compra {oc.numero}",
        }
    )
    return render(request, "compras/orden_compra_imprimir.html", ctx)

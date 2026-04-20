# -*- coding: utf-8 -*-
"""Cotizaciones ONCAE, catálogo materiales/bodega y movimientos de kardex."""
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from contabilidad.models import Inventario, EjercicioFiscal
from presupuestos.models import Compromiso, Fondo

from .forms import (
    InvitacionCotizacionFormSet,
    MovimientoBodegaEntradaForm,
    OfertaProveedorForm,
    SolicitudCotizacionDetalleFormSet,
    SolicitudCotizacionForm,
    SolicitudCotizacionNuevaForm,
    label_inventario_catalogo,
)
from .models import (
    InvitacionCotizacion,
    MovimientoBodega,
    OfertaProveedor,
    OrdenCompraDetalle,
    SolicitudCotizacion,
    SolicitudCotizacionDetalle,
)
from .views import _ctx, _empresa, _ejercicio_fiscal_actual, compras_require_auth


def generar_compromiso_desde_oc(oc):
    """
    Crea automáticamente un Compromiso (Reserva de Fondo) en el módulo de Presupuestos
    basado en la Orden de Compra aprobada.
    """
    if oc.compromiso:
        return oc.compromiso

    ejercicio = oc.ejercicio
    if not ejercicio:
        ejercicio = _ejercicio_fiscal_actual(oc.empresa)
    
    if not ejercicio:
        return None

    # Numero de reserva basado en OC
    reserva_num = f"RES-{oc.numero}"
    
    with transaction.atomic():
        # Crear encabezado de compromiso
        compromiso = Compromiso.objects.create(
            empresa=oc.empresa,
            numero=reserva_num,
            fecha=date.today(),
            ejercicio=ejercicio,
            favorecido=oc.proveedor.razon_social[:200],
            concepto=f"Reserva de fondo por Orden de Compra {oc.numero}. {oc.observaciones or ''}"[:500],
            total=oc.monto_total,
            estado="COMPROMETIDO"
        )
        
        # Vincular a la OC
        oc.compromiso = compromiso
        oc.save(update_fields=["compromiso"])
        
    return compromiso


def _siguiente_numero_solicitud_cotizacion(empresa: str) -> str:
    year = date.today().year
    prefix = f"SC-{year}-"
    ultimos = (
        SolicitudCotizacion.objects.filter(empresa=empresa, numero__startswith=prefix)
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


def _filtrar_querysets_solicitud_detalle(formset, empresa: str):
    if not empresa:
        return
    inv_qs = Inventario.objects.filter(empresa=empresa, is_active=True).order_by(
        "tipo_inventario", "codigo"
    )
    for frm in formset.forms:
        if "inventario" in frm.fields:
            frm.fields["inventario"].queryset = inv_qs
            frm.fields["inventario"].label_from_instance = label_inventario_catalogo
            frm.fields["inventario"].required = False


def _queryset_inventario_entrada_bodega(empresa: str):
    """Catálogo de ítems de inventario para validación POST y búsqueda AJAX."""
    return (
        Inventario.objects.filter(empresa=empresa, is_active=True)
        .select_related("tipo_inventario")
        .order_by("tipo_inventario__orden", "tipo_inventario__nombre", "codigo")
    )


@compras_require_auth
def ajax_buscar_inventario_entrada(request):
    """JSON para Select2: buscar ítem inventario por código, descripción, nomenclatura o tipo."""
    emp = _empresa(request)
    if not emp:
        return JsonResponse({"resultados": []})
    q = (request.GET.get("q") or "").strip()
    qs = _queryset_inventario_entrada_bodega(emp)
    if q:
        qs = qs.filter(
            Q(codigo__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(nomenclatura__icontains=q)
            | Q(tipo_inventario__nombre__icontains=q)
        )
    resultados = [
        {"id": inv.pk, "texto": label_inventario_catalogo(inv)}
        for inv in qs[:50]
    ]
    return JsonResponse({"resultados": resultados})


def _actualizar_inventario_por_movimiento(mov: MovimientoBodega) -> None:
    """Actualiza existencias y costo promedio (NIC 2) según entrada o salida."""
    inv = Inventario.objects.select_for_update().get(pk=mov.inventario_id)
    q0, c0 = inv.cantidad, inv.costo_unitario or Decimal("0")
    q1 = mov.cantidad
    c1 = mov.costo_unitario or Decimal("0")
    if mov.tipo == "ENTRADA":
        qn = q0 + q1
        if qn > 0:
            cn = (q0 * c0 + q1 * c1) / qn
        else:
            cn = c0
    elif mov.tipo == "SALIDA":
        qn = q0 - q1
        if qn < 0:
            raise ValueError("Salida supera existencia en bodega.")
        cn = c0
    else:
        return
    inv.cantidad = qn
    inv.costo_unitario = cn.quantize(Decimal("0.0001"))
    inv.costo_total = (qn * cn).quantize(Decimal("0.01"))
    inv.save(update_fields=["cantidad", "costo_unitario", "costo_total"])


@compras_require_auth
def materiales_bodega_list(request):
    emp = _empresa(request)
    ctx = _ctx(request)
    if not emp:
        ctx["sin_empresa"] = True
        ctx["object_list"] = []
    else:
        ctx["object_list"] = (
            Inventario.objects.filter(empresa=emp, is_active=True)
            .select_related("tipo_inventario")
            .order_by("tipo_inventario__orden", "tipo_inventario__nombre", "codigo")
        )
    return render(request, "compras/materiales_bodega_list.html", ctx)


@compras_require_auth
def solicitud_cotizacion_list(request):
    emp = _empresa(request)
    ctx = _ctx(request)
    if not emp:
        ctx["sin_empresa"] = True
        ctx["object_list"] = []
    else:
        ctx["object_list"] = (
            SolicitudCotizacion.objects.filter(empresa=emp)
            .select_related("requisicion")
            .order_by("-fecha", "-id")
        )
    return render(request, "compras/solicitud_cotizacion_list.html", ctx)


@compras_require_auth
def solicitud_cotizacion_create(request):
    emp = _empresa(request)
    if not emp:
        messages.error(request, "Se requiere empresa en sesión.")
        return redirect("compras:compras_menu_principal")

    req_id = request.GET.get("req")
    initial = {"fecha": date.today()}
    if req_id:
        from .models import Requisicion
        req_obj = Requisicion.objects.filter(pk=req_id, empresa=emp).first()
        if req_obj:
            initial["requisicion"] = req_obj
            initial["observaciones"] = f"Desde Requisición {req_obj.numero}. {req_obj.observaciones or ''}"

    if request.method == "POST":
        form = SolicitudCotizacionNuevaForm(request.POST, empresa=emp)
        if form.is_valid():
            sc = form.save(commit=False)
            sc.empresa = emp
            sc.numero = _siguiente_numero_solicitud_cotizacion(emp)
            sc.estado = "BORRADOR"
            sc.save()
            
            # Si viene de requisición, copiar líneas
            if sc.requisicion:
                for det in sc.requisicion.detalles.all():
                    SolicitudCotizacionDetalle.objects.create(
                        solicitud=sc,
                        nro_linea=det.nro_linea,
                        descripcion=det.descripcion,
                        cantidad=det.cantidad,
                        unidad=det.unidad,
                        inventario=det.inventario
                    )
                messages.success(request, f"Solicitud {sc.numero} creada con {sc.requisicion.detalles.count()} ítems de la requisición.")
            else:
                messages.success(request, f"Solicitud {sc.numero} creada. Complete ítems e invitaciones.")
            
            return redirect("compras:solicitud_cotizacion_edit", pk=sc.pk)
    else:
        form = SolicitudCotizacionNuevaForm(empresa=emp, initial=initial)
    ctx = _ctx(request)
    ctx.update({"form": form, "titulo": "Nueva solicitud de cotización"})
    return render(request, "compras/solicitud_cotizacion_nueva.html", ctx)


@compras_require_auth
def solicitud_cotizacion_edit(request, pk):
    emp = _empresa(request)
    if not emp:
        messages.error(request, "Se requiere empresa en sesión.")
        return redirect("compras:compras_menu_principal")

    sc = get_object_or_404(
        SolicitudCotizacion.objects.select_related("requisicion").prefetch_related(
            Prefetch(
                "detalles",
                queryset=SolicitudCotizacionDetalle.objects.select_related("inventario"),
            )
        ),
        pk=pk,
        empresa=emp,
    )
    if request.method == "POST":
        form = SolicitudCotizacionForm(request.POST, instance=sc, empresa=emp)
        fs_d = SolicitudCotizacionDetalleFormSet(request.POST, instance=sc)
        fs_i = InvitacionCotizacionFormSet(request.POST, instance=sc)
        _filtrar_querysets_solicitud_detalle(fs_d, emp)
        if form.is_valid() and fs_d.is_valid() and fs_i.is_valid():
            with transaction.atomic():
                form.save()
                fs_d.save()
                fs_i.save()
            messages.success(request, "Solicitud de cotización guardada.")
            return redirect("compras:solicitud_cotizacion_list")
    else:
        form = SolicitudCotizacionForm(instance=sc, empresa=emp)
        fs_d = SolicitudCotizacionDetalleFormSet(instance=sc)
        fs_i = InvitacionCotizacionFormSet(instance=sc)
        _filtrar_querysets_solicitud_detalle(fs_d, emp)

    invitaciones = InvitacionCotizacion.objects.filter(solicitud=sc).select_related("proveedor", "oferta")
    ctx = _ctx(request)
    ctx.update(
        {
            "form": form,
            "formset_det": fs_d,
            "formset_inv": fs_i,
            "solicitud": sc,
            "invitaciones": invitaciones,
            "titulo": f"Editar {sc.numero}",
        }
    )
    return render(request, "compras/solicitud_cotizacion_form.html", ctx)


@compras_require_auth
def solicitud_cotizacion_imprimir_oncae(request, pk):
    emp = _empresa(request)
    if not emp:
        return redirect("compras:compras_menu_principal")
    sc = get_object_or_404(
        SolicitudCotizacion.objects.select_related("requisicion").prefetch_related(
            Prefetch("detalles", queryset=SolicitudCotizacionDetalle.objects.select_related("inventario"))
        ),
        pk=pk,
        empresa=emp,
    )
    invitaciones = InvitacionCotizacion.objects.filter(solicitud=sc).select_related("proveedor")
    ctx = _ctx(request)
    ctx.update({"solicitud": sc, "invitaciones": invitaciones, "titulo": f"Formato convocatoria {sc.numero}"})
    return render(request, "compras/solicitud_cotizacion_oncae_print.html", ctx)


@compras_require_auth
def invitacion_oferta_edit(request, pk):
    emp = _empresa(request)
    inv = get_object_or_404(
        InvitacionCotizacion.objects.select_related("solicitud", "proveedor"),
        pk=pk,
        solicitud__empresa=emp,
    )
    oferta = OfertaProveedor.objects.filter(invitacion=inv).first()
    if request.method == "POST":
        form = OfertaProveedorForm(request.POST, instance=oferta)
        if form.is_valid():
            o = form.save(commit=False)
            o.invitacion = inv
            o.save()
            if o.es_seleccionada:
                OfertaProveedor.objects.filter(invitacion__solicitud_id=inv.solicitud_id).exclude(pk=o.pk).update(
                    es_seleccionada=False
                )
            inv.estado = "RECIBIDA"
            inv.save(update_fields=["estado"])
            messages.success(request, "Oferta registrada.")
            return redirect("compras:solicitud_cotizacion_edit", pk=inv.solicitud_id)
    else:
        initial = {} if oferta else {"fecha_recepcion": date.today()}
        form = OfertaProveedorForm(instance=oferta, initial=initial)
    ctx = _ctx(request)
    ctx.update({"form": form, "invitacion": inv, "oferta": oferta, "titulo": f"Oferta — {inv.proveedor}"})
    return render(request, "compras/invitacion_oferta_form.html", ctx)


@compras_require_auth
def generar_oc_desde_oferta(request, pk):
    """
    Crea una Orden de Compra (OC) basada en una Oferta de Proveedor seleccionada.
    """
    emp = _empresa(request)
    if not emp:
        return redirect("compras:compras_menu_principal")
    
    # Seguridad: solo aprobadores pueden generar OC definitivas
    if not _usuario_es_aprobador(request):
        messages.error(request, "🚫 No tiene permisos para generar Órdenes de Compra.")
        return redirect("compras:solicitud_cotizacion_edit", pk=pk) # pk es de la SC

    sc = get_object_or_404(SolicitudCotizacion, pk=pk, empresa=emp)
    oferta_ganadora = OfertaProveedor.objects.filter(invitacion__solicitud=sc, es_seleccionada=True).first()
    
    if not oferta_ganadora:
        messages.error(request, "Debe seleccionar una oferta como ganadora antes de generar la OC.")
        return redirect("compras:solicitud_cotizacion_edit", pk=pk)

    from .models import OrdenCompra, OrdenCompraDetalle
    from .views import _siguiente_numero_orden_compra

    with transaction.atomic():
        oc = OrdenCompra.objects.create(
            empresa=emp,
            numero=_siguiente_numero_orden_compra(emp),
            fecha=date.today(),
            proveedor=oferta_ganadora.invitacion.proveedor,
            ejercicio=sc.requisicion.ejercicio if sc.requisicion else _ejercicio_fiscal_actual(emp),
            requisicion=sc.requisicion,
            solicitud_cotizacion=sc,
            monto_total=oferta_ganadora.monto_total,
            estado="BORRADOR",
            observaciones=f"Generada desde Cotización {sc.numero}. Oferta seleccionada: {oferta_ganadora.notas or ''}"
        )
        
        # Copiar líneas de la SC (o de la oferta si tuviera detalles, pero SC ya tiene los items)
        for det in sc.detalles.all():
            OrdenCompraDetalle.objects.create(
                orden=oc,
                nro_linea=det.nro_linea,
                descripcion=det.descripcion,
                cantidad=det.cantidad,
                inventario=det.inventario,
                precio_unitario=0 # El usuario deberá revisar precios finales en la OC
            )
        
        sc.estado = "CERRADA"
        sc.save(update_fields=["estado"])

    messages.success(request, f"Orden de Compra {oc.numero} generada exitosamente desde la oferta ganadora.")
    return redirect("compras:orden_compra_edit", pk=oc.pk)


@compras_require_auth
def orden_compra_recibir(request, pk):
    """
    Interfaz para registrar la recepción física de materiales de una OC.
    Permite el ingreso parcial o total de los ítems.
    """
    emp = _empresa(request)
    if not emp:
        return redirect("compras:compras_menu_principal")
    
    oc = get_object_or_404(
        OrdenCompra.objects.prefetch_related(
            Prefetch(
                "detalles",
                queryset=OrdenCompraDetalle.objects.select_related("inventario").prefetch_related("movimientos_bodega")
            )
        ),
        pk=pk, 
        empresa=emp
    )

    if request.method == "POST":
        cantidades = request.POST.getlist("cantidad_recibida")
        detalle_ids = request.POST.getlist("detalle_id")
        referencia = request.POST.get("referencia", f"Rec. OC {oc.numero}")
        
        recepciones_ok = 0
        with transaction.atomic():
            for idx, d_id in enumerate(detalle_ids):
                det = get_object_or_404(OrdenCompraDetalle, pk=d_id, orden=oc)
                cant_txt = cantidades[idx] if idx < len(cantidades) else "0"
                
                try:
                    cant = Decimal(cant_txt)
                except (ValueError, TypeError):
                    continue
                
                if cant <= 0:
                    continue
                
                if not det.inventario:
                    messages.warning(request, f"El ítem '{det.descripcion}' no tiene vínculo con inventario. No se pudo ingresar a bodega.")
                    continue

                # Crear movimiento de bodega
                mov = MovimientoBodega.objects.create(
                    empresa=emp,
                    fecha=date.today(),
                    fecha_compra=oc.fecha,
                    tipo="ENTRADA",
                    inventario=det.inventario,
                    cantidad=cant,
                    costo_unitario=det.precio_unitario,
                    orden_detalle=det,
                    referencia=referencia,
                    notas=f"Recepción parcial/total de OC {oc.numero}"
                )
                _actualizar_inventario_por_movimiento(mov)
                recepciones_ok += 1
            
            # Verificar si la OC está totalmente recibida
            # (Simplificación: si se recibió algo, actualizamos estado. Un control más fino compararía cantidades totales)
            if recepciones_ok > 0:
                oc.estado = "RECIBIDA"
                oc.save(update_fields=["estado"])
                messages.success(request, f"Se registraron {recepciones_ok} ingresos a bodega desde la OC {oc.numero}.")
            else:
                messages.warning(request, "No se registraron ingresos (cantidades en cero o inválidas).")
                
        return redirect("compras:orden_compra_edit", pk=oc.pk)

    detalles_con_saldo = []
    for d in oc.detalles.all():
        recibido = d.movimientos_bodega.aggregate(s=Sum("cantidad"))["s"] or Decimal("0")
        pendiente = d.cantidad - recibido
        detalles_con_saldo.append({
            "det": d,
            "recibido": recibido,
            "pendiente": pendiente if pendiente > 0 else 0
        })

    ctx = _ctx(request)
    ctx.update({
        "orden": oc,
        "detalles": detalles_con_saldo,
        "titulo": f"Recepción de Bodega - OC {oc.numero}"
    })
    return render(request, "compras/recepcion_oc.html", ctx)


@compras_require_auth
def movimiento_bodega_list(request):
    emp = _empresa(request)
    ctx = _ctx(request)
    if not emp:
        ctx["sin_empresa"] = True
        ctx["object_list"] = []
    else:
        ctx["object_list"] = (
            MovimientoBodega.objects.filter(empresa=emp)
            .select_related("inventario", "orden_detalle", "orden_detalle__orden")
            .order_by("-fecha", "-id")[:500]
        )
    return render(request, "compras/movimiento_bodega_list.html", ctx)


@compras_require_auth
def movimiento_bodega_entrada(request):
    emp = _empresa(request)
    if not emp:
        messages.error(request, "Se requiere empresa en sesión.")
        return redirect("compras:compras_menu_principal")

    if request.method == "POST":
        form = MovimientoBodegaEntradaForm(request.POST, empresa=emp)
        form.fields["inventario"].queryset = _queryset_inventario_entrada_bodega(emp)
        if form.is_valid():
            try:
                with transaction.atomic():
                    mov = form.save(commit=False)
                    mov.empresa = emp
                    mov.tipo = "ENTRADA"
                    if not mov.fecha_compra:
                        mov.fecha_compra = mov.fecha
                    mov.save()
                    _actualizar_inventario_por_movimiento(mov)
            except ValueError as e:
                messages.error(request, str(e))
            else:
                messages.success(request, "Entrada a bodega registrada; existencias actualizadas.")
                return redirect("compras:movimiento_bodega_list")
        else:
            inv_raw = (request.POST.get("inventario") or "").strip()
            if inv_raw.isdigit():
                form.fields["inventario"].queryset = (
                    Inventario.objects.filter(pk=int(inv_raw), empresa=emp, is_active=True).select_related(
                        "tipo_inventario"
                    )
                )
            else:
                form.fields["inventario"].queryset = Inventario.objects.none()
    else:
        form = MovimientoBodegaEntradaForm(
            empresa=emp,
            initial={"fecha": date.today(), "fecha_compra": date.today()},
        )
        form.fields["inventario"].queryset = Inventario.objects.none()
    ctx = _ctx(request)
    ctx.update({"form": form, "titulo": "Entrada a bodega (desde compras)"})
    return render(request, "compras/movimiento_bodega_entrada.html", ctx)

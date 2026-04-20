from django.contrib import admin

from .models import (
    InvitacionCotizacion,
    MovimientoBodega,
    OfertaProveedor,
    OrdenCompra,
    OrdenCompraDetalle,
    Requisicion,
    RequisicionDetalle,
    SolicitudCotizacion,
)


class RequisicionDetalleInline(admin.TabularInline):
    model = RequisicionDetalle
    extra = 0


@admin.register(Requisicion)
class RequisicionAdmin(admin.ModelAdmin):
    list_display = ("numero", "empresa", "fecha", "estado")
    list_filter = ("estado", "empresa")
    inlines = [RequisicionDetalleInline]


class OrdenCompraDetalleInline(admin.TabularInline):
    model = OrdenCompraDetalle
    extra = 0


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ("numero", "empresa", "fecha", "proveedor", "estado", "monto_total")
    list_filter = ("estado", "empresa")
    inlines = [OrdenCompraDetalleInline]


class InvitacionInline(admin.TabularInline):
    model = InvitacionCotizacion
    extra = 0


@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    list_display = ("numero", "empresa", "fecha", "estado")
    inlines = [InvitacionInline]


@admin.register(InvitacionCotizacion)
class InvitacionCotizacionAdmin(admin.ModelAdmin):
    list_display = ("solicitud", "proveedor", "estado")


@admin.register(OfertaProveedor)
class OfertaProveedorAdmin(admin.ModelAdmin):
    list_display = ("invitacion", "fecha_recepcion", "monto_total", "es_seleccionada")


@admin.register(MovimientoBodega)
class MovimientoBodegaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "fecha_compra", "empresa", "tipo", "inventario", "cantidad")

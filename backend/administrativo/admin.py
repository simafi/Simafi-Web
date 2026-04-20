from django.contrib import admin

from .models import ContratoAdministrativo, ExpedienteGestion, Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'empresa', 'nit', 'doc_digital', 'activo')

    @admin.display(description='Doc.', boolean=True)
    def doc_digital(self, obj):
        return obj.documentacion_cargada
    list_filter = ('empresa', 'activo')
    search_fields = ('razon_social', 'nit', 'email')


@admin.register(ContratoAdministrativo)
class ContratoAdministrativoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'empresa', 'proveedor', 'estado', 'fecha_inicio', 'fecha_fin', 'monto_estimado')
    list_filter = ('empresa', 'estado')
    search_fields = ('numero', 'descripcion')


@admin.register(ExpedienteGestion)
class ExpedienteGestionAdmin(admin.ModelAdmin):
    list_display = ('codigo_interno', 'titulo', 'empresa', 'tipo', 'estado', 'fecha_apertura')
    list_filter = ('empresa', 'tipo', 'estado')
    search_fields = ('codigo_interno', 'titulo', 'descripcion')

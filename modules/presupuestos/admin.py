from django.contrib import admin
from .models import PresupuestoIngresos, PresupuestoGastos, EjecucionPresupuestaria, ModificacionPresupuestaria


@admin.register(PresupuestoIngresos)
class PresupuestoIngresosAdmin(admin.ModelAdmin):
    list_display = ['ano', 'fuente_ingreso', 'monto_presupuestado', 'monto_ejecutado', 'fecha_modificacion']
    list_filter = ['ano', 'fecha_creacion']
    search_fields = ['fuente_ingreso', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']


@admin.register(PresupuestoGastos)
class PresupuestoGastosAdmin(admin.ModelAdmin):
    list_display = ['ano', 'categoria_gasto', 'subcategoria', 'monto_presupuestado', 'monto_ejecutado', 'fecha_modificacion']
    list_filter = ['ano', 'categoria_gasto', 'fecha_creacion']
    search_fields = ['categoria_gasto', 'subcategoria', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']


@admin.register(EjecucionPresupuestaria)
class EjecucionPresupuestariaAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'fecha_ejecucion', 'monto', 'descripcion', 'fecha_creacion']
    list_filter = ['tipo', 'fecha_ejecucion', 'fecha_creacion']
    search_fields = ['descripcion', 'documento_referencia']
    readonly_fields = ['fecha_creacion']


@admin.register(ModificacionPresupuestaria)
class ModificacionPresupuestariaAdmin(admin.ModelAdmin):
    list_display = ['tipo_modificacion', 'presupuesto_origen', 'presupuesto_destino', 'monto', 'fecha_modificacion']
    list_filter = ['tipo_modificacion', 'fecha_modificacion', 'fecha_creacion']
    search_fields = ['justificacion', 'documento_aprobacion']
    readonly_fields = ['fecha_creacion']
from django.contrib import admin
from .models import Municipio, Departamento, SystemConfig, AuditLog, Oficina


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    list_filter = ('codigo',)
    search_fields = ('codigo', 'descripcion')
    ordering = ('codigo',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'depto', 'descripcion')
    list_filter = ('depto',)
    search_fields = ('depto', 'descripcion')
    ordering = ('depto',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('depto', 'descripcion')
        }),
    )


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'municipio')
    list_filter = ('municipio',)
    search_fields = ('key', 'value', 'description')
    ordering = ('key',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'created_at')
    list_filter = ('action', 'model_name', 'created_at', 'municipio')
    search_fields = ('user', 'model_name', 'details')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'municipio', 'telefono')
    list_filter = ('municipio',)
    search_fields = ('codigo', 'descripcion', 'direccion')
    ordering = ('municipio', 'codigo')
































































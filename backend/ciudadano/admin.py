from django.contrib import admin

from .models import SolicitudTramite


@admin.register(SolicitudTramite)
class SolicitudTramiteAdmin(admin.ModelAdmin):
    list_display = (
        "referencia",
        "tipo_tramite",
        "identificacion",
        "nombre_completo",
        "estado",
        "fecha_respuesta",
        "empresa",
        "created_at",
    )
    list_filter = ("estado", "tipo_tramite", "empresa")
    search_fields = ("referencia", "identificacion", "nombre_completo", "detalle", "respuesta_municipal")
    readonly_fields = ("referencia", "created_at", "updated_at")

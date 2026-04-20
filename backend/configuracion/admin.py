from django.contrib import admin

from . import models


def _non_pk_field_names(m):
    return [f.name for f in m._meta.fields if not f.primary_key]


class CatalogoPredioAdmin(admin.ModelAdmin):
    """list_display según columnas reales del modelo."""

    def __init__(self, model, admin_site):
        self.list_display = tuple(_non_pk_field_names(model)[:10])
        self.search_fields = tuple(
            f.name for f in model._meta.fields
            if not f.primary_key and f.get_internal_type() in ('CharField', 'TextField')
        )
        self.ordering = tuple(model._meta.ordering) if model._meta.ordering else ('pk',)
        super().__init__(model, admin_site)


@admin.register(models.Sitio)
class SitioAdmin(CatalogoPredioAdmin):
    pass


_CATALOGO_PREDIO_MODELS = (
    models.Habitacional,
    models.Agua,
    models.Alumbrado,
    models.Calle,
    models.Colindancias,
    models.Dominio,
    models.Drenaje,
    models.Electricidad,
    models.Explotacion,
    models.Irrigacion,
    models.Naturaleza,
    models.CfgSubuso,
    models.Telefono,
    models.Tipomedida,
    models.CfgTopografia,
    models.Usotierra,
    models.Vias,
    models.Zonasusos,
)

for _model in _CATALOGO_PREDIO_MODELS:
    admin.site.register(_model, CatalogoPredioAdmin)

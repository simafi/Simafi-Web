# -*- coding: utf-8 -*-
"""Catálogos de predio (código + descripción): registro para vistas genéricas y menú."""
from django.http import Http404

from . import models

# Orden del menú: clave URL, modelo, título corto, icono Font Awesome (clase sin prefijo fa-)
CATALOGO_PREDIO_ITEMS = [
    ('habitacional', models.Habitacional, 'Código habitacional', 'home'),
    ('agua', models.Agua, 'Agua', 'tint'),
    ('alumbrado', models.Alumbrado, 'Alumbrado', 'lightbulb'),
    ('calle', models.Calle, 'Calle', 'road'),
    ('colindancias', models.Colindancias, 'Colindancias', 'vector-square'),
    ('dominio', models.Dominio, 'Tipo de dominio', 'file-signature'),
    ('drenaje', models.Drenaje, 'Alcantarillado', 'toilet'),
    ('electricidad', models.Electricidad, 'Electricidad', 'bolt'),
    ('explotacion', models.Explotacion, 'Explotación del predio', 'industry'),
    ('irrigacion', models.Irrigacion, 'Sistema de irrigación', 'seedling'),
    ('naturaleza', models.Naturaleza, 'Naturaleza jurídica', 'balance-scale'),
    ('subuso', models.CfgSubuso, 'Uso del predio', 'layer-group'),
    ('telefono', models.Telefono, 'Teléfono', 'phone'),
    ('tipomedida', models.Tipomedida, 'Tipo de medida', 'ruler'),
    ('topografia', models.CfgTopografia, 'Topografía del predio', 'mountain'),
    ('usotierra', models.Usotierra, 'Uso de tierra', 'globe-americas'),
    ('vias', models.Vias, 'Vías de comunicación', 'route'),
    ('zonasusos', models.Zonasusos, 'Zonificación', 'map-marked-alt'),
]

CATALOGO_BY_CLAVE = {row[0]: {'model': row[1], 'titulo': row[2], 'icon': row[3]} for row in CATALOGO_PREDIO_ITEMS}

# Campo HTML (nombre del campo Django) que dispara la búsqueda AJAX al escribir
AJAX_LOOKUP_TRIGGER_FIELD = {
    'subuso': 'codsubuso',
    'topografia': 'cotopo',
}


def get_catalogo_predio(clave: str):
    """Devuelve metadatos del catálogo o lanza Http404."""
    if clave not in CATALOGO_BY_CLAVE:
        raise Http404('Catálogo no encontrado')
    return CATALOGO_BY_CLAVE[clave]

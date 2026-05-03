# -*- coding: utf-8 -*-
"""
Mapas digitales en Catastro — modelo práctico para digitalización vectorial.

- Las geometrías se guardan como GeoJSON (RFC 7946) en JSONField: portable entre
  PostgreSQL y otros motores, y compatible con Leaflet/OpenLayers sin GDAL en el servidor.
- En PostgreSQL puede habilitarse PostGIS (`CREATE EXTENSION postgis`) y usar consultas
  espaciales sobre el mismo GeoJSON, por ejemplo:
    SELECT id FROM catastro_mapa_elemento
    WHERE geom IS NOT NULL;  -- si se añade columna generada en migración avanzada
  o bien ST_GeomFromGeoJSON(geometria::text) en SQL crudo desde la aplicación.

Ver: https://postgis.net/docs/ST_GeomFromGeoJSON.html
"""
from django.db import models


class MapaProyecto(models.Model):
    """Proyecto de mapa por municipio (empresa de sesión). Agrupa capas y elementos."""

    empresa = models.CharField(max_length=4, db_index=True, verbose_name='Empresa / municipio')
    nombre = models.CharField(max_length=200, verbose_name='Nombre del mapa')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    # EPSG habitual: 4326 (WGS84 lat/lng para Leaflet); 32616 UTM zona 16N (Honduras).
    srid = models.PositiveIntegerField(
        default=4326,
        verbose_name='SRID (EPSG)',
        help_text='Sistema de coordenadas de referencia, ej. 4326 WGS84',
    )
    usuario_creacion = models.CharField(max_length=80, blank=True, verbose_name='Usuario')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        app_label = 'catastro'
        db_table = 'catastro_mapa_proyecto'
        verbose_name = 'Proyecto de mapa'
        verbose_name_plural = 'Proyectos de mapas'
        ordering = ['-actualizado_en', 'nombre']
        indexes = [
            models.Index(fields=['empresa', 'activo'], name='catastro_mapa_proj_emp_act'),
        ]

    def __str__(self):
        return f'{self.nombre} ({self.empresa})'


class MapaCapa(models.Model):
    """Capa temática dentro de un proyecto (polígonos, líneas, puntos en un mismo mapa)."""

    proyecto = models.ForeignKey(
        MapaProyecto,
        related_name='capas',
        on_delete=models.CASCADE,
        verbose_name='Proyecto',
    )
    nombre = models.CharField(max_length=120, verbose_name='Nombre de la capa')
    orden = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    color_linea = models.CharField(max_length=32, default='#2563eb', verbose_name='Color línea')
    color_relleno = models.CharField(max_length=32, default='#2563eb', verbose_name='Color relleno')
    opacidad_relleno = models.FloatField(default=0.25, verbose_name='Opacidad relleno (0–1)')
    visible = models.BooleanField(default=True, verbose_name='Visible')

    class Meta:
        app_label = 'catastro'
        db_table = 'catastro_mapa_capa'
        verbose_name = 'Capa de mapa'
        verbose_name_plural = 'Capas de mapa'
        ordering = ['orden', 'id']

    def __str__(self):
        return f'{self.nombre}'


class MapaElemento(models.Model):
    """
    Entidad geográfica dibujada: geometría GeoJSON + propiedades libres (clave/valor).
    Tipos habituales: Point, LineString, Polygon, MultiPolygon.
    """

    capa = models.ForeignKey(
        MapaCapa,
        related_name='elementos',
        on_delete=models.CASCADE,
        verbose_name='Capa',
    )
    etiqueta = models.CharField(max_length=200, blank=True, verbose_name='Etiqueta')
    geometria = models.JSONField(verbose_name='Geometría (GeoJSON)')
    propiedades = models.JSONField(default=dict, blank=True, verbose_name='Propiedades')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'catastro'
        db_table = 'catastro_mapa_elemento'
        verbose_name = 'Elemento del mapa'
        verbose_name_plural = 'Elementos del mapa'
        indexes = [
            models.Index(fields=['capa'], name='catastro_mapa_elem_capa'),
        ]

    def __str__(self):
        return self.etiqueta or f'Elemento #{self.pk}'

# -*- coding: utf-8 -*-
"""Vistas del submódulo Mapas Simafi — listado, editor y API GeoJSON."""
import json
import logging

from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from catastro.decorators import catastro_require_permiso
from catastro.models_mapas import MapaCapa, MapaElemento, MapaProyecto
from catastro.permisos_codigos import CATASTRO_PERM_MAPA_VER
from catastro.views import catastro_require_auth

logger = logging.getLogger(__name__)


def _empresa_session(request):
    return (request.session.get('catastro_empresa') or request.session.get('empresa') or '').strip()


def _usuario_nombre(request):
    return request.session.get('catastro_usuario_nombre') or request.session.get('usuario_nombre') or ''


@catastro_require_auth
@catastro_require_permiso(CATASTRO_PERM_MAPA_VER)
def mapas_simafi_list(request):
    """Listado de proyectos de mapa del municipio en sesión."""
    empresa = _empresa_session(request)
    proyectos = []
    if empresa:
        proyectos = MapaProyecto.objects.filter(empresa=empresa, activo=True).order_by('-actualizado_en')

    if request.method == 'POST' and empresa:
        nombre = (request.POST.get('nombre') or '').strip()
        if nombre:
            MapaProyecto.objects.create(
                empresa=empresa,
                nombre=nombre[:200],
                descripcion=(request.POST.get('descripcion') or '').strip()[:2000],
                usuario_creacion=_usuario_nombre(request)[:80],
            )
            return redirect('catastro:mapas_simafi_list')

    ctx = {
        'titulo': 'Mapas Simafi — Digitalización',
        'modulo': 'Catastro — Mapas',
        'empresa': empresa,
        'proyectos': proyectos,
        'usuario_nombre': _usuario_nombre(request),
        'municipio_descripcion': request.session.get('catastro_municipio_descripcion', ''),
    }
    return render(request, 'mapas_simafi/list.html', ctx)


@catastro_require_auth
@catastro_require_permiso(CATASTRO_PERM_MAPA_VER)
def mapas_simafi_editor(request, proyecto_id):
    """Editor Leaflet: dibuja y guarda elementos GeoJSON por capa."""
    empresa = _empresa_session(request)
    proyecto = get_object_or_404(MapaProyecto, pk=proyecto_id, empresa=empresa, activo=True)
    capas = proyecto.capas.all().order_by('orden', 'id')
    capas_info = [
        {
            'id': c.id,
            'nombre': c.nombre,
            'color_linea': c.color_linea,
            'color_relleno': c.color_relleno,
            'opacidad_relleno': float(c.opacidad_relleno),
        }
        for c in capas
    ]
    ctx = {
        'proyecto': proyecto,
        'capas': capas,
        'capas_info': capas_info,
        'titulo': f'Mapa: {proyecto.nombre}',
        'usuario_nombre': _usuario_nombre(request),
        'municipio_descripcion': request.session.get('catastro_municipio_descripcion', ''),
    }
    return render(request, 'mapas_simafi/editor.html', ctx)


def _feature_collection(proyecto):
    features = []
    for capa in proyecto.capas.all().order_by('orden', 'id'):
        for el in capa.elementos.all():
            try:
                geom = el.geometria
                if not isinstance(geom, dict) or 'type' not in geom:
                    continue
                props = dict(el.propiedades or {})
                props.setdefault('_capa_id', capa.id)
                props.setdefault('_capa_nombre', capa.nombre)
                props.setdefault('_elemento_id', el.id)
                props.setdefault('etiqueta', el.etiqueta)
                features.append({'type': 'Feature', 'geometry': geom, 'properties': props})
            except Exception as e:
                logger.warning('GeoJSON skip elemento %s: %s', el.pk, e)
    return {'type': 'FeatureCollection', 'features': features}


@catastro_require_auth
@catastro_require_permiso(CATASTRO_PERM_MAPA_VER)
def api_mapas_geojson(request, proyecto_id):
    empresa = _empresa_session(request)
    proyecto = get_object_or_404(MapaProyecto, pk=proyecto_id, empresa=empresa, activo=True)
    return JsonResponse(_feature_collection(proyecto))


@catastro_require_auth
@catastro_require_permiso(CATASTRO_PERM_MAPA_VER)
@require_http_methods(['POST'])
def api_mapas_elemento_guardar(request, proyecto_id):
    empresa = _empresa_session(request)
    proyecto = get_object_or_404(MapaProyecto, pk=proyecto_id, empresa=empresa, activo=True)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    capa_id = payload.get('capa_id')
    elemento_id = payload.get('elemento_id')
    geometria = payload.get('geometry') or payload.get('geometria')
    etiqueta = (payload.get('etiqueta') or '')[:200]
    propiedades = payload.get('properties') or payload.get('propiedades') or {}
    if not isinstance(propiedades, dict):
        propiedades = {}

    if not geometria or not isinstance(geometria, dict):
        return JsonResponse({'ok': False, 'error': 'Falta geometry (GeoJSON)'}, status=400)
    gtype = geometria.get('type')
    if gtype not in ('Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon'):
        return JsonResponse({'ok': False, 'error': 'Tipo de geometría no soportado'}, status=400)

    capa = None
    if capa_id:
        capa = MapaCapa.objects.filter(pk=capa_id, proyecto=proyecto).first()
    if capa is None:
        capa = MapaCapa.objects.filter(proyecto=proyecto, nombre='Digitalización').first()
        if capa is None:
            capa = MapaCapa.objects.create(
                proyecto=proyecto,
                nombre='Digitalización',
                orden=0,
                visible=True,
            )

    if elemento_id:
        el = MapaElemento.objects.filter(pk=elemento_id, capa__proyecto=proyecto).first()
        if not el:
            return JsonResponse({'ok': False, 'error': 'Elemento no encontrado'}, status=404)
        el.capa = capa
        el.etiqueta = etiqueta
        el.geometria = geometria
        el.propiedades = propiedades
        el.save()
        return JsonResponse({'ok': True, 'elemento_id': el.id, 'capa_id': capa.id})

    el = MapaElemento.objects.create(
        capa=capa,
        etiqueta=etiqueta,
        geometria=geometria,
        propiedades=propiedades,
    )
    return JsonResponse({'ok': True, 'elemento_id': el.id, 'capa_id': capa.id})


@catastro_require_auth
@catastro_require_permiso(CATASTRO_PERM_MAPA_VER)
@require_http_methods(['POST'])
def api_mapas_elemento_eliminar(request, proyecto_id):
    empresa = _empresa_session(request)
    proyecto = get_object_or_404(MapaProyecto, pk=proyecto_id, empresa=empresa, activo=True)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)
    eid = payload.get('elemento_id')
    if not eid:
        return JsonResponse({'ok': False, 'error': 'elemento_id requerido'}, status=400)
    deleted, _ = MapaElemento.objects.filter(pk=eid, capa__proyecto=proyecto).delete()
    return JsonResponse({'ok': bool(deleted)})


@catastro_require_auth
@catastro_require_permiso(CATASTRO_PERM_MAPA_VER)
@require_http_methods(['POST'])
def api_mapas_capa_crear(request, proyecto_id):
    empresa = _empresa_session(request)
    proyecto = get_object_or_404(MapaProyecto, pk=proyecto_id, empresa=empresa, activo=True)
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        payload = {}
    nombre = (payload.get('nombre') or request.POST.get('nombre') or 'Nueva capa').strip()[:120]
    max_orden = proyecto.capas.aggregate(m=Max('orden'))['m']
    orden = (max_orden or 0) + 1
    capa = MapaCapa.objects.create(
        proyecto=proyecto,
        nombre=nombre,
        orden=orden,
        color_linea=payload.get('color_linea') or '#2563eb',
        color_relleno=payload.get('color_relleno') or '#2563eb',
    )
    return JsonResponse({'ok': True, 'capa_id': capa.id, 'nombre': capa.nombre})

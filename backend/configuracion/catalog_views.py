# -*- coding: utf-8 -*-
"""Vistas genéricas para catálogos de predio (tablas reales MySQL)."""
from datetime import datetime
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import models as cfg_models
from .catalog_registry import AJAX_LOOKUP_TRIGGER_FIELD, get_catalogo_predio
from .export_helpers import build_http_excel, build_http_pdf, queryset_to_matrix
from .sistema_general_forms import catalogo_predio_form
from .sistema_general_views import (
    _NOTA_CODIGO_EXISTENTE,
    api_sistema_require_auth,
    sistema_require_auth,
)


def _catalog_field_names(model):
    return [f.name for f in model._meta.fields if not f.primary_key]


def _search_q(model, term):
    """Búsqueda OR en campos de texto."""
    if not term:
        return Q()
    q = Q()
    for f in model._meta.fields:
        if f.primary_key:
            continue
        t = f.get_internal_type()
        if t in ('CharField', 'TextField'):
            q |= Q(**{f'{f.name}__icontains': term})
    return q


def _ordering(model):
    o = model._meta.ordering
    if o:
        return list(o)
    return ['pk']


def _existente_por_post(model, post):
    """Registro existente por clave natural (para actualizar en lugar de duplicar)."""
    if model is cfg_models.CfgSubuso:
        uso = (post.get('uso') or '').strip()
        if not uso:
            return None
        cs = (post.get('codsubuso') or '').strip()
        qs = model.objects.filter(uso=uso)
        if cs:
            return qs.filter(codsubuso=cs).first()
        return qs.filter(Q(codsubuso='') | Q(codsubuso__isnull=True)).first()

    if model is cfg_models.CfgTopografia:
        co = (post.get('cotopo') or '').strip()
        if not co:
            return None
        emp = (post.get('empresa') or '').strip()
        qs = model.objects.filter(cotopo=co)
        if emp:
            return qs.filter(empresa=emp).first()
        return qs.filter(Q(empresa='') | Q(empresa__isnull=True)).first()

    if 'codigo' not in _catalog_field_names(model):
        return None

    raw = post.get('codigo')
    if raw is None or (isinstance(raw, str) and raw.strip() == ''):
        return None

    field = model._meta.get_field('codigo')
    if field.get_internal_type() == 'DecimalField':
        try:
            val = Decimal(str(raw).strip())
        except (InvalidOperation, ValueError):
            return None
        return model.objects.filter(codigo=val).first()

    return model.objects.filter(codigo=str(raw).strip()).first()


def _serialize_catalog_obj(obj):
    out = {}
    for f in obj._meta.fields:
        if f.primary_key:
            continue
        v = getattr(obj, f.name)
        if v is None:
            out[f.name] = ''
        elif hasattr(v, 'isoformat'):
            out[f.name] = v.isoformat()
        elif isinstance(v, Decimal):
            out[f.name] = format(v, 'f')
        else:
            out[f.name] = str(v)
    return out


def _ajax_lookup_config_catastro(request, clave: str):
    """Config JSON para geo_form: búsqueda AJAX; subuso requiere ?uso= y dispara por codsubuso."""
    trigger = AJAX_LOOKUP_TRIGGER_FIELD.get(clave, 'codigo')
    cfg = {
        'url': reverse('configuracion:api_lookup_catalogo_catastro', kwargs={'clave': clave}),
        'mode': 'catalogo_catastro',
        'triggerField': trigger,
    }
    if clave == 'subuso':
        uso_ctx = (request.GET.get('uso') or '').strip()
        if uso_ctx:
            cfg['usoFiltro'] = uso_ctx
    return cfg


def _uso_padre_descripcion(uso_cod: str) -> str:
    if not uso_cod:
        return ''
    try:
        from catastro.models import Usos

        u = Usos.objects.filter(uso=uso_cod).first()
        return (u.desuso or '') if u else ''
    except Exception:
        return ''


def _subuso_uso_get(request) -> str:
    return (request.GET.get('uso') or '').strip()


def _subuso_extra_query(uso: str) -> str:
    if not uso:
        return ''
    return '?' + urlencode({'uso': uso})


def _export_querystring(request):
    q = request.GET.urlencode()
    return f'?{q}' if q else ''


def _redirect_catalog_list_preserve_get(request, clave: str):
    url = reverse('configuracion:catalogo_catastro_list', kwargs={'clave': clave})
    if request.GET:
        url = f'{url}?{request.GET.urlencode()}'
    return redirect(url)


def _redirect_subuso_list(uso: str):
    base = reverse('configuracion:catalogo_catastro_list', kwargs={'clave': 'subuso'})
    if uso:
        return redirect(f'{base}?{urlencode({"uso": uso})}')
    return redirect('catastro:usos_predio_list')


def _objeto_etiqueta_editar(obj):
    if hasattr(obj, 'codigo') and obj.codigo is not None:
        return str(obj.codigo)
    if hasattr(obj, 'uso'):
        return f'{obj.uso} {getattr(obj, "codsubuso", "") or ""}'.strip()
    if hasattr(obj, 'cotopo'):
        return f'{getattr(obj, "empresa", "") or ""} {obj.cotopo}'.strip()
    return str(obj)[:80]


@sistema_require_auth
def catalogo_catastro_list(request, clave: str):
    cfg = get_catalogo_predio(clave)
    model = cfg['model']
    uso_filtro = ''
    uso_padre_desc = ''
    extra_querystring = ''

    if clave == 'subuso':
        uso_filtro = _subuso_uso_get(request)
        if not uso_filtro:
            messages.info(
                request,
                'Seleccione un uso en el catálogo de usos (Catastro) para administrar los usos del predio filtrados por ese código.',
            )
            return redirect('catastro:usos_predio_list')
        uso_padre_desc = _uso_padre_descripcion(uso_filtro)
        extra_querystring = _subuso_extra_query(uso_filtro)

    qs = model.objects.all()
    if clave == 'subuso' and uso_filtro:
        qs = qs.filter(uso=uso_filtro)

    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(_search_q(model, search))
    qs = qs.order_by(*_ordering(model))
    return render(request, 'configuracion/catalogo_catastro_list.html', {
        'titulo': cfg['titulo'],
        'catalogo_clave': clave,
        'tabla': model._meta.db_table,
        'list_fields': _catalog_field_names(model),
        'object_list': qs,
        'search': search,
        'uso_filtro': uso_filtro,
        'uso_padre_descripcion': uso_padre_desc,
        'extra_querystring': extra_querystring,
        'export_querystring': _export_querystring(request),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def catalogo_catastro_create(request, clave: str):
    cfg = get_catalogo_predio(clave)
    model = cfg['model']
    uso_filtro = _subuso_uso_get(request) if clave == 'subuso' else ''
    extra_querystring = _subuso_extra_query(uso_filtro) if clave == 'subuso' else ''

    if clave == 'subuso' and not uso_filtro:
        messages.info(request, 'Debe elegir un uso desde el listado de usos en Catastro.')
        return redirect('catastro:usos_predio_list')

    FormClass = catalogo_predio_form(model)
    if request.method == 'POST':
        if clave == 'subuso' and uso_filtro:
            posted_uso = (request.POST.get('uso') or '').strip()
            if posted_uso != uso_filtro:
                messages.error(request, 'El uso no coincide con el filtro seleccionado.')
                return _redirect_subuso_list(uso_filtro)
        existente = _existente_por_post(model, request.POST)
        form = FormClass(request.POST, instance=existente) if existente else FormClass(request.POST)
        if form.is_valid():
            form.save()
            if existente:
                messages.info(request, 'La clave ya existía; se actualizó sin crear duplicado.')
            else:
                messages.success(request, 'Registro guardado correctamente.')
            if clave == 'subuso':
                return _redirect_subuso_list(uso_filtro)
            return redirect('configuracion:catalogo_catastro_list', clave=clave)
        messages.error(request, 'Revise los datos del formulario.')
    else:
        initial = {}
        if clave == 'subuso' and uso_filtro:
            initial['uso'] = uso_filtro
        form = FormClass(initial=initial) if initial else FormClass()
        if clave == 'subuso' and uso_filtro and 'uso' in form.fields:
            form.fields['uso'].widget.attrs['readonly'] = True

    return render(request, 'configuracion/geo_form.html', {
        'titulo': f"Nuevo — {cfg['titulo']}",
        'form': form,
        'list_url': 'configuracion:catalogo_catastro_list',
        'catalogo_clave': clave,
        'nota_codigo_existente': _NOTA_CODIGO_EXISTENTE,
        'ajax_lookup': _ajax_lookup_config_catastro(request, clave),
        'extra_querystring': extra_querystring,
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def catalogo_catastro_update(request, clave: str, pk: int):
    cfg = get_catalogo_predio(clave)
    model = cfg['model']
    obj = get_object_or_404(model, pk=pk)
    uso_filtro = _subuso_uso_get(request) if clave == 'subuso' else ''
    extra_querystring = _subuso_extra_query(uso_filtro) if clave == 'subuso' else ''

    if clave == 'subuso':
        if not uso_filtro:
            messages.info(request, 'Debe elegir un uso desde el listado de usos en Catastro.')
            return redirect('catastro:usos_predio_list')
        if getattr(obj, 'uso', None) != uso_filtro:
            messages.error(request, 'Este registro no pertenece al uso seleccionado.')
            return _redirect_subuso_list(uso_filtro)

    FormClass = catalogo_predio_form(model)
    if request.method == 'POST':
        if clave == 'subuso' and uso_filtro:
            posted_uso = (request.POST.get('uso') or '').strip()
            if posted_uso != uso_filtro:
                messages.error(request, 'El uso no coincide con el filtro seleccionado.')
                return _redirect_subuso_list(uso_filtro)
        form = FormClass(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro actualizado.')
            if clave == 'subuso':
                return _redirect_subuso_list(uso_filtro)
            return redirect('configuracion:catalogo_catastro_list', clave=clave)
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = FormClass(instance=obj)
        if clave == 'subuso' and uso_filtro and 'uso' in form.fields:
            form.fields['uso'].widget.attrs['readonly'] = True

    return render(request, 'configuracion/geo_form.html', {
        'titulo': f"Editar — {cfg['titulo']} ({_objeto_etiqueta_editar(obj)})",
        'form': form,
        'list_url': 'configuracion:catalogo_catastro_list',
        'catalogo_clave': clave,
        'extra_querystring': extra_querystring,
        'ajax_lookup': _ajax_lookup_config_catastro(request, clave),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def catalogo_catastro_delete(request, clave: str, pk: int):
    cfg = get_catalogo_predio(clave)
    model = cfg['model']
    obj = get_object_or_404(model, pk=pk)
    uso_filtro = _subuso_uso_get(request) if clave == 'subuso' else ''
    extra_querystring = _subuso_extra_query(uso_filtro) if clave == 'subuso' else ''

    if clave == 'subuso':
        if not uso_filtro:
            messages.info(request, 'Debe elegir un uso desde el listado de usos en Catastro.')
            return redirect('catastro:usos_predio_list')
        if getattr(obj, 'uso', None) != uso_filtro:
            messages.error(request, 'Este registro no pertenece al uso seleccionado.')
            return _redirect_subuso_list(uso_filtro)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro eliminado.')
        if clave == 'subuso':
            return _redirect_subuso_list(uso_filtro)
        return redirect('configuracion:catalogo_catastro_list', clave=clave)
    return render(request, 'configuracion/geo_confirm_delete.html', {
        'titulo': f"Eliminar — {cfg['titulo']}",
        'object': obj,
        'label': str(obj),
        'list_url': 'configuracion:catalogo_catastro_list',
        'catalogo_clave': clave,
        'extra_querystring': extra_querystring,
    })


@api_sistema_require_auth
@require_http_methods(['GET'])
def api_lookup_catalogo_catastro(request, clave: str):
    cfg = get_catalogo_predio(clave)
    model = cfg['model']

    if model is cfg_models.CfgSubuso:
        uso = (request.GET.get('uso') or '').strip()
        codsubuso = (request.GET.get('codsubuso') or '').strip()
        if not uso or not codsubuso:
            return JsonResponse({'found': False})
        obj = model.objects.filter(uso=uso, codsubuso=codsubuso).first()
    elif model is cfg_models.CfgTopografia:
        cot = (request.GET.get('cotopo') or request.GET.get('codigo') or '').strip()
        if not cot:
            return JsonResponse({'found': False})
        obj = model.objects.filter(cotopo=cot).first()
    else:
        codigo = (request.GET.get('codigo') or '').strip()
        if not codigo:
            return JsonResponse({'found': False})
        field = model._meta.get_field('codigo')
        if field.get_internal_type() == 'DecimalField':
            try:
                codigo = Decimal(codigo)
            except (InvalidOperation, ValueError):
                return JsonResponse({'found': False})
        obj = model.objects.filter(codigo=codigo).first()

    if not obj:
        return JsonResponse({'found': False})
    return JsonResponse({
        'found': True,
        'data': _serialize_catalog_obj(obj),
    })


def _catalogo_catastro_queryset_for_list(request, clave: str):
    """Misma lógica de filtro que `catalogo_catastro_list` (qs ordenado)."""
    cfg = get_catalogo_predio(clave)
    model = cfg['model']
    uso_filtro = ''
    if clave == 'subuso':
        uso_filtro = _subuso_uso_get(request)
        if not uso_filtro:
            return None, None, None
    qs = model.objects.all()
    if clave == 'subuso' and uso_filtro:
        qs = qs.filter(uso=uso_filtro)
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(_search_q(model, search))
    qs = qs.order_by(*_ordering(model))
    return cfg, model, qs


@sistema_require_auth
def catalogo_catastro_export_excel(request, clave: str):
    result = _catalogo_catastro_queryset_for_list(request, clave)
    cfg, model, qs = result
    if cfg is None:
        messages.info(
            request,
            'Seleccione un uso en el catálogo de usos (Catastro) para exportar subusos.',
        )
        return redirect('catastro:usos_predio_list')
    field_names = _catalog_field_names(model)
    headers = [fn.replace('_', ' ').title() for fn in field_names]
    h, rows = queryset_to_matrix(qs, field_names, headers)
    sheet = (cfg['titulo'] or clave)[:31]
    uso_bit = f"_{_subuso_uso_get(request)}" if clave == 'subuso' else ''
    base = f'catalogo_{clave}{uso_bit}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, sheet, h, rows)
    if err:
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return _redirect_catalog_list_preserve_get(request, clave)
    return resp


@sistema_require_auth
def catalogo_catastro_export_pdf(request, clave: str):
    result = _catalogo_catastro_queryset_for_list(request, clave)
    cfg, model, qs = result
    if cfg is None:
        messages.info(
            request,
            'Seleccione un uso en el catálogo de usos (Catastro) para exportar subusos.',
        )
        return redirect('catastro:usos_predio_list')
    field_names = _catalog_field_names(model)
    headers = [fn.replace('_', ' ').title() for fn in field_names]
    h, rows = queryset_to_matrix(qs, field_names, headers)
    title = cfg['titulo'] or clave
    uso_bit = f"_{_subuso_uso_get(request)}" if clave == 'subuso' else ''
    base = f'catalogo_{clave}{uso_bit}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, title, h, rows)
    if err:
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return _redirect_catalog_list_preserve_get(request, clave)
    return resp

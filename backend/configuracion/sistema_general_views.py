# -*- coding: utf-8 -*-
"""
Configuración general del sistema (departamentos, municipios, caseríos, nacionalidades, sitio del predio).
Autenticación: sesión modular (`user_id`), sin filtro por empresa/municipio de Catastro.
"""
from datetime import datetime
from functools import wraps
from decimal import Decimal
from urllib.parse import urlencode

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.models import Departamento, Municipio

from .export_helpers import build_http_excel, build_http_pdf, queryset_to_matrix
from .models import Caserio, Nacionalidad, Sitio
from core.caserio_municipio import depto_y_codmuni_desde_codigo_municipio
from core.municipio_depto import (
    departamento_para_codigo_municipio,
    dos_digitos_codigo_departamento,
    municipio_prefijo_codigo,
)


def _departamento_desde_request_get(request):
    """Departamento desde ?depto= (valor del campo departamento.depto)."""
    raw = (request.GET.get('depto') or '').strip()
    if not raw:
        return None
    dep = Departamento.objects.filter(depto=raw).first()
    if dep:
        return dep
    if len(raw) >= 2:
        pref = raw[:2]
        for d in Departamento.objects.order_by('depto'):
            if dos_digitos_codigo_departamento(d.depto) == pref:
                return d
    return None


def _municipio_extra_query(depto_val):
    if not depto_val:
        return ''
    return '?' + urlencode({'depto': depto_val})


def _redirect_municipios_list_depto(depto_val):
    return redirect(f"{reverse('configuracion:municipios_list')}?{urlencode({'depto': depto_val})}")


def _caserio_contexto_get(request):
    depto = (request.GET.get('depto') or '').strip()
    codmuni = (request.GET.get('codmuni') or '').strip()
    if depto and codmuni:
        return depto, codmuni
    return None, None


def _caserio_extra_query(depto, codmuni):
    if not depto or not codmuni:
        return ''
    return '?' + urlencode({'depto': depto, 'codmuni': codmuni})


def _redirect_caserios_list(depto, codmuni):
    return redirect(f"{reverse('configuracion:caserios_list')}?{urlencode({'depto': depto, 'codmuni': codmuni})}")


def _export_querystring(request):
    q = request.GET.urlencode()
    return f'?{q}' if q else ''


def _redirect_list_preserve_get(request, url_name, url_kwargs=None):
    url = reverse(url_name, kwargs=url_kwargs or {})
    if request.GET:
        url = f'{url}?{request.GET.urlencode()}'
    return redirect(url)


from .sistema_general_forms import (
    CaserioForm,
    DepartamentoForm,
    MunicipioForm,
    NacionalidadForm,
    SitioForm,
)

# Texto de ayuda en pantallas "Nuevo" (código existente → se actualiza, sin duplicar)
_NOTA_CODIGO_EXISTENTE = (
    'Al escribir el código, si ya existe se cargan automáticamente la descripción y los demás '
    'datos para que pueda corregirlos antes de guardar. Si guarda con un código existente, '
    'se actualiza el registro sin crear duplicado.'
)


def _dec_str(val):
    if val is None:
        return ''
    if isinstance(val, Decimal):
        return format(val, 'f')
    return str(val)


def _date_str(val):
    if val is None:
        return ''
    return val.isoformat()


def _ajax_lookup_config(mode):
    """Config para geo_form.html: búsqueda interactiva por código (JSON)."""
    names = {
        'departamento': 'api_lookup_departamento',
        'municipio': 'api_lookup_municipio',
        'nacionalidad': 'api_lookup_nacionalidad',
        'caserio': 'api_lookup_caserio',
        'sitio': 'api_lookup_sitio',
    }
    return {'url': reverse(f'configuracion:{names[mode]}'), 'mode': mode}


def api_sistema_require_auth(view_func):
    """API: JSON 401 si no hay sesión modular (sin redirección HTML)."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return JsonResponse({'found': False, 'error': 'No autenticado'}, status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


@api_sistema_require_auth
@require_http_methods(['GET'])
def api_lookup_departamento(request):
    depto = request.GET.get('depto', '').strip()
    if not depto:
        return JsonResponse({'found': False})
    obj = Departamento.objects.filter(depto=depto).first()
    if not obj:
        return JsonResponse({'found': False})
    return JsonResponse({
        'found': True,
        'data': {'descripcion': obj.descripcion or ''},
    })


@api_sistema_require_auth
@require_http_methods(['GET'])
def api_lookup_municipio(request):
    codigo = request.GET.get('codigo', '').strip()
    if not codigo:
        return JsonResponse({'found': False})
    obj = Municipio.objects.filter(codigo=codigo).first()
    if not obj:
        return JsonResponse({'found': False})
    dep = departamento_para_codigo_municipio(obj.codigo)
    return JsonResponse({
        'found': True,
        'data': {
            'departamento': str(dep.pk) if dep else '',
            'descripcion': obj.descripcion or '',
            'fesqui': _dec_str(obj.fesqui),
            'por_concer': _dec_str(obj.por_concer),
            'vl_exento': _dec_str(obj.vl_exento),
            'tasau': _dec_str(obj.tasau),
            'tasar': _dec_str(obj.tasar),
            'interes': _dec_str(obj.interes),
            'desc_tercera': _dec_str(obj.desc_tercera),
            'alcalde': obj.alcalde or '',
            'auditor': obj.auditor or '',
            'presupuestos': obj.presupuestos or '',
            'contador': obj.contador or '',
            'tesorero': obj.tesorero or '',
            'secretario': obj.secretario or '',
            'tesorera': obj.tesorera or '',
            'financiero': obj.financiero or '',
            'tributacion': obj.tributacion or '',
            'gerentefin': obj.gerentefin or '',
            'gerentegeneral': obj.gerentegeneral or '',
            'proyecto': obj.proyecto or '',
            'activo': obj.activo or '',
            'porce_condo1': _dec_str(obj.porce_condo1),
            'porce_condo2': _dec_str(obj.porce_condo2),
            'fecondona1': _date_str(obj.fecondona1),
            'fecondona2': _date_str(obj.fecondona2),
        },
    })


@api_sistema_require_auth
@require_http_methods(['GET'])
def api_lookup_nacionalidad(request):
    codigo = request.GET.get('codigo', '').strip()
    if not codigo:
        return JsonResponse({'found': False})
    obj = Nacionalidad.objects.filter(codigo=codigo).first()
    if not obj:
        return JsonResponse({'found': False})
    return JsonResponse({
        'found': True,
        'data': {'descripcion': obj.descripcion or ''},
    })


@api_sistema_require_auth
@require_http_methods(['GET'])
def api_lookup_sitio(request):
    codigo = request.GET.get('codigo', '').strip()
    if not codigo:
        return JsonResponse({'found': False})
    obj = Sitio.objects.filter(codigo=codigo).first()
    if not obj:
        return JsonResponse({'found': False})
    return JsonResponse({
        'found': True,
        'data': {'descripcion': obj.descripcion or ''},
    })


@api_sistema_require_auth
@require_http_methods(['GET'])
def api_lookup_caserio(request):
    depto = request.GET.get('depto', '').strip()
    codmuni = request.GET.get('codmuni', '').strip()
    codbarrio = request.GET.get('codbarrio', '').strip()
    codigo = request.GET.get('codigo', '').strip()
    if not (depto and codmuni and codigo):
        return JsonResponse({'found': False})
    obj = Caserio.objects.filter(
        depto=depto,
        codmuni=codmuni,
        codbarrio=codbarrio,
        codigo=codigo,
    ).first()
    if not obj:
        return JsonResponse({'found': False})
    return JsonResponse({
        'found': True,
        'data': {'descripcion': obj.descripcion or ''},
    })


def _departamento_existente_por_post(post):
    depto = (post.get('depto') or '').strip()
    if not depto:
        return None
    return Departamento.objects.filter(depto=depto).first()


def _municipio_existente_por_post(post):
    codigo = (post.get('codigo') or '').strip()
    if not codigo:
        return None
    return Municipio.objects.filter(codigo=codigo).first()


def _nacionalidad_existente_por_post(post):
    codigo = (post.get('codigo') or '').strip()
    if not codigo:
        return None
    return Nacionalidad.objects.filter(codigo=codigo).first()


def _sitio_existente_por_post(post):
    codigo = (post.get('codigo') or '').strip()
    if not codigo:
        return None
    return Sitio.objects.filter(codigo=codigo).first()


def _caserio_existente_por_post(post):
    depto = (post.get('depto') or '').strip()
    codmuni = (post.get('codmuni') or '').strip()
    codbarrio = (post.get('codbarrio') or '').strip()
    codigo = (post.get('codigo') or '').strip()
    if not (depto and codmuni and codigo):
        return None
    return Caserio.objects.filter(
        depto=depto,
        codmuni=codmuni,
        codbarrio=codbarrio,
        codigo=codigo,
    ).first()


def sistema_require_auth(view_func):
    """Requiere sesión del menú modular (`modules_core`)."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('modules_core:login_principal')
        return view_func(request, *args, **kwargs)

    return wrapper


@sistema_require_auth
def sistema_general_menu(request):
    """Menú de catálogos generales (multi-municipio)."""
    from .catalog_registry import CATALOGO_PREDIO_ITEMS

    catalogos_predio = [
        {
            'clave': row[0],
            'titulo': row[2],
            'icon': row[3],
            'tabla': row[1]._meta.db_table,
        }
        for row in CATALOGO_PREDIO_ITEMS
    ]
    return render(request, 'configuracion/sistema_general_menu.html', {
        'titulo': 'Configuración general del sistema',
        'usuario': request.session.get('nombre'),
        'empresa': request.session.get('empresa'),
        'catalogos_predio': catalogos_predio,
    })


# --- Departamentos ---
@sistema_require_auth
def departamentos_list(request):
    qs = Departamento.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(depto__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('depto')
    return render(request, 'configuracion/departamentos_list.html', {
        'titulo': 'Departamentos',
        'object_list': qs,
        'search': search,
        'export_querystring': _export_querystring(request),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def departamento_create(request):
    if request.method == 'POST':
        existente = _departamento_existente_por_post(request.POST)
        form = DepartamentoForm(request.POST, instance=existente) if existente else DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            if existente:
                messages.info(
                    request,
                    'El código de departamento ya existía; se actualizó la información sin crear duplicado.',
                )
            else:
                messages.success(request, 'Departamento guardado correctamente.')
            return redirect('configuracion:departamentos_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = DepartamentoForm()
    return render(request, 'configuracion/geo_form.html', {
        'titulo': 'Nuevo departamento',
        'form': form,
        'list_url': 'configuracion:departamentos_list',
        'nota_codigo_existente': _NOTA_CODIGO_EXISTENTE,
        'ajax_lookup': _ajax_lookup_config('departamento'),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def departamento_update(request, codigo):
    obj = get_object_or_404(Departamento, depto=codigo)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento actualizado.')
            return redirect('configuracion:departamentos_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = DepartamentoForm(instance=obj)
    return render(request, 'configuracion/geo_form.html', {
        'titulo': f'Editar departamento {obj.depto}',
        'form': form,
        'list_url': 'configuracion:departamentos_list',
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def departamento_delete(request, codigo):
    obj = get_object_or_404(Departamento, depto=codigo)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Departamento eliminado.')
        return redirect('configuracion:departamentos_list')
    return render(request, 'configuracion/geo_confirm_delete.html', {
        'titulo': 'Eliminar departamento',
        'object': obj,
        'label': str(obj),
        'list_url': 'configuracion:departamentos_list',
    })


# --- Municipios (siempre en contexto de un departamento: ?depto= desde el listado de departamentos) ---
@sistema_require_auth
def municipios_list(request):
    dep = _departamento_desde_request_get(request)
    if not dep:
        messages.info(
            request,
            'Seleccione un departamento en el catálogo y use «Municipios» en su fila para administrar los municipios de ese departamento.',
        )
        return redirect('configuracion:departamentos_list')
    pref = dos_digitos_codigo_departamento(dep.depto)
    qs = Municipio.objects.filter(codigo__startswith=pref)
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    object_list = list(qs)
    extra_querystring = _municipio_extra_query(dep.depto)
    return render(request, 'configuracion/municipios_list.html', {
        'titulo': f'Municipios — {dep.depto} {dep.descripcion}',
        'object_list': object_list,
        'search': search,
        'depto_filtro': dep.depto,
        'departamento_obj': dep,
        'extra_querystring': extra_querystring,
        'export_querystring': _export_querystring(request),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def municipio_create(request):
    dep = _departamento_desde_request_get(request)
    if not dep:
        messages.info(
            request,
            'Para crear municipios, abra primero el catálogo de Departamentos y use el botón «Municipios» del departamento correspondiente.',
        )
        return redirect('configuracion:departamentos_list')
    extra_querystring = _municipio_extra_query(dep.depto)
    if request.method == 'POST':
        existente = _municipio_existente_por_post(request.POST)
        form = (
            MunicipioForm(request.POST, instance=existente, depto_bloqueado=dep)
            if existente
            else MunicipioForm(request.POST, depto_bloqueado=dep)
        )
        if form.is_valid():
            form.save()
            if existente:
                messages.info(
                    request,
                    'El código de municipio ya existía; se actualizó el registro sin crear duplicado.',
                )
            else:
                messages.success(request, 'Municipio guardado correctamente.')
            return _redirect_municipios_list_depto(dep.depto)
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = MunicipioForm(depto_bloqueado=dep)
    return render(request, 'configuracion/geo_form.html', {
        'titulo': f'Nuevo municipio — Depto. {dep.depto}',
        'form': form,
        'list_url': 'configuracion:municipios_list',
        'nota_codigo_existente': _NOTA_CODIGO_EXISTENTE,
        'ajax_lookup': _ajax_lookup_config('municipio'),
        'extra_querystring': extra_querystring,
        'municipio_depto_bloqueado_label': f'Departamento: {dep.depto} — {dep.descripcion}',
        'municipio_depto_prefijos': {
            str(d.pk): dos_digitos_codigo_departamento(d.depto)
            for d in Departamento.objects.order_by('depto')
        },
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def municipio_update(request, pk):
    obj = get_object_or_404(Municipio, pk=pk)
    dep = _departamento_desde_request_get(request)
    if not dep:
        dep = departamento_para_codigo_municipio(obj.codigo)
        if dep:
            return redirect(f"{reverse('configuracion:municipio_update', kwargs={'pk': pk})}?{urlencode({'depto': dep.depto})}")
        messages.error(request, 'No se pudo determinar el departamento del municipio.')
        return redirect('configuracion:departamentos_list')
    if municipio_prefijo_codigo(obj.codigo) != dos_digitos_codigo_departamento(dep.depto):
        messages.error(request, 'Este municipio no pertenece al departamento indicado.')
        return _redirect_municipios_list_depto(dep.depto)
    extra_querystring = _municipio_extra_query(dep.depto)
    if request.method == 'POST':
        form = MunicipioForm(request.POST, instance=obj, depto_bloqueado=dep)
        if form.is_valid():
            form.save()
            messages.success(request, 'Municipio actualizado.')
            return _redirect_municipios_list_depto(dep.depto)
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = MunicipioForm(instance=obj, depto_bloqueado=dep)
    d_cas, m_cas = depto_y_codmuni_desde_codigo_municipio(obj.codigo)
    ctx_mun = {
        'titulo': f'Editar municipio {obj.codigo}',
        'form': form,
        'list_url': 'configuracion:municipios_list',
        'ajax_lookup': _ajax_lookup_config('municipio'),
        'extra_querystring': extra_querystring,
        'municipio_depto_bloqueado_label': f'Departamento: {dep.depto} — {dep.descripcion}',
        'municipio_depto_prefijos': {
            str(d.pk): dos_digitos_codigo_departamento(d.depto)
            for d in Departamento.objects.order_by('depto')
        },
    }
    if d_cas and m_cas:
        ctx_mun['enlace_auxiliar_url'] = (
            f"{reverse('configuracion:caserios_list')}?{urlencode({'depto': d_cas, 'codmuni': m_cas})}"
        )
        ctx_mun['enlace_auxiliar_texto'] = 'Caseríos'
    return render(request, 'configuracion/geo_form.html', ctx_mun)


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def municipio_delete(request, pk):
    obj = get_object_or_404(Municipio, pk=pk)
    dep = _departamento_desde_request_get(request)
    if not dep:
        dep = departamento_para_codigo_municipio(obj.codigo)
        if dep:
            return redirect(f"{reverse('configuracion:municipio_delete', kwargs={'pk': pk})}?{urlencode({'depto': dep.depto})}")
        messages.error(request, 'No se pudo determinar el departamento del municipio.')
        return redirect('configuracion:departamentos_list')
    if municipio_prefijo_codigo(obj.codigo) != dos_digitos_codigo_departamento(dep.depto):
        messages.error(request, 'Este municipio no pertenece al departamento indicado.')
        return _redirect_municipios_list_depto(dep.depto)
    extra_querystring = _municipio_extra_query(dep.depto)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Municipio eliminado.')
        return _redirect_municipios_list_depto(dep.depto)
    return render(request, 'configuracion/geo_confirm_delete.html', {
        'titulo': 'Eliminar municipio',
        'object': obj,
        'label': str(obj),
        'list_url': 'configuracion:municipios_list',
        'extra_querystring': extra_querystring,
    })


# --- Caseríos (desde municipio: ?depto= + ?codmuni= = primeros 2 y últimos 2 dígitos de municipio.codigo) ---
@sistema_require_auth
def caserios_list(request):
    depto_f, codmuni_f = _caserio_contexto_get(request)
    if not depto_f or not codmuni_f:
        messages.info(
            request,
            'Abra el listado de municipios (desde Departamentos), elija un municipio con código de 4 dígitos y use «Caseríos».',
        )
        return redirect('configuracion:departamentos_list')
    qs = Caserio.objects.filter(depto=depto_f, codmuni=codmuni_f)
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(
            Q(codigo__icontains=search)
            | Q(descripcion__icontains=search)
            | Q(codbarrio__icontains=search)
        )
    qs = qs.order_by('depto', 'codmuni', 'codbarrio', 'codigo')
    extra_querystring = _caserio_extra_query(depto_f, codmuni_f)
    codigo_sintetico = f'{depto_f}{codmuni_f}'
    dep_mun = departamento_para_codigo_municipio(codigo_sintetico) if len(codigo_sintetico) >= 4 else None
    volver_municipios_url = ''
    if dep_mun:
        volver_municipios_url = f"{reverse('configuracion:municipios_list')}?{urlencode({'depto': dep_mun.depto})}"
    return render(request, 'configuracion/caserios_list.html', {
        'titulo': f'Caseríos — depto {depto_f} / municipio {codmuni_f}',
        'object_list': qs,
        'search': search,
        'depto_filtro': depto_f,
        'codmuni_filtro': codmuni_f,
        'extra_querystring': extra_querystring,
        'volver_municipios_url': volver_municipios_url,
        'export_querystring': _export_querystring(request),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def caserio_create(request):
    depto_f, codmuni_f = _caserio_contexto_get(request)
    if not depto_f or not codmuni_f:
        messages.info(
            request,
            'Para crear caseríos, use «Caseríos» en la fila de un municipio (código de 4 dígitos).',
        )
        return redirect('configuracion:departamentos_list')
    bloqueado = (depto_f, codmuni_f)
    extra_querystring = _caserio_extra_query(depto_f, codmuni_f)
    if request.method == 'POST':
        existente = _caserio_existente_por_post(request.POST)
        form = (
            CaserioForm(request.POST, instance=existente, depto_codmuni_bloqueado=bloqueado)
            if existente
            else CaserioForm(request.POST, depto_codmuni_bloqueado=bloqueado)
        )
        if form.is_valid():
            form.save()
            if existente:
                messages.info(
                    request,
                    'Ya existía un caserío con la misma clave (depto, municipio, barrio y código); '
                    'se actualizó sin crear duplicado.',
                )
            else:
                messages.success(request, 'Caserío guardado correctamente.')
            return _redirect_caserios_list(depto_f, codmuni_f)
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = CaserioForm(depto_codmuni_bloqueado=bloqueado)
    return render(request, 'configuracion/geo_form.html', {
        'titulo': f'Nuevo caserío — depto {depto_f} / muni {codmuni_f}',
        'form': form,
        'list_url': 'configuracion:caserios_list',
        'nota_codigo_existente': _NOTA_CODIGO_EXISTENTE,
        'ajax_lookup': _ajax_lookup_config('caserio'),
        'extra_querystring': extra_querystring,
        'caserio_contexto_label': f'Departamento (caserío) {depto_f}, código municipio {codmuni_f} — coincide con el código del municipio (2+2 dígitos).',
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def caserio_update(request, pk):
    obj = get_object_or_404(Caserio, pk=pk)
    depto_f, codmuni_f = _caserio_contexto_get(request)
    if not depto_f or not codmuni_f:
        return redirect(
            f"{reverse('configuracion:caserio_update', kwargs={'pk': pk})}"
            f"?{urlencode({'depto': obj.depto, 'codmuni': obj.codmuni})}"
        )
    if (obj.depto or '').strip() != depto_f or (obj.codmuni or '').strip() != codmuni_f:
        messages.error(request, 'Este caserío no corresponde al municipio indicado en la URL.')
        return _redirect_caserios_list(depto_f, codmuni_f)
    bloqueado = (depto_f, codmuni_f)
    extra_querystring = _caserio_extra_query(depto_f, codmuni_f)
    if request.method == 'POST':
        form = CaserioForm(request.POST, instance=obj, depto_codmuni_bloqueado=bloqueado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caserío actualizado.')
            return _redirect_caserios_list(depto_f, codmuni_f)
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = CaserioForm(instance=obj, depto_codmuni_bloqueado=bloqueado)
    return render(request, 'configuracion/geo_form.html', {
        'titulo': f'Editar caserío {obj.codigo}',
        'form': form,
        'list_url': 'configuracion:caserios_list',
        'ajax_lookup': _ajax_lookup_config('caserio'),
        'extra_querystring': extra_querystring,
        'caserio_contexto_label': f'Departamento {depto_f}, municipio {codmuni_f}',
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def caserio_delete(request, pk):
    obj = get_object_or_404(Caserio, pk=pk)
    depto_f, codmuni_f = _caserio_contexto_get(request)
    if not depto_f or not codmuni_f:
        return redirect(
            f"{reverse('configuracion:caserio_delete', kwargs={'pk': pk})}"
            f"?{urlencode({'depto': obj.depto, 'codmuni': obj.codmuni})}"
        )
    if (obj.depto or '').strip() != depto_f or (obj.codmuni or '').strip() != codmuni_f:
        messages.error(request, 'Este caserío no corresponde al municipio indicado en la URL.')
        return _redirect_caserios_list(depto_f, codmuni_f)
    extra_querystring = _caserio_extra_query(depto_f, codmuni_f)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Caserío eliminado.')
        return _redirect_caserios_list(depto_f, codmuni_f)
    return render(request, 'configuracion/geo_confirm_delete.html', {
        'titulo': 'Eliminar caserío',
        'object': obj,
        'label': str(obj),
        'list_url': 'configuracion:caserios_list',
        'extra_querystring': extra_querystring,
    })


# --- Nacionalidades ---
@sistema_require_auth
def nacionalidades_list(request):
    qs = Nacionalidad.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    return render(request, 'configuracion/nacionalidades_list.html', {
        'titulo': 'Nacionalidades',
        'object_list': qs,
        'search': search,
        'export_querystring': _export_querystring(request),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def nacionalidad_create(request):
    if request.method == 'POST':
        existente = _nacionalidad_existente_por_post(request.POST)
        form = NacionalidadForm(request.POST, instance=existente) if existente else NacionalidadForm(request.POST)
        if form.is_valid():
            form.save()
            if existente:
                messages.info(
                    request,
                    'El código de nacionalidad ya existía; se actualizó la descripción sin crear duplicado.',
                )
            else:
                messages.success(request, 'Nacionalidad guardada correctamente.')
            return redirect('configuracion:nacionalidades_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = NacionalidadForm()
    return render(request, 'configuracion/geo_form.html', {
        'titulo': 'Nueva nacionalidad',
        'form': form,
        'list_url': 'configuracion:nacionalidades_list',
        'nota_codigo_existente': _NOTA_CODIGO_EXISTENTE,
        'ajax_lookup': _ajax_lookup_config('nacionalidad'),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def nacionalidad_update(request, pk):
    obj = get_object_or_404(Nacionalidad, pk=pk)
    if request.method == 'POST':
        form = NacionalidadForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nacionalidad actualizada.')
            return redirect('configuracion:nacionalidades_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = NacionalidadForm(instance=obj)
    return render(request, 'configuracion/geo_form.html', {
        'titulo': f'Editar nacionalidad {obj.codigo}',
        'form': form,
        'list_url': 'configuracion:nacionalidades_list',
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def nacionalidad_delete(request, pk):
    obj = get_object_or_404(Nacionalidad, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Nacionalidad eliminada.')
        return redirect('configuracion:nacionalidades_list')
    return render(request, 'configuracion/geo_confirm_delete.html', {
        'titulo': 'Eliminar nacionalidad',
        'object': obj,
        'label': str(obj),
        'list_url': 'configuracion:nacionalidades_list',
    })


# --- Sitio del predio ---
@sistema_require_auth
def sitios_list(request):
    qs = Sitio.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    return render(request, 'configuracion/sitios_list.html', {
        'titulo': 'Sitio del predio',
        'object_list': qs,
        'search': search,
        'export_querystring': _export_querystring(request),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def sitio_create(request):
    if request.method == 'POST':
        existente = _sitio_existente_por_post(request.POST)
        form = SitioForm(request.POST, instance=existente) if existente else SitioForm(request.POST)
        if form.is_valid():
            form.save()
            if existente:
                messages.info(
                    request,
                    'El código ya existía; se actualizó la descripción sin crear duplicado.',
                )
            else:
                messages.success(request, 'Registro de sitio guardado correctamente.')
            return redirect('configuracion:sitios_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = SitioForm()
    return render(request, 'configuracion/geo_form.html', {
        'titulo': 'Nuevo sitio del predio',
        'form': form,
        'list_url': 'configuracion:sitios_list',
        'nota_codigo_existente': _NOTA_CODIGO_EXISTENTE,
        'ajax_lookup': _ajax_lookup_config('sitio'),
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def sitio_update(request, pk):
    obj = get_object_or_404(Sitio, pk=pk)
    if request.method == 'POST':
        form = SitioForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sitio del predio actualizado.')
            return redirect('configuracion:sitios_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = SitioForm(instance=obj)
    return render(request, 'configuracion/geo_form.html', {
        'titulo': f'Editar sitio del predio {obj.codigo}',
        'form': form,
        'list_url': 'configuracion:sitios_list',
    })


@sistema_require_auth
@require_http_methods(['GET', 'POST'])
def sitio_delete(request, pk):
    obj = get_object_or_404(Sitio, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Sitio del predio eliminado.')
        return redirect('configuracion:sitios_list')
    return render(request, 'configuracion/geo_confirm_delete.html', {
        'titulo': 'Eliminar sitio del predio',
        'object': obj,
        'label': str(obj),
        'list_url': 'configuracion:sitios_list',
    })


# --- Exportación Excel / PDF (mismos filtros que el listado) ---
_MUNICIPIOS_EXPORT_FIELDS = [
    'codigo',
    'descripcion',
    'fesqui',
    'por_concer',
    'vl_exento',
    'tasau',
    'tasar',
]
_MUNICIPIOS_EXPORT_HEADERS = [
    'Código',
    'Descripción',
    'F. esquina',
    '% conc.',
    'V. exento',
    'Tasa U',
    'Tasa R',
]


@sistema_require_auth
def departamentos_export_excel(request):
    qs = Departamento.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(depto__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('depto')
    fields = ['depto', 'descripcion']
    headers = ['Depto', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'departamentos_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, 'Departamentos', h, rows)
    if err:
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return _redirect_list_preserve_get(request, 'configuracion:departamentos_list')
    return resp


@sistema_require_auth
def departamentos_export_pdf(request):
    qs = Departamento.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(depto__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('depto')
    fields = ['depto', 'descripcion']
    headers = ['Depto', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'departamentos_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, 'Departamentos', h, rows)
    if err:
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return _redirect_list_preserve_get(request, 'configuracion:departamentos_list')
    return resp


@sistema_require_auth
def municipios_export_excel(request):
    dep = _departamento_desde_request_get(request)
    if not dep:
        messages.info(
            request,
            'Seleccione un departamento y abra Municipios desde su fila para exportar.',
        )
        return redirect('configuracion:departamentos_list')
    pref = dos_digitos_codigo_departamento(dep.depto)
    qs = Municipio.objects.filter(codigo__startswith=pref)
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    h, rows = queryset_to_matrix(qs, _MUNICIPIOS_EXPORT_FIELDS, _MUNICIPIOS_EXPORT_HEADERS)
    safe_depto = (dep.depto or 'depto').replace('/', '_')[:20]
    base = f'municipios_{safe_depto}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, 'Municipios', h, rows)
    if err:
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return _redirect_list_preserve_get(request, 'configuracion:municipios_list')
    return resp


@sistema_require_auth
def municipios_export_pdf(request):
    dep = _departamento_desde_request_get(request)
    if not dep:
        messages.info(
            request,
            'Seleccione un departamento y abra Municipios desde su fila para exportar.',
        )
        return redirect('configuracion:departamentos_list')
    pref = dos_digitos_codigo_departamento(dep.depto)
    qs = Municipio.objects.filter(codigo__startswith=pref)
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    h, rows = queryset_to_matrix(qs, _MUNICIPIOS_EXPORT_FIELDS, _MUNICIPIOS_EXPORT_HEADERS)
    title = f'Municipios — {dep.depto} {dep.descripcion}'
    safe_depto = (dep.depto or 'depto').replace('/', '_')[:20]
    base = f'municipios_{safe_depto}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, title, h, rows)
    if err:
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return _redirect_list_preserve_get(request, 'configuracion:municipios_list')
    return resp


@sistema_require_auth
def caserios_export_excel(request):
    depto_f, codmuni_f = _caserio_contexto_get(request)
    if not depto_f or not codmuni_f:
        messages.info(request, 'Indique departamento y municipio en la URL para exportar caseríos.')
        return redirect('configuracion:departamentos_list')
    qs = Caserio.objects.filter(depto=depto_f, codmuni=codmuni_f)
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(
            Q(codigo__icontains=search)
            | Q(descripcion__icontains=search)
            | Q(codbarrio__icontains=search)
        )
    qs = qs.order_by('depto', 'codmuni', 'codbarrio', 'codigo')
    fields = ['depto', 'codmuni', 'codbarrio', 'codigo', 'descripcion']
    headers = ['Depto', 'Muni', 'Barrio', 'Caserío', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'caserios_{depto_f}_{codmuni_f}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, 'Caseríos', h, rows)
    if err:
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return _redirect_list_preserve_get(request, 'configuracion:caserios_list')
    return resp


@sistema_require_auth
def caserios_export_pdf(request):
    depto_f, codmuni_f = _caserio_contexto_get(request)
    if not depto_f or not codmuni_f:
        messages.info(request, 'Indique departamento y municipio en la URL para exportar caseríos.')
        return redirect('configuracion:departamentos_list')
    qs = Caserio.objects.filter(depto=depto_f, codmuni=codmuni_f)
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(
            Q(codigo__icontains=search)
            | Q(descripcion__icontains=search)
            | Q(codbarrio__icontains=search)
        )
    qs = qs.order_by('depto', 'codmuni', 'codbarrio', 'codigo')
    fields = ['depto', 'codmuni', 'codbarrio', 'codigo', 'descripcion']
    headers = ['Depto', 'Muni', 'Barrio', 'Caserío', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    title = f'Caseríos — depto {depto_f} / municipio {codmuni_f}'
    base = f'caserios_{depto_f}_{codmuni_f}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, title, h, rows)
    if err:
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return _redirect_list_preserve_get(request, 'configuracion:caserios_list')
    return resp


@sistema_require_auth
def nacionalidades_export_excel(request):
    qs = Nacionalidad.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    fields = ['codigo', 'descripcion']
    headers = ['Código', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'nacionalidades_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, 'Nacionalidades', h, rows)
    if err:
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return _redirect_list_preserve_get(request, 'configuracion:nacionalidades_list')
    return resp


@sistema_require_auth
def nacionalidades_export_pdf(request):
    qs = Nacionalidad.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    fields = ['codigo', 'descripcion']
    headers = ['Código', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'nacionalidades_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, 'Nacionalidades', h, rows)
    if err:
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return _redirect_list_preserve_get(request, 'configuracion:nacionalidades_list')
    return resp


@sistema_require_auth
def sitios_export_excel(request):
    qs = Sitio.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    fields = ['codigo', 'descripcion']
    headers = ['Código', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'sitio_predio_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, 'Sitio del predio', h, rows)
    if err:
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return _redirect_list_preserve_get(request, 'configuracion:sitios_list')
    return resp


@sistema_require_auth
def sitios_export_pdf(request):
    qs = Sitio.objects.all()
    search = (request.GET.get('search') or '').strip()
    if search:
        qs = qs.filter(Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    qs = qs.order_by('codigo')
    fields = ['codigo', 'descripcion']
    headers = ['Código', 'Descripción']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'sitio_predio_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, 'Sitio del predio', h, rows)
    if err:
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return _redirect_list_preserve_get(request, 'configuracion:sitios_list')
    return resp

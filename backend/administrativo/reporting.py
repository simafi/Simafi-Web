# -*- coding: utf-8 -*-
"""Filtros de listados e informes tabulares (Excel/PDF) por categorías internas del módulo."""
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse

from configuracion.export_helpers import build_http_excel, build_http_pdf, cell_str, queryset_to_matrix

from .models import ContratoAdministrativo, ExpedienteGestion, Proveedor


def export_querystring(request):
    q = request.GET.urlencode()
    return f'?{q}' if q else ''


def redirect_list_preserve_get(request, url_name):
    url = reverse(url_name)
    if request.GET:
        url = f'{url}?{request.GET.urlencode()}'
    return redirect(url)


def proveedor_queryset(request, emp):
    qs = Proveedor.objects.all()
    if emp:
        qs = qs.filter(empresa=emp)
    q = (request.GET.get('search') or '').strip()
    if q:
        qs = qs.filter(
            Q(razon_social__icontains=q)
            | Q(nit__icontains=q)
            | Q(email__icontains=q)
        )
    perfil = (request.GET.get('perfil') or '').strip()
    if perfil == 'activo':
        qs = qs.filter(activo=True)
    elif perfil == 'inactivo':
        qs = qs.filter(activo=False)
    return qs.order_by('razon_social')


def proveedor_subtitulo_informe(request):
    parts = []
    perfil = (request.GET.get('perfil') or '').strip()
    if perfil == 'activo':
        parts.append('Categoría: solo activos')
    elif perfil == 'inactivo':
        parts.append('Categoría: solo inactivos')
    else:
        parts.append('Categoría: todos los perfiles')
    q = (request.GET.get('search') or '').strip()
    if q:
        parts.append(f'Filtro búsqueda: {q}')
    return ' · '.join(parts)


def contrato_queryset(request, emp):
    qs = ContratoAdministrativo.objects.select_related('proveedor').all()
    if emp:
        qs = qs.filter(empresa=emp)
    q = (request.GET.get('search') or '').strip()
    if q:
        qs = qs.filter(
            Q(numero__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(proveedor__razon_social__icontains=q)
        )
    estado = (request.GET.get('estado') or '').strip()
    valid = {c[0] for c in ContratoAdministrativo.ESTADO_CHOICES}
    if estado and estado in valid:
        qs = qs.filter(estado=estado)
    return qs.order_by('-fecha_inicio', 'numero')


def contrato_subtitulo_informe(request):
    parts = []
    estado = (request.GET.get('estado') or '').strip()
    valid = dict(ContratoAdministrativo.ESTADO_CHOICES)
    if estado and estado in valid:
        parts.append(f'Categoría estado: {valid[estado]}')
    else:
        parts.append('Categoría estado: todos')
    q = (request.GET.get('search') or '').strip()
    if q:
        parts.append(f'Búsqueda: {q}')
    return ' · '.join(parts)


def expediente_queryset(request, emp):
    qs = ExpedienteGestion.objects.all()
    if emp:
        qs = qs.filter(empresa=emp)
    q = (request.GET.get('search') or '').strip()
    if q:
        qs = qs.filter(
            Q(codigo_interno__icontains=q)
            | Q(titulo__icontains=q)
            | Q(descripcion__icontains=q)
        )
    tipo = (request.GET.get('tipo') or '').strip()
    tipos = {c[0] for c in ExpedienteGestion.TIPO_CHOICES}
    if tipo and tipo in tipos:
        qs = qs.filter(tipo=tipo)
    estado = (request.GET.get('estado') or '').strip()
    estados = {c[0] for c in ExpedienteGestion.ESTADO_CHOICES}
    if estado and estado in estados:
        qs = qs.filter(estado=estado)
    return qs.order_by('-fecha_apertura')


def expediente_subtitulo_informe(request):
    parts = []
    tipo = (request.GET.get('tipo') or '').strip()
    tdict = dict(ExpedienteGestion.TIPO_CHOICES)
    if tipo and tipo in tdict:
        parts.append(f'Categoría tipo: {tdict[tipo]}')
    else:
        parts.append('Categoría tipo: todos')
    estado = (request.GET.get('estado') or '').strip()
    edict = dict(ExpedienteGestion.ESTADO_CHOICES)
    if estado and estado in edict:
        parts.append(f'Estado trámite: {edict[estado]}')
    else:
        parts.append('Estado trámite: todos')
    q = (request.GET.get('search') or '').strip()
    if q:
        parts.append(f'Búsqueda: {q}')
    return ' · '.join(parts)


def proveedor_export_excel_response(request, emp):
    qs = proveedor_queryset(request, emp)
    fields = ['empresa', 'razon_social', 'nit', 'telefono', 'email', 'direccion', 'activo', 'documentacion_cargada']
    headers = ['Empresa', 'Razón social', 'RTN / DNI / NIT', 'Teléfono', 'Email', 'Dirección', 'Activo', 'Doc. digital']
    h, rows = queryset_to_matrix(qs, fields, headers)
    base = f'informe_proveedores_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    title_sheet = 'Proveedores'
    resp, err = build_http_excel(base, title_sheet, h, rows)
    if err == 'openpyxl':
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return redirect_list_preserve_get(request, 'administrativo:proveedor_list')
    return resp


def proveedor_export_pdf_response(request, emp):
    qs = proveedor_queryset(request, emp)
    fields = ['empresa', 'razon_social', 'nit', 'telefono', 'email', 'direccion', 'activo', 'documentacion_cargada']
    headers = ['Empresa', 'Razón social', 'RTN / DNI / NIT', 'Teléfono', 'Email', 'Dirección', 'Activo', 'Doc. digital']
    h, rows = queryset_to_matrix(qs, fields, headers)
    title = f'Proveedores — {proveedor_subtitulo_informe(request)}'
    base = f'informe_proveedores_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, title, h, rows)
    if err == 'reportlab':
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return redirect_list_preserve_get(request, 'administrativo:proveedor_list')
    return resp


def contrato_export_excel_response(request, emp):
    qs = contrato_queryset(request, emp)
    headers = [
        'Empresa',
        'Número',
        'Proveedor',
        'Inicio',
        'Fin',
        'Monto',
        'Estado',
    ]
    rows = []
    for o in qs:
        rows.append(
            [
                cell_str(o.empresa),
                cell_str(o.numero),
                cell_str(o.proveedor.razon_social if o.proveedor_id else ''),
                cell_str(o.fecha_inicio),
                cell_str(o.fecha_fin),
                cell_str(o.monto_estimado),
                o.get_estado_display(),
            ]
        )
    base = f'informe_contratos_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, 'Contratos', headers, rows)
    if err == 'openpyxl':
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return redirect_list_preserve_get(request, 'administrativo:contrato_list')
    return resp


def contrato_export_pdf_response(request, emp):
    qs = contrato_queryset(request, emp)
    headers = [
        'Empresa',
        'Número',
        'Proveedor',
        'Inicio',
        'Fin',
        'Monto',
        'Estado',
    ]
    rows = []
    for o in qs:
        rows.append(
            [
                cell_str(o.empresa),
                cell_str(o.numero),
                cell_str(o.proveedor.razon_social if o.proveedor_id else ''),
                cell_str(o.fecha_inicio),
                cell_str(o.fecha_fin),
                cell_str(o.monto_estimado),
                o.get_estado_display(),
            ]
        )
    title = f'Contratos — {contrato_subtitulo_informe(request)}'
    base = f'informe_contratos_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, title, headers, rows)
    if err == 'reportlab':
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return redirect_list_preserve_get(request, 'administrativo:contrato_list')
    return resp


def expediente_export_excel_response(request, emp):
    qs = expediente_queryset(request, emp)
    headers = [
        'Empresa',
        'Código',
        'Título',
        'Tipo',
        'Apertura',
        'Estado',
        'Descripción',
    ]
    rows = []
    for o in qs:
        rows.append(
            [
                cell_str(o.empresa),
                cell_str(o.codigo_interno),
                cell_str(o.titulo),
                o.get_tipo_display(),
                cell_str(o.fecha_apertura),
                o.get_estado_display(),
                cell_str(o.descripcion)[:500],
            ]
        )
    base = f'informe_expedientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_excel(base, 'Expedientes', headers, rows)
    if err == 'openpyxl':
        messages.error(
            request,
            'La librería openpyxl no está instalada. Instálela con: pip install openpyxl',
        )
        return redirect_list_preserve_get(request, 'administrativo:expediente_list')
    return resp


def expediente_export_pdf_response(request, emp):
    qs = expediente_queryset(request, emp)
    headers = ['Empresa', 'Código', 'Título', 'Tipo', 'Apertura', 'Estado']
    rows = []
    for o in qs:
        rows.append(
            [
                cell_str(o.empresa),
                cell_str(o.codigo_interno),
                cell_str(o.titulo),
                o.get_tipo_display(),
                cell_str(o.fecha_apertura),
                o.get_estado_display(),
            ]
        )
    title = f'Expedientes — {expediente_subtitulo_informe(request)}'
    base = f'informe_expedientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    resp, err = build_http_pdf(base, title, headers, rows)
    if err == 'reportlab':
        messages.error(
            request,
            'La librería reportlab no está instalada. Instálela con: pip install reportlab',
        )
        return redirect_list_preserve_get(request, 'administrativo:expediente_list')
    return resp

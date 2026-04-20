# -*- coding: utf-8 -*-
import json
import os
from datetime import date
from functools import wraps

from django.contrib import messages
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models import Departamento

from .forms import (
    ContratoAdministrativoForm,
    DepartamentoForm,
    ExpedienteGestionForm,
    ProveedorForm,
)
from . import reporting
from .models import ContratoAdministrativo, ExpedienteGestion, Proveedor


def administrativo_require_auth(view_func):
    """Requiere sesión del menú modular (`modules_core`)."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('modules_core:login_principal')
        return view_func(request, *args, **kwargs)

    return wrapper


def _empresa_session(request):
    return (request.session.get('empresa') or '').strip()


def _ctx_base(request):
    return {
        'usuario': request.session.get('nombre'),
        'empresa': _empresa_session(request),
    }


# --- Hub principal ---
@administrativo_require_auth
def menu_principal(request):
    emp = _empresa_session(request)
    ctx = _ctx_base(request)
    prov = Proveedor.objects.all()
    con = ContratoAdministrativo.objects.all()
    exp = ExpedienteGestion.objects.all()
    if emp:
        prov = prov.filter(empresa=emp)
        con = con.filter(empresa=emp)
        exp = exp.filter(empresa=emp)
    hoy = date.today()
    con_fil = con.filter(estado=ContratoAdministrativo.ESTADO_VIGENTE)
    con_vigentes = con_fil.count()
    con_por_vencer = con_fil.filter(fecha_fin__isnull=False, fecha_fin__lt=hoy).count()
    ctx.update({
        'titulo': 'Gestión administrativa',
        'count_proveedores': prov.count(),
        'count_proveedores_activos': prov.filter(activo=True).count(),
        'count_contratos': con.count(),
        'count_contratos_vigentes': con_vigentes,
        'count_contratos_revision_fecha': con_por_vencer,
        'count_expedientes': exp.count(),
        'count_expedientes_abiertos': exp.filter(
            estado__in=(ExpedienteGestion.ESTADO_ABIERTO, ExpedienteGestion.ESTADO_TRAMITE)
        ).count(),
        'sin_empresa': not bool(emp),
    })
    return render(request, 'administrativo/menu.html', ctx)


# --- Proveedores ---
@administrativo_require_auth
def proveedor_list(request):
    emp = _empresa_session(request)
    qs = reporting.proveedor_queryset(request, emp)
    perfil = (request.GET.get('perfil') or '').strip()
    ctx = _ctx_base(request)
    ctx.update({
        'titulo': 'Proveedores y contratistas',
        'object_list': qs,
        'search': (request.GET.get('search') or '').strip(),
        'perfil_filtro': perfil,
        'export_querystring': reporting.export_querystring(request),
        'reporte_subtitulo': reporting.proveedor_subtitulo_informe(request),
    })
    return render(request, 'administrativo/proveedor_list.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def proveedor_create(request):
    emp = _empresa_session(request)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, empresa_sesion=emp or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor guardado.')
            return redirect('administrativo:proveedor_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = ProveedorForm(initial={'empresa': emp} if emp else {}, empresa_sesion=emp or None)
    ctx = _ctx_base(request)
    ctx.update({'titulo': 'Nuevo proveedor', 'form': form})
    return render(request, 'administrativo/proveedor_form.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def proveedor_update(request, pk):
    emp = _empresa_session(request)
    if emp:
        obj = get_object_or_404(Proveedor, pk=pk, empresa=emp)
    else:
        obj = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES, instance=obj, empresa_sesion=emp or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado.')
            return redirect('administrativo:proveedor_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = ProveedorForm(instance=obj, empresa_sesion=emp or None)
    ctx = _ctx_base(request)
    ctx.update({'titulo': f'Editar proveedor — {obj.razon_social}', 'form': form, 'object': obj})
    return render(request, 'administrativo/proveedor_form.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def proveedor_delete(request, pk):
    emp = _empresa_session(request)
    if emp:
        obj = get_object_or_404(Proveedor, pk=pk, empresa=emp)
    else:
        obj = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Proveedor eliminado.')
        return redirect('administrativo:proveedor_list')
    ctx = _ctx_base(request)
    ctx.update({'titulo': 'Eliminar proveedor', 'object': obj})
    return render(request, 'administrativo/proveedor_confirm_delete.html', ctx)


@administrativo_require_auth
def proveedor_documentacion_descargar(request, pk):
    """Descarga del archivo solo si el proveedor pertenece al municipio en sesión."""
    emp = _empresa_session(request)
    if emp:
        obj = get_object_or_404(Proveedor, pk=pk, empresa=emp)
    else:
        obj = get_object_or_404(Proveedor, pk=pk)
    if not obj.documentacion or not obj.documentacion.name:
        raise Http404()
    try:
        path = obj.documentacion.path
    except NotImplementedError:
        path = None
    filename = os.path.basename(obj.documentacion.name)
    if path and os.path.isfile(path):
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=filename)
    fh = obj.documentacion.open('rb')
    return FileResponse(fh, as_attachment=True, filename=filename)


# --- Contratos ---
@administrativo_require_auth
def contrato_list(request):
    emp = _empresa_session(request)
    qs = reporting.contrato_queryset(request, emp)
    estado_f = (request.GET.get('estado') or '').strip()
    ctx = _ctx_base(request)
    ctx.update({
        'titulo': 'Contratos y órdenes administrativas',
        'object_list': qs,
        'search': (request.GET.get('search') or '').strip(),
        'estado_filtro': estado_f,
        'estados_choice': ContratoAdministrativo.ESTADO_CHOICES,
        'export_querystring': reporting.export_querystring(request),
        'reporte_subtitulo': reporting.contrato_subtitulo_informe(request),
    })
    return render(request, 'administrativo/contrato_list.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def contrato_create(request):
    emp = _empresa_session(request)
    if request.method == 'POST':
        form = ContratoAdministrativoForm(request.POST, empresa=emp or None, empresa_sesion=emp or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato guardado.')
            return redirect('administrativo:contrato_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = ContratoAdministrativoForm(
            initial={'empresa': emp} if emp else {},
            empresa=emp or None,
            empresa_sesion=emp or None,
        )
    ctx = _ctx_base(request)
    ctx.update({'titulo': 'Nuevo contrato / orden', 'form': form})
    return render(request, 'administrativo/contrato_form.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def contrato_update(request, pk):
    emp = _empresa_session(request)
    obj = get_object_or_404(ContratoAdministrativo.objects.select_related('proveedor'), pk=pk)
    if emp and obj.empresa != emp:
        messages.error(request, 'El registro no pertenece a su empresa.')
        return redirect('administrativo:contrato_list')
    if request.method == 'POST':
        form = ContratoAdministrativoForm(
            request.POST,
            instance=obj,
            empresa=emp or obj.empresa,
            empresa_sesion=emp or None,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato actualizado.')
            return redirect('administrativo:contrato_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = ContratoAdministrativoForm(
            instance=obj,
            empresa=emp or obj.empresa,
            empresa_sesion=emp or None,
        )
    ctx = _ctx_base(request)
    ctx.update({'titulo': f'Editar contrato — {obj.numero}', 'form': form, 'object': obj})
    return render(request, 'administrativo/contrato_form.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def contrato_delete(request, pk):
    emp = _empresa_session(request)
    obj = get_object_or_404(ContratoAdministrativo, pk=pk)
    if emp and obj.empresa != emp:
        messages.error(request, 'El registro no pertenece a su empresa.')
        return redirect('administrativo:contrato_list')
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro eliminado.')
        return redirect('administrativo:contrato_list')
    ctx = _ctx_base(request)
    ctx.update({'titulo': 'Eliminar contrato', 'object': obj})
    return render(request, 'administrativo/contrato_confirm_delete.html', ctx)


# --- Expedientes ---
@administrativo_require_auth
def expediente_list(request):
    emp = _empresa_session(request)
    qs = reporting.expediente_queryset(request, emp)
    ctx = _ctx_base(request)
    ctx.update({
        'titulo': 'Expedientes de gestión',
        'object_list': qs,
        'search': (request.GET.get('search') or '').strip(),
        'tipo_filtro': (request.GET.get('tipo') or '').strip(),
        'estado_filtro': (request.GET.get('estado') or '').strip(),
        'tipos_choice': ExpedienteGestion.TIPO_CHOICES,
        'estados_exp_choice': ExpedienteGestion.ESTADO_CHOICES,
        'export_querystring': reporting.export_querystring(request),
        'reporte_subtitulo': reporting.expediente_subtitulo_informe(request),
    })
    return render(request, 'administrativo/expediente_list.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def expediente_create(request):
    emp = _empresa_session(request)
    if request.method == 'POST':
        form = ExpedienteGestionForm(request.POST, empresa_sesion=emp or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expediente guardado.')
            return redirect('administrativo:expediente_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = ExpedienteGestionForm(initial={'empresa': emp} if emp else {}, empresa_sesion=emp or None)
    ctx = _ctx_base(request)
    ctx.update({'titulo': 'Nuevo expediente', 'form': form})
    return render(request, 'administrativo/expediente_form.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def expediente_update(request, pk):
    emp = _empresa_session(request)
    obj = get_object_or_404(ExpedienteGestion, pk=pk)
    if emp and obj.empresa != emp:
        messages.error(request, 'El registro no pertenece a su empresa.')
        return redirect('administrativo:expediente_list')
    if request.method == 'POST':
        form = ExpedienteGestionForm(request.POST, instance=obj, empresa_sesion=emp or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expediente actualizado.')
            return redirect('administrativo:expediente_list')
        messages.error(request, 'Revise los datos del formulario.')
    else:
        form = ExpedienteGestionForm(instance=obj, empresa_sesion=emp or None)
    ctx = _ctx_base(request)
    ctx.update({'titulo': f'Editar expediente — {obj.codigo_interno}', 'form': form, 'object': obj})
    return render(request, 'administrativo/expediente_form.html', ctx)


@administrativo_require_auth
@require_http_methods(['GET', 'POST'])
def expediente_delete(request, pk):
    emp = _empresa_session(request)
    obj = get_object_or_404(ExpedienteGestion, pk=pk)
    if emp and obj.empresa != emp:
        messages.error(request, 'El registro no pertenece a su empresa.')
        return redirect('administrativo:expediente_list')
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Expediente eliminado.')
        return redirect('administrativo:expediente_list')
    ctx = _ctx_base(request)
    ctx.update({'titulo': 'Eliminar expediente', 'object': obj})
    return render(request, 'administrativo/expediente_confirm_delete.html', ctx)


# --- Informes (Excel / PDF; mismos filtros y categorías que el listado) ---
@administrativo_require_auth
def proveedor_export_excel(request):
    emp = _empresa_session(request)
    return reporting.proveedor_export_excel_response(request, emp)


@administrativo_require_auth
def proveedor_export_pdf(request):
    emp = _empresa_session(request)
    return reporting.proveedor_export_pdf_response(request, emp)


@administrativo_require_auth
def contrato_export_excel(request):
    emp = _empresa_session(request)
    return reporting.contrato_export_excel_response(request, emp)


@administrativo_require_auth
def contrato_export_pdf(request):
    emp = _empresa_session(request)
    return reporting.contrato_export_pdf_response(request, emp)


@administrativo_require_auth
def expediente_export_excel(request):
    emp = _empresa_session(request)
    return reporting.expediente_export_excel_response(request, emp)


@administrativo_require_auth
def expediente_export_pdf(request):
    emp = _empresa_session(request)
    return reporting.expediente_export_pdf_response(request, emp)


# --- Legacy: departamento (mantener compatibilidad) ---
def departamento_crud(request):
    """Vista CRUD para Departamentos (legacy)."""
    mensaje = None
    exito = False

    if request.method == 'POST':
        action = request.POST.get('action', 'guardar')

        if action == 'guardar':
            form = DepartamentoForm(request.POST)
            if form.is_valid():
                try:
                    departamento = form.save()
                    mensaje = f"Departamento '{departamento.depto}' creado exitosamente."
                    exito = True
                    form = DepartamentoForm()
                except Exception as e:
                    mensaje = f"Error al crear el departamento: {str(e)}"
                    exito = False
            else:
                mensaje = "Por favor, corrija los errores en el formulario."
                exito = False

        elif action == 'actualizar':
            codigo = request.POST.get('depto') or request.POST.get('codigo')
            try:
                departamento = Departamento.objects.get(depto=codigo)
                form = DepartamentoForm(request.POST, instance=departamento)
                if form.is_valid():
                    departamento = form.save()
                    mensaje = f"Departamento '{departamento.depto}' actualizado exitosamente."
                    exito = True
                    form = DepartamentoForm()
                else:
                    mensaje = "Por favor, corrija los errores en el formulario."
                    exito = False
            except Departamento.DoesNotExist:
                mensaje = f"No se encontró el departamento con código {codigo}."
                exito = False
                form = DepartamentoForm()

        elif action == 'eliminar':
            codigo = request.POST.get('depto') or request.POST.get('codigo')
            try:
                departamento = Departamento.objects.get(depto=codigo)
                codigo_eliminado = departamento.depto
                departamento.delete()
                mensaje = f"Departamento '{codigo_eliminado}' eliminado exitosamente."
                exito = True
                form = DepartamentoForm()
            except Departamento.DoesNotExist:
                mensaje = f"No se encontró el departamento con código {codigo}."
                exito = False
                form = DepartamentoForm()

        elif action == 'nuevo':
            form = DepartamentoForm()
            mensaje = "Formulario listo para nuevo departamento."
            exito = True
    else:
        form = DepartamentoForm()

    departamentos = Departamento.objects.all().order_by('depto')

    context = {
        'form': form,
        'departamentos': departamentos,
        'mensaje': mensaje,
        'exito': exito,
    }

    return render(request, 'formulario_departamento.html', context)


@csrf_exempt
@require_http_methods(['POST'])
def buscar_departamento(request):
    """Vista AJAX para buscar departamento (legacy)."""
    try:
        data = json.loads(request.body)
        codigo = data.get('codigo', '').strip()

        if not codigo:
            return JsonResponse({'exito': False, 'mensaje': 'Código es requerido'})

        try:
            departamento = Departamento.objects.get(depto=codigo)
            return JsonResponse({
                'exito': True,
                'departamento': {
                    'depto': departamento.depto,
                    'codigo': departamento.depto,
                    'descripcion': departamento.descripcion,
                },
            })
        except Departamento.DoesNotExist:
            return JsonResponse({
                'exito': False,
                'mensaje': f'No se encontró el departamento con código {codigo}',
            })

    except json.JSONDecodeError:
        return JsonResponse({'exito': False, 'mensaje': 'Datos JSON inválidos'})
    except Exception as e:
        return JsonResponse({'exito': False, 'mensaje': f'Error interno: {str(e)}'})

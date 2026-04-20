"""
Vistas del Módulo de Contabilidad - SIMAFI Web
Basado en Normas Internacionales de Contabilidad (NIC/IAS)
"""
import json
from decimal import Decimal
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q, OuterRef, Subquery
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import (
    EjercicioFiscal, PeriodoContable, GrupoCuenta, CuentaContable,
    CentroCosto, Moneda, TipoAsiento, AsientoContable, DetalleAsiento,
    LibroMayor, ActivoFijo, Depreciacion, Inventario, Provision, TipoInventario,
)
from .forms import (
    EjercicioFiscalForm, CuentaContableForm, AsientoContableForm,
    DetalleAsientoForm, ActivoFijoForm, InventarioForm, ProvisionForm,
    CentroCostoForm, GRUPO_ETIQUETAS, TipoInventarioForm,
)


# ============================================================================
# UTILIDADES
# ============================================================================

# Grupos por defecto para el plan de cuentas (si no existen en BD)
GRUPOS_DEFAULT_BD = [
    {'codigo': '1', 'nombre': 'Activo', 'naturaleza': 'DEUDORA', 'orden': 1},
    {'codigo': '2', 'nombre': 'Pasivo', 'naturaleza': 'ACREEDORA', 'orden': 2},
    {'codigo': '3', 'nombre': 'Patrimonio', 'naturaleza': 'ACREEDORA', 'orden': 3},
    {'codigo': '4', 'nombre': 'Cuentas de Orden', 'naturaleza': 'ACREEDORA', 'orden': 4},
    {'codigo': '5', 'nombre': 'Ingresos', 'naturaleza': 'ACREEDORA', 'orden': 5},
    {'codigo': '6', 'nombre': 'Gastos', 'naturaleza': 'DEUDORA', 'orden': 6},
    {'codigo': '7', 'nombre': 'Gastos Administrativos y Otros', 'naturaleza': 'DEUDORA', 'orden': 7},
]

TASIO_DEFAULTS = [
    # Nota: esto evita que el combo "Tipo de Asiento" salga vacío
    # cuando la BD aún no tiene datos precargados.
    {'codigo': '01', 'nombre': 'Asiento Manual', 'prefijo': 'M', 'es_automatico': False},
    {'codigo': '02', 'nombre': 'Asiento de Ajuste', 'prefijo': 'AJ', 'es_automatico': False},
    {'codigo': '03', 'nombre': 'Asiento Automático', 'prefijo': 'AUTO', 'es_automatico': True},
]


def ensure_tipos_asiento_plan_cuentas():
    """Crea tipos de asiento mínimos si la tabla está vacía (para que el combo no quede sin opciones)."""
    if TipoAsiento.objects.filter(is_active=True).exists():
        return

    for t in TASIO_DEFAULTS:
        TipoAsiento.objects.get_or_create(
            codigo=t['codigo'],
            defaults={
                'nombre': t['nombre'],
                'prefijo': t['prefijo'],
                'descripcion': 'Tipo de asiento (configuración inicial)',
                'es_automatico': t['es_automatico'],
            },
        )


def ensure_grupos_plan_cuentas():
    """Crea los 7 grupos contables por defecto si no existen (para que el combo Grupo tenga opciones)."""
    if GrupoCuenta.objects.filter(is_active=True).exists():
        return
    for g in GRUPOS_DEFAULT_BD:
        GrupoCuenta.objects.get_or_create(
            codigo=g['codigo'],
            defaults={'nombre': g['nombre'], 'naturaleza': g['naturaleza'], 'orden': g['orden']},
        )


def get_grupo_choices_para_vista():
    """Lista (value, label) para el combo Grupo en el template, con etiquetas como en la explicación."""
    ensure_grupos_plan_cuentas()
    grupos = GrupoCuenta.objects.filter(is_active=True).order_by('codigo')
    return [
        (str(g.pk), GRUPO_ETIQUETAS.get(g.codigo) or f"{g.codigo} - {g.nombre}")
        for g in grupos
    ]


def cuentas_seleccionables_para_movimiento(empresa):
    """
    Cuentas del plan de la empresa utilizables en formularios (inventario NIC 2, activos, etc.).

    El sistema no infiere automáticamente qué cuenta es «de inventario»: debe existir en el plan de cuentas
    y el usuario elige la subcuenta de detalle adecuada (p. ej. existencias bajo Activo, y costo de ventas/consumo bajo Gastos).

    Criterio (igual que en asiento_crear):
    1) Preferir cuentas con «Acepta movimiento».
    2) Si no hay ninguna, usar tipo DETALLE (p. ej. datos cargados sin marcar el checkbox).
    3) Si aún no hay, mostrar todas las cuentas activas de la empresa para no dejar el combo vacío.
    """
    emp = (empresa or "").strip()
    if not emp:
        return CuentaContable.objects.none()
    cuentas_base = CuentaContable.objects.filter(empresa=emp, is_active=True).order_by("codigo")
    cuentas = cuentas_base.filter(acepta_movimiento=True)
    if not cuentas.exists():
        cuentas = cuentas_base.filter(tipo="DETALLE")
    if not cuentas.exists():
        cuentas = cuentas_base
    return cuentas


def _aplicar_queryset_cuentas_inventario(form, empresa):
    """Asigna el mismo queryset a cuenta_inventario y cuenta_costo_venta (debe llamarse también en POST)."""
    cuentas = cuentas_seleccionables_para_movimiento(empresa)
    form.fields["cuenta_inventario"].queryset = cuentas
    form.fields["cuenta_costo_venta"].queryset = cuentas
    return cuentas


def _queryset_cuentas_inventario_solo_html(form, inv=None):
    """
    En GET del formulario inventario: no renderizar miles de <option> (búsqueda vía Select2 + AJAX).
    - Alta: queryset vacío; el usuario elige cuenta y Select2 envía el id en POST (validado con queryset completo).
    - Edición: solo la(s) cuenta(s) ya guardada(s) para mostrar el valor inicial.
    """
    if inv is None:
        form.fields["cuenta_inventario"].queryset = CuentaContable.objects.none()
        form.fields["cuenta_costo_venta"].queryset = CuentaContable.objects.none()
        return
    ci = inv.cuenta_inventario_id
    cc = inv.cuenta_costo_venta_id
    form.fields["cuenta_inventario"].queryset = (
        CuentaContable.objects.filter(pk=ci) if ci else CuentaContable.objects.none()
    )
    form.fields["cuenta_costo_venta"].queryset = (
        CuentaContable.objects.filter(pk=cc) if cc else CuentaContable.objects.none()
    )


def get_empresa(request):
    """Obtiene la empresa del usuario en sesión"""
    return request.session.get('empresa', '')


def verificar_sesion(request):
    """Verifica si el usuario tiene sesión activa"""
    return request.session.get('user_id') is not None


# ============================================================================
# LOGIN / LOGOUT / MENÚ
# ============================================================================

def contabilidad_login(request):
    """Vista de login del módulo contabilidad"""
    if verificar_sesion(request):
        return redirect('contabilidad:contabilidad_menu_principal')
    return redirect('modules_core:login_principal')


def contabilidad_logout(request):
    """Vista de logout del módulo contabilidad"""
    messages.success(request, 'Sesión del módulo Contabilidad cerrada correctamente')
    return redirect('modules_core:menu_principal')


def contabilidad_menu_principal(request):
    """Menú principal del módulo contabilidad con estadísticas"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)

    # Estadísticas generales
    total_cuentas = CuentaContable.objects.filter(empresa=empresa, is_active=True).count()
    total_asientos = AsientoContable.objects.filter(empresa=empresa).count()
    asientos_borrador = AsientoContable.objects.filter(empresa=empresa, estado='BORRADOR').count()
    total_activos_fijos = ActivoFijo.objects.filter(empresa=empresa, estado='ACTIVO').count()

    # Ejercicio fiscal activo
    ejercicio_activo = EjercicioFiscal.objects.filter(empresa=empresa, estado='ABIERTO').first()

    context = {
        'modulo': 'Contabilidad',
        'descripcion': 'Sistema Contable basado en NIC/IAS',
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
        'total_cuentas': total_cuentas,
        'total_asientos': total_asientos,
        'asientos_borrador': asientos_borrador,
        'total_activos_fijos': total_activos_fijos,
        'ejercicio_activo': ejercicio_activo,
        'opciones_menu': [
            {
                'nombre': 'Configuración inicial',
                'descripcion': 'Guía paso a paso: Activo, Pasivo, Capital, Ingresos y Egresos',
                'url': 'contabilidad:configuracion_inicial',
                'icono': 'fas fa-road',
                'color': '#16a085'
            },
            {
                'nombre': 'Plan de Cuentas',
                'descripcion': 'Catálogo de cuentas contables (Marco Conceptual)',
                'url': 'contabilidad:plan_cuentas',
                'icono': 'fas fa-sitemap',
                'color': '#3498db'
            },
            {
                'nombre': 'Asientos Contables',
                'descripcion': 'Registro de asientos en libro diario (NIC 1)',
                'url': 'contabilidad:asientos_lista',
                'icono': 'fas fa-book-open',
                'color': '#2ecc71'
            },
            {
                'nombre': 'Libro Mayor / Auxiliar de Cuenta',
                'descripcion': 'Saldos y movimientos por cuenta contable (NIC 1)',
                'url': 'contabilidad:libro_mayor',
                'icono': 'fas fa-book',
                'color': '#9b59b6'
            },
            {
                'nombre': 'Estados Financieros',
                'descripcion': 'Balance General, Estado de Resultados y Balanza de Comprobación (NIC 1)',
                'url': 'contabilidad:estados_financieros',
                'icono': 'fas fa-file-invoice-dollar',
                'color': '#e74c3c'
            },
            {
                'nombre': 'Balanza de Comprobación',
                'descripcion': 'Débitos, créditos y saldos por cuenta (comprobación)',
                'url': 'contabilidad:balanza_comprobacion',
                'icono': 'fas fa-balance-scale-right',
                'color': '#1abc9c'
            },
            {
                'nombre': 'Activos Fijos',
                'descripcion': 'Propiedad, planta y equipo (NIC 16)',
                'url': 'contabilidad:activos_fijos',
                'icono': 'fas fa-industry',
                'color': '#f39c12'
            },
            {
                'nombre': 'Inventarios',
                'descripcion': 'Valoración de inventarios (NIC 2)',
                'url': 'contabilidad:inventarios',
                'icono': 'fas fa-boxes',
                'color': '#1abc9c'
            },
            {
                'nombre': 'Ejercicios Fiscales',
                'descripcion': 'Gestión de períodos contables',
                'url': 'contabilidad:ejercicios_fiscales',
                'icono': 'fas fa-calendar-alt',
                'color': '#34495e'
            },
            {
                'nombre': 'Centros de Costo',
                'descripcion': 'Distribución de gastos e ingresos',
                'url': 'contabilidad:centros_costo',
                'icono': 'fas fa-project-diagram',
                'color': '#e67e22'
            },
            {
                'nombre': 'Informes CGR',
                'descripcion': 'Contraloría General de la República (ejecución presupuestaria)',
                'url': 'contabilidad:cgr_informes_hub',
                'icono': 'fas fa-shield-alt',
                'color': '#2c3e50'
            },
        ]
    }
    return render(request, 'contabilidad_menu_principal.html', context)


def configuracion_inicial(request):
    """Vista de ayuda: configuración inicial y cómo configurar Activo, Pasivo, Capital, Ingresos y Egresos"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')
    context = {
        'usuario': request.session.get('nombre', ''),
        'empresa': get_empresa(request),
    }
    return render(request, 'contabilidad_configuracion_inicial.html', context)


# ============================================================================
# PLAN DE CUENTAS (Marco Conceptual / NIC 1)
# ============================================================================

def plan_cuentas(request):
    """Vista del catálogo de cuentas contables jerárquico"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    grupos = GrupoCuenta.objects.filter(is_active=True).order_by('codigo')
    cuentas = CuentaContable.objects.filter(empresa=empresa, is_active=True).order_by('codigo')

    # Filtros
    grupo_filtro = request.GET.get('grupo', '')
    tipo_filtro = request.GET.get('tipo', '')
    busqueda = request.GET.get('q', '')

    if grupo_filtro:
        cuentas = cuentas.filter(grupo__codigo=grupo_filtro)
    if tipo_filtro:
        cuentas = cuentas.filter(tipo=tipo_filtro)
    if busqueda:
        cuentas = cuentas.filter(Q(codigo__icontains=busqueda) | Q(nombre__icontains=busqueda))

    context = {
        'cuentas': cuentas,
        'grupos': grupos,
        'grupo_filtro': grupo_filtro,
        'tipo_filtro': tipo_filtro,
        'busqueda': busqueda,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_plan_cuentas.html', context)


def cuenta_crear(request):
    """Crear nueva cuenta contable"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)

    if request.method == 'POST':
        form = CuentaContableForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.empresa = empresa
            cuenta.created_by = request.session.get('usuario', '')
            cuenta.save()
            messages.success(request, f'Cuenta {cuenta.codigo} - {cuenta.nombre} guardada. Puede seguir agregando más cuentas o terminar e ir al plan de cuentas.')
            return redirect('contabilidad:cuenta_crear')
    else:
        form = CuentaContableForm(initial={'empresa': empresa})

    # Filtrar cuentas padre por empresa
    form.fields['cuenta_padre'].queryset = CuentaContable.objects.filter(
        empresa=empresa, tipo='TITULO', is_active=True
    ).order_by('codigo')

    context = {
        'form': form,
        'titulo': 'Nueva Cuenta Contable',
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
        'grupo_choices': get_grupo_choices_para_vista(),
    }
    return render(request, 'contabilidad_cuenta_form.html', context)


def cuenta_editar(request, pk):
    """Editar cuenta contable existente"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    cuenta = get_object_or_404(CuentaContable, pk=pk, empresa=empresa)

    if request.method == 'POST':
        form = CuentaContableForm(request.POST, instance=cuenta)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.updated_by = request.session.get('usuario', '')
            cuenta.save()
            messages.success(request, f'Cuenta {cuenta.codigo} actualizada exitosamente')
            return redirect('contabilidad:plan_cuentas')
    else:
        form = CuentaContableForm(instance=cuenta)

    form.fields['cuenta_padre'].queryset = CuentaContable.objects.filter(
        empresa=empresa, tipo='TITULO', is_active=True
    ).exclude(pk=pk).order_by('codigo')

    context = {
        'form': form,
        'titulo': f'Editar Cuenta: {cuenta.codigo}',
        'cuenta': cuenta,
        'usuario': request.session.get('nombre', ''),
        'grupo_choices': get_grupo_choices_para_vista(),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_cuenta_form.html', context)


def cuenta_eliminar(request, pk):
    """Eliminar (desactivar) cuenta contable"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    cuenta = get_object_or_404(CuentaContable, pk=pk, empresa=empresa)

    if request.method == 'POST':
        # Verificar que no tenga movimientos
        tiene_movimientos = DetalleAsiento.objects.filter(cuenta=cuenta).exists()
        if tiene_movimientos:
            messages.error(request, f'No se puede eliminar la cuenta {cuenta.codigo} porque tiene movimientos asociados')
        else:
            cuenta.is_active = False
            cuenta.save()
            messages.success(request, f'Cuenta {cuenta.codigo} eliminada exitosamente')

    return redirect('contabilidad:plan_cuentas')


def ajax_cuenta_por_codigo(request):
    """AJAX: verifica si existe una cuenta por código y empresa; si existe, devuelve URL para editar (mostrar datos)."""
    if not verificar_sesion(request):
        return JsonResponse({'existe': False, 'error': 'no_sesion'}, status=401)
    codigo = (request.GET.get('codigo') or '').strip()
    if not codigo:
        return JsonResponse({'existe': False})
    empresa = get_empresa(request)
    cuenta = CuentaContable.objects.filter(
        empresa=empresa, codigo=codigo, is_active=True
    ).first()
    if not cuenta:
        return JsonResponse({'existe': False})
    return JsonResponse({
        'existe': True,
        'pk': cuenta.pk,
        'codigo': cuenta.codigo,
        'nombre': cuenta.nombre,
        'url_editar': reverse('contabilidad:cuenta_editar', args=[cuenta.pk]),
    })


# ============================================================================
# ASIENTOS CONTABLES (NIC 1 - Libro Diario)
# ============================================================================

def asientos_lista(request):
    """Listado de asientos contables"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    asientos = AsientoContable.objects.filter(empresa=empresa).select_related('tipo', 'periodo')

    # Filtros
    estado_filtro = request.GET.get('estado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    busqueda = request.GET.get('q', '')

    if estado_filtro:
        asientos = asientos.filter(estado=estado_filtro)
    if fecha_desde:
        asientos = asientos.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        asientos = asientos.filter(fecha__lte=fecha_hasta)
    if busqueda:
        asientos = asientos.filter(
            Q(numero__icontains=busqueda) | Q(concepto__icontains=busqueda)
        )

    context = {
        'asientos': asientos[:100],
        'estado_filtro': estado_filtro,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'busqueda': busqueda,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_asientos_lista.html', context)


def asiento_crear(request):
    """Crear nuevo asiento contable con líneas de detalle"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    ensure_tipos_asiento_plan_cuentas()
    cuentas = cuentas_seleccionables_para_movimiento(empresa)
    tipos_asiento = TipoAsiento.objects.filter(is_active=True).order_by('codigo')
    periodos = PeriodoContable.objects.filter(
        ejercicio__empresa=empresa, estado='ABIERTO'
    ).select_related('ejercicio')
    centros = CentroCosto.objects.filter(empresa=empresa, is_active=True)

    if request.method == 'POST':
        form = AsientoContableForm(request.POST)
        # Asegurar que el dropdown muestre las opciones activas (y valide correctamente).
        form.fields['tipo'].queryset = tipos_asiento
        if form.is_valid():
            asiento = form.save(commit=False)
            asiento.empresa = empresa
            asiento.created_by = request.session.get('usuario', '')
            asiento.save()

            # Procesar líneas de detalle
            lineas = json.loads(request.POST.get('lineas_json', '[]'))
            total_debe = Decimal('0.00')
            total_haber = Decimal('0.00')

            for i, linea in enumerate(lineas, 1):
                if linea.get('cuenta_id'):
                    debe = Decimal(str(linea.get('debe', '0')))
                    haber = Decimal(str(linea.get('haber', '0')))
                    DetalleAsiento.objects.create(
                        asiento=asiento,
                        linea=i,
                        cuenta_id=linea['cuenta_id'],
                        concepto=linea.get('concepto', ''),
                        debe=debe,
                        haber=haber,
                        centro_costo_id=linea.get('centro_costo_id') or None,
                        tercero=linea.get('tercero', ''),
                        referencia=linea.get('referencia', ''),
                    )
                    total_debe += debe
                    total_haber += haber

            asiento.total_debe = total_debe
            asiento.total_haber = total_haber
            asiento.save(update_fields=['total_debe', 'total_haber'])

            if total_debe == total_haber:
                messages.success(request, f'Asiento {asiento.numero} creado exitosamente. ¡El asiento cuadra!')
            else:
                messages.warning(request, f'Asiento {asiento.numero} creado, pero NO cuadra. Debe: {total_debe}, Haber: {total_haber}')

            return redirect('contabilidad:asientos_lista')
    else:
        form = AsientoContableForm(initial={'empresa': empresa})
        form.fields['tipo'].queryset = tipos_asiento

    context = {
        'form': form,
        'cuentas': cuentas,
        'tipos_asiento': tipos_asiento,
        'periodos': periodos,
        'centros': centros,
        'titulo': 'Nuevo Asiento Contable',
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_asiento_contable.html', context)


def asiento_ver(request, pk):
    """Ver detalle de un asiento contable"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    asiento = get_object_or_404(AsientoContable, pk=pk, empresa=empresa)
    detalles = asiento.detalles.all().select_related('cuenta', 'centro_costo')

    context = {
        'asiento': asiento,
        'detalles': detalles,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_asiento_ver.html', context)


def asiento_aprobar(request, pk):
    """Aprobar un asiento contable"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    asiento = get_object_or_404(AsientoContable, pk=pk, empresa=empresa)

    if asiento.estado == 'BORRADOR':
        if asiento.esta_cuadrado:
            from django.utils import timezone as tz
            asiento.estado = 'APROBADO'
            asiento.aprobado_por = request.session.get('usuario', '')
            asiento.fecha_aprobacion = tz.now()
            asiento.save()
            messages.success(request, f'Asiento {asiento.numero} aprobado exitosamente')
        else:
            messages.error(request, f'No se puede aprobar el asiento {asiento.numero}: no está cuadrado')
    else:
        messages.warning(request, f'El asiento {asiento.numero} no puede ser aprobado (estado: {asiento.estado})')

    return redirect('contabilidad:asiento_ver', pk=pk)


def asiento_contabilizar(request, pk):
    """Contabilizar un asiento aprobado (actualiza libro mayor)"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    asiento = get_object_or_404(AsientoContable, pk=pk, empresa=empresa)

    if asiento.estado == 'APROBADO':
        # Actualizar libro mayor por cada línea
        for detalle in asiento.detalles.all():
            libro, created = LibroMayor.objects.get_or_create(
                cuenta=detalle.cuenta,
                periodo=asiento.periodo,
                empresa=empresa,
                defaults={'saldo_anterior': Decimal('0.00')}
            )
            libro.debitos += detalle.debe
            libro.creditos += detalle.haber
            libro.calcular_saldo_final()
            libro.save()

        asiento.estado = 'CONTABILIZADO'
        asiento.save()
        messages.success(request, f'Asiento {asiento.numero} contabilizado. Libro mayor actualizado.')
    else:
        messages.warning(request, f'Solo se pueden contabilizar asientos aprobados')

    return redirect('contabilidad:asiento_ver', pk=pk)


# ============================================================================
# LIBRO MAYOR
# ============================================================================

def libro_mayor(request):
    """Consulta del libro mayor por cuenta y período"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    cuentas = CuentaContable.objects.filter(empresa=empresa, is_active=True).order_by('codigo')
    ejercicios = EjercicioFiscal.objects.filter(empresa=empresa).order_by('-anio')

    cuenta_id = request.GET.get('cuenta', '')
    ejercicio_id = request.GET.get('ejercicio', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    registros = []
    cuenta_seleccionada = None

    if ejercicio_id:
        ejercicio_actual = EjercicioFiscal.objects.filter(pk=ejercicio_id, empresa=empresa).first()
        if ejercicio_actual:
            fecha_desde = fecha_desde or ejercicio_actual.fecha_inicio.isoformat()
            fecha_hasta = fecha_hasta or ejercicio_actual.fecha_fin.isoformat()

    if cuenta_id:
        cuenta_seleccionada = get_object_or_404(CuentaContable, pk=cuenta_id, empresa=empresa)
        registros_qs = LibroMayor.objects.filter(
            cuenta=cuenta_seleccionada, empresa=empresa
        ).select_related('periodo', 'periodo__ejercicio')

        if ejercicio_id:
            registros_qs = registros_qs.filter(periodo__ejercicio_id=ejercicio_id)

        # Filtro por rango (en base a fechas del período).
        if fecha_desde and fecha_hasta:
            registros_qs = registros_qs.filter(
                periodo__fecha_inicio__lte=fecha_hasta,
                periodo__fecha_fin__gte=fecha_desde,
            )
        elif fecha_desde:
            registros_qs = registros_qs.filter(periodo__fecha_fin__gte=fecha_desde)
        elif fecha_hasta:
            registros_qs = registros_qs.filter(periodo__fecha_fin__lte=fecha_hasta)

        registros = registros_qs.order_by('periodo__ejercicio__anio', 'periodo__numero')

    # Obtener movimientos individuales si hay cuenta seleccionada
    movimientos = []
    if cuenta_seleccionada:
        movimientos_qs = DetalleAsiento.objects.filter(
            cuenta=cuenta_seleccionada,
            asiento__empresa=empresa,
            asiento__estado='CONTABILIZADO'
        ).select_related('asiento').order_by('asiento__fecha', 'linea')

        if ejercicio_id:
            movimientos_qs = movimientos_qs.filter(asiento__periodo__ejercicio_id=ejercicio_id)

        if fecha_desde:
            movimientos_qs = movimientos_qs.filter(asiento__fecha__gte=fecha_desde)
        if fecha_hasta:
            movimientos_qs = movimientos_qs.filter(asiento__fecha__lte=fecha_hasta)

        movimientos = movimientos_qs[:200]

    context = {
        'cuentas': cuentas,
        'ejercicios': ejercicios,
        'registros': registros,
        'movimientos': movimientos,
        'cuenta_id': cuenta_id,
        'ejercicio_id': ejercicio_id,
        'cuenta_seleccionada': cuenta_seleccionada,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_libro_mayor.html', context)


# ============================================================================
# ESTADOS FINANCIEROS (NIC 1)
# ============================================================================

def _date_from_iso_or_none(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except Exception:
        return None


def _shift_year_safe(d, years):
    """
    Desplaza el año preservando mes/día cuando sea posible.
    Si la fecha cae en 29-feb y el año destino no es bisiesto, ajusta a 28-feb.
    """
    if d is None:
        return None
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        # Caso típico: 29-feb -> 28-feb
        return d.replace(year=d.year + years, day=28)


def _clamp_date(d, min_d, max_d):
    if d is None:
        return None
    if min_d and d < min_d:
        return min_d
    if max_d and d > max_d:
        return max_d
    return d


def _balance_por_grupo_a_fecha(*, empresa, ejercicio_id, fecha_hasta, codigo_grupo):
    """
    Balance General "a la fecha": saldo_final del último período <= fecha_hasta para cada cuenta.
    """
    libro_subq = LibroMayor.objects.filter(
        empresa=empresa,
        cuenta_id=OuterRef('pk'),
        periodo__ejercicio_id=ejercicio_id,
        periodo__fecha_fin__lte=fecha_hasta,
    ).order_by('-periodo__numero').values('saldo_final')[:1]

    cuentas = CuentaContable.objects.filter(
        empresa=empresa,
        grupo__codigo=codigo_grupo,
        is_active=True,
    ).annotate(saldo=Subquery(libro_subq)).order_by('codigo')

    out = []
    for c in cuentas:
        saldo = c.saldo if c.saldo is not None else Decimal('0.00')
        out.append({
            'cuenta__codigo': c.codigo,
            'cuenta__nombre': c.nombre,
            'saldo': saldo,
        })
    return out


def _resultado_por_grupos_rango(*, empresa, fecha_desde, fecha_hasta, codigos_grupo):
    """
    Estado de Resultados por rango usando DetalleAsiento (asientos CONTABILIZADOS).
    """
    qs = (
        DetalleAsiento.objects.filter(
            asiento__empresa=empresa,
            asiento__estado='CONTABILIZADO',
            cuenta__grupo__codigo__in=list(codigos_grupo),
            asiento__fecha__gte=fecha_desde,
            asiento__fecha__lte=fecha_hasta,
        )
        .values('cuenta__codigo', 'cuenta__nombre', 'cuenta__naturaleza')
        .annotate(total_debe=Sum('debe'), total_haber=Sum('haber'))
        .order_by('cuenta__codigo')
    )

    out = []
    total = Decimal('0.00')
    for r in qs:
        debe = r['total_debe'] or Decimal('0.00')
        haber = r['total_haber'] or Decimal('0.00')
        naturaleza = r['cuenta__naturaleza']
        saldo = (debe - haber) if naturaleza == 'DEUDORA' else (haber - debe)
        out.append({
            'cuenta__codigo': r['cuenta__codigo'],
            'cuenta__nombre': r['cuenta__nombre'],
            'saldo': saldo,
        })
        total += saldo or Decimal('0.00')
    return out, total


def estados_financieros(request):
    """Generación de estados financieros: Balance General y Estado de Resultados"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    ejercicios = EjercicioFiscal.objects.filter(empresa=empresa).order_by('-anio')
    ejercicio_id = request.GET.get('ejercicio', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    balance = {'activos': [], 'pasivos': [], 'patrimonio': []}
    resultado = {'ingresos': [], 'gastos': []}
    totales = {
        'total_activos': Decimal('0.00'),
        'total_pasivos': Decimal('0.00'),
        'total_patrimonio': Decimal('0.00'),
        'total_ingresos': Decimal('0.00'),
        'total_gastos': Decimal('0.00'),
        'utilidad_neta': Decimal('0.00'),
    }

    if ejercicio_id:
        ejercicio_actual = EjercicioFiscal.objects.filter(pk=ejercicio_id, empresa=empresa).first()
        if not ejercicio_actual:
            ejercicios = EjercicioFiscal.objects.filter(empresa=empresa).order_by('-anio')
        else:
            # Defaults: desde inicio y hasta fin del ejercicio, pero el usuario puede cambiarlo.
            fecha_desde = fecha_desde or ejercicio_actual.fecha_inicio.isoformat()
            fecha_hasta = fecha_hasta or ejercicio_actual.fecha_fin.isoformat()

        # Nota: el Balance General se calcula "a la fecha" usando el último saldo del Libro Mayor
        # cuyo período termina antes o en la fecha_hasta.
        def _balance_por_grupo(codigo_grupo):
            # Saldos: toma el saldo_final del último período <= fecha_hasta para cada cuenta.
            libro_subq = LibroMayor.objects.filter(
                empresa=empresa,
                cuenta_id=OuterRef('pk'),
                periodo__ejercicio_id=ejercicio_id,
                periodo__fecha_fin__lte=fecha_hasta,
            ).order_by('-periodo__numero').values('saldo_final')[:1]

            cuentas = CuentaContable.objects.filter(
                empresa=empresa,
                grupo__codigo=codigo_grupo,
                is_active=True,
            ).annotate(saldo=Subquery(libro_subq)).order_by('codigo')

            out = []
            for c in cuentas:
                saldo = c.saldo if c.saldo is not None else Decimal('0.00')
                out.append({
                    'cuenta__codigo': c.codigo,
                    'cuenta__nombre': c.nombre,
                    'saldo': saldo,
                })
            return out

        activos = _balance_por_grupo('1')
        pasivos = _balance_por_grupo('2')
        patrimonio = _balance_por_grupo('3')

        for a in activos:
            balance['activos'].append(a)
            totales['total_activos'] += a['saldo'] or Decimal('0.00')

        for p in pasivos:
            balance['pasivos'].append(p)
            totales['total_pasivos'] += p['saldo'] or Decimal('0.00')

        for pat in patrimonio:
            balance['patrimonio'].append(pat)
            totales['total_patrimonio'] += pat['saldo'] or Decimal('0.00')

        # Estado de Resultados: se calcula por rango usando las líneas (DetalleAsiento)
        # para evitar el problema de saldos acumulados por período.
        ingresos_qs = (
            DetalleAsiento.objects.filter(
                asiento__empresa=empresa,
                asiento__estado='CONTABILIZADO',
                cuenta__grupo__codigo='5',
                asiento__fecha__gte=fecha_desde,
                asiento__fecha__lte=fecha_hasta,
            )
            .values('cuenta__codigo', 'cuenta__nombre', 'cuenta__naturaleza')
            .annotate(total_debe=Sum('debe'), total_haber=Sum('haber'))
            .order_by('cuenta__codigo')
        )

        for i in ingresos_qs:
            debe = i['total_debe'] or Decimal('0.00')
            haber = i['total_haber'] or Decimal('0.00')
            naturaleza = i['cuenta__naturaleza']
            saldo = (debe - haber) if naturaleza == 'DEUDORA' else (haber - debe)
            resultado['ingresos'].append({
                'cuenta__codigo': i['cuenta__codigo'],
                'cuenta__nombre': i['cuenta__nombre'],
                'saldo': saldo,
            })
            totales['total_ingresos'] += saldo or Decimal('0.00')

        gastos_qs = (
            DetalleAsiento.objects.filter(
                asiento__empresa=empresa,
                asiento__estado='CONTABILIZADO',
                cuenta__grupo__codigo__in=['6', '7'],
                asiento__fecha__gte=fecha_desde,
                asiento__fecha__lte=fecha_hasta,
            )
            .values('cuenta__codigo', 'cuenta__nombre', 'cuenta__naturaleza')
            .annotate(total_debe=Sum('debe'), total_haber=Sum('haber'))
            .order_by('cuenta__codigo')
        )

        for g in gastos_qs:
            debe = g['total_debe'] or Decimal('0.00')
            haber = g['total_haber'] or Decimal('0.00')
            naturaleza = g['cuenta__naturaleza']
            saldo = (debe - haber) if naturaleza == 'DEUDORA' else (haber - debe)
            resultado['gastos'].append({
                'cuenta__codigo': g['cuenta__codigo'],
                'cuenta__nombre': g['cuenta__nombre'],
                'saldo': saldo,
            })
            totales['total_gastos'] += saldo or Decimal('0.00')

        totales['utilidad_neta'] = totales['total_ingresos'] - totales['total_gastos']

    context = {
        'ejercicios': ejercicios,
        'ejercicio_id': ejercicio_id,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'balance': balance,
        'resultado': resultado,
        'totales': totales,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_estados_financieros.html', context)


def balance_general_comparativo(request):
    """
    Modelo comparativo de Balance General:
    compara el ejercicio fiscal actual vs el ejercicio fiscal anterior a la misma fecha (fecha_hasta - 1 año).
    """
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    ejercicios = EjercicioFiscal.objects.filter(empresa=empresa).order_by('-anio')
    ejercicio_id = (request.GET.get('ejercicio') or '').strip()
    fecha_hasta_str = (request.GET.get('fecha_hasta') or '').strip()

    ejercicio_actual = None
    ejercicio_anterior = None
    fecha_hasta = None
    fecha_hasta_anterior = None

    comparativo = {
        'activos': [],
        'pasivos': [],
        'patrimonio': [],
    }
    totales = {
        'actual': {'activos': Decimal('0.00'), 'pasivos': Decimal('0.00'), 'patrimonio': Decimal('0.00')},
        'anterior': {'activos': Decimal('0.00'), 'pasivos': Decimal('0.00'), 'patrimonio': Decimal('0.00')},
        'variacion': {'activos': Decimal('0.00'), 'pasivos': Decimal('0.00'), 'patrimonio': Decimal('0.00')},
    }

    if ejercicio_id:
        ejercicio_actual = EjercicioFiscal.objects.filter(pk=ejercicio_id, empresa=empresa).first()
        if ejercicio_actual:
            ejercicio_anterior = EjercicioFiscal.objects.filter(
                empresa=empresa,
                anio=ejercicio_actual.anio - 1
            ).first()

            fecha_hasta = _date_from_iso_or_none(fecha_hasta_str)
            if fecha_hasta is None:
                # Default: fin del ejercicio actual
                fecha_hasta = ejercicio_actual.fecha_fin

            fecha_hasta = _clamp_date(fecha_hasta, ejercicio_actual.fecha_inicio, ejercicio_actual.fecha_fin)

            if ejercicio_anterior:
                fecha_hasta_anterior = _shift_year_safe(fecha_hasta, -1)
                fecha_hasta_anterior = _clamp_date(
                    fecha_hasta_anterior,
                    ejercicio_anterior.fecha_inicio,
                    ejercicio_anterior.fecha_fin
                )
            else:
                messages.warning(request, 'No se encontró el ejercicio fiscal anterior para comparación.')

            def _build_rows(codigo_grupo):
                actual_rows = _balance_por_grupo_a_fecha(
                    empresa=empresa,
                    ejercicio_id=ejercicio_actual.pk,
                    fecha_hasta=fecha_hasta,
                    codigo_grupo=codigo_grupo,
                )
                anterior_rows = []
                if ejercicio_anterior and fecha_hasta_anterior:
                    anterior_rows = _balance_por_grupo_a_fecha(
                        empresa=empresa,
                        ejercicio_id=ejercicio_anterior.pk,
                        fecha_hasta=fecha_hasta_anterior,
                        codigo_grupo=codigo_grupo,
                    )

                anterior_by_codigo = {r['cuenta__codigo']: r for r in anterior_rows}
                out = []
                for r in actual_rows:
                    prev = anterior_by_codigo.get(r['cuenta__codigo'])
                    saldo_actual = r['saldo'] or Decimal('0.00')
                    saldo_anterior = (prev['saldo'] if prev else Decimal('0.00')) or Decimal('0.00')
                    out.append({
                        'cuenta__codigo': r['cuenta__codigo'],
                        'cuenta__nombre': r['cuenta__nombre'],
                        'saldo_actual': saldo_actual,
                        'saldo_anterior': saldo_anterior,
                        'variacion': saldo_actual - saldo_anterior,
                    })
                return out

            comparativo['activos'] = _build_rows('1')
            comparativo['pasivos'] = _build_rows('2')
            comparativo['patrimonio'] = _build_rows('3')

            for row in comparativo['activos']:
                totales['actual']['activos'] += row['saldo_actual']
                totales['anterior']['activos'] += row['saldo_anterior']
            for row in comparativo['pasivos']:
                totales['actual']['pasivos'] += row['saldo_actual']
                totales['anterior']['pasivos'] += row['saldo_anterior']
            for row in comparativo['patrimonio']:
                totales['actual']['patrimonio'] += row['saldo_actual']
                totales['anterior']['patrimonio'] += row['saldo_anterior']

            totales['variacion']['activos'] = totales['actual']['activos'] - totales['anterior']['activos']
            totales['variacion']['pasivos'] = totales['actual']['pasivos'] - totales['anterior']['pasivos']
            totales['variacion']['patrimonio'] = totales['actual']['patrimonio'] - totales['anterior']['patrimonio']

    context = {
        'ejercicios': ejercicios,
        'ejercicio_id': ejercicio_id,
        'fecha_hasta': fecha_hasta.isoformat() if fecha_hasta else fecha_hasta_str,
        'ejercicio_actual': ejercicio_actual,
        'ejercicio_anterior': ejercicio_anterior,
        'fecha_hasta_anterior': fecha_hasta_anterior.isoformat() if fecha_hasta_anterior else '',
        'comparativo': comparativo,
        'totales': totales,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_balance_general_comparativo.html', context)


def estado_resultados_comparativo(request):
    """
    Modelo comparativo de Estado de Resultados:
    compara el rango [fecha_desde, fecha_hasta] del ejercicio actual vs el rango del ejercicio anterior
    desplazado 1 año (misma fecha calendario), ajustado al rango del ejercicio anterior.
    """
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    ejercicios = EjercicioFiscal.objects.filter(empresa=empresa).order_by('-anio')
    ejercicio_id = (request.GET.get('ejercicio') or '').strip()
    fecha_desde_str = (request.GET.get('fecha_desde') or '').strip()
    fecha_hasta_str = (request.GET.get('fecha_hasta') or '').strip()

    ejercicio_actual = None
    ejercicio_anterior = None
    fecha_desde = None
    fecha_hasta = None
    fecha_desde_anterior = None
    fecha_hasta_anterior = None

    ingresos = []
    gastos = []
    ingresos_prev = []
    gastos_prev = []
    totales = {
        'actual': {'ingresos': Decimal('0.00'), 'gastos': Decimal('0.00'), 'utilidad': Decimal('0.00')},
        'anterior': {'ingresos': Decimal('0.00'), 'gastos': Decimal('0.00'), 'utilidad': Decimal('0.00')},
        'variacion': {'ingresos': Decimal('0.00'), 'gastos': Decimal('0.00'), 'utilidad': Decimal('0.00')},
    }

    if ejercicio_id:
        ejercicio_actual = EjercicioFiscal.objects.filter(pk=ejercicio_id, empresa=empresa).first()
        if ejercicio_actual:
            ejercicio_anterior = EjercicioFiscal.objects.filter(
                empresa=empresa,
                anio=ejercicio_actual.anio - 1
            ).first()

            fecha_desde = _date_from_iso_or_none(fecha_desde_str) or ejercicio_actual.fecha_inicio
            fecha_hasta = _date_from_iso_or_none(fecha_hasta_str) or ejercicio_actual.fecha_fin
            fecha_desde = _clamp_date(fecha_desde, ejercicio_actual.fecha_inicio, ejercicio_actual.fecha_fin)
            fecha_hasta = _clamp_date(fecha_hasta, ejercicio_actual.fecha_inicio, ejercicio_actual.fecha_fin)

            ingresos, tot_ing = _resultado_por_grupos_rango(
                empresa=empresa, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta, codigos_grupo={'5'}
            )
            gastos, tot_gas = _resultado_por_grupos_rango(
                empresa=empresa, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta, codigos_grupo={'6', '7'}
            )
            totales['actual']['ingresos'] = tot_ing
            totales['actual']['gastos'] = tot_gas
            totales['actual']['utilidad'] = tot_ing - tot_gas

            if ejercicio_anterior:
                fecha_desde_anterior = _shift_year_safe(fecha_desde, -1)
                fecha_hasta_anterior = _shift_year_safe(fecha_hasta, -1)
                fecha_desde_anterior = _clamp_date(
                    fecha_desde_anterior, ejercicio_anterior.fecha_inicio, ejercicio_anterior.fecha_fin
                )
                fecha_hasta_anterior = _clamp_date(
                    fecha_hasta_anterior, ejercicio_anterior.fecha_inicio, ejercicio_anterior.fecha_fin
                )

                ingresos_prev, tot_ing_prev = _resultado_por_grupos_rango(
                    empresa=empresa,
                    fecha_desde=fecha_desde_anterior,
                    fecha_hasta=fecha_hasta_anterior,
                    codigos_grupo={'5'}
                )
                gastos_prev, tot_gas_prev = _resultado_por_grupos_rango(
                    empresa=empresa,
                    fecha_desde=fecha_desde_anterior,
                    fecha_hasta=fecha_hasta_anterior,
                    codigos_grupo={'6', '7'}
                )
                totales['anterior']['ingresos'] = tot_ing_prev
                totales['anterior']['gastos'] = tot_gas_prev
                totales['anterior']['utilidad'] = tot_ing_prev - tot_gas_prev
            else:
                messages.warning(request, 'No se encontró el ejercicio fiscal anterior para comparación.')

            totales['variacion']['ingresos'] = totales['actual']['ingresos'] - totales['anterior']['ingresos']
            totales['variacion']['gastos'] = totales['actual']['gastos'] - totales['anterior']['gastos']
            totales['variacion']['utilidad'] = totales['actual']['utilidad'] - totales['anterior']['utilidad']

    # Unificar por código para presentación comparativa
    def _merge(actual_rows, prev_rows):
        prev_by_codigo = {r['cuenta__codigo']: r for r in prev_rows}
        out = []
        for r in actual_rows:
            prev = prev_by_codigo.get(r['cuenta__codigo'])
            sa = r['saldo'] or Decimal('0.00')
            sp = (prev['saldo'] if prev else Decimal('0.00')) or Decimal('0.00')
            out.append({
                'cuenta__codigo': r['cuenta__codigo'],
                'cuenta__nombre': r['cuenta__nombre'],
                'saldo_actual': sa,
                'saldo_anterior': sp,
                'variacion': sa - sp,
            })
        return out

    comparativo = {
        'ingresos': _merge(ingresos, ingresos_prev),
        'gastos': _merge(gastos, gastos_prev),
    }

    context = {
        'ejercicios': ejercicios,
        'ejercicio_id': ejercicio_id,
        'ejercicio_actual': ejercicio_actual,
        'ejercicio_anterior': ejercicio_anterior,
        'fecha_desde': fecha_desde.isoformat() if fecha_desde else fecha_desde_str,
        'fecha_hasta': fecha_hasta.isoformat() if fecha_hasta else fecha_hasta_str,
        'fecha_desde_anterior': fecha_desde_anterior.isoformat() if fecha_desde_anterior else '',
        'fecha_hasta_anterior': fecha_hasta_anterior.isoformat() if fecha_hasta_anterior else '',
        'comparativo': comparativo,
        'totales': totales,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_estado_resultados_comparativo.html', context)


def balanza_comprobacion(request):
    """Balanza de comprobación por ejercicio: todas las cuentas con movimiento, débitos, créditos y saldos."""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    ejercicios = EjercicioFiscal.objects.filter(empresa=empresa).order_by('-anio')
    ejercicio_id = request.GET.get('ejercicio', '')
    filas = []
    total_debitos = Decimal('0.00')
    total_creditos = Decimal('0.00')
    total_saldo_deudor = Decimal('0.00')
    total_saldo_acreedor = Decimal('0.00')
    cuadra = False

    if ejercicio_id:
        qs = LibroMayor.objects.filter(
            empresa=empresa,
            periodo__ejercicio_id=ejercicio_id
        ).values(
            'cuenta_id', 'cuenta__codigo', 'cuenta__nombre', 'cuenta__naturaleza'
        ).annotate(
            total_debitos=Sum('debitos'),
            total_creditos=Sum('creditos')
        ).order_by('cuenta__codigo')

        for r in qs:
            deb = r['total_debitos'] or Decimal('0.00')
            cred = r['total_creditos'] or Decimal('0.00')
            # Saldo según naturaleza: DEUDORA = débitos - créditos; ACREEDORA = créditos - débitos
            if r['cuenta__naturaleza'] == 'DEUDORA':
                saldo = deb - cred
            else:
                saldo = cred - deb
            saldo_deudor = saldo if saldo > 0 else Decimal('0.00')
            saldo_acreedor = -saldo if saldo < 0 else Decimal('0.00')
            filas.append({
                'cuenta_id': r['cuenta_id'],
                'codigo': r['cuenta__codigo'],
                'nombre': r['cuenta__nombre'],
                'debitos': deb,
                'creditos': cred,
                'saldo_deudor': saldo_deudor,
                'saldo_acreedor': saldo_acreedor,
            })
            total_debitos += deb
            total_creditos += cred
            total_saldo_deudor += saldo_deudor
            total_saldo_acreedor += saldo_acreedor

        cuadra = (total_debitos == total_creditos) and (total_saldo_deudor == total_saldo_acreedor)

    ejercicio_actual = None
    if ejercicio_id:
        ejercicio_actual = EjercicioFiscal.objects.filter(pk=ejercicio_id, empresa=empresa).first()

    context = {
        'ejercicios': ejercicios,
        'ejercicio_id': ejercicio_id,
        'ejercicio_actual': ejercicio_actual,
        'filas': filas,
        'total_debitos': total_debitos,
        'total_creditos': total_creditos,
        'total_saldo_deudor': total_saldo_deudor,
        'total_saldo_acreedor': total_saldo_acreedor,
        'cuadra': cuadra,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_balanza_comprobacion.html', context)


# ============================================================================
# ACTIVOS FIJOS (NIC 16)
# ============================================================================

def activos_fijos(request):
    """Listado de activos fijos"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    activos = ActivoFijo.objects.filter(empresa=empresa).order_by('codigo')

    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        activos = activos.filter(estado=estado_filtro)

    context = {
        'activos': activos,
        'estado_filtro': estado_filtro,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_activos_fijos.html', context)


def activo_fijo_crear(request):
    """Crear nuevo activo fijo"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)

    if request.method == 'POST':
        form = ActivoFijoForm(request.POST)
        if form.is_valid():
            activo = form.save(commit=False)
            activo.empresa = empresa
            activo.valor_en_libros = activo.costo_adquisicion
            activo.created_by = request.session.get('usuario', '')
            activo.save()
            messages.success(request, f'Activo fijo {activo.codigo} creado exitosamente')
            return redirect('contabilidad:activos_fijos')
    else:
        form = ActivoFijoForm(initial={'empresa': empresa})

    cuentas = cuentas_seleccionables_para_movimiento(empresa)
    form.fields['cuenta_activo'].queryset = cuentas
    form.fields['cuenta_depreciacion'].queryset = cuentas
    form.fields['cuenta_gasto_depreciacion'].queryset = cuentas

    context = {
        'form': form,
        'titulo': 'Nuevo Activo Fijo (NIC 16)',
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_activo_fijo_form.html', context)


# ============================================================================
# INVENTARIOS (NIC 2)
# ============================================================================

# Misma lista que la migración 0003: referencia estándar (cargar tipos faltantes)
LEGACY_TIPOS_REFERENCIA = [
    ("MATERIA_PRIMA", "Materia prima e insumos", 10),
    ("SUMINISTROS", "Suministros de oficina y operación", 20),
    ("REPUESTOS", "Repuestos y accesorios", 30),
    ("MERCADERIA", "Mercadería para reventa", 40),
    ("PRODUCTO_TERMINADO", "Producto terminado", 50),
    ("EMBALAJE", "Embalajes y envases", 60),
    ("SERVICIOS_ALMACENADOS", "Servicios almacenables / pendientes", 70),
    ("OTROS", "Otros / diversos", 90),
]

NOTAS_TIPO_REF = (
    "Referencia del listado estándar original. Puede renombrar, desactivar o dejar de usar los que no apliquen "
    "a su municipio u organismo."
)

# Tabla guía en pantalla: qué significaba cada clave y cómo suele usarse al configurar el catálogo
REFERENCIA_INICIAL_TIPOS_GUIA = [
    {
        "clave": "MATERIA_PRIMA",
        "nombre": "Materia prima e insumos",
        "orden": 10,
        "guia": "Insumos que se transforman en servicio o producto (ej. materiales de obra, insumos de operación).",
    },
    {
        "clave": "SUMINISTROS",
        "nombre": "Suministros de oficina y operación",
        "orden": 20,
        "guia": "Papelería, útiles de escritorio, consumibles administrativos y similares.",
    },
    {
        "clave": "REPUESTOS",
        "nombre": "Repuestos y accesorios",
        "orden": 30,
        "guia": "Piezas para equipos, vehículos, bombas, válvulas; mantenimiento de infraestructura.",
    },
    {
        "clave": "MERCADERIA",
        "nombre": "Mercadería para reventa",
        "orden": 40,
        "guia": "Bienes adquiridos para reventa sin transformación (si aplica al negocio del ente).",
    },
    {
        "clave": "PRODUCTO_TERMINADO",
        "nombre": "Producto terminado",
        "orden": 50,
        "guia": "Productos acabados en almacén listos para entrega o distribución.",
    },
    {
        "clave": "EMBALAJE",
        "nombre": "Embalajes y envases",
        "orden": 60,
        "guia": "Envases retornables o de un solo uso vinculados a almacenamiento o distribución.",
    },
    {
        "clave": "SERVICIOS_ALMACENADOS",
        "nombre": "Servicios almacenables / pendientes",
        "orden": 70,
        "guia": "Costos de servicios en curso o pendientes de imputación cuando aplique su contabilización en inventario.",
    },
    {
        "clave": "OTROS",
        "nombre": "Otros / diversos",
        "orden": 90,
        "guia": "Residuo clasificatorio; use cuando ningún otro tipo encaje o como comodín inicial.",
    },
]


def inventarios(request):
    """Listado de inventarios"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    items = (
        Inventario.objects.filter(empresa=empresa, is_active=True)
        .select_related("tipo_inventario")
        .order_by("tipo_inventario__orden", "tipo_inventario__nombre", "codigo")
    )

    context = {
        'items': items,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_inventarios.html', context)


def tipo_inventario_list(request):
    """Catálogo de tipos de inventario por empresa."""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')
    empresa = get_empresa(request)
    tipos = TipoInventario.objects.filter(empresa=empresa).order_by("orden", "nombre")
    return render(
        request,
        "contabilidad_tipo_inventario_list.html",
        {
            "tipos": tipos,
            "usuario": request.session.get("nombre", ""),
            "empresa": empresa,
            "referencia_inicial": REFERENCIA_INICIAL_TIPOS_GUIA,
        },
    )


def tipo_inventario_crear(request):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    empresa = get_empresa(request)
    if request.method == "POST":
        form = TipoInventarioForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.empresa = empresa
            t.created_by = request.session.get("usuario", "")
            t.save()
            messages.success(request, f'Tipo "{t.nombre}" registrado.')
            return redirect("contabilidad:tipo_inventario_list")
    else:
        form = TipoInventarioForm(initial={"empresa": empresa, "orden": 100})
    return render(
        request,
        "contabilidad_tipo_inventario_form.html",
        {"form": form, "titulo": "Nuevo tipo de inventario", "empresa": empresa},
    )


def tipo_inventario_editar(request, pk):
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    empresa = get_empresa(request)
    tipo = get_object_or_404(TipoInventario, pk=pk, empresa=empresa)
    if request.method == "POST":
        form = TipoInventarioForm(request.POST, instance=tipo)
        if form.is_valid():
            t = form.save(commit=False)
            t.updated_by = request.session.get("usuario", "")
            t.save()
            messages.success(request, "Tipo actualizado.")
            return redirect("contabilidad:tipo_inventario_list")
    else:
        form = TipoInventarioForm(instance=tipo)
    return render(
        request,
        "contabilidad_tipo_inventario_form.html",
        {"form": form, "titulo": f'Editar tipo — {tipo.nombre}', "empresa": empresa, "tipo_obj": tipo},
    )


def tipo_inventario_referencias_cargar(request):
    """Inserta los tipos del listado estándar que falten (misma referencia que la migración)."""
    if not verificar_sesion(request):
        return redirect("modules_core:login_principal")
    if request.method != "POST":
        return redirect("contabilidad:tipo_inventario_list")
    empresa = get_empresa(request)
    creados = 0
    for clave, nombre, orden in LEGACY_TIPOS_REFERENCIA:
        obj, created = TipoInventario.objects.get_or_create(
            empresa=empresa,
            nombre=nombre,
            defaults={
                "orden": orden,
                "codigo_legacy": clave,
                "notas": NOTAS_TIPO_REF,
                "is_active": True,
            },
        )
        if created:
            creados += 1
        elif not obj.codigo_legacy:
            obj.codigo_legacy = clave
            obj.notas = obj.notas or NOTAS_TIPO_REF
            obj.save(update_fields=["codigo_legacy", "notas"])
    messages.success(
        request,
        f"Referencias estándar: {creados} nuevas; el resto ya existía.",
    )
    return redirect("contabilidad:tipo_inventario_list")


def inventario_crear(request):
    """Alta de ítem de inventario / bodega (NIC 2) con tipo y nomenclatura."""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)

    if request.method == 'POST':
        form = InventarioForm(request.POST, empresa=empresa)
        cuentas = _aplicar_queryset_cuentas_inventario(form, empresa)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.empresa = empresa
            inv.created_by = request.session.get('usuario', '')
            inv.save()
            messages.success(request, f'Ítem de inventario {inv.codigo} registrado correctamente.')
            return redirect('contabilidad:inventarios')
    else:
        form = InventarioForm(initial={'empresa': empresa}, empresa=empresa)
        cuentas = cuentas_seleccionables_para_movimiento(empresa)
        _queryset_cuentas_inventario_solo_html(form, None)

    context = {
        'form': form,
        'titulo': 'Nuevo ítem de inventario (bodega)',
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
        'es_edicion': False,
        'plan_cuentas_opciones': cuentas.count(),
    }
    return render(request, 'contabilidad_inventario_form.html', context)


def inventario_editar(request, pk):
    """Edición de ítem de inventario / bodega."""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    inv = get_object_or_404(Inventario, pk=pk, empresa=empresa, is_active=True)

    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inv, empresa=empresa)
        cuentas = _aplicar_queryset_cuentas_inventario(form, empresa)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.session.get('usuario', '')
            obj.save()
            messages.success(request, f'Ítem {obj.codigo} actualizado.')
            return redirect('contabilidad:inventarios')
    else:
        form = InventarioForm(instance=inv, empresa=empresa)
        cuentas = cuentas_seleccionables_para_movimiento(empresa)
        _queryset_cuentas_inventario_solo_html(form, inv)

    context = {
        'form': form,
        'titulo': f'Editar inventario — {inv.codigo}',
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
        'es_edicion': True,
        'inventario': inv,
        'plan_cuentas_opciones': cuentas.count(),
    }
    return render(request, 'contabilidad_inventario_form.html', context)


# ============================================================================
# EJERCICIOS FISCALES
# ============================================================================

def ejercicios_fiscales(request):
    """Gestión de ejercicios fiscales"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    ejercicios = EjercicioFiscal.objects.filter(empresa=empresa).order_by('-anio')

    context = {
        'ejercicios': ejercicios,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_ejercicios_fiscales.html', context)


def ejercicio_crear(request):
    """Crear nuevo ejercicio fiscal"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)

    if request.method == 'POST':
        form = EjercicioFiscalForm(request.POST)
        if form.is_valid():
            ejercicio = form.save(commit=False)
            ejercicio.empresa = empresa
            ejercicio.created_by = request.session.get('usuario', '')
            ejercicio.save()

            # Crear 12 períodos mensuales automáticamente
            import calendar
            for mes in range(1, 13):
                ultimo_dia = calendar.monthrange(ejercicio.anio, mes)[1]
                PeriodoContable.objects.create(
                    ejercicio=ejercicio,
                    numero=mes,
                    nombre=f'{calendar.month_name[mes]} {ejercicio.anio}',
                    fecha_inicio=f'{ejercicio.anio}-{mes:02d}-01',
                    fecha_fin=f'{ejercicio.anio}-{mes:02d}-{ultimo_dia:02d}',
                    estado='ABIERTO',
                )

            messages.success(request, f'Ejercicio fiscal {ejercicio.anio} creado con 12 períodos mensuales')
            return redirect('contabilidad:ejercicios_fiscales')
    else:
        import datetime
        anio_actual = datetime.date.today().year
        form = EjercicioFiscalForm(initial={
            'empresa': empresa,
            'anio': anio_actual,
            'descripcion': f'Ejercicio Fiscal {anio_actual}',
            'fecha_inicio': f'{anio_actual}-01-01',
            'fecha_fin': f'{anio_actual}-12-31',
        })

    context = {
        'form': form,
        'titulo': 'Nuevo Ejercicio Fiscal',
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_ejercicio_form.html', context)


# ============================================================================
# CENTROS DE COSTO
# ============================================================================

def centros_costo(request):
    """Listado de centros de costo"""
    if not verificar_sesion(request):
        return redirect('modules_core:login_principal')

    empresa = get_empresa(request)
    centros = CentroCosto.objects.filter(empresa=empresa, is_active=True).order_by('codigo')

    context = {
        'centros': centros,
        'usuario': request.session.get('nombre', ''),
        'empresa': empresa,
    }
    return render(request, 'contabilidad_centros_costo.html', context)


# ============================================================================
# AJAX VIEWS
# ============================================================================

def ajax_buscar_cuentas(request):
    """Búsqueda AJAX de cuentas contables por código o nombre (mismo criterio que formularios con plan de cuentas)."""
    if not verificar_sesion(request):
        return JsonResponse({'error': 'No autenticado'}, status=401)

    empresa = (get_empresa(request) or '').strip()
    if not empresa:
        return JsonResponse({'resultados': [], 'mensaje': 'Sin empresa en sesión'})

    q = (request.GET.get('q') or '').strip()
    base = cuentas_seleccionables_para_movimiento(empresa)
    if q:
        cuentas = base.filter(Q(codigo__icontains=q) | Q(nombre__icontains=q))[:50]
    else:
        cuentas = base[:50]

    resultados = [
        {
            'id': c.id,
            'codigo': c.codigo,
            'nombre': c.nombre,
            'naturaleza': c.naturaleza,
            'texto': f'{c.codigo} - {c.nombre}',
        }
        for c in cuentas
    ]

    return JsonResponse({'resultados': resultados})


def ajax_saldo_cuenta(request):
    """Obtener saldo actual de una cuenta vía AJAX"""
    if not verificar_sesion(request):
        return JsonResponse({'error': 'No autenticado'}, status=401)

    empresa = get_empresa(request)
    cuenta_id = request.GET.get('cuenta_id', '')

    try:
        cuenta = CuentaContable.objects.get(pk=cuenta_id, empresa=empresa)
        ultimo_saldo = LibroMayor.objects.filter(
            cuenta=cuenta, empresa=empresa
        ).order_by('-periodo__ejercicio__anio', '-periodo__numero').first()

        saldo = ultimo_saldo.saldo_final if ultimo_saldo else Decimal('0.00')
        return JsonResponse({
            'cuenta': cuenta.codigo,
            'nombre': cuenta.nombre,
            'saldo': str(saldo),
            'naturaleza': cuenta.naturaleza,
        })
    except CuentaContable.DoesNotExist:
        return JsonResponse({'error': 'Cuenta no encontrada'}, status=404)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal, InvalidOperation

from .models import (
    PropiedadInmueble, Terreno, Construccion, Vehiculo, EstablecimientoComercial
)
from .forms import (
    PropiedadInmuebleForm, TerrenoForm, ConstruccionForm, 
    VehiculoForm, EstablecimientoComercialForm
)
from modules.core.models import Municipio

# Importar modelos desde el módulo tributario
try:
    from tributario.models import Tarifas, TasasDecla
except ImportError:
    # Si falla, intentar desde la ruta completa
    try:
        import sys
        import os
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'venv', 'Scripts')
        if base_path not in sys.path:
            sys.path.insert(0, base_path)
        from tributario.models import Tarifas, TasasDecla
    except ImportError:
        Tarifas = None
        TasasDecla = None

# Importar modelo local de catastro
from .models import TasasMunicipales

# ============================================================================
# VISTAS PRINCIPALES DEL MÓDULO CATASTRO
# ============================================================================

@login_required
def catastro_dashboard(request):
    """
    Dashboard principal del módulo de catastro
    """
    # Obtener estadísticas generales
    total_propiedades = PropiedadInmueble.objects.filter(estado='A').count()
    total_terrenos = Terreno.objects.filter(estado='A').count()
    total_construcciones = Construccion.objects.filter(estado='A').count()
    total_vehiculos = Vehiculo.objects.filter(estado='A').count()
    total_establecimientos = EstablecimientoComercial.objects.filter(estado='A').count()
    
    # Calcular valores totales
    valor_propiedades = PropiedadInmueble.objects.filter(estado='A').aggregate(
        total=Sum('valor_catastral'))['total'] or Decimal('0.00')
    valor_terrenos = Terreno.objects.filter(estado='A').aggregate(
        total=Sum('valor_catastral'))['total'] or Decimal('0.00')
    valor_construcciones = Construccion.objects.filter(estado='A').aggregate(
        total=Sum('valor_catastral'))['total'] or Decimal('0.00')
    valor_vehiculos = Vehiculo.objects.filter(estado='A').aggregate(
        total=Sum('valor_catastral'))['total'] or Decimal('0.00')
    valor_establecimientos = EstablecimientoComercial.objects.filter(estado='A').aggregate(
        total=Sum('valor_catastral'))['total'] or Decimal('0.00')
    
    valor_total = valor_propiedades + valor_terrenos + valor_construcciones + valor_vehiculos + valor_establecimientos
    
    # Obtener municipios únicos
    municipios_unicos = Municipio.objects.filter(
        catastro_propiedadinmueble__estado='A'
    ).distinct().count()
    
    # Obtener registros recientes
    propiedades_recientes = PropiedadInmueble.objects.filter(estado='A').order_by('-fecha_creacion')[:5]
    vehiculos_recientes = Vehiculo.objects.filter(estado='A').order_by('-fecha_creacion')[:5]
    
    context = {
        'titulo': 'Dashboard - Sistema de Gestión Catastral',
        'total_propiedades': total_propiedades,
        'total_terrenos': total_terrenos,
        'total_construcciones': total_construcciones,
        'total_vehiculos': total_vehiculos,
        'total_establecimientos': total_establecimientos,
        'valor_propiedades': valor_propiedades,
        'valor_terrenos': valor_terrenos,
        'valor_construcciones': valor_construcciones,
        'valor_vehiculos': valor_vehiculos,
        'valor_establecimientos': valor_establecimientos,
        'valor_total': valor_total,
        'municipios_unicos': municipios_unicos,
        'propiedades_recientes': propiedades_recientes,
        'vehiculos_recientes': vehiculos_recientes,
    }
    
    return render(request, 'catastro/dashboard.html', context)

# ============================================================================
# GESTIÓN DE PROPIEDADES INMUEBLES
# ============================================================================

@login_required
def propiedades_list(request):
    """
    Lista de propiedades inmuebles
    """
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    
    propiedades = PropiedadInmueble.objects.all()
    
    if search:
        propiedades = propiedades.filter(
            Q(codigo_catastral__icontains=search) |
            Q(propietario__icontains=search) |
            Q(direccion__icontains=search)
        )
    
    if estado:
        propiedades = propiedades.filter(estado=estado)
    
    # Paginación
    paginator = Paginator(propiedades, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'titulo': 'Propiedades Inmuebles - Catastro',
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'total_registros': propiedades.count(),
    }
    
    return render(request, 'catastro/propiedades_list.html', context)

@login_required
def propiedad_create(request):
    """
    Crear nueva propiedad inmueble
    """
    if request.method == 'POST':
        form = PropiedadInmuebleForm(request.POST)
        if form.is_valid():
            propiedad = form.save()
            messages.success(request, f'Propiedad {propiedad.codigo_catastral} creada exitosamente.')
            return redirect('catastro:propiedades_list')
    else:
        form = PropiedadInmuebleForm()
    
    context = {
        'titulo': 'Nueva Propiedad Inmueble - Catastro',
        'form': form,
    }
    
    return render(request, 'catastro/propiedad_form.html', context)

@login_required
def propiedad_update(request, pk):
    """
    Actualizar propiedad inmueble
    """
    propiedad = get_object_or_404(PropiedadInmueble, pk=pk)
    
    if request.method == 'POST':
        form = PropiedadInmuebleForm(request.POST, instance=propiedad)
        if form.is_valid():
            propiedad = form.save()
            messages.success(request, f'Propiedad {propiedad.codigo_catastral} actualizada exitosamente.')
            return redirect('catastro:propiedades_list')
    else:
        form = PropiedadInmuebleForm(instance=propiedad)
    
    context = {
        'titulo': f'Editar Propiedad {propiedad.codigo_catastral} - Catastro',
        'form': form,
        'propiedad': propiedad,
    }
    
    return render(request, 'catastro/propiedad_form.html', context)

@login_required
def propiedad_detail(request, pk):
    """
    Detalle de propiedad inmueble
    """
    propiedad = get_object_or_404(PropiedadInmueble, pk=pk)
    
    context = {
        'titulo': f'Propiedad {propiedad.codigo_catastral} - Catastro',
        'propiedad': propiedad,
    }
    
    return render(request, 'catastro/propiedad_detail.html', context)

@login_required
def propiedad_delete(request, pk):
    """
    Eliminar propiedad inmueble
    """
    propiedad = get_object_or_404(PropiedadInmueble, pk=pk)
    
    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, f'Propiedad {propiedad.codigo_catastral} eliminada exitosamente.')
        return redirect('catastro:propiedades_list')
    
    context = {
        'titulo': f'Eliminar Propiedad {propiedad.codigo_catastral} - Catastro',
        'propiedad': propiedad,
    }
    
    return render(request, 'catastro/propiedad_confirm_delete.html', context)

# ============================================================================
# GESTIÓN DE TERRENOS
# ============================================================================

@login_required
def terrenos_list(request):
    """
    Lista de terrenos
    """
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    
    terrenos = Terreno.objects.all()
    
    if search:
        terrenos = terrenos.filter(
            Q(codigo_terreno__icontains=search) |
            Q(propietario__icontains=search) |
            Q(direccion__icontains=search)
        )
    
    if estado:
        terrenos = terrenos.filter(estado=estado)
    
    paginator = Paginator(terrenos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'titulo': 'Terrenos - Catastro',
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'total_registros': terrenos.count(),
    }
    
    return render(request, 'catastro/terrenos_list.html', context)

@login_required
def terreno_create(request):
    """
    Crear nuevo terreno
    """
    if request.method == 'POST':
        form = TerrenoForm(request.POST)
        if form.is_valid():
            terreno = form.save()
            messages.success(request, f'Terreno {terreno.codigo_terreno} creado exitosamente.')
            return redirect('catastro:terrenos_list')
    else:
        form = TerrenoForm()
    
    context = {
        'titulo': 'Nuevo Terreno - Catastro',
        'form': form,
    }
    
    return render(request, 'catastro/terreno_form.html', context)

@login_required
def terreno_update(request, pk):
    """
    Actualizar terreno
    """
    terreno = get_object_or_404(Terreno, pk=pk)
    
    if request.method == 'POST':
        form = TerrenoForm(request.POST, instance=terreno)
        if form.is_valid():
            terreno = form.save()
            messages.success(request, f'Terreno {terreno.codigo_terreno} actualizado exitosamente.')
            return redirect('catastro:terrenos_list')
    else:
        form = TerrenoForm(instance=terreno)
    
    context = {
        'titulo': f'Editar Terreno {terreno.codigo_terreno} - Catastro',
        'form': form,
        'terreno': terreno,
    }
    
    return render(request, 'catastro/terreno_form.html', context)

@login_required
def terreno_detail(request, pk):
    """
    Detalle de terreno
    """
    terreno = get_object_or_404(Terreno, pk=pk)
    
    context = {
        'titulo': f'Terreno {terreno.codigo_terreno} - Catastro',
        'terreno': terreno,
    }
    
    return render(request, 'catastro/terreno_detail.html', context)

@login_required
def terreno_delete(request, pk):
    """
    Eliminar terreno
    """
    terreno = get_object_or_404(Terreno, pk=pk)
    
    if request.method == 'POST':
        terreno.delete()
        messages.success(request, f'Terreno {terreno.codigo_terreno} eliminado exitosamente.')
        return redirect('catastro:terrenos_list')
    
    context = {
        'titulo': f'Eliminar Terreno {terreno.codigo_terreno} - Catastro',
        'terreno': terreno,
    }
    
    return render(request, 'catastro/terreno_confirm_delete.html', context)

# ============================================================================
# GESTIÓN DE CONSTRUCCIONES
# ============================================================================

@login_required
def construcciones_list(request):
    """
    Lista de construcciones
    """
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    
    construcciones = Construccion.objects.all()
    
    if search:
        construcciones = construcciones.filter(
            Q(codigo_construccion__icontains=search) |
            Q(propietario__icontains=search) |
            Q(direccion__icontains=search)
        )
    
    if estado:
        construcciones = construcciones.filter(estado=estado)
    
    paginator = Paginator(construcciones, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'titulo': 'Construcciones - Catastro',
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'total_registros': construcciones.count(),
    }
    
    return render(request, 'catastro/construcciones_list.html', context)

@login_required
def construccion_create(request):
    """
    Crear nueva construcción
    """
    if request.method == 'POST':
        form = ConstruccionForm(request.POST)
        if form.is_valid():
            construccion = form.save()
            messages.success(request, f'Construcción {construccion.codigo_construccion} creada exitosamente.')
            return redirect('catastro:construcciones_list')
    else:
        form = ConstruccionForm()
    
    context = {
        'titulo': 'Nueva Construcción - Catastro',
        'form': form,
    }
    
    return render(request, 'catastro/construccion_form.html', context)

@login_required
def construccion_update(request, pk):
    """
    Actualizar construcción
    """
    construccion = get_object_or_404(Construccion, pk=pk)
    
    if request.method == 'POST':
        form = ConstruccionForm(request.POST, instance=construccion)
        if form.is_valid():
            construccion = form.save()
            messages.success(request, f'Construcción {construccion.codigo_construccion} actualizada exitosamente.')
            return redirect('catastro:construcciones_list')
    else:
        form = ConstruccionForm(instance=construccion)
    
    context = {
        'titulo': f'Editar Construcción {construccion.codigo_construccion} - Catastro',
        'form': form,
        'construccion': construccion,
    }
    
    return render(request, 'catastro/construccion_form.html', context)

@login_required
def construccion_detail(request, pk):
    """
    Detalle de construcción
    """
    construccion = get_object_or_404(Construccion, pk=pk)
    
    context = {
        'titulo': f'Construcción {construccion.codigo_construccion} - Catastro',
        'construccion': construccion,
    }
    
    return render(request, 'catastro/construccion_detail.html', context)

@login_required
def construccion_delete(request, pk):
    """
    Eliminar construcción
    """
    construccion = get_object_or_404(Construccion, pk=pk)
    
    if request.method == 'POST':
        construccion.delete()
        messages.success(request, f'Construcción {construccion.codigo_construccion} eliminada exitosamente.')
        return redirect('catastro:construcciones_list')
    
    context = {
        'titulo': f'Eliminar Construcción {construccion.codigo_construccion} - Catastro',
        'construccion': construccion,
    }
    
    return render(request, 'catastro/construccion_confirm_delete.html', context)

# ============================================================================
# GESTIÓN DE VEHÍCULOS
# ============================================================================

@login_required
def vehiculos_list(request):
    """
    Lista de vehículos
    """
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    
    vehiculos = Vehiculo.objects.all()
    
    if search:
        vehiculos = vehiculos.filter(
            Q(placa__icontains=search) |
            Q(propietario__icontains=search) |
            Q(marca__icontains=search) |
            Q(modelo__icontains=search)
        )
    
    if estado:
        vehiculos = vehiculos.filter(estado=estado)
    
    paginator = Paginator(vehiculos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'titulo': 'Vehículos - Catastro',
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'total_registros': vehiculos.count(),
    }
    
    return render(request, 'catastro/vehiculos_list.html', context)

@login_required
def vehiculo_create(request):
    """
    Crear nuevo vehículo
    """
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, f'Vehículo {vehiculo.placa} creado exitosamente.')
            return redirect('catastro:vehiculos_list')
    else:
        form = VehiculoForm()
    
    context = {
        'titulo': 'Nuevo Vehículo - Catastro',
        'form': form,
    }
    
    return render(request, 'catastro/vehiculo_form.html', context)

@login_required
def vehiculo_update(request, pk):
    """
    Actualizar vehículo
    """
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, f'Vehículo {vehiculo.placa} actualizado exitosamente.')
            return redirect('catastro:vehiculos_list')
    else:
        form = VehiculoForm(instance=vehiculo)
    
    context = {
        'titulo': f'Editar Vehículo {vehiculo.placa} - Catastro',
        'form': form,
        'vehiculo': vehiculo,
    }
    
    return render(request, 'catastro/vehiculo_form.html', context)

@login_required
def vehiculo_detail(request, pk):
    """
    Detalle de vehículo
    """
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    context = {
        'titulo': f'Vehículo {vehiculo.placa} - Catastro',
        'vehiculo': vehiculo,
    }
    
    return render(request, 'catastro/vehiculo_detail.html', context)

@login_required
def vehiculo_delete(request, pk):
    """
    Eliminar vehículo
    """
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, f'Vehículo {vehiculo.placa} eliminado exitosamente.')
        return redirect('catastro:vehiculos_list')
    
    context = {
        'titulo': f'Eliminar Vehículo {vehiculo.placa} - Catastro',
        'vehiculo': vehiculo,
    }
    
    return render(request, 'catastro/vehiculo_confirm_delete.html', context)

# ============================================================================
# GESTIÓN DE ESTABLECIMIENTOS COMERCIALES
# ============================================================================

@login_required
def establecimientos_list(request):
    """
    Lista de establecimientos comerciales
    """
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    
    establecimientos = EstablecimientoComercial.objects.all()
    
    if search:
        establecimientos = establecimientos.filter(
            Q(codigo_establecimiento__icontains=search) |
            Q(nombre_comercial__icontains=search) |
            Q(propietario__icontains=search) |
            Q(actividad_comercial__icontains=search)
        )
    
    if estado:
        establecimientos = establecimientos.filter(estado=estado)
    
    paginator = Paginator(establecimientos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'titulo': 'Establecimientos Comerciales - Catastro',
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'total_registros': establecimientos.count(),
    }
    
    return render(request, 'catastro/establecimientos_list.html', context)

@login_required
def establecimiento_create(request):
    """
    Crear nuevo establecimiento comercial
    """
    if request.method == 'POST':
        form = EstablecimientoComercialForm(request.POST)
        if form.is_valid():
            establecimiento = form.save()
            messages.success(request, f'Establecimiento {establecimiento.codigo_establecimiento} creado exitosamente.')
            return redirect('catastro:establecimientos_list')
    else:
        form = EstablecimientoComercialForm()
    
    context = {
        'titulo': 'Nuevo Establecimiento Comercial - Catastro',
        'form': form,
    }
    
    return render(request, 'catastro/establecimiento_form.html', context)

@login_required
def establecimiento_update(request, pk):
    """
    Actualizar establecimiento comercial
    """
    establecimiento = get_object_or_404(EstablecimientoComercial, pk=pk)
    
    if request.method == 'POST':
        form = EstablecimientoComercialForm(request.POST, instance=establecimiento)
        if form.is_valid():
            establecimiento = form.save()
            messages.success(request, f'Establecimiento {establecimiento.codigo_establecimiento} actualizado exitosamente.')
            return redirect('catastro:establecimientos_list')
    else:
        form = EstablecimientoComercialForm(instance=establecimiento)
    
    context = {
        'titulo': f'Editar Establecimiento {establecimiento.codigo_establecimiento} - Catastro',
        'form': form,
        'establecimiento': establecimiento,
    }
    
    return render(request, 'catastro/establecimiento_form.html', context)

@login_required
def establecimiento_detail(request, pk):
    """
    Detalle de establecimiento comercial
    """
    establecimiento = get_object_or_404(EstablecimientoComercial, pk=pk)
    
    context = {
        'titulo': f'Establecimiento {establecimiento.codigo_establecimiento} - Catastro',
        'establecimiento': establecimiento,
    }
    
    return render(request, 'catastro/establecimiento_detail.html', context)

@login_required
def establecimiento_delete(request, pk):
    """
    Eliminar establecimiento comercial
    """
    establecimiento = get_object_or_404(EstablecimientoComercial, pk=pk)
    
    if request.method == 'POST':
        establecimiento.delete()
        messages.success(request, f'Establecimiento {establecimiento.codigo_establecimiento} eliminado exitosamente.')
        return redirect('catastro:establecimientos_list')
    
    context = {
        'titulo': f'Eliminar Establecimiento {establecimiento.codigo_establecimiento} - Catastro',
        'establecimiento': establecimiento,
    }
    
    return render(request, 'catastro/establecimiento_confirm_delete.html', context)

# ============================================================================
# REPORTES Y ESTADÍSTICAS
# ============================================================================

@login_required
def reportes_catastro(request):
    """
    Página de reportes del catastro
    """
    # Estadísticas por municipio
    stats_municipio = PropiedadInmueble.objects.filter(estado='A').values(
        'municipio__descripcion'
    ).annotate(
        total=Count('id'),
        valor_total=Sum('valor_catastral')
    ).order_by('-valor_total')
    
    # Estadísticas por tipo de bien
    stats_tipo = {
        'propiedades': PropiedadInmueble.objects.filter(estado='A').count(),
        'terrenos': Terreno.objects.filter(estado='A').count(),
        'construcciones': Construccion.objects.filter(estado='A').count(),
        'vehiculos': Vehiculo.objects.filter(estado='A').count(),
        'establecimientos': EstablecimientoComercial.objects.filter(estado='A').count(),
    }
    
    context = {
        'titulo': 'Reportes - Catastro',
        'stats_municipio': stats_municipio,
        'stats_tipo': stats_tipo,
    }
    
    return render(request, 'catastro/reportes.html', context)

# ============================================================================
# AVALÚO CATASTRAL - RUBROS Y TASAS
# ============================================================================

@login_required
def rubros_tasas(request):
    """
    Vista para mostrar las tasas registradas en un grid
    Subsección Rubros dentro de Avalúo Catastral
    """
    if Tarifas is None:
        messages.error(request, 'El modelo de Tarifas no está disponible.')
        return redirect('catastro:dashboard')
    
    # Obtener el municipio de la sesión
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Obtener todas las tasas registradas
    tasas = Tarifas.objects.filter(empresa=municipio_codigo).order_by('-ano', 'rubro', 'cod_tarifa')
    
    # Búsqueda
    search = request.GET.get('search', '')
    if search:
        tasas = tasas.filter(
            Q(cod_tarifa__icontains=search) |
            Q(descripcion__icontains=search) |
            Q(rubro__icontains=search)
        )
    
    # Filtro por año
    ano_filter = request.GET.get('ano', '')
    if ano_filter:
        tasas = tasas.filter(ano=ano_filter)
    
    # Paginación
    paginator = Paginator(tasas, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener años únicos para el filtro
    anos_disponibles = Tarifas.objects.filter(empresa=municipio_codigo).values_list('ano', flat=True).distinct().order_by('-ano')
    
    context = {
        'titulo': 'Rubros - Avalúo Catastral',
        'page_obj': page_obj,
        'search': search,
        'ano_filter': ano_filter,
        'anos_disponibles': anos_disponibles,
        'total_registros': tasas.count(),
    }
    
    return render(request, 'catastro/rubros_tasas.html', context)

@login_required
def tasas_impuestos(request):
    """
    Vista para mostrar las tasas e impuestos municipales registrados
    Subsección Tasas e Impuestos Municipales dentro de Avalúo Catastral
    """
    if TasasDecla is None:
        messages.error(request, 'El modelo de TasasDecla no está disponible.')
        return redirect('catastro:dashboard')
    
    # Obtener el municipio de la sesión
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Obtener todas las tasas e impuestos registrados
    tasas_impuestos = TasasDecla.objects.filter(empresa=municipio_codigo).order_by('-ano', 'rtm', 'expe', 'rubro')
    
    # Búsqueda
    search = request.GET.get('search', '')
    if search:
        tasas_impuestos = tasas_impuestos.filter(
            Q(rtm__icontains=search) |
            Q(expe__icontains=search) |
            Q(rubro__icontains=search) |
            Q(cod_tarifa__icontains=search) |
            Q(nodecla__icontains=search)
        )
    
    # Filtro por año
    ano_filter = request.GET.get('ano', '')
    if ano_filter:
        tasas_impuestos = tasas_impuestos.filter(ano=ano_filter)
    
    # Filtro por tipo de tasa
    tipo_filter = request.GET.get('tipo', '')
    if tipo_filter:
        tasas_impuestos = tasas_impuestos.filter(tipota=tipo_filter)
    
    # Paginación
    paginator = Paginator(tasas_impuestos, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener años únicos para el filtro
    anos_disponibles = TasasDecla.objects.filter(empresa=municipio_codigo).values_list('ano', flat=True).distinct().order_by('-ano')
    
    context = {
        'titulo': 'Tasas e Impuestos Municipales - Avalúo Catastral',
        'page_obj': page_obj,
        'search': search,
        'ano_filter': ano_filter,
        'tipo_filter': tipo_filter,
        'anos_disponibles': anos_disponibles,
        'total_registros': tasas_impuestos.count(),
    }
    
    return render(request, 'catastro/tasas_impuestos.html', context)

@login_required
def tasas_municipales(request):
    """
    Vista para mostrar las tasas municipales registradas según tabla tasassmunicipales
    Subsección Tasas e Impuestos Municipales dentro de Avalúo Catastral
    """
    # Obtener el municipio de la sesión
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Obtener todas las tasas municipales registradas
    tasas_municipales = TasasMunicipales.objects.filter(empresa=municipio_codigo).order_by('clave', 'rubro')
    
    # Búsqueda
    search = request.GET.get('search', '')
    if search:
        tasas_municipales = tasas_municipales.filter(
            Q(clave__icontains=search) |
            Q(rubro__icontains=search) |
            Q(cod_tarifa__icontains=search) |
            Q(cuenta__icontains=search)
        )
    
    # Filtro por rubro
    rubro_filter = request.GET.get('rubro', '')
    if rubro_filter:
        tasas_municipales = tasas_municipales.filter(rubro=rubro_filter)
    
    # Paginación
    paginator = Paginator(tasas_municipales, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener rubros únicos para el filtro
    rubros_disponibles = TasasMunicipales.objects.filter(empresa=municipio_codigo).values_list('rubro', flat=True).distinct().order_by('rubro')
    
    context = {
        'titulo': 'Tasas e Impuestos Municipales - Avalúo Catastral',
        'page_obj': page_obj,
        'search': search,
        'rubro_filter': rubro_filter,
        'rubros_disponibles': rubros_disponibles,
        'total_registros': tasas_municipales.count(),
    }
    
    return render(request, 'catastro/tasas_municipales.html', context)

# ============================================================================
# APIs PARA AJAX
# ============================================================================

@login_required
def ajax_tasas_municipales(request):
    """
    Vista AJAX para obtener las tasas municipales filtradas por empresa y clave
    """
    try:
        empresa = request.GET.get('empresa', '')
        clave = request.GET.get('clave', '')
        
        if not empresa or not clave:
            return JsonResponse({
                'success': False,
                'message': 'Empresa y clave son requeridos'
            })
        
        # Obtener tasas municipales filtradas
        tasas = TasasMunicipales.objects.filter(
            empresa=empresa,
            clave=clave
        ).order_by('rubro', 'cod_tarifa')
        
        # Convertir a lista de diccionarios
        tasas_list = []
        for tasa in tasas:
            tasas_list.append({
                'id': tasa.id,
                'empresa': tasa.empresa or '',
                'clave': tasa.clave or '',
                'rubro': tasa.rubro or '',
                'cod_tarifa': tasa.cod_tarifa or '',
                'valor': str(tasa.valor),
                'cuenta': tasa.cuenta or '',
                'cuentarez': tasa.cuentarez or '',
            })
        
        return JsonResponse({
            'success': True,
            'tasas': tasas_list,
            'total': len(tasas_list)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener tasas municipales: {str(e)}'
        })

@login_required
@csrf_exempt
def ajax_guardar_tasa_municipal(request):
    """
    Vista AJAX para guardar una nueva tasa municipal
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido'
        })
    
    try:
        empresa = request.POST.get('empresa', '')
        clave = request.POST.get('clave', '').strip()
        rubro = request.POST.get('rubro', '').strip()
        cod_tarifa = request.POST.get('cod_tarifa', '').strip() or None
        valor = request.POST.get('valor', '0.00')
        cuenta = request.POST.get('cuenta', '').strip()
        cuentarez = request.POST.get('cuentarez', '').strip()
        
        # Validaciones
        if not empresa:
            return JsonResponse({
                'success': False,
                'message': 'Empresa es requerida'
            })
        
        if not clave:
            return JsonResponse({
                'success': False,
                'message': 'Clave es requerida'
            })
        
        if not rubro:
            return JsonResponse({
                'success': False,
                'message': 'Rubro es requerido'
            })
        
        try:
            valor_decimal = Decimal(valor)
            if valor_decimal < 0:
                return JsonResponse({
                    'success': False,
                    'message': 'El valor debe ser mayor o igual a cero'
                })
        except (ValueError, InvalidOperation):
            return JsonResponse({
                'success': False,
                'message': 'El valor debe ser un número válido'
            })
        
        # Verificar si ya existe una tasa con la misma empresa, clave y rubro
        tasa_existente = TasasMunicipales.objects.filter(
            empresa=empresa,
            clave=clave,
            rubro=rubro
        ).first()
        
        if tasa_existente:
            return JsonResponse({
                'success': False,
                'message': 'Ya existe una tasa municipal con esta empresa, clave y rubro'
            })
        
        # Crear nueva tasa municipal
        nueva_tasa = TasasMunicipales.objects.create(
            empresa=empresa,
            clave=clave,
            rubro=rubro,
            cod_tarifa=cod_tarifa,
            valor=valor_decimal,
            cuenta=cuenta,
            cuentarez=cuentarez
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Tasa municipal guardada exitosamente',
            'tasa_id': nueva_tasa.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al guardar tasa municipal: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def api_buscar_propiedad(request):
    """
    API para buscar propiedades por código catastral
    """
    try:
        data = json.loads(request.body)
        codigo = data.get('codigo_catastral', '')
        
        if codigo:
            propiedad = PropiedadInmueble.objects.filter(
                codigo_catastral__icontains=codigo,
                estado='A'
            ).first()
            
            if propiedad:
                return JsonResponse({
                    'success': True,
                    'data': {
                        'id': propiedad.id,
                        'codigo_catastral': propiedad.codigo_catastral,
                        'propietario': propiedad.propietario,
                        'direccion': propiedad.direccion,
                        'valor_catastral': str(propiedad.valor_catastral),
                    }
                })
        
        return JsonResponse({
            'success': False,
            'message': 'Propiedad no encontrada'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def api_buscar_vehiculo(request):
    """
    API para buscar vehículos por placa
    """
    try:
        data = json.loads(request.body)
        placa = data.get('placa', '')
        
        if placa:
            vehiculo = Vehiculo.objects.filter(
                placa__icontains=placa,
                estado='A'
            ).first()
            
            if vehiculo:
                return JsonResponse({
                    'success': True,
                    'data': {
                        'id': vehiculo.id,
                        'placa': vehiculo.placa,
                        'propietario': vehiculo.propietario,
                        'marca': vehiculo.marca,
                        'modelo': vehiculo.modelo,
                        'valor_catastral': str(vehiculo.valor_catastral),
                    }
                })
        
        return JsonResponse({
            'success': False,
            'message': 'Vehículo no encontrado'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from .models import PresupuestoIngresos, PresupuestoGastos, EjecucionPresupuestaria, ModificacionPresupuestaria
from .forms import PresupuestoIngresosForm, PresupuestoGastosForm, EjecucionPresupuestariaForm, ModificacionPresupuestariaForm


@login_required
def dashboard_presupuestos(request):
    """
    Vista principal del módulo de presupuestos
    """
    # Obtener datos para el dashboard
    ano_actual = 2024  # TODO: Obtener del sistema de configuración

    # Presupuestos de ingresos
    ingresos = PresupuestoIngresos.objects.filter(ano=ano_actual)
    total_ingresos_presupuestados = ingresos.aggregate(total=Sum('monto_presupuestado'))['total'] or 0
    total_ingresos_ejecutados = ingresos.aggregate(total=Sum('monto_ejecutado'))['total'] or 0

    # Presupuestos de gastos
    gastos = PresupuestoGastos.objects.filter(ano=ano_actual)
    total_gastos_presupuestados = gastos.aggregate(total=Sum('monto_presupuestado'))['total'] or 0
    total_gastos_ejecutados = gastos.aggregate(total=Sum('monto_ejecutado'))['total'] or 0

    context = {
        'total_ingresos_presupuestados': total_ingresos_presupuestados,
        'total_ingresos_ejecutados': total_ingresos_ejecutados,
        'total_gastos_presupuestados': total_gastos_presupuestados,
        'total_gastos_ejecutados': total_gastos_ejecutados,
        'ano_actual': ano_actual,
    }

    return render(request, 'presupuestos/dashboard.html', context)


# Vistas para Presupuesto de Ingresos
@login_required
def lista_ingresos(request):
    ingresos = PresupuestoIngresos.objects.all().order_by('-ano', 'fuente_ingreso')
    return render(request, 'presupuestos/lista_ingresos.html', {'ingresos': ingresos})


@login_required
def crear_ingreso(request):
    if request.method == 'POST':
        form = PresupuestoIngresosForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.usuario_creacion = request.user
            ingreso.save()
            messages.success(request, 'Presupuesto de ingresos creado exitosamente.')
            return redirect('presupuestos:lista_ingresos')
    else:
        form = PresupuestoIngresosForm()
    return render(request, 'presupuestos/form_ingreso.html', {'form': form})


@login_required
def editar_ingreso(request, pk):
    ingreso = get_object_or_404(PresupuestoIngresos, pk=pk)
    if request.method == 'POST':
        form = PresupuestoIngresosForm(request.POST, instance=ingreso)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.usuario_modificacion = request.user
            ingreso.save()
            messages.success(request, 'Presupuesto de ingresos actualizado exitosamente.')
            return redirect('presupuestos:lista_ingresos')
    else:
        form = PresupuestoIngresosForm(instance=ingreso)
    return render(request, 'presupuestos/form_ingreso.html', {'form': form})


# Vistas para Presupuesto de Gastos
@login_required
def lista_gastos(request):
    gastos = PresupuestoGastos.objects.all().order_by('-ano', 'categoria_gasto')
    return render(request, 'presupuestos/lista_gastos.html', {'gastos': gastos})


@login_required
def crear_gasto(request):
    if request.method == 'POST':
        form = PresupuestoGastosForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.usuario_creacion = request.user
            gasto.save()
            messages.success(request, 'Presupuesto de gastos creado exitosamente.')
            return redirect('presupuestos:lista_gastos')
    else:
        form = PresupuestoGastosForm()
    return render(request, 'presupuestos/form_gasto.html', {'form': form})


@login_required
def editar_gasto(request, pk):
    gasto = get_object_or_404(PresupuestoGastos, pk=pk)
    if request.method == 'POST':
        form = PresupuestoGastosForm(request.POST, instance=gasto)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.usuario_modificacion = request.user
            gasto.save()
            messages.success(request, 'Presupuesto de gastos actualizado exitosamente.')
            return redirect('presupuestos:lista_gastos')
    else:
        form = PresupuestoGastosForm(instance=gasto)
    return render(request, 'presupuestos/form_gasto.html', {'form': form})


# Vistas para Ejecución Presupuestaria
@login_required
def lista_ejecucion(request):
    ejecuciones = EjecucionPresupuestaria.objects.all().order_by('-fecha_ejecucion')
    return render(request, 'presupuestos/lista_ejecucion.html', {'ejecuciones': ejecuciones})


@login_required
def crear_ejecucion(request):
    if request.method == 'POST':
        form = EjecucionPresupuestariaForm(request.POST)
        if form.is_valid():
            ejecucion = form.save(commit=False)
            ejecucion.usuario_creacion = request.user
            ejecucion.save()
            messages.success(request, 'Ejecución presupuestaria registrada exitosamente.')
            return redirect('presupuestos:lista_ejecucion')
    else:
        form = EjecucionPresupuestariaForm()
    return render(request, 'presupuestos/form_ejecucion.html', {'form': form})


# Vistas para Modificaciones Presupuestarias
@login_required
def lista_modificaciones(request):
    modificaciones = ModificacionPresupuestaria.objects.all().order_by('-fecha_modificacion')
    return render(request, 'presupuestos/lista_modificaciones.html', {'modificaciones': modificaciones})


@login_required
def crear_modificacion(request):
    if request.method == 'POST':
        form = ModificacionPresupuestariaForm(request.POST)
        if form.is_valid():
            modificacion = form.save(commit=False)
            modificacion.usuario_creacion = request.user
            modificacion.save()
            messages.success(request, 'Modificación presupuestaria registrada exitosamente.')
            return redirect('presupuestos:lista_modificaciones')
    else:
        form = ModificacionPresupuestariaForm()
    return render(request, 'presupuestos/form_modificacion.html', {'form': form})


# API endpoints para AJAX
@login_required
def api_ingresos_por_ano(request, ano):
    ingresos = PresupuestoIngresos.objects.filter(ano=ano)
    data = list(ingresos.values('fuente_ingreso', 'monto_presupuestado', 'monto_ejecutado'))
    return JsonResponse(data, safe=False)


@login_required
def api_gastos_por_ano(request, ano):
    gastos = PresupuestoGastos.objects.filter(ano=ano)
    data = list(gastos.values('categoria_gasto', 'monto_presupuestado', 'monto_ejecutado'))
    return JsonResponse(data, safe=False)
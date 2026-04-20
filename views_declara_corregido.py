# VISTAS DJANGO CORREGIDAS - views.py
# Cambiar todas las referencias de 'cocontrolado' por 'controlado'

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Declara
from .forms import DeclaraForm

def declaracio, Anosn_volumen(request):
    """Vista para declaración de volumen corregida"""
    
    rtm = request.GET.get('rtm')
    expe = request.GET.get('expe')
    
    # Buscar registro existente
    declara = None
    if rtm and expe:
        try:
            declara = Declara.objects.get(rtm=rtm, expe=expe)
        except Declara.DoesNotExist:
            declara = None
    
    if request.method == 'POST':
        form = DeclaraForm(request.POST, instance=declara)
        if form.is_valid():
            # Procesar datos corregidos
            instance = form.save(commit=False)
            
            # Calcular impuesto basado en campos corregidos
            total_ventas = (
                (instance.ventai or 0) +
                (instance.ventac or 0) + 
                (instance.ventas or 0) +
                (instance.controlado or 0)  # CORREGIDO: era cocontrolado
            )
            
            # Calcular impuesto ICS
            instance.impuesto = calcular_impuesto_ics(total_ventas)
            instance.save()
            
            return JsonResponse({
                'success': True,
                'impuesto': float(instance.impuesto),
                'total_ventas': float(total_ventas)
            })
    else:
        form = DeclaraForm(instance=declara)
    
    context = {
        'form': form,
        'rtm': rtm,
        'expe': expe,
        'declara': declara
            'anos_disponibles': anos_disponibles,
    }
    
    return render(request, 'declaracion_volumen.html', context)

def calcular_impuesto_ics(total_ventas):
    """Calcula el impuesto ICS basado en el total de ventas"""
    
    if not total_ventas or total_ventas <= 0:
        return 0
    
    # Tarifas progresivas ICS
    tarifas = [
        (1000000, 0.002),      # 0-1M: 0.2%
        (5000000, 0.004),      # 1M-5M: 0.4%
        (10000000, 0.003),     # 5M-10M: 0.3%
        (20000000, 0.003),     # 10M-20M: 0.3%
        (30000000, 0.002),     # 20M-30M: 0.2%
        (float('inf'), 0.0015) # >30M: 0.15%
    ]
    
    impuesto_total = 0
    base_anterior = 0
    
    for limite, tarifa in tarifas:
        if total_ventas <= base_anterior:
            break
            
        base_gravable = min(total_ventas, limite) - base_anterior
        impuesto_tramo = base_gravable * tarifa
        impuesto_total += impuesto_tramo
        
        base_anterior = limite
        
        if total_ventas <= limite:
            break
    
    return round(impuesto_total, 2)

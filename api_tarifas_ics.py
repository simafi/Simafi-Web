#!/usr/bin/env python
"""
API endpoint para obtener las tarifas ICS desde el formulario JavaScript
"""

import os
import sys
import django
import json
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
try:
    django.setup()
except:
    pass

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def obtener_tarifas_ics(request):
    """
    Endpoint para obtener las tarifas ICS por categoría
    URL: /tributario/api/tarifas-ics/
    """
    try:
        from tributario_app.models import TarifasImptoICS
        
        categoria = request.GET.get('categoria', '1')
        
        # Obtener tarifas ordenadas por rango1
        tarifas = TarifasImptoICS.objects.filter(
            categoria=categoria
        ).order_by('rango1')
        
        # Convertir a lista de diccionarios
        tarifas_data = []
        for tarifa in tarifas:
            tarifas_data.append({
                'id': tarifa.id,
                'categoria': tarifa.categoria,
                'descripcion': tarifa.descripcion or f'Rango {tarifa.rango1} - {tarifa.rango2}',
                'codigo': float(tarifa.codigo) if tarifa.codigo else 0,
                'rango1': float(tarifa.rango1),
                'rango2': float(tarifa.rango2),
                'valor': float(tarifa.valor)
            })
        
        return JsonResponse({
            'success': True,
            'tarifas': tarifas_data,
            'categoria': categoria,
            'total': len(tarifas_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Error al obtener las tarifas ICS'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def calcular_impuesto_ics(request):
    """
    Endpoint para calcular el impuesto ICS
    URL: /tributario/api/calcular-ics/
    """
    try:
        from tributario_app.models import TarifasImptoICS
        
        # Obtener datos del POST
        data = json.loads(request.body)
        ventai = Decimal(str(data.get('ventai', 0)))
        ventac = Decimal(str(data.get('ventac', 0)))
        ventas = Decimal(str(data.get('ventas', 0)))
        categoria = data.get('categoria', '1')
        
        # Función auxiliar para calcular impuesto
        def calcular_por_tipo(valor_ventas):
            if valor_ventas <= 0:
                return {
                    'impuesto_total': 0,
                    'detalle_calculo': [],
                    'valor_ventas': float(valor_ventas)
                }
            
            tarifas = TarifasImptoICS.objects.filter(
                categoria=categoria
            ).order_by('rango1')
            
            impuesto_total = Decimal('0.00')
            valor_restante = valor_ventas
            detalle_calculo = []
            
            for tarifa in tarifas:
                if valor_restante <= 0:
                    break
                
                rango1 = Decimal(str(tarifa.rango1))
                rango2 = Decimal(str(tarifa.rango2))
                valor_tarifa = Decimal(str(tarifa.valor))
                
                diferencial_rango = rango2 - rango1
                
                if diferencial_rango <= 0:
                    continue
                
                if valor_restante <= diferencial_rango:
                    valor_aplicable = valor_restante
                    valor_restante = Decimal('0.00')
                else:
                    valor_aplicable = diferencial_rango
                    valor_restante -= diferencial_rango
                
                impuesto_rango = (valor_aplicable * valor_tarifa / Decimal('1000')).quantize(
                    Decimal('0.01')
                )
                
                impuesto_total += impuesto_rango
                
                detalle_calculo.append({
                    'rango1': float(rango1),
                    'rango2': float(rango2),
                    'diferencial': float(diferencial_rango),
                    'valor_aplicable': float(valor_aplicable),
                    'tarifa_por_mil': float(valor_tarifa),
                    'impuesto_rango': float(impuesto_rango),
                    'descripcion': tarifa.descripcion or f'Rango {rango1} - {rango2}'
                })
            
            return {
                'impuesto_total': float(impuesto_total),
                'detalle_calculo': detalle_calculo,
                'valor_ventas': float(valor_ventas)
            }
        
        # Calcular para cada tipo
        resultado_industria = calcular_por_tipo(ventai)
        resultado_comercio = calcular_por_tipo(ventac)
        resultado_servicios = calcular_por_tipo(ventas)
        
        # Calcular totales
        total_ventas = float(ventai + ventac + ventas)
        total_impuesto = (
            resultado_industria['impuesto_total'] +
            resultado_comercio['impuesto_total'] +
            resultado_servicios['impuesto_total']
        )
        
        return JsonResponse({
            'success': True,
            'resultados': {
                'industria': resultado_industria,
                'comercio': resultado_comercio,
                'servicios': resultado_servicios,
                'totales': {
                    'total_ventas': total_ventas,
                    'total_impuesto': total_impuesto,
                    'ventai': float(ventai),
                    'ventac': float(ventac),
                    'ventas': float(ventas)
                }
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Error al calcular el impuesto ICS'
        }, status=500)

# URLs para agregar al urls.py
"""
Agregar estas URLs al archivo urls.py del módulo tributario:

from . import api_tarifas_ics

urlpatterns = [
    # ... otras URLs ...
    path('api/tarifas-ics/', api_tarifas_ics.obtener_tarifas_ics, name='api_tarifas_ics'),
    path('api/calcular-ics/', api_tarifas_ics.calcular_impuesto_ics, name='api_calcular_ics'),
]
"""

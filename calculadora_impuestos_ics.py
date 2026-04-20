#!/usr/bin/env python
"""
Sistema de cálculo automático de impuestos ICS basado en rangos progresivos
para el formulario de declaración de volumen de ventas.

Campos del formulario:
- ventai (Industria)
- ventac (Comercio) 
- ventas (Servicios)

Tabla: tarifasimptoics
- categoria: CHAR(1) - Filtro por categoría "1"
- rango1: DECIMAL(12,2) - Rango inferior
- rango2: DECIMAL(12,2) - Rango superior
- valor: DECIMAL(12,2) - Tarifa por mil
"""

import os
import sys
import django
from decimal import Decimal, ROUND_HALF_UP

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
try:
    django.setup()
except:
    pass

def calcular_impuesto_ics(valor_ventas, categoria="1"):
    """
    Calcula el impuesto ICS basado en rangos progresivos
    
    Args:
        valor_ventas (Decimal): Valor de ventas declarado
        categoria (str): Categoría de tarifa (por defecto "1")
    
    Returns:
        dict: {
            'impuesto_total': Decimal,
            'detalle_calculo': list,
            'valor_ventas': Decimal
        }
    """
    try:
        from tributario_app.models import TarifasImptoICS
    except ImportError:
        # Simulación para pruebas sin Django
        return simular_calculo_impuesto(valor_ventas)
    
    # Convertir a Decimal para precisión
    valor_ventas = Decimal(str(valor_ventas))
    
    # Obtener tarifas ordenadas por rango1
    tarifas = TarifasImptoICS.objects.filter(
        categoria=categoria
    ).order_by('rango1')
    
    if not tarifas.exists():
        return {
            'impuesto_total': Decimal('0.00'),
            'detalle_calculo': [],
            'valor_ventas': valor_ventas,
            'error': 'No se encontraron tarifas para la categoría especificada'
        }
    
    impuesto_total = Decimal('0.00')
    valor_restante = valor_ventas
    detalle_calculo = []
    
    for tarifa in tarifas:
        if valor_restante <= 0:
            break
            
        rango1 = Decimal(str(tarifa.rango1))
        rango2 = Decimal(str(tarifa.rango2))
        valor_tarifa = Decimal(str(tarifa.valor))
        
        # Calcular diferencial del rango
        diferencial_rango = rango2 - rango1
        
        if diferencial_rango <= 0:
            continue
            
        # Determinar valor a aplicar en este rango
        if valor_restante <= diferencial_rango:
            # El valor restante cabe completamente en este rango
            valor_aplicable = valor_restante
            valor_restante = Decimal('0.00')
        else:
            # El valor excede este rango, aplicar solo el diferencial
            valor_aplicable = diferencial_rango
            valor_restante -= diferencial_rango
        
        # Calcular impuesto para este rango: (valor * tarifa) / 1000
        impuesto_rango = (valor_aplicable * valor_tarifa / Decimal('1000')).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        impuesto_total += impuesto_rango
        
        # Agregar detalle del cálculo
        detalle_calculo.append({
            'rango1': float(rango1),
            'rango2': float(rango2),
            'diferencial': float(diferencial_rango),
            'valor_aplicable': float(valor_aplicable),
            'tarifa_por_mil': float(valor_tarifa),
            'impuesto_rango': float(impuesto_rango),
            'descripcion': getattr(tarifa, 'descripcion', f'Rango {rango1} - {rango2}')
        })
    
    return {
        'impuesto_total': impuesto_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'detalle_calculo': detalle_calculo,
        'valor_ventas': valor_ventas,
        'valor_restante': valor_restante
    }

def simular_calculo_impuesto(valor_ventas):
    """
    Simulación del cálculo para pruebas sin acceso a la base de datos
    """
    # Tarifas de ejemplo basadas en la estructura real
    tarifas_ejemplo = [
        {'rango1': 0, 'rango2': 1000000, 'valor': 2.5, 'descripcion': 'Primer rango'},
        {'rango1': 1000000, 'rango2': 5000000, 'valor': 4.0, 'descripcion': 'Segundo rango'},
        {'rango1': 5000000, 'rango2': 10000000, 'valor': 6.0, 'descripcion': 'Tercer rango'},
        {'rango1': 10000000, 'rango2': 999999999, 'valor': 8.0, 'descripcion': 'Cuarto rango'},
    ]
    
    valor_ventas = Decimal(str(valor_ventas))
    impuesto_total = Decimal('0.00')
    valor_restante = valor_ventas
    detalle_calculo = []
    
    for tarifa in tarifas_ejemplo:
        if valor_restante <= 0:
            break
            
        rango1 = Decimal(str(tarifa['rango1']))
        rango2 = Decimal(str(tarifa['rango2']))
        valor_tarifa = Decimal(str(tarifa['valor']))
        
        diferencial_rango = rango2 - rango1
        
        if valor_restante <= diferencial_rango:
            valor_aplicable = valor_restante
            valor_restante = Decimal('0.00')
        else:
            valor_aplicable = diferencial_rango
            valor_restante -= diferencial_rango
        
        impuesto_rango = (valor_aplicable * valor_tarifa / Decimal('1000')).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        impuesto_total += impuesto_rango
        
        detalle_calculo.append({
            'rango1': float(rango1),
            'rango2': float(rango2),
            'diferencial': float(diferencial_rango),
            'valor_aplicable': float(valor_aplicable),
            'tarifa_por_mil': float(valor_tarifa),
            'impuesto_rango': float(impuesto_rango),
            'descripcion': tarifa['descripcion']
        })
    
    return {
        'impuesto_total': impuesto_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'detalle_calculo': detalle_calculo,
        'valor_ventas': valor_ventas
    }

def calcular_impuestos_formulario(ventai=0, ventac=0, ventas=0):
    """
    Calcula impuestos para los tres campos del formulario
    
    Args:
        ventai (float): Ventas Industria
        ventac (float): Ventas Comercio
        ventas (float): Ventas Servicios
    
    Returns:
        dict: Resultados de cálculo para cada campo
    """
    resultados = {}
    
    # Calcular impuesto para Industria
    if ventai > 0:
        resultados['industria'] = calcular_impuesto_ics(ventai, "1")
    else:
        resultados['industria'] = {'impuesto_total': Decimal('0.00'), 'detalle_calculo': []}
    
    # Calcular impuesto para Comercio
    if ventac > 0:
        resultados['comercio'] = calcular_impuesto_ics(ventac, "1")
    else:
        resultados['comercio'] = {'impuesto_total': Decimal('0.00'), 'detalle_calculo': []}
    
    # Calcular impuesto para Servicios
    if ventas > 0:
        resultados['servicios'] = calcular_impuesto_ics(ventas, "1")
    else:
        resultados['servicios'] = {'impuesto_total': Decimal('0.00'), 'detalle_calculo': []}
    
    # Calcular totales
    total_impuesto = (
        resultados['industria']['impuesto_total'] +
        resultados['comercio']['impuesto_total'] +
        resultados['servicios']['impuesto_total']
    )
    
    total_ventas = Decimal(str(ventai)) + Decimal(str(ventac)) + Decimal(str(ventas))
    
    resultados['totales'] = {
        'total_ventas': float(total_ventas),
        'total_impuesto': float(total_impuesto),
        'ventai': float(ventai),
        'ventac': float(ventac),
        'ventas': float(ventas)
    }
    
    return resultados

def test_calculadora():
    """
    Función de prueba para verificar el funcionamiento
    """
    print("🧮 PRUEBA DE CALCULADORA DE IMPUESTOS ICS")
    print("=" * 60)
    
    # Casos de prueba
    casos_prueba = [
        {'ventai': 500000, 'ventac': 0, 'ventas': 0, 'descripcion': 'Solo Industria - Primer rango'},
        {'ventai': 0, 'ventac': 2000000, 'ventas': 0, 'descripcion': 'Solo Comercio - Segundo rango'},
        {'ventai': 0, 'ventac': 0, 'ventas': 8000000, 'descripcion': 'Solo Servicios - Tercer rango'},
        {'ventai': 1500000, 'ventac': 3000000, 'ventas': 2000000, 'descripcion': 'Combinado - Múltiples rangos'},
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n📊 CASO {i}: {caso['descripcion']}")
        print("-" * 50)
        
        resultado = calcular_impuestos_formulario(
            ventai=caso['ventai'],
            ventac=caso['ventac'],
            ventas=caso['ventas']
        )
        
        print(f"Industria: ${caso['ventai']:,.2f} → Impuesto: ${resultado['industria']['impuesto_total']:,.2f}")
        print(f"Comercio:  ${caso['ventac']:,.2f} → Impuesto: ${resultado['comercio']['impuesto_total']:,.2f}")
        print(f"Servicios: ${caso['ventas']:,.2f} → Impuesto: ${resultado['servicios']['impuesto_total']:,.2f}")
        print(f"TOTAL:     ${resultado['totales']['total_ventas']:,.2f} → Impuesto: ${resultado['totales']['total_impuesto']:,.2f}")

if __name__ == "__main__":
    test_calculadora()

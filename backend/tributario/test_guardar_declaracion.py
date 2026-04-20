#!/usr/bin/env python
"""
Script para probar la funcionalidad completa del botón Guardar Declaración
"""

import os
import sys
import django
import json

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from tributario_app.forms import DeclaracionVolumenForm
from tributario.models import DeclaracionVolumen

def test_guardar_declaracion():
    print("="*80)
    print("PROBANDO FUNCIONALIDAD GUARDAR DECLARACION")
    print("="*80)
    
    # Datos de ejemplo que simulan lo que envía el JavaScript
    datos_ejemplo = {
        'idneg': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'ano': 2024,
        'mes': 12,
        'tipo': 1,
        'ventai': 5000000,
        'ventac': 5000000,
        'ventas': 5000000,
        'valorexcento': 0,
        'controlado': 31000000,
        'unidad': 1,  # Cambiar a entero
        'factor': 1.0,
        'multadecla': 0,
        'impuesto': 0,
        'ajuste': 0
    }
    
    print("\n1. Creando formulario con datos de ejemplo...")
    form = DeclaracionVolumenForm(datos_ejemplo)
    
    print(f"   - Datos de entrada: {datos_ejemplo}")
    print(f"   - Formulario válido: {form.is_valid()}")
    
    if not form.is_valid():
        print("   - Errores del formulario:")
        for campo, errores in form.errors.items():
            print(f"     * {campo}: {errores}")
        return False
    
    print("\n2. Procesando formulario...")
    cleaned_data = form.cleaned_data
    
    # Calcular valor_base
    ventai = cleaned_data.get('ventai', 0) or 0
    ventac = cleaned_data.get('ventac', 0) or 0
    ventas = cleaned_data.get('ventas', 0) or 0
    valorexcento = cleaned_data.get('valorexcento', 0) or 0
    controlado = cleaned_data.get('controlado', 0) or 0
    
    total_ventas = ventai + ventac + ventas + valorexcento + controlado
    print(f"   - Ventas individuales: {ventai:,} + {ventac:,} + {ventas:,} + {valorexcento:,} + {controlado:,}")
    print(f"   - Total ventas (valor_base): {total_ventas:,}")
    
    # Simular guardado
    print("\n3. Simulando guardado...")
    try:
        # Crear nueva instancia
        declaracion = DeclaracionVolumen(
            idneg=cleaned_data['idneg'],
            rtm=cleaned_data['rtm'],
            expe=cleaned_data['expe'],
            ano=cleaned_data['ano'],
            mes=cleaned_data['mes'],
            tipo=cleaned_data['tipo'],
            ventai=cleaned_data['ventai'],
            ventac=cleaned_data['ventac'],
            ventas=cleaned_data['ventas'],
            valorexcento=cleaned_data['valorexcento'],
            controlado=cleaned_data['controlado'],
            unidad=cleaned_data['unidad'],
            factor=cleaned_data['factor'],
            multadecla=cleaned_data['multadecla'],
            impuesto=cleaned_data['impuesto'],
            ajuste=cleaned_data['ajuste']
        )
        
        # Calcular impuesto (simulación)
        from decimal import Decimal
        impuesto = total_ventas * Decimal('0.001')  # 0.1% como ejemplo
        declaracion.impuesto = impuesto
        
        print(f"   - Declaración creada exitosamente")
        print(f"   - Impuesto calculado: {impuesto:,.2f}")
        print(f"   - Valor base (propiedad): {declaracion.valor_base:,.2f}")
        
        # Simular respuesta JSON
        respuesta_json = {
            'exito': True,
            'mensaje': 'Declaración guardada exitosamente',
            'impuesto': float(impuesto)
        }
        
        print(f"\n4. Respuesta JSON simulada:")
        print(f"   {json.dumps(respuesta_json, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error al guardar: {e}")
        return False

if __name__ == "__main__":
    test_guardar_declaracion()

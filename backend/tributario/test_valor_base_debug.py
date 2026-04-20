#!/usr/bin/env python
"""
Script para debuggear el cálculo del Valor Base
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from tributario_app.forms import DeclaracionVolumenForm
from tributario.models import DeclaracionVolumen

def test_valor_base_debug():
    print("="*80)
    print("DEBUG VALOR BASE - VERIFICANDO CÁLCULO")
    print("="*80)
    
    # Crear datos de prueba
    datos_prueba = {
        'idneg': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'ano': 2025,
        'mes': 10,
        'tipo': 1,
        'ventai': 5000000,
        'ventac': 5000000,
        'ventas': 5000000,
        'valorexcento': 0,
        'controlado': 31000000,
        'unidad': 1,
        'factor': 1.0,
        'multadecla': 0,
        'impuesto': 0,
        'ajuste': 0
    }
    
    print("1. Datos de entrada:")
    for campo, valor in datos_prueba.items():
        print(f"   - {campo}: {valor}")
    
    # Calcular suma manual
    suma_manual = datos_prueba['ventai'] + datos_prueba['ventac'] + datos_prueba['ventas'] + datos_prueba['valorexcento'] + datos_prueba['controlado']
    print(f"\n2. Suma manual: {suma_manual:,}")
    
    # Crear formulario
    print("\n3. Creando formulario...")
    form = DeclaracionVolumenForm(datos_prueba)
    
    print(f"   - Formulario válido: {form.is_valid()}")
    if not form.is_valid():
        print(f"   - Errores: {form.errors}")
    
    # Verificar initial data
    print(f"\n4. Initial data:")
    if hasattr(form, 'initial') and form.initial:
        print(f"   - valor_base en initial: {form.initial.get('valor_base', 'NO ENCONTRADO')}")
    
    # Verificar cleaned_data
    if form.is_valid():
        print(f"\n5. Cleaned data:")
        print(f"   - valor_base en cleaned_data: {form.cleaned_data.get('valor_base', 'NO ENCONTRADO')}")
        
        # Verificar campos individuales
        print(f"\n6. Campos individuales en cleaned_data:")
        campos_ventas = ['ventai', 'ventac', 'ventas', 'valorexcento', 'controlado']
        suma_cleaned = 0
        for campo in campos_ventas:
            valor = form.cleaned_data.get(campo, 0)
            suma_cleaned += float(valor) if valor else 0
            print(f"   - {campo}: {valor}")
        print(f"   - Suma de cleaned_data: {suma_cleaned:,}")
    
    # Verificar si hay una instancia del modelo
    print(f"\n7. Verificando instancia del modelo:")
    if hasattr(form, 'instance') and form.instance:
        print(f"   - Instancia existe: {form.instance}")
        print(f"   - valor_base de la instancia: {form.instance.valor_base}")
    else:
        print("   - No hay instancia del modelo")
    
    # Renderizar el campo para ver el HTML generado
    print(f"\n8. HTML del campo valor_base:")
    try:
        html_campo = str(form['valor_base'])
        print(f"   - HTML: {html_campo}")
        
        # Extraer el ID del campo
        import re
        id_match = re.search(r'id="([^"]+)"', html_campo)
        if id_match:
            campo_id = id_match.group(1)
            print(f"   - ID del campo: {campo_id}")
        else:
            print("   - No se pudo extraer el ID del campo")
            
    except Exception as e:
        print(f"   - Error al renderizar campo: {e}")
    
    print(f"\n{'='*80}")
    print("RESUMEN:")
    print(f"- Suma manual esperada: {suma_manual:,}")
    print(f"- Formulario válido: {form.is_valid()}")
    if form.is_valid():
        print(f"- valor_base en cleaned_data: {form.cleaned_data.get('valor_base', 'NO ENCONTRADO')}")
    print(f"{'='*80}")

if __name__ == "__main__":
    test_valor_base_debug()































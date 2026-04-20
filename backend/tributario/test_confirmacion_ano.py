#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST CONFIRMACIÓN AÑO: Verificar que al confirmar se cargan los datos
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from django.test import RequestFactory
from modules.tributario.views import declaracion_volumen
import re

def test_confirmacion_ano():
    """Test para verificar la confirmación y carga de datos"""
    print("="*80)
    print("TEST CONFIRMACIÓN AÑO")
    print("="*80)
    
    factory = RequestFactory()
    
    # Test 1: Cargar declaración existente (2024)
    print("\n1. CARGAR DECLARACIÓN EXISTENTE (AÑO 2024)")
    request = factory.get('/declaracion-volumen/', {
        'empresa': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'ano_cargar': '2024'
    })
    request.session = {'empresa': '0301'}
    
    response = declaracion_volumen(request)
    html = response.content.decode('utf-8')
    
    # Verificar año seleccionado
    select_pattern = r'<select[^>]*id="id_ano"[^>]*>.*?</select>'
    select_match = re.search(select_pattern, html, re.DOTALL)
    
    if select_match:
        ano_html = select_match.group(0)
        selected_pattern = r'<option[^>]*value="([^"]*)"[^>]*selected[^>]*>'
        selected_matches = re.findall(selected_pattern, ano_html)
        
        if '2024' in selected_matches:
            print("   CORRECTO: Año 2024 seleccionado")
            
            # Verificar que hay datos cargados
            ventai_pattern = r'value="([^"]*)"[^>]*id="id_ventai"'
            ventai_match = re.search(ventai_pattern, html)
            
            if ventai_match:
                ventai_value = ventai_match.group(1)
                print(f"   Ventas Industria cargadas: {ventai_value}")
                
                if ventai_value and ventai_value not in ['0', '0.00', '']:
                    print("   CORRECTO: Datos de declaración 2024 cargados")
                else:
                    print("   INFO: No hay datos de ventas")
        else:
            print(f"   ERROR: Año 2024 no seleccionado. Seleccionados: {selected_matches}")
    else:
        print("   ERROR: No se encontró el campo año")
    
    # Test 2: Cargar año sin declaración (2023)
    print("\n2. CARGAR AÑO SIN DECLARACIÓN (2023)")
    request2 = factory.get('/declaracion-volumen/', {
        'empresa': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'ano_cargar': '2023'
    })
    request2.session = {'empresa': '0301'}
    
    response2 = declaracion_volumen(request2)
    html2 = response2.content.decode('utf-8')
    
    select_match2 = re.search(select_pattern, html2, re.DOTALL)
    
    if select_match2:
        ano_html2 = select_match2.group(0)
        selected_matches2 = re.findall(selected_pattern, ano_html2)
        
        if '2023' in selected_matches2:
            print("   CORRECTO: Año 2023 seleccionado")
            print("   INFO: Formulario nuevo (sin declaración para 2023)")
        else:
            print(f"   ERROR: Año 2023 no seleccionado")
    
    print("\n" + "="*80)
    print("RESUMEN DE FUNCIONALIDAD:")
    print("="*80)
    print("\n1. Usuario selecciona un año diferente en el combo")
    print("2. Aparece mensaje de confirmación:")
    print("   '¿Desea cargar los datos del año XXXX?'")
    print("\n3. SI el usuario confirma (presiona OK):")
    print("   - La página se recarga con parámetro ano_cargar=XXXX")
    print("   - Si existe declaración: Se cargan los datos")
    print("   - Si NO existe: Formulario nuevo")
    print("   - El año queda seleccionado en el combo")
    print("\n4. SI el usuario cancela:")
    print("   - El combo vuelve al año anterior")
    print("   - No se recarga la página")
    print("="*80)

if __name__ == '__main__':
    test_confirmacion_ano()


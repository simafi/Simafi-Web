#!/usr/bin/env python
"""
Script para probar la detección de AJAX en el backend
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from tributario.views import declaracion_volumen

def test_ajax_detection():
    print("="*80)
    print("PROBANDO DETECCION DE AJAX EN BACKEND")
    print("="*80)
    
    # Crear factory para requests
    factory = RequestFactory()
    
    # Datos de prueba
    datos = {
        'accion': 'guardar',
        'form_data': {
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
            'unidad': 1,
            'factor': 1.0,
            'multadecla': 0,
            'impuesto': 0,
            'ajuste': 0
        }
    }
    
    # Crear request AJAX
    print("1. Creando request AJAX...")
    request = factory.post(
        '/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151',
        data=datos,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    
    # Simular usuario anónimo
    request.user = AnonymousUser()
    
    print(f"   - Method: {request.method}")
    print(f"   - Content-Type: {request.content_type}")
    print(f"   - X-Requested-With: {request.META.get('HTTP_X_REQUESTED_WITH')}")
    print(f"   - Headers: {dict(request.META)}")
    
    # Probar detección de AJAX
    print("\n2. Probando detección de AJAX...")
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    content_type = request.META.get('CONTENT_TYPE', '')
    
    print(f"   - is_ajax: {is_ajax}")
    print(f"   - content_type: {content_type}")
    
    if is_ajax:
        print("   - ✅ Petición detectada como AJAX")
    else:
        print("   - ❌ Petición NO detectada como AJAX")
    
    # Probar con diferentes variaciones del header
    print("\n3. Probando variaciones del header...")
    variations = [
        'XMLHttpRequest',
        'xmlhttprequest',
        'XmlHttpRequest',
        'XMLHttpRequest ',
        ' XMLHttpRequest'
    ]
    
    for variation in variations:
        request.META['HTTP_X_REQUESTED_WITH'] = variation
        is_ajax_var = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        print(f"   - '{variation}': {is_ajax_var}")
    
    print("\n" + "="*80)
    print("PRUEBA COMPLETADA")
    print("="*80)

if __name__ == "__main__":
    test_ajax_detection()































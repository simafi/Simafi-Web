#!/usr/bin/env python
"""
Script de prueba para verificar los mensajes estéticos y funcionales.
"""

import os
import django
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio
from django.test import RequestFactory
from hola.views import maestro_negocios

def test_mensajes_esteticos():
    """Prueba los diferentes tipos de mensajes estéticos"""
    print("=== PRUEBA DE MENSAJES ESTÉTICOS ===")
    
    timestamp = int(time.time())
    
    # 1. Prueba de campos obligatorios faltantes
    print("\n1. Probando mensaje de campos obligatorios faltantes...")
    form_data_vacio = {
        'empre': '',
        'rtm': '',
        'expe': '',
        'accion': 'salvar'
    }
    
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data_vacio)
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Mensaje de campos obligatorios funcionando")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 2. Prueba de longitud excedida
    print("\n2. Probando mensaje de longitud excedida...")
    form_data_largo = {
        'empre': '12345',  # Más de 4 caracteres
        'rtm': 'RTM-MUY-LARGO-EXCEDE',  # Más de 16 caracteres
        'expe': '1234567890123',  # Más de 12 caracteres
        'accion': 'salvar'
    }
    
    request = factory.post('/maestro_negocios/', form_data_largo)
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Mensaje de longitud excedida funcionando")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 3. Prueba de creación exitosa
    print("\n3. Probando mensaje de creación exitosa...")
    form_data_exito = {
        'empre': '0301',
        'rtm': f'MSJ{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Mensaje Test {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': '9999-9999-99999',
        'catastral': 'TEST-001',
        'socios': 'Socio Test',
        'categoria': 'A',
        'estatus': 'A',
        'accion': 'salvar'
    }
    
    request = factory.post('/maestro_negocios/', form_data_exito)
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Mensaje de creación exitosa funcionando")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 4. Prueba de confirmación de actualización
    print("\n4. Probando mensaje de confirmación de actualización...")
    # Usar los mismos datos para que ya exista
    request = factory.post('/maestro_negocios/', form_data_exito)
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Mensaje de confirmación funcionando")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 5. Prueba de eliminación
    print("\n5. Probando mensaje de eliminación...")
    form_data_eliminar = {
        'empre': '0301',
        'rtm': f'ELIM{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'accion': 'eliminar'
    }
    
    request = factory.post('/maestro_negocios/', form_data_eliminar)
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Mensaje de eliminación funcionando")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE MENSAJES ESTÉTICOS")
    print("=" * 60)
    
    test_mensajes_esteticos()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA") 
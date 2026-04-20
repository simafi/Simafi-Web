#!/usr/bin/env python
"""
Script de diagnóstico para identificar el problema del botón salvar.
"""

import os
import sys
import django
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from django.test import RequestFactory
from hola.views import maestro_negocios

def test_diagnostico():
    """Diagnóstico del problema"""
    print("=== DIAGNÓSTICO DEL PROBLEMA ===")
    
    timestamp = int(time.time())
    
    # Datos únicos para evitar conflictos
    form_data = {
        'empre': '0301',
        'rtm': f'DIAG-{timestamp}',
        'expe': f'{timestamp}',
        'nombrenego': f'Diagnóstico {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': f'9999-{timestamp}-99999',
        'direccion': f'Dirección {timestamp}',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    request.headers = {'X-Requested-With': 'XMLHttpRequest'}
    
    print(f"\nSimulando petición AJAX...")
    print(f"Headers enviados: {dict(request.headers)}")
    
    try:
        response = maestro_negocios(request)
        
        print(f"\n=== RESULTADO ===")
        print(f"Status de respuesta: {response.status_code}")
        print(f"Content-Type: {response.get('Content-Type', 'No especificado')}")
        print(f"Longitud de respuesta: {len(response.content)} bytes")
        
        # Mostrar los primeros 500 caracteres de la respuesta
        content = response.content.decode('utf-8', errors='ignore')
        print(f"\nPrimeros 500 caracteres de la respuesta:")
        print("=" * 50)
        print(content[:500])
        print("=" * 50)
        
        if response.status_code == 200:
            try:
                import json
                data = json.loads(content)
                print(f"\n✅ Respuesta JSON válida:")
                print(json.dumps(data, indent=2))
                return True
            except json.JSONDecodeError as e:
                print(f"\n❌ Error al parsear JSON: {e}")
                print(f"La respuesta no es JSON válido")
                return False
        else:
            print(f"\n❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        print("=== INICIANDO DIAGNÓSTICO ===")
        
        result = test_diagnostico()
        
        if result:
            print("\n✅ Diagnóstico exitoso - El problema está resuelto")
        else:
            print("\n❌ Diagnóstico fallido - El problema persiste")
        
    except Exception as e:
        print(f"\n❌ Error durante el diagnóstico: {str(e)}")
        import traceback
        traceback.print_exc() 
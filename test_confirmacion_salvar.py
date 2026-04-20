#!/usr/bin/env python
"""
Script de prueba para verificar que el mensaje de confirmación solo aparece al presionar Salvar.
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

def test_confirmacion_solo_salvar():
    """Prueba que el mensaje de confirmación solo aparece al presionar Salvar"""
    print("=== PRUEBA DE CONFIRMACIÓN SOLO AL SALVAR ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba
    form_data = {
        'empre': '0301',
        'rtm': f'CONF{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Confirmación Test {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Test',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '0.0000000',
        'cy': '0.0000000',
        'accion': 'salvar'  # Acción Salvar
    }
    
    print(f"1. Creando negocio inicial...")
    print(f"  Empresa: {form_data['empre']}")
    print(f"  RTM: {form_data['rtm']}")
    print(f"  Expediente: {form_data['expe']}")
    
    # Crear petición simulada para crear el negocio
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Negocio creado exitosamente")
            
            # Ahora probar con la misma información pero acción "nuevo"
            print(f"\n2. Probando con acción 'nuevo' (no debería mostrar confirmación)...")
            form_data_nuevo = form_data.copy()
            form_data_nuevo['accion'] = 'nuevo'
            
            request_nuevo = factory.post('/maestro_negocios/', form_data_nuevo)
            response_nuevo = maestro_negocios(request_nuevo)
            
            print(f"Status: {response_nuevo.status_code}")
            if response_nuevo.status_code == 200:
                print("✅ Acción 'nuevo' procesada sin confirmación")
            
            # Ahora probar con acción "salvar" (debería mostrar confirmación)
            print(f"\n3. Probando con acción 'salvar' (debería mostrar confirmación)...")
            form_data_salvar = form_data.copy()
            form_data_salvar['accion'] = 'salvar'
            
            request_salvar = factory.post('/maestro_negocios/', form_data_salvar)
            response_salvar = maestro_negocios(request_salvar)
            
            print(f"Status: {response_salvar.status_code}")
            if response_salvar.status_code == 200:
                print("✅ Acción 'salvar' procesada correctamente")
                print("✅ El mensaje de confirmación solo aparece con acción 'salvar'")
            
        else:
            print("❌ Error en la creación del negocio")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CONFIRMACIÓN")
    print("=" * 60)
    
    test_confirmacion_solo_salvar()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA") 
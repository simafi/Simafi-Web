#!/usr/bin/env python
"""
Script de prueba simple para verificar coordenadas sin validaciones complejas.
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

def test_coordenadas_simple():
    """Prueba simple de coordenadas sin validaciones complejas"""
    print("=== PRUEBA SIMPLE DE COORDENADAS ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba simples
    form_data = {
        'empre': '0301',
        'rtm': f'SIMPLE{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Simple Test {timestamp}',
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
        'cx': '0,0',  # Coordenada simple
        'cy': '0,0',  # Coordenada simple
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario:")
    print(f"  CX: {form_data['cx']}")
    print(f"  CY: {form_data['cy']}")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    
    print(f"\nEnviando petición POST...")
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Petición procesada correctamente")
            
            # Verificar que se guardó en la base de datos
            negocio_guardado = Negocio.objects.filter(
                empre=form_data['empre'],
                rtm=form_data['rtm'],
                expe=form_data['expe']
            ).first()
            
            if negocio_guardado:
                print(f"✅ Negocio encontrado en BD:")
                print(f"  ID: {negocio_guardado.id}")
                print(f"  CX: {negocio_guardado.cx}")
                print(f"  CY: {negocio_guardado.cy}")
                print("✅ Sistema funcionando correctamente")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la petición")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA SIMPLE")
    print("=" * 60)
    
    test_coordenadas_simple()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA") 
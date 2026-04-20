#!/usr/bin/env python
"""
Script de prueba para verificar que el formulario funciona sin coordenadas.
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

def test_sin_coordenadas():
    """Prueba que el formulario funciona sin coordenadas"""
    print("=== PRUEBA SIN COORDENADAS ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba sin coordenadas
    form_data = {
        'empre': '0301',
        'rtm': f'SINCOORD{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Sin Coordenadas {timestamp}',
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
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario:")
    print(f"  Empresa: {form_data['empre']}")
    print(f"  RTM: {form_data['rtm']}")
    print(f"  Expediente: {form_data['expe']}")
    print(f"  Nombre: {form_data['nombrenego']}")
    print(f"  Sin coordenadas CX/CY")
    
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
                print(f"  Nombre: {negocio_guardado.nombrenego}")
                print(f"  CX: {negocio_guardado.cx}")
                print(f"  CY: {negocio_guardado.cy}")
                print("✅ Sistema funcionando correctamente sin coordenadas")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la petición")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA SIN COORDENADAS")
    print("=" * 60)
    
    test_sin_coordenadas()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA") 
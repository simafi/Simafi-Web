#!/usr/bin/env python
"""
Script de prueba final para verificar que el botón salvar funcione correctamente.
"""

import os
import sys
import django
import time
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio
from django.test import RequestFactory
from hola.views import maestro_negocios

def test_salvar_final():
    """Prueba final del botón salvar"""
    print("=== PRUEBA FINAL DEL BOTÓN SALVAR ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba con longitudes válidas
    form_data = {
        'empre': '0301',
        'rtm': f'SALVAR{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Test {timestamp}',
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
    
    print(f"\nEnviando petición POST...")
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.get('Content-Type', 'No especificado')}")
        
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
                print(f"  Identidad: {negocio_guardado.identidad}")
                print(f"  Catastral: {negocio_guardado.catastral}")
                print(f"  Estatus: {negocio_guardado.estatus}")
                print(f"  Categoría: {negocio_guardado.categoria}")
                print(f"  Socios: {negocio_guardado.socios}")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la petición")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA FINAL DEL BOTÓN SALVAR")
    print("=" * 60)
    
    # Ejecutar prueba
    test_salvar_final()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA") 
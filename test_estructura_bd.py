#!/usr/bin/env python
"""
Script de prueba para verificar que el modelo coincide con la estructura de la base de datos.
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

def test_estructura_bd():
    """Prueba que el modelo coincide con la estructura de la base de datos"""
    print("=== PRUEBA DE ESTRUCTURA DE BASE DE DATOS ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba según la estructura de la BD
    form_data = {
        'empre': '0301',
        'rtm': f'ESTRUCT{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Estructura Test {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': ' ',
        'rtnnego': ' ',
        'catastral': 'TEST-001',
        'identidadrep': ' ',
        'representante': ' ',
        'direccion': f'Dirección {timestamp}',
        'actividad': ' ',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': ' ',
        'celular': ' ',
        'socios': 'Socio Test',
        'correo': ' ',
        'pagweb': ' ',
        'comentario': '',
        'usuario': ' ',
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario según estructura BD:")
    print(f"  Empresa: {form_data['empre']}")
    print(f"  RTM: {form_data['rtm']}")
    print(f"  Expediente: {form_data['expe']}")
    print(f"  Nombre: {form_data['nombrenego']}")
    print(f"  Identidad: {form_data['identidad']}")
    print(f"  Catastral: {form_data['catastral']}")
    print(f"  Socios: {form_data['socios']}")
    print(f"  Categoría: {form_data['categoria']}")
    print(f"  Estatus: {form_data['estatus']}")
    
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
                print(f"  Empresa: {negocio_guardado.empre}")
                print(f"  RTM: {negocio_guardado.rtm}")
                print(f"  Expediente: {negocio_guardado.expe}")
                print(f"  Nombre: {negocio_guardado.nombrenego}")
                print(f"  Comerciante: {negocio_guardado.comerciante}")
                print(f"  Identidad: {negocio_guardado.identidad}")
                print(f"  Catastral: {negocio_guardado.catastral}")
                print(f"  Socios: {negocio_guardado.socios}")
                print(f"  Categoría: {negocio_guardado.categoria}")
                print(f"  Estatus: {negocio_guardado.estatus}")
                print(f"  CX: {negocio_guardado.cx}")
                print(f"  CY: {negocio_guardado.cy}")
                print("✅ Estructura de BD funcionando correctamente")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la petición")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE ESTRUCTURA BD")
    print("=" * 60)
    
    test_estructura_bd()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA") 
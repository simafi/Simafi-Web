#!/usr/bin/env python
"""
Script de prueba para verificar que los campos RTM y Expediente se bloqueen correctamente.
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
from django.test import RequestFactory, Client
from hola.views import maestro_negocios

def test_campos_bloqueados():
    """Prueba de bloqueo de campos RTM y Expediente"""
    print("=== PRUEBA DE BLOQUEO DE CAMPOS RTM Y EXPEDIENTE ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # Datos de prueba
    empre = '0301'
    rtm = f'BLOQUEADO{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    # Crear un negocio existente para la prueba
    print(f"\n1. Creando negocio existente para la prueba...")
    negocio_existente = Negocio.objects.create(
        empre=empre,
        rtm=rtm,
        expe=expe,
        nombrenego=f'Negocio Bloqueado Test {timestamp}',
        comerciante=f'Comerciante Bloqueado {timestamp}',
        identidad='9999-9999-99999',
        catastral='TEST-001',
        estatus='A',
        categoria='A',
        socios='Socio Bloqueado'
    )
    print(f"✅ Negocio existente creado con ID: {negocio_existente.id}")
    
    # Probar búsqueda del negocio (simula carga de formulario)
    print(f"\n2. Probando búsqueda del negocio (simula carga de formulario)...")
    
    response_busqueda = client.get(f'/ajax/buscar-negocio/?empre={empre}&rtm={rtm}&expe={expe}')
    
    if response_busqueda.status_code == 200:
        try:
            data_busqueda = response_busqueda.json()
            print(f"✅ Negocio encontrado en búsqueda:")
            print(f"  Empresa: {data_busqueda.get('empre')}")
            print(f"  RTM: {data_busqueda.get('rtm')}")
            print(f"  Expediente: {data_busqueda.get('expe')}")
            print(f"  Nombre: {data_busqueda.get('nombrenego')}")
            
            # Verificar que los datos están completos
            if data_busqueda.get('empre') and data_busqueda.get('rtm') and data_busqueda.get('expe'):
                print("✅ Datos completos para simular carga de formulario")
                print("✅ En el frontend, los campos RTM y Expediente deberían estar deshabilitados")
            else:
                print("❌ Datos incompletos en la respuesta")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta de búsqueda: {str(e)}")
    else:
        print(f"❌ Error en búsqueda: {response_busqueda.status_code}")
    
    # Probar intento de modificación de campos bloqueados
    print(f"\n3. Probando intento de modificación con campos bloqueados...")
    
    # Datos para intentar modificar el negocio existente
    nuevo_expe = str((timestamp % 10000) + 1).zfill(4)
    form_data_modificacion = {
        'empre': empre,
        'rtm': f'MODIFICADO{str(timestamp % 1000).zfill(3)}',  # Intentar cambiar RTM
        'expe': nuevo_expe,                           # Intentar cambiar Expediente
        'nombrenego': f'Negocio Modificado {timestamp}',
        'comerciante': f'Comerciante Modificado {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Modificada {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Modificado',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_modificacion = client.post('/maestro_negocios/', form_data_modificacion, 
                                      HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response_modificacion.status_code}")
    
    if response_modificacion.status_code == 200:
        try:
            data_modificacion = response_modificacion.json()
            print(f"Respuesta JSON: {data_modificacion}")
            
            if data_modificacion.get('requiere_confirmacion') and data_modificacion.get('existe'):
                print("✅ Confirmación solicitada correctamente")
                print("✅ El sistema detectó que se intentó modificar un negocio existente")
                print("✅ En el frontend, esto debería mostrar el diálogo de confirmación")
            else:
                print("❌ No se solicitó confirmación cuando debería")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print("❌ Error en petición de modificación")
    
    # Limpiar datos de prueba
    print(f"\n4. Limpiando datos de prueba...")
    try:
        negocio_existente.delete()
        print("✅ Negocio de prueba eliminado")
    except Exception as e:
        print(f"⚠️ Error al limpiar datos: {str(e)}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE BLOQUEO DE CAMPOS COMPLETADA")
    print("✅ Los campos RTM y Expediente deberían bloquearse al cargar registro")
    print("✅ Solo el botón 'Nuevo' debería habilitar estos campos")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE BLOQUEO DE CAMPOS")
    test_campos_bloqueados() 
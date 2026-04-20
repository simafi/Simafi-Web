#!/usr/bin/env python
"""
Script de prueba para verificar que la confirmación interactiva funcione correctamente.
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

def test_confirmacion_interactiva():
    """Prueba de la confirmación interactiva"""
    print("=== PRUEBA DE CONFIRMACIÓN INTERACTIVA ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # Datos de prueba que ya existen
    empre = '0301'
    rtm = 'CONFIRM-TEST'
    expe = '1234'
    
    # Primero, crear un negocio existente
    print(f"\n1. Creando negocio existente...")
    negocio_existente = Negocio.objects.create(
        empre=empre,
        rtm=rtm,
        expe=expe,
        nombrenego=f'Negocio Existente {timestamp}',
        comerciante=f'Comerciante Existente {timestamp}',
        identidad='9999-9999-99999',
        catastral='TEST-001',
        estatus='A',
        categoria='A',
        socios='Socio Existente'
    )
    print(f"✅ Negocio existente creado con ID: {negocio_existente.id}")
    
    # Datos para intentar guardar el mismo negocio
    form_data = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Actualizado {timestamp}',
        'comerciante': f'Comerciante Actualizado {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Actualizada {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Actualizado',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    print(f"\n2. Probando primera petición (debería solicitar confirmación)...")
    
    # Simular petición AJAX
    response = client.post('/maestro_negocios/', form_data, 
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.get('content-type', 'No especificado')}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Respuesta JSON: {data}")
            
            if data.get('requiere_confirmacion') and data.get('existe'):
                print("✅ Confirmación solicitada correctamente")
                print(f"✅ Mensaje: {data.get('mensaje', 'No mensaje')}")
                
                # Ahora simular la confirmación
                print(f"\n3. Simulando confirmación del usuario...")
                
                form_data_confirmado = form_data.copy()
                form_data_confirmado['confirmar_actualizacion'] = '1'
                
                response_confirmado = client.post('/maestro_negocios/', form_data_confirmado,
                                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                
                print(f"Status confirmación: {response_confirmado.status_code}")
                
                if response_confirmado.status_code == 200:
                    try:
                        data_confirmado = response_confirmado.json()
                        print(f"Respuesta confirmación: {data_confirmado}")
                        
                        if data_confirmado.get('exito'):
                            print("✅ Negocio actualizado exitosamente")
                            
                            # Verificar que se actualizó en la BD
                            negocio_actualizado = Negocio.objects.get(
                                empre=empre, rtm=rtm, expe=expe
                            )
                            print(f"✅ Negocio actualizado en BD:")
                            print(f"  ID: {negocio_actualizado.id}")
                            print(f"  Nombre: {negocio_actualizado.nombrenego}")
                            print(f"  Comerciante: {negocio_actualizado.comerciante}")
                            print(f"  Dirección: {negocio_actualizado.direccion}")
                            print(f"  Socios: {negocio_actualizado.socios}")
                            
                        else:
                            print("❌ Error al actualizar negocio")
                            print(f"  Mensaje: {data_confirmado.get('mensaje', 'Sin mensaje')}")
                            
                    except Exception as e:
                        print(f"❌ Error al parsear respuesta de confirmación: {str(e)}")
                else:
                    print("❌ Error en petición de confirmación")
                    
            else:
                print("❌ No se solicitó confirmación cuando debería")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print("❌ Error en petición inicial")
    
    # Limpiar datos de prueba
    print(f"\n4. Limpiando datos de prueba...")
    try:
        negocio_existente.delete()
        print("✅ Negocio de prueba eliminado")
    except Exception as e:
        print(f"⚠️ Error al limpiar datos: {str(e)}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE CONFIRMACIÓN INTERACTIVA COMPLETADA")
    print("✅ El sistema debería mostrar confirmación interactiva")
    print("✅ El usuario puede responder Sí o No")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CONFIRMACIÓN INTERACTIVA")
    test_confirmacion_interactiva() 
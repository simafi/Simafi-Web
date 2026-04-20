#!/usr/bin/env python
"""
Script de prueba para verificar que todos los botones funcionen correctamente.
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

def test_botones_funcionalidad():
    """Prueba de funcionalidad de todos los botones"""
    print("=== PRUEBA DE FUNCIONALIDAD DE BOTONES ===")
    
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
    rtm = f'BOTONES{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    # Crear un negocio existente para las pruebas
    print(f"\n1. Creando negocio existente para las pruebas...")
    negocio_existente = Negocio.objects.create(
        empre=empre,
        rtm=rtm,
        expe=expe,
        nombrenego=f'Negocio Botones Test {timestamp}',
        comerciante=f'Comerciante Botones {timestamp}',
        identidad='9999-9999-99999',
        catastral='TEST-001',
        estatus='A',
        categoria='A',
        socios='Socio Botones'
    )
    print(f"✅ Negocio existente creado con ID: {negocio_existente.id}")
    
    # Probar botón SALVAR con negocio existente (debería solicitar confirmación)
    print(f"\n2. Probando botón SALVAR con negocio existente...")
    
    form_data_salvar = {
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
    
    response_salvar = client.post('/maestro_negocios/', form_data_salvar, 
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status SALVAR: {response_salvar.status_code}")
    
    if response_salvar.status_code == 200:
        try:
            data_salvar = response_salvar.json()
            print(f"Respuesta SALVAR: {data_salvar}")
            
            if data_salvar.get('requiere_confirmacion') and data_salvar.get('existe'):
                print("✅ Botón SALVAR funciona correctamente - solicita confirmación")
                
                # Simular confirmación
                print(f"\n3. Simulando confirmación del usuario...")
                form_data_confirmado = form_data_salvar.copy()
                form_data_confirmado['confirmar_actualizacion'] = '1'
                
                response_confirmado = client.post('/maestro_negocios/', form_data_confirmado,
                                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                
                if response_confirmado.status_code == 200:
                    try:
                        data_confirmado = response_confirmado.json()
                        print(f"Respuesta confirmación: {data_confirmado}")
                        
                        if data_confirmado.get('exito'):
                            print("✅ Confirmación procesada correctamente")
                        else:
                            print("❌ Error en confirmación")
                    except Exception as e:
                        print(f"❌ Error al parsear respuesta de confirmación: {str(e)}")
                else:
                    print(f"❌ Error en petición de confirmación: {response_confirmado.status_code}")
            else:
                print("❌ No se solicitó confirmación cuando debería")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta SALVAR: {str(e)}")
    else:
        print(f"❌ Error en petición SALVAR: {response_salvar.status_code}")
    
    # Probar botón ELIMINAR
    print(f"\n4. Probando botón ELIMINAR...")
    
    form_data_eliminar = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'accion': 'eliminar'
    }
    
    response_eliminar = client.post('/maestro_negocios/', form_data_eliminar, 
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status ELIMINAR: {response_eliminar.status_code}")
    
    if response_eliminar.status_code == 200:
        try:
            data_eliminar = response_eliminar.json()
            print(f"Respuesta ELIMINAR: {data_eliminar}")
            
            if data_eliminar.get('exito'):
                print("✅ Botón ELIMINAR funciona correctamente")
            else:
                print("❌ Error en eliminación")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta ELIMINAR: {str(e)}")
    else:
        print(f"❌ Error en petición ELIMINAR: {response_eliminar.status_code}")
    
    # Probar botón NUEVO (crear nuevo negocio)
    print(f"\n5. Probando botón NUEVO (crear nuevo negocio)...")
    
    nuevo_rtm = f'NUEVO{str(timestamp % 1000).zfill(3)}'
    nuevo_expe = str((timestamp % 10000) + 1).zfill(4)
    
    form_data_nuevo = {
        'empre': empre,
        'rtm': nuevo_rtm,
        'expe': nuevo_expe,
        'nombrenego': f'Negocio Nuevo {timestamp}',
        'comerciante': f'Comerciante Nuevo {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Nueva {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Nuevo',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_nuevo = client.post('/maestro_negocios/', form_data_nuevo, 
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status NUEVO: {response_nuevo.status_code}")
    
    if response_nuevo.status_code == 200:
        try:
            data_nuevo = response_nuevo.json()
            print(f"Respuesta NUEVO: {data_nuevo}")
            
            if data_nuevo.get('exito'):
                print("✅ Botón NUEVO funciona correctamente - creó nuevo negocio")
                
                # Verificar que se creó en la BD
                try:
                    negocio_nuevo = Negocio.objects.get(
                        empre=empre, rtm=nuevo_rtm, expe=nuevo_expe
                    )
                    print(f"✅ Negocio nuevo creado en BD con ID: {negocio_nuevo.id}")
                    
                    # Limpiar negocio nuevo
                    negocio_nuevo.delete()
                    print("✅ Negocio nuevo eliminado")
                except Negocio.DoesNotExist:
                    print("❌ Negocio nuevo no encontrado en BD")
                except Exception as e:
                    print(f"❌ Error al verificar negocio nuevo: {str(e)}")
            else:
                print("❌ Error al crear nuevo negocio")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta NUEVO: {str(e)}")
    else:
        print(f"❌ Error en petición NUEVO: {response_nuevo.status_code}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE FUNCIONALIDAD DE BOTONES COMPLETADA")
    print("✅ Todos los botones deberían funcionar correctamente")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE FUNCIONALIDAD DE BOTONES")
    test_botones_funcionalidad() 
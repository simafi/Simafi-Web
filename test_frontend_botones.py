#!/usr/bin/env python
"""
Script de prueba para verificar que los botones funcionan correctamente en el frontend.
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

def test_frontend_botones():
    """Prueba de funcionalidad de botones en el frontend"""
    print("=== PRUEBA DE BOTONES EN FRONTEND ===")
    
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
    rtm = f'FRONTEND{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    print(f"\n📋 DATOS DE PRUEBA:")
    print(f"  Empresa: {empre}")
    print(f"  RTM: {rtm}")
    print(f"  Expediente: {expe}")
    
    # ===== PRUEBA 1: VERIFICAR QUE EL FORMULARARIO SE CARGA =====
    print(f"\n🔵 PRUEBA 1: VERIFICAR QUE EL FORMULARARIO SE CARGA")
    
    response_form = client.get('/maestro_negocios/')
    
    print(f"Status del formulario: {response_form.status_code}")
    
    if response_form.status_code == 200:
        print("✅ Formulario maestro_negocios se carga correctamente")
        
        # Verificar que contiene los botones necesarios
        content = response_form.content.decode('utf-8')
        
        if 'value="salvar"' in content:
            print("✅ Botón SALVAR encontrado en el formulario")
        else:
            print("❌ Botón SALVAR NO encontrado en el formulario")
            
        if 'value="eliminar"' in content:
            print("✅ Botón ELIMINAR encontrado en el formulario")
        else:
            print("❌ Botón ELIMINAR NO encontrado en el formulario")
            
        if 'value="nuevo"' in content or 'type="reset"' in content:
            print("✅ Botón NUEVO encontrado en el formulario")
        else:
            print("❌ Botón NUEVO NO encontrado en el formulario")
            
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== PRUEBA 2: CREAR NEGOCIO PARA PRUEBAS =====
    print(f"\n🔵 PRUEBA 2: CREAR NEGOCIO PARA PRUEBAS")
    
    form_data_nuevo = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Frontend Test {timestamp}',
        'comerciante': f'Comerciante Frontend Test {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Frontend Test {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Frontend Test',
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
    
    print(f"Status: {response_nuevo.status_code}")
    
    if response_nuevo.status_code == 200:
        try:
            data_nuevo = response_nuevo.json()
            print(f"Respuesta: {data_nuevo}")
            
            if data_nuevo.get('exito'):
                print("✅ Negocio creado exitosamente para pruebas")
                
                # Verificar que se creó en la BD
                try:
                    negocio_creado = Negocio.objects.get(
                        empre=empre, rtm=rtm, expe=expe
                    )
                    print(f"✅ Negocio creado en BD con ID: {negocio_creado.id}")
                except Negocio.DoesNotExist:
                    print("❌ Negocio no encontrado en BD")
                    return
                except Exception as e:
                    print(f"❌ Error al verificar negocio: {str(e)}")
                    return
            else:
                print("❌ Error al crear negocio")
                return
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
            return
    else:
        print(f"❌ Error en petición: {response_nuevo.status_code}")
        return
    
    # ===== PRUEBA 3: VERIFICAR BOTÓN SALVAR CON NEGOCIO EXISTENTE =====
    print(f"\n🔵 PRUEBA 3: VERIFICAR BOTÓN SALVAR CON NEGOCIO EXISTENTE")
    
    form_data_actualizar = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Actualizado Frontend {timestamp}',
        'comerciante': f'Comerciante Actualizado Frontend {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Actualizada Frontend {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Actualizado Frontend',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_actualizar = client.post('/maestro_negocios/', form_data_actualizar, 
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response_actualizar.status_code}")
    
    if response_actualizar.status_code == 200:
        try:
            data_actualizar = response_actualizar.json()
            print(f"Respuesta: {data_actualizar}")
            
            if data_actualizar.get('requiere_confirmacion') and data_actualizar.get('existe'):
                print("✅ Botón SALVAR funciona correctamente - Solicita confirmación")
                
                # Simular confirmación
                print(f"🔄 Simulando confirmación del usuario...")
                form_data_confirmado = form_data_actualizar.copy()
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
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_actualizar.status_code}")
    
    # ===== PRUEBA 4: VERIFICAR BOTÓN ELIMINAR =====
    print(f"\n🔵 PRUEBA 4: VERIFICAR BOTÓN ELIMINAR")
    
    form_data_eliminar = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'accion': 'eliminar'
    }
    
    response_eliminar = client.post('/maestro_negocios/', form_data_eliminar, 
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response_eliminar.status_code}")
    
    if response_eliminar.status_code == 200:
        try:
            data_eliminar = response_eliminar.json()
            print(f"Respuesta: {data_eliminar}")
            
            if data_eliminar.get('exito'):
                print("✅ Botón ELIMINAR funciona correctamente")
                
                # Verificar que se eliminó de la BD
                try:
                    negocio_eliminado = Negocio.objects.get(
                        empre=empre, rtm=rtm, expe=expe
                    )
                    print("❌ Negocio aún existe en BD (no se eliminó)")
                except Negocio.DoesNotExist:
                    print("✅ Negocio eliminado correctamente de la BD")
                except Exception as e:
                    print(f"❌ Error al verificar eliminación: {str(e)}")
            else:
                print("❌ Error en eliminación")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_eliminar.status_code}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE BOTONES EN FRONTEND FINALIZADA")
    print("✅ Verificando que los botones funcionan correctamente en el frontend")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE BOTONES EN FRONTEND")
    test_frontend_botones() 
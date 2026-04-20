#!/usr/bin/env python
"""
Script de prueba para verificar específicamente el botón salvar en el frontend.
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

def test_frontend_salvar():
    """Prueba específica del botón salvar en el frontend"""
    print("=== PRUEBA ESPECÍFICA DEL BOTÓN SALVAR ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # ===== PRUEBA 1: VERIFICAR QUE EL FORMULARARIO SE CARGA =====
    print(f"\n🔵 PRUEBA 1: VERIFICAR QUE EL FORMULARARIO SE CARGA")
    
    response_form = client.get('/maestro_negocios/')
    
    print(f"Status del formulario: {response_form.status_code}")
    
    if response_form.status_code == 200:
        print("✅ Formulario maestro_negocios se carga correctamente")
        
        # Verificar que contiene el botón salvar
        content = response_form.content.decode('utf-8')
        
        if 'value="salvar"' in content:
            print("✅ Botón SALVAR encontrado en el formulario")
            
            # Verificar que el botón tiene el texto correcto
            if 'Salvar' in content:
                print("✅ Texto 'Salvar' encontrado en el botón")
            else:
                print("❌ Texto 'Salvar' NO encontrado en el botón")
                
        else:
            print("❌ Botón SALVAR NO encontrado en el formulario")
            return
            
        # Verificar que el formulario tiene el método POST
        if 'method="post"' in content.lower():
            print("✅ Formulario tiene método POST")
        else:
            print("❌ Formulario NO tiene método POST")
            
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== PRUEBA 2: VERIFICAR ENVÍO DE FORMULARIO SIN AJAX =====
    print(f"\n🔵 PRUEBA 2: VERIFICAR ENVÍO DE FORMULARIO SIN AJAX")
    
    # Datos de prueba
    empre = '0301'
    rtm = f'SALVAR{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    form_data_simple = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Salvar Test {timestamp}',
        'comerciante': f'Comerciante Salvar Test {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Salvar Test {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Salvar Test',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    # Enviar sin AJAX (simular envío normal del formulario)
    response_simple = client.post('/maestro_negocios/', form_data_simple)
    
    print(f"Status: {response_simple.status_code}")
    
    if response_simple.status_code == 200:
        print("✅ Formulario enviado sin AJAX - Status 200")
        
        # Verificar que se creó el negocio
        try:
            negocio_creado = Negocio.objects.get(
                empre=empre, rtm=rtm, expe=expe
            )
            print(f"✅ Negocio creado en BD con ID: {negocio_creado.id}")
            
            # Limpiar negocio de prueba
            negocio_creado.delete()
            print("✅ Negocio de prueba eliminado")
            
        except Negocio.DoesNotExist:
            print("❌ Negocio no encontrado en BD")
        except Exception as e:
            print(f"❌ Error al verificar negocio: {str(e)}")
    else:
        print(f"❌ Error en envío simple: {response_simple.status_code}")
    
    # ===== PRUEBA 3: VERIFICAR ENVÍO CON AJAX =====
    print(f"\n🔵 PRUEBA 3: VERIFICAR ENVÍO CON AJAX")
    
    # Datos de prueba para AJAX
    rtm_ajax = f'AJAX{str(timestamp % 1000).zfill(3)}'
    expe_ajax = str((timestamp % 10000) + 1).zfill(4)
    
    form_data_ajax = {
        'empre': empre,
        'rtm': rtm_ajax,
        'expe': expe_ajax,
        'nombrenego': f'Negocio AJAX Test {timestamp}',
        'comerciante': f'Comerciante AJAX Test {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección AJAX Test {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio AJAX Test',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    # Enviar con AJAX
    response_ajax = client.post('/maestro_negocios/', form_data_ajax, 
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response_ajax.status_code}")
    
    if response_ajax.status_code == 200:
        try:
            data_ajax = response_ajax.json()
            print(f"Respuesta AJAX: {data_ajax}")
            
            if data_ajax.get('exito'):
                print("✅ AJAX funciona correctamente - Negocio creado")
                
                # Verificar que se creó en la BD
                try:
                    negocio_ajax = Negocio.objects.get(
                        empre=empre, rtm=rtm_ajax, expe=expe_ajax
                    )
                    print(f"✅ Negocio AJAX creado en BD con ID: {negocio_ajax.id}")
                    
                    # Limpiar negocio AJAX
                    negocio_ajax.delete()
                    print("✅ Negocio AJAX eliminado")
                    
                except Negocio.DoesNotExist:
                    print("❌ Negocio AJAX no encontrado en BD")
                except Exception as e:
                    print(f"❌ Error al verificar negocio AJAX: {str(e)}")
            else:
                print("❌ Error en respuesta AJAX")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta AJAX: {str(e)}")
    else:
        print(f"❌ Error en petición AJAX: {response_ajax.status_code}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA ESPECÍFICA DEL BOTÓN SALVAR FINALIZADA")
    print("✅ Verificando que el botón salvar funciona correctamente")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA ESPECÍFICA DEL BOTÓN SALVAR")
    test_frontend_salvar() 
#!/usr/bin/env python
"""
Script para diagnosticar el problema específico de validación.
"""

import os
import sys
import django
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio
from django.test import Client

def test_problema_validacion():
    """Prueba específica para diagnosticar el problema de validación"""
    print("=== DIAGNÓSTICO DEL PROBLEMA DE VALIDACIÓN ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # ===== PRUEBA 1: SIMULAR EXACTAMENTE LO QUE ENVÍA EL FRONTEND =====
    print(f"\n🔵 PRUEBA 1: SIMULAR ENVÍO DEL FRONTEND")
    
    # Datos que debería enviar el frontend cuando los campos están completos
    form_data_completo = {
        'empre': '0301',
        'rtm': 'TEST123',
        'expe': '4567',
        'nombrenego': f'Negocio Test {timestamp}',
        'comerciante': f'Comerciante Test {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Test {timestamp}',
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
    
    print("🔍 Datos que se envían:")
    for key, value in form_data_completo.items():
        print(f"  {key}: '{value}'")
    
    response = client.post('/maestro_negocios/', form_data_completo, 
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Respuesta del servidor: {data}")
            
            if data.get('exito'):
                print("✅ Servidor procesó correctamente")
                
                # Limpiar
                try:
                    negocio = Negocio.objects.get(
                        empre=form_data_completo['empre'], 
                        rtm=form_data_completo['rtm'], 
                        expe=form_data_completo['expe']
                    )
                    negocio.delete()
                    print("✅ Negocio de prueba eliminado")
                except:
                    pass
            else:
                print("❌ Servidor devolvió error")
                print(f"   Mensaje: {data.get('mensaje')}")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response.status_code}")
    
    # ===== PRUEBA 2: VERIFICAR QUÉ RECIBE EL BACKEND =====
    print(f"\n🔵 PRUEBA 2: VERIFICAR DATOS RECIBIDOS EN BACKEND")
    
    # Simular exactamente lo que el backend debería recibir
    from django.test import RequestFactory
    from hola.views import maestro_negocios
    
    factory = RequestFactory()
    
    # Crear request con datos completos
    request = factory.post('/maestro_negocios/', form_data_completo, 
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    # Simular sesión
    request.session = client.session
    
    # Llamar directamente a la vista
    response_direct = maestro_negocios(request)
    
    print(f"Status directo: {response_direct.status_code}")
    
    if response_direct.status_code == 200:
        try:
            data_direct = response_direct.json()
            print(f"Respuesta directa: {data_direct}")
            
            if data_direct.get('exito'):
                print("✅ Vista procesó correctamente")
            else:
                print("❌ Vista devolvió error")
                print(f"   Mensaje: {data_direct.get('mensaje')}")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta directa: {str(e)}")
    else:
        print(f"❌ Error en respuesta directa: {response_direct.status_code}")
    
    # ===== PRUEBA 3: VERIFICAR VALIDACIÓN ESPECÍFICA =====
    print(f"\n🔵 PRUEBA 3: VERIFICAR VALIDACIÓN ESPECÍFICA")
    
    # Probar con datos que sabemos que deberían funcionar
    form_data_simple = {
        'empre': '0301',
        'rtm': 'SIMPLE',
        'expe': '1234',
        'nombrenego': 'Test Simple',
        'comerciante': 'Test Simple',
        'identidad': '9999-9999-99999',
        'catastral': 'TEST-001',
        'direccion': 'Test Simple',
        'categoria': 'A',
        'estatus': 'A',
        'socios': 'Test Simple',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_simple = client.post('/maestro_negocios/', form_data_simple, 
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status simple: {response_simple.status_code}")
    
    if response_simple.status_code == 200:
        try:
            data_simple = response_simple.json()
            print(f"Respuesta simple: {data_simple}")
            
            if data_simple.get('exito'):
                print("✅ Validación simple funcionó")
                
                # Limpiar
                try:
                    negocio = Negocio.objects.get(
                        empre=form_data_simple['empre'], 
                        rtm=form_data_simple['rtm'], 
                        expe=form_data_simple['expe']
                    )
                    negocio.delete()
                    print("✅ Negocio simple eliminado")
                except:
                    pass
            else:
                print("❌ Validación simple falló")
                print(f"   Mensaje: {data_simple.get('mensaje')}")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta simple: {str(e)}")
    else:
        print(f"❌ Error en petición simple: {response_simple.status_code}")
    
    print(f"\n============================================================")
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("📋 Si todas las pruebas pasan, el problema está en el frontend")
    print("📋 Si alguna prueba falla, el problema está en el backend")

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO DE VALIDACIÓN")
    test_problema_validacion() 
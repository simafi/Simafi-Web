#!/usr/bin/env python
"""
Script para verificar que la validación de campos funciona correctamente.
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

def test_validacion_campos():
    """Prueba de validación de campos obligatorios"""
    print("=== PRUEBA DE VALIDACIÓN DE CAMPOS OBLIGATORIOS ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # ===== PRUEBA 1: VERIFICAR HTML =====
    print(f"\n🔵 PRUEBA 1: VERIFICAR HTML")
    
    response_form = client.get('/maestro_negocios/')
    
    if response_form.status_code == 200:
        print("✅ Formulario se carga correctamente")
        content = response_form.content.decode('utf-8')
        
        # Verificar elementos de validación
        elementos_validacion = [
            'validarCamposObligatorios',
            'Campos obligatorios faltantes',
            'complete todos los campos requeridos'
        ]
        
        for elemento in elementos_validacion:
            if elemento in content:
                print(f"✅ {elemento} encontrado")
            else:
                print(f"❌ {elemento} NO encontrado")
        
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== PRUEBA 2: PROBAR CON CAMPOS VACÍOS =====
    print(f"\n🔵 PRUEBA 2: PROBAR CON CAMPOS VACÍOS")
    
    form_data_vacio = {
        'empre': '0301',
        'rtm': '',  # Campo vacío
        'expe': '',  # Campo vacío
        'nombrenego': f'Negocio Test {timestamp}',
        'comerciante': f'Comerciante Test {timestamp}',
        'identidad': '9999-9999-99999',
        'catastral': 'TEST-001',
        'direccion': f'Dirección Test {timestamp}',
        'categoria': 'A',
        'estatus': 'A',
        'socios': 'Socio Test',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_vacio = client.post('/maestro_negocios/', form_data_vacio, 
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status con campos vacíos: {response_vacio.status_code}")
    
    if response_vacio.status_code == 200:
        try:
            data_vacio = response_vacio.json()
            print(f"Respuesta con campos vacíos: {data_vacio}")
            
            if not data_vacio.get('exito') and 'Campos obligatorios faltantes' in data_vacio.get('mensaje', ''):
                print("✅ Validación de campos vacíos funciona correctamente")
            else:
                print("❌ Error en validación de campos vacíos")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_vacio.status_code}")
    
    # ===== PRUEBA 3: PROBAR CON CAMPOS COMPLETOS =====
    print(f"\n🔵 PRUEBA 3: PROBAR CON CAMPOS COMPLETOS")
    
    form_data_completo = {
        'empre': '0301',
        'rtm': f'VALID{str(timestamp % 1000).zfill(3)}',
        'expe': str(timestamp % 10000).zfill(4),
        'nombrenego': f'Negocio Válido {timestamp}',
        'comerciante': f'Comerciante Válido {timestamp}',
        'identidad': '9999-9999-99999',
        'catastral': 'TEST-001',
        'direccion': f'Dirección Válida {timestamp}',
        'categoria': 'A',
        'estatus': 'A',
        'socios': 'Socio Válido',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_completo = client.post('/maestro_negocios/', form_data_completo, 
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status con campos completos: {response_completo.status_code}")
    
    if response_completo.status_code == 200:
        try:
            data_completo = response_completo.json()
            print(f"Respuesta con campos completos: {data_completo}")
            
            if data_completo.get('exito'):
                print("✅ Validación con campos completos funciona correctamente")
                
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
                print("❌ Error en validación con campos completos")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_completo.status_code}")
    
    # ===== PRUEBA 4: PROBAR CON SOLO RTM VACÍO =====
    print(f"\n🔵 PRUEBA 4: PROBAR CON SOLO RTM VACÍO")
    
    form_data_rtm_vacio = form_data_completo.copy()
    form_data_rtm_vacio['rtm'] = ''  # Solo RTM vacío
    
    response_rtm_vacio = client.post('/maestro_negocios/', form_data_rtm_vacio, 
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status con RTM vacío: {response_rtm_vacio.status_code}")
    
    if response_rtm_vacio.status_code == 200:
        try:
            data_rtm_vacio = response_rtm_vacio.json()
            print(f"Respuesta con RTM vacío: {data_rtm_vacio}")
            
            if not data_rtm_vacio.get('exito') and 'RTM' in data_rtm_vacio.get('mensaje', ''):
                print("✅ Validación de RTM vacío funciona correctamente")
            else:
                print("❌ Error en validación de RTM vacío")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_rtm_vacio.status_code}")
    
    # ===== PRUEBA 5: PROBAR CON SOLO EXPEDIENTE VACÍO =====
    print(f"\n🔵 PRUEBA 5: PROBAR CON SOLO EXPEDIENTE VACÍO")
    
    form_data_expe_vacio = form_data_completo.copy()
    form_data_expe_vacio['expe'] = ''  # Solo Expediente vacío
    
    response_expe_vacio = client.post('/maestro_negocios/', form_data_expe_vacio, 
                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status con Expediente vacío: {response_expe_vacio.status_code}")
    
    if response_expe_vacio.status_code == 200:
        try:
            data_expe_vacio = response_expe_vacio.json()
            print(f"Respuesta con Expediente vacío: {data_expe_vacio}")
            
            if not data_expe_vacio.get('exito') and 'Expediente' in data_expe_vacio.get('mensaje', ''):
                print("✅ Validación de Expediente vacío funciona correctamente")
            else:
                print("❌ Error en validación de Expediente vacío")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_expe_vacio.status_code}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE VALIDACIÓN COMPLETADA")
    print("📋 Para verificar en el navegador:")
    print("1. Abre las herramientas de desarrollador (F12)")
    print("2. Ve a la pestaña 'Console'")
    print("3. Intenta presionar SALVAR sin llenar RTM y Expediente")
    print("4. Verifica que aparezca el mensaje de validación")
    print("5. Llena los campos y presiona SALVAR nuevamente")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE VALIDACIÓN DE CAMPOS")
    test_validacion_campos() 
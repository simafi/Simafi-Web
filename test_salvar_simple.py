#!/usr/bin/env python
"""
Script simple para verificar que el botón salvar funciona correctamente.
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

def test_salvar_simple():
    """Prueba simple del botón salvar"""
    print("=== PRUEBA SIMPLE DEL BOTÓN SALVAR ===")
    
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
        
        # Verificar elementos clave
        elementos_clave = [
            'value="salvar"',
            'handleSalvarSubmit',
            'BOTONES_CONFIG',
            'manejarBoton'
        ]
        
        for elemento in elementos_clave:
            if elemento in content:
                print(f"✅ {elemento} encontrado")
            else:
                print(f"❌ {elemento} NO encontrado")
        
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== PRUEBA 2: PROBAR BOTÓN SALVAR =====
    print(f"\n🔵 PRUEBA 2: PROBAR BOTÓN SALVAR")
    
    form_data = {
        'empre': '0301',
        'rtm': f'SIMPLE{str(timestamp % 1000).zfill(3)}',
        'expe': str(timestamp % 10000).zfill(4),
        'nombrenego': f'Negocio Simple {timestamp}',
        'comerciante': f'Comerciante Simple {timestamp}',
        'identidad': '9999-9999-99999',
        'catastral': 'TEST-001',
        'direccion': f'Dirección Simple {timestamp}',
        'categoria': 'A',
        'estatus': 'A',
        'socios': 'Socio Simple',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response = client.post('/maestro_negocios/', form_data, 
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Respuesta: {data}")
            
            if data.get('exito'):
                print("✅ Botón SALVAR funciona correctamente")
                
                # Limpiar
                try:
                    negocio = Negocio.objects.get(
                        empre=form_data['empre'], 
                        rtm=form_data['rtm'], 
                        expe=form_data['expe']
                    )
                    negocio.delete()
                    print("✅ Negocio de prueba eliminado")
                except:
                    pass
            else:
                print("❌ Error en botón SALVAR")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response.status_code}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA SIMPLE COMPLETADA")
    print("📋 Para verificar en el navegador:")
    print("1. Abre las herramientas de desarrollador (F12)")
    print("2. Ve a la pestaña 'Console'")
    print("3. Presiona el botón SALVAR")
    print("4. Verifica los mensajes de console.log")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA SIMPLE DEL BOTÓN SALVAR")
    test_salvar_simple() 
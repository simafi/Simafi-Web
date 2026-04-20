#!/usr/bin/env python
"""
Script para verificar que el botón salvar funciona como antes.
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

def test_boton_salvar_restaurado():
    """Prueba para verificar que el botón salvar funciona como antes"""
    print("=== PRUEBA DE BOTÓN SALVAR RESTAURADO ===")
    
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
    
    # ===== PRUEBA 2: PROBAR BOTÓN SALVAR CON DATOS COMPLETOS =====
    print(f"\n🔵 PRUEBA 2: PROBAR BOTÓN SALVAR CON DATOS COMPLETOS")
    
    form_data = {
        'empre': '0301',
        'rtm': f'REST{str(timestamp % 1000).zfill(3)}',
        'expe': str(timestamp % 10000).zfill(4),
        'nombrenego': f'Negocio Restaurado {timestamp}',
        'comerciante': f'Comerciante Restaurado {timestamp}',
        'identidad': '9999-9999-99999',
        'catastral': 'TEST-001',
        'direccion': f'Dirección Restaurada {timestamp}',
        'categoria': 'A',
        'estatus': 'A',
        'socios': 'Socio Restaurado',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    print("🔍 Enviando datos completos...")
    for key, value in form_data.items():
        print(f"  {key}: '{value}'")
    
    response = client.post('/maestro_negocios/', form_data, 
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Respuesta: {data}")
            
            if data.get('exito'):
                print("✅ BOTÓN SALVAR FUNCIONA: El servidor procesó correctamente")
                
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
                print("❌ PROBLEMA PERSISTE: El servidor devolvió error")
                print(f"   Mensaje: {data.get('mensaje')}")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response.status_code}")
    
    # ===== PRUEBA 3: PROBAR CON NEGOCIO EXISTENTE =====
    print(f"\n🔵 PRUEBA 3: PROBAR CON NEGOCIO EXISTENTE")
    
    # Crear negocio existente
    negocio_existente = Negocio.objects.create(
        empre='0301',
        rtm=f'EXIST{str(timestamp % 1000).zfill(3)}',
        expe=str((timestamp % 10000) + 1).zfill(4),
        nombrenego=f'Negocio Existente {timestamp}',
        comerciante=f'Comerciante Existente {timestamp}',
        identidad='9999-9999-99999',
        catastral='TEST-001',
        direccion=f'Dirección Existente {timestamp}',
        categoria='A',
        estatus='A',
        socios='Socio Existente',
        cx=0.00000000,
        cy=0.00000000
    )
    
    print(f"✅ Negocio existente creado con ID: {negocio_existente.id}")
    
    # Intentar guardar el mismo negocio
    form_data_existente = {
        'empre': '0301',
        'rtm': f'EXIST{str(timestamp % 1000).zfill(3)}',
        'expe': str((timestamp % 10000) + 1).zfill(4),
        'nombrenego': f'Negocio Actualizado {timestamp}',
        'comerciante': f'Comerciante Actualizado {timestamp}',
        'identidad': '9999-9999-99999',
        'catastral': 'TEST-001',
        'direccion': f'Dirección Actualizada {timestamp}',
        'categoria': 'A',
        'estatus': 'A',
        'socios': 'Socio Actualizado',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_existente = client.post('/maestro_negocios/', form_data_existente, 
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status con negocio existente: {response_existente.status_code}")
    
    if response_existente.status_code == 200:
        try:
            data_existente = response_existente.json()
            print(f"Respuesta con negocio existente: {data_existente}")
            
            if data_existente.get('requiere_confirmacion') and data_existente.get('existe'):
                print("✅ CONFIRMACIÓN FUNCIONA: El servidor detecta negocio existente")
            else:
                print("❌ PROBLEMA CON CONFIRMACIÓN: No se detectó negocio existente")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_existente.status_code}")
    
    # Limpiar
    try:
        negocio_existente.delete()
        print("✅ Negocio existente eliminado")
    except:
        pass
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE BOTÓN SALVAR RESTAURADO COMPLETADA")
    print("📋 Si las pruebas pasan, el botón salvar funciona como antes")
    print("📋 Ahora puedes implementar el bloqueo de campos RTM y Expediente")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE BOTÓN SALVAR RESTAURADO")
    test_boton_salvar_restaurado() 
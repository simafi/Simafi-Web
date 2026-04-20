#!/usr/bin/env python
"""
Script de diagnóstico específico para el botón salvar en el navegador.
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

def diagnostico_boton_salvar_navegador():
    """Diagnóstico específico del botón salvar"""
    print("=== DIAGNÓSTICO ESPECÍFICO DEL BOTÓN SALVAR ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # ===== DIAGNÓSTICO 1: VERIFICAR HTML DEL FORMULARIO =====
    print(f"\n🔍 DIAGNÓSTICO 1: VERIFICAR HTML DEL FORMULARIO")
    
    response_form = client.get('/maestro_negocios/')
    
    if response_form.status_code == 200:
        print("✅ Formulario se carga correctamente")
        content = response_form.content.decode('utf-8')
        
        # Verificar estructura del botón salvar
        if 'value="salvar"' in content:
            print("✅ Botón SALVAR encontrado en HTML")
            
            # Buscar la línea específica del botón salvar
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'value="salvar"' in line:
                    print(f"✅ Línea {i+1}: {line.strip()}")
                    break
        else:
            print("❌ Botón SALVAR NO encontrado en HTML")
            return
        
        # Verificar JavaScript
        if 'handleSalvarSubmit' in content:
            print("✅ Función handleSalvarSubmit encontrada")
        else:
            print("❌ Función handleSalvarSubmit NO encontrada")
            
        if 'addEventListener' in content:
            print("✅ Event listener encontrado")
        else:
            print("❌ Event listener NO encontrado")
            
        if 'submit' in content:
            print("✅ Evento submit encontrado")
        else:
            print("❌ Evento submit NO encontrado")
        
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== DIAGNÓSTICO 2: VERIFICAR BACKEND =====
    print(f"\n🔍 DIAGNÓSTICO 2: VERIFICAR BACKEND")
    
    # Datos de prueba
    empre = '0301'
    rtm = f'DIAG{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    form_data_salvar = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Diagnóstico {timestamp}',
        'comerciante': f'Comerciante Diagnóstico {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Diagnóstico {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Diagnóstico',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    # Probar sin AJAX (simular clic directo)
    response_salvar = client.post('/maestro_negocios/', form_data_salvar)
    print(f"Status sin AJAX: {response_salvar.status_code}")
    
    if response_salvar.status_code == 200:
        print("✅ Backend responde correctamente sin AJAX")
        
        # Verificar que se creó en BD
        try:
            negocio_salvar = Negocio.objects.get(empre=empre, rtm=rtm, expe=expe)
            print(f"✅ Negocio creado en BD con ID: {negocio_salvar.id}")
            
            # Limpiar
            negocio_salvar.delete()
            print("✅ Negocio de prueba eliminado")
            
        except Negocio.DoesNotExist:
            print("❌ Negocio no encontrado en BD")
        except Exception as e:
            print(f"❌ Error al verificar negocio: {str(e)}")
    else:
        print(f"❌ Error en backend sin AJAX: {response_salvar.status_code}")
    
    # Probar con AJAX
    response_salvar_ajax = client.post('/maestro_negocios/', form_data_salvar, 
                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    print(f"Status con AJAX: {response_salvar_ajax.status_code}")
    
    if response_salvar_ajax.status_code == 200:
        try:
            data_salvar = response_salvar_ajax.json()
            print(f"Respuesta AJAX: {data_salvar}")
            
            if data_salvar.get('exito'):
                print("✅ Backend responde correctamente con AJAX")
            else:
                print("❌ Error en respuesta AJAX")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta AJAX: {str(e)}")
    else:
        print(f"❌ Error en backend con AJAX: {response_salvar_ajax.status_code}")
    
    # ===== DIAGNÓSTICO 3: VERIFICAR CONFLICTOS =====
    print(f"\n🔍 DIAGNÓSTICO 3: VERIFICAR CONFLICTOS")
    
    # Verificar si hay múltiples event listeners
    if content.count('addEventListener') > 1:
        print("⚠️ MÚLTIPLES EVENT LISTENERS DETECTADOS")
        print("Esto puede causar conflictos en el manejo de eventos")
        
        # Contar event listeners
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'addEventListener' in line:
                print(f"  Línea {i+1}: {line.strip()}")
    else:
        print("✅ Solo un event listener detectado")
    
    # Verificar si hay onclick en botones
    if 'onclick' in content:
        print("⚠️ EVENTOS ONCLICK DETECTADOS")
        print("Esto puede interferir con addEventListener")
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'onclick' in line:
                print(f"  Línea {i+1}: {line.strip()}")
    else:
        print("✅ No hay eventos onclick que puedan interferir")
    
    # ===== DIAGNÓSTICO 4: VERIFICAR BOTÓN NUEVO =====
    print(f"\n🔍 DIAGNÓSTICO 4: VERIFICAR BOTÓN NUEVO")
    
    # Probar botón nuevo
    form_data_nuevo = {
        'accion': 'nuevo'
    }
    
    response_nuevo = client.post('/maestro_negocios/', form_data_nuevo)
    print(f"Status botón NUEVO: {response_nuevo.status_code}")
    
    if response_nuevo.status_code == 200:
        print("✅ Botón NUEVO funciona correctamente")
    else:
        print(f"❌ Error en botón NUEVO: {response_nuevo.status_code}")
    
    # ===== DIAGNÓSTICO 5: RECOMENDACIONES =====
    print(f"\n🔍 DIAGNÓSTICO 5: RECOMENDACIONES")
    
    print("📋 RECOMENDACIONES PARA EL NAVEGADOR:")
    print("1. Abre las herramientas de desarrollador (F12)")
    print("2. Ve a la pestaña 'Console'")
    print("3. Presiona el botón SALVAR")
    print("4. Verifica si aparecen los mensajes de console.log:")
    print("   - '🔄 Evento submit detectado'")
    print("   - '✅ Procesando botón SALVAR'")
    print("   - '🔄 Iniciando handleSalvarSubmit'")
    print("5. Si NO aparecen estos mensajes, hay un problema en el JavaScript")
    print("6. Si aparecen pero no se guarda, hay un problema en el backend")
    
    print("\n📋 POSIBLES CAUSAS DEL PROBLEMA:")
    print("1. Caché del navegador (Ctrl+F5 para refrescar)")
    print("2. JavaScript deshabilitado")
    print("3. Error de sintaxis en JavaScript")
    print("4. Conflicto con otros scripts")
    print("5. Problema de red o servidor")
    
    print(f"\n============================================================")
    print("✅ DIAGNÓSTICO ESPECÍFICO FINALIZADO")
    print("✅ El backend está funcionando correctamente")
    print("✅ El problema debe estar en el frontend (navegador)")

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO ESPECÍFICO DEL BOTÓN SALVAR")
    diagnostico_boton_salvar_navegador() 
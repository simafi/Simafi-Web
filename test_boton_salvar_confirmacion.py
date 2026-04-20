#!/usr/bin/env python
"""
Script para verificar que el botón salvar muestre el mensaje de confirmación correctamente.
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

def test_boton_salvar_confirmacion():
    """Prueba específica del botón salvar y confirmación"""
    print("=== PRUEBA ESPECÍFICA DEL BOTÓN SALVAR Y CONFIRMACIÓN ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # ===== PRUEBA 1: VERIFICAR HTML Y JAVASCRIPT =====
    print(f"\n🔵 PRUEBA 1: VERIFICAR HTML Y JAVASCRIPT")
    
    response_form = client.get('/maestro_negocios/')
    
    if response_form.status_code == 200:
        print("✅ Formulario se carga correctamente")
        content = response_form.content.decode('utf-8')
        
        # Verificar que el botón salvar está presente
        if 'value="salvar"' in content:
            print("✅ Botón SALVAR encontrado en HTML")
        else:
            print("❌ Botón SALVAR NO encontrado en HTML")
            return
        
        # Verificar que la función handleSalvarSubmit está presente
        if 'handleSalvarSubmit' in content:
            print("✅ Función handleSalvarSubmit encontrada")
        else:
            print("❌ Función handleSalvarSubmit NO encontrada")
            return
        
        # Verificar que la arquitectura modular está presente
        if 'BOTONES_CONFIG' in content:
            print("✅ Arquitectura modular BOTONES_CONFIG encontrada")
        else:
            print("❌ Arquitectura modular BOTONES_CONFIG NO encontrada")
            return
        
        # Verificar que la función manejarBoton está presente
        if 'manejarBoton' in content:
            print("✅ Función manejarBoton encontrada")
        else:
            print("❌ Función manejarBoton NO encontrada")
            return
        
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== PRUEBA 2: CREAR NEGOCIO EXISTENTE =====
    print(f"\n🔵 PRUEBA 2: CREAR NEGOCIO EXISTENTE")
    
    empre = '0301'
    rtm = f'CONFIRM{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    # Crear negocio existente
    negocio_existente = Negocio.objects.create(
        empre=empre,
        rtm=rtm,
        expe=expe,
        nombrenego=f'Negocio Existente {timestamp}',
        comerciante=f'Comerciante Existente {timestamp}',
        identidad='9999-9999-99999',
        catastral='TEST-001',
        direccion=f'Dirección Existente {timestamp}',
        categoria='A',
        estatus='A',
        socios='Socio Existente',
        cx=Decimal('-86.2419055'),
        cy=Decimal('15.1999999')
    )
    
    print(f"✅ Negocio existente creado con ID: {negocio_existente.id}")
    
    # ===== PRUEBA 3: PROBAR BOTÓN SALVAR CON NEGOCIO EXISTENTE =====
    print(f"\n🔵 PRUEBA 3: PROBAR BOTÓN SALVAR CON NEGOCIO EXISTENTE")
    
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
    
    # Probar con AJAX (como debería funcionar en el frontend)
    response_salvar = client.post('/maestro_negocios/', form_data_salvar, 
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response_salvar.status_code}")
    
    if response_salvar.status_code == 200:
        try:
            data_salvar = response_salvar.json()
            print(f"Respuesta del servidor: {data_salvar}")
            
            # Verificar que el servidor detecta que el negocio existe
            if data_salvar.get('requiere_confirmacion') and data_salvar.get('existe'):
                print("✅ Servidor detecta negocio existente y requiere confirmación")
                print(f"✅ Mensaje de confirmación: {data_salvar.get('mensaje')}")
                
                # Simular confirmación del usuario
                form_data_confirmado = form_data_salvar.copy()
                form_data_confirmado['confirmar_actualizacion'] = '1'
                
                response_confirmado = client.post('/maestro_negocios/', form_data_confirmado, 
                                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                
                print(f"Status confirmación: {response_confirmado.status_code}")
                
                if response_confirmado.status_code == 200:
                    try:
                        data_confirmado = response_confirmado.json()
                        print(f"Respuesta de confirmación: {data_confirmado}")
                        
                        if data_confirmado.get('exito'):
                            print("✅ Negocio actualizado correctamente después de confirmación")
                            
                            # Verificar que se actualizó
                            negocio_actualizado = Negocio.objects.get(empre=empre, rtm=rtm, expe=expe)
                            if negocio_actualizado.nombrenego == f'Negocio Actualizado {timestamp}':
                                print("✅ Datos actualizados correctamente en BD")
                            else:
                                print("❌ Datos no se actualizaron correctamente")
                                
                        else:
                            print("❌ Error en actualización después de confirmación")
                            
                    except Exception as e:
                        print(f"❌ Error al parsear respuesta de confirmación: {str(e)}")
                else:
                    print(f"❌ Error en petición de confirmación: {response_confirmado.status_code}")
                    
            else:
                print("❌ Servidor no detecta negocio existente o no requiere confirmación")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición del botón SALVAR: {response_salvar.status_code}")
    
    # ===== PRUEBA 4: PROBAR BOTÓN SALVAR CON NEGOCIO NUEVO =====
    print(f"\n🔵 PRUEBA 4: PROBAR BOTÓN SALVAR CON NEGOCIO NUEVO")
    
    rtm_nuevo = f'NUEVO{str(timestamp % 1000).zfill(3)}'
    expe_nuevo = str((timestamp % 10000) + 1).zfill(4)
    
    form_data_nuevo = form_data_salvar.copy()
    form_data_nuevo['rtm'] = rtm_nuevo
    form_data_nuevo['expe'] = expe_nuevo
    form_data_nuevo['nombrenego'] = f'Negocio Nuevo {timestamp}'
    
    response_nuevo = client.post('/maestro_negocios/', form_data_nuevo, 
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status negocio nuevo: {response_nuevo.status_code}")
    
    if response_nuevo.status_code == 200:
        try:
            data_nuevo = response_nuevo.json()
            print(f"Respuesta negocio nuevo: {data_nuevo}")
            
            if data_nuevo.get('exito'):
                print("✅ Negocio nuevo creado correctamente")
                
                # Verificar que se creó
                try:
                    negocio_nuevo = Negocio.objects.get(empre=empre, rtm=rtm_nuevo, expe=expe_nuevo)
                    print(f"✅ Negocio nuevo encontrado en BD con ID: {negocio_nuevo.id}")
                    
                    # Limpiar
                    negocio_nuevo.delete()
                    print("✅ Negocio nuevo eliminado")
                    
                except Negocio.DoesNotExist:
                    print("❌ Negocio nuevo no encontrado en BD")
                    
            else:
                print("❌ Error al crear negocio nuevo")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta de negocio nuevo: {str(e)}")
    else:
        print(f"❌ Error en petición de negocio nuevo: {response_nuevo.status_code}")
    
    # ===== PRUEBA 5: LIMPIAR Y VERIFICAR =====
    print(f"\n🔵 PRUEBA 5: LIMPIAR Y VERIFICAR")
    
    # Limpiar negocio existente
    try:
        negocio_existente.delete()
        print("✅ Negocio existente eliminado")
    except:
        pass
    
    print("\n📋 INSTRUCCIONES PARA VERIFICAR EN EL NAVEGADOR:")
    print("1. Abre el navegador y ve a la página del formulario")
    print("2. Abre las herramientas de desarrollador (F12)")
    print("3. Ve a la pestaña 'Console'")
    print("4. Llena los campos obligatorios (Municipio, RTM, Expediente)")
    print("5. Presiona el botón SALVAR")
    print("6. Verifica que aparezcan estos mensajes en la consola:")
    print("   - '🔄 Procesando botón: salvar'")
    print("   - '✅ Configuración encontrada para salvar: Guardar registro'")
    print("   - '🔄 Llamando a handleSalvarSubmit'")
    print("   - '🔄 Iniciando handleSalvarSubmit'")
    print("7. Si existe el registro, debería aparecer un mensaje de confirmación")
    print("8. Si es nuevo, debería guardarse directamente")
    
    print(f"\n============================================================")
    print("✅ PRUEBA ESPECÍFICA DEL BOTÓN SALVAR COMPLETADA")
    print("✅ Verificar en el navegador que el mensaje de confirmación aparece")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA ESPECÍFICA DEL BOTÓN SALVAR")
    test_boton_salvar_confirmacion() 
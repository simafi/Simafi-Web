#!/usr/bin/env python
"""
Script de prueba para verificar el estado actual de los botones después de los cambios.
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

def test_botones_estado_actual():
    """Prueba del estado actual de los botones después de los cambios"""
    print("=== PRUEBA DE ESTADO ACTUAL DE BOTONES ===")
    
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
    rtm = f'ESTADO{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    print(f"\n📋 DATOS DE PRUEBA:")
    print(f"  Empresa: {empre}")
    print(f"  RTM: {rtm}")
    print(f"  Expediente: {expe}")
    
    # ===== PRUEBA 1: CREAR NEGOCIO NUEVO =====
    print(f"\n🔵 PRUEBA 1: CREAR NEGOCIO NUEVO (BOTÓN SALVAR)")
    
    form_data_nuevo = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Estado Actual {timestamp}',
        'comerciante': f'Comerciante Estado Actual {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Estado Actual {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Estado Actual',
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
                print("✅ Botón SALVAR funciona correctamente - Negocio nuevo creado")
                
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
                print("❌ Error al crear negocio nuevo")
                return
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
            return
    else:
        print(f"❌ Error en petición: {response_nuevo.status_code}")
        return
    
    # ===== PRUEBA 2: ACTUALIZAR NEGOCIO EXISTENTE =====
    print(f"\n🔵 PRUEBA 2: ACTUALIZAR NEGOCIO EXISTENTE (BOTÓN SALVAR)")
    
    form_data_actualizar = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Actualizado Estado {timestamp}',
        'comerciante': f'Comerciante Actualizado Estado {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Actualizada Estado {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Actualizado Estado',
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
    
    # ===== PRUEBA 3: ELIMINAR NEGOCIO =====
    print(f"\n🔵 PRUEBA 3: ELIMINAR NEGOCIO (BOTÓN ELIMINAR)")
    
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
    
    # ===== PRUEBA 4: CREAR NEGOCIO FINAL =====
    print(f"\n🔵 PRUEBA 4: CREAR NEGOCIO FINAL (BOTÓN SALVAR)")
    
    nuevo_rtm = f'FINAL{str(timestamp % 1000).zfill(3)}'
    nuevo_expe = str((timestamp % 10000) + 1).zfill(4)
    
    form_data_final = {
        'empre': empre,
        'rtm': nuevo_rtm,
        'expe': nuevo_expe,
        'nombrenego': f'Negocio Final Estado {timestamp}',
        'comerciante': f'Comerciante Final Estado {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Final Estado {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Final Estado',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    response_final = client.post('/maestro_negocios/', form_data_final, 
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response_final.status_code}")
    
    if response_final.status_code == 200:
        try:
            data_final = response_final.json()
            print(f"Respuesta: {data_final}")
            
            if data_final.get('exito'):
                print("✅ Botón SALVAR funciona correctamente - Negocio final creado")
                
                # Verificar que se creó en la BD
                try:
                    negocio_final = Negocio.objects.get(
                        empre=empre, rtm=nuevo_rtm, expe=nuevo_expe
                    )
                    print(f"✅ Negocio final creado en BD con ID: {negocio_final.id}")
                    
                    # Limpiar negocio final
                    negocio_final.delete()
                    print("✅ Negocio final eliminado")
                except Negocio.DoesNotExist:
                    print("❌ Negocio final no encontrado en BD")
                except Exception as e:
                    print(f"❌ Error al verificar negocio final: {str(e)}")
            else:
                print("❌ Error al crear negocio final")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición: {response_final.status_code}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE ESTADO ACTUAL DE BOTONES FINALIZADA")
    print("✅ Verificando funcionalidad de botones después de los cambios")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE ESTADO ACTUAL DE BOTONES")
    test_botones_estado_actual() 
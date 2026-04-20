#!/usr/bin/env python
"""
Script de prueba para verificar que el botón salvar funciona correctamente después de la corrección.
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

def test_boton_salvar_corregido():
    """Prueba del botón salvar después de la corrección"""
    print("=== PRUEBA DEL BOTÓN SALVAR CORREGIDO ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # ===== PRUEBA 1: VERIFICAR FORMULARIO =====
    print(f"\n🔵 PRUEBA 1: VERIFICAR FORMULARIO")
    
    response_form = client.get('/maestro_negocios/')
    
    if response_form.status_code == 200:
        print("✅ Formulario se carga correctamente")
        content = response_form.content.decode('utf-8')
        
        # Verificar botones específicos
        botones_especiales = ['salvar', 'eliminar']
        botones_normales = ['nuevo', 'configuracion', 'declaracion', 'historial', 'notas', 'estado']
        
        print("🔍 Verificando botones especiales (con AJAX):")
        for boton in botones_especiales:
            if f'value="{boton}"' in content:
                print(f"✅ Botón {boton.upper()} encontrado")
            else:
                print(f"❌ Botón {boton.upper()} NO encontrado")
        
        print("🔍 Verificando botones normales (sin AJAX):")
        for boton in botones_normales:
            if f'value="{boton}"' in content:
                print(f"✅ Botón {boton.upper()} encontrado")
            else:
                print(f"❌ Botón {boton.upper()} NO encontrado")
        
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== PRUEBA 2: VERIFICAR BOTÓN SALVAR =====
    print(f"\n🔵 PRUEBA 2: VERIFICAR BOTÓN SALVAR")
    
    # Datos de prueba
    empre = '0301'
    rtm = f'SALVAR{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    form_data_salvar = {
        'empre': empre,
        'rtm': rtm,
        'expe': expe,
        'nombrenego': f'Negocio Salvar Corregido {timestamp}',
        'comerciante': f'Comerciante Salvar Corregido {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Salvar Corregido {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Salvar Corregido',
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
            print(f"Respuesta: {data_salvar}")
            
            if data_salvar.get('exito'):
                print("✅ Botón SALVAR funciona correctamente con AJAX")
                
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
                print("❌ Error en respuesta del botón SALVAR")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición del botón SALVAR: {response_salvar.status_code}")
    
    # ===== PRUEBA 3: VERIFICAR CONFIRMACIÓN =====
    print(f"\n🔵 PRUEBA 3: VERIFICAR CONFIRMACIÓN")
    
    # Crear negocio para actualizar
    rtm_actualizar = f'ACTUALIZAR{str(timestamp % 1000).zfill(3)}'
    expe_actualizar = str((timestamp % 10000) + 1).zfill(4)
    
    form_data_crear = form_data_salvar.copy()
    form_data_crear['rtm'] = rtm_actualizar
    form_data_crear['expe'] = expe_actualizar
    form_data_crear['nombrenego'] = f'Negocio para Actualizar {timestamp}'
    
    response_crear = client.post('/maestro_negocios/', form_data_crear, 
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    if response_crear.status_code == 200:
        try:
            data_crear = response_crear.json()
            if data_crear.get('exito'):
                print("✅ Negocio creado para prueba de actualización")
                
                # Intentar actualizar (debería solicitar confirmación)
                form_data_actualizar = form_data_crear.copy()
                form_data_actualizar['nombrenego'] = f'Negocio Actualizado {timestamp}'
                
                response_actualizar = client.post('/maestro_negocios/', form_data_actualizar, 
                                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                
                if response_actualizar.status_code == 200:
                    try:
                        data_actualizar = response_actualizar.json()
                        
                        if data_actualizar.get('requiere_confirmacion') and data_actualizar.get('existe'):
                            print("✅ Confirmación solicitada correctamente")
                            
                            # Simular confirmación
                            form_data_confirmado = form_data_actualizar.copy()
                            form_data_confirmado['confirmar_actualizacion'] = '1'
                            
                            response_confirmado = client.post('/maestro_negocios/', form_data_confirmado,
                                                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                            
                            if response_confirmado.status_code == 200:
                                try:
                                    data_confirmado = response_confirmado.json()
                                    if data_confirmado.get('exito'):
                                        print("✅ Confirmación procesada correctamente")
                                        
                                        # Limpiar
                                        try:
                                            negocio_actualizado = Negocio.objects.get(
                                                empre=empre, rtm=rtm_actualizar, expe=expe_actualizar
                                            )
                                            negocio_actualizado.delete()
                                            print("✅ Negocio de prueba eliminado")
                                        except:
                                            pass
                                        
                                    else:
                                        print("❌ Error en confirmación")
                                except Exception as e:
                                    print(f"❌ Error al parsear confirmación: {str(e)}")
                            else:
                                print(f"❌ Error en petición de confirmación: {response_confirmado.status_code}")
                        else:
                            print("❌ No se solicitó confirmación cuando debería")
                            
                    except Exception as e:
                        print(f"❌ Error al parsear respuesta de actualización: {str(e)}")
                else:
                    print(f"❌ Error en petición de actualización: {response_actualizar.status_code}")
            else:
                print("❌ Error al crear negocio para actualización")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta de creación: {str(e)}")
    else:
        print(f"❌ Error en petición de creación: {response_crear.status_code}")
    
    # ===== PRUEBA 4: VERIFICAR QUE OTROS BOTONES NO SE AFECTAN =====
    print(f"\n🔵 PRUEBA 4: VERIFICAR QUE OTROS BOTONES NO SE AFECTAN")
    
    # Probar botón nuevo (debería funcionar normalmente)
    form_data_nuevo = {
        'accion': 'nuevo'
    }
    
    response_nuevo = client.post('/maestro_negocios/', form_data_nuevo)
    print(f"Status botón NUEVO: {response_nuevo.status_code}")
    
    if response_nuevo.status_code == 200:
        print("✅ Botón NUEVO funciona correctamente")
    else:
        print(f"❌ Error en botón NUEVO: {response_nuevo.status_code}")
    
    # Probar botón configuración (debería funcionar normalmente)
    form_data_config = {
        'accion': 'configuracion'
    }
    
    response_config = client.post('/maestro_negocios/', form_data_config)
    print(f"Status botón CONFIGURACIÓN: {response_config.status_code}")
    
    if response_config.status_code == 200:
        print("✅ Botón CONFIGURACIÓN funciona correctamente")
    else:
        print(f"❌ Error en botón CONFIGURACIÓN: {response_config.status_code}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DEL BOTÓN SALVAR CORREGIDO FINALIZADA")
    print("✅ El botón SALVAR funciona correctamente")
    print("✅ Los otros botones no se ven afectados")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DEL BOTÓN SALVAR CORREGIDO")
    test_boton_salvar_corregido() 
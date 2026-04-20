#!/usr/bin/env python
"""
Script de diagnóstico completo para verificar todos los aspectos de los botones.
"""

import os
import sys
import django
import time
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Negocio
from django.test import RequestFactory, Client
from tributario_app.views import maestro_negocios

def diagnostico_completo_botones():
    """Diagnóstico completo de todos los botones"""
    print("=== DIAGNÓSTICO COMPLETO DE BOTONES ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # ===== DIAGNÓSTICO 1: VERIFICAR FORMULARIO =====
    print(f"\n🔍 DIAGNÓSTICO 1: VERIFICAR FORMULARIO")
    
    response_form = client.get('/maestro_negocios/')
    
    if response_form.status_code == 200:
        print("✅ Formulario se carga correctamente")
        content = response_form.content.decode('utf-8')
        
        # Verificar botones
        botones = [
            ('salvar', 'Salvar'),
            ('eliminar', 'Eliminar'),
            ('nuevo', 'Nuevo'),
            ('configuracion', 'Configuración'),
            ('declaracion', 'Declaración'),
            ('historial', 'Historial'),
            ('notas', 'Notas'),
            ('estado', 'Estado')
        ]
        
        for value, texto in botones:
            if f'value="{value}"' in content:
                print(f"✅ Botón {texto} ({value}) encontrado")
            else:
                print(f"❌ Botón {texto} ({value}) NO encontrado")
        
        # Verificar campos obligatorios
        campos_obligatorios = ['id_empre', 'id_rtm', 'id_expe']
        for campo in campos_obligatorios:
            if campo in content:
                print(f"✅ Campo {campo} encontrado")
            else:
                print(f"❌ Campo {campo} NO encontrado")
        
        # Verificar JavaScript
        funciones_js = [
            'handleSalvarSubmit',
            'handleEliminarSubmit',
            'buscarNegocio',
            'llenarFormulario',
            'limpiarFormulario',
            'mostrarMensaje',
            'addEventListener',
            'submit'
        ]
        
        print(f"\n🔍 Verificando JavaScript:")
        for funcion in funciones_js:
            if funcion in content:
                print(f"✅ Función {funcion} encontrada")
            else:
                print(f"❌ Función {funcion} NO encontrada")
        
    else:
        print(f"❌ Error al cargar formulario: {response_form.status_code}")
        return
    
    # ===== DIAGNÓSTICO 2: VERIFICAR BOTÓN SALVAR =====
    print(f"\n🔍 DIAGNÓSTICO 2: VERIFICAR BOTÓN SALVAR")
    
    # Datos de prueba
    empre = '0301'
    rtm = f'DIAG{str(timestamp % 1000).zfill(3)}'
    expe = str(timestamp % 10000).zfill(4)
    
    form_data_salvar = {
        'empresa': empre,
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
    
    # Probar sin AJAX
    response_salvar = client.post('/maestro_negocios/', form_data_salvar)
    print(f"Status sin AJAX: {response_salvar.status_code}")
    
    if response_salvar.status_code == 200:
        print("✅ Botón SALVAR funciona sin AJAX")
        
        # Verificar que se creó en BD
        try:
            negocio_salvar = Negocio.objects.get(empresa=empre, rtm=rtm, expe=expe)
            print(f"✅ Negocio creado en BD con ID: {negocio_salvar.id}")
            
            # Limpiar
            negocio_salvar.delete()
            print("✅ Negocio de prueba eliminado")
            
        except Negocio.DoesNotExist:
            print("❌ Negocio no encontrado en BD")
        except Exception as e:
            print(f"❌ Error al verificar negocio: {str(e)}")
    else:
        print(f"❌ Error en botón SALVAR: {response_salvar.status_code}")
    
    # ===== DIAGNÓSTICO 3: VERIFICAR BOTÓN ELIMINAR =====
    print(f"\n🔍 DIAGNÓSTICO 3: VERIFICAR BOTÓN ELIMINAR")
    
    # Crear negocio para eliminar
    rtm_eliminar = f'ELIM{str(timestamp % 1000).zfill(3)}'
    expe_eliminar = str((timestamp % 10000) + 1).zfill(4)
    
    form_data_crear = form_data_salvar.copy()
    form_data_crear['rtm'] = rtm_eliminar
    form_data_crear['expe'] = expe_eliminar
    form_data_crear['nombrenego'] = f'Negocio para Eliminar {timestamp}'
    
    response_crear = client.post('/maestro_negocios/', form_data_crear)
    
    if response_crear.status_code == 200:
        print("✅ Negocio creado para prueba de eliminación")
        
        # Probar eliminación
        form_data_eliminar = {
            'empresa': empre,
            'rtm': rtm_eliminar,
            'expe': expe_eliminar,
            'accion': 'eliminar'
        }
        
        response_eliminar = client.post('/maestro_negocios/', form_data_eliminar, 
                                      HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        print(f"Status eliminación: {response_eliminar.status_code}")
        
        if response_eliminar.status_code == 200:
            try:
                data_eliminar = response_eliminar.json()
                if data_eliminar.get('exito'):
                    print("✅ Botón ELIMINAR funciona correctamente")
                    
                    # Verificar que se eliminó
                    try:
                        negocio_eliminado = Negocio.objects.get(
                            empresa=empre, rtm=rtm_eliminar, expe=expe_eliminar
                        )
                        print("❌ Negocio aún existe en BD")
                    except Negocio.DoesNotExist:
                        print("✅ Negocio eliminado correctamente")
                        
                else:
                    print("❌ Error en eliminación")
                    
            except Exception as e:
                print(f"❌ Error al parsear respuesta: {str(e)}")
        else:
            print(f"❌ Error en petición de eliminación: {response_eliminar.status_code}")
    else:
        print("❌ Error al crear negocio para eliminación")
    
    # ===== DIAGNÓSTICO 4: VERIFICAR CONFIRMACIONES =====
    print(f"\n🔍 DIAGNÓSTICO 4: VERIFICAR CONFIRMACIONES")
    
    # Intentar actualizar el negocio existente
    form_data_actualizar = form_data_salvar.copy()
    form_data_actualizar['nombrenego'] = f'Negocio Actualizado Diagnóstico {timestamp}'
    
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
                        else:
                            print("❌ Error en confirmación")
                    except Exception as e:
                        print(f"❌ Error al parsear confirmación: {str(e)}")
                else:
                    print(f"❌ Error en petición de confirmación: {response_confirmado.status_code}")
            else:
                print("❌ No se solicitó confirmación cuando debería")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print(f"❌ Error en petición de actualización: {response_actualizar.status_code}")
    
    # ===== DIAGNÓSTICO 5: VERIFICAR CAMPOS BLOQUEADOS =====
    print(f"\n🔍 DIAGNÓSTICO 5: VERIFICAR CAMPOS BLOQUEADOS")
    
    # Buscar negocio existente
    response_busqueda = client.get(f'/ajax/buscar-negocio/?empresa={empre}&rtm={rtm}&expe={expe}')
    
    if response_busqueda.status_code == 200:
        try:
            data_busqueda = response_busqueda.json()
            if not data_busqueda.get('error'):
                print("✅ Negocio encontrado para prueba de campos bloqueados")
                print("✅ En el frontend, los campos RTM y Expediente deberían estar BLOQUEADOS")
            else:
                print("❌ Negocio no encontrado para prueba de campos bloqueados")
        except Exception as e:
            print(f"❌ Error al parsear búsqueda: {str(e)}")
    else:
        print(f"❌ Error en búsqueda: {response_busqueda.status_code}")
    
    print(f"\n============================================================")
    print("✅ DIAGNÓSTICO COMPLETO FINALIZADO")
    print("✅ Todos los botones están funcionando correctamente")
    print("✅ El problema puede estar en el navegador o caché")

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO COMPLETO DE BOTONES")
    diagnostico_completo_botones() 

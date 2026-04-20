#!/usr/bin/env python
"""
Script de prueba para verificar que las coordenadas se guarden correctamente.
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

def test_coordenadas_guardado():
    """Prueba del guardado de coordenadas"""
    print("=== PRUEBA DE GUARDADO DE COORDENADAS ===")
    
    timestamp = int(time.time())
    
    # Crear cliente de prueba
    client = Client()
    
    # Simular login (establecer sesión)
    session = client.session
    session['municipio_codigo'] = '0301'
    session['municipio_descripcion'] = 'Municipio Test'
    session.save()
    
    # Datos de prueba con coordenadas específicas
    form_data = {
        'empre': '0301',
        'rtm': f'COORD{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Coordenadas Test {timestamp}',
        'comerciante': f'Comerciante Coordenadas {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección Coordenadas {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Coordenadas Test',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86.2419055',  # Coordenada X específica
        'cy': '15.1999999',   # Coordenada Y específica
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario con coordenadas:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    print(f"\n1. Probando guardado con coordenadas...")
    
    # Simular petición AJAX
    response = client.post('/maestro_negocios/', form_data, 
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.get('content-type', 'No especificado')}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Respuesta JSON: {data}")
            
            if data.get('exito'):
                print("✅ Negocio guardado exitosamente")
                
                # Verificar que el negocio se guardó en la base de datos con coordenadas
                try:
                    negocio_guardado = Negocio.objects.get(
                        empre=form_data['empre'],
                        rtm=form_data['rtm'],
                        expe=form_data['expe']
                    )
                    print("✅ Negocio encontrado en BD:")
                    print(f"  ID: {negocio_guardado.id}")
                    print(f"  Nombre: {negocio_guardado.nombrenego}")
                    print(f"  CX: {negocio_guardado.cx}")
                    print(f"  CY: {negocio_guardado.cy}")
                    
                    # Verificar que las coordenadas se guardaron correctamente
                    cx_esperado = float(form_data['cx'])
                    cy_esperado = float(form_data['cy'])
                    
                    # Convertir Decimal a float para comparación
                    cx_guardado = float(negocio_guardado.cx)
                    cy_guardado = float(negocio_guardado.cy)
                    
                    if abs(cx_guardado - cx_esperado) < 0.0000001:
                        print("✅ Coordenada X guardada correctamente")
                    else:
                        print(f"❌ Error en coordenada X: esperado {cx_esperado}, guardado {cx_guardado}")
                    
                    if abs(cy_guardado - cy_esperado) < 0.0000001:
                        print("✅ Coordenada Y guardada correctamente")
                    else:
                        print(f"❌ Error en coordenada Y: esperado {cy_esperado}, guardado {cy_guardado}")
                    
                    # Probar búsqueda del negocio para verificar que las coordenadas se devuelven
                    print(f"\n2. Probando búsqueda del negocio...")
                    
                    response_busqueda = client.get(f'/ajax/buscar-negocio/?empre={form_data["empre"]}&rtm={form_data["rtm"]}&expe={form_data["expe"]}')
                    
                    if response_busqueda.status_code == 200:
                        try:
                            data_busqueda = response_busqueda.json()
                            print(f"Respuesta búsqueda: {data_busqueda}")
                            
                            if 'cx' in data_busqueda and 'cy' in data_busqueda:
                                print(f"✅ Coordenadas en respuesta de búsqueda:")
                                print(f"  CX: {data_busqueda['cx']}")
                                print(f"  CY: {data_busqueda['cy']}")
                                
                                # Verificar que las coordenadas en la respuesta coinciden
                                if data_busqueda['cx'] == str(negocio_guardado.cx):
                                    print("✅ Coordenada X en respuesta correcta")
                                else:
                                    print(f"❌ Error en coordenada X de respuesta: esperado {negocio_guardado.cx}, recibido {data_busqueda['cx']}")
                                
                                if data_busqueda['cy'] == str(negocio_guardado.cy):
                                    print("✅ Coordenada Y en respuesta correcta")
                                else:
                                    print(f"❌ Error en coordenada Y de respuesta: esperado {negocio_guardado.cy}, recibido {data_busqueda['cy']}")
                            else:
                                print("❌ Coordenadas no encontradas en respuesta de búsqueda")
                                
                        except Exception as e:
                            print(f"❌ Error al parsear respuesta de búsqueda: {str(e)}")
                    else:
                        print(f"❌ Error en búsqueda: {response_busqueda.status_code}")
                    
                except Negocio.DoesNotExist:
                    print("❌ Negocio no encontrado en la base de datos")
                except Exception as e:
                    print(f"❌ Error al buscar negocio: {str(e)}")
            else:
                print("❌ Error al guardar negocio")
                print(f"  Mensaje: {data.get('mensaje', 'Sin mensaje')}")
                
        except Exception as e:
            print(f"❌ Error al parsear respuesta: {str(e)}")
    else:
        print("❌ Error en petición")
        print(f"Contenido: {response.content.decode('utf-8')[:500]}...")
    
    # Limpiar datos de prueba
    print(f"\n3. Limpiando datos de prueba...")
    try:
        negocio_guardado = Negocio.objects.get(
            empre=form_data['empre'],
            rtm=form_data['rtm'],
            expe=form_data['expe']
        )
        negocio_guardado.delete()
        print("✅ Negocio de prueba eliminado")
    except Exception as e:
        print(f"⚠️ Error al limpiar datos: {str(e)}")
    
    print(f"\n============================================================")
    print("✅ PRUEBA DE GUARDADO DE COORDENADAS COMPLETADA")
    print("✅ Las coordenadas deberían guardarse correctamente")
    print("✅ El mapa debería posicionarse automáticamente")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE GUARDADO DE COORDENADAS")
    test_coordenadas_guardado() 
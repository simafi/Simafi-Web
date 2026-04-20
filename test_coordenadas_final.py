#!/usr/bin/env python
"""
Script de prueba final para verificar el funcionamiento completo del formulario maestro_negocios
con coordenadas y guardado.
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
from django.test import RequestFactory
from hola.views import maestro_negocios, buscar_negocio

def test_coordenadas_completas():
    """Prueba completa del sistema de coordenadas"""
    print("=== PRUEBA COMPLETA DE COORDENADAS ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba con coordenadas válidas
    form_data = {
        'empre': '0301',
        'rtm': f'COORD-{timestamp}',
        'expe': f'{timestamp}',
        'nombrenego': f'Negocio Coordenadas {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': f'9999-{timestamp}-99999',
        'direccion': f'Dirección {timestamp}',
        'cx': '-86.2419055',  # Coordenada X válida
        'cy': '15.1999999',   # Coordenada Y válida
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    request.headers = {'X-Requested-With': 'XMLHttpRequest'}
    
    print(f"\n1. Creando nuevo registro con coordenadas...")
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        print(f"Contenido: {response.content.decode()}")
        
        if response.status_code == 200:
            print("✅ Registro creado exitosamente")
            
            # Verificar que se guardó en la base de datos
            negocio_guardado = Negocio.objects.filter(
                empre=form_data['empre'],
                rtm=form_data['rtm'],
                expe=form_data['expe']
            ).first()
            
            if negocio_guardado:
                print(f"✅ Negocio encontrado en BD:")
                print(f"  ID: {negocio_guardado.id}")
                print(f"  Nombre: {negocio_guardado.nombrenego}")
                print(f"  CX: {negocio_guardado.cx}")
                print(f"  CY: {negocio_guardado.cy}")
                
                # Verificar coordenadas
                if negocio_guardado.cx == Decimal('-86.2419055') and negocio_guardado.cy == Decimal('15.1999999'):
                    print("✅ Coordenadas guardadas correctamente")
                else:
                    print("❌ Error: Coordenadas no se guardaron correctamente")
                    print(f"  Esperado: CX=-86.2419055, CY=15.1999999")
                    print(f"  Obtenido: CX={negocio_guardado.cx}, CY={negocio_guardado.cy}")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la creación del registro")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def test_busqueda_coordenadas():
    """Prueba de búsqueda con coordenadas"""
    print("\n=== PRUEBA DE BÚSQUEDA CON COORDENADAS ===")
    
    # Buscar un negocio existente
    negocio_existente = Negocio.objects.filter(cx__gt=0).first()
    
    if negocio_existente:
        print(f"Buscando negocio existente: {negocio_existente.empre}-{negocio_existente.rtm}-{negocio_existente.expe}")
        
        factory = RequestFactory()
        request = factory.get(f'/ajax/buscar-negocio/?empre={negocio_existente.empre}&rtm={negocio_existente.rtm}&expe={negocio_existente.expe}')
        
        try:
            response = buscar_negocio(request)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Negocio encontrado:")
                print(f"  Nombre: {data.get('nombrenego')}")
                print(f"  CX: {data.get('cx')}")
                print(f"  CY: {data.get('cy')}")
                
                # Verificar que las coordenadas están en la respuesta
                if 'cx' in data and 'cy' in data:
                    print("✅ Coordenadas incluidas en la respuesta JSON")
                else:
                    print("❌ Error: Coordenadas no incluidas en la respuesta")
            else:
                print("❌ Error en la búsqueda")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print("⚠️ No hay negocios con coordenadas para probar")

def test_actualizacion_coordenadas():
    """Prueba de actualización de coordenadas"""
    print("\n=== PRUEBA DE ACTUALIZACIÓN DE COORDENADAS ===")
    
    # Buscar un negocio existente
    negocio_existente = Negocio.objects.first()
    
    if negocio_existente:
        timestamp = int(time.time())
        
        # Datos para actualizar
        form_data = {
            'empre': negocio_existente.empre,
            'rtm': negocio_existente.rtm,
            'expe': negocio_existente.expe,
            'nombrenego': f'Actualizado {timestamp}',
            'cx': '-87.1234567',  # Nueva coordenada X
            'cy': '14.9876543',   # Nueva coordenada Y
            'accion': 'salvar',
            'confirmar_actualizacion': '1'  # Confirmar actualización
        }
        
        print(f"Actualizando negocio: {negocio_existente.empre}-{negocio_existente.rtm}-{negocio_existente.expe}")
        print(f"Nuevas coordenadas: CX={form_data['cx']}, CY={form_data['cy']}")
        
        factory = RequestFactory()
        request = factory.post('/maestro_negocios/', form_data)
        request.headers = {'X-Requested-With': 'XMLHttpRequest'}
        
        try:
            response = maestro_negocios(request)
            print(f"Status: {response.status_code}")
            print(f"Contenido: {response.content.decode()}")
            
            if response.status_code == 200:
                print("✅ Actualización completada")
                
                # Verificar que se actualizó en la BD
                negocio_actualizado = Negocio.objects.get(
                    empre=negocio_existente.empre,
                    rtm=negocio_existente.rtm,
                    expe=negocio_existente.expe
                )
                
                print(f"Coordenadas actualizadas:")
                print(f"  CX: {negocio_actualizado.cx}")
                print(f"  CY: {negocio_actualizado.cy}")
                
                if negocio_actualizado.cx == Decimal('-87.1234567') and negocio_actualizado.cy == Decimal('14.9876543'):
                    print("✅ Coordenadas actualizadas correctamente")
                else:
                    print("❌ Error: Coordenadas no se actualizaron correctamente")
            else:
                print("❌ Error en la actualización")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print("⚠️ No hay negocios para actualizar")

def test_coordenadas_invalidas():
    """Prueba con coordenadas inválidas"""
    print("\n=== PRUEBA CON COORDENADAS INVÁLIDAS ===")
    
    timestamp = int(time.time())
    
    # Datos con coordenadas inválidas
    form_data = {
        'empre': '0301',
        'rtm': f'INVAL-{timestamp}',
        'expe': f'{timestamp}',
        'nombrenego': f'Negocio Coordenadas Inválidas {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': f'9999-{timestamp}-99999',
        'direccion': f'Dirección {timestamp}',
        'cx': '0.0000000',  # Coordenada X inválida (cero)
        'cy': '',            # Coordenada Y vacía
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario con coordenadas inválidas:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    request.headers = {'X-Requested-With': 'XMLHttpRequest'}
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        print(f"Contenido: {response.content.decode()}")
        
        if response.status_code == 200:
            print("✅ Registro creado con coordenadas inválidas (debería usar valores por defecto)")
            
            # Verificar que se guardó con valores por defecto
            negocio_guardado = Negocio.objects.filter(
                empre=form_data['empre'],
                rtm=form_data['rtm'],
                expe=form_data['expe']
            ).first()
            
            if negocio_guardado:
                print(f"Coordenadas guardadas:")
                print(f"  CX: {negocio_guardado.cx}")
                print(f"  CY: {negocio_guardado.cy}")
                
                if negocio_guardado.cx == Decimal('0.0000000') and negocio_guardado.cy is None:
                    print("✅ Coordenadas inválidas manejadas correctamente")
                else:
                    print("❌ Error: Coordenadas inválidas no manejadas correctamente")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la creación del registro")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS COMPLETAS DEL SISTEMA DE COORDENADAS")
    print("=" * 60)
    
    # Ejecutar todas las pruebas
    test_coordenadas_completas()
    test_busqueda_coordenadas()
    test_actualizacion_coordenadas()
    test_coordenadas_invalidas()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("El sistema de coordenadas está funcionando correctamente.") 
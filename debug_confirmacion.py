#!/usr/bin/env python
"""
Script de debugging para el problema de confirmación de actualización.
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio
from django.test import RequestFactory
from hola.views import maestro_negocios

def debug_confirmacion_problema():
    """Debug específico del problema de confirmación"""
    print("=== DEBUG CONFIRMACIÓN PROBLEMA ===")
    
    # Buscar el negocio específico del problema
    negocio = Negocio.objects.filter(
        empre='0301',
        rtm='114-03-23',
        expe='1151'
    ).first()
    
    if not negocio:
        print("Creando negocio de prueba...")
        negocio = Negocio.objects.create(
            empre='0301',
            rtm='114-03-23',
            expe='1151',
            nombrenego='Negocio de Prueba',
            cx=Decimal('0.0000000'),
            cy=None
        )
        print(f"Negocio creado con ID: {negocio.id}")
    
    print(f"Negocio encontrado:")
    print(f"  ID: {negocio.id}")
    print(f"  Empresa: {negocio.empre}")
    print(f"  RTM: {negocio.rtm}")
    print(f"  Expediente: {negocio.expe}")
    print(f"  Coordenadas actuales - CX: {negocio.cx}, CY: {negocio.cy}")
    
    # Simular datos del formulario que causan el problema
    form_data = {
        'empre': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'nombrenego': 'Negocio Actualizado - Debug',
        'direccion': 'Dirección Actualizada',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar',
        'confirmar_actualizacion': '1'  # Confirmación
    }
    
    print(f"\nDatos del formulario:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    request.headers = {'X-Requested-With': 'XMLHttpRequest'}
    
    print(f"\nSimulando petición de confirmación...")
    
    try:
        # Llamar directamente a la vista
        response = maestro_negocios(request)
        
        print(f"Status de respuesta: {response.status_code}")
        print(f"Contenido de respuesta: {response.content.decode()}")
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content.decode())
            print(f"Respuesta JSON: {json.dumps(data, indent=2)}")
            
            if data.get('exito'):
                print("✅ Actualización exitosa")
                
                # Verificar en la base de datos
                negocio_refresh = Negocio.objects.get(id=negocio.id)
                print(f"Verificación en BD:")
                print(f"  CX: {negocio_refresh.cx}")
                print(f"  CY: {negocio_refresh.cy}")
                print(f"  Nombre: {negocio_refresh.nombrenego}")
            else:
                print(f"❌ Error en actualización: {data.get('mensaje')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()

def debug_modelo_negocio():
    """Debug del modelo Negocio"""
    print("\n=== DEBUG MODELO NEGOCIO ===")
    
    # Verificar estructura del modelo
    negocio = Negocio.objects.first()
    if negocio:
        print(f"Campos del modelo Negocio:")
        for field in negocio._meta.fields:
            print(f"  {field.name}: {field.get_internal_type()} - {getattr(negocio, field.name)}")
    
    # Verificar restricciones de la base de datos
    print(f"\nVerificando restricciones de BD...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE negocios")
            columns = cursor.fetchall()
            print("Estructura de la tabla negocios:")
            for column in columns:
                print(f"  {column[0]}: {column[1]}")
    except Exception as e:
        print(f"Error al verificar estructura: {e}")

def debug_coordenadas():
    """Debug específico de coordenadas"""
    print("\n=== DEBUG COORDENADAS ===")
    
    # Probar diferentes formatos de coordenadas
    test_coordinates = [
        '-86.2419055',
        '15.1999999',
        '-86,2419055',
        '15,1999999',
        '',
        '0',
        '0.0000000'
    ]
    
    for coord in test_coordinates:
        try:
            # Simular el parse_coordinate del backend
            if not coord or coord == '':
                parsed = 0.0000000
            else:
                if isinstance(coord, str):
                    coord = coord.replace(',', '.')
                parsed = float(coord)
            
            print(f"Coordenada '{coord}' -> {parsed} (tipo: {type(parsed)})")
        except Exception as e:
            print(f"Error parseando '{coord}': {e}")

def debug_actualizacion_directa():
    """Debug de actualización directa en BD"""
    print("\n=== DEBUG ACTUALIZACIÓN DIRECTA ===")
    
    negocio = Negocio.objects.filter(
        empre='0301',
        rtm='114-03-23',
        expe='1151'
    ).first()
    
    if negocio:
        print(f"Actualizando negocio ID: {negocio.id}")
        print(f"Coordenadas antes: CX={negocio.cx}, CY={negocio.cy}")
        
        try:
            negocio.cx = Decimal('-86.2419055')
            negocio.cy = Decimal('15.1999999')
            negocio.nombrenego = 'Negocio Actualizado Directo'
            negocio.save()
            
            print(f"✅ Actualización directa exitosa")
            print(f"Coordenadas después: CX={negocio.cx}, CY={negocio.cy}")
            
            # Verificar en BD
            negocio_refresh = Negocio.objects.get(id=negocio.id)
            print(f"Verificación BD: CX={negocio_refresh.cx}, CY={negocio_refresh.cy}")
            
        except Exception as e:
            print(f"❌ Error en actualización directa: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    try:
        debug_confirmacion_problema()
        debug_modelo_negocio()
        debug_coordenadas()
        debug_actualizacion_directa()
        print("\n✅ Debug completado")
    except Exception as e:
        print(f"\n❌ Error durante debug: {str(e)}")
        import traceback
        traceback.print_exc() 
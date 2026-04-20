#!/usr/bin/env python
"""
Script de prueba final para verificar la corrección del problema de confirmación.
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

def test_confirmacion_final():
    """Prueba final de confirmación"""
    print("=== PRUEBA FINAL DE CONFIRMACIÓN ===")
    
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
            nombrenego='Negocio de Prueba Final',
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
        'nombrenego': 'Negocio Actualizado - Prueba Final',
        'direccion': 'Dirección Actualizada - Final',
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
                
                return True
            else:
                print(f"❌ Error en actualización: {data.get('mensaje')}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_coordenadas_final():
    """Verificar que las coordenadas se guardaron correctamente"""
    print("\n=== VERIFICACIÓN FINAL DE COORDENADAS ===")
    
    negocio = Negocio.objects.filter(
        empre='0301',
        rtm='114-03-23',
        expe='1151'
    ).first()
    
    if negocio:
        print(f"Negocio encontrado en BD:")
        print(f"  ID: {negocio.id}")
        print(f"  Empresa: {negocio.empre}")
        print(f"  RTM: {negocio.rtm}")
        print(f"  Expediente: {negocio.expe}")
        print(f"  Nombre: {negocio.nombrenego}")
        print(f"  Dirección: {negocio.direccion}")
        print(f"  CX: {negocio.cx}")
        print(f"  CY: {negocio.cy}")
        
        # Verificar que las coordenadas sean las esperadas
        if negocio.cx == Decimal('-86.2419055') and negocio.cy == Decimal('15.1999999'):
            print("✅ Coordenadas correctas en la base de datos")
            return True
        else:
            print("❌ Coordenadas incorrectas en la base de datos")
            return False
    else:
        print("❌ Negocio no encontrado en la base de datos")
        return False

def test_sin_confirmacion():
    """Probar sin confirmación para verificar que solicita confirmación"""
    print("\n=== PRUEBA SIN CONFIRMACIÓN ===")
    
    # Simular datos del formulario SIN confirmación
    form_data = {
        'empre': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'nombrenego': 'Negocio Actualizado - Sin Confirmación',
        'direccion': 'Dirección Actualizada - Sin Confirmación',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
        # Sin confirmar_actualizacion
    }
    
    print(f"Datos del formulario (sin confirmación):")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    request.headers = {'X-Requested-With': 'XMLHttpRequest'}
    
    print(f"\nSimulando petición sin confirmación...")
    
    try:
        # Llamar directamente a la vista
        response = maestro_negocios(request)
        
        print(f"Status de respuesta: {response.status_code}")
        print(f"Contenido de respuesta: {response.content.decode()}")
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content.decode())
            print(f"Respuesta JSON: {json.dumps(data, indent=2)}")
            
            if data.get('requiere_confirmacion') or data.get('existe'):
                print("✅ Correcto: Solicita confirmación")
                return True
            else:
                print("❌ Error: No solicita confirmación")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la simulación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        print("=== INICIANDO PRUEBAS FINALES ===")
        
        # Probar sin confirmación primero
        test_sin_confirmacion()
        
        # Probar con confirmación
        success = test_confirmacion_final()
        if success:
            verificar_coordenadas_final()
        
        print("\n✅ Todas las pruebas completadas")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc() 
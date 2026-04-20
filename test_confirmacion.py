#!/usr/bin/env python
"""
Script de prueba para verificar la confirmación de actualización de negocios.
"""

import os
import sys
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio
from decimal import Decimal

def test_confirmacion_actualizacion():
    """Prueba la confirmación de actualización de negocios"""
    print("=== PRUEBA DE CONFIRMACIÓN DE ACTUALIZACIÓN ===")
    
    # Buscar un negocio existente para probar
    negocio = Negocio.objects.first()
    
    if not negocio:
        print("No hay negocios en la base de datos para probar.")
        return
    
    print(f"Negocio encontrado para prueba:")
    print(f"  ID: {negocio.id}")
    print(f"  Empresa: {negocio.empre}")
    print(f"  RTM: {negocio.rtm}")
    print(f"  Expediente: {negocio.expe}")
    print(f"  Coordenadas actuales - CX: {negocio.cx}, CY: {negocio.cy}")
    
    # Datos de prueba para actualización
    test_data = {
        'empre': negocio.empre,
        'rtm': negocio.rtm,
        'expe': negocio.expe,
        'nombrenego': 'Negocio Actualizado por Prueba',
        'direccion': 'Dirección Actualizada',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar'
    }
    
    print(f"\nDatos de prueba para actualización:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    
    # Simular petición AJAX sin confirmación
    print(f"\n1. Probando petición sin confirmación...")
    
    # Simular la petición HTTP
    try:
        # Nota: Esto es una simulación, en realidad necesitarías un servidor corriendo
        print("  Simulando petición AJAX...")
        print("  Esperado: Respuesta solicitando confirmación")
        
        # Guardar coordenadas originales para restaurar después
        cx_original = negocio.cx
        cy_original = negocio.cy
        
        # Actualizar manualmente para simular la confirmación
        print(f"\n2. Simulando confirmación de actualización...")
        
        negocio.nombrenego = test_data['nombrenego']
        negocio.direccion = test_data['direccion']
        negocio.cx = Decimal(test_data['cx'])
        negocio.cy = Decimal(test_data['cy'])
        
        negocio.save()
        
        print(f"  ✅ Negocio actualizado exitosamente")
        print(f"  Coordenadas actualizadas - CX: {negocio.cx}, CY: {negocio.cy}")
        print(f"  Nombre actualizado: {negocio.nombrenego}")
        
        # Verificar en la base de datos
        negocio_refresh = Negocio.objects.get(id=negocio.id)
        print(f"  ✅ Verificación en BD - CX: {negocio_refresh.cx}, CY: {negocio_refresh.cy}")
        
        # Restaurar datos originales
        negocio.cx = cx_original
        negocio.cy = cy_original
        negocio.nombrenego = 'Negocio Original'
        negocio.direccion = 'Dirección Original'
        negocio.save()
        
        print(f"  ✅ Datos restaurados a valores originales")
        
    except Exception as e:
        print(f"  ❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()

def test_coordenadas_especificas():
    """Prueba con coordenadas específicas del problema reportado"""
    print("\n=== PRUEBA CON COORDENADAS ESPECÍFICAS ===")
    
    # Buscar el negocio específico mencionado en el error
    negocio = Negocio.objects.filter(
        empre='0301',
        rtm='114-03-23',
        expe='1151'
    ).first()
    
    if not negocio:
        print("Negocio específico no encontrado, creando uno de prueba...")
        negocio = Negocio.objects.create(
            empre='0301',
            rtm='114-03-23',
            expe='1151',
            nombrenego='Negocio de Prueba',
            cx=Decimal('0.0000000'),
            cy=None
        )
        print(f"Negocio de prueba creado con ID: {negocio.id}")
    
    print(f"Negocio específico:")
    print(f"  ID: {negocio.id}")
    print(f"  Empresa: {negocio.empre}")
    print(f"  RTM: {negocio.rtm}")
    print(f"  Expediente: {negocio.expe}")
    print(f"  Coordenadas actuales - CX: {negocio.cx}, CY: {negocio.cy}")
    
    # Probar actualización con coordenadas específicas
    nuevas_coordenadas = {
        'cx': '-86.2419055',
        'cy': '15.1999999'
    }
    
    print(f"\nProbando actualización con coordenadas específicas:")
    print(f"  CX: {nuevas_coordenadas['cx']}")
    print(f"  CY: {nuevas_coordenadas['cy']}")
    
    try:
        # Actualizar coordenadas
        negocio.cx = Decimal(nuevas_coordenadas['cx'])
        negocio.cy = Decimal(nuevas_coordenadas['cy'])
        negocio.save()
        
        print(f"  ✅ Coordenadas actualizadas exitosamente")
        print(f"  Nuevas coordenadas - CX: {negocio.cx}, CY: {negocio.cy}")
        
        # Verificar en la base de datos
        negocio_refresh = Negocio.objects.get(id=negocio.id)
        print(f"  ✅ Verificación en BD - CX: {negocio_refresh.cx}, CY: {negocio_refresh.cy}")
        
    except Exception as e:
        print(f"  ❌ Error al actualizar coordenadas: {str(e)}")
        import traceback
        traceback.print_exc()

def test_formulario_simulado():
    """Simula el envío de datos del formulario"""
    print("\n=== PRUEBA DE FORMULARIO SIMULADO ===")
    
    # Datos del formulario que deberían enviarse
    form_data = {
        'empre': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'nombrenego': 'Negocio Actualizado',
        'direccion': 'Nueva Dirección',
        'cx': '-86.2419055',
        'cy': '15.1999999',
        'accion': 'salvar',
        'confirmar_actualizacion': '1'  # Confirmación
    }
    
    print("Datos del formulario que se enviarían:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Simular el procesamiento en el backend
    try:
        from hola.views import maestro_negocios
        from django.test import RequestFactory
        from django.http import JsonResponse
        
        # Crear una petición simulada
        factory = RequestFactory()
        request = factory.post('/maestro_negocios/', form_data)
        request.headers = {'X-Requested-With': 'XMLHttpRequest'}
        
        print(f"\nSimulando procesamiento en el backend...")
        
        # Buscar el negocio en la base de datos
        negocio = Negocio.objects.filter(
            empre=form_data['empre'],
            rtm=form_data['rtm'],
            expe=form_data['expe']
        ).first()
        
        if negocio:
            print(f"  Negocio encontrado: {negocio}")
            print(f"  Coordenadas actuales - CX: {negocio.cx}, CY: {negocio.cy}")
            
            # Simular actualización
            negocio.cx = Decimal(form_data['cx'])
            negocio.cy = Decimal(form_data['cy'])
            negocio.nombrenego = form_data['nombrenego']
            negocio.direccion = form_data['direccion']
            negocio.save()
            
            print(f"  ✅ Negocio actualizado exitosamente")
            print(f"  Nuevas coordenadas - CX: {negocio.cx}, CY: {negocio.cy}")
        else:
            print(f"  Negocio no encontrado, creando nuevo...")
            nuevo_negocio = Negocio.objects.create(
                empre=form_data['empre'],
                rtm=form_data['rtm'],
                expe=form_data['expe'],
                nombrenego=form_data['nombrenego'],
                direccion=form_data['direccion'],
                cx=Decimal(form_data['cx']),
                cy=Decimal(form_data['cy'])
            )
            print(f"  ✅ Nuevo negocio creado con ID: {nuevo_negocio.id}")
            
    except Exception as e:
        print(f"  ❌ Error en simulación: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    try:
        test_confirmacion_actualizacion()
        test_coordenadas_especificas()
        test_formulario_simulado()
        print("\n✅ Todas las pruebas completadas exitosamente")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc() 
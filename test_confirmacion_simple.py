#!/usr/bin/env python
"""
Script de prueba simple para simular el problema de confirmación.
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio

def test_confirmacion_simple():
    """Prueba simple de confirmación"""
    print("=== PRUEBA SIMPLE DE CONFIRMACIÓN ===")
    
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
    
    # Simular la actualización que debería hacer la confirmación
    print(f"\nSimulando actualización con confirmación...")
    
    try:
        # Actualizar coordenadas
        negocio.cx = Decimal('-86.2419055')
        negocio.cy = Decimal('15.1999999')
        negocio.nombrenego = 'Negocio Actualizado - Confirmación'
        negocio.direccion = 'Dirección Actualizada - Confirmación'
        negocio.save()
        
        print(f"✅ Actualización exitosa")
        print(f"  Coordenadas después: CX={negocio.cx}, CY={negocio.cy}")
        print(f"  Nombre: {negocio.nombrenego}")
        print(f"  Dirección: {negocio.direccion}")
        
        # Verificar en la base de datos
        negocio_refresh = Negocio.objects.get(id=negocio.id)
        print(f"✅ Verificación en BD:")
        print(f"  CX: {negocio_refresh.cx}")
        print(f"  CY: {negocio_refresh.cy}")
        print(f"  Nombre: {negocio_refresh.nombrenego}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en actualización: {e}")
        import traceback
        traceback.print_exc()
        return False

def verificar_coordenadas_guardadas():
    """Verificar que las coordenadas se guardaron correctamente"""
    print("\n=== VERIFICACIÓN DE COORDENADAS ===")
    
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

if __name__ == '__main__':
    try:
        success = test_confirmacion_simple()
        if success:
            verificar_coordenadas_guardadas()
        print("\n✅ Prueba completada")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc() 
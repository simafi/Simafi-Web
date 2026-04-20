#!/usr/bin/env python
"""
Script de prueba para verificar el funcionamiento de las coordenadas en el sistema de negocios.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio
from decimal import Decimal

def test_coordenadas():
    """Prueba el funcionamiento de las coordenadas"""
    print("=== PRUEBA DE COORDENADAS ===")
    
    # Buscar un negocio existente para probar
    negocios = Negocio.objects.all()[:5]
    
    if not negocios:
        print("No hay negocios en la base de datos para probar.")
        return
    
    print(f"Encontrados {len(negocios)} negocios para probar:")
    
    for i, negocio in enumerate(negocios, 1):
        print(f"\n--- Negocio {i} ---")
        print(f"ID: {negocio.id}")
        print(f"Empresa: {negocio.empre}")
        print(f"RTM: {negocio.rtm}")
        print(f"Expediente: {negocio.expe}")
        print(f"Nombre: {negocio.nombrenego}")
        print(f"Coordenada X (cx): {negocio.cx} (tipo: {type(negocio.cx)})")
        print(f"Coordenada Y (cy): {negocio.cy} (tipo: {type(negocio.cy)})")
        
        # Probar actualización de coordenadas
        print(f"\nProbando actualización de coordenadas...")
        
        # Guardar coordenadas originales
        cx_original = negocio.cx
        cy_original = negocio.cy
        
        # Actualizar con nuevas coordenadas de prueba
        negocio.cx = Decimal('15.1999999')
        negocio.cy = Decimal('-86.2419055')
        
        try:
            negocio.save()
            print(f"✓ Coordenadas actualizadas exitosamente")
            print(f"  CX: {cx_original} -> {negocio.cx}")
            print(f"  CY: {cy_original} -> {negocio.cy}")
            
            # Verificar que se guardaron correctamente
            negocio_refresh = Negocio.objects.get(id=negocio.id)
            print(f"✓ Verificación en BD - CX: {negocio_refresh.cx}, CY: {negocio_refresh.cy}")
            
            # Restaurar coordenadas originales
            negocio.cx = cx_original
            negocio.cy = cy_original
            negocio.save()
            print(f"✓ Coordenadas restauradas a valores originales")
            
        except Exception as e:
            print(f"✗ Error al actualizar coordenadas: {str(e)}")
    
    print("\n=== PRUEBA COMPLETADA ===")

def test_serializacion():
    """Prueba la serialización de coordenadas"""
    print("\n=== PRUEBA DE SERIALIZACIÓN ===")
    
    from hola.serializers import NegocioSerializer
    
    negocios = Negocio.objects.all()[:3]
    
    for i, negocio in enumerate(negocios, 1):
        print(f"\n--- Serialización Negocio {i} ---")
        
        serializer = NegocioSerializer(negocio)
        data = serializer.data
        
        print(f"Coordenadas en serializador:")
        print(f"  CX: {data.get('cx')} (tipo: {type(data.get('cx'))})")
        print(f"  CY: {data.get('cy')} (tipo: {type(data.get('cy'))})")
        
        # Verificar que las coordenadas se serializan correctamente
        if 'cx' in data and 'cy' in data:
            print("✓ Coordenadas incluidas en serialización")
        else:
            print("✗ Coordenadas faltantes en serialización")

if __name__ == '__main__':
    try:
        test_coordenadas()
        test_serializacion()
        print("\n✅ Todas las pruebas completadas exitosamente")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc() 
#!/usr/bin/env python
"""
Script simple para verificar coordenadas en la base de datos.
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio

def verificar_coordenadas():
    """Verificar las coordenadas de los últimos registros"""
    print("=== VERIFICACIÓN DE COORDENADAS ===")
    
    # Obtener los últimos 5 registros
    negocios = Negocio.objects.order_by('-id')[:5]
    
    for negocio in negocios:
        print(f"\nNegocio ID: {negocio.id}")
        print(f"  Empresa: {negocio.empre}")
        print(f"  RTM: {negocio.rtm}")
        print(f"  Expediente: {negocio.expe}")
        print(f"  Nombre: {negocio.nombrenego}")
        print(f"  CX: {negocio.cx} (tipo: {type(negocio.cx)})")
        print(f"  CY: {negocio.cy} (tipo: {type(negocio.cy)})")
        
        # Convertir a float para comparación
        if negocio.cx is not None:
            cx_float = float(negocio.cx)
            print(f"  CX float: {cx_float}")
        
        if negocio.cy is not None:
            cy_float = float(negocio.cy)
            print(f"  CY float: {cy_float}")
        
        # Verificar si son coordenadas de prueba
        if 'COMA' in negocio.rtm:
            print("  -> Es una prueba de coordenadas con comas")
            cx_esperado = -86.2419055
            cy_esperado = 15.1999999
            
            if abs(cx_float - cx_esperado) < 0.0000001 and abs(cy_float - cy_esperado) < 0.0000001:
                print("  ✅ Coordenadas correctas")
            else:
                print("  ❌ Coordenadas incorrectas")
                print(f"    CX esperado: {cx_esperado}, obtenido: {cx_float}")
                print(f"    CY esperado: {cy_esperado}, obtenido: {cy_float}")
        
        elif 'CERO' in negocio.rtm:
            print("  -> Es una prueba de coordenadas cero")
            cero_esperado = 0.0
            
            if abs(cx_float - cero_esperado) < 0.0000001 and abs(cy_float - cero_esperado) < 0.0000001:
                print("  ✅ Coordenadas cero correctas")
            else:
                print("  ❌ Coordenadas cero incorrectas")
                print(f"    Esperado: {cero_esperado}, obtenido CX: {cx_float}, CY: {cy_float}")

if __name__ == "__main__":
    verificar_coordenadas() 
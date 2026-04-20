#!/usr/bin/env python3
"""
Script para probar el sistema de cálculo interactivo
"""

import requests
import re

def test_calculation_system():
    """Probar el sistema de cálculo interactivo"""
    url = "http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Verificar que el archivo JavaScript se esté cargando
            js_loaded = 'declaracion_volumen_interactivo.js' in content
            print(f"JavaScript cargado: {js_loaded}")
            
            # Verificar que la función de verificación esté presente
            verification_function = 'verificarSistemaCalculo' in content
            print(f"Función de verificación presente: {verification_function}")
            
            # Verificar que la clase DeclaracionVolumenInteractivo esté definida
            class_defined = 'DeclaracionVolumenInteractivo' in content
            print(f"Clase DeclaracionVolumenInteractivo definida: {class_defined}")
            
            # Buscar el script de verificación
            if 'verificarSistemaCalculo' in content:
                print("\n✅ Sistema de verificación encontrado en el template")
            else:
                print("\n❌ Sistema de verificación NO encontrado en el template")
                
            if js_loaded and verification_function and class_defined:
                print("\n✅ CORRECCIÓN EXITOSA: El sistema de cálculo interactivo está configurado correctamente")
            else:
                print("\n❌ PROBLEMA PERSISTE: El sistema no está configurado correctamente")
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_calculation_system()



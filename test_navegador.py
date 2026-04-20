#!/usr/bin/env python3
"""
Test para verificar si hay problemas en el navegador
"""

import requests
import re

def test_navegador():
    """Test para verificar si hay problemas en el navegador"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            print("\n=== TEST DE NAVEGADOR ===")
            
            # Buscar mensajes de error en el JavaScript
            print("1. Buscando mensajes de error en JavaScript...")
            errores_js = [
                "utiliza un formato",
                "formato que coincida",
                "coincida con el solicitado",
                "cálculo automático de impuesto activado",
                "impuesto activado"
            ]
            
            for error in errores_js:
                if error in content:
                    print(f"   ENCONTRADO: {error}")
                else:
                    print(f"   NO ENCONTRADO: {error}")
            
            # Buscar mensajes de validación en general
            print("\n2. Buscando mensajes de validación...")
            mensajes_validacion = [
                "formato",
                "coincida",
                "solicitado",
                "cálculo automático",
                "impuesto activado",
                "utiliza"
            ]
            
            for mensaje in mensajes_validacion:
                if mensaje in content:
                    print(f"   ENCONTRADO: {mensaje}")
                else:
                    print(f"   NO ENCONTRADO: {mensaje}")
            
            # Buscar alertas en el JavaScript
            print("\n3. Buscando alertas en JavaScript...")
            alertas = re.findall(r'alert\([^)]+\)', content)
            if alertas:
                print(f"   ALERTAS ENCONTRADAS: {len(alertas)}")
                for alerta in alertas[:5]:  # Mostrar solo las primeras 5
                    print(f"     - {alerta}")
            else:
                print("   NO HAY ALERTAS ENCONTRADAS")
            
            # Buscar mensajes de error en general
            print("\n4. Buscando mensajes de error en general...")
            mensajes_error = re.findall(r'console\.(error|warn)\([^)]+\)', content)
            if mensajes_error:
                print(f"   MENSAJES DE ERROR: {len(mensajes_error)}")
                for mensaje in mensajes_error[:5]:  # Mostrar solo los primeros 5
                    print(f"     - {mensaje}")
            else:
                print("   NO HAY MENSAJES DE ERROR ENCONTRADOS")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_navegador()



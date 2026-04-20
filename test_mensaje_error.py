#!/usr/bin/env python3
"""
Test para buscar el mensaje de error específico
"""

import requests
import re

def test_mensaje_error():
    """Test para buscar el mensaje de error específico"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            print("\n=== BUSCANDO MENSAJE DE ERROR ===")
            
            # Buscar el mensaje específico
            mensaje_exacto = "utiliza un formato que coincida con el solicitado cálculo automático de impuesto activado"
            if mensaje_exacto in content:
                print(f"   ENCONTRADO: {mensaje_exacto}")
            else:
                print(f"   NO ENCONTRADO: {mensaje_exacto}")
            
            # Buscar variaciones del mensaje
            variaciones = [
                "utiliza un formato",
                "formato que coincida",
                "coincida con el solicitado",
                "cálculo automático de impuesto activado",
                "impuesto activado"
            ]
            
            for variacion in variaciones:
                if variacion in content:
                    print(f"   ENCONTRADO: {variacion}")
                else:
                    print(f"   NO ENCONTRADO: {variacion}")
            
            # Buscar mensajes de validación en general
            print("\n=== BUSCANDO MENSAJES DE VALIDACIÓN ===")
            mensajes_validacion = [
                "formato",
                "coincida",
                "solicitado",
                "cálculo automático",
                "impuesto activado",
                "utiliza",
                "formato que",
                "coincida con",
                "solicitado cálculo"
            ]
            
            for mensaje in mensajes_validacion:
                if mensaje in content:
                    print(f"   ENCONTRADO: {mensaje}")
                else:
                    print(f"   NO ENCONTRADO: {mensaje}")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_mensaje_error()



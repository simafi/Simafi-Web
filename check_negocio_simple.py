#!/usr/bin/env python3
"""
Script simple para verificar el negocio
"""

import requests

def check_negocio_simple():
    """Verificar el negocio usando la API"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar mensajes de error
            if 'No se encontró el negocio' in content:
                print("PROBLEMA: No se encontró el negocio en la base de datos")
                print("SOLUCION: Necesitamos crear el negocio o usar datos existentes")
                
                # Buscar si hay algún negocio en la base de datos
                print("\nBuscando negocios existentes...")
                # Aquí podríamos hacer una búsqueda más amplia
                
            else:
                print("Negocio encontrado correctamente")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_negocio_simple()



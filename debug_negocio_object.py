#!/usr/bin/env python3
"""
Script para debuggear el objeto negocio
"""

import requests

def debug_negocio_object():
    """Debuggear el objeto negocio"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar información del negocio en el HTML
            if 'Negocio Actualizado - Prueba Final' in content:
                print("Negocio encontrado: 'Negocio Actualizado - Prueba Final'")
                
                # Buscar valores específicos en todo el HTML
                rtm_present = '114-03-23' in content
                expe_present = '1151' in content
                
                print(f"RTM (114-03-23) presente en todo el HTML: {rtm_present}")
                print(f"EXPE (1151) presente en todo el HTML: {expe_present}")
                
                if rtm_present and expe_present:
                    print("Los valores están presentes en el HTML, pero no en los campos")
                    print("Esto sugiere que el problema está en el template o en la renderización")
                else:
                    print("Los valores no están presentes en el HTML")
                    print("Esto sugiere que el objeto negocio no tiene los valores correctos")
                    
            else:
                print("Negocio no encontrado en el HTML")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_negocio_object()



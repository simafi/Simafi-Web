#!/usr/bin/env python3
"""
Script detallado para debuggear el problema de RTM y EXPE
"""

import requests
import json
import re

def debug_detailed():
    """Debug detallado del problema"""
    base_url = "http://localhost:8080"
    url = f"{base_url}/tributario/declaracion-volumen/?rtm=123456&expe=789012"
    
    print(f"Probando URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar la sección "Información Básica"
            basic_info_match = re.search(r'Información Básica.*?</div>', content, re.DOTALL)
            if basic_info_match:
                basic_info_section = basic_info_match.group(0)
                print("\n=== SECCIÓN INFORMACIÓN BÁSICA ===")
                print(basic_info_section[:1000])  # Primeros 1000 caracteres
                
                # Buscar campos RTM y EXPE en esta sección
                rtm_in_basic = '123456' in basic_info_section
                expe_in_basic = '789012' in basic_info_section
                
                print(f"\nRTM en sección básica: {rtm_in_basic}")
                print(f"EXPE en sección básica: {expe_in_basic}")
                
                # Buscar campos del formulario específicamente
                rtm_field_match = re.search(r'<input[^>]*name="rtm"[^>]*>', basic_info_section)
                expe_field_match = re.search(r'<input[^>]*name="expe"[^>]*>', basic_info_section)
                
                if rtm_field_match:
                    print(f"\nCampo RTM encontrado: {rtm_field_match.group(0)}")
                else:
                    print("\n❌ Campo RTM NO encontrado en la sección")
                    
                if expe_field_match:
                    print(f"\nCampo EXPE encontrado: {expe_field_match.group(0)}")
                else:
                    print("\n❌ Campo EXPE NO encontrado en la sección")
                    
            else:
                print("❌ Sección 'Información Básica' no encontrada")
                
        else:
            print(f"❌ Error al cargar la página: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_detailed()




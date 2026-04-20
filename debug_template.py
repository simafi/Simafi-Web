#!/usr/bin/env python3
"""
Script para debuggear el template
"""

import requests
import re

def debug_template():
    """Debug del template"""
    url = "http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar todos los campos input en la sección de información básica
            basic_info_match = re.search(r'Información Básica.*?</div>', content, re.DOTALL)
            if basic_info_match:
                basic_info_section = basic_info_match.group(0)
                
                # Buscar todos los campos input
                input_matches = re.findall(r'<input[^>]*>', basic_info_section)
                print("\n=== TODOS LOS CAMPOS INPUT EN INFORMACIÓN BÁSICA ===")
                for i, input_tag in enumerate(input_matches):
                    print(f"{i+1}. {input_tag}")
                
                # Buscar específicamente los campos que necesito
                rtm_inputs = [tag for tag in input_matches if 'name="rtm"' in tag]
                expe_inputs = [tag for tag in input_matches if 'name="expe"' in tag]
                idneg_inputs = [tag for tag in input_matches if 'name="idneg"' in tag]
                
                print(f"\nCampos RTM encontrados: {len(rtm_inputs)}")
                for tag in rtm_inputs:
                    print(f"  {tag}")
                    
                print(f"\nCampos EXPE encontrados: {len(expe_inputs)}")
                for tag in expe_inputs:
                    print(f"  {tag}")
                    
                print(f"\nCampos IDNEG encontrados: {len(idneg_inputs)}")
                for tag in idneg_inputs:
                    print(f"  {tag}")
                    
            else:
                print("❌ Sección 'Información Básica' no encontrada")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_template()




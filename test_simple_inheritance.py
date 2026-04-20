#!/usr/bin/env python3
"""
Script simple para probar la herencia de valores
"""

import requests
import re

def test_simple_inheritance():
    """Probar la herencia de valores"""
    url = "http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar la seccion "Informacion Basica"
            basic_info_match = re.search(r'Informacion Basica.*?</div>', content, re.DOTALL)
            if basic_info_match:
                basic_info_section = basic_info_match.group(0)
                
                # Buscar los campos especificos
                rtm_field_match = re.search(r'<input[^>]*name="rtm"[^>]*value="([^"]*)"[^>]*>', basic_info_section)
                expe_field_match = re.search(r'<input[^>]*name="expe"[^>]*value="([^"]*)"[^>]*>', basic_info_section)
                idneg_field_match = re.search(r'<input[^>]*name="idneg"[^>]*value="([^"]*)"[^>]*>', basic_info_section)
                
                print("\n=== CAMPOS EN INFORMACION BASICA ===")
                if rtm_field_match:
                    print(f"Campo RTM encontrado: {rtm_field_match.group(0)}")
                    print(f"Valor: {rtm_field_match.group(1)}")
                else:
                    print("Campo RTM NO encontrado")
                    
                if expe_field_match:
                    print(f"Campo EXPE encontrado: {expe_field_match.group(0)}")
                    print(f"Valor: {expe_field_match.group(1)}")
                else:
                    print("Campo EXPE NO encontrado")
                    
                if idneg_field_match:
                    print(f"Campo IDNEG encontrado: {idneg_field_match.group(0)}")
                    print(f"Valor: {idneg_field_match.group(1)}")
                else:
                    print("Campo IDNEG NO encontrado")
                
                # Verificar que los valores esten presentes
                rtm_present = '114-03-23' in basic_info_section
                expe_present = '1151' in basic_info_section
                
                print(f"\nRTM (114-03-23) presente: {rtm_present}")
                print(f"EXPE (1151) presente: {expe_present}")
                
                if rtm_present and expe_present:
                    print("\nCORRECCION EXITOSA: Los campos heredan correctamente los valores")
                    print("La declaracion ahora se podra guardar correctamente")
                else:
                    print("\nPROBLEMA PERSISTE: Los campos no heredan los valores")
                    
            else:
                print("Seccion 'Informacion Basica' no encontrada")
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple_inheritance()



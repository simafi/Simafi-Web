#!/usr/bin/env python3
"""
Script para probar la URL específica mencionada
"""

import requests
import re

def test_specific_url():
    """Probar la URL específica"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar la seccion de informacion basica
            if 'Informacion Basica' in content:
                print("Seccion 'Informacion Basica' encontrada")
                
                # Buscar los campos especificos
                rtm_fields = re.findall(r'<input[^>]*name="rtm"[^>]*>', content)
                expe_fields = re.findall(r'<input[^>]*name="expe"[^>]*>', content)
                idneg_fields = re.findall(r'<input[^>]*name="idneg"[^>]*>', content)
                
                print(f"\nCampos RTM encontrados: {len(rtm_fields)}")
                for i, field in enumerate(rtm_fields):
                    print(f"  {i+1}. {field}")
                    
                print(f"\nCampos EXPE encontrados: {len(expe_fields)}")
                for i, field in enumerate(expe_fields):
                    print(f"  {i+1}. {field}")
                    
                print(f"\nCampos IDNEG encontrados: {len(idneg_fields)}")
                for i, field in enumerate(idneg_fields):
                    print(f"  {i+1}. {field}")
                
                # Verificar si los valores estan presentes
                rtm_present = '114-03-23' in content
                expe_present = '1151' in content
                
                print(f"\nRTM (114-03-23) presente en todo el HTML: {rtm_present}")
                print(f"EXPE (1151) presente en todo el HTML: {expe_present}")
                
                # Buscar especificamente en la seccion de informacion basica
                basic_info_start = content.find('Informacion Basica')
                if basic_info_start != -1:
                    basic_info_section = content[basic_info_start:basic_info_start + 3000]
                    print(f"\nSeccion Informacion Basica (primeros 1000 caracteres):")
                    print(basic_info_section[:1000])
                    
                    rtm_in_section = '114-03-23' in basic_info_section
                    expe_in_section = '1151' in basic_info_section
                    
                    print(f"\nRTM en seccion basica: {rtm_in_section}")
                    print(f"EXPE en seccion basica: {expe_in_section}")
                    
                    if rtm_in_section and expe_in_section:
                        print("\nCORRECCION EXITOSA: Los campos heredan correctamente los valores")
                    else:
                        print("\nPROBLEMA PERSISTE: Los campos no heredan los valores")
                        print("Necesitamos revisar mas a fondo")
                    
            else:
                print("Seccion 'Informacion Basica' NO encontrada")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_specific_url()



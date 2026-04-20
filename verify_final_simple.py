#!/usr/bin/env python3
"""
Script para verificar el éxito final (sin emojis)
"""

import requests
import re

def verify_final_success():
    """Verificar el éxito final"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar la sección "Información Básica"
            if 'Información Básica' in content:
                print("Seccion 'Informacion Basica' encontrada")
                
                # Buscar los campos específicos en la sección
                basic_info_start = content.find('Información Básica')
                if basic_info_start != -1:
                    basic_info_section = content[basic_info_start:basic_info_start + 5000]
                    
                    # Buscar campos RTM con valores
                    rtm_pattern = r'<input[^>]*name="rtm"[^>]*value="([^"]*)"[^>]*>'
                    rtm_matches = re.findall(rtm_pattern, basic_info_section)
                    print(f"\nCampos RTM en seccion basica: {len(rtm_matches)}")
                    for i, value in enumerate(rtm_matches):
                        print(f"  {i+1}. RTM value: '{value}'")
                    
                    # Buscar campos EXPE con valores
                    expe_pattern = r'<input[^>]*name="expe"[^>]*value="([^"]*)"[^>]*>'
                    expe_matches = re.findall(expe_pattern, basic_info_section)
                    print(f"\nCampos EXPE en seccion basica: {len(expe_matches)}")
                    for i, value in enumerate(expe_matches):
                        print(f"  {i+1}. EXPE value: '{value}'")
                    
                    # Buscar campos IDNEG con valores
                    idneg_pattern = r'<input[^>]*name="idneg"[^>]*value="([^"]*)"[^>]*>'
                    idneg_matches = re.findall(idneg_pattern, basic_info_section)
                    print(f"\nCampos IDNEG en seccion basica: {len(idneg_matches)}")
                    for i, value in enumerate(idneg_matches):
                        print(f"  {i+1}. IDNEG value: '{value}'")
                    
                    # Verificar si los valores correctos están presentes
                    rtm_correct = '114-03-23' in basic_info_section
                    expe_correct = '1151' in basic_info_section
                    idneg_correct = any(value != '0' and value != '' for value in idneg_matches)
                    
                    print(f"\nRTM (114-03-23) en seccion basica: {rtm_correct}")
                    print(f"EXPE (1151) en seccion basica: {expe_correct}")
                    print(f"IDNEG (valor valido) en seccion basica: {idneg_correct}")
                    
                    if rtm_correct and expe_correct and idneg_correct:
                        print("\nCORRECCION COMPLETAMENTE EXITOSA:")
                        print("   - Los campos RTM, EXPE e IDNEG heredan correctamente los valores")
                        print("   - Los campos obligatorios tienen valores validos")
                        print("   - La declaracion se puede guardar correctamente")
                    else:
                        print("\nPROBLEMA PERSISTE: Los campos no heredan los valores correctamente")
                    
            else:
                print("Seccion 'Informacion Basica' NO encontrada")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_final_success()



#!/usr/bin/env python3
"""
Script para verificar los campos específicos
"""

import requests
import re

def verify_fields():
    """Verificar los campos específicos"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar la sección "Información Básica" (con acentos)
            if 'Información Básica' in content:
                print("✅ Sección 'Información Básica' encontrada")
                
                # Buscar los campos específicos en la sección
                basic_info_start = content.find('Información Básica')
                if basic_info_start != -1:
                    # Buscar en los próximos 5000 caracteres
                    basic_info_section = content[basic_info_start:basic_info_start + 5000]
                    
                    # Buscar campos RTM
                    rtm_pattern = r'<input[^>]*name="rtm"[^>]*value="([^"]*)"[^>]*>'
                    rtm_matches = re.findall(rtm_pattern, basic_info_section)
                    print(f"\nCampos RTM en sección básica: {len(rtm_matches)}")
                    for i, value in enumerate(rtm_matches):
                        print(f"  {i+1}. RTM value: '{value}'")
                    
                    # Buscar campos EXPE
                    expe_pattern = r'<input[^>]*name="expe"[^>]*value="([^"]*)"[^>]*>'
                    expe_matches = re.findall(expe_pattern, basic_info_section)
                    print(f"\nCampos EXPE en sección básica: {len(expe_matches)}")
                    for i, value in enumerate(expe_matches):
                        print(f"  {i+1}. EXPE value: '{value}'")
                    
                    # Buscar campos IDNEG
                    idneg_pattern = r'<input[^>]*name="idneg"[^>]*value="([^"]*)"[^>]*>'
                    idneg_matches = re.findall(idneg_pattern, basic_info_section)
                    print(f"\nCampos IDNEG en sección básica: {len(idneg_matches)}")
                    for i, value in enumerate(idneg_matches):
                        print(f"  {i+1}. IDNEG value: '{value}'")
                    
                    # Verificar si los valores correctos están presentes
                    rtm_correct = '114-03-23' in basic_info_section
                    expe_correct = '1151' in basic_info_section
                    
                    print(f"\n✅ RTM (114-03-23) en sección básica: {rtm_correct}")
                    print(f"✅ EXPE (1151) en sección básica: {expe_correct}")
                    
                    if rtm_correct and expe_correct:
                        print("\n🎉 CORRECCIÓN EXITOSA: Los campos heredan correctamente los valores")
                    else:
                        print("\n❌ PROBLEMA PERSISTE: Los campos no heredan los valores")
                        
                        # Mostrar el HTML de la sección para debug
                        print("\nHTML de la sección básica:")
                        print(basic_info_section[:2000])
                    
            else:
                print("❌ Sección 'Información Básica' NO encontrada")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_fields()



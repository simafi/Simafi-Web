#!/usr/bin/env python3
"""
Script para probar la corrección final de los campos RTM, EXPE e ID
"""

import requests
import re

def test_correction_final():
    """Probar la corrección final"""
    url = "http://localhost:8080/tributario/declaracion-volumen/?rtm=123456&expe=789012"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar la sección "Información Básica"
            basic_info_match = re.search(r'Información Básica.*?</div>', content, re.DOTALL)
            if basic_info_match:
                basic_info_section = basic_info_match.group(0)
                print("\n=== SECCIÓN INFORMACIÓN BÁSICA ===")
                print(basic_info_section[:1500])  # Primeros 1500 caracteres
                
                # Verificar que los valores estén presentes
                rtm_present = '123456' in basic_info_section
                expe_present = '789012' in basic_info_section
                
                print(f"\nRTM (123456) presente: {rtm_present}")
                print(f"EXPE (789012) presente: {expe_present}")
                
                # Buscar campos específicos
                rtm_field_match = re.search(r'<input[^>]*name="rtm"[^>]*value="123456"[^>]*>', basic_info_section)
                expe_field_match = re.search(r'<input[^>]*name="expe"[^>]*value="789012"[^>]*>', basic_info_section)
                
                if rtm_field_match:
                    print(f"✅ Campo RTM encontrado: {rtm_field_match.group(0)}")
                else:
                    print("❌ Campo RTM NO encontrado con valor correcto")
                    
                if expe_field_match:
                    print(f"✅ Campo EXPE encontrado: {expe_field_match.group(0)}")
                else:
                    print("❌ Campo EXPE NO encontrado con valor correcto")
                
                if rtm_present and expe_present:
                    print("\n✅ CORRECCIÓN EXITOSA: Los campos RTM y EXPE se llenan correctamente")
                else:
                    print("\n❌ PROBLEMA PERSISTE: Los campos no se llenan correctamente")
                    
            else:
                print("❌ Sección 'Información Básica' no encontrada")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_correction_final()




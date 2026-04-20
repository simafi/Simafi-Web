#!/usr/bin/env python3
"""
Script para verificar el contenido del template
"""

import os

def check_template():
    """Verificar el contenido del template"""
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar la sección de información básica
        if 'Información Básica' in content:
            start = content.find('Información Básica')
            end = content.find('</div>', start + 2000)
            section = content[start:end] if end > start else content[start:start+2000]
            
            print("=== SECCIÓN INFORMACIÓN BÁSICA EN EL TEMPLATE ===")
            print(section)
            
            # Verificar si mis campos personalizados están presentes
            if 'idneg_field' in section:
                print("\n✅ Campo idneg_field encontrado en el template")
            else:
                print("\n❌ Campo idneg_field NO encontrado en el template")
                
            if 'rtm_field' in section:
                print("✅ Campo rtm_field encontrado en el template")
            else:
                print("❌ Campo rtm_field NO encontrado en el template")
                
            if 'expe_field' in section:
                print("✅ Campo expe_field encontrado en el template")
            else:
                print("❌ Campo expe_field NO encontrado en el template")
        else:
            print("❌ Sección 'Información Básica' no encontrada en el template")
    else:
        print(f"❌ Template no encontrado en: {template_path}")

if __name__ == "__main__":
    check_template()




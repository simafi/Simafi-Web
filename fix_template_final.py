#!/usr/bin/env python3
"""
Script para corregir el template definitivamente
"""

def fix_template_final():
    """Corregir el template definitivamente"""
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Reemplazar todos los filtros problemáticos
        content = content.replace('{{ negocio.rtm|default:rtm }}', '{{ negocio.rtm }}')
        content = content.replace('{{ negocio.expe|default:expe }}', '{{ negocio.expe }}')
        
        # Guardar el archivo corregido
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Template corregido exitosamente")
        
        # Verificar que los cambios se aplicaron
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        rtm_fixed = '{{ negocio.rtm|default:rtm }}' not in content
        expe_fixed = '{{ negocio.expe|default:expe }}' not in content
        
        print(f"RTM corregido: {rtm_fixed}")
        print(f"EXPE corregido: {expe_fixed}")
        
        if rtm_fixed and expe_fixed:
            print("CORRECCION EXITOSA: Template corregido definitivamente")
        else:
            print("PROBLEMA PERSISTE: Template no se corrigió correctamente")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_template_final()



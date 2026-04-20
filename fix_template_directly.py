#!/usr/bin/env python3
"""
Script para corregir el template directamente
"""

def fix_template_directly():
    """Corregir el template directamente"""
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Reemplazar los campos del formulario Django por campos HTML directos
        # Campo IDNEG
        content = content.replace(
            '{{ form.idneg }}',
            '<input type="number" id="idneg_field" name="idneg" class="form-control" value="{{ negocio.id }}" readonly style="background-color: #f8f9fa; border: 1px solid #dee2e6;">'
        )
        
        # Campo RTM
        content = content.replace(
            '{{ form.rtm }}',
            '<input type="text" id="rtm_field" name="rtm" class="form-control" value="{{ negocio.rtm|default:rtm }}" readonly style="background-color: #f8f9fa; border: 1px solid #dee2e6;">'
        )
        
        # Campo EXPE
        content = content.replace(
            '{{ form.expe }}',
            '<input type="text" id="expe_field" name="expe" class="form-control" value="{{ negocio.expe|default:expe }}" readonly style="background-color: #f8f9fa; border: 1px solid #dee2e6;">'
        )
        
        # Guardar el archivo corregido
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Template corregido exitosamente")
        
        # Verificar que los cambios se aplicaron
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        rtm_fields = content.count('value="{{ negocio.rtm|default:rtm }}"')
        expe_fields = content.count('value="{{ negocio.expe|default:expe }}"')
        idneg_fields = content.count('value="{{ negocio.id }}"')
        
        print(f"Campos RTM con negocio.rtm|default:rtm: {rtm_fields}")
        print(f"Campos EXPE con negocio.expe|default:expe: {expe_fields}")
        print(f"Campos IDNEG con negocio.id: {idneg_fields}")
        
        if rtm_fields > 0 and expe_fields > 0 and idneg_fields > 0:
            print("CORRECCION EXITOSA: Template ahora usa negocio.rtm, negocio.expe, negocio.id")
        else:
            print("PROBLEMA PERSISTE: Template no se corrigió correctamente")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_template_directly()



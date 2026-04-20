#!/usr/bin/env python3
"""
Script para verificar el contenido del template
"""

def check_template_content():
    """Verificar el contenido del template"""
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar la sección de información básica
        if 'Información Básica' in content:
            print("Seccion 'Informacion Basica' encontrada en template")
            
            # Buscar los campos específicos
            rtm_fields = content.count('value="{{ negocio.rtm|default:rtm }}"')
            expe_fields = content.count('value="{{ negocio.expe|default:expe }}"')
            idneg_fields = content.count('value="{{ negocio.id }}"')
            
            print(f"Campos RTM con negocio.rtm|default:rtm: {rtm_fields}")
            print(f"Campos EXPE con negocio.expe|default:expe: {expe_fields}")
            print(f"Campos IDNEG con negocio.id: {idneg_fields}")
            
            # Buscar si hay campos usando form.rtm
            form_rtm_fields = content.count('{{ form.rtm }}')
            form_expe_fields = content.count('{{ form.expe }}')
            form_idneg_fields = content.count('{{ form.idneg }}')
            
            print(f"Campos RTM con form.rtm: {form_rtm_fields}")
            print(f"Campos EXPE con form.expe: {form_expe_fields}")
            print(f"Campos IDNEG con form.idneg: {form_idneg_fields}")
            
            if rtm_fields > 0 and expe_fields > 0 and idneg_fields > 0:
                print("Template CORRECTO: Usa negocio.rtm, negocio.expe, negocio.id")
            else:
                print("Template INCORRECTO: No usa negocio.rtm, negocio.expe, negocio.id")
                
        else:
            print("Seccion 'Informacion Basica' NO encontrada en template")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_template_content()



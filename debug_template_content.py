#!/usr/bin/env python3
"""
Script para debuggear el contenido del template
"""

def debug_template_content():
    """Debuggear el contenido del template"""
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar específicamente los campos
        ajuste_base_found = 'hidden_ajuste_base' in content
        ajuste_impuesto_found = 'hidden_ajuste_impuesto' in content
        
        print(f"hidden_ajuste_base encontrado: {ajuste_base_found}")
        print(f"hidden_ajuste_impuesto encontrado: {ajuste_impuesto_found}")
        
        # Buscar el contexto alrededor de estos campos
        if ajuste_base_found:
            start = content.find('hidden_ajuste_base')
            context = content[start-50:start+100]
            print(f"\nContexto de hidden_ajuste_base:")
            print(context)
        
        if ajuste_impuesto_found:
            start = content.find('hidden_ajuste_impuesto')
            context = content[start-50:start+100]
            print(f"\nContexto de hidden_ajuste_impuesto:")
            print(context)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_template_content()



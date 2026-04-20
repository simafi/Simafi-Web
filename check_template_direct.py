#!/usr/bin/env python3
"""
Script para verificar directamente el contenido del template
"""

def check_template_direct():
    """Verificar directamente el contenido del template"""
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar los campos ocultos específicos
        hidden_fields = [
            'hidden_ajuste_base',
            'hidden_ajuste_impuesto',
            'hidden_ventai_base',
            'hidden_ventai_impuesto'
        ]
        
        print("Verificando campos ocultos en el template:")
        for field in hidden_fields:
            if field in content:
                print(f"  OK {field}: Encontrado en template")
            else:
                print(f"  ERROR {field}: NO encontrado en template")
        
        # Buscar el comentario de force reload
        if 'FORCE RELOAD: Ajuste fields added' in content:
            print("\nOK: Comentario de force reload encontrado")
        else:
            print("\nERROR: Comentario de force reload NO encontrado")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_template_direct()



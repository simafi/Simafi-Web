#!/usr/bin/env python3
"""
Script para forzar la actualización del template
"""

def fix_template_force():
    """Forzar la actualización del template"""
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar la línea que contiene hidden_unidadFactor_impuesto
        if 'hidden_unidadFactor_impuesto' in content:
            # Reemplazar la línea para agregar los campos faltantes
            old_line = '<input type="hidden" id="hidden_unidadFactor_impuesto" name="unidadFactor_impuesto" value="0">'
            new_line = '''<input type="hidden" id="hidden_unidadFactor_impuesto" name="unidadFactor_impuesto" value="0">
                        <input type="hidden" id="hidden_ajuste_base" name="ajuste_base" value="0">
                        <input type="hidden" id="hidden_ajuste_impuesto" name="ajuste_impuesto" value="0">'''
            
            content = content.replace(old_line, new_line)
            
            # Guardar el archivo
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print("Template actualizado exitosamente")
            
            # Verificar que los cambios se aplicaron
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            ajuste_base_found = 'hidden_ajuste_base' in content
            ajuste_impuesto_found = 'hidden_ajuste_impuesto' in content
            
            print(f"hidden_ajuste_base encontrado: {ajuste_base_found}")
            print(f"hidden_ajuste_impuesto encontrado: {ajuste_impuesto_found}")
            
            if ajuste_base_found and ajuste_impuesto_found:
                print("CORRECCION EXITOSA: Campos ocultos agregados correctamente")
            else:
                print("PROBLEMA PERSISTE: Campos ocultos no se agregaron")
                
        else:
            print("ERROR: No se encontró la línea hidden_unidadFactor_impuesto")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_template_force()



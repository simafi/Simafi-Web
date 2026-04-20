#!/usr/bin/env python
"""
Script completo para corregir todos los problemas de indentación
"""

import os

def fix_all_indentation_complete():
    """
    Corregir todos los problemas de indentación de una vez
    """
    file_path = "venv/Scripts/tributario/modules/tributario/views.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Total de líneas en el archivo: {len(lines)}")
    
    # Lista de líneas problemáticas conocidas
    problem_lines = [40, 41, 122, 149, 239, 249]
    
    print(f"🔧 Corrigiendo líneas problemáticas: {problem_lines}")
    
    fixed = False
    
    for line_num in problem_lines:
        idx = line_num - 1  # Convertir a índice 0-based
        if idx < len(lines):
            line = lines[idx]
            original_line = line
            
            # Corregir try mal indentado
            if line.strip() == 'try:' and line.startswith('        '):
                lines[idx] = '    ' + line.lstrip()
                print(f"✅ Corregido try en línea {line_num}")
                fixed = True
            
            # Corregir data = json.loads mal indentado
            elif 'data = json.loads(request.body)' in line and line.startswith('            '):
                lines[idx] = '            ' + line.lstrip()
                print(f"✅ Corregido data = json.loads en línea {line_num}")
                fixed = True
            
            # Corregir negocio = Negocio.objects.get mal indentado
            elif 'negocio = Negocio.objects.get(' in line:
                lines[idx] = '            ' + line.lstrip()
                print(f"✅ Corregido negocio = Negocio.objects.get en línea {line_num}")
                fixed = True
            
            # Corregir otras líneas con indentación incorrecta
            elif line.strip() and not line.startswith('    ') and not line.startswith('def ') and not line.startswith('class '):
                if any(keyword in line for keyword in ['try:', 'except', 'finally', 'if ', 'for ', 'while ', 'with ']):
                    lines[idx] = '    ' + line.lstrip()
                    print(f"✅ Corregida indentación en línea {line_num}")
                    fixed = True
    
    if fixed:
        # Escribir el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"✅ Archivo corregido exitosamente")
        return True
    else:
        print("❌ No se encontraron problemas para corregir")
        return False

if __name__ == "__main__":
    fix_all_indentation_complete()

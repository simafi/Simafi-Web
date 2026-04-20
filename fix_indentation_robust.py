#!/usr/bin/env python
"""
Script robusto para corregir toda la estructura de indentación del archivo views.py
"""

import re
import os

def fix_indentation_robust():
    """
    Corregir toda la estructura de indentación de manera robusta
    """
    file_path = "venv/Scripts/tributario/modules/tributario/views.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Total de líneas en el archivo: {len(lines)}")
    
    # Función para obtener el nivel de indentación
    def get_indent_level(line):
        return len(line) - len(line.lstrip())
    
    # Función para crear indentación
    def create_indent(level):
        return '    ' * level
    
    # Lista de líneas problemáticas conocidas con sus niveles correctos
    fixes = [
        (40, 2, 'try:'),  # try debe estar en nivel 2
        (41, 3, 'data = json.loads(request.body)'),  # data debe estar en nivel 3
        (122, 2, 'try:'),  # try debe estar en nivel 2
        (149, 2, 'try:'),  # try debe estar en nivel 2
        (239, 2, 'try:'),  # try debe estar en nivel 2
        (249, 3, 'negocio = Negocio.objects.get('),  # negocio debe estar en nivel 3
    ]
    
    print(f"🔧 Aplicando correcciones específicas...")
    
    fixed = False
    
    for line_num, correct_level, expected_content in fixes:
        idx = line_num - 1  # Convertir a índice 0-based
        if idx < len(lines):
            line = lines[idx]
            current_level = get_indent_level(line)
            
            # Verificar si la línea contiene el contenido esperado
            if expected_content in line:
                if current_level != correct_level:
                    # Corregir la indentación
                    new_line = create_indent(correct_level) + line.lstrip()
                    lines[idx] = new_line
                    print(f"✅ Línea {line_num}: {current_level} → {correct_level} espacios")
                    fixed = True
                else:
                    print(f"✅ Línea {line_num}: Ya tiene la indentación correcta")
            else:
                print(f"⚠️  Línea {line_num}: No contiene '{expected_content}'")
    
    # Corrección adicional para líneas que siguen a los try
    print(f"\n🔧 Corrigiendo líneas que siguen a los try...")
    
    for i, line in enumerate(lines):
        if line.strip() == 'try:':
            # Buscar la siguiente línea que no esté vacía
            for j in range(i + 1, min(i + 5, len(lines))):
                next_line = lines[j]
                if next_line.strip() and not next_line.startswith('    '):
                    # Esta línea debe estar indentada dentro del try
                    if any(keyword in next_line for keyword in ['data =', 'negocio =', 'if ', 'for ', 'while ']):
                        current_level = get_indent_level(line)
                        correct_level = current_level + 1
                        new_line = create_indent(correct_level) + next_line.lstrip()
                        lines[j] = new_line
                        print(f"✅ Línea {j+1}: Corregida indentación después de try")
                        fixed = True
                    break
    
    if fixed:
        # Escribir el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"\n✅ Archivo corregido exitosamente")
        return True
    else:
        print(f"\n❌ No se encontraron problemas para corregir")
        return False

if __name__ == "__main__":
    fix_indentation_robust()

#!/usr/bin/env python
"""
Script de depuración para analizar y corregir el error de sintaxis
"""

import os
import re

def analyze_syntax_error():
    """
    Analizar el error de sintaxis y corregirlo
    """
    file_path = "venv/Scripts/tributario/modules/tributario/views.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Total de líneas en el archivo: {len(lines)}")
    
    # Buscar el problema específico alrededor de la línea 566
    print(f"\n🔍 Análisis detallado alrededor de la línea 566:")
    for i in range(555, min(575, len(lines))):
        line_content = lines[i].rstrip()
        print(f"   Línea {i+1:3d}: {repr(line_content)}")
    
    # Buscar bloques try sin except/finally
    print(f"\n🔍 Análisis de bloques try:")
    try_blocks = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('try:'):
            try_blocks.append(i)
            print(f"   Try en línea {i}: {line.strip()}")
    
    # Buscar bloques except/finally
    print(f"\n🔍 Análisis de bloques except/finally:")
    except_blocks = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('except') or line.strip().startswith('finally'):
            except_blocks.append(i)
            print(f"   Except/Finally en línea {i}: {line.strip()}")
    
    # Buscar funciones alrededor del problema
    print(f"\n🔍 Funciones alrededor del problema:")
    for i, line in enumerate(lines, 1):
        if i >= 550 and i <= 580:
            if line.strip().startswith('def '):
                print(f"   Función en línea {i}: {line.strip()}")
    
    # Identificar el problema específico
    print(f"\n🔍 Identificando el problema específico:")
    problem_line = None
    for i in range(560, min(570, len(lines))):
        if lines[i].strip().startswith('try:'):
            # Verificar si hay except/finally después
            has_except = False
            for j in range(i+1, min(i+50, len(lines))):
                if lines[j].strip().startswith('except') or lines[j].strip().startswith('finally'):
                    has_except = True
                    break
                elif lines[j].strip().startswith('def ') or lines[j].strip().startswith('class '):
                    break
            
            if not has_except:
                problem_line = i
                print(f"   ❌ PROBLEMA ENCONTRADO: Try en línea {i+1} sin except/finally")
                break
    
    return problem_line

def fix_syntax_error():
    """
    Corregir el error de sintaxis
    """
    file_path = "venv/Scripts/tributario/modules/tributario/views.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Buscar el try problemático
    problem_line = None
    for i, line in enumerate(lines):
        if line.strip().startswith('try:'):
            # Verificar si hay except/finally después
            has_except = False
            for j in range(i+1, min(i+50, len(lines))):
                if lines[j].strip().startswith('except') or lines[j].strip().startswith('finally'):
                    has_except = True
                    break
                elif lines[j].strip().startswith('def ') or lines[j].strip().startswith('class '):
                    break
            
            if not has_except:
                problem_line = i
                break
    
    if problem_line is None:
        print("❌ No se encontró el problema específico")
        return False
    
    print(f"🔧 Corrigiendo el problema en la línea {problem_line + 1}")
    
    # Buscar las líneas que están fuera del try
    indent_level = len(lines[problem_line]) - len(lines[problem_line].lstrip())
    problem_lines = []
    
    for i in range(problem_line + 1, len(lines)):
        line = lines[i]
        if line.strip() == '':
            continue
        
        current_indent = len(line) - len(line.lstrip())
        
        # Si la línea tiene la misma indentación que el try, está fuera del bloque
        if current_indent == indent_level and not line.strip().startswith('except') and not line.strip().startswith('finally'):
            problem_lines.append(i)
        elif current_indent < indent_level:
            break
    
    print(f"🔧 Líneas problemáticas encontradas: {[i+1 for i in problem_lines]}")
    
    # Corregir la indentación
    for i in problem_lines:
        if not lines[i].strip().startswith('except') and not lines[i].strip().startswith('finally'):
            # Aumentar la indentación en 4 espacios
            lines[i] = '    ' + lines[i]
    
    # Escribir el archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ Archivo corregido exitosamente")
    return True

if __name__ == "__main__":
    print("🔍 Analizando el error de sintaxis...")
    problem_line = analyze_syntax_error()
    
    if problem_line is not None:
        print(f"\n🔧 Aplicando corrección...")
        fix_syntax_error()
    else:
        print("❌ No se encontró el problema específico")


















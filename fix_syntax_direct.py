#!/usr/bin/env python
"""
Script directo para corregir el error de sintaxis
"""

import os

def fix_syntax_error():
    """
    Corregir el error de sintaxis específico
    """
    file_path = "venv/Scripts/tributario/modules/tributario/views.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Total de líneas en el archivo: {len(lines)}")
    
    # Buscar el problema específico alrededor de la línea 566
    print(f"\n🔍 Contexto alrededor de la línea 566:")
    for i in range(560, min(570, len(lines))):
        print(f"   Línea {i+1}: {repr(lines[i])}")
    
    # Buscar la función que contiene el problema
    print(f"\n🔍 Buscando la función problemática:")
    for i, line in enumerate(lines, 1):
        if i >= 550 and i <= 580:
            if line.strip().startswith('def '):
                print(f"   Función en línea {i}: {line.strip()}")
            elif line.strip().startswith('try:'):
                print(f"   Try en línea {i}: {line.strip()}")
            elif line.strip().startswith('except') or line.strip().startswith('finally'):
                print(f"   Except/Finally en línea {i}: {line.strip()}")
    
    return True

if __name__ == "__main__":
    fix_syntax_error()


















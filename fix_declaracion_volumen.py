#!/usr/bin/env python
"""
Corrección directa para el error UnboundLocalError en declaracion_volumen
"""

import os
import shutil

def fix_declaracion_volumen():
    """
    Corrige el error UnboundLocalError añadiendo la inicialización de tarifas_ics
    """
    print("🔧 CORRIGIENDO ERROR UnboundLocalError")
    print("=" * 50)
    
    archivo_views = r"C:\simafiweb\venv\Scripts\tributario\modules\tributario\views.py"
    archivo_backup = archivo_views + ".backup"
    
    try:
        # Crear backup
        shutil.copy2(archivo_views, archivo_backup)
        print(f"✅ Backup creado: {archivo_backup}")
        
        # Leer archivo
        with open(archivo_views, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Buscar y corregir
        corrected = False
        for i, line in enumerate(lines):
            # Buscar la línea después de declaraciones = []
            if 'declaraciones = []' in line and i + 1 < len(lines):
                # Verificar si ya existe la inicialización
                next_line = lines[i + 1] if i + 1 < len(lines) else ""
                if 'tarifas_ics = []' not in next_line:
                    # Insertar la inicialización
                    indent = '    '  # 4 espacios de indentación
                    new_line = f"{indent}tarifas_ics = []  # Fix UnboundLocalError\n"
                    lines.insert(i + 1, new_line)
                    corrected = True
                    print(f"✅ Corrección aplicada en línea {i + 2}")
                    break
        
        if corrected:
            # Escribir archivo corregido
            with open(archivo_views, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print("✅ Archivo corregido y guardado")
            return True
        else:
            print("⚠️  No se encontró el patrón para corregir")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        # Restaurar backup si existe
        if os.path.exists(archivo_backup):
            shutil.copy2(archivo_backup, archivo_views)
            print("🔄 Backup restaurado")
        return False

if __name__ == "__main__":
    success = fix_declaracion_volumen()
    if success:
        print("\n🎉 CORRECCIÓN COMPLETADA")
        print("   Reinicie el servidor Django para aplicar cambios")
    else:
        print("\n❌ CORRECCIÓN FALLÓ")
        print("   Aplique la corrección manualmente")

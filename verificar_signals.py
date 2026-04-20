#!/usr/bin/env python
"""
Script para verificar qué módulos necesitan archivos signals.py
"""

import os
import glob

def verificar_signals():
    """Verifica qué módulos necesitan archivos signals.py"""
    
    # Directorio de módulos
    modules_dir = "venv/Scripts/tributario/modules"
    
    print("🔍 Verificando módulos que necesitan signals.py...")
    print("=" * 60)
    
    # Buscar todos los archivos apps.py en módulos
    apps_files = glob.glob(f"{modules_dir}/*/apps.py")
    
    for apps_file in apps_files:
        module_name = apps_file.split(os.sep)[-2]  # Obtener nombre del módulo
        
        print(f"\n📁 Módulo: {module_name}")
        
        try:
            with open(apps_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificar si importa signals
            if 'import' in content and 'signals' in content:
                print(f"  ✅ Tiene importación de signals")
                
                # Verificar si existe el archivo signals.py
                signals_file = apps_file.replace('apps.py', 'signals.py')
                if os.path.exists(signals_file):
                    print(f"  ✅ Archivo signals.py existe")
                else:
                    print(f"  ❌ Archivo signals.py NO existe - NECESITA CREARSE")
                    
            else:
                print(f"  ℹ️ No importa signals")
                
        except Exception as e:
            print(f"  ❌ Error leyendo archivo: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Verificación completada")

if __name__ == "__main__":
    verificar_signals()









































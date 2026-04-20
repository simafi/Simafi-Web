#!/usr/bin/env python3
"""
Script para aplicar correcciones de 'cocontrolado' -> 'controlado' en Django
"""

import os
import shutil
from pathlib import Path

def aplicar_correcciones():
    """Aplica las correcciones a los archivos Django"""
    
    # Archivos a corregir
    archivos_django = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/models.py",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/forms.py",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/views.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/models.py",
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/forms.py", 
        "c:/simafiweb/venv/Scripts/tributario/modules/tributario/views.py"
    ]
    
    correcciones = [
        ("cocontrolado", "controlado"),
        ("'cocontrolado'", "'controlado'"),
        ('"cocontrolado"', '"controlado"'),
        ("Cocontrolado", "Controlado")
    ]
    
    archivos_corregidos = 0
    
    for archivo_path in archivos_django:
        archivo = Path(archivo_path)
        
        if archivo.exists():
            print(f"🔧 Corrigiendo: {archivo}")
            
            # Leer contenido
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Aplicar correcciones
            contenido_original = contenido
            for buscar, reemplazar in correcciones:
                contenido = contenido.replace(buscar, reemplazar)
            
            # Guardar si hubo cambios
            if contenido != contenido_original:
                # Hacer backup
                backup_path = archivo.with_suffix('.backup_controlado')
                shutil.copy2(archivo, backup_path)
                print(f"  📁 Backup: {backup_path}")
                
                # Guardar corregido
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                archivos_corregidos += 1
                print(f"  ✅ Corregido")
            else:
                print(f"  ℹ️ Sin cambios necesarios")
        else:
            print(f"❌ No existe: {archivo}")
    
    print(f"\n✅ Correcciones aplicadas a {archivos_corregidos} archivos")
    
    return archivos_corregidos > 0

if __name__ == "__main__":
    print("🔧 APLICANDO CORRECCIONES DJANGO: cocontrolado -> controlado")
    print("=" * 60)
    
    if aplicar_correcciones():
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Reiniciar servidor Django")
        print("2. Probar URL: /tributario/declaracion-volumen/")
        print("3. Verificar que no hay más errores OperationalError")
    else:
        print("\n⚠️ No se aplicaron correcciones")

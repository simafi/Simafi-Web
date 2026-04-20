#!/usr/bin/env python
"""
Script para limpiar el cache de Python
"""

import os
import sys
import shutil

def limpiar_cache():
    print("="*80)
    print("LIMPIANDO CACHE DE PYTHON")
    print("="*80)
    
    try:
        # Buscar archivos .pyc y __pycache__
        directorio_actual = os.getcwd()
        print(f"Directorio actual: {directorio_actual}")
        
        # Buscar directorios __pycache__
        for root, dirs, files in os.walk(directorio_actual):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    pycache_path = os.path.join(root, dir_name)
                    print(f"Eliminando: {pycache_path}")
                    shutil.rmtree(pycache_path)
        
        # Buscar archivos .pyc
        for root, dirs, files in os.walk(directorio_actual):
            for file_name in files:
                if file_name.endswith('.pyc'):
                    pyc_path = os.path.join(root, file_name)
                    print(f"Eliminando: {pyc_path}")
                    os.remove(pyc_path)
        
        print("✅ Cache limpiado correctamente")
        
    except Exception as e:
        print(f"❌ Error al limpiar cache: {e}")
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    limpiar_cache()































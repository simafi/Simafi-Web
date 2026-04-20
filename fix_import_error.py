#!/usr/bin/env python
"""
Corrección del error de importación en urls.py
ImportError: cannot import name 'include' from 'django.http'
"""

import os
import shutil

def corregir_import_error():
    """
    Corrige el error de importación en urls.py
    """
    print("🔧 CORRIGIENDO ERROR DE IMPORTACIÓN")
    print("=" * 45)
    
    archivo_urls = r"C:\simafiweb\venv\Scripts\tributario\tributario\urls.py"
    
    if not os.path.exists(archivo_urls):
        print(f"❌ Archivo no encontrado: {archivo_urls}")
        return False
    
    try:
        # Crear backup
        backup_file = archivo_urls + ".backup_import"
        shutil.copy2(archivo_urls, backup_file)
        print(f"✅ Backup creado: {backup_file}")
        
        # Leer contenido
        with open(archivo_urls, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print("📝 Contenido actual encontrado:")
        lines = contenido.split('\n')[:10]  # Primeras 10 líneas
        for i, line in enumerate(lines, 1):
            print(f"   {i}: {line}")
        
        # Corregir importaciones incorrectas
        correcciones = [
            {
                'incorrecto': 'from django.http import HttpResponse, include',
                'correcto': 'from django.http import HttpResponse\nfrom django.urls import include'
            },
            {
                'incorrecto': 'from django.http import include',
                'correcto': 'from django.urls import include'
            }
        ]
        
        contenido_corregido = contenido
        correcciones_aplicadas = []
        
        for correccion in correcciones:
            if correccion['incorrecto'] in contenido_corregido:
                contenido_corregido = contenido_corregido.replace(
                    correccion['incorrecto'], 
                    correccion['correcto']
                )
                correcciones_aplicadas.append(correccion['incorrecto'])
        
        if correcciones_aplicadas:
            # Escribir archivo corregido
            with open(archivo_urls, 'w', encoding='utf-8') as f:
                f.write(contenido_corregido)
            
            print("✅ Correcciones aplicadas:")
            for correccion in correcciones_aplicadas:
                print(f"   - {correccion}")
            
            print("\n📝 Contenido corregido:")
            lines = contenido_corregido.split('\n')[:10]
            for i, line in enumerate(lines, 1):
                print(f"   {i}: {line}")
            
            return True
        else:
            print("⚠️  No se encontraron las importaciones incorrectas específicas")
            print("    El error puede estar en otra línea")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la corrección: {e}")
        # Restaurar backup
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, archivo_urls)
            print("🔄 Backup restaurado")
        return False

def mostrar_solucion_manual():
    """
    Muestra la solución manual
    """
    print("\n📋 SOLUCIÓN MANUAL")
    print("=" * 30)
    print("1. Abra el archivo:")
    print("   C:\\simafiweb\\venv\\Scripts\\tributario\\tributario\\urls.py")
    print()
    print("2. Busque la línea que contiene:")
    print("   from django.http import HttpResponse, include")
    print("   O:")
    print("   from django.http import include")
    print()
    print("3. Reemplácela por:")
    print("   from django.http import HttpResponse")
    print("   from django.urls import include")
    print()
    print("4. Guarde el archivo y reinicie el servidor")

if __name__ == "__main__":
    print("🚀 CORRECCIÓN DE ERROR DE IMPORTACIÓN")
    print("   Error: cannot import name 'include' from 'django.http'")
    print()
    
    exito = corregir_import_error()
    
    if exito:
        print("\n🎉 CORRECCIÓN COMPLETADA")
        print("   ✅ Importaciones corregidas")
        print("   🔄 Reinicie el servidor Django")
    else:
        print("\n⚠️  CORRECCIÓN AUTOMÁTICA FALLÓ")
        mostrar_solucion_manual()
    
    print("\n" + "=" * 50)

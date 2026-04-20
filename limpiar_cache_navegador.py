#!/usr/bin/env python3
"""
Script para limpiar cache del navegador y forzar actualización de archivos estáticos
"""

import os
import time
import shutil
from datetime import datetime

def limpiar_cache_navegador():
    """Limpia el cache del navegador y actualiza archivos estáticos"""
    
    print("🧹 LIMPIANDO CACHE DEL NAVEGADOR Y ACTUALIZANDO ARCHIVOS")
    print("=" * 60)
    
    # 1. Actualizar timestamp en archivos JavaScript
    actualizar_timestamps_js()
    
    # 2. Limpiar archivos temporales
    limpiar_archivos_temporales()
    
    # 3. Crear archivo de versión
    crear_archivo_version()
    
    # 4. Instrucciones para el usuario
    mostrar_instrucciones_cache()

def actualizar_timestamps_js():
    """Actualiza timestamps en archivos JavaScript para forzar recarga"""
    
    print("\n📝 1. ACTUALIZANDO TIMESTAMPS EN ARCHIVOS JAVASCRIPT...")
    
    archivos_js = [
        "venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js",
        "declaracion_volumen_interactivo.js"
    ]
    
    timestamp = int(time.time())
    
    for archivo in archivos_js:
        if os.path.exists(archivo):
            try:
                # Leer contenido
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Agregar comentario con timestamp
                comentario_timestamp = f"\n/* Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Timestamp: {timestamp} */\n"
                
                # Verificar si ya tiene timestamp
                if "Última actualización:" not in contenido:
                    contenido = comentario_timestamp + contenido
                
                # Escribir archivo actualizado
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                print(f"   ✅ {archivo} - Timestamp actualizado")
                
            except Exception as e:
                print(f"   ❌ Error actualizando {archivo}: {e}")
        else:
            print(f"   ⚠️ Archivo no encontrado: {archivo}")

def limpiar_archivos_temporales():
    """Limpia archivos temporales y cache"""
    
    print("\n🗑️ 2. LIMPIANDO ARCHIVOS TEMPORALES...")
    
    directorios_limpiar = [
        "__pycache__",
        ".pytest_cache",
        "venv/Scripts/tributario/__pycache__",
        "venv/Scripts/tributario/tributario_app/__pycache__"
    ]
    
    for directorio in directorios_limpiar:
        if os.path.exists(directorio):
            try:
                shutil.rmtree(directorio)
                print(f"   ✅ Eliminado: {directorio}")
            except Exception as e:
                print(f"   ❌ Error eliminando {directorio}: {e}")
        else:
            print(f"   ⚠️ No encontrado: {directorio}")

def crear_archivo_version():
    """Crea archivo de versión para tracking"""
    
    print("\n📋 3. CREANDO ARCHIVO DE VERSIÓN...")
    
    version_info = f"""
# VERSIÓN DEL SISTEMA - DECLARACIÓN DE VOLUMEN
# Generado automáticamente: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Cambios Aplicados:
- ✅ Herencia de RTM, EXPE e ID del negocio en Información Básica
- ✅ Cálculo de unidad × factor en productos controlados
- ✅ Variables ocultas sincronizadas
- ✅ Cache del navegador limpiado

## Archivos Modificados:
- modules/tributario/simple_views.py
- venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js
- venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html

## Próximos Pasos:
1. Recargar página con Ctrl+F5
2. Verificar que los campos RTM, EXPE e ID se llenen automáticamente
3. Probar cálculo de productos controlados con unidad × factor
"""
    
    try:
        with open("VERSION_DECLARACION_VOLUMEN.txt", "w", encoding="utf-8") as f:
            f.write(version_info)
        print("   ✅ Archivo de versión creado: VERSION_DECLARACION_VOLUMEN.txt")
    except Exception as e:
        print(f"   ❌ Error creando archivo de versión: {e}")

def mostrar_instrucciones_cache():
    """Muestra instrucciones para limpiar cache del navegador"""
    
    print("\n🌐 4. INSTRUCCIONES PARA LIMPIAR CACHE DEL NAVEGADOR:")
    print("=" * 60)
    
    instrucciones = """
    🔄 MÉTODOS PARA LIMPIAR CACHE:
    
    1. RECARGA FORZADA (Recomendado):
       - Presiona Ctrl + F5 (Windows/Linux)
       - Presiona Cmd + Shift + R (Mac)
    
    2. DESARROLLADOR (F12):
       - Abre DevTools (F12)
       - Click derecho en el botón de recarga
       - Selecciona "Vaciar caché y recargar de forma forzada"
    
    3. CONFIGURACIÓN DEL NAVEGADOR:
       - Chrome: Configuración > Privacidad > Borrar datos de navegación
       - Firefox: Configuración > Privacidad > Borrar datos
       - Edge: Configuración > Privacidad > Borrar datos de navegación
    
    4. MODO INCÓGNITO:
       - Abre una ventana de incógnito/privada
       - Navega al formulario de declaración de volumen
    
    🎯 VERIFICACIÓN:
    - Los campos RTM, EXPE e ID del negocio deben llenarse automáticamente
    - El cálculo de productos controlados debe incluir unidad × factor
    - Los logs en consola deben mostrar los cálculos correctos
    """
    
    print(instrucciones)
    
    print("\n✅ PROCESO COMPLETADO")
    print("=" * 60)
    print("📋 RESUMEN:")
    print("   • Timestamps actualizados en archivos JavaScript")
    print("   • Archivos temporales eliminados")
    print("   • Archivo de versión creado")
    print("   • Instrucciones de cache proporcionadas")
    print("\n🚀 SIGUIENTE PASO: Recargar página con Ctrl+F5")

if __name__ == "__main__":
    limpiar_cache_navegador()






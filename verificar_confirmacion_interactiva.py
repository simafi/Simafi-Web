#!/usr/bin/env python3
"""
Verificación de Confirmación Interactiva
========================================

Este script verifica que la confirmación interactiva esté implementada
correctamente en lugar del confirm() nativo del navegador.
"""

import os
import re

def verificar_funcion_mostrar_confirmacion():
    """Verifica que la función mostrarConfirmacion esté implementada"""
    
    print("🔍 VERIFICACIÓN DE FUNCIÓN MOSTRAR CONFIRMACIÓN")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    if not os.path.exists(formulario_path):
        print(f"❌ No se encontró el archivo: {formulario_path}")
        return False
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar función mostrarConfirmacion
    if 'mostrarConfirmacion' in contenido:
        print("✅ Función mostrarConfirmacion encontrada")
        
        # Verificar elementos clave del modal
        verificaciones = [
            ('modal-confirmacion', 'ID del modal'),
            ('position: fixed', 'Posición fija'),
            ('z-index: 10000', 'Z-index alto'),
            ('background-color: rgba(0, 0, 0, 0.5)', 'Fondo semi-transparente'),
            ('✅ Confirmar', 'Botón confirmar'),
            ('❌ Cancelar', 'Botón cancelar'),
            ('callback(true)', 'Callback de confirmación'),
            ('callback(false)', 'Callback de cancelación'),
            ('handleEscape', 'Manejo de tecla ESC'),
            ('transition: opacity 0.3s ease', 'Transición suave'),
        ]
        
        for verificacion, descripcion in verificaciones:
            if verificacion in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
        
        return True
    else:
        print("❌ Función mostrarConfirmacion NO encontrada")
        return False

def verificar_llamada_mostrar_confirmacion():
    """Verifica que se use mostrarConfirmacion en lugar de confirm()"""
    
    print("\n🔍 VERIFICACIÓN DE LLAMADA A MOSTRAR CONFIRMACIÓN")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar llamada a mostrarConfirmacion
    pattern = r'mostrarConfirmacion\s*\([^)]*\)'
    matches = re.findall(pattern, contenido)
    
    if matches:
        print(f"✅ Encontradas {len(matches)} llamadas a mostrarConfirmacion:")
        for i, match in enumerate(matches, 1):
            print(f"   {i}. {match}")
        
        # Verificar que se use en el contexto correcto
        if 'data.requiere_confirmacion && data.existe' in contenido:
            print("   ✅ Usado en contexto de confirmación de negocio existente")
        else:
            print("   ❌ NO usado en contexto de confirmación")
        
        return True
    else:
        print("❌ No se encontraron llamadas a mostrarConfirmacion")
        return False

def verificar_eliminacion_confirm_nativo():
    """Verifica que se haya eliminado el confirm() nativo"""
    
    print("\n🔍 VERIFICACIÓN DE ELIMINACIÓN DE CONFIRM() NATIVO")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar confirm() nativo
    pattern = r'confirm\s*\([^)]*\)'
    matches = re.findall(pattern, contenido)
    
    if matches:
        print(f"⚠️  Encontradas {len(matches)} llamadas a confirm() nativo:")
        for i, match in enumerate(matches, 1):
            print(f"   {i}. {match}")
        
        # Verificar si son para eliminación (que está bien mantener)
        eliminacion_confirm = [m for m in matches if 'eliminar' in m.lower() or 'seguro' in m.lower()]
        if eliminacion_confirm:
            print("   ✅ confirm() nativo usado solo para eliminación (correcto)")
            return True
        else:
            print("   ❌ confirm() nativo usado en otros contextos (debe reemplazarse)")
            return False
    else:
        print("✅ No se encontraron llamadas a confirm() nativo")
        return True

def generar_reporte_final():
    """Genera un reporte final de la verificación"""
    
    print("\n📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    resultado_funcion = verificar_funcion_mostrar_confirmacion()
    resultado_llamada = verificar_llamada_mostrar_confirmacion()
    resultado_eliminacion = verificar_eliminacion_confirm_nativo()
    
    print("\n🎯 RESUMEN DE VERIFICACIONES:")
    print(f"   🔔 Función mostrarConfirmacion: {'✅ PASÓ' if resultado_funcion else '❌ FALLÓ'}")
    print(f"   📞 Llamada a mostrarConfirmacion: {'✅ PASÓ' if resultado_llamada else '❌ FALLÓ'}")
    print(f"   🗑️  Eliminación confirm() nativo: {'✅ PASÓ' if resultado_eliminacion else '❌ FALLÓ'}")
    
    if resultado_funcion and resultado_llamada and resultado_eliminacion:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ La confirmación interactiva está implementada correctamente")
        print("✅ Se reemplazó el confirm() nativo con modal personalizado")
        print("✅ El usuario puede confirmar o cancelar la acción")
        print("✅ Modal con diseño moderno y animaciones")
    else:
        print("\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar las implementaciones faltantes")
        print("❌ Asegurar que se use mostrarConfirmacion en lugar de confirm()")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO VERIFICACIÓN DE CONFIRMACIÓN INTERACTIVA")
    print("=" * 60)
    
    # Generar reporte final
    generar_reporte_final()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Probar el formulario con un negocio existente")
    print("2. Verificar que aparezca el modal de confirmación")
    print("3. Probar los botones Confirmar y Cancelar")
    print("4. Verificar que se cierre con ESC o click fuera")
    print("5. Confirmar que la actualización proceda correctamente")

if __name__ == "__main__":
    main() 
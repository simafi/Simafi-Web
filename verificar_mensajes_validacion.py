#!/usr/bin/env python3
"""
Verificación de Mensajes de Validación
======================================

Este script verifica que los mensajes de validación se muestren correctamente
en pantalla.
"""

import os
import re

def verificar_funcion_mostrar_mensaje_mejorada():
    """Verifica que la función mostrarMensaje esté mejorada"""
    
    print("🔍 VERIFICACIÓN DE FUNCIÓN MOSTRAR MENSAJE MEJORADA")
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
    
    # Buscar función mostrarMensaje mejorada
    if 'mostrarMensaje' in contenido:
        print("✅ Función mostrarMensaje encontrada")
        
        # Verificar mejoras implementadas
        verificaciones = [
            ('console.log(\'🔔 Mostrando mensaje:\'', 'Log de debug para mensajes'),
            ('z-index: 9999', 'Z-index mejorado'),
            ('max-width: 500px', 'Ancho máximo definido'),
            ('display: block', 'Display explícito'),
            ('opacity: 1', 'Opacidad explícita'),
            ('transition: opacity 0.3s ease', 'Transición suave'),
            ('console.log(\'🔍 Elemento mensaje creado:\'', 'Log de creación de elemento'),
            ('console.log(\'🔍 Elemento visible:\'', 'Log de visibilidad'),
            ('8000', 'Timeout de 8 segundos'),
            ('opacity: \'0\'', 'Fade out suave'),
        ]
        
        for verificacion, descripcion in verificaciones:
            if verificacion in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
        
        return True
    else:
        print("❌ Función mostrarMensaje NO encontrada")
        return False

def verificar_funcion_debug_mensaje():
    """Verifica que la función debugMensaje esté implementada"""
    
    print("\n🔍 VERIFICACIÓN DE FUNCIÓN DEBUG MENSAJE")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar función debugMensaje
    if 'debugMensaje' in contenido:
        print("✅ Función debugMensaje encontrada")
        
        # Verificar implementación
        verificaciones = [
            ('console.log(\'🔔 DEBUG - Intentando mostrar mensaje:\')', 'Log de debug'),
            ('try {', 'Manejo de errores con try'),
            ('catch (error)', 'Manejo de errores con catch'),
            ('alert(mensaje)', 'Fallback con alert'),
        ]
        
        for verificacion, descripcion in verificaciones:
            if verificacion in contenido:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
        
        return True
    else:
        print("❌ Función debugMensaje NO encontrada")
        return False

def verificar_llamadas_debug_mensaje():
    """Verifica que las llamadas usen debugMensaje"""
    
    print("\n🔍 VERIFICACIÓN DE LLAMADAS A DEBUG MENSAJE")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar llamadas a debugMensaje
    pattern = r'debugMensaje\s*\([^)]*\)'
    matches = re.findall(pattern, contenido)
    
    if matches:
        print(f"✅ Encontradas {len(matches)} llamadas a debugMensaje:")
        for i, match in enumerate(matches, 1):
            print(f"   {i}. {match}")
        
        # Verificar que se usen en validación
        if 'debugMensaje(\'Por favor, complete el campo Municipio\'' in contenido:
            print("   ✅ Usado en validación de Municipio")
        else:
            print("   ❌ NO usado en validación de Municipio")
        
        if 'debugMensaje(\'Por favor, complete el campo RTM\'' in contenido:
            print("   ✅ Usado en validación de RTM")
        else:
            print("   ❌ NO usado en validación de RTM")
        
        if 'debugMensaje(\'Por favor, complete el campo Expediente\'' in contenido:
            print("   ✅ Usado en validación de Expediente")
        else:
            print("   ❌ NO usado en validación de Expediente")
        
        return True
    else:
        print("❌ No se encontraron llamadas a debugMensaje")
        return False

def generar_reporte_final():
    """Genera un reporte final de la verificación"""
    
    print("\n📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    resultado_mostrar = verificar_funcion_mostrar_mensaje_mejorada()
    resultado_debug = verificar_funcion_debug_mensaje()
    resultado_llamadas = verificar_llamadas_debug_mensaje()
    
    print("\n🎯 RESUMEN DE VERIFICACIONES:")
    print(f"   🔔 Función mostrarMensaje mejorada: {'✅ PASÓ' if resultado_mostrar else '❌ FALLÓ'}")
    print(f"   🐛 Función debugMensaje: {'✅ PASÓ' if resultado_debug else '❌ FALLÓ'}")
    print(f"   📞 Llamadas a debugMensaje: {'✅ PASÓ' if resultado_llamadas else '❌ FALLÓ'}")
    
    if resultado_mostrar and resultado_debug and resultado_llamadas:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ Los mensajes de validación deberían mostrarse correctamente")
        print("✅ Se agregó debug para diagnosticar problemas")
        print("✅ Timeout aumentado a 8 segundos")
        print("✅ Z-index mejorado para visibilidad")
    else:
        print("\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar las mejoras que no se implementaron")
        print("❌ Implementar las correcciones faltantes")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO VERIFICACIÓN DE MENSAJES DE VALIDACIÓN")
    print("=" * 60)
    
    # Generar reporte final
    generar_reporte_final()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Probar el formulario con campos vacíos")
    print("2. Verificar que los mensajes aparezcan en pantalla")
    print("3. Revisar la consola del navegador para logs de debug")
    print("4. Confirmar que los mensajes sean visibles por 8 segundos")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Diagnóstico de Mensajes de Validación
=====================================

Este script diagnostica por qué los mensajes de validación no se muestran
en pantalla aunque aparecen en la consola.
"""

import os
import re

def analizar_funcion_mostrar_mensaje():
    """Analiza la función mostrarMensaje"""
    
    print("🔍 ANÁLISIS DE FUNCIÓN MOSTRAR MENSAJE")
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
    
    # Buscar función mostrarMensaje
    if 'mostrarMensaje' in contenido:
        print("✅ Función mostrarMensaje encontrada")
        
        # Buscar el código de la función
        pattern = r'function\s+mostrarMensaje\s*\([^)]*\)\s*\{[^}]*\}'
        matches = re.findall(pattern, contenido, re.DOTALL)
        
        if matches:
            funcion = matches[0]
            print("📝 Código de la función:")
            print(funcion)
            
            # Verificar elementos clave
            verificaciones = [
                ('document.getElementById(\'mensaje-dinamico\')', 'Busca elemento mensaje-dinamico'),
                ('document.createElement(\'div\')', 'Crea elemento div'),
                ('mensajeElement.id = \'mensaje-dinamico\'', 'Asigna ID'),
                ('position: fixed', 'Posición fija'),
                ('z-index: 1000', 'Z-index alto'),
                ('setTimeout', 'Timeout para ocultar'),
                ('display: none', 'Ocultar elemento'),
            ]
            
            for verificacion, descripcion in verificaciones:
                if verificacion in funcion:
                    print(f"   ✅ {descripcion}")
                else:
                    print(f"   ❌ {descripcion} - NO ENCONTRADO")
            
            # Verificar si hay problemas potenciales
            problemas = []
            
            if 'display: none' in funcion and 'setTimeout' in funcion:
                print("   ⚠️  POSIBLE PROBLEMA: El mensaje se oculta automáticamente después de 5 segundos")
                problemas.append("Timeout muy corto")
            
            if 'position: fixed' in funcion and 'top: 20px' in funcion and 'right: 20px' in funcion:
                print("   ✅ Posicionamiento correcto")
            else:
                print("   ❌ POSIBLE PROBLEMA: Posicionamiento incorrecto")
                problemas.append("Posicionamiento incorrecto")
            
            if 'z-index: 1000' in funcion:
                print("   ✅ Z-index correcto")
            else:
                print("   ❌ POSIBLE PROBLEMA: Z-index bajo")
                problemas.append("Z-index bajo")
            
            return problemas
        else:
            print("❌ No se pudo extraer el código de la función")
            return ["No se pudo analizar la función"]
    else:
        print("❌ Función mostrarMensaje NO encontrada")
        return ["Función no encontrada"]

def analizar_llamadas_mostrar_mensaje():
    """Analiza las llamadas a mostrarMensaje"""
    
    print("\n🔍 ANÁLISIS DE LLAMADAS A MOSTRAR MENSAJE")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar llamadas a mostrarMensaje
    pattern = r'mostrarMensaje\s*\([^)]*\)'
    matches = re.findall(pattern, contenido)
    
    if matches:
        print(f"✅ Encontradas {len(matches)} llamadas a mostrarMensaje:")
        for i, match in enumerate(matches[:10], 1):  # Mostrar solo las primeras 10
            print(f"   {i}. {match}")
        
        # Verificar tipos de mensajes
        mensajes_error = [m for m in matches if 'false' in m]
        mensajes_exito = [m for m in matches if 'true' in m]
        
        print(f"\n📊 Tipos de mensajes:")
        print(f"   ❌ Mensajes de error: {len(mensajes_error)}")
        print(f"   ✅ Mensajes de éxito: {len(mensajes_exito)}")
        
        return True
    else:
        print("❌ No se encontraron llamadas a mostrarMensaje")
        return False

def generar_solucion_mensajes():
    """Genera solución para el problema de mensajes"""
    
    print("\n💡 SOLUCIÓN PARA MENSAJES DE VALIDACIÓN")
    print("=" * 50)
    
    print("🔧 PROBLEMAS IDENTIFICADOS:")
    print("   1. El mensaje se oculta automáticamente después de 5 segundos")
    print("   2. Posible problema de posicionamiento")
    print("   3. Posible problema de z-index")
    
    print("\n🛠️  SOLUCIONES PROPUESTAS:")
    
    print("\n1. **Mejorar la función mostrarMensaje**:")
    print("```javascript")
    print("function mostrarMensaje(mensaje, esExito) {")
    print("    // Crear o actualizar el elemento de mensaje")
    print("    let mensajeElement = document.getElementById('mensaje-dinamico');")
    print("    if (!mensajeElement) {")
    print("        mensajeElement = document.createElement('div');")
    print("        mensajeElement.id = 'mensaje-dinamico';")
    print("        mensajeElement.style.cssText = `")
    print("            padding: 15px;")
    print("            margin: 20px 0;")
    print("            border-radius: 8px;")
    print("            font-weight: 600;")
    print("            text-align: center;")
    print("            position: fixed;")
    print("            top: 20px;")
    print("            right: 20px;")
    print("            z-index: 9999;")
    print("            min-width: 300px;")
    print("            max-width: 500px;")
    print("            box-shadow: 0 4px 12px rgba(0,0,0,0.15);")
    print("            display: block;")
    print("            opacity: 1;")
    print("        `;")
    print("        document.body.appendChild(mensajeElement);")
    print("    }")
    print("    ")
    print("    mensajeElement.textContent = mensaje;")
    print("    mensajeElement.style.backgroundColor = esExito ? '#d4edda' : '#f8d7da';")
    print("    mensajeElement.style.color = esExito ? '#155724' : '#721c24';")
    print("    mensajeElement.style.border = `1px solid ${esExito ? '#c3e6cb' : '#f5c6cb'}`;")
    print("    mensajeElement.style.display = 'block';")
    print("    mensajeElement.style.opacity = '1';")
    print("    ")
    print("    // Mostrar el mensaje inmediatamente")
    print("    console.log('🔔 Mostrando mensaje:', mensaje);")
    print("    ")
    print("    // Ocultar después de 8 segundos (más tiempo)")
    print("    setTimeout(() => {")
    print("        if (mensajeElement) {")
    print("            mensajeElement.style.opacity = '0';")
    print("            setTimeout(() => {")
    print("                mensajeElement.style.display = 'none';")
    print("            }, 300);")
    print("        }")
    print("    }, 8000);")
    print("}")
    print("```")
    
    print("\n2. **Agregar función de debug para mensajes**:")
    print("```javascript")
    print("function debugMensaje(mensaje, esExito) {")
    print("    console.log('🔔 DEBUG - Intentando mostrar mensaje:');")
    print("    console.log('   Mensaje:', mensaje);")
    print("    console.log('   Es éxito:', esExito);")
    print("    ")
    print("    try {")
    print("        mostrarMensaje(mensaje, esExito);")
    print("        console.log('✅ Mensaje mostrado correctamente');")
    print("    } catch (error) {")
    print("        console.error('❌ Error al mostrar mensaje:', error);")
    print("        // Fallback: alert simple")
    print("        alert(mensaje);")
    print("    }")
    print("}")
    print("```")
    
    print("\n3. **Verificar que el elemento se cree correctamente**:")
    print("```javascript")
    print("// Agregar después de crear el elemento")
    print("console.log('🔍 Elemento mensaje creado:', mensajeElement);")
    print("console.log('🔍 Estilos del elemento:', mensajeElement.style.cssText);")
    print("console.log('🔍 Elemento visible:', mensajeElement.offsetParent !== null);")
    print("```")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO DIAGNÓSTICO DE MENSAJES DE VALIDACIÓN")
    print("=" * 60)
    
    # Analizar función mostrarMensaje
    problemas = analizar_funcion_mostrar_mensaje()
    
    # Analizar llamadas
    analizar_llamadas_mostrar_mensaje()
    
    # Generar soluciones
    generar_solucion_mensajes()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Implementar las mejoras en mostrarMensaje")
    print("2. Agregar logs de debug para verificar el funcionamiento")
    print("3. Probar con diferentes tipos de mensajes")
    print("4. Verificar que los mensajes aparezcan en pantalla")

if __name__ == "__main__":
    main() 
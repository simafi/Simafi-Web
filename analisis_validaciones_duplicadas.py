#!/usr/bin/env python3
"""
Análisis de Validaciones Duplicadas en el Proceso de Salvar
==========================================================

Este script identifica todas las validaciones duplicadas que pueden estar
afectando el proceso de salvar un registro en maestro_negocios.html
"""

import os
import re

def analizar_validaciones_html5():
    """Analiza las validaciones HTML5 en el formulario"""
    
    print("🔍 ANÁLISIS DE VALIDACIONES HTML5")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    if not os.path.exists(formulario_path):
        print(f"❌ No se encontró el archivo: {formulario_path}")
        return []
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return []
    
    # Buscar campos con validaciones HTML5
    validaciones_html5 = []
    
    # Patrones para buscar validaciones HTML5
    patterns = [
        (r'required', 'required'),
        (r'pattern="([^"]+)"', 'pattern'),
        (r'title="([^"]+)"', 'title'),
        (r'maxlength="(\d+)"', 'maxlength'),
        (r'minlength="(\d+)"', 'minlength'),
    ]
    
    for pattern, tipo in patterns:
        matches = re.findall(pattern, contenido)
        if matches:
            print(f"✅ Encontradas validaciones {tipo}: {len(matches)}")
            for match in matches[:5]:  # Mostrar solo las primeras 5
                print(f"   - {match}")
            validaciones_html5.extend(matches)
    
    return validaciones_html5

def analizar_validaciones_javascript():
    """Analiza las validaciones JavaScript en el formulario"""
    
    print("\n🔍 ANÁLISIS DE VALIDACIONES JAVASCRIPT")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return []
    
    validaciones_js = []
    
    # Buscar funciones de validación
    funciones_validacion = [
        'validarCamposObligatorios',
        'handleSalvarSubmit',
        'handleEliminarSubmit',
        'manejarBoton'
    ]
    
    for funcion in funciones_validacion:
        if funcion in contenido:
            print(f"✅ Función encontrada: {funcion}")
            validaciones_js.append(funcion)
        else:
            print(f"❌ Función no encontrada: {funcion}")
    
    # Buscar validaciones específicas de campos
    validaciones_campos = [
        (r'!empre\s*\|\|\s*!rtm\s*\|\|\s*!expe', 'Validación múltiple de campos'),
        (r'!empre\s*\|\|\s*empre\s*===\s*[\'"]\s*[\'"]', 'Validación específica empre'),
        (r'!rtm\s*\|\|\s*rtm\s*===\s*[\'"]\s*[\'"]', 'Validación específica rtm'),
        (r'!expe\s*\|\|\s*expe\s*===\s*[\'"]\s*[\'"]', 'Validación específica expe'),
        (r'empre\.trim\(\)', 'Trim de empre'),
        (r'rtm\.trim\(\)', 'Trim de rtm'),
        (r'expe\.trim\(\)', 'Trim de expe'),
    ]
    
    for pattern, descripcion in validaciones_campos:
        matches = re.findall(pattern, contenido)
        if matches:
            print(f"✅ {descripcion}: {len(matches)} ocurrencias")
            validaciones_js.append(descripcion)
    
    return validaciones_js

def analizar_validaciones_servidor():
    """Analiza las validaciones del servidor"""
    
    print("\n🔍 ANÁLISIS DE VALIDACIONES DEL SERVIDOR")
    print("=" * 50)
    
    views_path = "venv/Scripts/mi_proyecto/hola/views.py"
    
    if not os.path.exists(views_path):
        print(f"❌ No se encontró el archivo: {views_path}")
        return []
    
    try:
        with open(views_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return []
    
    validaciones_servidor = []
    
    # Buscar validaciones específicas
    validaciones_especificas = [
        (r'if\s+not\s+empre\s+or\s+not\s+rtm\s+or\s+not\s+expe', 'Validación múltiple campos'),
        (r'if\s+not\s+empre\s+or\s+empre\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación empre vacío'),
        (r'if\s+not\s+rtm\s+or\s+rtm\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación rtm vacío'),
        (r'if\s+not\s+expe\s+or\s+expe\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación expe vacío'),
        (r'campos_faltantes\.append\([\'"]Municipio[\'"]\)', 'Mensaje Municipio'),
        (r'campos_faltantes\.append\([\'"]RTM[\'"]\)', 'Mensaje RTM'),
        (r'campos_faltantes\.append\([\'"]Expediente[\'"]\)', 'Mensaje Expediente'),
    ]
    
    for pattern, descripcion in validaciones_especificas:
        matches = re.findall(pattern, contenido)
        if matches:
            print(f"✅ {descripcion}: {len(matches)} ocurrencias")
            validaciones_servidor.append(descripcion)
    
    return validaciones_servidor

def identificar_validaciones_duplicadas():
    """Identifica validaciones duplicadas que pueden estar causando conflictos"""
    
    print("\n🔍 IDENTIFICACIÓN DE VALIDACIONES DUPLICADAS")
    print("=" * 50)
    
    # Obtener todas las validaciones
    html5_validaciones = analizar_validaciones_html5()
    js_validaciones = analizar_validaciones_javascript()
    servidor_validaciones = analizar_validaciones_servidor()
    
    print("\n📊 RESUMEN DE VALIDACIONES ENCONTRADAS:")
    print(f"   HTML5: {len(html5_validaciones)} validaciones")
    print(f"   JavaScript: {len(js_validaciones)} validaciones")
    print(f"   Servidor: {len(servidor_validaciones)} validaciones")
    
    # Identificar posibles conflictos
    conflictos = []
    
    # 1. Verificar si hay múltiples validaciones para los mismos campos
    if len(js_validaciones) > 3:  # Más de 3 funciones de validación
        conflictos.append("Múltiples funciones de validación JavaScript")
    
    # 2. Verificar si hay validaciones HTML5 y JavaScript para los mismos campos
    if 'required' in html5_validaciones and len(js_validaciones) > 0:
        conflictos.append("Validación HTML5 required + JavaScript")
    
    # 3. Verificar si hay validaciones en cliente y servidor
    if len(js_validaciones) > 0 and len(servidor_validaciones) > 0:
        conflictos.append("Validación duplicada cliente-servidor")
    
    # 4. Verificar si hay múltiples validaciones de campos vacíos
    validaciones_vacias = 0
    for validacion in js_validaciones + servidor_validaciones:
        if 'vacío' in validacion or 'faltante' in validacion:
            validaciones_vacias += 1
    
    if validaciones_vacias > 3:
        conflictos.append("Múltiples validaciones de campos vacíos")
    
    return conflictos

def generar_recomendaciones(conflictos):
    """Genera recomendaciones para resolver conflictos de validación"""
    
    print("\n💡 RECOMENDACIONES PARA RESOLVER CONFLICTOS")
    print("=" * 50)
    
    if not conflictos:
        print("✅ No se identificaron conflictos de validación")
        return
    
    print("❌ CONFLICTOS IDENTIFICADOS:")
    for conflicto in conflictos:
        print(f"   - {conflicto}")
    
    print("\n🔧 SOLUCIONES RECOMENDADAS:")
    
    if "Múltiples funciones de validación JavaScript" in conflictos:
        print("   1. Consolidar todas las validaciones JavaScript en una sola función")
        print("   2. Usar validarCamposObligatorios() como función principal")
        print("   3. Eliminar validaciones duplicadas en handleSalvarSubmit")
    
    if "Validación HTML5 required + JavaScript" in conflictos:
        print("   1. Mantener validación HTML5 para UX inmediata")
        print("   2. Usar JavaScript solo para validaciones complejas")
        print("   3. Evitar validaciones redundantes")
    
    if "Validación duplicada cliente-servidor" in conflictos:
        print("   1. Usar validación del cliente para UX")
        print("   2. Usar validación del servidor para seguridad")
        print("   3. Asegurar que los mensajes sean consistentes")
    
    if "Múltiples validaciones de campos vacíos" in conflictos:
        print("   1. Consolidar validaciones de campos vacíos")
        print("   2. Usar una sola función de validación")
        print("   3. Eliminar validaciones redundantes")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO ANÁLISIS DE VALIDACIONES DUPLICADAS")
    print("=" * 60)
    
    # Identificar conflictos
    conflictos = identificar_validaciones_duplicadas()
    
    # Generar recomendaciones
    generar_recomendaciones(conflictos)
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Revisar las validaciones identificadas")
    print("2. Implementar las recomendaciones sugeridas")
    print("3. Probar el formulario después de los cambios")
    print("4. Verificar que no haya más conflictos")

if __name__ == "__main__":
    main() 
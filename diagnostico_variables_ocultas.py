#!/usr/bin/env python3
"""
Diagnóstico de Variables Ocultas y Campos Vacíos en maestro_negocios.html
=======================================================================

Este script identifica problemas específicos con:
1. Variables ocultas que pueden estar causando conflictos
2. Campos RTM y EXPE vacíos al presionar grabar
3. Validaciones y manejo de datos en el formulario
"""

import os
import re
from pathlib import Path

def analizar_formulario_html():
    """Analiza el formulario maestro_negocios.html para identificar problemas"""
    
    print("🔍 DIAGNÓSTICO DE VARIABLES OCULTAS Y CAMPOS VACÍOS")
    print("=" * 60)
    
    # Ruta del formulario
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    if not os.path.exists(formulario_path):
        print(f"❌ No se encontró el archivo: {formulario_path}")
        return
    
    print(f"📁 Analizando formulario: {formulario_path}")
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    print(f"📊 Tamaño del archivo: {len(contenido)} caracteres")
    
    # 1. Buscar variables ocultas (hidden inputs)
    print("\n🔍 1. ANÁLISIS DE VARIABLES OCULTAS")
    print("-" * 40)
    
    hidden_patterns = [
        r'<input[^>]*type\s*=\s*["\']hidden["\'][^>]*>',
        r'<input[^>]*hidden[^>]*>',
        r'value\s*=\s*["\']["\']',  # Valores vacíos
    ]
    
    variables_ocultas = []
    for pattern in hidden_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"⚠️  Encontradas {len(matches)} posibles variables ocultas:")
            for match in matches[:5]:  # Mostrar solo las primeras 5
                print(f"   - {match.strip()}")
            variables_ocultas.extend(matches)
    
    if not variables_ocultas:
        print("✅ No se encontraron variables ocultas problemáticas")
    
    # 2. Analizar campos RTM y EXPE
    print("\n🔍 2. ANÁLISIS DE CAMPOS RTM Y EXPE")
    print("-" * 40)
    
    # Buscar definiciones de campos RTM y EXPE
    rtm_pattern = r'<input[^>]*name\s*=\s*["\']rtm["\'][^>]*>'
    expe_pattern = r'<input[^>]*name\s*=\s*["\']expe["\'][^>]*>'
    
    rtm_matches = re.findall(rtm_pattern, contenido, re.IGNORECASE)
    expe_matches = re.findall(expe_pattern, contenido, re.IGNORECASE)
    
    print(f"📝 Campo RTM encontrado: {'✅' if rtm_matches else '❌'}")
    if rtm_matches:
        print(f"   - Definición: {rtm_matches[0].strip()}")
    
    print(f"📝 Campo EXPE encontrado: {'✅' if expe_matches else '❌'}")
    if expe_matches:
        print(f"   - Definición: {expe_matches[0].strip()}")
    
    # 3. Analizar validaciones JavaScript
    print("\n🔍 3. ANÁLISIS DE VALIDACIONES JAVASCRIPT")
    print("-" * 40)
    
    # Buscar validaciones de campos vacíos
    validacion_patterns = [
        r'!rtm\s*\|\|\s*!expe',  # Validación de campos vacíos
        r'rtm\.trim\(\)',        # Uso de trim()
        r'expe\.trim\(\)',       # Uso de trim()
        r'if\s*\([^)]*rtm[^)]*\)',  # Condiciones con RTM
        r'if\s*\([^)]*expe[^)]*\)', # Condiciones con EXPE
    ]
    
    for pattern in validacion_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"✅ Encontrada validación: {pattern}")
            for match in matches[:3]:
                print(f"   - {match.strip()}")
    
    # 4. Analizar función handleSalvarSubmit
    print("\n🔍 4. ANÁLISIS DE FUNCIÓN handleSalvarSubmit")
    print("-" * 40)
    
    salvar_pattern = r'function\s+handleSalvarSubmit\s*\([^)]*\)\s*\{[^}]*\}'
    salvar_matches = re.findall(salvar_pattern, contenido, re.DOTALL)
    
    if salvar_matches:
        print("✅ Función handleSalvarSubmit encontrada")
        # Buscar validaciones específicas dentro de la función
        funcion = salvar_matches[0]
        
        # Buscar validaciones de campos vacíos
        validaciones_vacias = re.findall(r'!\w+\s*\|\|\s*!\w+', funcion)
        if validaciones_vacias:
            print("⚠️  Validaciones de campos vacíos encontradas:")
            for validacion in validaciones_vacias:
                print(f"   - {validacion}")
        
        # Buscar obtención de valores
        obtencion_valores = re.findall(r'getElementById\([\'"]id_(rtm|expe)[\'"]\)\.value', funcion)
        if obtencion_valores:
            print("✅ Obtención de valores RTM/EXPE encontrada")
    
    # 5. Analizar manejo de FormData
    print("\n🔍 5. ANÁLISIS DE MANEJO DE FORMDATA")
    print("-" * 40)
    
    formdata_patterns = [
        r'FormData\s*\([^)]*\)',
        r'formData\.append\s*\([^)]*\)',
    ]
    
    for pattern in formdata_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"✅ FormData encontrado: {len(matches)} usos")
            for match in matches[:3]:
                print(f"   - {match.strip()}")
    
    # 6. Buscar posibles conflictos de nombres
    print("\n🔍 6. ANÁLISIS DE POSIBLES CONFLICTOS")
    print("-" * 40)
    
    # Buscar nombres de campos duplicados o conflictivos
    name_pattern = r'name\s*=\s*["\']([^"\']+)["\']'
    nombres_campos = re.findall(name_pattern, contenido)
    
    duplicados = {}
    for nombre in nombres_campos:
        if nombre in duplicados:
            duplicados[nombre] += 1
        else:
            duplicados[nombre] = 1
    
    conflictos = {k: v for k, v in duplicados.items() if v > 1}
    if conflictos:
        print("⚠️  Posibles conflictos de nombres de campos:")
        for nombre, count in conflictos.items():
            print(f"   - {nombre}: {count} veces")
    else:
        print("✅ No se encontraron conflictos de nombres de campos")
    
    # 7. Recomendaciones
    print("\n🔍 7. RECOMENDACIONES")
    print("-" * 40)
    
    problemas_identificados = []
    
    if variables_ocultas:
        problemas_identificados.append("Variables ocultas encontradas")
    
    if not rtm_matches or not expe_matches:
        problemas_identificados.append("Campos RTM o EXPE no encontrados")
    
    if conflictos:
        problemas_identificados.append("Conflictos de nombres de campos")
    
    if problemas_identificados:
        print("❌ PROBLEMAS IDENTIFICADOS:")
        for problema in problemas_identificados:
            print(f"   - {problema}")
        
        print("\n💡 SOLUCIONES RECOMENDADAS:")
        print("   1. Verificar que no haya campos hidden con nombres conflictivos")
        print("   2. Asegurar que los campos RTM y EXPE tengan valores por defecto")
        print("   3. Revisar validaciones JavaScript para campos vacíos")
        print("   4. Verificar el manejo de FormData en el envío")
        print("   5. Comprobar que no haya duplicados en nombres de campos")
    else:
        print("✅ No se identificaron problemas evidentes en el análisis")
        print("💡 Verificar comportamiento en tiempo de ejecución")

def analizar_vista_django():
    """Analiza la vista de Django para identificar problemas en el backend"""
    
    print("\n🔍 8. ANÁLISIS DE VISTA DJANGO")
    print("-" * 40)
    
    views_path = "venv/Scripts/mi_proyecto/hola/views.py"
    
    if not os.path.exists(views_path):
        print(f"❌ No se encontró el archivo: {views_path}")
        return
    
    try:
        with open(views_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # Buscar manejo de campos RTM y EXPE en la vista
    rtm_expe_patterns = [
        r'rtm\s*=\s*request\.POST\.get\([\'"]rtm[\'"][^)]*\)',
        r'expe\s*=\s*request\.POST\.get\([\'"]expe[\'"][^)]*\)',
        r'if\s+not\s+rtm\s+or\s+not\s+expe',
        r'rtm\.strip\(\)',
        r'expe\.strip\(\)',
    ]
    
    print("🔍 Buscando manejo de campos RTM y EXPE en la vista:")
    for pattern in rtm_expe_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"✅ Encontrado: {pattern}")
            for match in matches[:2]:
                print(f"   - {match.strip()}")
    
    # Buscar validaciones de campos vacíos
    validacion_vacia_pattern = r'if\s+not\s+\w+\s+or\s+not\s+\w+\s+or\s+not\s+\w+'
    validaciones = re.findall(validacion_vacia_pattern, contenido)
    if validaciones:
        print("✅ Validaciones de campos vacíos encontradas en la vista")
        for validacion in validaciones[:3]:
            print(f"   - {validacion.strip()}")

def main():
    """Función principal del diagnóstico"""
    
    print("🚀 INICIANDO DIAGNÓSTICO COMPLETO")
    print("=" * 60)
    
    # Analizar formulario HTML
    analizar_formulario_html()
    
    # Analizar vista Django
    analizar_vista_django()
    
    print("\n🎯 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    print("✅ Análisis completado")
    print("📋 Revisar los resultados anteriores para identificar problemas específicos")
    print("🔧 Implementar las soluciones recomendadas según los problemas encontrados")

if __name__ == "__main__":
    main() 
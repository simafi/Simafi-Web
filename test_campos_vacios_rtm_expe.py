#!/usr/bin/env python3
"""
Prueba Específica de Campos RTM y EXPE Vacíos
==============================================

Este script identifica específicamente el problema con:
1. Campos RTM y EXPE que llegan vacíos al servidor
2. Variables ocultas que pueden estar interfiriendo
3. Validaciones que pueden estar bloqueando el envío
"""

import os
import re

def analizar_campos_rtm_expe():
    """Analiza específicamente los campos RTM y EXPE"""
    
    print("🔍 ANÁLISIS ESPECÍFICO DE CAMPOS RTM Y EXPE")
    print("=" * 50)
    
    # Ruta del formulario
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    if not os.path.exists(formulario_path):
        print(f"❌ No se encontró el archivo: {formulario_path}")
        return
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # 1. Buscar definiciones exactas de campos RTM y EXPE
    print("\n📝 1. DEFINICIONES DE CAMPOS RTM Y EXPE")
    print("-" * 40)
    
    # Patrón más específico para campos RTM y EXPE
    rtm_pattern = r'<input[^>]*id\s*=\s*["\']id_rtm["\'][^>]*>'
    expe_pattern = r'<input[^>]*id\s*=\s*["\']id_expe["\'][^>]*>'
    
    rtm_matches = re.findall(rtm_pattern, contenido, re.IGNORECASE)
    expe_matches = re.findall(expe_pattern, contenido, re.IGNORECASE)
    
    print("Campo RTM:")
    if rtm_matches:
        print(f"✅ Encontrado: {rtm_matches[0].strip()}")
    else:
        print("❌ No encontrado")
    
    print("Campo EXPE:")
    if expe_matches:
        print(f"✅ Encontrado: {expe_matches[0].strip()}")
    else:
        print("❌ No encontrado")
    
    # 2. Buscar valores por defecto
    print("\n📝 2. VALORES POR DEFECTO")
    print("-" * 40)
    
    # Buscar valores por defecto en los campos
    default_patterns = [
        r'value\s*=\s*["\']([^"\']*)["\']',
        r'default_if_none:\s*["\']([^"\']*)["\']',
    ]
    
    for pattern in default_patterns:
        matches = re.findall(pattern, contenido)
        if matches:
            print(f"Valores encontrados: {matches[:5]}")
    
    # 3. Buscar validaciones JavaScript específicas
    print("\n📝 3. VALIDACIONES JAVASCRIPT")
    print("-" * 40)
    
    # Buscar validaciones específicas para RTM y EXPE
    validacion_patterns = [
        r'const\s+rtm\s*=\s*document\.getElementById\([\'"]id_rtm[\'"]\)\.value',
        r'const\s+expe\s*=\s*document\.getElementById\([\'"]id_expe[\'"]\)\.value',
        r'rtm\.trim\(\)',
        r'expe\.trim\(\)',
        r'!rtm\s*\|\|\s*!expe',
        r'if\s*\([^)]*rtm[^)]*\)',
        r'if\s*\([^)]*expe[^)]*\)',
    ]
    
    for pattern in validacion_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"✅ Encontrada validación: {pattern}")
            for match in matches[:2]:
                print(f"   - {match.strip()}")
    
    # 4. Buscar función handleSalvarSubmit específicamente
    print("\n📝 4. FUNCIÓN handleSalvarSubmit")
    print("-" * 40)
    
    # Buscar la función completa
    salvar_pattern = r'function\s+handleSalvarSubmit\s*\([^)]*\)\s*\{[^}]*\}'
    salvar_matches = re.findall(salvar_pattern, contenido, re.DOTALL)
    
    if salvar_matches:
        print("✅ Función handleSalvarSubmit encontrada")
        funcion = salvar_matches[0]
        
        # Buscar líneas específicas dentro de la función
        lineas_importantes = [
            r'const\s+rtm\s*=\s*document\.getElementById\([\'"]id_rtm[\'"]\)\.value\.trim\(\)',
            r'const\s+expe\s*=\s*document\.getElementById\([\'"]id_expe[\'"]\)\.value\.trim\(\)',
            r'if\s*\(!empre\s*\|\|\s*!rtm\s*\|\|\s*!expe\)',
            r'mostrarMensaje\([^)]*\)',
        ]
        
        for pattern in lineas_importantes:
            matches = re.findall(pattern, funcion, re.IGNORECASE)
            if matches:
                print(f"✅ Encontrada línea: {pattern}")
                for match in matches:
                    print(f"   - {match.strip()}")
    else:
        print("❌ Función handleSalvarSubmit no encontrada")
    
    # 5. Buscar posibles variables ocultas o conflictos
    print("\n📝 5. POSIBLES CONFLICTOS")
    print("-" * 40)
    
    # Buscar campos con nombres similares
    conflict_patterns = [
        r'name\s*=\s*["\']rtm["\']',
        r'name\s*=\s*["\']expe["\']',
        r'id\s*=\s*["\']rtm["\']',
        r'id\s*=\s*["\']expe["\']',
        r'<input[^>]*rtm[^>]*>',
        r'<input[^>]*expe[^>]*>',
    ]
    
    for pattern in conflict_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"✅ Encontrado patrón: {pattern}")
            for match in matches[:3]:
                print(f"   - {match.strip()}")
    
    # 6. Buscar manejo de FormData
    print("\n📝 6. MANEJO DE FORMDATA")
    print("-" * 40)
    
    formdata_patterns = [
        r'FormData\s*\([^)]*\)',
        r'formData\.append\s*\([\'"]rtm[\'"][^)]*\)',
        r'formData\.append\s*\([\'"]expe[\'"][^)]*\)',
    ]
    
    for pattern in formdata_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"✅ Encontrado FormData: {pattern}")
            for match in matches[:2]:
                print(f"   - {match.strip()}")

def analizar_vista_django_especifica():
    """Analiza específicamente el manejo de RTM y EXPE en la vista"""
    
    print("\n📝 7. ANÁLISIS DE VISTA DJANGO")
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
    
    # Buscar manejo específico de RTM y EXPE
    rtm_expe_patterns = [
        r'rtm\s*=\s*request\.POST\.get\([\'"]rtm[\'"][^)]*\)',
        r'expe\s*=\s*request\.POST\.get\([\'"]expe[\'"][^)]*\)',
        r'rtm\.strip\(\)',
        r'expe\.strip\(\)',
        r'if\s+not\s+rtm\s+or\s+not\s+expe',
        r'len\(rtm\)\s*>\s*\d+',
        r'len\(expe\)\s*>\s*\d+',
    ]
    
    print("Manejo de campos RTM y EXPE en la vista:")
    for pattern in rtm_expe_patterns:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"✅ Encontrado: {pattern}")
            for match in matches[:2]:
                print(f"   - {match.strip()}")

def generar_recomendaciones():
    """Genera recomendaciones específicas basadas en el análisis"""
    
    print("\n💡 RECOMENDACIONES ESPECÍFICAS")
    print("=" * 50)
    
    print("1. VERIFICAR CAMPOS RTM Y EXPE:")
    print("   - Asegurar que los campos tengan valores por defecto")
    print("   - Verificar que no estén deshabilitados (disabled)")
    print("   - Comprobar que los IDs sean únicos")
    
    print("\n2. REVISAR VALIDACIONES JAVASCRIPT:")
    print("   - Verificar que las validaciones no bloqueen campos válidos")
    print("   - Asegurar que trim() no elimine espacios necesarios")
    print("   - Comprobar que las condiciones sean correctas")
    
    print("\n3. VERIFICAR MANEJO DE FORMDATA:")
    print("   - Asegurar que los campos se incluyan en FormData")
    print("   - Verificar que no haya campos duplicados")
    print("   - Comprobar que los nombres de campos sean correctos")
    
    print("\n4. REVISAR VISTA DJANGO:")
    print("   - Verificar que los campos se reciban correctamente")
    print("   - Asegurar que las validaciones del servidor sean apropiadas")
    print("   - Comprobar que no haya conflictos de nombres")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO ANÁLISIS ESPECÍFICO DE CAMPOS RTM Y EXPE")
    print("=" * 60)
    
    # Analizar campos específicos
    analizar_campos_rtm_expe()
    
    # Analizar vista Django
    analizar_vista_django_especifica()
    
    # Generar recomendaciones
    generar_recomendaciones()
    
    print("\n🎯 RESUMEN")
    print("=" * 30)
    print("✅ Análisis específico completado")
    print("📋 Revisar los resultados para identificar el problema exacto")
    print("🔧 Implementar las recomendaciones según los hallazgos")

if __name__ == "__main__":
    main() 
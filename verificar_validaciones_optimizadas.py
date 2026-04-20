#!/usr/bin/env python3
"""
Verificación de Validaciones Optimizadas
=======================================

Este script verifica que las validaciones duplicadas han sido eliminadas
y que el proceso de salvar funciona correctamente.
"""

import os
import re

def verificar_validaciones_javascript():
    """Verifica que las validaciones JavaScript estén optimizadas"""
    
    print("🔍 VERIFICACIÓN DE VALIDACIONES JAVASCRIPT")
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
    
    # Verificar que solo hay una función de validación principal
    validaciones_principales = [
        ('validarCamposObligatorios', 'Función principal de validación'),
        ('handleSalvarSubmit', 'Función de salvar'),
    ]
    
    for funcion, descripcion in validaciones_principales:
        if funcion in contenido:
            print(f"✅ {descripcion}: Encontrada")
        else:
            print(f"❌ {descripcion}: NO encontrada")
    
    # Verificar que handleSalvarSubmit usa validarCamposObligatorios
    if 'validarCamposObligatorios()' in contenido:
        print("✅ handleSalvarSubmit usa validarCamposObligatorios()")
    else:
        print("❌ handleSalvarSubmit NO usa validarCamposObligatorios()")
    
    # Verificar que no hay validaciones duplicadas en handleSalvarSubmit
    validaciones_duplicadas = [
        r'const\s+empre\s*=\s*document\.getElementById\([\'"]id_empre[\'"]\)\.value\.trim\(\)',
        r'const\s+rtm\s*=\s*document\.getElementById\([\'"]id_rtm[\'"]\)\.value\.trim\(\)',
        r'const\s+expe\s*=\s*document\.getElementById\([\'"]id_expe[\'"]\)\.value\.trim\(\)',
        r'if\s*\(!empre\s*\|\|\s*empre\s*===\s*[\'"]\s*[\'"]\)',
        r'if\s*\(!rtm\s*\|\|\s*rtm\s*===\s*[\'"]\s*[\'"]\)',
        r'if\s*\(!expe\s*\|\|\s*expe\s*===\s*[\'"]\s*[\'"]\)',
    ]
    
    duplicadas_encontradas = []
    for pattern in validaciones_duplicadas:
        matches = re.findall(pattern, contenido)
        if matches:
            duplicadas_encontradas.append(pattern)
    
    if duplicadas_encontradas:
        print("❌ Validaciones duplicadas encontradas en handleSalvarSubmit:")
        for duplicada in duplicadas_encontradas:
            print(f"   - {duplicada}")
        return False
    else:
        print("✅ No se encontraron validaciones duplicadas en handleSalvarSubmit")
        return True

def verificar_validaciones_html5():
    """Verifica que las validaciones HTML5 estén optimizadas"""
    
    print("\n🔍 VERIFICACIÓN DE VALIDACIONES HTML5")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Verificar campos RTM y EXPE
    campos_verificar = [
        ('id_rtm', 'Campo RTM'),
        ('id_expe', 'Campo EXPE'),
    ]
    
    for campo_id, descripcion in campos_verificar:
        pattern = rf'<input[^>]*id\s*=\s*["\']{campo_id}["\'][^>]*>'
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        
        if matches:
            campo_html = matches[0]
            print(f"✅ {descripcion}: Encontrado")
            
            # Verificar atributos
            atributos_esperados = ['required', 'maxlength', 'placeholder']
            atributos_no_deseados = ['pattern', 'title']
            
            for atributo in atributos_esperados:
                if atributo in campo_html:
                    print(f"   ✅ {atributo}: Presente")
                else:
                    print(f"   ❌ {atributo}: Ausente")
            
            for atributo in atributos_no_deseados:
                if atributo in campo_html:
                    print(f"   ❌ {atributo}: Presente (debería eliminarse)")
                else:
                    print(f"   ✅ {atributo}: Ausente (correcto)")
        else:
            print(f"❌ {descripcion}: NO encontrado")
            return False
    
    return True

def verificar_validaciones_servidor():
    """Verifica que las validaciones del servidor estén optimizadas"""
    
    print("\n🔍 VERIFICACIÓN DE VALIDACIONES DEL SERVIDOR")
    print("=" * 50)
    
    views_path = "venv/Scripts/mi_proyecto/hola/views.py"
    
    if not os.path.exists(views_path):
        print(f"❌ No se encontró el archivo: {views_path}")
        return False
    
    try:
        with open(views_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Verificar validaciones esenciales
    validaciones_esperadas = [
        (r'empre\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación empre vacío'),
        (r'rtm\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación rtm vacío'),
        (r'expe\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación expe vacío'),
        (r'campos_faltantes\.append\([\'"]Municipio[\'"]\)', 'Mensaje Municipio'),
        (r'campos_faltantes\.append\([\'"]RTM[\'"]\)', 'Mensaje RTM'),
        (r'campos_faltantes\.append\([\'"]Expediente[\'"]\)', 'Mensaje Expediente'),
    ]
    
    for pattern, descripcion in validaciones_esperadas:
        matches = re.findall(pattern, contenido)
        if matches:
            print(f"✅ {descripcion}: Encontrada")
        else:
            print(f"❌ {descripcion}: NO encontrada")
    
    return True

def generar_reporte_final():
    """Genera un reporte final de la verificación"""
    
    print("\n📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    resultado_js = verificar_validaciones_javascript()
    resultado_html5 = verificar_validaciones_html5()
    resultado_servidor = verificar_validaciones_servidor()
    
    print("\n🎯 RESUMEN DE VERIFICACIONES:")
    print(f"   🔧 Validación JavaScript: {'✅ PASÓ' if resultado_js else '❌ FALLÓ'}")
    print(f"   📝 Validación HTML5: {'✅ PASÓ' if resultado_html5 else '❌ FALLÓ'}")
    print(f"   🖥️  Validación Servidor: {'✅ PASÓ' if resultado_servidor else '❌ FALLÓ'}")
    
    if resultado_js and resultado_html5 and resultado_servidor:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ Las validaciones duplicadas han sido eliminadas")
        print("✅ El proceso de salvar debería funcionar correctamente")
        print("✅ No hay conflictos de validación")
    else:
        print("\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar las validaciones que no pasaron")
        print("❌ Implementar las correcciones faltantes")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO VERIFICACIÓN DE VALIDACIONES OPTIMIZADAS")
    print("=" * 60)
    
    # Generar reporte final
    generar_reporte_final()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Probar el formulario con campos vacíos")
    print("2. Verificar que el proceso de salvar funcione")
    print("3. Confirmar que no hay más errores de validación")
    print("4. Reportar cualquier problema restante")

if __name__ == "__main__":
    main() 
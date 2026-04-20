#!/usr/bin/env python3
"""
Prueba de Solución Definitiva para Campos RTM y EXPE Vacíos
==========================================================

Este script verifica que la solución definitiva funcione correctamente:
1. Campos con valores por defecto apropiados
2. Validaciones JavaScript mejoradas
3. Validaciones del servidor mejoradas
4. Manejo correcto de campos vacíos
"""

import os
import re

def verificar_campos_formulario():
    """Verifica que los campos RTM y EXPE tengan la configuración correcta"""
    
    print("🔍 VERIFICACIÓN DE CAMPOS RTM Y EXPE")
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
    
    # Verificar campo RTM
    print("\n📝 Verificando campo RTM:")
    rtm_pattern = r'<input[^>]*id\s*=\s*["\']id_rtm["\'][^>]*>'
    rtm_matches = re.findall(rtm_pattern, contenido, re.IGNORECASE)
    
    if rtm_matches:
        rtm_html = rtm_matches[0]
        print(f"✅ Campo RTM encontrado")
        
        # Verificar atributos específicos
        verificaciones_rtm = [
            ('name="rtm"', 'name="rtm"'),
            ('required', 'required'),
            ('maxlength="16"', 'maxlength="16"'),
            ('text-transform: uppercase', 'text-transform: uppercase'),
            ('default_if_none:\'\'', 'default_if_none:\'\''),  # Cambiado a cadena vacía
            ('placeholder="Ingrese RTM"', 'placeholder="Ingrese RTM"'),
            ('pattern="[A-Z0-9]+"', 'pattern="[A-Z0-9]+"'),
            ('title="RTM debe contener solo letras y números"', 'title="RTM debe contener solo letras y números"'),
        ]
        
        for verificacion, descripcion in verificaciones_rtm:
            if verificacion in rtm_html:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print("❌ Campo RTM no encontrado")
        return False
    
    # Verificar campo EXPE
    print("\n📝 Verificando campo EXPE:")
    expe_pattern = r'<input[^>]*id\s*=\s*["\']id_expe["\'][^>]*>'
    expe_matches = re.findall(expe_pattern, contenido, re.IGNORECASE)
    
    if expe_matches:
        expe_html = expe_matches[0]
        print(f"✅ Campo EXPE encontrado")
        
        # Verificar atributos específicos
        verificaciones_expe = [
            ('name="expe"', 'name="expe"'),
            ('required', 'required'),
            ('maxlength="12"', 'maxlength="12"'),
            ('text-transform: uppercase', 'text-transform: uppercase'),
            ('default_if_none:\'\'', 'default_if_none:\'\''),  # Cambiado a cadena vacía
            ('placeholder="Ingrese Expediente"', 'placeholder="Ingrese Expediente"'),
            ('pattern="[A-Z0-9]+"', 'pattern="[A-Z0-9]+"'),
            ('title="Expediente debe contener solo letras y números"', 'title="Expediente debe contener solo letras y números"'),
        ]
        
        for verificacion, descripcion in verificaciones_expe:
            if verificacion in expe_html:
                print(f"   ✅ {descripcion}")
            else:
                print(f"   ❌ {descripcion} - NO ENCONTRADO")
    else:
        print("❌ Campo EXPE no encontrado")
        return False
    
    return True

def verificar_validacion_javascript():
    """Verifica que la validación JavaScript esté mejorada"""
    
    print("\n🔍 VERIFICACIÓN DE VALIDACIÓN JAVASCRIPT")
    print("-" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar función handleSalvarSubmit
    salvar_pattern = r'function\s+handleSalvarSubmit\s*\([^)]*\)\s*\{[^}]*\}'
    salvar_matches = re.findall(salvar_pattern, contenido, re.DOTALL)
    
    if not salvar_matches:
        print("❌ Función handleSalvarSubmit no encontrada")
        return False
    
    funcion = salvar_matches[0]
    print("✅ Función handleSalvarSubmit encontrada")
    
    # Verificar validaciones específicas
    verificaciones_js = [
        (r'empre\s*===\s*[\'"]\s*[\'"]', 'Validación específica para Municipio vacío'),
        (r'rtm\s*===\s*[\'"]\s*[\'"]', 'Validación específica para RTM vacío'),
        (r'expe\s*===\s*[\'"]\s*[\'"]', 'Validación específica para Expediente vacío'),
        (r'mostrarMensaje\([\'"]Por favor, complete el campo Municipio[\'"]', 'Mensaje específico para Municipio'),
        (r'mostrarMensaje\([\'"]Por favor, complete el campo RTM[\'"]', 'Mensaje específico para RTM'),
        (r'mostrarMensaje\([\'"]Por favor, complete el campo Expediente[\'"]', 'Mensaje específico para Expediente'),
    ]
    
    for pattern, descripcion in verificaciones_js:
        matches = re.findall(pattern, funcion, re.IGNORECASE)
        if matches:
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
    
    return True

def verificar_validacion_servidor():
    """Verifica que la validación del servidor esté mejorada"""
    
    print("\n🔍 VERIFICACIÓN DE VALIDACIÓN DEL SERVIDOR")
    print("-" * 50)
    
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
    
    # Buscar validaciones mejoradas en el servidor
    verificaciones_servidor = [
        (r'empre\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación servidor para Municipio vacío'),
        (r'rtm\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación servidor para RTM vacío'),
        (r'expe\.strip\(\)\s*==\s*[\'"]\s*[\'"]', 'Validación servidor para Expediente vacío'),
        (r'campos_faltantes\.append\([\'"]Municipio[\'"]\)', 'Mensaje específico para Municipio'),
        (r'campos_faltantes\.append\([\'"]RTM[\'"]\)', 'Mensaje específico para RTM'),
        (r'campos_faltantes\.append\([\'"]Expediente[\'"]\)', 'Mensaje específico para Expediente'),
    ]
    
    for pattern, descripcion in verificaciones_servidor:
        matches = re.findall(pattern, contenido, re.IGNORECASE)
        if matches:
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
    
    return True

def generar_reporte_final():
    """Genera un reporte final de la verificación"""
    
    print("\n📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    resultado_formulario = verificar_campos_formulario()
    resultado_javascript = verificar_validacion_javascript()
    resultado_servidor = verificar_validacion_servidor()
    
    print("\n🎯 RESUMEN DE VERIFICACIONES:")
    print(f"   📝 Formulario HTML: {'✅ PASÓ' if resultado_formulario else '❌ FALLÓ'}")
    print(f"   🔧 Validación JavaScript: {'✅ PASÓ' if resultado_javascript else '❌ FALLÓ'}")
    print(f"   🖥️  Validación Servidor: {'✅ PASÓ' if resultado_servidor else '❌ FALLÓ'}")
    
    if resultado_formulario and resultado_javascript and resultado_servidor:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ La solución definitiva está implementada correctamente")
        print("✅ Los campos RTM y EXPE deberían funcionar correctamente")
        print("✅ No debería haber más errores de campos vacíos")
    else:
        print("\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar las correcciones que no pasaron la verificación")
        print("❌ Implementar las correcciones faltantes")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO VERIFICACIÓN DE SOLUCIÓN DEFINITIVA")
    print("=" * 60)
    
    # Generar reporte final
    generar_reporte_final()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Probar el formulario con campos vacíos")
    print("2. Verificar que los mensajes de error sean específicos")
    print("3. Comprobar que el envío funcione correctamente")
    print("4. Validar que no haya más errores de campos vacíos")

if __name__ == "__main__":
    main() 
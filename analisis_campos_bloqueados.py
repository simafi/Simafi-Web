#!/usr/bin/env python3
"""
Análisis de Campos RTM y EXPE Bloqueados
=========================================

Este script analiza el problema de campos RTM y EXPE que quedan vacíos
cuando están bloqueados/deshabilitados.
"""

import os
import re

def analizar_funcion_bloquear():
    """Analiza la función bloquearCamposRTMExpe()"""
    
    print("🔍 ANÁLISIS DE FUNCIÓN BLOQUEAR CAMPOS")
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
    
    # Buscar función bloquearCamposRTMExpe
    if 'bloquearCamposRTMExpe' in contenido:
        print("✅ Función bloquearCamposRTMExpe encontrada")
        
        # Buscar el código de la función
        pattern = r'function\s+bloquearCamposRTMExpe\s*\([^)]*\)\s*\{[^}]*\}'
        matches = re.findall(pattern, contenido, re.DOTALL)
        
        if matches:
            funcion = matches[0]
            print("📝 Código de la función:")
            print(funcion)
            
            # Verificar si usa disabled
            if 'disabled = true' in funcion:
                print("✅ Usa disabled = true")
            else:
                print("❌ NO usa disabled = true")
            
            # Verificar si cambia el estilo
            if 'backgroundColor' in funcion:
                print("✅ Cambia backgroundColor")
            else:
                print("❌ NO cambia backgroundColor")
        else:
            print("❌ No se pudo extraer el código de la función")
    else:
        print("❌ Función bloquearCamposRTMExpe NO encontrada")
        return False
    
    return True

def analizar_validacion_campos_deshabilitados():
    """Analiza si la validación considera campos deshabilitados"""
    
    print("\n🔍 ANÁLISIS DE VALIDACIÓN CON CAMPOS DESHABILITADOS")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar función validarCamposObligatorios
    if 'validarCamposObligatorios' in contenido:
        print("✅ Función validarCamposObligatorios encontrada")
        
        # Buscar el código de la función
        pattern = r'function\s+validarCamposObligatorios\s*\([^)]*\)\s*\{[^}]*\}'
        matches = re.findall(pattern, contenido, re.DOTALL)
        
        if matches:
            funcion = matches[0]
            
            # Verificar si considera campos deshabilitados
            verificaciones = [
                ('disabled', 'Verifica si campos están deshabilitados'),
                ('readonly', 'Verifica si campos están readonly'),
                ('getAttribute', 'Usa getAttribute para verificar estado'),
                ('element.disabled', 'Verifica propiedad disabled'),
            ]
            
            for verificacion, descripcion in verificaciones:
                if verificacion in funcion:
                    print(f"✅ {descripcion}")
                else:
                    print(f"❌ {descripcion} - NO ENCONTRADO")
            
            # Verificar si solo usa .value.trim()
            if '.value.trim()' in funcion and 'disabled' not in funcion:
                print("⚠️  PROBLEMA: Solo usa .value.trim() sin verificar disabled")
                print("   Los campos deshabilitados pueden tener valores pero no se envían")
        else:
            print("❌ No se pudo extraer el código de la función")
    else:
        print("❌ Función validarCamposObligatorios NO encontrada")
        return False
    
    return True

def analizar_formdata_campos_deshabilitados():
    """Analiza cómo FormData maneja campos deshabilitados"""
    
    print("\n🔍 ANÁLISIS DE FORMDATA CON CAMPOS DESHABILITADOS")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar uso de FormData
    if 'FormData' in contenido:
        print("✅ FormData encontrado en el código")
        
        # Buscar creación de FormData
        pattern = r'new\s+FormData\s*\([^)]*\)'
        matches = re.findall(pattern, contenido)
        
        if matches:
            print(f"✅ FormData creado: {len(matches)} veces")
            
            # Verificar si hay manejo especial para campos deshabilitados
            verificaciones = [
                ('disabled', 'Manejo de campos disabled'),
                ('readonly', 'Manejo de campos readonly'),
                ('append', 'Uso de append para agregar campos'),
                ('set', 'Uso de set para establecer campos'),
            ]
            
            for verificacion, descripcion in verificaciones:
                if verificacion in contenido:
                    print(f"✅ {descripcion}")
                else:
                    print(f"❌ {descripcion} - NO ENCONTRADO")
        else:
            print("❌ No se encontró creación de FormData")
    else:
        print("❌ FormData NO encontrado en el código")
        return False
    
    return True

def identificar_problema_campos_bloqueados():
    """Identifica el problema específico con campos bloqueados"""
    
    print("\n🔍 IDENTIFICACIÓN DEL PROBLEMA")
    print("=" * 50)
    
    # Obtener análisis
    resultado_bloquear = analizar_funcion_bloquear()
    resultado_validacion = analizar_validacion_campos_deshabilitados()
    resultado_formdata = analizar_formdata_campos_deshabilitados()
    
    print("\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"   🔒 Función bloquear: {'✅ PASÓ' if resultado_bloquear else '❌ FALLÓ'}")
    print(f"   🔍 Validación: {'✅ PASÓ' if resultado_validacion else '❌ FALLÓ'}")
    print(f"   📝 FormData: {'✅ PASÓ' if resultado_formdata else '❌ FALLÓ'}")
    
    # Identificar problemas específicos
    problemas = []
    
    if resultado_validacion:
        problemas.append("La validación no considera campos deshabilitados")
    
    if resultado_formdata:
        problemas.append("FormData no maneja campos deshabilitados correctamente")
    
    if problemas:
        print("\n❌ PROBLEMAS IDENTIFICADOS:")
        for problema in problemas:
            print(f"   - {problema}")
    else:
        print("\n✅ No se identificaron problemas específicos")
    
    return problemas

def generar_solucion_campos_bloqueados():
    """Genera solución para campos bloqueados"""
    
    print("\n💡 SOLUCIÓN PARA CAMPOS BLOQUEADOS")
    print("=" * 50)
    
    print("🔧 PROBLEMA IDENTIFICADO:")
    print("   Los campos RTM y EXPE se bloquean con disabled=true")
    print("   Los campos deshabilitados NO se envían en FormData")
    print("   La validación no considera el estado disabled")
    
    print("\n🛠️  SOLUCIONES PROPUESTAS:")
    
    print("\n1. **Modificar validación para considerar campos deshabilitados**:")
    print("```javascript")
    print("function validarCamposObligatorios() {")
    print("    const empre = document.getElementById('id_empre');")
    print("    const rtm = document.getElementById('id_rtm');")
    print("    const expe = document.getElementById('id_expe');")
    print("    ")
    print("    // Verificar si campos están deshabilitados")
    print("    if (rtm.disabled && expe.disabled) {")
    print("        console.log('✅ Campos RTM y EXPE están bloqueados (registro existe)');")
    print("        return true; // Permitir envío si están bloqueados")
    print("    }")
    print("    ")
    print("    // Validación normal para campos habilitados")
    print("    const empreValue = empre.value.trim();")
    print("    const rtmValue = rtm.value.trim();")
    print("    const expeValue = expe.value.trim();")
    print("    ")
    print("    if (!empreValue || empreValue === '') {")
    print("        mostrarMensaje('Por favor, complete el campo Municipio', false);")
    print("        return false;")
    print("    }")
    print("    ")
    print("    if (!rtmValue || rtmValue === '') {")
    print("        mostrarMensaje('Por favor, complete el campo RTM', false);")
    print("        return false;")
    print("    }")
    print("    ")
    print("    if (!expeValue || expeValue === '') {")
    print("        mostrarMensaje('Por favor, complete el campo Expediente', false);")
    print("        return false;")
    print("    }")
    print("    ")
    print("    return true;")
    print("}")
    print("```")
    
    print("\n2. **Modificar FormData para incluir campos deshabilitados**:")
    print("```javascript")
    print("function handleSalvarSubmit() {")
    print("    if (!validarCamposObligatorios()) {")
    print("        return;")
    print("    }")
    print("    ")
    print("    const form = document.querySelector('form');")
    print("    const formData = new FormData(form);")
    print("    ")
    print("    // Agregar campos deshabilitados manualmente")
    print("    const rtm = document.getElementById('id_rtm');")
    print("    const expe = document.getElementById('id_expe');")
    print("    ")
    print("    if (rtm.disabled && rtm.value) {")
    print("        formData.append('rtm', rtm.value);")
    print("    }")
    print("    if (expe.disabled && expe.value) {")
    print("        formData.append('expe', expe.value);")
    print("    }")
    print("    ")
    print("    formData.append('accion', 'salvar');")
    print("    // Continuar con el envío...")
    print("}")
    print("```")
    
    print("\n3. **Alternativa: Usar readonly en lugar de disabled**:")
    print("```javascript")
    print("function bloquearCamposRTMExpe() {")
    print("    const rtmElement = document.getElementById('id_rtm');")
    print("    const expeElement = document.getElementById('id_expe');")
    print("    ")
    print("    if (rtmElement) {")
    print("        rtmElement.readOnly = true; // En lugar de disabled")
    print("        rtmElement.style.backgroundColor = '#f8f9fa';")
    print("        rtmElement.style.color = '#6c757d';")
    print("    }")
    print("    ")
    print("    if (expeElement) {")
    print("        expeElement.readOnly = true; // En lugar de disabled")
    print("        expeElement.style.backgroundColor = '#f8f9fa';")
    print("        expeElement.style.color = '#6c757d';")
    print("    }")
    print("}")
    print("```")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO ANÁLISIS DE CAMPOS BLOQUEADOS")
    print("=" * 60)
    
    # Identificar problemas
    problemas = identificar_problema_campos_bloqueados()
    
    # Generar soluciones
    generar_solucion_campos_bloqueados()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Implementar la solución elegida")
    print("2. Probar con campos bloqueados")
    print("3. Verificar que los valores se envíen correctamente")
    print("4. Confirmar que no hay más errores de validación")

if __name__ == "__main__":
    main() 
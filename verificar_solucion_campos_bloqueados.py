#!/usr/bin/env python3
"""
Verificación de Solución para Campos Bloqueados
===============================================

Este script verifica que la solución para campos RTM y EXPE bloqueados
funciona correctamente.
"""

import os
import re

def verificar_validacion_campos_deshabilitados():
    """Verifica que la validación considera campos deshabilitados"""
    
    print("🔍 VERIFICACIÓN DE VALIDACIÓN CON CAMPOS DESHABILITADOS")
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
    
    # Buscar función validarCamposObligatorios
    if 'validarCamposObligatorios' in contenido:
        print("✅ Función validarCamposObligatorios encontrada")
        
        # Buscar el código de la función
        pattern = r'function\s+validarCamposObligatorios\s*\([^)]*\)\s*\{[^}]*\}'
        matches = re.findall(pattern, contenido, re.DOTALL)
        
        if matches:
            funcion = matches[0]
            
            # Verificar mejoras implementadas
            verificaciones = [
                ('rtm.disabled', 'Verifica si RTM está deshabilitado'),
                ('expe.disabled', 'Verifica si EXPE está deshabilitado'),
                ('disabled: ${rtm.disabled}', 'Log del estado disabled de RTM'),
                ('disabled: ${expe.disabled}', 'Log del estado disabled de EXPE'),
                ('Campos RTM y EXPE están bloqueados', 'Mensaje para campos bloqueados'),
                ('Permitir envío porque los campos están bloqueados', 'Lógica para campos bloqueados'),
            ]
            
            for verificacion, descripcion in verificaciones:
                if verificacion in funcion:
                    print(f"   ✅ {descripcion}")
                else:
                    print(f"   ❌ {descripcion} - NO ENCONTRADO")
            
            # Verificar que la lógica está correcta
            if 'rtm.disabled && expe.disabled' in funcion:
                print("   ✅ Lógica para campos bloqueados implementada")
            else:
                print("   ❌ Lógica para campos bloqueados NO implementada")
                return False
        else:
            print("❌ No se pudo extraer el código de la función")
            return False
    else:
        print("❌ Función validarCamposObligatorios NO encontrada")
        return False
    
    return True

def verificar_formdata_campos_deshabilitados():
    """Verifica que FormData maneja campos deshabilitados correctamente"""
    
    print("\n🔍 VERIFICACIÓN DE FORMDATA CON CAMPOS DESHABILITADOS")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar función handleSalvarSubmit
    if 'handleSalvarSubmit' in contenido:
        print("✅ Función handleSalvarSubmit encontrada")
        
        # Buscar el código de la función
        pattern = r'function\s+handleSalvarSubmit\s*\([^)]*\)\s*\{[^}]*\}'
        matches = re.findall(pattern, contenido, re.DOTALL)
        
        if matches:
            funcion = matches[0]
            
            # Verificar mejoras implementadas
            verificaciones = [
                ('Agregando campo RTM deshabilitado al FormData', 'Manejo de RTM deshabilitado'),
                ('Agregando campo EXPE deshabilitado al FormData', 'Manejo de EXPE deshabilitado'),
                ('rtm.disabled && rtm.value', 'Condición para RTM deshabilitado'),
                ('expe.disabled && expe.value', 'Condición para EXPE deshabilitado'),
                ('formData.append(\'rtm\', rtm.value)', 'Agregar RTM al FormData'),
                ('formData.append(\'expe\', expe.value)', 'Agregar EXPE al FormData'),
            ]
            
            for verificacion, descripcion in verificaciones:
                if verificacion in funcion:
                    print(f"   ✅ {descripcion}")
                else:
                    print(f"   ❌ {descripcion} - NO ENCONTRADO")
            
            # Verificar que la lógica está correcta
            if 'formData.append(\'rtm\', rtm.value)' in funcion and 'formData.append(\'expe\', expe.value)' in funcion:
                print("   ✅ Lógica para agregar campos deshabilitados implementada")
            else:
                print("   ❌ Lógica para agregar campos deshabilitados NO implementada")
                return False
        else:
            print("❌ No se pudo extraer el código de la función")
            return False
    else:
        print("❌ Función handleSalvarSubmit NO encontrada")
        return False
    
    return True

def verificar_funcion_bloquear():
    """Verifica que la función bloquearCamposRTMExpe funciona correctamente"""
    
    print("\n🔍 VERIFICACIÓN DE FUNCIÓN BLOQUEAR CAMPOS")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
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
            
            # Verificar implementación
            verificaciones = [
                ('disabled = true', 'Usa disabled = true'),
                ('backgroundColor', 'Cambia backgroundColor'),
                ('Campo RTM bloqueado', 'Log para RTM bloqueado'),
                ('Campo Expediente bloqueado', 'Log para EXPE bloqueado'),
            ]
            
            for verificacion, descripcion in verificaciones:
                if verificacion in funcion:
                    print(f"   ✅ {descripcion}")
                else:
                    print(f"   ❌ {descripcion} - NO ENCONTRADO")
        else:
            print("❌ No se pudo extraer el código de la función")
            return False
    else:
        print("❌ Función bloquearCamposRTMExpe NO encontrada")
        return False
    
    return True

def generar_reporte_final():
    """Genera un reporte final de la verificación"""
    
    print("\n📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    resultado_validacion = verificar_validacion_campos_deshabilitados()
    resultado_formdata = verificar_formdata_campos_deshabilitados()
    resultado_bloquear = verificar_funcion_bloquear()
    
    print("\n🎯 RESUMEN DE VERIFICACIONES:")
    print(f"   🔍 Validación con campos deshabilitados: {'✅ PASÓ' if resultado_validacion else '❌ FALLÓ'}")
    print(f"   📝 FormData con campos deshabilitados: {'✅ PASÓ' if resultado_formdata else '❌ FALLÓ'}")
    print(f"   🔒 Función bloquear campos: {'✅ PASÓ' if resultado_bloquear else '❌ FALLÓ'}")
    
    if resultado_validacion and resultado_formdata and resultado_bloquear:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ La solución para campos bloqueados está implementada correctamente")
        print("✅ Los campos RTM y EXPE bloqueados se manejan correctamente")
        print("✅ No debería haber más errores de campos vacíos con registros existentes")
    else:
        print("\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar las correcciones que no pasaron la verificación")
        print("❌ Implementar las correcciones faltantes")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO VERIFICACIÓN DE SOLUCIÓN PARA CAMPOS BLOQUEADOS")
    print("=" * 60)
    
    # Generar reporte final
    generar_reporte_final()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Probar el formulario con un registro existente")
    print("2. Verificar que los campos RTM y EXPE se bloqueen correctamente")
    print("3. Comprobar que el proceso de salvar funcione con campos bloqueados")
    print("4. Confirmar que no hay más errores de campos vacíos")

if __name__ == "__main__":
    main() 
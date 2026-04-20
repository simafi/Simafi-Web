#!/usr/bin/env python3
"""
Verificación de Confirmación en Botón Salvar
============================================

Este script verifica que el botón Salvar ahora muestre una confirmación
interactiva antes de proceder, igual que el botón Eliminar.
"""

import os
import re

def verificar_confirmacion_salvar():
    """Verifica que el botón Salvar use confirmación interactiva"""
    
    print("🔍 VERIFICACIÓN DE CONFIRMACIÓN EN BOTÓN SALVAR")
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
    
    # Buscar confirmación en handleSalvarSubmit
    if 'mostrarConfirmacion' in contenido and 'handleSalvarSubmit' in contenido:
        print("✅ Función handleSalvarSubmit encontrada con mostrarConfirmacion")
        
        # Verificar que use mostrarConfirmacion para salvar
        if '¿Está seguro de que desea guardar este negocio?' in contenido:
            print("   ✅ Confirmación de guardado implementada")
        else:
            print("   ❌ Confirmación de guardado NO encontrada")
            return False
        
        # Verificar que no use confirm() nativo para salvar
        if 'confirm(' in contenido and 'guardar' in contenido.lower():
            print("   ❌ Aún usa confirm() nativo para guardar")
            return False
        else:
            print("   ✅ No usa confirm() nativo para guardar")
        
        return True
    else:
        print("❌ Función handleSalvarSubmit con mostrarConfirmacion NO encontrada")
        return False

def verificar_confirmacion_eliminar():
    """Verifica que el botón Eliminar también use confirmación interactiva"""
    
    print("\n🔍 VERIFICACIÓN DE CONFIRMACIÓN EN BOTÓN ELIMINAR")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar confirmación en handleEliminarSubmit
    if 'mostrarConfirmacion' in contenido and 'handleEliminarSubmit' in contenido:
        print("✅ Función handleEliminarSubmit encontrada con mostrarConfirmacion")
        
        # Verificar que use mostrarConfirmacion para eliminar
        if '¿Está seguro de que desea eliminar este negocio?' in contenido:
            print("   ✅ Confirmación de eliminación implementada")
        else:
            print("   ❌ Confirmación de eliminación NO encontrada")
            return False
        
        # Verificar que no use confirm() nativo para eliminar
        if 'confirm(' in contenido and 'eliminar' in contenido.lower():
            print("   ❌ Aún usa confirm() nativo para eliminar")
            return False
        else:
            print("   ✅ No usa confirm() nativo para eliminar")
        
        return True
    else:
        print("❌ Función handleEliminarSubmit con mostrarConfirmacion NO encontrada")
        return False

def verificar_funcion_mostrar_confirmacion():
    """Verifica que la función mostrarConfirmacion esté implementada"""
    
    print("\n🔍 VERIFICACIÓN DE FUNCIÓN MOSTRAR CONFIRMACIÓN")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Verificar elementos clave del modal
    verificaciones = [
        ('modal-confirmacion', 'ID del modal'),
        ('✅ Confirmar', 'Botón confirmar'),
        ('❌ Cancelar', 'Botón cancelar'),
        ('callback(true)', 'Callback de confirmación'),
        ('callback(false)', 'Callback de cancelación'),
        ('handleEscape', 'Manejo de tecla ESC'),
    ]
    
    todas_pasaron = True
    for verificacion, descripcion in verificaciones:
        if verificacion in contenido:
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
            todas_pasaron = False
    
    return todas_pasaron

def generar_reporte_final():
    """Genera un reporte final de la verificación"""
    
    print("\n📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    resultado_salvar = verificar_confirmacion_salvar()
    resultado_eliminar = verificar_confirmacion_eliminar()
    resultado_funcion = verificar_funcion_mostrar_confirmacion()
    
    print("\n🎯 RESUMEN DE VERIFICACIONES:")
    print(f"   💾 Botón Salvar con confirmación: {'✅ PASÓ' if resultado_salvar else '❌ FALLÓ'}")
    print(f"   🗑️  Botón Eliminar con confirmación: {'✅ PASÓ' if resultado_eliminar else '❌ FALLÓ'}")
    print(f"   🔔 Función mostrarConfirmacion: {'✅ PASÓ' if resultado_funcion else '❌ FALLÓ'}")
    
    if resultado_salvar and resultado_eliminar and resultado_funcion:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ Ambos botones (Salvar y Eliminar) usan confirmación interactiva")
        print("✅ Se eliminó el uso de confirm() nativo")
        print("✅ Modal personalizado implementado correctamente")
        print("✅ Experiencia de usuario consistente")
    else:
        print("\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar las implementaciones faltantes")
        print("❌ Asegurar que ambos botones usen mostrarConfirmacion")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO VERIFICACIÓN DE CONFIRMACIÓN EN BOTONES")
    print("=" * 60)
    
    # Generar reporte final
    generar_reporte_final()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Probar el botón Salvar con datos del formulario")
    print("2. Verificar que aparezca el modal de confirmación")
    print("3. Probar el botón Eliminar con datos del formulario")
    print("4. Confirmar que ambos usen el mismo modal personalizado")
    print("5. Verificar que no se use confirm() nativo")

if __name__ == "__main__":
    main() 
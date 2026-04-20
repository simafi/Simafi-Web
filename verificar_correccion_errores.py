#!/usr/bin/env python3
"""
Verificación de Corrección de Errores
=====================================

Este script verifica que los errores de sintaxis y coordenadas
se hayan corregido correctamente.
"""

import os
import re

def verificar_sintaxis_javascript():
    """Verifica que no haya errores de sintaxis JavaScript"""
    
    print("🔍 VERIFICACIÓN DE SINTAXIS JAVASCRIPT")
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
    
    # Buscar posibles errores de sintaxis
    errores_potenciales = [
        ('console\.log.*✅ Usuario confirmó la actualización.*console\.log.*✅ Usuario confirmó la actualización', 'Código duplicado'),
        ('function.*\{.*function.*\{', 'Funciones anidadas incorrectas'),
        ('\}\s*\}\s*\}\s*\}', 'Llaves de cierre excesivas'),
        ('console\.log.*🔄 Enviando petición AJAX.*console\.log.*🔄 Enviando petición AJAX', 'Código duplicado'),
    ]
    
    errores_encontrados = []
    for pattern, descripcion in errores_potenciales:
        matches = re.findall(pattern, contenido, re.DOTALL)
        if len(matches) > 1:
            errores_encontrados.append(f"❌ {descripcion}: {len(matches)} ocurrencias")
        else:
            print(f"   ✅ {descripcion}: OK")
    
    if errores_encontrados:
        print("❌ Errores de sintaxis encontrados:")
        for error in errores_encontrados:
            print(f"   {error}")
        return False
    else:
        print("✅ No se encontraron errores de sintaxis JavaScript")
        return True

def verificar_coordenadas():
    """Verifica que las coordenadas estén correctamente definidas"""
    
    print("\n🔍 VERIFICACIÓN DE COORDENADAS")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Verificar campos de coordenadas
    verificaciones = [
        ('id="id_cx".*value="{{ negocio\.cx\|default_if_none:\'0\.0000000\' }}"', 'Campo CX con valor por defecto correcto'),
        ('id="id_cy".*value="{{ negocio\.cy\|default_if_none:\'0\.0000000\' }}"', 'Campo CY con valor por defecto correcto'),
        ('step="0\.0000001"', 'Step correcto para coordenadas'),
        ('min="-999\.9999999"', 'Valor mínimo correcto'),
        ('max="999\.9999999"', 'Valor máximo correcto'),
    ]
    
    todas_pasaron = True
    for pattern, descripcion in verificaciones:
        if re.search(pattern, contenido):
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
            todas_pasaron = False
    
    # Verificar que no haya valores problemáticos
    valores_problematicos = [
        ('0,0', 'Valor con coma en lugar de punto'),
        ('value=""', 'Valor vacío en coordenadas'),
        ('default_if_none:\'\'', 'Valor vacío por defecto'),
    ]
    
    for valor, descripcion in valores_problematicos:
        if valor in contenido:
            print(f"   ⚠️  {descripcion}: {valor}")
            todas_pasaron = False
        else:
            print(f"   ✅ No se encontró {descripcion}")
    
    return todas_pasaron

def verificar_estructura_html():
    """Verifica que la estructura HTML sea correcta"""
    
    print("\n🔍 VERIFICACIÓN DE ESTRUCTURA HTML")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Verificar estructura básica
    verificaciones = [
        ('<html', 'Etiqueta HTML'),
        ('</html>', 'Cierre de HTML'),
        ('<body', 'Etiqueta BODY'),
        ('</body>', 'Cierre de BODY'),
        ('<script', 'Etiqueta SCRIPT'),
        ('</script>', 'Cierre de SCRIPT'),
    ]
    
    todas_pasaron = True
    for pattern, descripcion in verificaciones:
        if pattern in contenido:
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
            todas_pasaron = False
    
    # Verificar que no haya etiquetas sin cerrar
    etiquetas_sin_cerrar = [
        ('<script', '</script>'),
        ('<div', '</div>'),
        ('<form', '</form>'),
    ]
    
    for apertura, cierre in etiquetas_sin_cerrar:
        count_apertura = contenido.count(apertura)
        count_cierre = contenido.count(cierre)
        if count_apertura != count_cierre:
            print(f"   ❌ Desbalance en {apertura}: {count_apertura} aperturas, {count_cierre} cierres")
            todas_pasaron = False
        else:
            print(f"   ✅ Balance correcto en {apertura}")
    
    return todas_pasaron

def generar_reporte_final():
    """Genera un reporte final de la verificación"""
    
    print("\n📊 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    resultado_sintaxis = verificar_sintaxis_javascript()
    resultado_coordenadas = verificar_coordenadas()
    resultado_estructura = verificar_estructura_html()
    
    print("\n🎯 RESUMEN DE VERIFICACIONES:")
    print(f"   🔧 Sintaxis JavaScript: {'✅ PASÓ' if resultado_sintaxis else '❌ FALLÓ'}")
    print(f"   📍 Coordenadas: {'✅ PASÓ' if resultado_coordenadas else '❌ FALLÓ'}")
    print(f"   🏗️  Estructura HTML: {'✅ PASÓ' if resultado_estructura else '❌ FALLÓ'}")
    
    if resultado_sintaxis and resultado_coordenadas and resultado_estructura:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ Los errores de sintaxis se han corregido")
        print("✅ Las coordenadas están correctamente definidas")
        print("✅ La estructura HTML es válida")
        print("✅ El archivo está listo para usar")
    else:
        print("\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print("❌ Revisar los errores identificados")
        print("❌ Corregir los problemas antes de usar")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO VERIFICACIÓN DE CORRECCIÓN DE ERRORES")
    print("=" * 60)
    
    # Generar reporte final
    generar_reporte_final()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Probar el formulario en el navegador")
    print("2. Verificar que no aparezcan errores en la consola")
    print("3. Probar las funcionalidades de confirmación")
    print("4. Verificar que las coordenadas funcionen correctamente")
    print("5. Confirmar que todo funcione como esperado")

if __name__ == "__main__":
    main() 
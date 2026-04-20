#!/usr/bin/env python3
"""
Diagnóstico de Problema de Guardado
===================================

Este script diagnostica por qué el botón Salvar no está guardando
en la base de datos correctamente.
"""

import os
import re

def verificar_campos_formulario():
    """Verifica que todos los campos necesarios estén presentes en el formulario"""
    
    print("🔍 VERIFICACIÓN DE CAMPOS DEL FORMULARIO")
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
    
    # Campos obligatorios que deben estar en el formulario
    campos_obligatorios = [
        ('id_empre', 'Municipio'),
        ('id_rtm', 'RTM'),
        ('id_expe', 'Expediente'),
    ]
    
    # Campos adicionales importantes
    campos_adicionales = [
        ('id_nombrenego', 'Nombre del Negocio'),
        ('id_comerciante', 'Comerciante'),
        ('id_identidad', 'Identidad'),
        ('id_rtnpersonal', 'RTN Personal'),
        ('id_rtnnego', 'RTN Negocio'),
        ('id_catastral', 'Catastral'),
        ('id_identidadrep', 'Identidad Representante'),
        ('id_representante', 'Representante'),
        ('id_direccion', 'Dirección'),
        ('id_actividad', 'Actividad'),
        ('id_estatus', 'Estado'),
        ('id_cx', 'Coordenada X'),
        ('id_cy', 'Coordenada Y'),
    ]
    
    print("📋 CAMPOS OBLIGATORIOS:")
    todos_presentes = True
    for campo_id, descripcion in campos_obligatorios:
        if f'id="{campo_id}"' in contenido:
            print(f"   ✅ {descripcion} ({campo_id})")
        else:
            print(f"   ❌ {descripcion} ({campo_id}) - NO ENCONTRADO")
            todos_presentes = False
    
    print("\n📋 CAMPOS ADICIONALES:")
    for campo_id, descripcion in campos_adicionales:
        if f'id="{campo_id}"' in contenido:
            print(f"   ✅ {descripcion} ({campo_id})")
        else:
            print(f"   ⚠️  {descripcion} ({campo_id}) - NO ENCONTRADO")
    
    return todos_presentes

def verificar_enviado_formdata():
    """Verifica que el FormData esté enviando todos los campos correctamente"""
    
    print("\n🔍 VERIFICACIÓN DE ENVÍO DE FORMDATA")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar el código de envío de FormData
    verificaciones = [
        ('FormData(form)', 'FormData creado correctamente'),
        ('formData.append', 'Campos agregados al FormData'),
        ('formData.append(\'accion\', \'salvar\')', 'Acción salvar agregada'),
        ('formData.append(\'rtm\', rtm.value)', 'Campo RTM agregado manualmente'),
        ('formData.append(\'expe\', expe.value)', 'Campo EXPE agregado manualmente'),
        ('for (let [key, value] of formData.entries())', 'Iteración sobre FormData'),
        ('urlParams.append(key, value)', 'Datos convertidos a URLSearchParams'),
    ]
    
    todas_pasaron = True
    for pattern, descripcion in verificaciones:
        if pattern in contenido:
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
            todas_pasaron = False
    
    return todas_pasaron

def verificar_peticion_ajax():
    """Verifica que la petición AJAX esté configurada correctamente"""
    
    print("\n🔍 VERIFICACIÓN DE PETICIÓN AJAX")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Verificar configuración de AJAX
    verificaciones = [
        ('XMLHttpRequest()', 'XMLHttpRequest creado'),
        ('xhr.open(\'POST\'', 'Método POST configurado'),
        ('xhr.setRequestHeader(\'X-Requested-With\', \'XMLHttpRequest\')', 'Header AJAX configurado'),
        ('xhr.setRequestHeader(\'Content-Type\', \'application/x-www-form-urlencoded\')', 'Content-Type configurado'),
        ('xhr.onreadystatechange', 'Event handler configurado'),
        ('xhr.readyState === 4', 'Verificación de estado'),
        ('xhr.send(urlParams.toString())', 'Envío de datos'),
    ]
    
    todas_pasaron = True
    for pattern, descripcion in verificaciones:
        if pattern in contenido:
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
            todas_pasaron = False
    
    return todas_pasaron

def verificar_manejo_respuesta():
    """Verifica que el manejo de respuesta esté correcto"""
    
    print("\n🔍 VERIFICACIÓN DE MANEJO DE RESPUESTA")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Verificar manejo de respuesta
    verificaciones = [
        ('JSON.parse(xhr.responseText)', 'Parsing de respuesta JSON'),
        ('data.exito', 'Verificación de éxito'),
        ('data.mensaje', 'Manejo de mensaje'),
        ('mostrarMensaje(data.mensaje', 'Mostrar mensaje al usuario'),
        ('data.requiere_confirmacion', 'Manejo de confirmación'),
        ('data.existe', 'Verificación de existencia'),
    ]
    
    todas_pasaron = True
    for pattern, descripcion in verificaciones:
        if pattern in contenido:
            print(f"   ✅ {descripcion}")
        else:
            print(f"   ❌ {descripcion} - NO ENCONTRADO")
            todas_pasaron = False
    
    return todas_pasaron

def verificar_logs_consola():
    """Verifica que haya logs de consola para debugging"""
    
    print("\n🔍 VERIFICACIÓN DE LOGS DE CONSOLA")
    print("=" * 50)
    
    formulario_path = "venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html"
    
    try:
        with open(formulario_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Buscar logs importantes
    logs_importantes = [
        ('console.log(\'🔄 Iniciando handleSalvarSubmit\')', 'Inicio de función'),
        ('console.log(\'✅ Usuario confirmó el guardado\')', 'Confirmación de usuario'),
        ('console.log(\'✅ FormData creado\')', 'FormData creado'),
        ('console.log(\'Enviando petición AJAX\')', 'Envío de petición'),
        ('console.log(\'Status de respuesta\')', 'Status de respuesta'),
        ('console.log(\'Respuesta del servidor\')', 'Respuesta del servidor'),
        ('console.log(\'❌ Error del servidor\')', 'Manejo de errores'),
    ]
    
    logs_encontrados = 0
    for pattern, descripcion in logs_importantes:
        if pattern in contenido:
            print(f"   ✅ {descripcion}")
            logs_encontrados += 1
        else:
            print(f"   ⚠️  {descripcion} - NO ENCONTRADO")
    
    return logs_encontrados >= 5  # Al menos 5 logs importantes

def generar_diagnostico():
    """Genera un diagnóstico completo"""
    
    print("🚀 INICIANDO DIAGNÓSTICO DE PROBLEMA DE GUARDADO")
    print("=" * 60)
    
    # Ejecutar todas las verificaciones
    resultado_campos = verificar_campos_formulario()
    resultado_formdata = verificar_enviado_formdata()
    resultado_ajax = verificar_peticion_ajax()
    resultado_respuesta = verificar_manejo_respuesta()
    resultado_logs = verificar_logs_consola()
    
    print("\n📊 DIAGNÓSTICO FINAL")
    print("=" * 50)
    
    print(f"   📋 Campos del formulario: {'✅ OK' if resultado_campos else '❌ PROBLEMA'}")
    print(f"   📦 Envío de FormData: {'✅ OK' if resultado_formdata else '❌ PROBLEMA'}")
    print(f"   🌐 Configuración AJAX: {'✅ OK' if resultado_ajax else '❌ PROBLEMA'}")
    print(f"   📨 Manejo de respuesta: {'✅ OK' if resultado_respuesta else '❌ PROBLEMA'}")
    print(f"   🔍 Logs de debugging: {'✅ OK' if resultado_logs else '⚠️  INSUFICIENTES'}")
    
    if resultado_campos and resultado_formdata and resultado_ajax and resultado_respuesta:
        print("\n🎉 ¡CONFIGURACIÓN CORRECTA!")
        print("✅ El código JavaScript parece estar bien configurado")
        print("✅ El problema puede estar en:")
        print("   - Validación de campos en el servidor")
        print("   - Problemas de base de datos")
        print("   - Errores en el servidor Django")
        print("   - Problemas de permisos")
    else:
        print("\n⚠️  PROBLEMAS DETECTADOS")
        print("❌ Hay problemas en la configuración del JavaScript")
        print("❌ Revisar las verificaciones que fallaron")
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Abrir la consola del navegador (F12)")
    print("2. Intentar guardar un negocio")
    print("3. Revisar los logs en la consola")
    print("4. Verificar si hay errores JavaScript")
    print("5. Revisar la pestaña Network para ver la petición AJAX")
    print("6. Verificar la respuesta del servidor")

def main():
    """Función principal"""
    generar_diagnostico()

if __name__ == "__main__":
    main() 
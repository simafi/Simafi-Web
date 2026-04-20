#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de carga de actividades
en el formulario de misceláneos.
"""

import os
import sys
import django
import requests
import json

# Configurar Django
sys.path.append('venv/Scripts/tributario')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_cargar_actividades_ajax():
    """Prueba la carga de actividades via AJAX"""
    print("🔍 PRUEBA DE CARGA DE ACTIVIDADES AJAX")
    print("=" * 50)
    
    # URL de la vista AJAX
    url = 'http://127.0.0.1:8080/tributario/ajax/cargar-actividades/'
    
    # Código de municipio de prueba
    municipio_prueba = '0301'
    
    print(f"📋 Probando carga de actividades para municipio: {municipio_prueba}")
    
    try:
        # Realizar petición GET
        params = {'empresa': municipio_prueba}
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 URL: {response.url}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Respuesta JSON válida")
                
                if data.get('exito'):
                    actividades = data.get('actividades', [])
                    print(f"✅ Actividades cargadas: {len(actividades)} encontradas")
                    
                    if actividades:
                        print("📋 Primeras 5 actividades:")
                        for i, act in enumerate(actividades[:5]):
                            print(f"   {i+1}. {act['codigo']} - {act['descripcion']}")
                    else:
                        print("⚠️ No se encontraron actividades para este municipio")
                        
                else:
                    print(f"❌ Error en la respuesta: {data.get('mensaje', 'Mensaje no disponible')}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error al decodificar JSON: {e}")
                print(f"📄 Respuesta del servidor: {response.text[:200]}")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📄 Respuesta del servidor: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
    except requests.exceptions.Timeout:
        print("❌ Error de timeout: La petición tardó demasiado")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_formulario_miscelaneos_actividades():
    """Prueba el acceso al formulario de misceláneos y verifica la funcionalidad de actividades"""
    print("\n📝 PRUEBA DE FORMULARIO DE MISCELÁNEOS - ACTIVIDADES")
    print("=" * 60)
    
    url = 'http://127.0.0.1:8080/tributario/miscelaneos/'
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Formulario de misceláneos accesible")
            
            # Verificar que contenga elementos importantes
            content = response.text
            
            # Verificar campo empresa (municipio)
            if 'id="empresa"' in content:
                print("✅ Campo empresa (municipio) encontrado en el formulario")
            else:
                print("❌ Campo empresa (municipio) no encontrado")
                
            # Verificar combobox de códigos
            if 'codigo-select' in content:
                print("✅ Combobox de códigos encontrado en el formulario")
            else:
                print("❌ Combobox de códigos no encontrado")
                
            # Verificar función JavaScript de carga de actividades
            if 'cargarActividadesPorEmpresa()' in content:
                print("✅ Función JavaScript cargarActividadesPorEmpresa() encontrada")
            else:
                print("❌ Función JavaScript cargarActividadesPorEmpresa() no encontrada")
                
            # Verificar función JavaScript de autocompletar descripción
            if 'autocompletarDescripcion' in content:
                print("✅ Función JavaScript autocompletarDescripcion() encontrada")
            else:
                print("❌ Función JavaScript autocompletarDescripcion() no encontrada")
                
            # Verificar URL de carga de actividades
            if '/tributario/ajax/cargar-actividades/' in content:
                print("✅ URL de carga de actividades correcta en JavaScript")
            else:
                print("❌ URL de carga de actividades incorrecta o no encontrada")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_buscar_actividad_ajax():
    """Prueba la búsqueda de actividad por código via AJAX"""
    print("\n🔍 PRUEBA DE BÚSQUEDA DE ACTIVIDAD AJAX")
    print("=" * 50)
    
    # URL de la vista AJAX
    url = 'http://127.0.0.1:8080/tributario/ajax/buscar-actividad/'
    
    # Datos de prueba
    municipio_prueba = '0301'
    codigo_prueba = '001'  # Código de actividad de prueba
    
    print(f"📋 Probando búsqueda de actividad: municipio={municipio_prueba}, código={codigo_prueba}")
    
    try:
        # Realizar petición GET
        params = {'empresa': municipio_prueba, 'codigo': codigo_prueba}
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 URL: {response.url}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Respuesta JSON válida")
                
                if data.get('exito'):
                    descripcion = data.get('descripcion', '')
                    print(f"✅ Actividad encontrada: {descripcion}")
                else:
                    print(f"ℹ️ Actividad no encontrada: {data.get('mensaje', 'Mensaje no disponible')}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error al decodificar JSON: {e}")
                print(f"📄 Respuesta del servidor: {response.text[:200]}")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📄 Respuesta del servidor: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
    except requests.exceptions.Timeout:
        print("❌ Error de timeout: La petición tardó demasiado")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE ACTIVIDADES EN MISCELÁNEOS")
    print("=" * 70)
    
    # Prueba 1: Verificar carga de actividades via AJAX
    test_cargar_actividades_ajax()
    
    # Prueba 2: Verificar formulario de misceláneos
    test_formulario_miscelaneos_actividades()
    
    # Prueba 3: Verificar búsqueda de actividad via AJAX
    test_buscar_actividad_ajax()
    
    print("\n" + "=" * 70)
    print("🏁 PRUEBAS COMPLETADAS")
    print("\n📝 INSTRUCCIONES PARA PROBAR MANUALMENTE:")
    print("1. Abra el navegador y vaya a: http://127.0.0.1:8080/tributario/miscelaneos/")
    print("2. Verifique que el campo 'Municipio' muestre el código correcto")
    print("3. Verifique que el combobox 'Código' se llene con las actividades del municipio")
    print("4. Seleccione una actividad y verifique que se autocomplete la descripción")
    print("5. Complete el resto del formulario y pruebe el envío")

if __name__ == '__main__':
    main()

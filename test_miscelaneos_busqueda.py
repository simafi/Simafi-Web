#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de búsqueda por tarjeta de identidad
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

def test_busqueda_identificacion():
    """Prueba la búsqueda de identificación por DNI"""
    print("🔍 PRUEBA DE BÚSQUEDA DE IDENTIFICACIÓN")
    print("=" * 50)
    
    # URL de la vista de búsqueda
    url = 'http://127.0.0.1:8080/tributario/buscar-identificacion/'
    
    # DNI de prueba (debe existir en la base de datos)
    dni_prueba = '0318-1970-01003'
    
    print(f"📋 Probando búsqueda con DNI: {dni_prueba}")
    
    try:
        # Realizar petición POST
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'identidad': dni_prueba
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Respuesta: {json.dumps(result, indent=2)}")
            
            if result.get('exito'):
                print("✅ Búsqueda exitosa")
                identificacion = result.get('identificacion', {})
                print(f"   Nombre: {identificacion.get('nombre_completo', 'N/A')}")
                print(f"   DNI: {identificacion.get('identidad', 'N/A')}")
            else:
                print(f"❌ Búsqueda fallida: {result.get('mensaje', 'Error desconocido')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        print("   Asegúrese de que el servidor esté ejecutándose en http://127.0.0.1:8080")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_formulario_miscelaneos():
    """Prueba el acceso al formulario de misceláneos"""
    print("\n📝 PRUEBA DE ACCESO AL FORMULARIO DE MISCELÁNEOS")
    print("=" * 50)
    
    url = 'http://127.0.0.1:8080/tributario/miscelaneos/'
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Formulario de misceláneos accesible")
            
            # Verificar que contenga elementos importantes
            content = response.text
            
            if 'id="dni"' in content:
                print("✅ Campo DNI encontrado en el formulario")
            else:
                print("❌ Campo DNI no encontrado")
                
            if 'buscarContribuyente()' in content:
                print("✅ Función JavaScript buscarContribuyente() encontrada")
            else:
                print("❌ Función JavaScript buscarContribuyente() no encontrada")
                
            if 'id="id_nombre"' in content:
                print("✅ Campo nombre encontrado en el formulario")
            else:
                print("❌ Campo nombre no encontrado")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_datos_identificacion():
    """Prueba la existencia de datos en la tabla de identificación"""
    print("\n🗄️ PRUEBA DE DATOS EN TABLA DE IDENTIFICACIÓN")
    print("=" * 50)
    
    try:
        from tributario_app.models import Identificacion
        
        # Contar registros
        total_registros = Identificacion.objects.count()
        print(f"📊 Total de registros en tabla identificación: {total_registros}")
        
        if total_registros > 0:
            # Mostrar algunos ejemplos
            print("\n📋 Ejemplos de registros:")
            for i, ident in enumerate(Identificacion.objects.all()[:5]):
                print(f"   {i+1}. DNI: {ident.identidad} | Nombre: {ident.nombres} {ident.apellidos}")
        else:
            print("⚠️ No hay registros en la tabla de identificación")
            print("   Para probar la funcionalidad, agregue algunos registros de prueba")
            
    except Exception as e:
        print(f"❌ Error al acceder a la base de datos: {str(e)}")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE MISCELÁNEOS")
    print("=" * 60)
    
    # Prueba 1: Verificar datos en la base de datos
    test_datos_identificacion()
    
    # Prueba 2: Verificar acceso al formulario
    test_formulario_miscelaneos()
    
    # Prueba 3: Verificar búsqueda de identificación
    test_busqueda_identificacion()
    
    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")
    print("\n📝 INSTRUCCIONES PARA PROBAR MANUALMENTE:")
    print("1. Abra el navegador y vaya a: http://127.0.0.1:8080/tributario/miscelaneos/")
    print("2. En el campo DNI, ingrese un número de identidad válido")
    print("3. Presione el botón 'Buscar' o presione Enter")
    print("4. Verifique que el campo 'Nombre' se llene automáticamente")
    print("5. Complete el resto del formulario y pruebe el envío")

if __name__ == '__main__':
    main()

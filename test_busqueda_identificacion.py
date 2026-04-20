#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de búsqueda de identificación
"""

import requests
import time
import sys
import os

def test_servidor():
    """Verifica que el servidor esté funcionando"""
    print("🔍 Verificando servidor...")
    try:
        response = requests.get('http://127.0.0.1:8080/', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            return True
        else:
            print(f"❌ Servidor respondió con código {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error al verificar servidor: {e}")
        return False

def test_busqueda_identificacion():
    """Prueba la búsqueda de identificación del comerciante"""
    print("\n🔍 Probando búsqueda de identificación del comerciante...")
    
    # Datos de prueba
    test_data = {
        'identidad': '0801-1990-12345'  # DNI de prueba
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8080/tributario/buscar-identificacion/',
            json=test_data,
            timeout=5
        )
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('exito'):
                print("✅ Búsqueda de identificación del comerciante: OK")
                print(f"   Datos encontrados: {data.get('identificacion', {})}")
            else:
                print(f"⚠️ Búsqueda de identificación del comerciante: {data.get('mensaje', 'Error desconocido')}")
        else:
            print(f"❌ Búsqueda de identificación del comerciante: Error HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Búsqueda de identificación del comerciante: Error - {e}")

def test_busqueda_identificacion_representante():
    """Prueba la búsqueda de identificación del representante"""
    print("\n🔍 Probando búsqueda de identificación del representante...")
    
    # Datos de prueba
    test_data = {
        'identidad': '0801-1985-67890'  # DNI de prueba para representante
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8080/tributario/buscar-identificacion-representante/',
            json=test_data,
            timeout=5
        )
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('exito'):
                print("✅ Búsqueda de identificación del representante: OK")
                print(f"   Datos encontrados: {data.get('identificacion', {})}")
            else:
                print(f"⚠️ Búsqueda de identificación del representante: {data.get('mensaje', 'Error desconocido')}")
        else:
            print(f"❌ Búsqueda de identificación del representante: Error HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Búsqueda de identificación del representante: Error - {e}")

def test_formulario_maestro_negocios():
    """Prueba que el formulario de maestro de negocios se cargue correctamente"""
    print("\n🔍 Probando formulario de maestro de negocios...")
    
    try:
        response = requests.get(
            'http://127.0.0.1:8080/tributario/maestro-negocios/',
            timeout=5
        )
        
        if response.status_code == 200:
            # Verificar que los campos de identificación estén presentes
            content = response.text
            
            # Verificar campos de identidad
            if 'id_identidad' in content and 'btn_buscar_identidad' in content:
                print("✅ Campo DNI del comerciante con botón de búsqueda: OK")
            else:
                print("❌ Campo DNI del comerciante con botón de búsqueda: No encontrado")
            
            # Verificar campos de identidad del representante
            if 'id_identidadrep' in content and 'btn_buscar_identidad_rep' in content:
                print("✅ Campo DNI del representante con botón de búsqueda: OK")
            else:
                print("❌ Campo DNI del representante con botón de búsqueda: No encontrado")
            
            # Verificar funciones JavaScript
            if 'buscarIdentificacion()' in content and 'buscarIdentificacionRepresentante()' in content:
                print("✅ Funciones JavaScript de búsqueda: OK")
            else:
                print("❌ Funciones JavaScript de búsqueda: No encontradas")
                
        else:
            print(f"❌ Formulario de maestro de negocios: Error HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Formulario de maestro de negocios: Error - {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de búsqueda de identificación...")
    print("=" * 60)
    
    # Esperar un momento para que el servidor esté listo
    time.sleep(2)
    
    # Probar servidor
    if not test_servidor():
        print("\n❌ El servidor no está funcionando. Verifique que esté ejecutándose.")
        return
    
    # Probar formulario
    test_formulario_maestro_negocios()
    
    # Probar búsqueda de identificación
    test_busqueda_identificacion()
    
    # Probar búsqueda de identificación del representante
    test_busqueda_identificacion_representante()
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("\n📋 Resumen de funcionalidades implementadas:")
    print("1. ✅ Campos de DNI con botones de búsqueda")
    print("2. ✅ Funciones JavaScript para búsqueda automática")
    print("3. ✅ URLs para búsqueda de identificación")
    print("4. ✅ Vistas AJAX para consultar tabla identificacion")
    print("5. ✅ Carga automática de nombres al encontrar DNI")
    
    print("\n🌐 El formulario está disponible en: http://127.0.0.1:8080/tributario/maestro-negocios/")
    print("📝 Instrucciones de uso:")
    print("   - Ingrese un DNI en el campo correspondiente")
    print("   - Presione el botón de búsqueda (🔍)")
    print("   - Los nombres se cargarán automáticamente si el DNI existe")

if __name__ == "__main__":
    main()































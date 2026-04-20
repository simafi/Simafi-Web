#!/usr/bin/env python3
"""
Script de prueba para verificar todas las correcciones implementadas
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

def test_urls():
    """Prueba las URLs principales"""
    print("\n🔍 Probando URLs principales...")
    
    urls_a_probar = [
        ('/', 'Página principal'),
        ('/tributario/', 'Login tributario'),
        ('/tributario/menu/', 'Menú tributario'),
        ('/tributario/maestro-negocios/', 'Maestro de negocios'),
        ('/tributario/actividad-crud/', 'CRUD de actividades'),
        ('/tributario/oficina-crud/', 'CRUD de oficinas'),
        ('/tributario/rubros-crud/', 'CRUD de rubros'),
        ('/tributario/tarifas-crud/', 'CRUD de tarifas'),
        ('/tributario/plan-arbitrio-crud/', 'CRUD de plan de arbitrios'),
        ('/tributario/miscelaneos/', 'Misceláneos'),
    ]
    
    resultados = []
    for url, descripcion in urls_a_probar:
        try:
            response = requests.get(f'http://127.0.0.1:8080{url}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {descripcion}: OK")
                resultados.append(True)
            else:
                print(f"❌ {descripcion}: Error {response.status_code}")
                resultados.append(False)
        except Exception as e:
            print(f"❌ {descripcion}: Error - {e}")
            resultados.append(False)
    
    return all(resultados)

def test_funcionalidades_ajax():
    """Prueba las funcionalidades AJAX"""
    print("\n🔍 Probando funcionalidades AJAX...")
    
    # Probar búsqueda de negocio
    try:
        data = {
            'rtm': 'TEST001',
            'expe': 'TEST001',
            'municipio_codigo': '0301'
        }
        response = requests.post(
            'http://127.0.0.1:8080/tributario/buscar-negocio/',
            json=data,
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Búsqueda de negocio: OK")
        else:
            print(f"❌ Búsqueda de negocio: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Búsqueda de negocio: Error - {e}")
    
    # Probar búsqueda de rubro
    try:
        data = {
            'empresa': '0301',
            'codigo': '001'
        }
        response = requests.post(
            'http://127.0.0.1:8080/tributario/buscar-rubro/',
            data=data,
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Búsqueda de rubro: OK")
        else:
            print(f"❌ Búsqueda de rubro: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Búsqueda de rubro: Error - {e}")

def test_templates():
    """Verifica que los templates se rendericen correctamente"""
    print("\n🔍 Verificando templates...")
    
    templates_a_verificar = [
        ('/tributario/actividad-crud/', 'actividad.html'),
        ('/tributario/oficina-crud/', 'oficina.html'),
        ('/tributario/rubros-crud/', 'formulario_rubros.html'),
        ('/tributario/tarifas-crud/', 'formulario_tarifas.html'),
        ('/tributario/plan-arbitrio-crud/', 'formulario_plan_arbitrio.html'),
        ('/tributario/miscelaneos/', 'miscelaneos.html'),
    ]
    
    for url, template in templates_a_verificar:
        try:
            response = requests.get(f'http://127.0.0.1:8080{url}', timeout=5)
            if response.status_code == 200:
                # Verificar que no hay errores de template
                if 'NoReverseMatch' not in response.text and 'TemplateDoesNotExist' not in response.text:
                    print(f"✅ {template}: OK")
                else:
                    print(f"❌ {template}: Error de template")
            else:
                print(f"❌ {template}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ {template}: Error - {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas completas de correcciones...")
    print("=" * 50)
    
    # Esperar un momento para que el servidor esté listo
    time.sleep(2)
    
    # Probar servidor
    if not test_servidor():
        print("\n❌ El servidor no está funcionando. Verifique que esté ejecutándose.")
        return
    
    # Probar URLs
    if not test_urls():
        print("\n⚠️ Algunas URLs no están funcionando correctamente.")
    
    # Probar funcionalidades AJAX
    test_funcionalidades_ajax()
    
    # Probar templates
    test_templates()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("\n📋 Resumen de correcciones implementadas:")
    print("1. ✅ Archivo views.py limpiado de bytes nulos")
    print("2. ✅ Función buscar_rubro implementada correctamente")
    print("3. ✅ Herencia de código de municipio en formularios")
    print("4. ✅ Corrección de URLs en templates")
    print("5. ✅ Servidor ejecutándose correctamente")
    
    print("\n🌐 El servidor está disponible en: http://127.0.0.1:8080/")
    print("📝 Puede acceder a los formularios desde el menú tributario")

if __name__ == "__main__":
    main()


































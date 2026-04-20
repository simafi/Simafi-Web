#!/usr/bin/env python
"""
Test para diagnosticar el error de sintaxis JSON en búsqueda de actividades
"""

import os
import sys
import django
from django.test import Client
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_endpoint_buscar_actividad_directo():
    """Test directo del endpoint buscar-actividad"""
    print("🔍 TEST DIRECTO DEL ENDPOINT BUSCAR-ACTIVIDAD")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Test sin login primero
        print("   📋 Probando endpoint sin login...")
        response = client.get('/tributario-app/ajax/buscar-actividad/?empresa=0301&codigo=001')
        
        print(f"   📄 Status Code: {response.status_code}")
        print(f"   📄 Content-Type: {response.get('Content-Type', 'No definido')}")
        print(f"   📄 Contenido (primeros 200 chars): {response.content.decode()[:200]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON válido: {data}")
                return True
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                print(f"   📄 Contenido completo: {response.content.decode()}")
                return False
        else:
            print(f"   ❌ Status code inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test directo: {str(e)}")
        return False

def test_endpoint_con_login():
    """Test del endpoint con login"""
    print("\n🔍 TEST DEL ENDPOINT CON LOGIN")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        response = client.post('/tributario-app/login/', login_data, follow=True)
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Test del endpoint con login
        print("   📋 Probando endpoint con login...")
        response = client.get('/tributario-app/ajax/buscar-actividad/?empresa=0301&codigo=001')
        
        print(f"   📄 Status Code: {response.status_code}")
        print(f"   📄 Content-Type: {response.get('Content-Type', 'No definido')}")
        print(f"   📄 Contenido (primeros 200 chars): {response.content.decode()[:200]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON válido: {data}")
                return True
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                print(f"   📄 Contenido completo: {response.content.decode()}")
                return False
        else:
            print(f"   ❌ Status code inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test con login: {str(e)}")
        return False

def test_endpoint_cargar_actividades():
    """Test del endpoint cargar-actividades"""
    print("\n🔍 TEST DEL ENDPOINT CARGAR-ACTIVIDADES")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        response = client.post('/tributario-app/login/', login_data, follow=True)
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Test del endpoint
        print("   📋 Probando endpoint cargar-actividades...")
        response = client.get('/tributario-app/ajax/cargar-actividades/?empresa=0301')
        
        print(f"   📄 Status Code: {response.status_code}")
        print(f"   📄 Content-Type: {response.get('Content-Type', 'No definido')}")
        print(f"   📄 Contenido (primeros 200 chars): {response.content.decode()[:200]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON válido: {data}")
                return True
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                print(f"   📄 Contenido completo: {response.content.decode()}")
                return False
        else:
            print(f"   ❌ Status code inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test cargar actividades: {str(e)}")
        return False

def test_verificar_imports():
    """Test para verificar que los imports estén correctos"""
    print("\n🔍 TEST DE IMPORTS")
    print("=" * 60)
    
    try:
        from tributario_app.views import buscar_actividad, cargar_actividades
        print("   ✅ Imports de vistas correctos")
        
        from tributario_app.models import Actividad
        print("   ✅ Import de modelo Actividad correcto")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Error de import: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 DIAGNÓSTICO DE ERROR JSON EN BÚSQUEDA DE ACTIVIDADES")
    print("Investigando por qué se recibe HTML en lugar de JSON")
    print("=" * 70)
    
    try:
        # Test 1: Verificar imports
        imports_ok = test_verificar_imports()
        
        # Test 2: Endpoint sin login
        directo_ok = test_endpoint_buscar_actividad_directo()
        
        # Test 3: Endpoint con login
        login_ok = test_endpoint_con_login()
        
        # Test 4: Endpoint cargar actividades
        cargar_ok = test_endpoint_cargar_actividades()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE DIAGNÓSTICO")
        print("=" * 70)
        
        print(f"✅ Imports correctos: {'OK' if imports_ok else 'FALLO'}")
        print(f"✅ Endpoint sin login: {'OK' if directo_ok else 'FALLO'}")
        print(f"✅ Endpoint con login: {'OK' if login_ok else 'FALLO'}")
        print(f"✅ Endpoint cargar actividades: {'OK' if cargar_ok else 'FALLO'}")
        
        if directo_ok and login_ok and cargar_ok:
            print("\n🎉 TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE")
            print("El problema podría estar en el JavaScript del frontend")
            return 0
        else:
            print("\n⚠️  SE DETECTARON PROBLEMAS EN LOS ENDPOINTS")
            print("Revisar la configuración de URLs y vistas")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





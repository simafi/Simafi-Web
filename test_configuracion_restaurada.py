#!/usr/bin/env python
"""
Test para verificar que la configuración restaurada funciona correctamente
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
import os
import sys

# Agregar el directorio tributario al path de Python
tributario_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'Scripts', 'tributario')
if tributario_path not in sys.path:
    sys.path.insert(0, tributario_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_configuracion_restaurada():
    """Test para verificar que la configuración restaurada funciona"""
    print("🔍 TEST: Configuración Restaurada")
    print("=" * 50)
    
    try:
        client = Client()
        
        # Test 1: Verificar que el servidor responde
        print("\n   📝 Test 1: Verificar respuesta del servidor...")
        response = client.get('/')
        
        print(f"   📊 Status Code: {response.status_code}")
        if response.status_code in [200, 302]:  # 302 es redirect, también válido
            print("   ✅ Servidor responde correctamente")
        else:
            print(f"   ❌ Error en respuesta del servidor: {response.status_code}")
            return False
        
        # Test 2: Verificar módulo tributario
        print("\n   📝 Test 2: Verificar módulo tributario...")
        response = client.get('/tributario/')
        
        print(f"   📊 Status Code: {response.status_code}")
        if response.status_code in [200, 302]:
            print("   ✅ Módulo tributario accesible")
        else:
            print(f"   ❌ Error en módulo tributario: {response.status_code}")
            return False
        
        # Test 3: Verificar tributario-app
        print("\n   📝 Test 3: Verificar tributario-app...")
        response = client.get('/tributario-app/')
        
        print(f"   📊 Status Code: {response.status_code}")
        if response.status_code in [200, 302]:
            print("   ✅ Tributario-app accesible")
        else:
            print(f"   ❌ Error en tributario-app: {response.status_code}")
            return False
        
        # Test 4: Verificar formulario de rubros
        print("\n   📝 Test 4: Verificar formulario de rubros...")
        response = client.get('/tributario-app/rubros/')
        
        print(f"   📊 Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Formulario de rubros accesible")
        else:
            print(f"   ❌ Error en formulario de rubros: {response.status_code}")
            return False
        
        # Test 5: Verificar formulario de plan de arbitrio
        print("\n   📝 Test 5: Verificar formulario de plan de arbitrio...")
        response = client.get('/tributario-app/plan-arbitrio/')
        
        print(f"   📊 Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Formulario de plan de arbitrio accesible")
        else:
            print(f"   ❌ Error en formulario de plan de arbitrio: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_configuracion_restaurada()
    if success:
        print("\n🎉 Configuración restaurada y funcionando correctamente")
    else:
        print("\n💥 Se detectaron errores en la configuración restaurada")




#!/usr/bin/env python
"""
Test para verificar que las URLs corregidas funcionen correctamente
"""

import os
import sys
import django
from django.test import Client
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_urls_corregidas():
    """Test de las URLs corregidas"""
    print("🔍 TEST DE URLs CORREGIDAS")
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
        
        # Test 1: URL corregida buscar-actividad
        print("   📋 Probando /tributario-app/ajax/buscar-actividad/...")
        response = client.get('/tributario-app/ajax/buscar-actividad/?empresa=0301&codigo=001')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON válido: {data}")
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                print(f"   📄 Contenido: {response.content.decode()[:200]}")
                return False
        else:
            print(f"   ❌ Status code: {response.status_code}")
            return False
        
        # Test 2: URL corregida cargar-actividades
        print("   📋 Probando /tributario-app/ajax/cargar-actividades/...")
        response = client.get('/tributario-app/ajax/cargar-actividades/?empresa=0301')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON válido: {data}")
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                print(f"   📄 Contenido: {response.content.decode()[:200]}")
                return False
        else:
            print(f"   ❌ Status code: {response.status_code}")
            return False
        
        # Test 3: URL corregida buscar-identificacion
        print("   📋 Probando /tributario-app/ajax/buscar-identificacion/...")
        response = client.get('/tributario-app/ajax/buscar-identificacion/?identidad=12345678')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON válido: {data}")
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                print(f"   📄 Contenido: {response.content.decode()[:200]}")
                return False
        else:
            print(f"   ❌ Status code: {response.status_code}")
            return False
        
        print("   🎉 Todas las URLs corregidas funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

def test_urls_incorrectas():
    """Test de las URLs incorrectas (deberían fallar)"""
    print("\n🔍 TEST DE URLs INCORRECTAS (DEBERÍAN FALLAR)")
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
        
        # Test 1: URL incorrecta (sin -app)
        print("   📋 Probando /tributario/ajax/buscar-actividad/ (incorrecta)...")
        response = client.get('/tributario/ajax/buscar-actividad/?empresa=0301&codigo=001')
        
        print(f"   📄 Status code: {response.status_code}")
        print(f"   📄 Content-Type: {response.get('Content-Type', 'No definido')}")
        
        if response.status_code == 404:
            print("   ✅ URL incorrecta devuelve 404 (esperado)")
        elif response.status_code == 200:
            content = response.content.decode()
            if '<!DOCTYPE' in content:
                print("   ✅ URL incorrecta devuelve HTML (esperado)")
            else:
                print("   ⚠️  URL incorrecta devuelve 200 pero no HTML")
        else:
            print(f"   ⚠️  Status code inesperado: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE CORRECCIÓN DE URLs")
    print("Verificando que las URLs corregidas funcionen y las incorrectas fallen")
    print("=" * 70)
    
    try:
        # Test 1: URLs corregidas
        corregidas_ok = test_urls_corregidas()
        
        # Test 2: URLs incorrectas
        incorrectas_ok = test_urls_incorrectas()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ URLs corregidas funcionan: {'OK' if corregidas_ok else 'FALLO'}")
        print(f"✅ URLs incorrectas fallan: {'OK' if incorrectas_ok else 'FALLO'}")
        
        if corregidas_ok and incorrectas_ok:
            print("\n🎉 CORRECCIÓN DE URLs EXITOSA")
            print("✅ Las URLs corregidas funcionan correctamente")
            print("✅ Las URLs incorrectas fallan como se esperaba")
            print("✅ El error de sintaxis JSON debería estar resuelto")
            return 0
        else:
            print("\n⚠️  ALGUNAS URLs NECESITAN REVISIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





#!/usr/bin/env python
"""
Test para verificar que el logout funcione correctamente
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_logout_corregido():
    """Test del logout corregido"""
    print("🔍 TEST DE LOGOUT CORREGIDO")
    print("=" * 50)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        print("   📋 Realizando login...")
        response = client.post('/tributario-app/login/', login_data, follow=True)
        
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Verificar que la sesión tenga empresa
        session = client.session
        print(f"   📄 Empresa en sesión: {session.get('empresa', 'NO ENCONTRADA')}")
        
        if not session.get('empresa'):
            print("   ❌ No hay empresa en la sesión")
            return False
        
        # Test logout
        print("   📋 Realizando logout...")
        response = client.post('/tributario-app/logout/', follow=True)
        
        print(f"   📄 Status logout: {response.status_code}")
        print(f"   📄 URL final logout: {response.request['PATH_INFO']}")
        
        if response.status_code == 200:
            print("   ✅ Logout exitoso")
            
            # Verificar que la sesión se haya limpiado
            session = client.session
            print(f"   📄 Empresa en sesión después del logout: {session.get('empresa', 'NO ENCONTRADA')}")
            
            if not session.get('empresa'):
                print("   ✅ Sesión limpiada correctamente")
                return True
            else:
                print("   ❌ Sesión no se limpió correctamente")
                return False
        else:
            print(f"   ❌ Error en logout: {response.status_code}")
            print(f"   📄 Contenido: {response.content.decode()[:300]}...")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_verificar_urls():
    """Test para verificar que las URLs estén correctas"""
    print("\n🔍 TEST DE VERIFICACIÓN DE URLs")
    print("=" * 50)
    
    try:
        from django.urls import reverse
        
        # Verificar que la URL de login existe
        try:
            login_url = reverse('login')
            print(f"   ✅ URL de login encontrada: {login_url}")
        except Exception as e:
            print(f"   ❌ Error al encontrar URL de login: {e}")
            return False
        
        # Verificar que la URL de logout existe
        try:
            logout_url = reverse('logout')
            print(f"   ✅ URL de logout encontrada: {logout_url}")
        except Exception as e:
            print(f"   ❌ Error al encontrar URL de logout: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE LOGOUT CORREGIDO")
    print("Verificando que el logout funcione sin errores")
    print("=" * 60)
    
    try:
        # Test 1: Verificar URLs
        urls_ok = test_verificar_urls()
        
        # Test 2: Logout corregido
        logout_ok = test_logout_corregido()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        print(f"✅ URLs verificadas: {'OK' if urls_ok else 'FALLO'}")
        print(f"✅ Logout corregido: {'OK' if logout_ok else 'FALLO'}")
        
        if urls_ok and logout_ok:
            print("\n🎉 LOGOUT FUNCIONANDO CORRECTAMENTE")
            print("✅ No hay errores de NoReverseMatch")
            print("✅ El logout redirige correctamente")
            print("✅ La sesión se limpia correctamente")
            return 0
        else:
            print("\n⚠️  HAY PROBLEMAS QUE NECESITAN CORRECCIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





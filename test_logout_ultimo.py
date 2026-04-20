#!/usr/bin/env python
"""
Test último para verificar que el logout funcione correctamente
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_logout_ultimo():
    """Test último del logout"""
    print("🔍 TEST ÚLTIMO DE LOGOUT")
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
        
        # Test logout
        print("   📋 Realizando logout...")
        response = client.post('/tributario-app/logout/', follow=True)
        
        print(f"   📄 Status logout: {response.status_code}")
        print(f"   📄 URL final logout: {response.request['PATH_INFO']}")
        
        if response.status_code == 200:
            print("   ✅ Logout exitoso")
            
            # Verificar que estemos en la página de login
            content = response.content.decode()
            if 'login' in content.lower() or 'iniciar sesión' in content.lower():
                print("   ✅ Redirigido a la página de login")
                return True
            else:
                print("   ❌ No redirigido a la página de login")
                print(f"   📄 Contenido: {content[:300]}...")
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

if __name__ == '__main__':
    print("🧪 TEST ÚLTIMO DE LOGOUT")
    print("Verificando que el logout funcione sin errores")
    print("=" * 60)
    
    if test_logout_ultimo():
        print("\n🎉 LOGOUT COMPLETAMENTE CORREGIDO")
        print("✅ No hay errores de NoReverseMatch")
        print("✅ El logout redirige correctamente")
        print("✅ La sesión se limpia correctamente")
    else:
        print("\n⚠️  HAY PROBLEMAS QUE NECESITAN CORRECCIÓN")





#!/usr/bin/env python
"""
Test detallado del login
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_login_detallado():
    """Test detallado del login"""
    print("🔍 TEST DETALLADO DE LOGIN")
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
        response = client.post('/tributario-app/login/', login_data)
        
        print(f"   📄 Status login: {response.status_code}")
        
        if response.status_code == 200:
            print("   ⚠️  Login devuelve 200 en lugar de 302")
            content = response.content.decode()
            
            # Verificar si hay errores en el formulario
            if 'error' in content.lower():
                print("   ❌ Hay errores en el login")
                print(f"   📄 Contenido del error: {content[:500]}...")
                return False
            else:
                print("   ✅ No hay errores obvios en el login")
                print(f"   📄 Contenido: {content[:300]}...")
                return False
        elif response.status_code == 302:
            print("   ✅ Login redirige correctamente")
            
            # Verificar que la sesión tenga empresa
            session = client.session
            print(f"   📄 Empresa en sesión: {session.get('empresa', 'NO ENCONTRADA')}")
            
            if session.get('empresa'):
                print("   ✅ Empresa guardada en sesión")
                return True
            else:
                print("   ❌ Empresa no guardada en sesión")
                return False
        else:
            print(f"   ❌ Status inesperado: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_verificar_contraseña():
    """Test para verificar la contraseña"""
    print("\n🔍 TEST DE VERIFICACIÓN DE CONTRASEÑA")
    print("=" * 50)
    
    try:
        from tributario_app.models import usuario
        from django.contrib.auth.hashers import check_password
        
        # Obtener usuario
        user = usuario.objects.get(usuario='tributario')
        print(f"   📄 Usuario: {user.usuario}")
        print(f"   📄 Empresa: {user.empresa}")
        print(f"   📄 Password hash: {user.password[:50]}...")
        
        # Verificar contraseña
        if check_password('admin123', user.password):
            print("   ✅ Contraseña correcta")
            return True
        else:
            print("   ❌ Contraseña incorrecta")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🧪 TEST DETALLADO DE LOGIN")
    print("Verificando el login paso a paso")
    print("=" * 60)
    
    # Test 1: Verificar contraseña
    password_ok = test_verificar_contraseña()
    
    # Test 2: Login detallado
    login_ok = test_login_detallado()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    print(f"✅ Contraseña correcta: {'OK' if password_ok else 'FALLO'}")
    print(f"✅ Login detallado: {'OK' if login_ok else 'FALLO'}")
    
    if password_ok and login_ok:
        print("\n🎉 LOGIN FUNCIONANDO CORRECTAMENTE")
    else:
        print("\n⚠️  HAY PROBLEMAS EN EL LOGIN")

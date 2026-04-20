#!/usr/bin/env python
"""
Test final para verificar que el logout funcione correctamente
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_logout_final():
    """Test final del logout"""
    print("🔍 TEST FINAL DE LOGOUT")
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
            
            # Verificar que estemos en la página de login
            content = response.content.decode()
            if 'login' in content.lower() or 'iniciar sesión' in content.lower():
                print("   ✅ Redirigido a la página de login")
                
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

def test_verificar_correcciones():
    """Test para verificar que las correcciones estén aplicadas"""
    print("\n🔍 TEST DE VERIFICACIÓN DE CORRECCIONES")
    print("=" * 50)
    
    try:
        # Verificar que no haya referencias a 'municipio_codigo' en session
        with open('venv/Scripts/tributario/tributario_app/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'municipio_codigo' in content:
            print("   ⚠️  Aún hay referencias a 'municipio_codigo' en el código")
            return False
        else:
            print("   ✅ No hay referencias a 'municipio_codigo' en el código")
        
        # Verificar que la vista logout_view use la URL correcta
        if "return redirect('/tributario-app/login/')" in content:
            print("   ✅ Vista logout_view usa la URL correcta")
        else:
            print("   ❌ Vista logout_view no usa la URL correcta")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

if __name__ == '__main__':
    print("🧪 TEST FINAL DE LOGOUT")
    print("Verificando que el logout funcione sin errores")
    print("=" * 60)
    
    # Test 1: Verificar correcciones
    correcciones_ok = test_verificar_correcciones()
    
    # Test 2: Logout final
    logout_ok = test_logout_final()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    print(f"✅ Correcciones aplicadas: {'OK' if correcciones_ok else 'FALLO'}")
    print(f"✅ Logout final: {'OK' if logout_ok else 'FALLO'}")
    
    if correcciones_ok and logout_ok:
        print("\n🎉 LOGOUT COMPLETAMENTE CORREGIDO")
        print("✅ No hay errores de NoReverseMatch")
        print("✅ El logout redirige correctamente")
        print("✅ La sesión se limpia correctamente")
        print("✅ Todas las referencias a 'municipio_codigo' han sido corregidas")
    else:
        print("\n⚠️  HAY PROBLEMAS QUE NECESITAN CORRECCIÓN")





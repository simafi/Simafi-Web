#!/usr/bin/env python
"""
Test simple para verificar el login
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_login_simple():
    """Test simple del login"""
    print("🔍 TEST SIMPLE DE LOGIN")
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

def test_verificar_usuario():
    """Test para verificar que el usuario existe"""
    print("\n🔍 TEST DE VERIFICACIÓN DE USUARIO")
    print("=" * 50)
    
    try:
        from tributario_app.models import usuario, Municipio
        
        # Verificar que el usuario existe
        print("   📋 Verificando usuario...")
        try:
            user = usuario.objects.get(usuario='tributario')
            print(f"   ✅ Usuario encontrado: {user.usuario}")
            print(f"   📄 Empresa del usuario: {user.empresa}")
        except usuario.DoesNotExist:
            print("   ❌ Usuario no encontrado")
            return False
        
        # Verificar que el municipio existe
        print("   📋 Verificando municipio...")
        try:
            municipio = Municipio.objects.get(codigo='0301')
            print(f"   ✅ Municipio encontrado: {municipio.codigo} - {municipio.descripcion}")
        except Municipio.DoesNotExist:
            print("   ❌ Municipio no encontrado")
            return False
        
        # Verificar que el usuario tiene la empresa correcta
        if user.empresa == '0301':
            print("   ✅ Usuario tiene la empresa correcta")
            return True
        else:
            print(f"   ❌ Usuario tiene empresa incorrecta: {user.empresa}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🧪 TEST SIMPLE DE LOGIN")
    print("Verificando el login paso a paso")
    print("=" * 60)
    
    try:
        # Test 1: Verificar usuario
        usuario_ok = test_verificar_usuario()
        
        # Test 2: Login simple
        login_ok = test_login_simple()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        print(f"✅ Usuario verificado: {'OK' if usuario_ok else 'FALLO'}")
        print(f"✅ Login simple: {'OK' if login_ok else 'FALLO'}")
        
        if usuario_ok and login_ok:
            print("\n🎉 LOGIN FUNCIONANDO CORRECTAMENTE")
            return 0
        else:
            print("\n⚠️  HAY PROBLEMAS EN EL LOGIN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





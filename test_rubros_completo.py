#!/usr/bin/env python
"""
Test completo para verificar el formulario de rubros siguiendo todos los redirects
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_rubros_completo():
    """Test completo del formulario de rubros"""
    print("🔍 TEST COMPLETO DE FORMULARIO RUBROS")
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
        print(f"   📄 Status login: {response.status_code}")
        print(f"   📄 URL final login: {response.request['PATH_INFO']}")
        
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
        
        # Test 1: Acceder al formulario
        print("   📋 Accediendo al formulario de rubros...")
        response = client.get('/tributario-app/rubros/', follow=True)
        
        print(f"   📄 Status formulario: {response.status_code}")
        print(f"   📄 URL final formulario: {response.request['PATH_INFO']}")
        
        if response.status_code == 200:
            print("   ✅ Formulario de rubros accesible")
            content = response.content.decode()
            
            # Verificar que no haya errores de base de datos
            if 'Unknown column' in content or 'OperationalError' in content:
                print("   ❌ Error de base de datos detectado")
                print(f"   📄 Contenido del error: {content[:500]}...")
                return False
            else:
                print("   ✅ No se detectaron errores de base de datos")
            
            # Verificar que estemos en la página correcta
            if 'rubros' in content.lower() or 'rubro' in content.lower():
                print("   ✅ Contenido de rubros detectado")
            else:
                print("   ❌ No se detectó contenido de rubros")
                print(f"   📄 Contenido: {content[:300]}...")
                return False
            
            # Verificar campos básicos
            if 'id="id_empresa"' in content:
                print("   ✅ Campo empresa encontrado")
            else:
                print("   ❌ Campo empresa no encontrado")
                return False
            
            if 'id="id_cuntarez"' in content:
                print("   ✅ Campo cuntarez encontrado")
            else:
                print("   ❌ Campo cuntarez no encontrado")
                return False
            
            return True
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            print(f"   📄 Contenido: {response.content.decode()[:300]}...")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_login_directo():
    """Test del login directo"""
    print("\n🔍 TEST DE LOGIN DIRECTO")
    print("=" * 50)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login sin follow
        print("   📋 Realizando login sin follow...")
        response = client.post('/tributario-app/login/', login_data)
        print(f"   📄 Status login: {response.status_code}")
        print(f"   📄 URL login: {response.url}")
        
        if response.status_code == 302:
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
            print(f"   ❌ Login no redirige: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🧪 TEST COMPLETO DE FORMULARIO RUBROS")
    print("Verificando login y formulario paso a paso")
    print("=" * 60)
    
    try:
        # Test 1: Login directo
        login_ok = test_login_directo()
        
        # Test 2: Formulario completo
        formulario_ok = test_rubros_completo()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        print(f"✅ Login directo: {'OK' if login_ok else 'FALLO'}")
        print(f"✅ Formulario rubros: {'OK' if formulario_ok else 'FALLO'}")
        
        if login_ok and formulario_ok:
            print("\n🎉 FORMULARIO RUBROS FUNCIONANDO CORRECTAMENTE")
            print("✅ No hay errores de base de datos")
            print("✅ Los campos están correctos")
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





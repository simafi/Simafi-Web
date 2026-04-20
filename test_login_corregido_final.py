#!/usr/bin/env python
"""
Test final para verificar que el error de municipio_codigo se ha corregido
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.hashers import check_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import usuario, Municipio

def test_login_corregido_final():
    """Test final del login corregido"""
    print("🔧 TEST FINAL - LOGIN CORREGIDO")
    print("=" * 60)
    
    try:
        # 1. Verificar credenciales
        print("1. Verificando credenciales...")
        user = usuario.objects.get(usuario='tributario')
        municipio = Municipio.objects.get(codigo='0301')
        
        print(f"   ✅ Usuario: {user.usuario}")
        print(f"   ✅ Empresa: {user.empresa}")
        print(f"   ✅ Municipio: {municipio.codigo} - {municipio.descripcion}")
        
        # Verificar contraseña
        if check_password('admin123', user.password):
            print("   ✅ Contraseña admin123 verificada")
        else:
            print("   ❌ Contraseña admin123 NO verificada")
            return False
        
        # 2. Test de login real
        print("\n2. Probando login real...")
        client = Client()
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        print(f"   🔍 Datos de login: {login_data}")
        
        try:
            response = client.post('/tributario-app/login/', login_data, follow=True)
            print(f"   🔍 Status code: {response.status_code}")
            print(f"   🔍 URL final: {response.url if hasattr(response, 'url') else 'N/A'}")
            
            if response.status_code == 200:
                # Verificar sesión
                session = client.session
                print(f"   🔍 Sesión: {dict(session)}")
                
                if session.get('empresasa') == '0301':
                    print("   ✅ LOGIN EXITOSO - Sesión creada correctamente")
                    print("   ✅ Empresa en sesión: 0301")
                    print("   ✅ Municipio en sesión:", session.get('municipio_descripcion'))
                    return True
                else:
                    print("   ❌ Login falló - Sesión no creada correctamente")
                    print(f"   🔍 Empresa en sesión: {session.get('empresasa')}")
                    return False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error en login: {str(e)}")
            if 'municipio_codigo' in str(e):
                print("   ❌ ERROR NO CORREGIDO: Sigue apareciendo 'municipio_codigo'")
                return False
            else:
                print("   ⚠️  Error diferente al esperado")
                return False
        
    except Exception as e:
        print(f"\n💥 Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_navegacion_completa():
    """Test de navegación completa después del login"""
    print("\n" + "=" * 60)
    print("🧪 TEST DE NAVEGACIÓN COMPLETA")
    print("=" * 60)
    
    try:
        client = Client()
        
        # 1. Login
        print("1. Realizando login...")
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        response = client.post('/tributario-app/login/', login_data, follow=True)
        
        if response.status_code != 200:
            print(f"   ❌ Login falló: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # 2. Acceder al menú principal
        print("\n2. Accediendo al menú principal...")
        response = client.get('/tributario-app/menu/')
        
        if response.status_code == 200:
            print("   ✅ Menú principal accesible")
            content = response.content.decode()
            
            # Verificar elementos del menú
            elementos_esperados = [
                'Bienes Inmuebles',
                'Industria y Comercio',
                'Misceláneos',
                'Convenios de Pagos',
                'Maestro de Negocios',
                'Declaración de Volumen'
            ]
            
            elementos_encontrados = []
            for elemento in elementos_esperados:
                if elemento in content:
                    elementos_encontrados.append(elemento)
                    print(f"   ✅ Encontrado: {elemento}")
                else:
                    print(f"   ❌ No encontrado: {elemento}")
            
            if len(elementos_encontrados) >= 4:
                print(f"   ✅ Menú funcional: {len(elementos_encontrados)}/{len(elementos_esperados)} elementos")
                return True
            else:
                print(f"   ❌ Menú incompleto: {len(elementos_encontrados)}/{len(elementos_esperados)} elementos")
                return False
        else:
            print(f"   ❌ Error accediendo al menú: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en navegación: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST FINAL - ERROR CORREGIDO")
    print("Verificando que el error 'municipio_codigo' se ha corregido")
    print("Credenciales: tributario / admin123 / municipio 0301")
    print("URL: http://127.0.0.1:8080/tributario-app/")
    print("=" * 60)
    
    try:
        # Test 1: Login corregido
        login_ok = test_login_corregido_final()
        
        # Test 2: Navegación completa
        navegacion_ok = test_navegacion_completa()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL")
        print("=" * 60)
        
        if login_ok and navegacion_ok:
            print("🎉 ¡ERROR CORREGIDO EXITOSAMENTE!")
            print("✅ El login funciona correctamente")
            print("✅ La navegación es funcional")
            print("\n🎯 CREDENCIALES FUNCIONALES:")
            print("   URL: http://127.0.0.1:8080/tributario-app/")
            print("   Usuario: tributario")
            print("   Contraseña: admin123")
            print("   Municipio: 0301")
            return 0
        else:
            print("⚠️  AÚN HAY PROBLEMAS")
            if not login_ok:
                print("❌ El login no funciona correctamente")
            if not navegacion_ok:
                print("❌ La navegación no es funcional")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





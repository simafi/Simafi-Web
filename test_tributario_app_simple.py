#!/usr/bin/env python
"""
Test simple para tributario_app con las credenciales tributario/admin123/municipio 0301
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

def test_tributario_app_credenciales():
    """Test de credenciales en tributario_app"""
    print("🔍 VERIFICANDO CREDENCIALES EN TRIBUTARIO_APP")
    print("=" * 60)
    
    try:
        # 1. Verificar conexión
        print("1. Verificando conexión a tributario_app...")
        total_usuarios = usuario.objects.count()
        total_municipios = Municipio.objects.count()
        print(f"   ✅ Usuarios en tributario_app: {total_usuarios}")
        print(f"   ✅ Municipios en tributario_app: {total_municipios}")
        
        # 2. Buscar usuario tributario
        print("\n2. Buscando usuario 'tributario'...")
        try:
            user = usuario.objects.get(usuario='tributario')
            print(f"   ✅ Usuario encontrado: {user.usuario}")
            print(f"   ✅ Municipio código: {user.municipio_codigo}")
            print(f"   ✅ Activo: {user.is_active}")
            print(f"   ✅ Password Hash: {user.password[:30]}...")
        except usuario.DoesNotExist:
            print("   ❌ Usuario 'tributario' NO encontrado en tributario_app")
            return False
        
        # 3. Buscar municipio 0301
        print("\n3. Buscando municipio '0301'...")
        try:
            municipio = Municipio.objects.get(codigo='0301')
            print(f"   ✅ Municipio encontrado: {municipio.descripcion}")
            print(f"   ✅ Código: {municipio.codigo}")
        except Municipio.DoesNotExist:
            print("   ❌ Municipio '0301' NO encontrado en tributario_app")
            return False
        
        # 4. Verificar contraseña admin123
        print("\n4. Verificando contraseña 'admin123'...")
        if check_password('admin123', user.password):
            print("   ✅ Contraseña 'admin123' VERIFICADA")
            password_correcta = True
        else:
            print("   ❌ Contraseña 'admin123' NO coincide")
            password_correcta = False
        
        # 5. Verificar asociación usuario-municipio
        print("\n5. Verificando asociación usuario-municipio...")
        if user.municipio_codigo == municipio.codigo:
            print("   ✅ Usuario asociado al municipio correcto")
            municipio_correcto = True
        else:
            print(f"   ❌ Usuario asociado a municipio {user.municipio_codigo}, esperado {municipio.codigo}")
            municipio_correcto = False
        
        # 6. Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE VERIFICACIÓN - TRIBUTARIO_APP")
        print("=" * 60)
        
        resultados = [
            ("Conexión tributario_app", True),
            ("Usuario tributario", True),
            ("Municipio 0301", True),
            ("Contraseña admin123", password_correcta),
            ("Asociación usuario-municipio", municipio_correcto)
        ]
        
        for test, resultado in resultados:
            status = "✅ ÉXITO" if resultado else "❌ FALLO"
            print(f"{test:30s}: {status}")
        
        todos_correctos = all(resultado for _, resultado in resultados)
        
        if todos_correctos:
            print("\n🎉 ¡TODAS LAS CREDENCIALES ESTÁN CORRECTAS EN TRIBUTARIO_APP!")
            print("✅ El usuario puede acceder a tributario_app con:")
            print("   Usuario: tributario")
            print("   Contraseña: admin123")
            print("   Municipio: 0301")
            print("   URL: http://127.0.0.1:8080/tributario-app/")
        else:
            print("\n⚠️  ALGUNAS CREDENCIALES TIENEN PROBLEMAS EN TRIBUTARIO_APP")
            print("❌ Revisar los elementos marcados como FALLO")
        
        # 7. Test de login real
        print("\n" + "=" * 60)
        print("🧪 TEST DE LOGIN REAL EN TRIBUTARIO_APP")
        print("=" * 60)
        
        client = Client()
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        print("Probando login con datos:", login_data)
        
        try:
            response = client.post('/tributario-app/login/', login_data, follow=True)
            print(f"Status code: {response.status_code}")
            print(f"URL final: {response.url if hasattr(response, 'url') else 'N/A'}")
            
            if response.status_code == 200:
                session = client.session
                print(f"Sesión creada: {dict(session)}")
                
                if session.get('empresasa') == '0301':
                    print("✅ LOGIN EXITOSO EN TRIBUTARIO_APP")
                    print("✅ Sesión creada correctamente")
                    return True
                else:
                    print("❌ Login falló - Sesión no creada correctamente")
                    return False
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error en login: {str(e)}")
            return False
        
    except Exception as e:
        print(f"\n💥 Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def mostrar_usuarios_tributario_app():
    """Mostrar todos los usuarios en tributario_app"""
    print("\n" + "=" * 60)
    print("📋 USUARIOS EN TRIBUTARIO_APP")
    print("=" * 60)
    
    try:
        usuarios = usuario.objects.all()
        print(f"Total de usuarios: {usuarios.count()}\n")
        
        for i, u in enumerate(usuarios, 1):
            print(f"{i:2d}. Usuario: {u.usuario}")
            print(f"    Municipio código: {u.municipio_codigo}")
            print(f"    Activo: {u.is_active}")
            print(f"    Password Hash: {u.password[:30]}...")
            print()
            
    except Exception as e:
        print(f"Error al obtener usuarios: {str(e)}")

def mostrar_municipios_tributario_app():
    """Mostrar todos los municipios en tributario_app"""
    print("\n" + "=" * 60)
    print("📋 MUNICIPIOS EN TRIBUTARIO_APP")
    print("=" * 60)
    
    try:
        municipios = Municipio.objects.all()
        print(f"Total de municipios: {municipios.count()}\n")
        
        for i, m in enumerate(municipios, 1):
            print(f"{i:2d}. Código: {m.codigo}")
            print(f"    Descripción: {m.descripcion}")
            print()
            
    except Exception as e:
        print(f"Error al obtener municipios: {str(e)}")

def main():
    """Función principal"""
    print("🧪 TEST DE TRIBUTARIO_APP - SISTEMA LEGACY")
    print("Verificando credenciales: tributario / admin123 / municipio 0301")
    print("Ruta: C:\\simafiweb\\venv\\Scripts\\tributario\\tributario_app")
    print("=" * 60)
    
    try:
        # Ejecutar test principal
        exito = test_tributario_app_credenciales()
        
        # Mostrar información adicional
        mostrar_usuarios_tributario_app()
        mostrar_municipios_tributario_app()
        
        if exito:
            print("\n✅ TRIBUTARIO_APP VERIFICADO Y FUNCIONAL")
            print("🎯 Las credenciales tributario/admin123/municipio 0301 funcionan correctamente")
            print("🌐 Accede a: http://127.0.0.1:8080/tributario-app/")
            return 0
        else:
            print("\n❌ TRIBUTARIO_APP TIENE PROBLEMAS")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





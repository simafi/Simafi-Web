#!/usr/bin/env python
"""
Test completo final de autenticación - Incluye verificación de credenciales y test de login real
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.hashers import check_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
from modules.core.models import Municipio

class TestLoginCompletoFinal:
    """Test completo final de autenticación"""
    
    def __init__(self):
        self.client = Client()
        self.test_results = []
        
    def test_verificar_credenciales_bd(self):
        """Test 1: Verificar credenciales en base de datos"""
        print("🔍 TEST 1: Verificando credenciales en base de datos...")
        try:
            # Buscar usuario tributario
            usuario = Usuario.objects.get(usuario='tributario')
            municipio = Municipio.objects.get(codigo='0301')
            
            # Verificar contraseña
            password_ok = check_password('admin123', usuario.password)
            
            print(f"   ✅ Usuario: {usuario.usuario}")
            print(f"   ✅ Empresa: {usuario.empresa}")
            print(f"   ✅ Municipio: {municipio.descripcion} (ID: {municipio.id})")
            print(f"   ✅ Contraseña admin123: {'VERIFICADA' if password_ok else 'FALLO'}")
            print(f"   ✅ Usuario activo: {usuario.is_active}")
            
            resultado = password_ok and usuario.is_active and usuario.municipio_id == municipio.id
            self.test_results.append(("Credenciales BD", resultado, "Usuario, contraseña y municipio verificados"))
            return resultado
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Credenciales BD", False, str(e)))
            return False
    
    def test_login_sistema_principal(self):
        """Test 2: Probar login en el sistema principal"""
        print("\n🔍 TEST 2: Probando login sistema principal...")
        try:
            # Obtener municipio 0301
            municipio = Municipio.objects.get(codigo='0301')
            
            # Datos de login
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': str(municipio.id)
            }
            
            print(f"   🔍 Datos de login: {login_data}")
            
            # Intentar login
            response = self.client.post('/login/', login_data, follow=True)
            
            print(f"   🔍 Status code: {response.status_code}")
            print(f"   🔍 URL final: {response.url}")
            
            if response.status_code == 200:
                # Verificar redirección al menú principal
                if 'menu/' in response.url or 'Bienvenido' in str(response.content):
                    print("   ✅ Login exitoso - Redirigido al menú principal")
                    
                    # Verificar sesión
                    session = self.client.session
                    if session.get('user_id'):
                        print(f"   ✅ Sesión creada - User ID: {session.get('user_id')}")
                        print(f"   ✅ Usuario en sesión: {session.get('usuario')}")
                        print(f"   ✅ Municipio en sesión: {session.get('municipio_id')}")
                        
                        resultado = True
                    else:
                        print("   ❌ No se creó sesión")
                        resultado = False
                else:
                    print("   ❌ Login falló - No redirigido al menú")
                    print(f"   🔍 Contenido respuesta: {str(response.content)[:200]}...")
                    resultado = False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                resultado = False
            
            self.test_results.append(("Login Sistema Principal", resultado, f"Status: {response.status_code}, URL: {response.url}"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error en login: {str(e)}")
            self.test_results.append(("Login Sistema Principal", False, str(e)))
            return False
    
    def test_acceso_menu_principal(self):
        """Test 3: Verificar acceso al menú principal"""
        print("\n🔍 TEST 3: Verificando acceso al menú principal...")
        try:
            # Primero hacer login
            municipio = Municipio.objects.get(codigo='0301')
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': str(municipio.id)
            }
            
            # Login
            self.client.post('/login/', login_data)
            
            # Acceder al menú principal
            response = self.client.get('/menu/')
            
            print(f"   🔍 Status code: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode()
                
                # Verificar elementos del menú
                elementos_esperados = [
                    'Catastro',
                    'Tributario', 
                    'Administrativo',
                    'Bienvenido'
                ]
                
                elementos_encontrados = []
                for elemento in elementos_esperados:
                    if elemento in content:
                        elementos_encontrados.append(elemento)
                        print(f"   ✅ Encontrado: {elemento}")
                    else:
                        print(f"   ❌ No encontrado: {elemento}")
                
                if len(elementos_encontrados) >= 3:
                    print("   ✅ Menú principal accesible y funcional")
                    resultado = True
                else:
                    print("   ❌ Menú principal incompleto")
                    resultado = False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                resultado = False
            
            self.test_results.append(("Acceso Menú Principal", resultado, f"Elementos: {len(elementos_encontrados)}/4"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Acceso Menú Principal", False, str(e)))
            return False
    
    def test_logout_sistema(self):
        """Test 4: Verificar logout del sistema"""
        print("\n🔍 TEST 4: Verificando logout del sistema...")
        try:
            # Primero hacer login
            municipio = Municipio.objects.get(codigo='0301')
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': str(municipio.id)
            }
            
            self.client.post('/login/', login_data)
            
            # Verificar que hay sesión
            session = self.client.session
            if not session.get('user_id'):
                print("   ❌ No hay sesión activa para hacer logout")
                self.test_results.append(("Logout Sistema", False, "No hay sesión activa"))
                return False
            
            print(f"   ✅ Sesión activa - User ID: {session.get('user_id')}")
            
            # Hacer logout
            response = self.client.get('/logout/', follow=True)
            
            print(f"   🔍 Status code: {response.status_code}")
            print(f"   🔍 URL final: {response.url}")
            
            if response.status_code == 200:
                # Verificar que la sesión se limpió
                session = self.client.session
                if not session.get('user_id'):
                    print("   ✅ Logout exitoso - Sesión limpiada")
                    resultado = True
                else:
                    print("   ❌ Logout falló - Sesión no limpiada")
                    resultado = False
            else:
                print(f"   ❌ Error HTTP en logout: {response.status_code}")
                resultado = False
            
            self.test_results.append(("Logout Sistema", resultado, f"Status: {response.status_code}"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error en logout: {str(e)}")
            self.test_results.append(("Logout Sistema", False, str(e)))
            return False
    
    def ejecutar_todos_los_tests(self):
        """Ejecutar todos los tests y generar reporte"""
        print("🧪 TEST COMPLETO FINAL DE AUTENTICACIÓN")
        print("=" * 70)
        print("Credenciales a verificar:")
        print("  Usuario: tributario")
        print("  Contraseña: admin123") 
        print("  Municipio: 0301")
        print("=" * 70)
        
        # Ejecutar tests
        tests = [
            self.test_verificar_credenciales_bd,
            self.test_login_sistema_principal,
            self.test_acceso_menu_principal,
            self.test_logout_sistema
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Error crítico en test {test.__name__}: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # Generar reporte final
        self.generar_reporte_final()
    
    def generar_reporte_final(self):
        """Generar reporte final de todos los tests"""
        print("\n" + "=" * 70)
        print("📊 REPORTE FINAL DE TESTS")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        tests_exitosos = sum(1 for _, success, _ in self.test_results if success)
        tests_fallidos = total_tests - tests_exitosos
        
        print(f"Total de tests: {total_tests}")
        print(f"Tests exitosos: {tests_exitosos}")
        print(f"Tests fallidos: {tests_fallidos}")
        print(f"Porcentaje de éxito: {(tests_exitosos/total_tests)*100:.1f}%")
        
        print("\n📋 DETALLE DE RESULTADOS:")
        for i, (test_name, success, details) in enumerate(self.test_results, 1):
            status = "✅ ÉXITO" if success else "❌ FALLO"
            print(f"{i:2d}. {test_name}: {status}")
            print(f"    Detalles: {details}")
            print()
        
        if tests_exitosos == total_tests:
            print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
            print("✅ El sistema de autenticación está funcionando correctamente")
            print("\n🎯 CREDENCIALES VERIFICADAS Y FUNCIONALES:")
            print("   Usuario: tributario")
            print("   Contraseña: admin123")
            print("   Municipio: 0301")
            print("   URL Login: http://127.0.0.1:8080/login/")
            print("   URL Menú: http://127.0.0.1:8080/menu/")
        else:
            print("⚠️  ALGUNOS TESTS FALLARON")
            print("❌ Revisar los detalles de los tests fallidos")
        
        return tests_exitosos == total_tests

def main():
    """Función principal"""
    try:
        test_suite = TestLoginCompletoFinal()
        exito = test_suite.ejecutar_todos_los_tests()
        
        if exito:
            print("\n✅ SISTEMA DE AUTENTICACIÓN VERIFICADO Y FUNCIONAL")
            print("🎯 Las credenciales tributario/admin123/municipio 0301 están listas para usar")
            return 0
        else:
            print("\n❌ SISTEMA DE AUTENTICACIÓN TIENE PROBLEMAS")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





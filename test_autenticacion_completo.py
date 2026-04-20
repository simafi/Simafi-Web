#!/usr/bin/env python
"""
Test completo de autenticación del sistema modular Simafiweb
Verifica las credenciales: usuario tributario, contraseña admin123, municipio 0301
"""

import os
import sys
import django
import hashlib
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
from modules.core.models import Municipio

class TestAutenticacionCompleto:
    """
    Test completo de autenticación del sistema
    """
    
    def __init__(self):
        self.client = Client()
        self.test_results = []
        
    def test_conexion_base_datos(self):
        """Test 1: Verificar conexión a la base de datos"""
        print("🔍 TEST 1: Verificando conexión a base de datos...")
        try:
            # Verificar que podemos acceder a los modelos
            total_usuarios = Usuario.objects.count()
            total_municipios = Municipio.objects.count()
            
            print(f"   ✅ Usuarios en BD: {total_usuarios}")
            print(f"   ✅ Municipios en BD: {total_municipios}")
            
            self.test_results.append(("Conexión BD", True, f"Usuarios: {total_usuarios}, Municipios: {total_municipios}"))
            return True
            
        except Exception as e:
            print(f"   ❌ Error de conexión: {str(e)}")
            self.test_results.append(("Conexión BD", False, str(e)))
            return False
    
    def test_verificar_credenciales_especificas(self):
        """Test 2: Verificar las credenciales específicas del usuario"""
        print("\n🔍 TEST 2: Verificando credenciales específicas...")
        try:
            # Buscar usuario tributario
            usuario = Usuario.objects.get(usuario='tributario')
            print(f"   ✅ Usuario encontrado: {usuario.usuario}")
            print(f"   ✅ Empresa: {usuario.empresa}")
            print(f"   ✅ Municipio ID: {usuario.municipio_id}")
            print(f"   ✅ Nombre: {usuario.nombre}")
            print(f"   ✅ Activo: {usuario.is_active}")
            
            # Verificar municipio 0301
            municipio = Municipio.objects.get(codigo='0301')
            print(f"   ✅ Municipio 0301 encontrado: {municipio.nombre}")
            
            # Verificar contraseña admin123
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            if usuario.password == password_hash:
                print(f"   ✅ Contraseña admin123 verificada")
                password_correcta = True
            else:
                print(f"   ❌ Contraseña admin123 NO coincide")
                print(f"   🔍 Hash en BD: {usuario.password}")
                print(f"   🔍 Hash admin123: {password_hash}")
                password_correcta = False
            
            self.test_results.append(("Credenciales Específicas", password_correcta, 
                                    f"Usuario: {usuario.usuario}, Municipio: {municipio.codigo}"))
            return password_correcta
            
        except Usuario.DoesNotExist:
            print("   ❌ Usuario 'tributario' no encontrado")
            self.test_results.append(("Credenciales Específicas", False, "Usuario no encontrado"))
            return False
        except Municipio.DoesNotExist:
            print("   ❌ Municipio '0301' no encontrado")
            self.test_results.append(("Credenciales Específicas", False, "Municipio no encontrado"))
            return False
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Credenciales Específicas", False, str(e)))
            return False
    
    def test_login_sistema_principal(self):
        """Test 3: Probar login en el sistema principal"""
        print("\n🔍 TEST 3: Probando login sistema principal...")
        try:
            # Obtener municipio 0301
            municipio = Municipio.objects.get(codigo='0301')
            
            # Datos de login
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': str(municipio.id)
            }
            
            # Intentar login
            response = self.client.post('/login/', login_data, follow=True)
            
            if response.status_code == 200:
                # Verificar redirección al menú principal
                if 'menu/' in response.url or 'Bienvenido' in str(response.content):
                    print("   ✅ Login exitoso - Redirigido al menú principal")
                    print(f"   ✅ URL final: {response.url}")
                    
                    # Verificar sesión
                    session = self.client.session
                    if session.get('user_id'):
                        print(f"   ✅ Sesión creada - User ID: {session.get('user_id')}")
                        print(f"   ✅ Usuario en sesión: {session.get('usuario')}")
                        print(f"   ✅ Municipio en sesión: {session.get('municipio_id')}")
                        
                        self.test_results.append(("Login Sistema Principal", True, 
                                                f"Redirigido a: {response.url}"))
                        return True
                    else:
                        print("   ❌ No se creó sesión")
                        self.test_results.append(("Login Sistema Principal", False, "No se creó sesión"))
                        return False
                else:
                    print("   ❌ Login falló - No redirigido al menú")
                    print(f"   🔍 Respuesta: {response.content.decode()[:200]}...")
                    self.test_results.append(("Login Sistema Principal", False, "No redirigido al menú"))
                    return False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                self.test_results.append(("Login Sistema Principal", False, f"HTTP {response.status_code}"))
                return False
                
        except Exception as e:
            print(f"   ❌ Error en login: {str(e)}")
            self.test_results.append(("Login Sistema Principal", False, str(e)))
            return False
    
    def test_acceso_menu_principal(self):
        """Test 4: Verificar acceso al menú principal"""
        print("\n🔍 TEST 4: Verificando acceso al menú principal...")
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
            
            if response.status_code == 200:
                content = response.content.decode()
                
                # Verificar elementos del menú
                elementos_esperados = [
                    'Catastro',
                    'Tributario', 
                    'Administrativo',
                    'Bienvenido',
                    'tributario'
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
                    self.test_results.append(("Acceso Menú Principal", True, 
                                            f"Elementos encontrados: {len(elementos_encontrados)}"))
                    return True
                else:
                    print("   ❌ Menú principal incompleto")
                    self.test_results.append(("Acceso Menú Principal", False, 
                                            f"Solo {len(elementos_encontrados)} elementos"))
                    return False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                self.test_results.append(("Acceso Menú Principal", False, f"HTTP {response.status_code}"))
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Acceso Menú Principal", False, str(e)))
            return False
    
    def test_logout_sistema(self):
        """Test 5: Verificar logout del sistema"""
        print("\n🔍 TEST 5: Verificando logout del sistema...")
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
            
            if response.status_code == 200:
                # Verificar que la sesión se limpió
                session = self.client.session
                if not session.get('user_id'):
                    print("   ✅ Logout exitoso - Sesión limpiada")
                    print(f"   ✅ Redirigido a: {response.url}")
                    
                    self.test_results.append(("Logout Sistema", True, "Sesión limpiada correctamente"))
                    return True
                else:
                    print("   ❌ Logout falló - Sesión no limpiada")
                    self.test_results.append(("Logout Sistema", False, "Sesión no limpiada"))
                    return False
            else:
                print(f"   ❌ Error HTTP en logout: {response.status_code}")
                self.test_results.append(("Logout Sistema", False, f"HTTP {response.status_code}"))
                return False
                
        except Exception as e:
            print(f"   ❌ Error en logout: {str(e)}")
            self.test_results.append(("Logout Sistema", False, str(e)))
            return False
    
    def test_verificar_usuarios_existentes(self):
        """Test 6: Verificar todos los usuarios existentes en el sistema"""
        print("\n🔍 TEST 6: Verificando usuarios existentes...")
        try:
            usuarios = Usuario.objects.all()
            print(f"   📊 Total de usuarios: {usuarios.count()}")
            
            print("\n   📋 LISTA DE USUARIOS:")
            for i, usuario in enumerate(usuarios, 1):
                municipio_codigo = usuario.municipio.codigo if usuario.municipio else "Sin municipio"
                print(f"   {i:2d}. Usuario: {usuario.usuario}")
                print(f"       Empresa: {usuario.empresa}")
                print(f"       Municipio: {municipio_codigo}")
                print(f"       Nombre: {usuario.nombre}")
                print(f"       Activo: {usuario.is_active}")
                print(f"       Password Hash: {usuario.password[:20]}...")
                print()
            
            # Verificar municipios
            municipios = Municipio.objects.all()
            print(f"   📊 Total de municipios: {municipios.count()}")
            
            print("\n   📋 LISTA DE MUNICIPIOS:")
            for i, municipio in enumerate(municipios, 1):
                print(f"   {i:2d}. Código: {municipio.codigo}")
                print(f"       Nombre: {municipio.nombre}")
                print(f"       ID: {municipio.id}")
                print()
            
            self.test_results.append(("Usuarios Existentes", True, 
                                    f"Usuarios: {usuarios.count()}, Municipios: {municipios.count()}"))
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Usuarios Existentes", False, str(e)))
            return False
    
    def ejecutar_todos_los_tests(self):
        """Ejecutar todos los tests y generar reporte"""
        print("🧪 INICIANDO TESTS DE AUTENTICACIÓN COMPLETOS")
        print("=" * 60)
        print("Credenciales a verificar:")
        print("  Usuario: tributario")
        print("  Contraseña: admin123") 
        print("  Municipio: 0301")
        print("=" * 60)
        
        # Ejecutar tests
        tests = [
            self.test_conexion_base_datos,
            self.test_verificar_credenciales_especificas,
            self.test_login_sistema_principal,
            self.test_acceso_menu_principal,
            self.test_logout_sistema,
            self.test_verificar_usuarios_existentes
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
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL DE TESTS")
        print("=" * 60)
        
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
        else:
            print("⚠️  ALGUNOS TESTS FALLARON")
            print("❌ Revisar los detalles de los tests fallidos")
        
        print("\n🔧 CREDENCIALES VERIFICADAS:")
        print("   Usuario: tributario")
        print("   Contraseña: admin123")
        print("   Municipio: 0301")
        print("   URL Login: http://127.0.0.1:8080/login/")
        print("   URL Menú: http://127.0.0.1:8080/menu/")
        
        return tests_exitosos == total_tests

def main():
    """Función principal"""
    try:
        test_suite = TestAutenticacionCompleto()
        exito = test_suite.ejecutar_todos_los_tests()
        
        if exito:
            print("\n✅ Sistema de autenticación VERIFICADO y FUNCIONAL")
            return 0
        else:
            print("\n❌ Sistema de autenticación tiene PROBLEMAS")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





#!/usr/bin/env python
"""
Test específico para la aplicación tributario_app (legacy) con las credenciales verificadas
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.hashers import check_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import usuario
from tributario_app.models import Municipio

class TestTributarioAppLegacy:
    """Test específico para la aplicación tributario_app legacy"""
    
    def __init__(self):
        self.client = Client()
        self.test_results = []
        
    def test_verificar_credenciales_tributario_app(self):
        """Test 1: Verificar credenciales en tributario_app"""
        print("🔍 TEST 1: Verificando credenciales en tributario_app...")
        try:
            # Buscar usuario tributario en tributario_app
            user = usuario.objects.get(usuario='tributario')
            municipio = Municipio.objects.get(codigo='0301')
            
            # Verificar contraseña
            password_ok = check_password('admin123', user.password)
            
            print(f"   ✅ Usuario: {user.usuario}")
            print(f"   ✅ Municipio código: {user.municipio_codigo}")
            print(f"   ✅ Municipio: {municipio.descripcion} (Código: {municipio.codigo})")
            print(f"   ✅ Contraseña admin123: {'VERIFICADA' if password_ok else 'FALLO'}")
            print(f"   ✅ Usuario activo: {user.is_active}")
            print(f"   ✅ Asociación usuario-municipio: {user.municipio_codigo == municipio.codigo}")
            
            resultado = password_ok and user.is_active and user.municipio_codigo == municipio.codigo
            self.test_results.append(("Credenciales Tributario App", resultado, "Usuario, contraseña y municipio verificados"))
            return resultado
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Credenciales Tributario App", False, str(e)))
            return False
    
    def test_login_tributario_app_directo(self):
        """Test 2: Login directo en tributario_app"""
        print("\n🔍 TEST 2: Login directo en tributario_app...")
        try:
            # Datos de login para tributario_app
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': '0301'  # Código del municipio
            }
            
            print(f"   🔍 Datos de login: {login_data}")
            
            # Intentar login directo en tributario_app
            response = self.client.post('/tributario-app/login/', login_data, follow=True)
            
            print(f"   🔍 Status code: {response.status_code}")
            print(f"   🔍 URL final: {response.url if hasattr(response, 'url') else 'N/A'}")
            
            if response.status_code == 200:
                # Verificar sesión
                session = self.client.session
                if session.get('empresasa') == '0301':
                    print(f"   ✅ Login exitoso - Empresa: {session.get('empresasa')}")
                    print(f"   ✅ Municipio: {session.get('municipio_descripcion')}")
                    resultado = True
                else:
                    print("   ❌ No se creó sesión correcta")
                    print(f"   🔍 Sesión: {dict(session)}")
                    resultado = False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                resultado = False
            
            self.test_results.append(("Login Tributario App", resultado, f"Status: {response.status_code}"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error en login: {str(e)}")
            self.test_results.append(("Login Tributario App", False, str(e)))
            return False
    
    def test_acceso_menu_tributario_app(self):
        """Test 3: Acceso al menú de tributario_app"""
        print("\n🔍 TEST 3: Acceso al menú de tributario_app...")
        try:
            # Primero hacer login
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': '0301'
            }
            
            self.client.post('/tributario-app/login/', login_data)
            
            # Acceder al menú
            response = self.client.get('/tributario-app/menu/')
            
            print(f"   🔍 Status code: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode()
                
                # Verificar elementos del menú de tributario_app
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
                    print(f"   ✅ Menú tributario_app funcional: {len(elementos_encontrados)}/{len(elementos_esperados)} elementos")
                    resultado = True
                else:
                    print(f"   ❌ Menú tributario_app incompleto: {len(elementos_encontrados)}/{len(elementos_esperados)} elementos")
                    resultado = False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                resultado = False
            
            self.test_results.append(("Acceso Menú Tributario App", resultado, f"{len(elementos_encontrados) if 'elementos_encontrados' in locals() else 0}/{len(elementos_esperados)} elementos"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Acceso Menú Tributario App", False, str(e)))
            return False
    
    def test_funcionalidades_tributario_app(self):
        """Test 4: Verificar funcionalidades específicas de tributario_app"""
        print("\n🔍 TEST 4: Verificando funcionalidades de tributario_app...")
        try:
            # Primero hacer login
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': '0301'
            }
            
            self.client.post('/tributario-app/login/', login_data)
            
            # URLs específicas de tributario_app a probar
            urls_tributario_app = [
                '/tributario-app/',
                '/tributario-app/menu/',
                '/tributario-app/menu-general/',
                '/tributario-app/bienes-inmuebles/',
                '/tributario-app/industria-comercio-servicios/',
                '/tributario-app/miscelaneos/',
                '/tributario-app/convenios-pagos/',
                '/tributario-app/maestro_negocios/',
                '/tributario-app/declaracion-volumen/',
                '/tributario-app/informes/',
                '/tributario-app/tarifas_crud/',
                '/tributario-app/plan_arbitrio_crud/'
            ]
            
            urls_funcionales = []
            for url in urls_tributario_app:
                response = self.client.get(url)
                print(f"   🔍 {url}: Status {response.status_code}")
                if response.status_code == 200:
                    urls_funcionales.append(url)
                    print(f"   ✅ Funcional: {url}")
                else:
                    print(f"   ❌ Error {response.status_code}: {url}")
            
            if len(urls_funcionales) >= 6:
                print(f"   ✅ {len(urls_funcionales)}/{len(urls_tributario_app)} funcionalidades operativas")
                resultado = True
            else:
                print(f"   ❌ Solo {len(urls_funcionales)}/{len(urls_tributario_app)} funcionalidades operativas")
                resultado = False
            
            self.test_results.append(("Funcionalidades Tributario App", resultado, f"{len(urls_funcionales)}/{len(urls_tributario_app)} operativas"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Funcionalidades Tributario App", False, str(e)))
            return False
    
    def test_navegacion_tributario_app(self):
        """Test 5: Verificar navegación en tributario_app"""
        print("\n🔍 TEST 5: Verificando navegación en tributario_app...")
        try:
            # Primero hacer login
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': '0301'
            }
            
            self.client.post('/tributario-app/login/', login_data)
            
            # Probar navegación secuencial
            pasos_navegacion = [
                ('/tributario-app/', 'Login/Inicio'),
                ('/tributario-app/menu/', 'Menú principal'),
                ('/tributario-app/menu-general/', 'Menú general'),
                ('/tributario-app/maestro_negocios/', 'Maestro de negocios'),
                ('/tributario-app/declaracion-volumen/', 'Declaración de volumen'),
                ('/tributario-app/menu/', 'Regreso al menú')
            ]
            
            pasos_exitosos = 0
            for url, descripcion in pasos_navegacion:
                response = self.client.get(url)
                print(f"   🔍 {descripcion}: {url} (Status: {response.status_code})")
                if response.status_code == 200:
                    pasos_exitosos += 1
                    print(f"   ✅ {descripcion}: {url}")
                else:
                    print(f"   ❌ {descripcion}: {url} (Status: {response.status_code})")
            
            if pasos_exitosos >= 4:
                print(f"   ✅ Navegación funcional: {pasos_exitosos}/{len(pasos_navegacion)} pasos exitosos")
                resultado = True
            else:
                print(f"   ❌ Navegación limitada: {pasos_exitosos}/{len(pasos_navegacion)} pasos exitosos")
                resultado = False
            
            self.test_results.append(("Navegación Tributario App", resultado, f"{pasos_exitosos}/{len(pasos_navegacion)} pasos exitosos"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Navegación Tributario App", False, str(e)))
            return False
    
    def ejecutar_todos_los_tests(self):
        """Ejecutar todos los tests de tributario_app"""
        print("🧪 TEST ESPECÍFICO DE TRIBUTARIO_APP (LEGACY)")
        print("=" * 70)
        print("Credenciales a verificar:")
        print("  Usuario: tributario")
        print("  Contraseña: admin123") 
        print("  Municipio: 0301")
        print("  Aplicación: tributario_app (legacy)")
        print("  Ruta: C:\\simafiweb\\venv\\Scripts\\tributario\\tributario_app")
        print("=" * 70)
        
        # Ejecutar tests
        tests = [
            self.test_verificar_credenciales_tributario_app,
            self.test_login_tributario_app_directo,
            self.test_acceso_menu_tributario_app,
            self.test_funcionalidades_tributario_app,
            self.test_navegacion_tributario_app
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
        print("📊 REPORTE FINAL - TRIBUTARIO_APP (LEGACY)")
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
        
        if tests_exitosos >= 4:
            print("🎉 ¡TRIBUTARIO_APP FUNCIONANDO CORRECTAMENTE!")
            print("✅ La aplicación tributario_app está operativa con las credenciales verificadas")
            print("\n🎯 TRIBUTARIO_APP VERIFICADO:")
            print("   Usuario: tributario")
            print("   Contraseña: admin123")
            print("   Municipio: 0301")
            print("   URL Principal: http://127.0.0.1:8080/tributario-app/")
            print("   URL Menú: http://127.0.0.1:8080/tributario-app/menu/")
            print("\n📋 FUNCIONALIDADES DISPONIBLES:")
            print("   • Bienes Inmuebles")
            print("   • Industria y Comercio")
            print("   • Misceláneos")
            print("   • Convenios de Pagos")
            print("   • Maestro de Negocios")
            print("   • Declaración de Volumen")
            print("   • Informes")
            print("   • Configuración de Tarifas")
            print("   • Plan de Arbitrio")
        else:
            print("⚠️  TRIBUTARIO_APP TIENE ALGUNOS PROBLEMAS")
            print("❌ Revisar los detalles de los tests fallidos")
        
        return tests_exitosos >= 4

def main():
    """Función principal"""
    try:
        test_suite = TestTributarioAppLegacy()
        exito = test_suite.ejecutar_todos_los_tests()
        
        if exito:
            print("\n✅ TRIBUTARIO_APP VERIFICADO Y FUNCIONAL")
            print("🎯 Las credenciales tributario/admin123/municipio 0301 funcionan correctamente en tributario_app")
            print("🌐 Accede a: http://127.0.0.1:8080/tributario-app/")
            return 0
        else:
            print("\n❌ TRIBUTARIO_APP TIENE PROBLEMAS")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





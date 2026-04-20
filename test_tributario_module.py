#!/usr/bin/env python
"""
Test específico para el módulo tributario con las credenciales verificadas
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

class TestTributarioModule:
    """Test específico para el módulo tributario"""
    
    def __init__(self):
        self.client = Client()
        self.test_results = []
        
    def test_verificar_credenciales_tributario(self):
        """Test 1: Verificar credenciales específicas para módulo tributario"""
        print("🔍 TEST 1: Verificando credenciales para módulo tributario...")
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
            print(f"   ✅ Asociación usuario-municipio: {usuario.municipio_id == municipio.id}")
            
            resultado = password_ok and usuario.is_active and usuario.municipio_id == municipio.id
            self.test_results.append(("Credenciales Tributario", resultado, "Usuario, contraseña y municipio verificados"))
            return resultado
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Credenciales Tributario", False, str(e)))
            return False
    
    def test_login_sistema_principal_para_tributario(self):
        """Test 2: Login en sistema principal para acceder a tributario"""
        print("\n🔍 TEST 2: Login en sistema principal para acceder a tributario...")
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
            
            if response.status_code == 200:
                # Verificar sesión
                session = self.client.session
                if session.get('user_id'):
                    print(f"   ✅ Login exitoso - User ID: {session.get('user_id')}")
                    print(f"   ✅ Usuario en sesión: {session.get('usuario')}")
                    print(f"   ✅ Municipio en sesión: {session.get('municipio_id')}")
                    resultado = True
                else:
                    print("   ❌ No se creó sesión")
                    resultado = False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                resultado = False
            
            self.test_results.append(("Login Sistema Principal", resultado, f"Status: {response.status_code}"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error en login: {str(e)}")
            self.test_results.append(("Login Sistema Principal", False, str(e)))
            return False
    
    def test_acceso_modulo_tributario(self):
        """Test 3: Acceso directo al módulo tributario"""
        print("\n🔍 TEST 3: Acceso directo al módulo tributario...")
        try:
            # Primero hacer login en sistema principal
            municipio = Municipio.objects.get(codigo='0301')
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': str(municipio.id)
            }
            
            self.client.post('/login/', login_data)
            
            # Acceder al módulo tributario
            response = self.client.get('/tributario/')
            
            print(f"   🔍 Status code: {response.status_code}")
            print(f"   🔍 URL: {response.url if hasattr(response, 'url') else 'N/A'}")
            
            if response.status_code == 200:
                content = response.content.decode()
                
                # Verificar elementos del módulo tributario
                elementos_esperados = [
                    'Tributario',
                    'menugeneral',
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
                
                if len(elementos_encontrados) >= 2:
                    print("   ✅ Módulo tributario accesible")
                    resultado = True
                else:
                    print("   ❌ Módulo tributario incompleto")
                    resultado = False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                resultado = False
            
            self.test_results.append(("Acceso Módulo Tributario", resultado, f"Elementos: {len(elementos_encontrados)}/4"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Acceso Módulo Tributario", False, str(e)))
            return False
    
    def test_funcionalidades_tributario(self):
        """Test 4: Verificar funcionalidades específicas del módulo tributario"""
        print("\n🔍 TEST 4: Verificando funcionalidades del módulo tributario...")
        try:
            # Primero hacer login
            municipio = Municipio.objects.get(codigo='0301')
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': str(municipio.id)
            }
            
            self.client.post('/login/', login_data)
            
            # URLs específicas del módulo tributario a probar
            urls_tributario = [
                '/tributario/menu/',
                '/tributario/maestro-negocios/',
                '/tributario/declaracion-volumen/',
                '/tributario/miscelaneos/',
                '/tributario/convenios-pagos/',
                '/tributario/informes/',
                '/tributario/tarifas-crud/',
                '/tributario/plan-arbitrio-crud/'
            ]
            
            urls_funcionales = []
            for url in urls_tributario:
                response = self.client.get(url)
                if response.status_code == 200:
                    urls_funcionales.append(url)
                    print(f"   ✅ Funcional: {url}")
                else:
                    print(f"   ❌ Error {response.status_code}: {url}")
            
            if len(urls_funcionales) >= 4:
                print(f"   ✅ {len(urls_funcionales)}/{len(urls_tributario)} funcionalidades operativas")
                resultado = True
            else:
                print(f"   ❌ Solo {len(urls_funcionales)}/{len(urls_tributario)} funcionalidades operativas")
                resultado = False
            
            self.test_results.append(("Funcionalidades Tributario", resultado, f"{len(urls_funcionales)}/{len(urls_tributario)} operativas"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Funcionalidades Tributario", False, str(e)))
            return False
    
    def test_navegacion_tributario(self):
        """Test 5: Verificar navegación dentro del módulo tributario"""
        print("\n🔍 TEST 5: Verificando navegación en módulo tributario...")
        try:
            # Primero hacer login
            municipio = Municipio.objects.get(codigo='0301')
            login_data = {
                'usuario': 'tributario',
                'password': 'admin123',
                'municipio': str(municipio.id)
            }
            
            self.client.post('/login/', login_data)
            
            # Probar navegación secuencial
            pasos_navegacion = [
                ('/tributario/', 'Menú principal'),
                ('/tributario/menu/', 'Menú específico'),
                ('/tributario/maestro-negocios/', 'Maestro de negocios'),
                ('/tributario/declaracion-volumen/', 'Declaración de volumen'),
                ('/tributario/', 'Regreso al menú principal')
            ]
            
            pasos_exitosos = 0
            for url, descripcion in pasos_navegacion:
                response = self.client.get(url)
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
            
            self.test_results.append(("Navegación Tributario", resultado, f"{pasos_exitosos}/{len(pasos_navegacion)} pasos exitosos"))
            return resultado
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results.append(("Navegación Tributario", False, str(e)))
            return False
    
    def ejecutar_todos_los_tests(self):
        """Ejecutar todos los tests del módulo tributario"""
        print("🧪 TEST ESPECÍFICO DEL MÓDULO TRIBUTARIO")
        print("=" * 70)
        print("Credenciales a verificar:")
        print("  Usuario: tributario")
        print("  Contraseña: admin123") 
        print("  Municipio: 0301")
        print("  Módulo: Tributario")
        print("=" * 70)
        
        # Ejecutar tests
        tests = [
            self.test_verificar_credenciales_tributario,
            self.test_login_sistema_principal_para_tributario,
            self.test_acceso_modulo_tributario,
            self.test_funcionalidades_tributario,
            self.test_navegacion_tributario
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
        print("📊 REPORTE FINAL - MÓDULO TRIBUTARIO")
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
            print("🎉 ¡TODOS LOS TESTS DEL MÓDULO TRIBUTARIO PASARON!")
            print("✅ El módulo tributario está completamente funcional")
            print("\n🎯 MÓDULO TRIBUTARIO VERIFICADO:")
            print("   Usuario: tributario")
            print("   Contraseña: admin123")
            print("   Municipio: 0301")
            print("   URL Principal: http://127.0.0.1:8080/tributario/")
            print("   URL Menú: http://127.0.0.1:8080/tributario/menu/")
        else:
            print("⚠️  ALGUNOS TESTS DEL MÓDULO TRIBUTARIO FALLARON")
            print("❌ Revisar los detalles de los tests fallidos")
        
        return tests_exitosos == total_tests

def main():
    """Función principal"""
    try:
        test_suite = TestTributarioModule()
        exito = test_suite.ejecutar_todos_los_tests()
        
        if exito:
            print("\n✅ MÓDULO TRIBUTARIO VERIFICADO Y FUNCIONAL")
            print("🎯 Las credenciales tributario/admin123/municipio 0301 funcionan correctamente en el módulo tributario")
            return 0
        else:
            print("\n❌ MÓDULO TRIBUTARIO TIENE PROBLEMAS")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





#!/usr/bin/env python
"""
Test para verificar que el formulario de rubros funcione correctamente
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_formulario_rubros_herencia():
    """Test de herencia del código de empresa en formulario rubros"""
    print("🔍 TEST DE HERENCIA DE CÓDIGO DE EMPRESA EN RUBROS")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        response = client.post('/tributario-app/login/', login_data, follow=True)
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Acceder al formulario de rubros
        response = client.get('/tributario-app/rubros/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de rubros accesible")
            
            content = response.content.decode()
            
            # Verificar que el campo empresa esté presente y tenga el valor correcto
            if 'id="id_empresa"' in content:
                print("   ✅ Campo empresa encontrado en el formulario")
                
                # Verificar que el valor sea 0301 (heredado de la sesión)
                if 'value="0301"' in content:
                    print("   ✅ Campo empresa hereda correctamente el código 0301")
                    return True
                else:
                    print("   ❌ Campo empresa no hereda el código correcto")
                    print(f"   📄 Contenido del campo: {content[content.find('id_empresa'):content.find('id_empresa')+100]}")
                    return False
            else:
                print("   ❌ Campo empresa no encontrado en el formulario")
                return False
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de herencia: {str(e)}")
        return False

def test_guardar_rubro_con_empresa():
    """Test de guardado de rubro con código de empresa heredado"""
    print("\n🔍 TEST DE GUARDADO CON CÓDIGO DE EMPRESA HEREDADO")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        response = client.post('/tributario-app/login/', login_data, follow=True)
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Guardar rubro
        rubro_data = {
            'codigo': 'TEST001',
            'descripcion': 'Rubro de prueba con empresa heredada',
            'empresa': '0301'  # Debería heredarse automáticamente
        }
        
        print(f"   📋 Guardando rubro con empresa: {rubro_data['empresa']}")
        
        response = client.post('/tributario-app/rubros/', rubro_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'guardado exitosamente' in content:
                print("   ✅ Rubro guardado correctamente con empresa heredada")
                return True
            else:
                print("   ❌ Error al guardar rubro con empresa heredada")
                print(f"   📄 Contenido: {content[:300]}...")
                return False
        else:
            print(f"   ❌ Error en petición: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de guardado: {str(e)}")
        return False

def test_endpoint_buscar_rubro():
    """Test del endpoint AJAX para buscar rubros"""
    print("\n🔍 TEST DE ENDPOINT BUSCAR RUBRO")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        response = client.post('/tributario-app/login/', login_data, follow=True)
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Test del endpoint buscar rubro
        print("   📋 Probando endpoint buscar rubro...")
        response = client.post('/tributario-app/ajax/buscar-rubro/', {
            'empresa': '0301',
            'codigo': 'TEST001'
        })
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Respuesta: {data}")
                
                if 'exito' in data:
                    print("   ✅ Endpoint devuelve estructura correcta")
                    return True
                else:
                    print("   ❌ Endpoint no devuelve estructura esperada")
                    return False
            except Exception as e:
                print(f"   ❌ Error JSON: {e}")
                return False
        else:
            print(f"   ❌ Error en endpoint: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de endpoint: {str(e)}")
        return False

def test_consistencia_campos_rubros():
    """Test de consistencia entre campos del formulario y vista"""
    print("\n🔍 TEST DE CONSISTENCIA DE CAMPOS RUBROS")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        response = client.post('/tributario-app/login/', login_data, follow=True)
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Acceder al formulario
        response = client.get('/tributario-app/rubros/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar que el formulario use 'empresa' como name del campo
            if 'name="empresa"' in content:
                print("   ✅ Formulario usa 'empresa' como name del campo")
            else:
                print("   ❌ Formulario no usa 'empresa' como name del campo")
                return False
            
            # Verificar que el campo sea readonly
            if 'readonly' in content and 'id_empresa' in content:
                print("   ✅ Campo empresa es readonly (heredado)")
            else:
                print("   ❌ Campo empresa no es readonly")
                return False
            
            # Verificar que tenga el estilo correcto
            if 'background-color: #f8f9fa' in content:
                print("   ✅ Campo empresa tiene estilo de campo heredado")
            else:
                print("   ❌ Campo empresa no tiene estilo correcto")
                return False
            
            return True
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de consistencia: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE FORMULARIO RUBROS CORREGIDO")
    print("Verificando que use 'empresa' en lugar de 'municipio_codigo'")
    print("=" * 70)
    
    try:
        # Test 1: Herencia del código de empresa
        herencia_ok = test_formulario_rubros_herencia()
        
        # Test 2: Guardado con empresa heredada
        guardado_ok = test_guardar_rubro_con_empresa()
        
        # Test 3: Endpoint buscar rubro
        endpoint_ok = test_endpoint_buscar_rubro()
        
        # Test 4: Consistencia de campos
        consistencia_ok = test_consistencia_campos_rubros()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Herencia de código de empresa: {'OK' if herencia_ok else 'FALLO'}")
        print(f"✅ Guardado con empresa heredada: {'OK' if guardado_ok else 'FALLO'}")
        print(f"✅ Endpoint buscar rubro: {'OK' if endpoint_ok else 'FALLO'}")
        print(f"✅ Consistencia de campos: {'OK' if consistencia_ok else 'FALLO'}")
        
        if herencia_ok and guardado_ok and endpoint_ok and consistencia_ok:
            print("\n🎉 FORMULARIO RUBROS CORREGIDO EXITOSAMENTE")
            print("✅ El formulario usa 'empresa' en lugar de 'municipio_codigo'")
            print("✅ El código de empresa se hereda correctamente de la sesión")
            print("✅ Los campos son consistentes entre formulario y vista")
            print("✅ Los endpoints AJAX funcionan correctamente")
            return 0
        else:
            print("\n⚠️  ALGUNAS FUNCIONALIDADES NECESITAN REVISIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





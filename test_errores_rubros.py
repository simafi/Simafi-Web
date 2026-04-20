#!/usr/bin/env python
"""
Test para identificar errores específicos en el formulario de rubros
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_formulario_rubros_errores():
    """Test para identificar errores en el formulario de rubros"""
    print("🔍 TEST DE ERRORES EN FORMULARIO RUBROS")
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
        
        # Test 1: Acceder al formulario de rubros
        print("   📋 Accediendo al formulario de rubros...")
        response = client.get('/tributario-app/rubros/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de rubros accesible")
            content = response.content.decode()
            
            # Verificar si hay errores de formulario
            if 'error' in content.lower() or 'invalid' in content.lower():
                print("   ⚠️  Se detectaron errores en el formulario")
                print(f"   📄 Contenido con errores: {content[:500]}...")
            else:
                print("   ✅ No se detectaron errores obvios en el formulario")
            
            # Verificar que el campo empresa esté presente
            if 'id="id_empresa"' in content:
                print("   ✅ Campo empresa encontrado")
                
                if 'value="0301"' in content:
                    print("   ✅ Campo empresa tiene valor correcto")
                else:
                    print("   ❌ Campo empresa no tiene valor correcto")
                    return False
            else:
                print("   ❌ Campo empresa no encontrado")
                return False
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
        
        # Test 2: Intentar guardar un rubro
        print("   📋 Intentando guardar un rubro...")
        rubro_data = {
            'codigo': 'TEST001',
            'descripcion': 'Rubro de prueba',
            'empresa': '0301'
        }
        
        response = client.post('/tributario-app/rubros/', rubro_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'guardado exitosamente' in content:
                print("   ✅ Rubro guardado correctamente")
            elif 'error' in content.lower():
                print("   ❌ Error al guardar rubro")
                print(f"   📄 Contenido del error: {content[:500]}...")
                return False
            else:
                print("   ⚠️  Respuesta inesperada al guardar")
                print(f"   📄 Contenido: {content[:300]}...")
        else:
            print(f"   ❌ Error en petición POST: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_endpoint_buscar_rubro_errores():
    """Test del endpoint buscar rubro para identificar errores"""
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
        
        print(f"   📄 Status code: {response.status_code}")
        print(f"   📄 Content-Type: {response.get('Content-Type', 'No definido')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Respuesta JSON: {data}")
                return True
            except Exception as e:
                print(f"   ❌ Error al parsear JSON: {e}")
                print(f"   📄 Contenido: {response.content.decode()[:300]}...")
                return False
        else:
            print(f"   ❌ Error en endpoint: {response.status_code}")
            print(f"   📄 Contenido: {response.content.decode()[:300]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

def test_verificar_formulario_rubros():
    """Test para verificar la estructura del formulario de rubros"""
    print("\n🔍 TEST DE ESTRUCTURA DEL FORMULARIO")
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
            
            # Verificar elementos del formulario
            elementos_requeridos = [
                'id="id_empresa"',
                'id="id_codigo"',
                'id="id_descripcion"',
                'name="empresa"',
                'name="codigo"',
                'name="descripcion"'
            ]
            
            for elemento in elementos_requeridos:
                if elemento in content:
                    print(f"   ✅ Elemento encontrado: {elemento}")
                else:
                    print(f"   ❌ Elemento faltante: {elemento}")
                    return False
            
            # Verificar que no haya errores de sintaxis
            if 'syntax error' in content.lower() or 'parse error' in content.lower():
                print("   ❌ Se detectaron errores de sintaxis en el template")
                return False
            else:
                print("   ✅ No se detectaron errores de sintaxis")
            
            return True
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE ERRORES EN FORMULARIO RUBROS")
    print("Identificando errores específicos para corregir")
    print("=" * 70)
    
    try:
        # Test 1: Errores en formulario
        formulario_ok = test_formulario_rubros_errores()
        
        # Test 2: Errores en endpoint
        endpoint_ok = test_endpoint_buscar_rubro_errores()
        
        # Test 3: Estructura del formulario
        estructura_ok = test_verificar_formulario_rubros()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Formulario rubros: {'OK' if formulario_ok else 'FALLO'}")
        print(f"✅ Endpoint buscar rubro: {'OK' if endpoint_ok else 'FALLO'}")
        print(f"✅ Estructura del formulario: {'OK' if estructura_ok else 'FALLO'}")
        
        if formulario_ok and endpoint_ok and estructura_ok:
            print("\n🎉 FORMULARIO RUBROS FUNCIONANDO CORRECTAMENTE")
            return 0
        else:
            print("\n⚠️  SE DETECTARON ERRORES QUE NECESITAN CORRECCIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





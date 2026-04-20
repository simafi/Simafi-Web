#!/usr/bin/env python
"""
Test para verificar que las correcciones del formulario de rubros funcionen
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_formulario_rubros_corregido():
    """Test del formulario de rubros con las correcciones aplicadas"""
    print("🔍 TEST DE FORMULARIO RUBROS CORREGIDO")
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
        
        # Test 1: Acceder al formulario
        print("   📋 Accediendo al formulario de rubros...")
        response = client.get('/tributario-app/rubros/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de rubros accesible")
            content = response.content.decode()
            
            # Verificar que no haya errores de formulario
            if 'error' in content.lower() and 'form' in content.lower():
                print("   ❌ Se detectaron errores de formulario")
                print(f"   📄 Contenido con errores: {content[:500]}...")
                return False
            else:
                print("   ✅ No se detectaron errores de formulario")
            
            # Verificar que el campo empresa esté presente
            if 'id="id_empresa"' in content and 'value="0301"' in content:
                print("   ✅ Campo empresa correcto")
            else:
                print("   ❌ Campo empresa incorrecto")
                return False
            
            # Verificar que el campo cuentarez esté presente
            if 'id="id_cuentarez"' in content and 'name="cuentarez"' in content:
                print("   ✅ Campo cuentarez corregido")
            else:
                print("   ❌ Campo cuentarez no corregido")
                return False
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
        
        # Test 2: Intentar guardar un rubro
        print("   📋 Intentando guardar un rubro...")
        rubro_data = {
            'codigo': 'TEST',
            'descripcion': 'Rubro de prueba corregido',
            'cuenta': '001',
            'cuentarez': '002',
            'tipo': 'I',
            'empresa': '0301'
        }
        
        response = client.post('/tributario-app/rubros/', rubro_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'guardado exitosamente' in content:
                print("   ✅ Rubro guardado correctamente")
                return True
            elif 'error' in content.lower():
                print("   ❌ Error al guardar rubro")
                print(f"   📄 Contenido del error: {content[:500]}...")
                return False
            else:
                print("   ⚠️  Respuesta inesperada al guardar")
                print(f"   📄 Contenido: {content[:300]}...")
                return False
        else:
            print(f"   ❌ Error en petición POST: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_verificar_campos_formulario():
    """Test para verificar que todos los campos del formulario estén correctos"""
    print("\n🔍 TEST DE CAMPOS DEL FORMULARIO")
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
            
            # Verificar campos requeridos
            campos_requeridos = [
                'id="id_empresa"',
                'id="id_codigo"',
                'id="id_descripcion"',
                'id="id_cuenta"',
                'id="id_cuentarez"',
                'id="id_tipo"',
                'name="empresa"',
                'name="codigo"',
                'name="descripcion"',
                'name="cuenta"',
                'name="cuentarez"',
                'name="tipo"'
            ]
            
            for campo in campos_requeridos:
                if campo in content:
                    print(f"   ✅ Campo encontrado: {campo}")
                else:
                    print(f"   ❌ Campo faltante: {campo}")
                    return False
            
            return True
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE CORRECCIÓN DE FORMULARIO RUBROS")
    print("Verificando que los errores tipográficos estén corregidos")
    print("=" * 70)
    
    try:
        # Test 1: Formulario corregido
        formulario_ok = test_formulario_rubros_corregido()
        
        # Test 2: Campos del formulario
        campos_ok = test_verificar_campos_formulario()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Formulario rubros corregido: {'OK' if formulario_ok else 'FALLO'}")
        print(f"✅ Campos del formulario: {'OK' if campos_ok else 'FALLO'}")
        
        if formulario_ok and campos_ok:
            print("\n🎉 FORMULARIO RUBROS CORREGIDO EXITOSAMENTE")
            print("✅ Los errores tipográficos han sido corregidos")
            print("✅ El formulario funciona correctamente")
            print("✅ Todos los campos están presentes y correctos")
            return 0
        else:
            print("\n⚠️  ALGUNAS CORRECCIONES NECESITAN REVISIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





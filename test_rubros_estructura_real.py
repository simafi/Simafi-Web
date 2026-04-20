#!/usr/bin/env python
"""
Test para verificar que el formulario de rubros funcione con la estructura real de la BD
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_formulario_rubros_estructura_real():
    """Test del formulario de rubros con la estructura real de la BD"""
    print("🔍 TEST DE FORMULARIO RUBROS - ESTRUCTURA REAL BD")
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
            
            # Verificar que no haya errores de base de datos
            if 'Unknown column' in content or 'OperationalError' in content:
                print("   ❌ Error de base de datos detectado")
                print(f"   📄 Contenido del error: {content[:500]}...")
                return False
            else:
                print("   ✅ No se detectaron errores de base de datos")
            
            # Verificar que el campo empresa esté presente
            if 'id="id_empresa"' in content and 'value="0301"' in content:
                print("   ✅ Campo empresa correcto")
            else:
                print("   ❌ Campo empresa incorrecto")
                return False
            
            # Verificar que el campo cuntarez esté presente (con error tipográfico de la BD)
            if 'id="id_cuntarez"' in content and 'name="cuntarez"' in content:
                print("   ✅ Campo cuntarez correcto (coincide con BD)")
            else:
                print("   ❌ Campo cuntarez incorrecto")
                return False
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
        
        # Test 2: Intentar guardar un rubro
        print("   📋 Intentando guardar un rubro...")
        rubro_data = {
            'codigo': 'TEST',
            'descripcion': 'Rubro de prueba estructura real',
            'cuenta': '001',
            'cuntarez': '002',
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

def test_verificar_campos_estructura_real():
    """Test para verificar que todos los campos coincidan con la estructura real"""
    print("\n🔍 TEST DE CAMPOS - ESTRUCTURA REAL BD")
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
            
            # Verificar campos según la estructura real de la BD
            campos_requeridos = [
                'id="id_empresa"',
                'id="id_codigo"',
                'id="id_descripcion"',
                'id="id_cuenta"',
                'id="id_cuntarez"',  # Con error tipográfico como en la BD
                'id="id_tipo"',
                'name="empresa"',
                'name="codigo"',
                'name="descripcion"',
                'name="cuenta"',
                'name="cuntarez"',  # Con error tipográfico como en la BD
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
    print("🧪 TEST DE FORMULARIO RUBROS - ESTRUCTURA REAL BD")
    print("Verificando que coincida con la estructura real de la base de datos")
    print("=" * 70)
    
    try:
        # Test 1: Formulario con estructura real
        formulario_ok = test_formulario_rubros_estructura_real()
        
        # Test 2: Campos con estructura real
        campos_ok = test_verificar_campos_estructura_real()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Formulario rubros estructura real: {'OK' if formulario_ok else 'FALLO'}")
        print(f"✅ Campos estructura real: {'OK' if campos_ok else 'FALLO'}")
        
        if formulario_ok and campos_ok:
            print("\n🎉 FORMULARIO RUBROS CORREGIDO PARA ESTRUCTURA REAL")
            print("✅ El formulario coincide con la estructura real de la BD")
            print("✅ El campo 'cuntarez' mantiene el error tipográfico de la BD")
            print("✅ El formulario funciona correctamente")
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





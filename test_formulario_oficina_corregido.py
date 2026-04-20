#!/usr/bin/env python
"""
Test para verificar que el formulario de oficina herede correctamente el código de empresa
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_formulario_oficina_herencia():
    """Test de herencia del código de empresa en formulario oficina"""
    print("🔍 TEST DE HERENCIA DE CÓDIGO DE EMPRESA EN OFICINA")
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
        
        # Acceder al formulario de oficina
        response = client.get('/tributario-app/oficina/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de oficina accesible")
            
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

def test_guardar_oficina_con_empresa():
    """Test de guardado de oficina con código de empresa heredado"""
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
        
        # Guardar oficina usando el campo 'empresa' en lugar de 'municipio_codigo'
        oficina_data = {
            'accion': 'guardar',
            'empresa': '0301',  # Usando 'empresa' en lugar de 'municipio_codigo'
            'codigo': 'TEST001',
            'descripcion': 'Oficina de prueba con empresa heredada'
        }
        
        print(f"   📋 Guardando oficina con empresa: {oficina_data['empresa']}")
        
        response = client.post('/tributario-app/oficina/', oficina_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'creada correctamente' in content or 'actualizada correctamente' in content:
                print("   ✅ Oficina guardada correctamente con empresa heredada")
                return True
            else:
                print("   ❌ Error al guardar oficina con empresa heredada")
                print(f"   📄 Contenido: {content[:300]}...")
                return False
        else:
            print(f"   ❌ Error en petición: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de guardado: {str(e)}")
        return False

def test_eliminar_oficina_corregido():
    """Test de eliminación de oficina con corrección aplicada"""
    print("\n🔍 TEST DE ELIMINACIÓN DE OFICINA CORREGIDO")
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
        
        # Primero crear una oficina para poder eliminarla
        oficina_data = {
            'accion': 'guardar',
            'empresa': '0301',
            'codigo': 'TEST_DELETE',
            'descripcion': 'Oficina para probar eliminación'
        }
        
        print("   📋 Creando oficina de prueba...")
        response = client.post('/tributario-app/oficina/', oficina_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            if 'creada correctamente' in content or 'actualizada correctamente' in content:
                print("   ✅ Oficina creada correctamente")
            else:
                print("   ⚠️  Oficina no se creó, pero continuando con el test...")
        
        # Ahora intentar eliminar la oficina
        eliminar_data = {
            'accion': 'eliminar',
            'empresa': '0301',
            'codigo': 'TEST_DELETE'
        }
        
        print("   📋 Eliminando oficina de prueba...")
        response = client.post('/tributario-app/oficina/', eliminar_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'eliminada correctamente' in content:
                print("   ✅ Oficina eliminada correctamente")
                return True
            elif 'Cannot resolve keyword' in content:
                print("   ❌ Error de conflicto de variables aún presente")
                print(f"   📄 Contenido: {content[:200]}...")
                return False
            else:
                print("   ⚠️  Respuesta inesperada")
                print(f"   📄 Contenido: {content[:200]}...")
                return False
        else:
            print(f"   ❌ Error en petición: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de eliminación: {str(e)}")
        return False

def test_consistencia_campos_oficina():
    """Test de consistencia entre campos del formulario y vista"""
    print("\n🔍 TEST DE CONSISTENCIA DE CAMPOS OFICINA")
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
        response = client.get('/tributario-app/oficina/')
        
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
    print("🧪 TEST DE FORMULARIO OFICINA CORREGIDO")
    print("Verificando que use 'empresa' en lugar de 'municipio_codigo'")
    print("=" * 70)
    
    try:
        # Test 1: Herencia del código de empresa
        herencia_ok = test_formulario_oficina_herencia()
        
        # Test 2: Guardado con empresa heredada
        guardado_ok = test_guardar_oficina_con_empresa()
        
        # Test 3: Eliminación corregida
        eliminacion_ok = test_eliminar_oficina_corregido()
        
        # Test 4: Consistencia de campos
        consistencia_ok = test_consistencia_campos_oficina()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Herencia de código de empresa: {'OK' if herencia_ok else 'FALLO'}")
        print(f"✅ Guardado con empresa heredada: {'OK' if guardado_ok else 'FALLO'}")
        print(f"✅ Eliminación corregida: {'OK' if eliminacion_ok else 'FALLO'}")
        print(f"✅ Consistencia de campos: {'OK' if consistencia_ok else 'FALLO'}")
        
        if herencia_ok and guardado_ok and eliminacion_ok and consistencia_ok:
            print("\n🎉 FORMULARIO OFICINA CORREGIDO EXITOSAMENTE")
            print("✅ El formulario usa 'empresa' en lugar de 'municipio_codigo'")
            print("✅ El código de empresa se hereda correctamente de la sesión")
            print("✅ Los campos son consistentes entre formulario y vista")
            print("✅ Las operaciones CRUD funcionan correctamente")
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





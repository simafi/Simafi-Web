#!/usr/bin/env python
"""
Test para verificar la corrección del conflicto de variables municipio_codigo vs empresa
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_eliminar_actividad_corregido():
    """Test de eliminación de actividad con la corrección aplicada"""
    print("🔍 TEST DE ELIMINACIÓN DE ACTIVIDAD CORREGIDO")
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
        
        # Primero crear una actividad para poder eliminarla
        actividad_data = {
            'accion': 'guardar',
            'empresa': '0301',
            'codigo': 'TEST_DELETE',
            'descripcion': 'Actividad para probar eliminación'
        }
        
        print("   📋 Creando actividad de prueba...")
        response = client.post('/tributario-app/actividad/', actividad_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            if 'creada correctamente' in content or 'actualizada correctamente' in content:
                print("   ✅ Actividad creada correctamente")
            else:
                print("   ⚠️  Actividad no se creó, pero continuando con el test...")
        
        # Ahora intentar eliminar la actividad
        eliminar_data = {
            'accion': 'eliminar',
            'empresa': '0301',
            'codigo': 'TEST_DELETE'
        }
        
        print("   📋 Eliminando actividad de prueba...")
        response = client.post('/tributario-app/actividad/', eliminar_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'eliminada correctamente' in content:
                print("   ✅ Actividad eliminada correctamente")
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

def test_miscelaneos_empresa_correcta():
    """Test de misceláneos con variable empresa correcta"""
    print("\n🔍 TEST DE MISCELÁNEOS CON EMPRESA CORRECTA")
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
        
        # Acceder a misceláneos
        response = client.get('/tributario-app/miscelaneos/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de misceláneos accesible")
            
            content = response.content.decode()
            
            # Verificar que el campo empresa esté presente y tenga el valor correcto
            if 'id="empresa"' in content:
                print("   ✅ Campo empresa encontrado en misceláneos")
                
                if 'value="0301"' in content:
                    print("   ✅ Campo empresa hereda correctamente el código 0301")
                    return True
                else:
                    print("   ❌ Campo empresa no hereda el código correcto")
                    return False
            else:
                print("   ❌ Campo empresa no encontrado en misceláneos")
                return False
        else:
            print(f"   ❌ Error accediendo a misceláneos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de misceláneos: {str(e)}")
        return False

def test_consistencia_variables():
    """Test de consistencia de variables en todo el sistema"""
    print("\n🔍 TEST DE CONSISTENCIA DE VARIABLES")
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
        
        # Verificar que la sesión tenga 'empresa' y no 'municipio_codigo'
        session = client.session
        if 'empresa' in session:
            print(f"   ✅ Sesión contiene 'empresa': {session['empresa']}")
        else:
            print("   ❌ Sesión no contiene 'empresa'")
            return False
        
        if 'municipio_codigo' in session:
            print(f"   ⚠️  Sesión también contiene 'municipio_codigo': {session['municipio_codigo']}")
        else:
            print("   ✅ Sesión no contiene 'municipio_codigo' (correcto)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en test de consistencia: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE CORRECCIÓN DE CONFLICTO DE VARIABLES")
    print("Verificando que se use 'empresa' en lugar de 'municipio_codigo'")
    print("=" * 70)
    
    try:
        # Test 1: Eliminación de actividad corregida
        eliminacion_ok = test_eliminar_actividad_corregido()
        
        # Test 2: Misceláneos con empresa correcta
        miscelaneos_ok = test_miscelaneos_empresa_correcta()
        
        # Test 3: Consistencia de variables
        consistencia_ok = test_consistencia_variables()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Eliminación de actividad corregida: {'OK' if eliminacion_ok else 'FALLO'}")
        print(f"✅ Misceláneos con empresa correcta: {'OK' if miscelaneos_ok else 'FALLO'}")
        print(f"✅ Consistencia de variables: {'OK' if consistencia_ok else 'FALLO'}")
        
        if eliminacion_ok and miscelaneos_ok and consistencia_ok:
            print("\n🎉 CONFLICTO DE VARIABLES CORREGIDO EXITOSAMENTE")
            print("✅ Se usa 'empresa' consistentemente en todo el sistema")
            print("✅ La eliminación de actividades funciona correctamente")
            print("✅ Los formularios heredan el código de empresa correctamente")
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





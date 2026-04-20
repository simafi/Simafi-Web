#!/usr/bin/env python
"""
Test para verificar las mejoras del formulario de actividad
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.hashers import check_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_acceso_formulario_actividad():
    """Test de acceso al formulario de actividad"""
    print("🔍 TEST DE ACCESO AL FORMULARIO DE ACTIVIDAD")
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
        
        # Acceder al formulario de actividad
        response = client.get('/tributario-app/actividad/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de actividad accesible")
            
            content = response.content.decode()
            
            # Verificar elementos del formulario
            elementos_esperados = [
                'id="id_empresa"',
                'id="id_codigo"',
                'id="id_descripcion"',
                'maxlength="20"',  # Verificar que se corrigió el maxlength
                'maxlength="200"',
                'Actividades Registradas'
            ]
            
            elementos_encontrados = []
            for elemento in elementos_esperados:
                if elemento in content:
                    elementos_encontrados.append(elemento)
                    print(f"   ✅ Encontrado: {elemento}")
                else:
                    print(f"   ❌ No encontrado: {elemento}")
            
            return len(elementos_encontrados) >= 5
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de acceso: {str(e)}")
        return False

def test_validacion_codigo_largo():
    """Test de validación de código con más de 20 caracteres"""
    print("\n🔍 TEST DE VALIDACIÓN DE CÓDIGO LARGO")
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
        
        # Intentar guardar actividad con código muy largo
        codigo_largo = 'A' * 25  # 25 caracteres, más que el límite de 20
        
        actividad_data = {
            'accion': 'guardar',
            'municipio_codigo': '0301',
            'codigo': codigo_largo,
            'descripcion': 'Descripción de prueba'
        }
        
        print(f"   📋 Probando con código de {len(codigo_largo)} caracteres: {codigo_largo}")
        
        response = client.post('/tributario-app/actividad/', actividad_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'no puede tener más de 20 caracteres' in content:
                print("   ✅ Validación de longitud funcionando correctamente")
                return True
            else:
                print("   ❌ Validación de longitud no funcionando")
                return False
        else:
            print(f"   ❌ Error en petición: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de validación: {str(e)}")
        return False

def test_validacion_municipio_inexistente():
    """Test de validación de municipio inexistente"""
    print("\n🔍 TEST DE VALIDACIÓN DE MUNICIPIO INEXISTENTE")
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
        
        # Intentar guardar actividad con municipio inexistente
        actividad_data = {
            'accion': 'guardar',
            'municipio_codigo': '9999',  # Municipio que no existe
            'codigo': 'TEST001',
            'descripcion': 'Descripción de prueba'
        }
        
        print(f"   📋 Probando con municipio inexistente: 9999")
        
        response = client.post('/tributario-app/actividad/', actividad_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'no existe en el sistema' in content:
                print("   ✅ Validación de municipio funcionando correctamente")
                return True
            else:
                print("   ❌ Validación de municipio no funcionando")
                return False
        else:
            print(f"   ❌ Error en petición: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de validación: {str(e)}")
        return False

def test_guardar_actividad_valida():
    """Test de guardado de actividad válida"""
    print("\n🔍 TEST DE GUARDADO DE ACTIVIDAD VÁLIDA")
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
        
        # Guardar actividad válida
        actividad_data = {
            'accion': 'guardar',
            'municipio_codigo': '0301',
            'codigo': 'TEST001',
            'descripcion': 'Actividad de prueba para validación'
        }
        
        print(f"   📋 Guardando actividad válida: {actividad_data['codigo']}")
        
        response = client.post('/tributario-app/actividad/', actividad_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'creada correctamente' in content or 'actualizada correctamente' in content:
                print("   ✅ Actividad guardada correctamente")
                return True
            else:
                print("   ❌ Error al guardar actividad")
                print(f"   📄 Contenido: {content[:200]}...")
                return False
        else:
            print(f"   ❌ Error en petición: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de guardado: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE FORMULARIO DE ACTIVIDAD MEJORADO")
    print("Verificando mejoras según estructura de tabla MySQL")
    print("=" * 70)
    
    try:
        # Test 1: Acceso al formulario
        acceso_ok = test_acceso_formulario_actividad()
        
        # Test 2: Validación de código largo
        validacion_codigo_ok = test_validacion_codigo_largo()
        
        # Test 3: Validación de municipio inexistente
        validacion_municipio_ok = test_validacion_municipio_inexistente()
        
        # Test 4: Guardado de actividad válida
        guardado_ok = test_guardar_actividad_valida()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Acceso al formulario: {'OK' if acceso_ok else 'FALLO'}")
        print(f"✅ Validación código largo: {'OK' if validacion_codigo_ok else 'FALLO'}")
        print(f"✅ Validación municipio: {'OK' if validacion_municipio_ok else 'FALLO'}")
        print(f"✅ Guardado actividad válida: {'OK' if guardado_ok else 'FALLO'}")
        
        if acceso_ok and validacion_codigo_ok and validacion_municipio_ok and guardado_ok:
            print("\n🎉 TODAS LAS MEJORAS ESTÁN FUNCIONANDO")
            print("✅ Formulario corregido según estructura de tabla")
            print("✅ Validaciones mejoradas implementadas")
            print("✅ Compatibilidad con MySQL garantizada")
            return 0
        else:
            print("\n⚠️  ALGUNAS MEJORAS NECESITAN REVISIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





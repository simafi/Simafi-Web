#!/usr/bin/env python
"""
Test para verificar la búsqueda automática de actividades
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_endpoint_buscar_actividad():
    """Test del endpoint AJAX para buscar actividades"""
    print("🔍 TEST DE ENDPOINT BUSCAR ACTIVIDAD")
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
        
        # Test 1: Buscar actividad existente
        print("   📋 Probando búsqueda de actividad existente...")
        response = client.get('/tributario-app/ajax/buscar-actividad/?empresa=0301&codigo=001')
        
        if response.status_code == 200:
            data = response.json()
            print(f"   📄 Respuesta: {data}")
            
            if 'descripcion' in data and 'existe' in data:
                print("   ✅ Endpoint devuelve estructura correcta")
                return True
            else:
                print("   ❌ Endpoint no devuelve estructura esperada")
                return False
        else:
            print(f"   ❌ Error en endpoint: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de endpoint: {str(e)}")
        return False

def test_endpoint_cargar_actividades():
    """Test del endpoint AJAX para cargar actividades"""
    print("\n🔍 TEST DE ENDPOINT CARGAR ACTIVIDADES")
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
        
        # Test: Cargar actividades por empresa
        print("   📋 Probando carga de actividades por empresa...")
        response = client.get('/tributario-app/ajax/cargar-actividades/?empresa=0301')
        
        if response.status_code == 200:
            data = response.json()
            print(f"   📄 Respuesta: {data}")
            
            if 'actividades' in data:
                print("   ✅ Endpoint devuelve actividades")
                print(f"   📊 Número de actividades: {len(data['actividades'])}")
                return True
            else:
                print("   ❌ Endpoint no devuelve actividades")
                return False
        else:
            print(f"   ❌ Error en endpoint: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de cargar actividades: {str(e)}")
        return False

def test_endpoint_buscar_concepto():
    """Test del endpoint AJAX para buscar conceptos de cobro"""
    print("\n🔍 TEST DE ENDPOINT BUSCAR CONCEPTO")
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
        
        # Test: Buscar concepto de cobro
        print("   📋 Probando búsqueda de concepto de cobro...")
        response = client.post('/tributario-app/ajax/buscar-concepto-miscelaneos/', {
            'empresa': '0301',
            'cod_tarifa': '001'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   📄 Respuesta: {data}")
            
            if 'exito' in data:
                print("   ✅ Endpoint devuelve estructura correcta")
                return True
            else:
                print("   ❌ Endpoint no devuelve estructura esperada")
                return False
        else:
            print(f"   ❌ Error en endpoint: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de buscar concepto: {str(e)}")
        return False

def test_formulario_miscelaneos():
    """Test del formulario de misceláneos con búsqueda automática"""
    print("\n🔍 TEST DE FORMULARIO MISCELÁNEOS")
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
        
        # Acceder al formulario de misceláneos
        response = client.get('/tributario-app/miscelaneos/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de misceláneos accesible")
            
            content = response.content.decode()
            
            # Verificar que el campo empresa esté presente
            if 'id="empresa"' in content:
                print("   ✅ Campo empresa encontrado")
                
                if 'value="0301"' in content:
                    print("   ✅ Campo empresa hereda el código correcto")
                else:
                    print("   ❌ Campo empresa no hereda el código correcto")
                    return False
            else:
                print("   ❌ Campo empresa no encontrado")
                return False
            
            # Verificar que las funciones JavaScript estén presentes
            if 'cargarActividadesPorEmpresa' in content:
                print("   ✅ Función cargarActividadesPorEmpresa encontrada")
            else:
                print("   ❌ Función cargarActividadesPorEmpresa no encontrada")
                return False
            
            if 'buscarConcepto' in content:
                print("   ✅ Función buscarConcepto encontrada")
            else:
                print("   ❌ Función buscarConcepto no encontrada")
                return False
            
            if 'autocompletarDescripcion' in content:
                print("   ✅ Función autocompletarDescripcion encontrada")
            else:
                print("   ❌ Función autocompletarDescripcion no encontrada")
                return False
            
            return True
        else:
            print(f"   ❌ Error accediendo a misceláneos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de formulario: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE BÚSQUEDA AUTOMÁTICA DE ACTIVIDADES")
    print("Verificando endpoints AJAX y funcionalidad JavaScript")
    print("=" * 70)
    
    try:
        # Test 1: Endpoint buscar actividad
        buscar_ok = test_endpoint_buscar_actividad()
        
        # Test 2: Endpoint cargar actividades
        cargar_ok = test_endpoint_cargar_actividades()
        
        # Test 3: Endpoint buscar concepto
        concepto_ok = test_endpoint_buscar_concepto()
        
        # Test 4: Formulario misceláneos
        formulario_ok = test_formulario_miscelaneos()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Endpoint buscar actividad: {'OK' if buscar_ok else 'FALLO'}")
        print(f"✅ Endpoint cargar actividades: {'OK' if cargar_ok else 'FALLO'}")
        print(f"✅ Endpoint buscar concepto: {'OK' if concepto_ok else 'FALLO'}")
        print(f"✅ Formulario misceláneos: {'OK' if formulario_ok else 'FALLO'}")
        
        if buscar_ok and cargar_ok and concepto_ok and formulario_ok:
            print("\n🎉 BÚSQUEDA AUTOMÁTICA DE ACTIVIDADES FUNCIONANDO CORRECTAMENTE")
            print("✅ Todos los endpoints AJAX funcionan correctamente")
            print("✅ Las funciones JavaScript están implementadas")
            print("✅ El formulario hereda el código de empresa correctamente")
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





#!/usr/bin/env python
"""
Test para verificar la funcionalidad de búsqueda automática del DNI y conceptos de cobro en misceláneos
"""

import os
import sys
import django
from django.test import Client
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_acceso_miscelaneos():
    """Test de acceso al formulario de misceláneos"""
    print("🔍 TEST DE ACCESO A MISCELÁNEOS")
    print("=" * 50)
    
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
            
            # Verificar elementos del formulario
            elementos_esperados = [
                'id="dni"',
                'id="id_nombre"',
                'buscarContribuyente()',
                'Conceptos de Cobro',
                'conceptos-body'
            ]
            
            elementos_encontrados = []
            for elemento in elementos_esperados:
                if elemento in content:
                    elementos_encontrados.append(elemento)
                    print(f"   ✅ Encontrado: {elemento}")
                else:
                    print(f"   ❌ No encontrado: {elemento}")
            
            return len(elementos_encontrados) >= 4
        else:
            print(f"   ❌ Error accediendo a misceláneos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de acceso: {str(e)}")
        return False

def test_busqueda_identificacion():
    """Test de búsqueda de identificación por DNI"""
    print("\n🔍 TEST DE BÚSQUEDA DE IDENTIFICACIÓN")
    print("=" * 50)
    
    try:
        # URL de la vista de búsqueda
        url = 'http://127.0.0.1:8080/tributario-app/ajax/buscar-identificacion/'
        
        # DNI de prueba
        dni_prueba = '0318-1970-01003'
        
        print(f"   📋 Probando búsqueda con DNI: {dni_prueba}")
        
        try:
            response = requests.get(f"{url}?identidad={dni_prueba}", timeout=10)
            
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   📄 Respuesta: {json.dumps(result, indent=2)}")
                
                if result.get('encontrado'):
                    print("   ✅ Búsqueda exitosa")
                    print(f"   📝 Nombres: {result.get('nombres', 'N/A')}")
                    print(f"   📝 Apellidos: {result.get('apellidos', 'N/A')}")
                    return True
                else:
                    print("   ⚠️  Contribuyente no encontrado")
                    return False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Error de conexión: Servidor no disponible")
            return False
        except Exception as e:
            print(f"   ❌ Error inesperado: {str(e)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de identificación: {str(e)}")
        return False

def test_busqueda_conceptos():
    """Test de búsqueda de conceptos de cobro"""
    print("\n🔍 TEST DE BÚSQUEDA DE CONCEPTOS DE COBRO")
    print("=" * 50)
    
    try:
        # Verificar si hay funcionalidad de búsqueda de conceptos
        print("   📋 Verificando funcionalidad de búsqueda de conceptos...")
        
        # URL de búsqueda de tarifas
        url = 'http://127.0.0.1:8080/tributario-app/ajax/buscar-tarifa/'
        
        # Datos de prueba
        data = {
            'municipio_codigo': '0301',
            'cod_tarifa': '001'
        }
        
        print(f"   📋 Probando búsqueda con: {data}")
        
        try:
            response = requests.post(url, data=data, timeout=10)
            
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   📄 Respuesta: {json.dumps(result, indent=2)}")
                
                if result.get('exito'):
                    print("   ✅ Búsqueda de concepto exitosa")
                    print(f"   📝 Descripción: {result.get('tarifa', {}).get('descripcion', 'N/A')}")
                    print(f"   💰 Valor: {result.get('tarifa', {}).get('valor', 'N/A')}")
                    return True
                else:
                    print(f"   ⚠️  Concepto no encontrado: {result.get('mensaje', 'N/A')}")
                    return False
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Error de conexión: Servidor no disponible")
            return False
        except Exception as e:
            print(f"   ❌ Error inesperado: {str(e)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de conceptos: {str(e)}")
        return False

def test_comparacion_con_maestro_negocios():
    """Test de comparación con maestro_negocios"""
    print("\n🔍 COMPARACIÓN CON MAESTRO DE NEGOCIOS")
    print("=" * 50)
    
    try:
        # Verificar funcionalidades en maestro_negocios
        print("   📋 Verificando funcionalidades en maestro_negocios...")
        
        # URL de búsqueda de identificación en maestro_negocios
        url = 'http://127.0.0.1:8080/tributario-app/ajax/buscar-identificacion/'
        
        # DNI de prueba
        dni_prueba = '0318-1970-01003'
        
        try:
            response = requests.get(f"{url}?identidad={dni_prueba}", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('encontrado'):
                    print("   ✅ Búsqueda de identificación funciona en maestro_negocios")
                    
                    # Verificar si hay funcionalidad de búsqueda automática
                    print("   📋 Verificando búsqueda automática...")
                    
                    # Simular búsqueda automática
                    url_negocio = 'http://127.0.0.1:8080/tributario-app/ajax/buscar-negocio/'
                    params = {
                        'empresa': '0301',
                        'rtm': 'TEST001',
                        'expe': '001'
                    }
                    
                    response_negocio = requests.get(url_negocio, params=params, timeout=10)
                    
                    if response_negocio.status_code == 200:
                        print("   ✅ Búsqueda automática de negocio funciona")
                        return True
                    else:
                        print("   ⚠️  Búsqueda automática de negocio no disponible")
                        return False
                else:
                    print("   ⚠️  Búsqueda de identificación no funciona en maestro_negocios")
                    return False
            else:
                print(f"   ❌ Error HTTP en maestro_negocios: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Error de conexión: Servidor no disponible")
            return False
        except Exception as e:
            print(f"   ❌ Error inesperado: {str(e)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en comparación: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE FUNCIONALIDAD MISCELÁNEOS")
    print("Verificando búsqueda automática del DNI y conceptos de cobro")
    print("=" * 60)
    
    try:
        # Test 1: Acceso a misceláneos
        acceso_ok = test_acceso_miscelaneos()
        
        # Test 2: Búsqueda de identificación
        identificacion_ok = test_busqueda_identificacion()
        
        # Test 3: Búsqueda de conceptos
        conceptos_ok = test_busqueda_conceptos()
        
        # Test 4: Comparación con maestro_negocios
        comparacion_ok = test_comparacion_con_maestro_negocios()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        print(f"✅ Acceso a misceláneos: {'OK' if acceso_ok else 'FALLO'}")
        print(f"✅ Búsqueda de identificación: {'OK' if identificacion_ok else 'FALLO'}")
        print(f"✅ Búsqueda de conceptos: {'OK' if conceptos_ok else 'FALLO'}")
        print(f"✅ Comparación con maestro_negocios: {'OK' if comparacion_ok else 'FALLO'}")
        
        if acceso_ok and identificacion_ok and conceptos_ok and comparacion_ok:
            print("\n🎉 TODAS LAS FUNCIONALIDADES ESTÁN FUNCIONANDO")
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





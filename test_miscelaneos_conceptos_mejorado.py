#!/usr/bin/env python
"""
Test para verificar la funcionalidad mejorada de búsqueda automática de conceptos en misceláneos
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

def test_busqueda_concepto_miscelaneos():
    """Test de búsqueda de conceptos en misceláneos"""
    print("🔍 TEST DE BÚSQUEDA DE CONCEPTOS EN MISCELÁNEOS")
    print("=" * 60)
    
    try:
        # URL de la nueva función de búsqueda
        url = 'http://127.0.0.1:8080/tributario-app/ajax/buscar-concepto-miscelaneos/'
        
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
                    concepto = result.get('concepto', {})
                    print(f"   📝 Código: {concepto.get('cod_tarifa', 'N/A')}")
                    print(f"   📝 Descripción: {concepto.get('descripcion', 'N/A')}")
                    print(f"   💰 Valor: {concepto.get('valor', 'N/A')}")
                    print(f"   📅 Año: {concepto.get('ano', 'N/A')}")
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

def test_acceso_miscelaneos_mejorado():
    """Test de acceso al formulario de misceláneos mejorado"""
    print("\n🔍 TEST DE ACCESO A MISCELÁNEOS MEJORADO")
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
            
            # Verificar elementos del formulario mejorado
            elementos_esperados = [
                'id="dni"',
                'id="id_nombre"',
                'buscarContribuyente()',
                'buscarConcepto(',
                'cargarTarifasPorEmpresa(',
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
            
            return len(elementos_encontrados) >= 5
        else:
            print(f"   ❌ Error accediendo a misceláneos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de acceso: {str(e)}")
        return False

def test_busqueda_identificacion_mejorada():
    """Test de búsqueda de identificación mejorada"""
    print("\n🔍 TEST DE BÚSQUEDA DE IDENTIFICACIÓN MEJORADA")
    print("=" * 60)
    
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
                    print("   ✅ Búsqueda de identificación exitosa")
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

def test_carga_tarifas():
    """Test de carga de tarifas para los selects"""
    print("\n🔍 TEST DE CARGA DE TARIFAS")
    print("=" * 60)
    
    try:
        # URL de carga de tarifas
        url = 'http://127.0.0.1:8080/tributario-app/ajax/obtener-tarifas-rubro/'
        
        # Parámetros
        params = {
            'municipio_codigo': '0301'
        }
        
        print(f"   📋 Probando carga de tarifas con: {params}")
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   📄 Respuesta: {json.dumps(result, indent=2)}")
                
                if result.get('exito') and result.get('tarifas'):
                    print("   ✅ Carga de tarifas exitosa")
                    tarifas = result.get('tarifas', [])
                    print(f"   📊 Total de tarifas: {len(tarifas)}")
                    
                    if tarifas:
                        primera_tarifa = tarifas[0]
                        print(f"   📝 Primera tarifa: {primera_tarifa.get('cod_tarifa', 'N/A')} - {primera_tarifa.get('descripcion', 'N/A')}")
                    
                    return True
                else:
                    print(f"   ⚠️  No se encontraron tarifas: {result.get('mensaje', 'N/A')}")
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
        print(f"   ❌ Error en test de tarifas: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE FUNCIONALIDAD MISCELÁNEOS MEJORADA")
    print("Verificando búsqueda automática del DNI y conceptos de cobro mejorada")
    print("=" * 70)
    
    try:
        # Test 1: Acceso a misceláneos mejorado
        acceso_ok = test_acceso_miscelaneos_mejorado()
        
        # Test 2: Búsqueda de identificación mejorada
        identificacion_ok = test_busqueda_identificacion_mejorada()
        
        # Test 3: Búsqueda de conceptos
        conceptos_ok = test_busqueda_concepto_miscelaneos()
        
        # Test 4: Carga de tarifas
        tarifas_ok = test_carga_tarifas()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Acceso a misceláneos mejorado: {'OK' if acceso_ok else 'FALLO'}")
        print(f"✅ Búsqueda de identificación mejorada: {'OK' if identificacion_ok else 'FALLO'}")
        print(f"✅ Búsqueda de conceptos: {'OK' if conceptos_ok else 'FALLO'}")
        print(f"✅ Carga de tarifas: {'OK' if tarifas_ok else 'FALLO'}")
        
        if acceso_ok and identificacion_ok and conceptos_ok and tarifas_ok:
            print("\n🎉 TODAS LAS FUNCIONALIDADES MEJORADAS ESTÁN FUNCIONANDO")
            print("✅ Búsqueda automática del DNI: Implementada y funcionando")
            print("✅ Búsqueda automática de conceptos: Implementada y funcionando")
            print("✅ Carga automática de tarifas: Implementada y funcionando")
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





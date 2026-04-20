#!/usr/bin/env python
"""
Test para verificar la búsqueda automática de oficinas
"""

import os
import sys
import django
from django.test import Client
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_endpoint_buscar_oficina():
    """Test del endpoint AJAX para buscar oficinas"""
    print("🔍 TEST DE ENDPOINT BUSCAR OFICINA")
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
        
        # Test 1: Buscar oficina existente
        print("   📋 Probando búsqueda de oficina existente...")
        response = client.get('/tributario-app/ajax/buscar-oficina/?empresa=0301&codigo=001')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Respuesta: {data}")
                
                if 'descripcion' in data and 'existe' in data:
                    print("   ✅ Endpoint devuelve estructura correcta")
                    return True
                else:
                    print("   ❌ Endpoint no devuelve estructura esperada")
                    return False
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                print(f"   📄 Contenido: {response.content.decode()[:200]}")
                return False
        else:
            print(f"   ❌ Error en endpoint: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de endpoint: {str(e)}")
        return False

def test_formulario_oficina_busqueda():
    """Test del formulario de oficina con búsqueda automática"""
    print("\n🔍 TEST DE FORMULARIO OFICINA CON BÚSQUEDA")
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
                
                if 'value="0301"' in content:
                    print("   ✅ Campo empresa hereda correctamente el código 0301")
                else:
                    print("   ❌ Campo empresa no hereda el código correcto")
                    return False
            else:
                print("   ❌ Campo empresa no encontrado en el formulario")
                return False
            
            # Verificar que las funciones JavaScript estén presentes
            if 'buscarDescripcion' in content:
                print("   ✅ Función buscarDescripcion encontrada")
            else:
                print("   ❌ Función buscarDescripcion no encontrada")
                return False
            
            # Verificar que use la URL correcta
            if '/tributario-app/ajax/buscar-oficina/' in content:
                print("   ✅ URL correcta para búsqueda de oficinas")
            else:
                print("   ❌ URL incorrecta para búsqueda de oficinas")
                return False
            
            # Verificar que use data.existe
            if 'data.existe' in content:
                print("   ✅ JavaScript usa data.existe correctamente")
            else:
                print("   ❌ JavaScript no usa data.existe")
                return False
            
            return True
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de formulario: {str(e)}")
        return False

def test_buscar_oficina_inexistente():
    """Test de búsqueda de oficina inexistente"""
    print("\n🔍 TEST DE BÚSQUEDA DE OFICINA INEXISTENTE")
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
        
        # Buscar una oficina que sabemos que NO existe
        print("   📋 Buscando oficina 'CODIGO_INEXISTENTE'...")
        response = client.get('/tributario-app/ajax/buscar-oficina/?empresa=0301&codigo=CODIGO_INEXISTENTE')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Datos recibidos: {data}")
                
                # Verificar estructura de respuesta
                if 'descripcion' in data and 'existe' in data:
                    print("   ✅ Estructura de respuesta correcta")
                    
                    if not data['existe'] and not data['descripcion']:
                        print("   ✅ Oficina no encontrada (correcto)")
                        return True
                    else:
                        print("   ❌ Oficina encontrada cuando no debería existir")
                        return False
                else:
                    print("   ❌ Estructura de respuesta incorrecta")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON: {e}")
                return False
        else:
            print(f"   ❌ Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

def test_verificar_conflictos_variables():
    """Test para verificar que no haya conflictos de variables"""
    print("\n🔍 TEST DE VERIFICACIÓN DE CONFLICTOS DE VARIABLES")
    print("=" * 60)
    
    try:
        # Leer el template de oficina
        with open('tributario_app/templates/oficina.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que use data.existe
        if 'data.existe' in content:
            print("   ✅ Template usa data.existe correctamente")
        else:
            print("   ❌ Template no usa data.existe")
            return False
        
        # Verificar que NO use data.exito para oficinas
        if 'data.exito' in content and 'buscar-oficina' in content:
            print("   ❌ Template aún usa data.exito para buscar-oficina")
            return False
        else:
            print("   ✅ Template no usa data.exito para buscar-oficina")
        
        # Verificar que use la URL correcta
        if '/tributario-app/ajax/buscar-oficina/' in content:
            print("   ✅ Template usa URL correcta")
        else:
            print("   ❌ Template no usa URL correcta")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error leyendo template: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE BÚSQUEDA AUTOMÁTICA DE OFICINAS")
    print("Verificando que funcione correctamente y sin conflictos de variables")
    print("=" * 70)
    
    try:
        # Test 1: Endpoint buscar oficina
        endpoint_ok = test_endpoint_buscar_oficina()
        
        # Test 2: Formulario con búsqueda
        formulario_ok = test_formulario_oficina_busqueda()
        
        # Test 3: Búsqueda de oficina inexistente
        inexistente_ok = test_buscar_oficina_inexistente()
        
        # Test 4: Verificación de conflictos
        conflictos_ok = test_verificar_conflictos_variables()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Endpoint buscar oficina: {'OK' if endpoint_ok else 'FALLO'}")
        print(f"✅ Formulario con búsqueda: {'OK' if formulario_ok else 'FALLO'}")
        print(f"✅ Búsqueda oficina inexistente: {'OK' if inexistente_ok else 'FALLO'}")
        print(f"✅ Verificación de conflictos: {'OK' if conflictos_ok else 'FALLO'}")
        
        if endpoint_ok and formulario_ok and inexistente_ok and conflictos_ok:
            print("\n🎉 BÚSQUEDA AUTOMÁTICA DE OFICINAS FUNCIONANDO CORRECTAMENTE")
            print("✅ El endpoint devuelve JSON válido")
            print("✅ El formulario hereda el código de empresa correctamente")
            print("✅ La búsqueda automática funciona al ingresar códigos")
            print("✅ No hay conflictos de variables empresa vs municipio_codigo")
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





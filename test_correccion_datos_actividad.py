#!/usr/bin/env python
"""
Test para verificar la corrección del manejo de datos en búsqueda de actividades
"""

import os
import sys
import django
from django.test import Client
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_buscar_actividad_existente():
    """Test de búsqueda de actividad existente"""
    print("🔍 TEST DE BÚSQUEDA DE ACTIVIDAD EXISTENTE")
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
        
        # Buscar una actividad que sabemos que existe
        print("   📋 Buscando actividad '11.7.1.02.11.03' (TIENDA DE CONVENIENCIA)...")
        response = client.get('/tributario-app/ajax/buscar-actividad/?empresa=0301&codigo=11.7.1.02.11.03')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Datos recibidos: {data}")
                
                # Verificar estructura de respuesta
                if 'descripcion' in data and 'existe' in data:
                    print("   ✅ Estructura de respuesta correcta")
                    
                    if data['existe'] and data['descripcion']:
                        print(f"   ✅ Actividad encontrada: {data['descripcion']}")
                        return True
                    else:
                        print("   ❌ Actividad no encontrada cuando debería existir")
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

def test_buscar_actividad_inexistente():
    """Test de búsqueda de actividad inexistente"""
    print("\n🔍 TEST DE BÚSQUEDA DE ACTIVIDAD INEXISTENTE")
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
        
        # Buscar una actividad que sabemos que NO existe
        print("   📋 Buscando actividad 'CODIGO_INEXISTENTE'...")
        response = client.get('/tributario-app/ajax/buscar-actividad/?empresa=0301&codigo=CODIGO_INEXISTENTE')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Datos recibidos: {data}")
                
                # Verificar estructura de respuesta
                if 'descripcion' in data and 'existe' in data:
                    print("   ✅ Estructura de respuesta correcta")
                    
                    if not data['existe'] and not data['descripcion']:
                        print("   ✅ Actividad no encontrada (correcto)")
                        return True
                    else:
                        print("   ❌ Actividad encontrada cuando no debería existir")
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

def test_verificar_template_actividad():
    """Test para verificar que el template use data.existe"""
    print("\n🔍 TEST DE VERIFICACIÓN DE TEMPLATE")
    print("=" * 60)
    
    try:
        # Leer el template de actividad
        with open('tributario_app/templates/actividad.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que use data.existe
        if 'data.existe' in content:
            print("   ✅ Template usa data.existe correctamente")
        else:
            print("   ❌ Template no usa data.existe")
            return False
        
        # Verificar que NO use data.exito para actividades
        if 'data.exito' in content and 'buscar-actividad' in content:
            print("   ❌ Template aún usa data.exito para buscar-actividad")
            return False
        else:
            print("   ✅ Template no usa data.exito para buscar-actividad")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error leyendo template: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST DE CORRECCIÓN DE DATOS EN BÚSQUEDA DE ACTIVIDADES")
    print("Verificando que se use data.existe en lugar de data.exito")
    print("=" * 70)
    
    try:
        # Test 1: Búsqueda de actividad existente
        existente_ok = test_buscar_actividad_existente()
        
        # Test 2: Búsqueda de actividad inexistente
        inexistente_ok = test_buscar_actividad_inexistente()
        
        # Test 3: Verificación de template
        template_ok = test_verificar_template_actividad()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Búsqueda actividad existente: {'OK' if existente_ok else 'FALLO'}")
        print(f"✅ Búsqueda actividad inexistente: {'OK' if inexistente_ok else 'FALLO'}")
        print(f"✅ Template usa data.existe: {'OK' if template_ok else 'FALLO'}")
        
        if existente_ok and inexistente_ok and template_ok:
            print("\n🎉 CORRECCIÓN DE DATOS EXITOSA")
            print("✅ El template ahora usa data.existe correctamente")
            print("✅ Las actividades existentes se encuentran correctamente")
            print("✅ Las actividades inexistentes se manejan correctamente")
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





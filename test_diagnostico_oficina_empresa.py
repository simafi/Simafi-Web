#!/usr/bin/env python
"""
Test para diagnosticar el problema de herencia de empresa en oficina
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_diagnostico_sesion_oficina():
    """Test para diagnosticar la sesión en oficina"""
    print("🔍 DIAGNÓSTICO DE SESIÓN EN OFICINA")
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
        
        # Verificar la sesión después del login
        session = client.session
        print(f"   📄 Contenido de la sesión: {dict(session)}")
        
        if 'empresa' in session:
            print(f"   ✅ Sesión contiene 'empresa': {session['empresa']}")
        else:
            print("   ❌ Sesión no contiene 'empresa'")
            return False
        
        # Acceder al formulario de oficina
        response = client.get('/tributario-app/oficina/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de oficina accesible")
            
            content = response.content.decode()
            
            # Buscar el campo empresa en el HTML
            if 'id="id_empresa"' in content:
                print("   ✅ Campo empresa encontrado en el formulario")
                
                # Extraer el valor del campo
                import re
                match = re.search(r'value="([^"]*)"', content[content.find('id_empresa'):content.find('id_empresa')+200])
                if match:
                    valor_campo = match.group(1)
                    print(f"   📄 Valor del campo empresa: '{valor_campo}'")
                    
                    if valor_campo == '0301':
                        print("   ✅ Campo empresa tiene el valor correcto")
                        return True
                    else:
                        print("   ❌ Campo empresa no tiene el valor correcto")
                        return False
                else:
                    print("   ❌ No se pudo extraer el valor del campo")
                    return False
            else:
                print("   ❌ Campo empresa no encontrado en el formulario")
                return False
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en diagnóstico: {str(e)}")
        return False

def test_verificar_contexto_oficina():
    """Test para verificar el contexto pasado al template"""
    print("\n🔍 VERIFICACIÓN DE CONTEXTO DE OFICINA")
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
            
            # Verificar que el contexto contenga municipio_codigo
            if hasattr(response, 'context'):
                context = response.context
                print(f"   📄 Contexto disponible: {list(context.keys()) if context else 'No disponible'}")
                
                if context and 'municipio_codigo' in context:
                    print(f"   ✅ Contexto contiene 'municipio_codigo': {context['municipio_codigo']}")
                    return True
                else:
                    print("   ❌ Contexto no contiene 'municipio_codigo'")
                    return False
            else:
                print("   ⚠️  No se puede acceder al contexto de la respuesta")
                return False
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en verificación: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 DIAGNÓSTICO DE HERENCIA DE EMPRESA EN OFICINA")
    print("Investigando por qué no se hereda correctamente el código de empresa")
    print("=" * 70)
    
    try:
        # Test 1: Diagnóstico de sesión
        sesion_ok = test_diagnostico_sesion_oficina()
        
        # Test 2: Verificación de contexto
        contexto_ok = test_verificar_contexto_oficina()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE DIAGNÓSTICO")
        print("=" * 70)
        
        print(f"✅ Diagnóstico de sesión: {'OK' if sesion_ok else 'FALLO'}")
        print(f"✅ Verificación de contexto: {'OK' if contexto_ok else 'FALLO'}")
        
        if sesion_ok and contexto_ok:
            print("\n🎉 HERENCIA DE EMPRESA FUNCIONANDO CORRECTAMENTE")
            return 0
        else:
            print("\n⚠️  SE DETECTARON PROBLEMAS EN LA HERENCIA")
            print("Revisar la función oficina_crud y el template")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





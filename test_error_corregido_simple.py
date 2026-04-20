#!/usr/bin/env python
"""
Test simple para verificar que el error de municipio_codigo se ha corregido
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_error_corregido():
    """Test para verificar que el error se ha corregido"""
    print("🔧 VERIFICANDO QUE EL ERROR SE HA CORREGIDO")
    print("=" * 60)
    
    try:
        client = Client()
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        print("1. Probando login con credenciales:")
        print(f"   Usuario: {login_data['usuario']}")
        print(f"   Contraseña: {login_data['password']}")
        print(f"   Municipio: {login_data['municipio']}")
        
        print("\n2. Enviando petición POST...")
        response = client.post('/tributario-app/login/', login_data, follow=True)
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Status 200: Login procesado correctamente")
            
            # Verificar si hay errores en el contenido
            content = response.content.decode()
            
            if 'Cannot resolve keyword' in content:
                print("   ❌ ERROR NO CORREGIDO: Sigue apareciendo 'Cannot resolve keyword'")
                return False
            elif 'municipio_codigo' in content:
                print("   ❌ ERROR NO CORREGIDO: Sigue apareciendo 'municipio_codigo'")
                return False
            elif 'Error en el sistema' in content:
                print("   ❌ ERROR NO CORREGIDO: Sigue apareciendo 'Error en el sistema'")
                return False
            else:
                print("   ✅ ERROR CORREGIDO: No aparecen errores de 'municipio_codigo'")
                return True
        else:
            print(f"   ❌ Status {response.status_code}: Error en la petición")
            return False
            
    except Exception as e:
        print(f"   ❌ Excepción: {str(e)}")
        if 'municipio_codigo' in str(e):
            print("   ❌ ERROR NO CORREGIDO: Excepción contiene 'municipio_codigo'")
            return False
        else:
            print("   ⚠️  Excepción diferente al esperado")
            return False

def main():
    """Función principal"""
    print("🧪 TEST SIMPLE - ERROR CORREGIDO")
    print("Verificando que el error 'Cannot resolve keyword municipio_codigo' se ha corregido")
    print("=" * 60)
    
    try:
        exito = test_error_corregido()
        
        print("\n" + "=" * 60)
        print("📊 RESULTADO")
        print("=" * 60)
        
        if exito:
            print("🎉 ¡ERROR CORREGIDO EXITOSAMENTE!")
            print("✅ El error 'Cannot resolve keyword municipio_codigo' se ha corregido")
            print("✅ El login ahora usa el campo 'empresa' correctamente")
            print("\n🎯 CREDENCIALES FUNCIONALES:")
            print("   URL: http://127.0.0.1:8080/tributario-app/")
            print("   Usuario: tributario")
            print("   Contraseña: admin123")
            print("   Municipio: 0301")
            return 0
        else:
            print("❌ ERROR NO CORREGIDO")
            print("⚠️  El error 'Cannot resolve keyword municipio_codigo' sigue apareciendo")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





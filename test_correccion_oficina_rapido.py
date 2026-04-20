#!/usr/bin/env python
"""
Test rápido para verificar la corrección del error de oficina
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_guardar_oficina_corregido():
    """Test de guardado de oficina con la corrección aplicada"""
    print("🔍 TEST DE GUARDADO DE OFICINA CORREGIDO")
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
        
        # Guardar oficina
        oficina_data = {
            'accion': 'guardar',
            'empresa': '0301',
            'codigo': 'TEST_CORRECCION',
            'descripcion': 'Oficina de prueba para verificar corrección'
        }
        
        print("   📋 Guardando oficina...")
        response = client.post('/tributario-app/oficina/', oficina_data)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'creada correctamente' in content or 'actualizada correctamente' in content:
                print("   ✅ Oficina guardada correctamente")
                return True
            elif 'Cannot resolve keyword' in content:
                print("   ❌ Error de campo aún presente")
                print(f"   📄 Contenido: {content[:300]}...")
                return False
            else:
                print("   ⚠️  Respuesta inesperada")
                print(f"   📄 Contenido: {content[:300]}...")
                return False
        else:
            print(f"   ❌ Error en petición: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST RÁPIDO DE CORRECCIÓN DE OFICINA")
    print("Verificando que el error de municipio_codigo esté corregido")
    print("=" * 70)
    
    try:
        # Test de guardado
        guardado_ok = test_guardar_oficina_corregido()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Guardado de oficina: {'OK' if guardado_ok else 'FALLO'}")
        
        if guardado_ok:
            print("\n🎉 CORRECCIÓN EXITOSA")
            print("✅ El error de municipio_codigo ha sido corregido")
            print("✅ Las oficinas se pueden guardar correctamente")
            return 0
        else:
            print("\n⚠️  LA CORRECCIÓN NECESITA REVISIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





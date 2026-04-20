#!/usr/bin/env python
"""
Test simple para verificar el template
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_template_simple():
    """Test simple del template"""
    print("🔍 TEST SIMPLE DE TEMPLATE")
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
        
        # Acceder al formulario
        response = client.get('/tributario-app/rubros/', follow=True)
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Buscar campos específicos
            campos_buscar = [
                'id="id_empresa"',
                'id="id_codigo"',
                'id="id_descripcion"',
                'id="id_cuenta"',
                'id="id_cuentarez"',
                'id="id_tipo"',
                'name="empresa"',
                'name="codigo"',
                'name="descripcion"',
                'name="cuenta"',
                'name="cuentarez"',
                'name="tipo"'
            ]
            
            for campo in campos_buscar:
                if campo in content:
                    print(f"   ✅ Campo encontrado: {campo}")
                else:
                    print(f"   ❌ Campo faltante: {campo}")
            
            # Mostrar una parte del contenido para debug
            print(f"   📄 Contenido (primeros 500 chars): {content[:500]}...")
            
            return True
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_template_simple()





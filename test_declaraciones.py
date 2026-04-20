#!/usr/bin/env python
"""
Script para probar la vista de declaraciones
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.tributario_app.settings')
sys.path.insert(0, r'C:\simafiweb\venv\Scripts')
sys.path.insert(0, r'C:\simafiweb\modules')

# Cambiar al directorio correcto
os.chdir(r'C:\simafiweb\venv\Scripts')

django.setup()

from django.test import RequestFactory
from modules.tributario.simple_views import declaracion_volumen

def test_declaracion_volumen():
    """Probar la vista declaracion_volumen"""
    print("🧪 Probando vista declaracion_volumen...")
    
    # Crear request factory
    factory = RequestFactory()
    
    # Crear request GET
    request = factory.get('/tributario/declaraciones/')
    
    try:
        # Llamar a la vista
        response = declaracion_volumen(request)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Content Type: {response.get('Content-Type', 'No definido')}")
        
        # Verificar si es HTML o JSON
        content = response.content.decode('utf-8')
        if 'text/html' in str(response.get('Content-Type', '')):
            print("✅ Respuesta es HTML - Vista corregida correctamente")
            print(f"✅ Contenido HTML (primeros 200 caracteres): {content[:200]}...")
        elif 'application/json' in str(response.get('Content-Type', '')):
            print("❌ Respuesta es JSON - Vista aún devuelve JSON")
            print(f"❌ Contenido JSON: {content}")
        else:
            print(f"⚠️ Tipo de contenido inesperado: {response.get('Content-Type', '')}")
            print(f"Contenido: {content[:200]}...")
            
    except Exception as e:
        print(f"❌ Error al probar la vista: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_declaracion_volumen()

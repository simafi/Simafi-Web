#!/usr/bin/env python
"""
Script para probar el servidor Django directamente
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')

try:
    django.setup()
    print("✅ Django configurado correctamente")
    
    # Probar la vista directamente
    from django.test import RequestFactory
    from simple_views import declaracion_volumen
    
    # Crear una petición GET simulada
    factory = RequestFactory()
    request = factory.get('/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151')
    
    print("🔍 Probando vista declaracion_volumen...")
    response = declaracion_volumen(request)
    
    print(f"✅ Respuesta generada: {response.status_code}")
    print(f"✅ Tipo de respuesta: {type(response)}")
    
    # Verificar si el HTML contiene el campo valor_base
    if hasattr(response, 'content'):
        content = response.content.decode('utf-8')
        if 'id_valor_base' in content:
            print("✅ Campo id_valor_base encontrado en el HTML")
        else:
            print("❌ Campo id_valor_base NO encontrado en el HTML")
            
        if 'Valor Base' in content:
            print("✅ Texto 'Valor Base' encontrado en el HTML")
        else:
            print("❌ Texto 'Valor Base' NO encontrado en el HTML")
    
    print("\n🎉 Prueba de la vista exitosa!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()































#!/usr/bin/env python
"""
Script para probar la vista directamente
"""

import os
import sys
import django
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from tributario.views import declaracion_volumen

def test_vista_directa():
    print("="*80)
    print("PROBANDO VISTA DIRECTAMENTE")
    print("="*80)
    
    try:
        # Crear una petición GET simulada
        factory = RequestFactory()
        request = factory.get('/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151')
        
        # Agregar sesión
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request.session['empresa'] = '0301'
        
        # Llamar a la vista
        response = declaracion_volumen(request)
        
        print(f"1. Respuesta de la vista:")
        print(f"   - Status code: {response.status_code}")
        print(f"   - Content type: {response.get('Content-Type', 'No especificado')}")
        
        if response.status_code == 200:
            html_content = response.content.decode('utf-8')
            print(f"   - Tamaño del HTML: {len(html_content)} caracteres")
            
            # Buscar el campo valor_base
            import re
            pattern_valor_base = r'name="valor_base"[^>]*value="([^"]*)"'
            match_valor_base = re.search(pattern_valor_base, html_content)
            
            if match_valor_base:
                valor_base_html = match_valor_base.group(1)
                print(f"   - valor_base en HTML: '{valor_base_html}'")
                
                try:
                    valor_base_num = float(valor_base_html.replace(',', '').replace(' ', '').strip())
                    if valor_base_num > 0:
                        print(f"   - ✅ CORRECTO: El valor base se está mostrando correctamente")
                    else:
                        print(f"   - ❌ ERROR: El valor base es 0")
                except ValueError:
                    print(f"   - ❌ ERROR: No se pudo convertir el valor a número")
            else:
                print(f"   - ❌ ERROR: No se encontró el campo valor_base en el HTML")
                
        else:
            print(f"   - ❌ ERROR: La vista devolvió un error")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    test_vista_directa()































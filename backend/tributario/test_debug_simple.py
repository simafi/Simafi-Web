#!/usr/bin/env python
"""
Script simple para probar la detección de AJAX con logging
"""

import requests
import json

def test_debug_simple():
    print("="*80)
    print("PROBANDO DETECCION AJAX CON LOGGING")
    print("="*80)
    
    # URL del endpoint
    url = "http://127.0.0.1:8080/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151"
    
    # Primero obtener el token CSRF
    print("1. Obteniendo token CSRF...")
    try:
        session = requests.Session()
        csrf_response = session.get(url)
        csrf_token = None
        
        # Buscar el token CSRF en el HTML
        import re
        csrf_match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', csrf_response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"   - ✅ Token CSRF obtenido: {csrf_token[:20]}...")
        else:
            print("   - ❌ No se pudo obtener el token CSRF")
            return False
    except Exception as e:
        print(f"   - ❌ Error al obtener token CSRF: {e}")
        return False
    
    # Datos simples
    datos = {
        'accion': 'guardar',
        'form_data': {
            'idneg': '0301',
            'rtm': '114-03-23',
            'expe': '1151',
            'ano': 2024,
            'mes': 12,
            'tipo': 1,
            'ventai': 5000000,
            'ventac': 5000000,
            'ventas': 5000000,
            'valorexcento': 0,
            'controlado': 31000000,
            'unidad': 1,
            'factor': 1.0,
            'multadecla': 0,
            'impuesto': 0,
            'ajuste': 0
        }
    }
    
    # Headers para petición AJAX
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"\n2. Enviando petición AJAX...")
    print(f"   - URL: {url}")
    print(f"   - Headers: {headers}")
    print(f"   - Datos: {json.dumps(datos, indent=2)}")
    
    try:
        # Realizar petición POST usando la misma sesión
        response = session.post(url, json=datos, headers=headers, timeout=10)
        
        print(f"\n3. Respuesta recibida:")
        print(f"   - Status Code: {response.status_code}")
        print(f"   - Content-Type: {response.headers.get('content-type', 'No especificado')}")
        
        # Verificar si es JSON
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            print(f"   - ✅ Respuesta es JSON")
            try:
                json_data = response.json()
                print(f"   - Datos JSON: {json.dumps(json_data, indent=2)}")
                return True
            except json.JSONDecodeError as e:
                print(f"   - ❌ Error al parsear JSON: {e}")
                return False
        else:
            print(f"   - ❌ Respuesta NO es JSON")
            print(f"   - Contenido (primeros 200 chars): {response.text[:200]}...")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"   - ❌ Error en la petición: {e}")
        return False
    except Exception as e:
        print(f"   - ❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_debug_simple()
    print(f"\n{'='*80}")
    print(f"RESULTADO: {'✅ ÉXITO' if success else '❌ FALLO'}")
    print(f"{'='*80}")































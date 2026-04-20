#!/usr/bin/env python3
"""
Test detallado para buscar el mensaje de error específico
"""

import requests
import re

def test_mensaje_error_detallado():
    """Test detallado para buscar el mensaje de error específico"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        # Obtener la página
        response = session.get(url, timeout=10)
        print(f"GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Pagina cargada correctamente")
            
            # Buscar el token CSRF
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            
            if csrf_match:
                csrf_value = csrf_match.group(1)
                print(f"CSRF Token encontrado")
                
                # Test: Enviar formulario con datos de prueba
                form_data = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '1000.00',
                    'ventac': '2000.00',
                    'ventas': '3000.00',
                    'valorexcento': '0.00',
                    'controlado': '0.00',
                    'unidad': '0',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '150.00',
                    'ajuste': '0.00'
                }
                
                print("Enviando formulario...")
                post_response = session.post(url, data=form_data, timeout=10)
                print(f"POST Status: {post_response.status_code}")
                
                if post_response.status_code == 200:
                    print("POST exitoso")
                    
                    # Buscar el mensaje específico en la respuesta
                    if "utiliza un formato que coincida con el solicitado" in post_response.text:
                        print("❌ MENSAJE DE ERROR ENCONTRADO EN LA RESPUESTA")
                    else:
                        print("✅ No se encontró el mensaje de error en la respuesta")
                        
                    # Buscar otros mensajes de error
                    if "formato" in post_response.text:
                        print("⚠️ Se encontró la palabra 'formato' en la respuesta")
                    if "coincida" in post_response.text:
                        print("⚠️ Se encontró la palabra 'coincida' en la respuesta")
                    if "solicitado" in post_response.text:
                        print("⚠️ Se encontró la palabra 'solicitado' en la respuesta")
                        
                else:
                    print(f"Error HTTP: {post_response.status_code}")
                    print(f"Contenido: {post_response.text[:500]}")
                    
            else:
                print("No se encontro token CSRF")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_mensaje_error_detallado()
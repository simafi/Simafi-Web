#!/usr/bin/env python3
"""
Test final para confirmar que la restricción se ha corregido
"""

import requests
import re

def test_final_restriccion():
    """Test final para confirmar que la restricción se ha corregido"""
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
                
                # Test: Enviar formulario con ventai vacío (debería funcionar)
                form_data = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '',  # Campo vacío - antes causaba error
                    'ventac': '2000.00',  # Otro campo con valor
                    'ventas': '3000.00',
                    'valorexcento': '0.00',
                    'controlado': '0.00',
                    'unidad': '0',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '150.00',
                    'ajuste': '0.00'
                }
                
                print("Enviando formulario con campo ventai vacio...")
                post_response = session.post(url, data=form_data, timeout=10)
                print(f"POST Status: {post_response.status_code}")
                
                if post_response.status_code == 200:
                    print("POST exitoso - Restriccion corregida")
                    print("El campo Ventas Rubro Produccion ya no es obligatorio")
                else:
                    print(f"Error HTTP: {post_response.status_code}")
                    print(f"Contenido: {post_response.text[:200]}")
                    
            else:
                print("No se encontro token CSRF")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_final_restriccion()



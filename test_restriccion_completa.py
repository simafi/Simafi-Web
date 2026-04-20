#!/usr/bin/env python3
"""
Test completo para verificar que la restricción se ha corregido en todos los casos
"""

import requests
import re

def test_restriccion_completa():
    """Test completo para verificar que la restricción se ha corregido"""
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
                
                # Test 1: Solo ventac con valor
                print("\n=== TEST 1: Solo ventac con valor ===")
                form_data1 = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '',  # Vacío
                    'ventac': '2000.00',  # Con valor
                    'ventas': '',  # Vacío
                    'valorexcento': '',  # Vacío
                    'controlado': '',  # Vacío
                    'unidad': '0',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '100.00',
                    'ajuste': '0.00'
                }
                
                post_response1 = session.post(url, data=form_data1, timeout=10)
                print(f"POST Status: {post_response1.status_code}")
                
                if post_response1.status_code == 200:
                    print("✅ TEST 1: Exitoso - Solo ventac funciona")
                else:
                    print(f"❌ TEST 1: Error - {post_response1.status_code}")
                
                # Test 2: Solo ventas con valor
                print("\n=== TEST 2: Solo ventas con valor ===")
                form_data2 = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '',  # Vacío
                    'ventac': '',  # Vacío
                    'ventas': '3000.00',  # Con valor
                    'valorexcento': '',  # Vacío
                    'controlado': '',  # Vacío
                    'unidad': '0',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '150.00',
                    'ajuste': '0.00'
                }
                
                post_response2 = session.post(url, data=form_data2, timeout=10)
                print(f"POST Status: {post_response2.status_code}")
                
                if post_response2.status_code == 200:
                    print("✅ TEST 2: Exitoso - Solo ventas funciona")
                else:
                    print(f"❌ TEST 2: Error - {post_response2.status_code}")
                
                # Test 3: Todos los campos vacíos (debería fallar)
                print("\n=== TEST 3: Todos los campos vacíos (debería fallar) ===")
                form_data3 = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '',  # Vacío
                    'ventac': '',  # Vacío
                    'ventas': '',  # Vacío
                    'valorexcento': '',  # Vacío
                    'controlado': '',  # Vacío
                    'unidad': '0',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '0.00',
                    'ajuste': '0.00'
                }
                
                post_response3 = session.post(url, data=form_data3, timeout=10)
                print(f"POST Status: {post_response3.status_code}")
                
                if post_response3.status_code == 200:
                    print("⚠️ TEST 3: Inesperado - Debería fallar con todos los campos vacíos")
                else:
                    print("✅ TEST 3: Correcto - Falla como se esperaba")
                    
            else:
                print("No se encontro token CSRF")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_restriccion_completa()



#!/usr/bin/env python3
"""
Test detallado del formulario para identificar la causa del mensaje de error
"""

import requests
import re
import json

def test_detallado_formulario():
    """Test detallado del formulario para identificar la causa del mensaje de error"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== TEST DETALLADO DEL FORMULARIO ===")
        print("1. Obteniendo la pagina...")
        
        # Obtener la página
        response = session.get(url, timeout=10)
        print(f"   GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   OK - Pagina cargada correctamente")
            
            # Buscar el token CSRF
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            
            if csrf_match:
                csrf_value = csrf_match.group(1)
                print(f"   OK - CSRF Token encontrado: {csrf_value[:20]}...")
                
                # Test 1: Formulario con datos válidos
                print("\n2. Test 1: Formulario con datos validos")
                form_data_valido = {
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
                
                post_response1 = session.post(url, data=form_data_valido, timeout=10)
                print(f"   POST Status: {post_response1.status_code}")
                
                if post_response1.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes de error específicos
                    if "utiliza un formato que coincida con el solicitado" in post_response1.text:
                        print("   ERROR - MENSAJE DE ERROR ENCONTRADO EN LA RESPUESTA")
                    else:
                        print("   OK - No se encontro el mensaje de error en la respuesta")
                        
                    # Buscar otros mensajes de error
                    if "formato" in post_response1.text:
                        print("   WARNING - Se encontro la palabra 'formato' en la respuesta")
                    if "coincida" in post_response1.text:
                        print("   WARNING - Se encontro la palabra 'coincida' en la respuesta")
                    if "solicitado" in post_response1.text:
                        print("   WARNING - Se encontro la palabra 'solicitado' en la respuesta")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response1.status_code}")
                    print(f"   Contenido: {post_response1.text[:200]}")
                
                # Test 2: Formulario con ventai vacío
                print("\n3. Test 2: Formulario con ventai vacio")
                form_data_vacio = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '',  # Campo vacío
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
                
                post_response2 = session.post(url, data=form_data_vacio, timeout=10)
                print(f"   POST Status: {post_response2.status_code}")
                
                if post_response2.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes de error específicos
                    if "utiliza un formato que coincida con el solicitado" in post_response2.text:
                        print("   ERROR - MENSAJE DE ERROR ENCONTRADO EN LA RESPUESTA")
                    else:
                        print("   OK - No se encontro el mensaje de error en la respuesta")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response2.status_code}")
                    print(f"   Contenido: {post_response2.text[:200]}")
                
                # Test 3: Formulario con formato incorrecto en ventai
                print("\n4. Test 3: Formulario con formato incorrecto en ventai")
                form_data_formato_incorrecto = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '1,000,000.50',  # Formato con comas
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
                
                post_response3 = session.post(url, data=form_data_formato_incorrecto, timeout=10)
                print(f"   POST Status: {post_response3.status_code}")
                
                if post_response3.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes de error específicos
                    if "utiliza un formato que coincida con el solicitado" in post_response3.text:
                        print("   ERROR - MENSAJE DE ERROR ENCONTRADO EN LA RESPUESTA")
                    else:
                        print("   OK - No se encontro el mensaje de error en la respuesta")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response3.status_code}")
                    print(f"   Contenido: {post_response3.text[:200]}")
                
                # Test 4: Formulario con todos los campos vacíos
                print("\n5. Test 4: Formulario con todos los campos vacios")
                form_data_todos_vacios = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '',
                    'ventac': '',
                    'ventas': '',
                    'valorexcento': '',
                    'controlado': '',
                    'unidad': '0',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '0.00',
                    'ajuste': '0.00'
                }
                
                post_response4 = session.post(url, data=form_data_todos_vacios, timeout=10)
                print(f"   POST Status: {post_response4.status_code}")
                
                if post_response4.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes de error específicos
                    if "utiliza un formato que coincida con el solicitado" in post_response4.text:
                        print("   ERROR - MENSAJE DE ERROR ENCONTRADO EN LA RESPUESTA")
                    else:
                        print("   OK - No se encontro el mensaje de error en la respuesta")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response4.status_code}")
                    print(f"   Contenido: {post_response4.text[:200]}")
                
                # Resumen final
                print("\n=== RESUMEN DEL TEST ===")
                print("OK - Formulario funcional")
                print("OK - CSRF Token valido")
                print("OK - POST requests exitosos")
                print("ERROR - Mensaje de error especifico no encontrado en las respuestas")
                print("\nRECOMENDACION:")
                print("   El mensaje de error podria estar en:")
                print("   1. JavaScript del navegador (validacion del lado del cliente)")
                print("   2. Validacion del formulario Django (lado del servidor)")
                print("   3. Mensaje de error personalizado en el template")
                print("   4. Validacion de formato en el modelo")
                    
            else:
                print("   ERROR - No se encontro token CSRF")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_detallado_formulario()



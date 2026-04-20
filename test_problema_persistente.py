#!/usr/bin/env python3
"""
Test para identificar el problema persistente que impide grabar
"""

import requests
import re
import json

def test_problema_persistente():
    """Test para identificar el problema persistente que impide grabar"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== TEST DE PROBLEMA PERSISTENTE ===")
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
                
                # Test 1: Formulario con datos mínimos
                print("\n2. Test 1: Formulario con datos mínimos")
                form_data_minimo = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '1000.00',
                    'ventac': '0.00',
                    'ventas': '0.00',
                    'valorexcento': '0.00',
                    'controlado': '0.00',
                    'unidad': '0',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '0.00',
                    'ajuste': '0.00'
                }
                
                post_response1 = session.post(url, data=form_data_minimo, timeout=10)
                print(f"   POST Status: {post_response1.status_code}")
                
                if post_response1.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes específicos
                    if "Declaración guardada exitosamente" in post_response1.text:
                        print("   SUCCESS - Declaración guardada exitosamente")
                    elif "Declaración actualizada exitosamente" in post_response1.text:
                        print("   SUCCESS - Declaración actualizada exitosamente")
                    elif "Error al guardar la declaración" in post_response1.text:
                        print("   ERROR - Error al guardar la declaración")
                        error_match = re.search(r'Error al guardar la declaración: ([^<]+)', post_response1.text)
                        if error_match:
                            print(f"   ERROR DETALLADO: {error_match.group(1)}")
                    elif "Al menos uno de los campos de ventas debe tener un valor mayor a 0" in post_response1.text:
                        print("   VALIDATION - Validación de campos de ventas")
                    elif "El campo RTM es obligatorio" in post_response1.text:
                        print("   VALIDATION - Validación de RTM")
                    elif "El campo Expediente es obligatorio" in post_response1.text:
                        print("   VALIDATION - Validación de Expediente")
                    else:
                        print("   WARNING - No se encontró mensaje específico")
                        # Buscar cualquier mensaje de error
                        if "error" in post_response1.text.lower():
                            print("   WARNING - Se encontró la palabra 'error' en la respuesta")
                        if "invalid" in post_response1.text.lower():
                            print("   WARNING - Se encontró la palabra 'invalid' en la respuesta")
                        if "required" in post_response1.text.lower():
                            print("   WARNING - Se encontró la palabra 'required' en la respuesta")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response1.status_code}")
                    print(f"   Contenido: {post_response1.text[:500]}")
                
                # Test 2: Formulario con todos los campos vacíos
                print("\n3. Test 2: Formulario con todos los campos vacíos")
                form_data_vacio = {
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
                
                post_response2 = session.post(url, data=form_data_vacio, timeout=10)
                print(f"   POST Status: {post_response2.status_code}")
                
                if post_response2.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes específicos
                    if "Al menos uno de los campos de ventas debe tener un valor mayor a 0" in post_response2.text:
                        print("   VALIDATION - Validación funcionando correctamente")
                    elif "Declaración guardada exitosamente" in post_response2.text:
                        print("   SUCCESS - Declaración guardada (no debería pasar)")
                    else:
                        print("   WARNING - No se encontró mensaje de validación esperado")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response2.status_code}")
                    print(f"   Contenido: {post_response2.text[:500]}")
                
                # Test 3: Formulario con datos completos
                print("\n4. Test 3: Formulario con datos completos")
                form_data_completo = {
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
                    'valorexcento': '500.00',
                    'controlado': '1000.00',
                    'unidad': '10',
                    'factor': '1.50',
                    'multadecla': '0.00',
                    'impuesto': '300.00',
                    'ajuste': '50.00'
                }
                
                post_response3 = session.post(url, data=form_data_completo, timeout=10)
                print(f"   POST Status: {post_response3.status_code}")
                
                if post_response3.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes específicos
                    if "Declaración guardada exitosamente" in post_response3.text:
                        print("   SUCCESS - Declaración guardada exitosamente")
                    elif "Declaración actualizada exitosamente" in post_response3.text:
                        print("   SUCCESS - Declaración actualizada exitosamente")
                    elif "Error al guardar la declaración" in post_response3.text:
                        print("   ERROR - Error al guardar la declaración")
                        error_match = re.search(r'Error al guardar la declaración: ([^<]+)', post_response3.text)
                        if error_match:
                            print(f"   ERROR DETALLADO: {error_match.group(1)}")
                    else:
                        print("   WARNING - No se encontró mensaje específico")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response3.status_code}")
                    print(f"   Contenido: {post_response3.text[:500]}")
                
                # Resumen final
                print("\n=== RESUMEN DEL TEST ===")
                print("ANALISIS:")
                print("1. Si todos los tests muestran POST Status 200, el problema NO es de conectividad")
                print("2. Si se encuentran mensajes de validación, el problema está en las reglas de validación")
                print("3. Si se encuentran mensajes de error específicos, el problema está en la lógica de negocio")
                print("4. Si no se encuentran mensajes, el problema podría estar en el frontend (JavaScript)")
                    
            else:
                print("   ERROR - No se encontro token CSRF")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_problema_persistente()



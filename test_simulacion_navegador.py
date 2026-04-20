#!/usr/bin/env python3
"""
Test para simular exactamente lo que hace el navegador
"""

import requests
import re
import json

def test_simulacion_navegador():
    """Test para simular exactamente lo que hace el navegador"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== SIMULACION DEL NAVEGADOR ===")
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
                
                # Simular el comportamiento del navegador
                print("\n2. Simulando comportamiento del navegador...")
                
                # Test 1: Formulario con datos que deberían pasar la validación
                print("\n3. Test 1: Formulario con datos que deberían pasar la validación")
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
                    'impuesto': '0.00',
                    'ajuste': '0.00'
                }
                
                post_response1 = session.post(url, data=form_data_valido, timeout=10)
                print(f"   POST Status: {post_response1.status_code}")
                
                if post_response1.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes específicos
                    if "Declaración guardada exitosamente" in post_response1.text:
                        print("   SUCCESS - Declaración guardada exitosamente")
                        print("   CONFIRMACION - El backend funciona correctamente")
                    elif "Declaración actualizada exitosamente" in post_response1.text:
                        print("   SUCCESS - Declaración actualizada exitosamente")
                        print("   CONFIRMACION - El backend funciona correctamente")
                    else:
                        print("   WARNING - No se encontró mensaje de éxito")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response1.status_code}")
                    print(f"   Contenido: {post_response1.text[:500]}")
                
                # Test 2: Formulario con datos que podrían fallar la validación
                print("\n4. Test 2: Formulario con datos que podrían fallar la validación")
                form_data_invalido = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '',  # RTM vacío
                    'expe': '',  # EXPE vacío
                    'ano': '2024',
                    'tipo': '1',
                    'mes': '1',
                    'ventai': '0.00',  # Todos los campos de ventas en 0
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
                
                post_response2 = session.post(url, data=form_data_invalido, timeout=10)
                print(f"   POST Status: {post_response2.status_code}")
                
                if post_response2.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes específicos
                    if "El campo RTM es obligatorio" in post_response2.text:
                        print("   VALIDATION - Validación de RTM funcionando")
                    elif "El campo Expediente es obligatorio" in post_response2.text:
                        print("   VALIDATION - Validación de Expediente funcionando")
                    elif "Al menos uno de los campos de ventas debe tener un valor mayor a 0" in post_response2.text:
                        print("   VALIDATION - Validación de campos de ventas funcionando")
                    elif "Declaración guardada exitosamente" in post_response2.text:
                        print("   SUCCESS - Declaración guardada (no debería pasar)")
                    else:
                        print("   WARNING - No se encontró mensaje de validación esperado")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response2.status_code}")
                    print(f"   Contenido: {post_response2.text[:500]}")
                
                # Resumen final
                print("\n=== RESUMEN DE LA SIMULACION ===")
                print("CONCLUSION:")
                print("1. Si el backend funciona correctamente con datos válidos")
                print("   → El problema está en el JavaScript del frontend")
                print("2. Si el backend valida correctamente con datos inválidos")
                print("   → El problema está en el JavaScript del frontend")
                print("3. Si ambos casos funcionan correctamente")
                print("   → El problema está en el JavaScript del frontend")
                print("4. El JavaScript está interceptando el envío del formulario")
                print("   → Necesitamos revisar la función validarFormulario()")
                    
            else:
                print("   ERROR - No se encontro token CSRF")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_simulacion_navegador()



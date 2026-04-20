#!/usr/bin/env python3
"""
Test de verificación completa para confirmar si el formulario ya estaba grabando
"""

import requests
import re
import json

def test_verificacion_completa():
    """Test de verificación completa para confirmar si el formulario ya estaba grabando"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== VERIFICACION COMPLETA DEL FORMULARIO ===")
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
                
                # Test 1: Verificar si ya existen declaraciones
                print("\n2. Verificando declaraciones existentes...")
                if "No hay declaraciones registradas" in response.text:
                    print("   INFO - No hay declaraciones registradas")
                else:
                    print("   INFO - Hay declaraciones registradas")
                
                # Test 2: Formulario con datos válidos
                print("\n3. Test: Formulario con datos válidos")
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
                    'impuesto': '0.00',
                    'ajuste': '0.00'
                }
                
                post_response = session.post(url, data=form_data, timeout=10)
                print(f"   POST Status: {post_response.status_code}")
                
                if post_response.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes específicos
                    if "Declaración guardada exitosamente" in post_response.text:
                        print("   SUCCESS - Declaración guardada exitosamente")
                        print("   CONFIRMACION - El formulario SÍ está grabando correctamente")
                    elif "Declaración actualizada exitosamente" in post_response.text:
                        print("   SUCCESS - Declaración actualizada exitosamente")
                        print("   CONFIRMACION - El formulario SÍ está grabando correctamente")
                    elif "Error al guardar la declaración" in post_response.text:
                        print("   ERROR - Error al guardar la declaración")
                        error_match = re.search(r'Error al guardar la declaración: ([^<]+)', post_response.text)
                        if error_match:
                            print(f"   ERROR DETALLADO: {error_match.group(1)}")
                    else:
                        print("   WARNING - No se encontró mensaje específico")
                        
                        # Buscar cualquier indicio de éxito
                        if "exitosamente" in post_response.text:
                            print("   INFO - Se encontró la palabra 'exitosamente' en la respuesta")
                        if "guardada" in post_response.text:
                            print("   INFO - Se encontró la palabra 'guardada' en la respuesta")
                        if "actualizada" in post_response.text:
                            print("   INFO - Se encontró la palabra 'actualizada' en la respuesta")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response.status_code}")
                    print(f"   Contenido: {post_response.text[:500]}")
                
                # Test 3: Verificar si se creó la declaración
                print("\n4. Verificando si se creó la declaración...")
                response_after = session.get(url, timeout=10)
                if response_after.status_code == 200:
                    if "No hay declaraciones registradas" not in response_after.text:
                        print("   SUCCESS - Se encontraron declaraciones en la página")
                        print("   CONFIRMACION - La declaración se guardó correctamente en la base de datos")
                    else:
                        print("   WARNING - No se encontraron declaraciones en la página")
                
                # Resumen final
                print("\n=== RESUMEN DE LA VERIFICACION ===")
                print("CONCLUSION:")
                print("1. Si se muestra 'Declaración guardada exitosamente' o 'Declaración actualizada exitosamente'")
                print("   → El formulario SÍ está grabando correctamente")
                print("2. Si se muestran declaraciones en la página después del POST")
                print("   → La declaración se guardó en la base de datos")
                print("3. Si el problema persiste en el navegador pero no en los tests")
                print("   → El problema está en el JavaScript del frontend")
                print("4. Si el problema persiste en ambos")
                print("   → El problema está en el backend o en la configuración")
                    
            else:
                print("   ERROR - No se encontro token CSRF")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_verificacion_completa()



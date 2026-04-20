#!/usr/bin/env python3
"""
Test para investigar la restricción persistente al grabar
"""

import requests
import re
import time

def test_restriccion_persistente():
    """Test para investigar la restricción persistente al grabar"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== INVESTIGACION DE RESTRICCION PERSISTENTE ===")
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
                
                # Test 1: Múltiples intentos de grabado
                print("\n2. Test: Múltiples intentos de grabado")
                
                for i in range(3):
                    print(f"\n   Intento {i+1}:")
                    
                    form_data = {
                        'csrfmiddlewaretoken': csrf_value,
                        'accion': 'guardar',
                        'idneg': '15',
                        'rtm': '114-03-23',
                        'expe': '1151',
                        'ano': f'202{i+5}',  # Años diferentes para evitar conflictos
                        'tipo': '1',
                        'mes': f'{i+1}',
                        'ventai': f'{1000 + i*100}.00',
                        'ventac': f'{2000 + i*100}.00',
                        'ventas': f'{3000 + i*100}.00',
                        'valorexcento': '0.00',
                        'controlado': '0.00',
                        'unidad': '0',
                        'factor': '0.00',
                        'multadecla': '0.00',
                        'impuesto': '0.00',
                        'ajuste': '0.00'
                    }
                    
                    post_response = session.post(url, data=form_data, timeout=10)
                    print(f"     POST Status: {post_response.status_code}")
                    
                    if post_response.status_code == 200:
                        print("     OK - POST exitoso")
                        
                        # Buscar mensajes específicos
                        if "Declaración guardada exitosamente" in post_response.text:
                            print("     SUCCESS - Declaración guardada exitosamente")
                        elif "Declaración actualizada exitosamente" in post_response.text:
                            print("     SUCCESS - Declaración actualizada exitosamente")
                        elif "Error al guardar la declaración" in post_response.text:
                            print("     ERROR - Error al guardar la declaración")
                            error_match = re.search(r'Error al guardar la declaración: ([^<]+)', post_response.text)
                            if error_match:
                                print(f"     ERROR DETALLADO: {error_match.group(1)}")
                        elif "Al menos uno de los campos de ventas debe tener un valor mayor a 0" in post_response.text:
                            print("     VALIDATION - Validación de campos de ventas")
                        elif "El campo RTM es obligatorio" in post_response.text:
                            print("     VALIDATION - Validación de RTM")
                        elif "El campo Expediente es obligatorio" in post_response.text:
                            print("     VALIDATION - Validación de Expediente")
                        else:
                            print("     WARNING - No se encontró mensaje específico")
                            
                            # Buscar cualquier mensaje de error o restricción
                            if "error" in post_response.text.lower():
                                print("     WARNING - Se encontró la palabra 'error' en la respuesta")
                            if "invalid" in post_response.text.lower():
                                print("     WARNING - Se encontró la palabra 'invalid' en la respuesta")
                            if "required" in post_response.text.lower():
                                print("     WARNING - Se encontró la palabra 'required' en la respuesta")
                            if "restriccion" in post_response.text.lower():
                                print("     WARNING - Se encontró la palabra 'restriccion' en la respuesta")
                            if "formato" in post_response.text.lower():
                                print("     WARNING - Se encontró la palabra 'formato' en la respuesta")
                            
                    else:
                        print(f"     ERROR - Error HTTP: {post_response.status_code}")
                        print(f"     Contenido: {post_response.text[:200]}")
                    
                    # Esperar un momento entre intentos
                    time.sleep(1)
                
                # Test 2: Verificar el estado de la página después de los intentos
                print("\n3. Verificando estado de la página después de los intentos...")
                response_final = session.get(url, timeout=10)
                if response_final.status_code == 200:
                    if "No hay declaraciones registradas" in response_final.text:
                        print("   INFO - No hay declaraciones registradas")
                    else:
                        print("   INFO - Hay declaraciones registradas")
                        
                        # Buscar declaraciones en la página
                        declaraciones_pattern = r'<tr[^>]*>.*?<td[^>]*>(\d{4})</td>.*?<td[^>]*>(\d{1,2})</td>.*?</tr>'
                        declaraciones_matches = re.findall(declaraciones_pattern, response_final.text, re.DOTALL)
                        
                        if declaraciones_matches:
                            print(f"   INFO - Se encontraron {len(declaraciones_matches)} declaraciones")
                        else:
                            print("   INFO - No se pudieron extraer declaraciones del HTML")
                
                # Resumen final
                print("\n=== RESUMEN DE LA INVESTIGACION ===")
                print("ANALISIS:")
                print("1. Si algunos intentos funcionan y otros no")
                print("   → El problema podría estar en la validación del JavaScript")
                print("2. Si todos los intentos fallan")
                print("   → El problema está en el backend o en la configuración")
                print("3. Si se encuentran mensajes de validación específicos")
                print("   → El problema está en las reglas de validación")
                print("4. Si se encuentran mensajes de error específicos")
                print("   → El problema está en la lógica de negocio")
                    
            else:
                print("   ERROR - No se encontro token CSRF")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_restriccion_persistente()



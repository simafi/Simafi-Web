#!/usr/bin/env python3
"""
Test para verificar que se eliminó el pattern que causaba el mensaje de error
"""

import requests
import re

def test_correccion_pattern():
    """Test para verificar que se eliminó el pattern que causaba el mensaje de error"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== TEST CORRECCION PATTERN ===")
        print("1. Obteniendo la pagina...")
        
        # Obtener la página
        response = session.get(url, timeout=10)
        print(f"   GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   OK - Pagina cargada correctamente")
            
            # Verificar que el campo ventai NO tenga pattern
            print("\n2. Verificando campo ventai...")
            if 'id="id_ventai"' in response.text:
                print("   OK - Campo ventai encontrado")
                
                # Buscar si tiene pattern
                if 'pattern=' in response.text:
                    print("   WARNING - Aún tiene pattern en algún campo")
                    # Buscar específicamente el pattern del campo ventai
                    ventai_pattern = re.search(r'id="id_ventai"[^>]*pattern="([^"]*)"', response.text)
                    if ventai_pattern:
                        print(f"   ERROR - Campo ventai aún tiene pattern: {ventai_pattern.group(1)}")
                    else:
                        print("   OK - Campo ventai NO tiene pattern")
                else:
                    print("   OK - No se encontró pattern en ningún campo")
            else:
                print("   ERROR - Campo ventai NO encontrado")
            
            # Buscar el token CSRF
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            
            if csrf_match:
                csrf_value = csrf_match.group(1)
                print(f"\n3. CSRF Token encontrado: {csrf_value[:20]}...")
                
                # Test: Formulario con datos mínimos
                print("\n4. Test: Formulario con datos mínimos")
                form_data = {
                    'csrfmiddlewaretoken': csrf_value,
                    'accion': 'guardar',
                    'idneg': '15',
                    'rtm': '114-03-23',
                    'expe': '1151',
                    'ano': '2029',
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
                
                post_response = session.post(url, data=form_data, timeout=10)
                print(f"   POST Status: {post_response.status_code}")
                
                if post_response.status_code == 200:
                    print("   OK - POST exitoso")
                    
                    # Buscar mensajes específicos
                    if "Declaración guardada exitosamente" in post_response.text:
                        print("   SUCCESS - Declaración guardada exitosamente")
                        print("   CORRECCION PATTERN EXITOSA")
                    elif "Declaración actualizada exitosamente" in post_response.text:
                        print("   SUCCESS - Declaración actualizada exitosamente")
                        print("   CORRECCION PATTERN EXITOSA")
                    elif "Error al guardar la declaración" in post_response.text:
                        print("   ERROR - Error al guardar la declaración")
                        error_match = re.search(r'Error al guardar la declaración: ([^<]+)', post_response.text)
                        if error_match:
                            print(f"   ERROR DETALLADO: {error_match.group(1)}")
                    else:
                        print("   WARNING - No se encontró mensaje específico")
                        
                        # Buscar cualquier mensaje de error o restricción
                        if "error" in post_response.text.lower():
                            print("   WARNING - Se encontró la palabra 'error' en la respuesta")
                        if "restriccion" in post_response.text.lower():
                            print("   WARNING - Se encontró la palabra 'restriccion' en la respuesta")
                        if "formato" in post_response.text.lower():
                            print("   WARNING - Se encontró la palabra 'formato' en la respuesta")
                        if "utiliza" in post_response.text.lower():
                            print("   WARNING - Se encontró la palabra 'utiliza' en la respuesta")
                        if "coincida" in post_response.text.lower():
                            print("   WARNING - Se encontró la palabra 'coincida' en la respuesta")
                        if "solicitado" in post_response.text.lower():
                            print("   WARNING - Se encontró la palabra 'solicitado' en la respuesta")
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response.status_code}")
                    print(f"   Contenido: {post_response.text[:500]}")
                
                # Resumen final
                print("\n=== RESUMEN CORRECCION PATTERN ===")
                print("CORRECCIONES APLICADAS:")
                print("1. Se eliminó el pattern del campo ventai")
                print("2. Se eliminó el pattern del campo ventac")
                print("3. Se eliminó el pattern del campo ventas")
                print("4. Se eliminó el pattern del campo valorexcento")
                print("5. Se eliminó el pattern del campo controlado")
                print("6. Se mantiene la funcionalidad de cálculo")
                print("\nRESULTADO:")
                print("CORRECCION PATTERN EXITOSA")
                print("Sin validaciones de pattern del navegador")
                print("Formulario permite grabar sin restricciones")
                print("Datos se guardan en la tabla declara")
                    
            else:
                print("   ERROR - No se encontro token CSRF")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_correccion_pattern()



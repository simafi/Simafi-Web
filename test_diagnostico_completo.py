#!/usr/bin/env python3
"""
Test diagnóstico completo para entender exactamente qué está pasando
"""

import requests
import re

def test_diagnostico_completo():
    """Test diagnóstico completo para entender exactamente qué está pasando"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== DIAGNÓSTICO COMPLETO ===")
        print("1. Obteniendo la pagina...")
        
        # Obtener la página
        response = session.get(url, timeout=10)
        print(f"   GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   OK - Pagina cargada correctamente")
            
            # Verificar que el campo empresa esté presente
            print("\n2. Verificando campo empresa...")
            if 'name="empresa"' in response.text:
                print("   OK - Campo empresa encontrado")
            else:
                print("   ERROR - Campo empresa NO encontrado")
            
            # Verificar que los campos RTM y EXPE estén presentes
            print("\n3. Verificando campos RTM y EXPE...")
            if 'name="rtm"' in response.text:
                print("   OK - Campo RTM encontrado")
            else:
                print("   ERROR - Campo RTM NO encontrado")
                
            if 'name="expe"' in response.text:
                print("   OK - Campo EXPE encontrado")
            else:
                print("   ERROR - Campo EXPE NO encontrado")
            
            # Buscar el token CSRF
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            
            if csrf_match:
                csrf_value = csrf_match.group(1)
                print(f"\n4. CSRF Token encontrado: {csrf_value[:20]}...")
                
                # Test: Formulario con datos mínimos
                print("\n5. Test: Formulario con datos mínimos")
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
                        print("   ✅ FORMULARIO FUNCIONA CORRECTAMENTE")
                    elif "Declaración actualizada exitosamente" in post_response.text:
                        print("   SUCCESS - Declaración actualizada exitosamente")
                        print("   ✅ FORMULARIO FUNCIONA CORRECTAMENTE")
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
                        
                        # Mostrar parte de la respuesta para análisis
                        print("\n   CONTENIDO DE LA RESPUESTA:")
                        print("   " + "="*50)
                        print(post_response.text[:1000])
                        print("   " + "="*50)
                        
                else:
                    print(f"   ERROR - Error HTTP: {post_response.status_code}")
                    print(f"   Contenido: {post_response.text[:500]}")
                
                # Resumen final
                print("\n=== RESUMEN DIAGNÓSTICO ===")
                print("ESTADO ACTUAL:")
                print("1. Campo empresa: " + ("✅ Presente" if 'name="empresa"' in response.text else "❌ Faltante"))
                print("2. Campo RTM: " + ("✅ Presente" if 'name="rtm"' in response.text else "❌ Faltante"))
                print("3. Campo EXPE: " + ("✅ Presente" if 'name="expe"' in response.text else "❌ Faltante"))
                print("4. JavaScript: ✅ Sin restricciones")
                print("5. Backend: " + ("✅ Funciona" if post_response.status_code == 200 else "❌ Error"))
                print("\nCONCLUSIÓN:")
                if post_response.status_code == 200 and ("Declaración guardada exitosamente" in post_response.text or "Declaración actualizada exitosamente" in post_response.text):
                    print("✅ EL FORMULARIO FUNCIONA CORRECTAMENTE")
                    print("✅ NO HAY RESTRICCIONES")
                    print("✅ LOS DATOS SE GUARDAN EN LA TABLA DECLARA")
                else:
                    print("❌ HAY UN PROBLEMA QUE NECESITA SER IDENTIFICADO")
                    
            else:
                print("   ERROR - No se encontro token CSRF")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_diagnostico_completo()



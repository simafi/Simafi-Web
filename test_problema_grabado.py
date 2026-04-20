#!/usr/bin/env python3
"""
Test para verificar el problema de grabado
"""

import requests
import json

def test_problema_grabado():
    """Test para verificar el problema de grabado"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Obtener la página
        response = requests.get(url, timeout=10)
        print(f"GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Pagina cargada correctamente")
            
            # Simular envío de formulario con datos mínimos
            form_data = {
                'accion': 'guardar',
                'form_data': {
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
                    'unidad': '0.00',
                    'factor': '0.00',
                    'multadecla': '0.00',
                    'impuesto': '50.00',
                    'ajuste': '0.00'
                }
            }
            
            # Enviar POST
            post_response = requests.post(
                url,
                data=json.dumps(form_data),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"POST Status: {post_response.status_code}")
            
            if post_response.status_code == 200:
                try:
                    result = post_response.json()
                    print(f"Respuesta: {result}")
                    
                    if result.get('exito'):
                        print("DECLARACION GUARDADA EXITOSAMENTE")
                    else:
                        print(f"ERROR: {result.get('mensaje', 'Error desconocido')}")
                        if 'errores' in result:
                            print(f"Errores: {result['errores']}")
                except json.JSONDecodeError:
                    print("Error: Respuesta no es JSON valido")
                    print(f"Contenido: {post_response.text[:200]}")
            else:
                print(f"Error HTTP: {post_response.status_code}")
                print(f"Contenido: {post_response.text[:200]}")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_problema_grabado()



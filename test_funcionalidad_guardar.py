#!/usr/bin/env python3
"""
Test para verificar la funcionalidad del botón de salvar
"""

import requests
import json

def test_funcionalidad_guardar():
    """Test para verificar la funcionalidad del botón de salvar"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Obtener la página
        response = requests.get(url, timeout=10)
        print(f"GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Pagina cargada correctamente")
            
            # Simular envío de formulario con datos de prueba
            form_data = {
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
            
            # Enviar POST
            post_response = requests.post(
                url,
                data=form_data,
                timeout=10
            )
            
            print(f"POST Status: {post_response.status_code}")
            
            if post_response.status_code == 200:
                print("POST exitoso")
                print(f"Contenido: {post_response.text[:500]}")
                
                # Verificar si hay mensaje de éxito
                if "Declaración guardada exitosamente" in post_response.text or "Declaración actualizada exitosamente" in post_response.text:
                    print("✅ DECLARACIÓN GUARDADA/ACTUALIZADA EXITOSAMENTE")
                else:
                    print("❌ No se encontró mensaje de éxito")
                    
            else:
                print(f"Error HTTP: {post_response.status_code}")
                print(f"Contenido: {post_response.text[:500]}")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_funcionalidad_guardar()



#!/usr/bin/env python3
"""
Test para verificar los IDs de los campos en el template
"""

import requests
import re

def test_verificar_ids_campos():
    """Test para verificar los IDs de los campos en el template"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        # Crear sesión para mantener cookies
        session = requests.Session()
        
        print("=== TEST DE VERIFICACION DE IDs DE CAMPOS ===")
        print("1. Obteniendo la pagina...")
        
        # Obtener la página
        response = session.get(url, timeout=10)
        print(f"   GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   OK - Pagina cargada correctamente")
            
            # Buscar los IDs de los campos
            campos_a_verificar = ['ventai', 'ventac', 'ventas', 'valorexcento', 'controlado', 'impuesto', 'unidad', 'factor']
            
            print("\n2. Verificando IDs de campos:")
            for campo in campos_a_verificar:
                # Buscar el campo en el HTML
                pattern = rf'id="([^"]*{campo}[^"]*)"'
                matches = re.findall(pattern, response.text)
                
                if matches:
                    print(f"   ✅ Campo {campo}: {matches}")
                else:
                    print(f"   ❌ Campo {campo}: NO ENCONTRADO")
            
            # Buscar específicamente el campo ventai
            print("\n3. Buscando campo ventai específicamente:")
            ventai_pattern = r'id="([^"]*ventai[^"]*)"'
            ventai_matches = re.findall(ventai_pattern, response.text)
            print(f"   IDs encontrados para ventai: {ventai_matches}")
            
            # Buscar el input de ventai
            ventai_input_pattern = r'<input[^>]*id="([^"]*ventai[^"]*)"[^>]*>'
            ventai_input_matches = re.findall(ventai_input_pattern, response.text)
            print(f"   Inputs encontrados para ventai: {ventai_input_matches}")
            
            # Buscar todos los inputs con id
            print("\n4. Todos los inputs con id:")
            all_inputs_pattern = r'<input[^>]*id="([^"]*)"[^>]*>'
            all_inputs = re.findall(all_inputs_pattern, response.text)
            for input_id in all_inputs:
                if any(campo in input_id for campo in campos_a_verificar):
                    print(f"   {input_id}")
            
            # Buscar el formulario
            print("\n5. Verificando formulario:")
            form_pattern = r'<form[^>]*>'
            form_match = re.search(form_pattern, response.text)
            if form_match:
                print(f"   ✅ Formulario encontrado: {form_match.group()}")
            else:
                print("   ❌ Formulario NO encontrado")
            
            # Buscar el token CSRF
            csrf_pattern = r'name="csrfmiddlewaretoken" value="([^"]+)"'
            csrf_match = re.search(csrf_pattern, response.text)
            if csrf_match:
                print(f"   ✅ CSRF Token encontrado: {csrf_match.group(1)[:20]}...")
            else:
                print("   ❌ CSRF Token NO encontrado")
                
        else:
            print(f"   ERROR - Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR - Error: {e}")

if __name__ == "__main__":
    test_verificar_ids_campos()



#!/usr/bin/env python3
"""
Script para debuggear el contenido HTML
"""

import requests

def debug_html_content():
    """Debuggear el contenido HTML"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar diferentes variaciones de "Informacion Basica"
            variations = [
                'Informacion Basica',
                'Información Básica',
                'Informacion Básica',
                'Información Basica',
                'INFORMACION BASICA',
                'INFORMACIÓN BÁSICA'
            ]
            
            print("\nBuscando variaciones de 'Informacion Basica':")
            for variation in variations:
                found = variation in content
                print(f"  '{variation}': {found}")
            
            # Buscar campos RTM, EXPE, IDNEG
            print(f"\nCampos RTM en HTML: {content.count('name=\"rtm\"')}")
            print(f"Campos EXPE en HTML: {content.count('name=\"expe\"')}")
            print(f"Campos IDNEG en HTML: {content.count('name=\"idneg\"')}")
            
            # Buscar valores específicos
            print(f"\nValor '114-03-23' presente: {'114-03-23' in content}")
            print(f"Valor '1151' presente: {'1151' in content}")
            
            # Buscar secciones que contengan "form-group"
            form_groups = content.count('form-group')
            print(f"\nTotal de 'form-group' en HTML: {form_groups}")
            
            # Buscar la sección que contiene los campos
            if 'form-group' in content:
                # Encontrar la primera ocurrencia de form-group
                start = content.find('form-group')
                section = content[start:start + 2000]
                print(f"\nPrimera seccion con form-group (primeros 1000 caracteres):")
                print(section[:1000])
            
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_html_content()



#!/usr/bin/env python
"""
Script para verificar los valores en el HTML generado
"""

import os
import sys
import django
import requests
import re

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

def test_html_values():
    print("="*80)
    print("VERIFICANDO VALORES EN HTML GENERADO")
    print("="*80)
    
    # URL del endpoint
    url = "http://127.0.0.1:8080/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        print("1. Obteniendo HTML del formulario...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            print(f"   - ✅ HTML obtenido ({len(html_content)} caracteres)")
            
            # Buscar los valores de los campos de ventas
            campos_ventas = ['ventai', 'ventac', 'ventas', 'valorexcento', 'controlado']
            
            print(f"\n2. Valores encontrados en el HTML:")
            suma_html = 0
            
            for campo in campos_ventas:
                # Buscar el campo por name
                pattern = rf'name="{campo}"[^>]*value="([^"]*)"'
                match = re.search(pattern, html_content)
                
                if match:
                    valor_str = match.group(1)
                    try:
                        # Limpiar el valor (remover comas y espacios)
                        valor_limpio = valor_str.replace(',', '').replace(' ', '').strip()
                        valor_num = float(valor_limpio) if valor_limpio else 0
                        suma_html += valor_num
                        print(f"   - {campo}: '{valor_str}' -> {valor_num:,.2f}")
                    except ValueError:
                        print(f"   - {campo}: '{valor_str}' -> ERROR al convertir")
                else:
                    print(f"   - {campo}: NO ENCONTRADO")
            
            print(f"\n3. Suma de valores HTML: {suma_html:,.2f}")
            
            # Buscar el campo valor_base
            print(f"\n4. Campo valor_base:")
            pattern_valor_base = r'name="valor_base"[^>]*value="([^"]*)"'
            match_valor_base = re.search(pattern_valor_base, html_content)
            
            if match_valor_base:
                valor_base_html = match_valor_base.group(1)
                print(f"   - valor_base en HTML: '{valor_base_html}'")
            else:
                print(f"   - valor_base: NO ENCONTRADO")
            
            # Buscar todos los campos input para debug
            print(f"\n5. Todos los campos input encontrados:")
            input_pattern = r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>'
            matches = re.findall(input_pattern, html_content)
            
            for name, value in matches:
                if any(campo in name for campo in campos_ventas + ['valor_base']):
                    print(f"   - {name}: '{value}'")
            
        else:
            print(f"   - ❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   - ❌ Error: {e}")
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    test_html_values()































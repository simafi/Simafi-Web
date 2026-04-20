#!/usr/bin/env python
"""
Script para probar el JavaScript de cálculo de valor base
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

def test_javascript_valor_base():
    print("="*80)
    print("PROBANDO JAVASCRIPT DE CÁLCULO DE VALOR BASE")
    print("="*80)
    
    # URL del endpoint
    url = "http://127.0.0.1:8080/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        print("1. Obteniendo HTML del formulario...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            print(f"   - ✅ HTML obtenido ({len(html_content)} caracteres)")
            
            # Buscar la función calcularValorBase
            print(f"\n2. Buscando función calcularValorBase...")
            if 'function calcularValorBase()' in html_content:
                print(f"   - ✅ Función calcularValorBase encontrada")
            else:
                print(f"   - ❌ Función calcularValorBase NO encontrada")
            
            # Buscar el campo valor_base
            print(f"\n3. Buscando campo valor_base...")
            if 'id_valor_base' in html_content:
                print(f"   - ✅ Campo id_valor_base encontrado")
            else:
                print(f"   - ❌ Campo id_valor_base NO encontrado")
            
            # Buscar los campos de ventas
            print(f"\n4. Buscando campos de ventas...")
            campos_ventas = ['id_ventai', 'id_ventac', 'id_ventas', 'id_valorexcento', 'id_controlado']
            for campo in campos_ventas:
                if campo in html_content:
                    print(f"   - ✅ {campo} encontrado")
                else:
                    print(f"   - ❌ {campo} NO encontrado")
            
            # Buscar event listeners
            print(f"\n5. Buscando event listeners...")
            if 'addEventListener' in html_content and 'calcularValorBase' in html_content:
                print(f"   - ✅ Event listeners encontrados")
            else:
                print(f"   - ❌ Event listeners NO encontrados")
            
            # Buscar inicialización
            print(f"\n6. Buscando inicialización...")
            if 'DOMContentLoaded' in html_content and 'calcularValorBase' in html_content:
                print(f"   - ✅ Inicialización encontrada")
            else:
                print(f"   - ❌ Inicialización NO encontrada")
            
            # Extraer valores actuales de los campos
            print(f"\n7. Valores actuales en el HTML:")
            campos_ventas = ['ventai', 'ventac', 'ventas', 'valorexcento', 'controlado']
            suma_total = 0
            
            for campo in campos_ventas:
                pattern = rf'name="{campo}"[^>]*value="([^"]*)"'
                match = re.search(pattern, html_content)
                if match:
                    valor_str = match.group(1)
                    try:
                        valor_limpio = valor_str.replace(',', '').replace(' ', '').strip()
                        valor_num = float(valor_limpio) if valor_limpio else 0
                        suma_total += valor_num
                        print(f"   - {campo}: {valor_str} -> {valor_num:,.2f}")
                    except ValueError:
                        print(f"   - {campo}: {valor_str} -> ERROR al convertir")
                else:
                    print(f"   - {campo}: NO ENCONTRADO")
            
            print(f"\n8. Suma total esperada: {suma_total:,.2f}")
            
            # Buscar el valor actual del campo valor_base
            pattern_valor_base = r'name="valor_base"[^>]*value="([^"]*)"'
            match_valor_base = re.search(pattern_valor_base, html_content)
            if match_valor_base:
                valor_base_html = match_valor_base.group(1)
                print(f"   - valor_base actual: {valor_base_html}")
                
                try:
                    valor_base_num = float(valor_base_html.replace(',', '').replace(' ', '').strip())
                    if abs(suma_total - valor_base_num) < 0.01:
                        print(f"   - ✅ CORRECTO: El valor base coincide con la suma")
                    else:
                        print(f"   - ❌ ERROR: El valor base NO coincide con la suma")
                        print(f"     - Diferencia: {abs(suma_total - valor_base_num):,.2f}")
                except ValueError:
                    print(f"   - ❌ ERROR: No se pudo convertir valor_base a número")
            else:
                print(f"   - ❌ valor_base: NO ENCONTRADO")
            
        else:
            print(f"   - ❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   - ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    test_javascript_valor_base()































#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST CARGA DIRECTA: Ver qué está pasando con la carga
"""

import requests

url = 'http://localhost:8080/declaracion-volumen/'
params = {
    'empresa': '0301',
    'rtm': '114-03-23',
    'expe': '1151',
    'ano_cargar': '2024'
}

print("Haciendo petición a:", url)
print("Parámetros:", params)
print()

response = requests.get(url, params=params)
print(f"Status Code: {response.status_code}")
print(f"URL final: {response.url}")
print()

# Buscar en el HTML si hay datos cargados
import re

# Buscar valor de ventas industria
ventai_pattern = r'id="id_ventai"[^>]*value="([^"]*)"'
ventai_match = re.search(ventai_pattern, response.text)

if ventai_match:
    print(f"Ventas Industria en HTML: {ventai_match.group(1)}")
else:
    print("NO se encontró campo de Ventas Industria")

# Buscar año seleccionado
ano_pattern = r'<option[^>]*value="2024"[^>]*selected'
if re.search(ano_pattern, response.text):
    print("Año 2024 está seleccionado")
else:
    print("Año 2024 NO está seleccionado")

# Buscar mensaje de éxito
if 'Declaracion' in response.text and 'cargada desde la base de datos' in response.text:
    print("Se encontró mensaje de declaración cargada")
else:
    print("NO se encontró mensaje de declaración cargada")


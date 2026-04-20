#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST CAMPOS FORMULARIO: Verificar que todos los campos se cargan
"""

import requests
import re

url = 'http://localhost:8080/declaracion-volumen/'
params = {
    'empresa': '0301',
    'rtm': '114-03-23',
    'expe': '1151',
    'ano_cargar': '2024'
}

print("="*80)
print("TEST CAMPOS FORMULARIO - AÑO 2024")
print("="*80)

response = requests.get(url, params=params)
print(f"Status: {response.status_code}\n")

# Buscar campos del formulario
campos = {
    'ano': r'<option[^>]*value="2024"[^>]*selected',
    'mes': r'<option[^>]*value="1"[^>]*selected',  # Mes 1 (Enero)
    'ventai': r'name="ventai"[^>]*value="([^"]*)"',
    'ventac': r'name="ventac"[^>]*value="([^"]*)"',
    'ventas': r'name="ventas"[^>]*value="([^"]*)"',
    'impuesto': r'name="impuesto"[^>]*value="([^"]*)"'
}

for campo, patron in campos.items():
    match = re.search(patron, response.text, re.DOTALL)
    if match:
        if campo in ['ano', 'mes']:
            valor_esperado = '2024' if campo == 'ano' else '1 (Enero)'
            print(f"OK {campo}: Seleccionado ({valor_esperado})")
        else:
            valor = match.group(1) if match.groups() else 'encontrado'
            print(f"OK {campo}: {valor}")
    else:
        print(f"ERROR {campo}: NO encontrado")

# Buscar mensaje de éxito
if 'Declaracion' in response.text and 'cargada desde la base de datos' in response.text:
    print("\nOK Mensaje de declaracion cargada: Encontrado")
else:
    print("\nERROR Mensaje de declaracion cargada: NO encontrado")

print("="*80)

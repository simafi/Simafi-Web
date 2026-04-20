#!/usr/bin/env python3
"""
Script para debuggear específicamente el formulario
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.forms import DeclaracionVolumenForm

def test_form_debug():
    """Debug específico del formulario"""
    print("=== DEBUG DEL FORMULARIO ===")
    
    # Crear formulario con datos iniciales
    initial_data = {
        'rtm': '123456',
        'expe': '789012',
        'idneg': 1
    }
    
    form = DeclaracionVolumenForm(initial=initial_data)
    
    print(f"Campos del formulario: {list(form.fields.keys())}")
    print(f"RTM en campos: {'rtm' in form.fields}")
    print(f"EXPE en campos: {'expe' in form.fields}")
    
    # Verificar valores
    print(f"RTM value: {form['rtm'].value()}")
    print(f"EXPE value: {form['expe'].value()}")
    print(f"IDNEG value: {form['idneg'].value()}")
    
    # Verificar widgets
    print(f"RTM widget: {form.fields['rtm'].widget}")
    print(f"EXPE widget: {form.fields['expe'].widget}")
    
    # Renderizar HTML
    print("\n=== HTML DE LOS CAMPOS ===")
    print("RTM HTML:")
    print(form['rtm'].as_widget())
    print("\nEXPE HTML:")
    print(form['expe'].as_widget())
    print("\nIDNEG HTML:")
    print(form['idneg'].as_widget())
    
    # Verificar si el formulario es válido
    print(f"\nFormulario válido: {form.is_valid()}")
    if not form.is_valid():
        print(f"Errores: {form.errors}")

if __name__ == "__main__":
    test_form_debug()




#!/usr/bin/env python3
"""
Script para probar la herencia de RTM y EXPE en el formulario declaracion_volumen
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.forms import DeclaracionVolumenForm

def test_form_initialization():
    """Probar la inicialización del formulario con datos RTM y EXPE"""
    print("=== PRUEBA DE INICIALIZACIÓN DEL FORMULARIO ===")
    
    # Simular datos de prueba
    rtm = "123456"
    expe = "789012"
    idneg = 1
    
    # Crear datos iniciales
    initial_data = {
        'rtm': rtm,
        'expe': expe,
        'idneg': idneg
    }
    
    print(f"Datos iniciales: {initial_data}")
    
    # Crear formulario
    form = DeclaracionVolumenForm(initial=initial_data)
    
    # Forzar los valores en los campos del formulario
    form.fields['rtm'].initial = rtm
    form.fields['rtm'].widget.attrs['value'] = rtm
    form.fields['expe'].initial = expe
    form.fields['expe'].widget.attrs['value'] = expe
    
    # Verificar valores
    print(f"Form RTM value: {form['rtm'].value()}")
    print(f"Form EXPE value: {form['expe'].value()}")
    print(f"Form IDNEG value: {form['idneg'].value()}")
    
    # Verificar si los campos están readonly
    print(f"RTM readonly: {form.fields['rtm'].widget.attrs.get('readonly', False)}")
    print(f"EXPE readonly: {form.fields['expe'].widget.attrs.get('readonly', False)}")
    
    # Renderizar el HTML de los campos
    print("\n=== HTML DE LOS CAMPOS ===")
    print("RTM HTML:")
    print(form['rtm'].as_widget())
    print("\nEXPE HTML:")
    print(form['expe'].as_widget())
    print("\nIDNEG HTML:")
    print(form['idneg'].as_widget())
    
    return form

def test_form_validation():
    """Probar la validación del formulario"""
    print("\n=== PRUEBA DE VALIDACIÓN ===")
    
    # Crear formulario con datos completos
    form_data = {
        'rtm': '123456',
        'expe': '789012',
        'idneg': 1,
        'ano': 2024,
        'tipo': 1,
        'mes': 1,
        'ventai': '1000.00',
        'ventac': '2000.00',
        'ventas': '3000.00',
        'valorexcento': '0.00',
        'controlado': '0.00',
        'unidad': '0.00',
        'factor': '0.00',
        'multadecla': '0.00',
        'impuesto': '0.00',
        'ajuste': '0.00'
    }
    
    form = DeclaracionVolumenForm(data=form_data)
    
    print(f"Formulario válido: {form.is_valid()}")
    if not form.is_valid():
        print(f"Errores: {form.errors}")
    else:
        print("Formulario válido - se puede guardar")

if __name__ == "__main__":
    try:
        form = test_form_initialization()
        test_form_validation()
        print("\n✅ Pruebas completadas exitosamente")
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()




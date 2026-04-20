#!/usr/bin/env python
"""
Script para probar el formulario DeclaracionVolumenForm y verificar que el campo valor_base se renderiza correctamente
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from tributario_app.forms import DeclaracionVolumenForm
from tributario.models import DeclaracionVolumen

def test_formulario_valor_base():
    print("="*80)
    print("PROBANDO FORMULARIO DECLARACION VOLUMEN - CAMPO VALOR_BASE")
    print("="*80)
    
    # Crear un formulario vacío
    print("\n1. Creando formulario vacío...")
    form = DeclaracionVolumenForm()
    
    # Verificar que el campo valor_base existe
    if 'valor_base' in form.fields:
        print("✅ Campo 'valor_base' encontrado en el formulario")
        campo = form.fields['valor_base']
        print(f"   - Tipo: {type(campo).__name__}")
        print(f"   - Label: {campo.label}")
        print(f"   - Required: {campo.required}")
        print(f"   - Widget ID: {campo.widget.attrs.get('id', 'No definido')}")
    else:
        print("❌ Campo 'valor_base' NO encontrado en el formulario")
        print("   Campos disponibles:", list(form.fields.keys()))
        return False
    
    # Probar con datos de ejemplo
    print("\n2. Probando con datos de ejemplo...")
    datos_ejemplo = {
        'idneg': '0301',
        'rtm': '114-03-23',
        'expe': '1151',
        'ano': 2024,
        'mes': 12,
        'tipo': 1,
        'ventai': 5000000,
        'ventac': 5000000,
        'ventas': 5000000,
        'valorexcento': 0,
        'controlado': 31000000,
        'unidad': 'LITROS',
        'factor': 1.0,
        'multadecla': 0,
        'impuesto': 0,
        'ajuste': 0
    }
    
    form_con_datos = DeclaracionVolumenForm(datos_ejemplo)
    
    if form_con_datos.is_valid():
        print("✅ Formulario es válido")
        valor_base = form_con_datos.cleaned_data.get('valor_base', 0)
        print(f"   - Valor Base calculado: {valor_base:,.2f}")
    else:
        print("❌ Formulario NO es válido")
        print("   Errores:", form_con_datos.errors)
    
    # Probar renderizado del campo
    print("\n3. Probando renderizado del campo...")
    try:
        html_campo = str(form['valor_base'])
        print("✅ Campo se renderiza correctamente")
        print(f"   - HTML generado: {html_campo[:100]}...")
        
        # Verificar que contiene el ID correcto
        if 'id_valor_base' in html_campo:
            print("✅ ID 'id_valor_base' encontrado en el HTML")
        else:
            print("❌ ID 'id_valor_base' NO encontrado en el HTML")
            print(f"   HTML completo: {html_campo}")
    except Exception as e:
        print(f"❌ Error al renderizar campo: {e}")
    
    print("\n" + "="*80)
    print("PRUEBA COMPLETADA")
    print("="*80)
    
    return True

if __name__ == "__main__":
    test_formulario_valor_base()

#!/usr/bin/env python
"""
Script para probar la inicialización del formulario con valor_base
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

def test_formulario_valor_base_final():
    print("="*80)
    print("PROBANDO INICIALIZACIÓN DEL FORMULARIO CON VALOR_BASE")
    print("="*80)
    
    try:
        # Buscar la declaración existente
        declaracion = DeclaracionVolumen.objects.filter(
            empresa='0301',
            rtm='114-03-23',
            expe='1151',
            ano=2025
        ).first()
        
        if declaracion:
            print(f"1. Declaración encontrada: {declaracion}")
            print(f"   - valor_base del modelo: {declaracion.valor_base}")
            
            # Crear formulario con la instancia
            print(f"\n2. Creando formulario con instancia...")
            form = DeclaracionVolumenForm(instance=declaracion)
            
            print(f"   - Formulario válido: {form.is_valid()}")
            print(f"   - Initial data: {form.initial}")
            
            # Verificar el valor_base en initial
            if 'valor_base' in form.initial:
                print(f"   - valor_base en initial: {form.initial['valor_base']}")
            else:
                print(f"   - ❌ valor_base NO está en initial")
            
            # Renderizar el campo valor_base
            print(f"\n3. Renderizando campo valor_base...")
            try:
                html_campo = str(form['valor_base'])
                print(f"   - HTML del campo: {html_campo}")
                
                # Extraer el valor del campo
                import re
                value_match = re.search(r'value="([^"]*)"', html_campo)
                if value_match:
                    valor_campo = value_match.group(1)
                    print(f"   - Valor en el campo: {valor_campo}")
                    
                    try:
                        valor_num = float(valor_campo.replace(',', '').replace(' ', '').strip())
                        if abs(valor_num - float(declaracion.valor_base)) < 0.01:
                            print(f"   - ✅ CORRECTO: El valor coincide con el modelo")
                        else:
                            print(f"   - ❌ ERROR: El valor NO coincide con el modelo")
                            print(f"     - Diferencia: {abs(valor_num - float(declaracion.valor_base)):,.2f}")
                    except ValueError:
                        print(f"   - ❌ ERROR: No se pudo convertir el valor a número")
                else:
                    print(f"   - ❌ No se pudo extraer el valor del campo")
                    
            except Exception as e:
                print(f"   - ❌ Error al renderizar campo: {e}")
            
        else:
            print("❌ No se encontró la declaración")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    test_formulario_valor_base_final()































#!/usr/bin/env python
"""
Script para verificar la propiedad valor_base del modelo
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from tributario.models import DeclaracionVolumen

def test_modelo_valor_base():
    print("="*80)
    print("VERIFICANDO PROPIEDAD VALOR_BASE DEL MODELO")
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
            print(f"   - ID: {declaracion.id}")
            print(f"   - Nodecla: {declaracion.nodecla}")
            
            print(f"\n2. Valores de campos de ventas:")
            print(f"   - ventai: {declaracion.ventai} (tipo: {type(declaracion.ventai)})")
            print(f"   - ventac: {declaracion.ventac} (tipo: {type(declaracion.ventac)})")
            print(f"   - ventas: {declaracion.ventas} (tipo: {type(declaracion.ventas)})")
            print(f"   - valorexcento: {declaracion.valorexcento} (tipo: {type(declaracion.valorexcento)})")
            print(f"   - controlado: {declaracion.controlado} (tipo: {type(declaracion.controlado)})")
            
            print(f"\n3. Cálculo manual:")
            suma_manual = (
                float(declaracion.ventai or 0) +
                float(declaracion.ventac or 0) +
                float(declaracion.ventas or 0) +
                float(declaracion.valorexcento or 0) +
                float(declaracion.controlado or 0)
            )
            print(f"   - Suma manual: {suma_manual:,.2f}")
            
            print(f"\n4. Propiedad valor_base:")
            valor_base_propiedad = declaracion.valor_base
            print(f"   - valor_base: {valor_base_propiedad} (tipo: {type(valor_base_propiedad)})")
            
            print(f"\n5. Verificación:")
            if abs(suma_manual - float(valor_base_propiedad)) < 0.01:
                print(f"   - ✅ CORRECTO: La propiedad calcula correctamente")
            else:
                print(f"   - ❌ ERROR: La propiedad no calcula correctamente")
                print(f"     - Diferencia: {abs(suma_manual - float(valor_base_propiedad))}")
            
        else:
            print("❌ No se encontró la declaración")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    test_modelo_valor_base()































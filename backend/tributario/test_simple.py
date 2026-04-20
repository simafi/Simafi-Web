#!/usr/bin/env python
"""
Testeo simple para verificar datos
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla, PlanArbitrio

def test_simple():
    print("🧪 TESTEO SIMPLE")
    print("=" * 40)
    
    # Verificar tasasdecla
    print("1. TASASDECLA:")
    try:
        tasas = TasasDecla.objects.all()[:5]
        print(f"   Total registros: {TasasDecla.objects.count()}")
        for tasa in tasas:
            print(f"   - ID: {tasa.id}, RTM: {tasa.rtm}, Rubro: {tasa.rubro}, Tipota: '{tasa.tipota}'")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print()
    
    # Verificar planarbitio
    print("2. PLANARBITIO:")
    try:
        planes = PlanArbitrio.objects.all()[:5]
        print(f"   Total registros: {PlanArbitrio.objects.count()}")
        for plan in planes:
            print(f"   - ID: {plan.id}, Empresa: {plan.empresa}, Rubro: {plan.rubro}, Código: {plan.codigo}")
    except Exception as e:
        print(f"   ERROR: {e}")

if __name__ == "__main__":
    test_simple()










































#!/usr/bin/env python
"""
Verificación simple de datos
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def verificar_datos():
    print("🔍 VERIFICACIÓN DE DATOS")
    print("=" * 40)
    
    try:
        from tributario.models import TasasDecla, PlanArbitrio
        
        # Verificar tasasdecla
        print("1. TASASDECLA:")
        total_tasas = TasasDecla.objects.count()
        print(f"   Total registros: {total_tasas}")
        
        if total_tasas > 0:
            # Verificar tipota
            tasas_v = TasasDecla.objects.filter(tipota='V').count()
            tasas_f = TasasDecla.objects.filter(tipota='F').count()
            tasas_vacias = TasasDecla.objects.filter(tipota='').count()
            
            print(f"   - Con tipota='V': {tasas_v}")
            print(f"   - Con tipota='F': {tasas_f}")
            print(f"   - Con tipota vacío: {tasas_vacias}")
            
            # Mostrar algunos ejemplos
            print("   Ejemplos:")
            for tasa in TasasDecla.objects.all()[:3]:
                print(f"      - ID: {tasa.id}, RTM: {tasa.rtm}, Rubro: {tasa.rubro}, Tipota: '{tasa.tipota}'")
        
        print()
        
        # Verificar planarbitio
        print("2. PLANARBITIO:")
        total_planes = PlanArbitrio.objects.count()
        print(f"   Total registros: {total_planes}")
        
        if total_planes > 0:
            print("   Ejemplos:")
            for plan in PlanArbitrio.objects.all()[:3]:
                print(f"      - ID: {plan.id}, Empresa: {plan.empresa}, Rubro: {plan.rubro}")
                print(f"        Código: {plan.codigo}, Mínimo: {plan.minimo}, Máximo: {plan.maximo}")
        
        print("\n✅ VERIFICACIÓN COMPLETADA")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_datos()










































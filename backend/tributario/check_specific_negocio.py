#!/usr/bin/env python
"""
Script para verificar registros específicos en tasasdecla para un negocio
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla

def check_specific_negocio():
    print("🔍 VERIFICANDO REGISTROS ESPECÍFICOS EN TASASDECLA")
    print("=" * 60)
    
    # Parámetros del negocio de la URL
    empresa = "0301"
    rtm = "114-03-23"
    expe = "1151"
    
    print(f"📋 Buscando registros para:")
    print(f"   - Empresa: {empresa}")
    print(f"   - RTM: {rtm}")
    print(f"   - Expediente: {expe}")
    print()
    
    try:
        # Buscar registros específicos
        tasas = TasasDecla.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe
        )
        
        print(f"📊 Registros encontrados: {tasas.count()}")
        
        if tasas.count() == 0:
            print("❌ NO HAY REGISTROS para este negocio específico")
            print("\n🔍 Verificando si hay registros con RTM similar...")
            
            # Buscar con RTM similar
            tasas_similar = TasasDecla.objects.filter(rtm__icontains="114-03-23")
            print(f"📊 Registros con RTM similar: {tasas_similar.count()}")
            
            if tasas_similar.count() > 0:
                print("   Registros encontrados:")
                for tasa in tasas_similar[:3]:
                    print(f"   - ID: {tasa.id}, RTM: {tasa.rtm}, Expe: {tasa.expe}, Empresa: {tasa.empresa}")
            
            print("\n🔍 Verificando si hay registros con expediente similar...")
            tasas_expe = TasasDecla.objects.filter(expe__icontains="1151")
            print(f"📊 Registros con expediente similar: {tasas_expe.count()}")
            
            if tasas_expe.count() > 0:
                print("   Registros encontrados:")
                for tasa in tasas_expe[:3]:
                    print(f"   - ID: {tasa.id}, RTM: {tasa.rtm}, Expe: {tasa.expe}, Empresa: {tasa.empresa}")
        else:
            print("✅ REGISTROS ENCONTRADOS:")
            for i, tasa in enumerate(tasas, 1):
                print(f"   {i}. ID: {tasa.id}")
                print(f"      RTM: {tasa.rtm}")
                print(f"      Expediente: {tasa.expe}")
                print(f"      Empresa: {tasa.empresa}")
                print(f"      Rubro: {tasa.rubro}")
                print(f"      Tipota: '{tasa.tipota}' (longitud: {len(str(tasa.tipota))})")
                print(f"      Valor: {tasa.valor}")
                print(f"      Frecuencia: {tasa.frecuencia}")
                print()
        
        # Verificar todos los registros en la tabla
        print("📊 ESTADÍSTICAS GENERALES:")
        total = TasasDecla.objects.count()
        print(f"   - Total registros en tasasdecla: {total}")
        
        if total > 0:
            # Mostrar algunos registros de muestra
            print("\n📋 PRIMEROS 3 REGISTROS DE LA TABLA:")
            muestras = TasasDecla.objects.all()[:3]
            for i, tasa in enumerate(muestras, 1):
                print(f"   {i}. ID: {tasa.id}")
                print(f"      RTM: {tasa.rtm}")
                print(f"      Expediente: {tasa.expe}")
                print(f"      Empresa: {tasa.empresa}")
                print(f"      Tipota: '{tasa.tipota}'")
                print()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_specific_negocio()










































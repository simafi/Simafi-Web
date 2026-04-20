#!/usr/bin/env python
"""
Testeo real de la lógica de tasas variables
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla, PlanArbitrio
from decimal import Decimal

def test_tasas_variables_real():
    print("🧪 TESTEO REAL DE TASAS VARIABLES")
    print("=" * 60)
    
    # Parámetros reales del negocio
    empresa = "0301"
    rtm = "114-03-23"
    expe = "1151"
    ano = 2025
    
    # Valores de ventas simulados (como los que vendrían del formulario)
    ventai = Decimal('1000000.00')
    ventac = Decimal('500000.00')
    ventas = Decimal('2000000.00')
    valorexcento = Decimal('0.00')
    controlado = Decimal('500000.00')
    
    # Calcular valor base total
    valor_base_total = ventai + ventac + ventas + valorexcento + controlado
    
    print(f"📊 PARÁMETROS DE PRUEBA:")
    print(f"   Empresa: {empresa}")
    print(f"   RTM: {rtm}")
    print(f"   Expediente: {expe}")
    print(f"   Año: {ano}")
    print(f"   Valor Base Total: {valor_base_total:,}")
    print()
    
    # 1. Buscar tasas con tipota = "V"
    print("1. BUSCANDO TASAS CON TIPOTA = 'V':")
    try:
        tasas_variables = TasasDecla.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe,
            ano=ano,
            tipota='V'
        )
        
        print(f"   📊 Tasas variables encontradas: {tasas_variables.count()}")
        
        if tasas_variables.count() == 0:
            print("   ⚠️ NO HAY TASAS CON TIPOTA = 'V'")
            print("   💡 Verificando si hay tasas con otros valores de tipota...")
            
            # Verificar todos los valores de tipota
            todas_las_tasas = TasasDecla.objects.filter(
                empresa=empresa,
                rtm=rtm,
                expe=expe,
                ano=ano
            )
            
            print(f"   📊 Total de tasas para este negocio: {todas_las_tasas.count()}")
            for tasa in todas_las_tasas:
                print(f"      - Rubro: {tasa.rubro}, Tipota: '{tasa.tipota}', Valor: {tasa.valor}")
            
            return
        
        # 2. Procesar cada tasa variable
        print("\n2. PROCESANDO TASAS VARIABLES:")
        for i, tasa_variable in enumerate(tasas_variables, 1):
            print(f"\n   🔍 Tasa {i}:")
            print(f"      - Rubro: {tasa_variable.rubro}")
            print(f"      - Código Tarifa: {tasa_variable.cod_tarifa}")
            print(f"      - Valor actual: {tasa_variable.valor}")
            
            # Buscar en planarbitio
            try:
                plan_arbitio = PlanArbitrio.objects.filter(
                    empresa=empresa,
                    rubro=tasa_variable.rubro,
                    cod_tarifa=tasa_variable.cod_tarifa,
                    ano=ano
                ).first()
                
                if plan_arbitio:
                    print(f"      ✅ Plan Arbitrio encontrado:")
                    print(f"         - Código: {plan_arbitio.codigo}")
                    print(f"         - Descripción: {plan_arbitio.descripcion}")
                    print(f"         - Mínimo: {plan_arbitio.minimo:,}")
                    print(f"         - Máximo: {plan_arbitio.maximo:,}")
                    print(f"         - Valor a aplicar: {plan_arbitio.valor:,}")
                    
                    # Validar rango
                    if plan_arbitio.minimo <= valor_base_total <= plan_arbitio.maximo:
                        print(f"      ✅ VALOR BASE EN RANGO:")
                        print(f"         - Valor base: {valor_base_total:,}")
                        print(f"         - Rango: {plan_arbitio.minimo:,} - {plan_arbitio.maximo:,}")
                        print(f"         - NUEVO VALOR: {plan_arbitio.valor:,}")
                        print(f"         - VALOR ANTERIOR: {tasa_variable.valor:,}")
                        
                        # Simular actualización (sin hacerla realmente)
                        print(f"      🔄 SIMULANDO ACTUALIZACIÓN...")
                        print(f"         - Se actualizaría el valor de {tasa_variable.valor:,} a {plan_arbitio.valor:,}")
                    else:
                        print(f"      ⚠️ VALOR BASE FUERA DE RANGO:")
                        print(f"         - Valor base: {valor_base_total:,}")
                        print(f"         - Rango: {plan_arbitio.minimo:,} - {plan_arbitio.maximo:,}")
                        print(f"         - NO SE ACTUALIZARÍA")
                else:
                    print(f"      ❌ NO SE ENCONTRÓ PLAN ARBITRIO")
                    print(f"         - Empresa: {empresa}")
                    print(f"         - Rubro: {tasa_variable.rubro}")
                    print(f"         - Código Tarifa: {tasa_variable.cod_tarifa}")
                    print(f"         - Año: {ano}")
                    
                    # Verificar si hay planes de arbitrio para este rubro
                    planes_rubro = PlanArbitrio.objects.filter(
                        empresa=empresa,
                        rubro=tasa_variable.rubro,
                        ano=ano
                    )
                    print(f"         - Planes disponibles para este rubro: {planes_rubro.count()}")
                    for plan in planes_rubro[:3]:
                        print(f"            * Código: {plan.codigo}, Tarifa: {plan.cod_tarifa}")
                    
            except Exception as e:
                print(f"      ❌ ERROR al procesar: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "="*60)
        print("✅ TESTEO COMPLETADO")
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tasas_variables_real()










































#!/usr/bin/env python
"""
Script de testeo para verificar la lógica de tasas variables
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla, PlanArbitrio

def test_tasas_variables():
    print("🧪 TESTEO DE TASAS VARIABLES")
    print("=" * 60)
    
    # Parámetros de prueba
    empresa = "0301"
    rtm = "114-03-23"
    expe = "1151"
    ano = 2025
    
    # Valor base simulado
    ventai = 1000000
    ventac = 500000
    ventas = 2000000
    valorexcento = 0
    controlado = 500000
    valor_base_total = ventai + ventac + ventas + valorexcento + controlado
    
    print(f"📊 PARÁMETROS DE PRUEBA:")
    print(f"   Empresa: {empresa}")
    print(f"   RTM: {rtm}")
    print(f"   Expediente: {expe}")
    print(f"   Año: {ano}")
    print(f"   Valor Base Total: {valor_base_total:,}")
    print()
    
    # 1. Verificar si existen tasas con tipota = "V"
    print("1. VERIFICANDO TASAS CON TIPOTA = 'V':")
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
            print("   💡 Esto significa que no se ejecutará la lógica de cálculo")
            return
        
        for i, tasa in enumerate(tasas_variables, 1):
            print(f"   {i}. Rubro: {tasa.rubro}, Código Tarifa: {tasa.cod_tarifa}, Valor actual: {tasa.valor}")
        
    except Exception as e:
        print(f"   ❌ ERROR al buscar tasas variables: {e}")
        return
    
    print()
    
    # 2. Verificar si existen registros en planarbitio
    print("2. VERIFICANDO REGISTROS EN PLANARBITIO:")
    try:
        planes_arbitrio = PlanArbitrio.objects.filter(empresa=empresa, ano=ano)
        print(f"   📊 Planes de arbitrio encontrados: {planes_arbitrio.count()}")
        
        if planes_arbitrio.count() == 0:
            print("   ⚠️ NO HAY REGISTROS EN PLANARBITIO")
            print("   💡 Esto significa que no se podrán calcular las tasas variables")
            return
        
        for i, plan in enumerate(planes_arbitrio[:5], 1):  # Mostrar solo los primeros 5
            print(f"   {i}. Empresa: {plan.empresa}, Rubro: {plan.rubro}, Código: {plan.codigo}")
            print(f"      Tarifa: {plan.cod_tarifa}, Mínimo: {plan.minimo}, Máximo: {plan.maximo}, Valor: {plan.valor}")
        
        if planes_arbitrio.count() > 5:
            print(f"   ... y {planes_arbitrio.count() - 5} registros más")
        
    except Exception as e:
        print(f"   ❌ ERROR al buscar planes de arbitrio: {e}")
        return
    
    print()
    
    # 3. Simular la lógica de cálculo
    print("3. SIMULANDO LÓGICA DE CÁLCULO:")
    for tasa_variable in tasas_variables:
        print(f"   🔍 Procesando tasa variable:")
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
                else:
                    print(f"      ⚠️ VALOR BASE FUERA DE RANGO:")
                    print(f"         - Valor base: {valor_base_total:,}")
                    print(f"         - Rango: {plan_arbitio.minimo:,} - {plan_arbitio.maximo:,}")
                    print(f"         - NO SE ACTUALIZARÁ")
            else:
                print(f"      ❌ NO SE ENCONTRÓ PLAN ARBITRIO")
                print(f"         - Empresa: {empresa}")
                print(f"         - Rubro: {tasa_variable.rubro}")
                print(f"         - Código Tarifa: {tasa_variable.cod_tarifa}")
                print(f"         - Año: {ano}")
                
        except Exception as e:
            print(f"      ❌ ERROR al procesar: {e}")
        
        print()
    
    print("=" * 60)
    print("✅ TESTEO COMPLETADO")

if __name__ == "__main__":
    test_tasas_variables()










































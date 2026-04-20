#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que el proceso de crear tasas desde tarifasics funcione
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simafiweb.settings')
django.setup()

from tributario_app.models import TarifasICS
from tributario.models import TasasDecla
from decimal import Decimal

def test_buscar_tarifasics(empresa='0301', rtm='114-03-23', expe='1151'):
    """Test para buscar tarifasics"""
    print("="*80)
    print("TEST: Buscar TarifasICS")
    print("="*80)
    
    print(f"Buscando: empresa={empresa}, rtm={rtm}, expe={expe}")
    
    tarifas_ics = TarifasICS.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe
    )
    
    print(f"TarifasICS encontradas: {tarifas_ics.count()}")
    
    if tarifas_ics.exists():
        print("\nDetalle de tarifasics encontradas:")
        for tarifa in tarifas_ics:
            print(f"  ID: {tarifa.id}")
            print(f"    Empresa: {tarifa.empresa}")
            print(f"    RTM: {tarifa.rtm}")
            print(f"    EXPE: {tarifa.expe}")
            print(f"    Rubro: {tarifa.rubro}")
            print(f"    Cod_Tarifa: {tarifa.cod_tarifa}")
            print(f"    Valor: {tarifa.valor}")
            print(f"    IDNeg: {tarifa.idneg}")
            print(f"    Cuenta: {tarifa.cuenta}")
            print(f"    CuentaRez: {tarifa.cuentarez}")
            print()
        return tarifas_ics
    else:
        print("⚠️ No se encontraron tarifasics")
        return None


def test_verificar_tasasdecla(empresa='0301', rtm='114-03-23', expe='1151', ano=2025):
    """Test para verificar tasas en tasasdecla"""
    print("="*80)
    print("TEST: Verificar TasasDecla existentes")
    print("="*80)
    
    ano_decimal = Decimal(str(ano))
    
    print(f"Buscando: empresa={empresa}, rtm={rtm}, expe={expe}, ano={ano}")
    
    tasas = TasasDecla.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        ano=ano_decimal
    )
    
    print(f"TasasDecla encontradas: {tasas.count()}")
    
    if tasas.exists():
        print("\nDetalle de tasas encontradas:")
        for tasa in tasas:
            print(f"  ID: {tasa.id}")
            print(f"    Rubro: {tasa.rubro}")
            print(f"    Cod_Tarifa: {tasa.cod_tarifa}")
            print(f"    Valor: {tasa.valor}")
            print(f"    IDNeg: {tasa.idneg}")
            print(f"    Nodecla: {tasa.nodecla}")
            print(f"    Tipo: {tasa.tipota}")
            print()
        return tasas
    else:
        print("⚠️ No se encontraron tasas en tasasdecla")
        return None


def test_comparar_tarifasics_vs_tasasdecla(empresa='0301', rtm='114-03-23', expe='1151', ano=2025):
    """Compara tarifasics con tasasdecla para ver qué falta"""
    print("="*80)
    print("TEST: Comparar TarifasICS vs TasasDecla")
    print("="*80)
    
    tarifas_ics = TarifasICS.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe
    )
    
    ano_decimal = Decimal(str(ano))
    tasas_decla = TasasDecla.objects.filter(
        empresa=empresa,
        rtm=rtm,
        expe=expe,
        ano=ano_decimal
    )
    
    rubros_ics = set()
    for tarifa in tarifas_ics:
        if tarifa.rubro and tarifa.rubro.strip():
            rubros_ics.add(tarifa.rubro.strip())
    
    rubros_decla = set()
    for tasa in tasas_decla:
        if tasa.rubro and tasa.rubro.strip():
            rubros_decla.add(tasa.rubro.strip())
    
    print(f"Rubros en TarifasICS: {len(rubros_ics)}")
    print(f"Rubros en TasasDecla: {len(rubros_decla)}")
    
    rubros_faltantes = rubros_ics - rubros_decla
    
    if rubros_faltantes:
        print(f"\n⚠️ Rubros que están en TarifasICS pero NO en TasasDecla: {len(rubros_faltantes)}")
        for rubro in sorted(rubros_faltantes):
            print(f"  - {rubro}")
    else:
        print("\n✅ Todos los rubros de TarifasICS están en TasasDecla")
    
    rubros_extra = rubros_decla - rubros_ics
    if rubros_extra:
        print(f"\n📝 Rubros que están en TasasDecla pero NO en TarifasICS: {len(rubros_extra)}")
        for rubro in sorted(rubros_extra):
            print(f"  - {rubro}")
    
    return rubros_faltantes


if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTEO DEL PROCESO DE CREACIÓN DE TASAS")
    print("="*80)
    print()
    
    # Valores de prueba (ajustar según necesidad)
    empresa = '0301'
    rtm = '114-03-23'
    expe = '1151'
    ano = 2025
    
    print(f"Parámetros de prueba:")
    print(f"  Empresa: {empresa}")
    print(f"  RTM: {rtm}")
    print(f"  EXPE: {expe}")
    print(f"  Año: {ano}")
    print()
    
    # Test 1: Buscar tarifasics
    tarifas_ics = test_buscar_tarifasics(empresa, rtm, expe)
    print()
    
    # Test 2: Verificar tasasdecla
    tasas_decla = test_verificar_tasasdecla(empresa, rtm, expe, ano)
    print()
    
    # Test 3: Comparar
    rubros_faltantes = test_comparar_tarifasics_vs_tasasdecla(empresa, rtm, expe, ano)
    print()
    
    print("="*80)
    print("RESUMEN")
    print("="*80)
    if tarifas_ics:
        print(f"✅ TarifasICS encontradas: {tarifas_ics.count()}")
    else:
        print("❌ No se encontraron TarifasICS - Este es el problema principal")
    
    if tasas_decla:
        print(f"✅ TasasDecla encontradas: {tasas_decla.count()}")
    else:
        print("⚠️ No se encontraron TasasDecla - Puede ser normal si no se ha guardado declaración")
    
    if rubros_faltantes:
        print(f"⚠️ Rubros faltantes en TasasDecla: {len(rubros_faltantes)}")
        print("   Estos rubros deberían crearse automáticamente al guardar la declaración")
    else:
        print("✅ Todos los rubros están en ambas tablas")
























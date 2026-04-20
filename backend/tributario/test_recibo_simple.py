#!/usr/bin/env python
"""
Script de prueba simple para diagnosticar generación de recibo
Se ejecuta con: python manage.py shell < test_recibo_simple.py
O directamente desde el shell de Django
"""
from django.db.models import Q
from tributario.models import TransaccionesIcs, TasasDecla, Actividad, Negocio, Rubro
from decimal import Decimal

# Parámetros de prueba - CAMBIAR SEGÚN NECESITE
EMPRESA = '0301'
RTM = '114-03-23'
EXPE = '1151'

print("\n" + "=" * 80)
print("🔍 TEST SIMPLE - GENERACIÓN DE RECIBO")
print("=" * 80)

# 1. Verificar negocio
print("\n1️⃣ Verificando negocio...")
negocio = Negocio.objects.filter(empresa=EMPRESA, rtm=RTM, expe=EXPE).first()
if negocio:
    print(f"   ✅ Negocio: {negocio.nombrenego}")
else:
    print(f"   ❌ Negocio NO encontrado")
    exit()

# 2. Verificar transacciones
print("\n2️⃣ Verificando transacciones pendientes...")
transacciones = TransaccionesIcs.objects.filter(
    empresa=EMPRESA,
    rtm=RTM,
    expe=EXPE,
    operacion='D',
    saldoact__gt=0
)
print(f"   ✅ Transacciones con saldoact > 0: {transacciones.count()}")

if transacciones.count() == 0:
    print("\n   ⚠️ Verificando todas las transacciones (sin filtro saldoact)...")
    todas = TransaccionesIcs.objects.filter(
        empresa=EMPRESA,
        rtm=RTM,
        expe=EXPE,
        operacion='D'
    )
    print(f"   Total transacciones operacion='D': {todas.count()}")
    if todas.exists():
        print("\n   Primeras 5 transacciones:")
        for t in todas[:5]:
            print(f"      Año: {t.ano}, Mes: {t.mes}, Rubro: {t.rubro}, SaldoAct: {t.saldoact}")

# 3. Verificar TasasDecla
print("\n3️⃣ Verificando vinculación con TasasDecla...")
if transacciones.exists():
    primera = transacciones.first()
    tasas = TasasDecla.objects.filter(
        empresa=EMPRESA,
        rtm=RTM,
        expe=EXPE,
        ano=int(float(primera.ano)),
        rubro=primera.rubro
    )
    print(f"   TasasDecla encontradas para primera transacción: {tasas.count()}")
    if tasas.exists():
        tasa = tasas.first()
        print(f"   ✅ Cuenta: {tasa.cuenta}")
        
        # Verificar Actividad
        actividad = Actividad.objects.filter(
            empresa=EMPRESA,
            codigo=tasa.cuenta
        ).first()
        if actividad:
            print(f"   ✅ Descripción: {actividad.descripcion}")
        else:
            print(f"   ⚠️ Descripción NO encontrada en Actividad")
    else:
        print(f"   ⚠️ NO se encontró cuenta en TasasDecla para rubro {primera.rubro}")

print("\n" + "=" * 80)
print("✅ TEST COMPLETADO")
print("=" * 80)




















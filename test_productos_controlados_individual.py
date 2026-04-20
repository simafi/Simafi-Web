#!/usr/bin/env python3
"""
Test específico para verificar el cálculo individual de Productos Controlados
"""

def test_productos_controlados_individual():
    print("🔍 TEST CÁLCULO INDIVIDUAL PRODUCTOS CONTROLADOS")
    print("=" * 60)
    
    # Escenario de prueba
    print("\n📊 ESCENARIO DE PRUEBA:")
    print("   • Productos Controlados: 500,000.00")
    print("   • Resultado esperado: L. 50.00")
    
    # Calcular impuesto individual
    controlado = 500000.0
    impuesto_controlado = calcular_impuesto_ics_controlados(controlado)
    
    print(f"\n💰 CÁLCULO INDIVIDUAL:")
    print(f"   Valor ingresado: L. {controlado:,.2f}")
    print(f"   Impuesto calculado: L. {impuesto_controlado:.2f}")
    
    # Verificar resultado
    print(f"\n✅ VERIFICACIÓN:")
    if impuesto_controlado == 50.0:
        print("   ✅ CORRECTO: El cálculo individual funciona")
    else:
        print(f"   ❌ INCORRECTO: Esperado L. 50.00, obtenido L. {impuesto_controlado:.2f}")
        print(f"   Diferencia: L. {impuesto_controlado - 50:.2f}")
    
    # Verificar tarifas
    print(f"\n🔍 VERIFICACIÓN DE TARIFAS:")
    print("   Rango aplicable: $0 - $1,000,000")
    print("   Tarifa: 0.1% (0.1/1000)")
    print(f"   Cálculo: {controlado:,.2f} ÷ 1000 × 0.1 = {controlado/1000 * 0.1:.2f}")
    
    # Test con diferentes valores
    print(f"\n🧪 TEST CON DIFERENTES VALORES:")
    valores_test = [100000, 500000, 1000000, 2000000, 6000000]
    
    for valor in valores_test:
        impuesto = calcular_impuesto_ics_controlados(valor)
        print(f"   L. {valor:,.2f} → L. {impuesto:.2f}")

def calcular_impuesto_ics_controlados(valor_ventas):
    """Calcular impuesto ICS controlados"""
    if not valor_ventas or valor_ventas <= 0:
        return 0
    
    # Tarifas ICS controlados
    tarifas = [
        {"rango1": 0.0, "rango2": 1000000.0, "valor": 0.1, "categoria": "2", "descripcion": "Controlados $0 - $1,000,000"},
        {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 0.05, "categoria": "2", "descripcion": "Controlados $1,000,000 - $5,000,000"},
        {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 0.1, "categoria": "2", "descripcion": "Controlados $5,000,000+"}
    ]
    
    impuesto_total = 0
    for tarifa in tarifas:
        if valor_ventas >= tarifa["rango1"] and valor_ventas <= tarifa["rango2"]:
            impuesto = (valor_ventas / 1000) * tarifa["valor"]
            impuesto_total += impuesto
            break
    
    return impuesto_total

if __name__ == "__main__":
    test_productos_controlados_individual()

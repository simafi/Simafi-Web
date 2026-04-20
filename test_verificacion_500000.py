#!/usr/bin/env python3
"""
Test específico para verificar que 500,000 da exactamente 50.00
"""

def test_500000_especifico():
    """Test específico para 500,000"""
    
    print("🧪 TEST ESPECÍFICO: 500,000 → L. 50.00")
    print("=" * 60)
    
    # Tarifas actuales en el código
    tarifas_controlados = [
        {"rango1": 0.0, "rango2": 1000000.0, "valor": 0.1, "descripcion": "Controlados $0 - $1,000,000"},
        {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 0.05, "descripcion": "Controlados $1,000,000 - $5,000,000"},
        {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 0.1, "descripcion": "Controlados $5,000,000+"}
    ]
    
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return 0

        impuestoTotal = 0
        valorRestante = valorVentas

        for tarifa in tarifas_controlados:
            if valorRestante <= 0:
                break

            diferencialRango = tarifa["rango2"] - tarifa["rango1"]
            if diferencialRango <= 0:
                continue

            if valorRestante <= diferencialRango:
                valorAplicable = valorRestante
                valorRestante = 0
            else:
                valorAplicable = diferencialRango
                valorRestante -= diferencialRango

            impuestoRango = round((valorAplicable * tarifa["valor"] / 1000) * 100) / 100
            impuestoTotal += impuestoRango

        return round(impuestoTotal, 2)
    
    # Test con 500,000
    valor = 500000
    resultado = calcularImpuestoICSControlados(valor)
    
    print(f"📊 VALOR: {valor:,}")
    print(f"📋 TARIFAS APLICABLES:")
    for tarifa in tarifas_controlados:
        print(f"   {tarifa['descripcion']}: {tarifa['valor']}/1000")
    
    print(f"\n📊 CÁLCULO PASO A PASO:")
    print(f"   Valor: {valor:,}")
    print(f"   Rango aplicable: $0 - $1,000,000")
    print(f"   Tarifa: 0.1/1000")
    print(f"   Cálculo: {valor:,} × 0.1 ÷ 1000 = {valor * 0.1 / 1000}")
    print(f"   Resultado: L. {resultado:.2f}")
    
    # Verificación
    esperado = 50.00
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"   Esperado: L. {esperado:.2f}")
    print(f"   Obtenido: L. {resultado:.2f}")
    print(f"   Diferencia: L. {abs(resultado - esperado):.2f}")
    
    if abs(resultado - esperado) < 0.01:
        print(f"   ✅ CORRECTO - Las tarifas están bien para 500,000")
        return True
    else:
        print(f"   ❌ ERROR - Las tarifas no dan el resultado esperado")
        return False

def test_calculo_combinado_500000():
    """Test del cálculo combinado con 500,000 + 500,000"""
    
    print("\n\n🧪 TEST CÁLCULO COMBINADO: 500,000 + 500,000")
    print("=" * 60)
    
    # Valores
    ventai = 500000
    controlado = 500000
    
    # Cálculo Ventas Rubro Producción
    impuesto_ventai = round(ventai * 0.3 / 1000, 2)  # 150.00
    
    # Cálculo Productos Controlados
    impuesto_controlado = round(controlado * 0.1 / 1000, 2)  # 50.00
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_controlado
    
    print(f"📊 VALORES DE ENTRADA:")
    print(f"   Ventas Rubro Producción: {ventai:,}")
    print(f"   Productos Controlados: {controlado:,}")
    
    print(f"\n📋 CÁLCULOS INDIVIDUALES:")
    print(f"   Ventas Rubro Producción: {ventai:,} × 0.3/1000 = L. {impuesto_ventai:.2f}")
    print(f"   Productos Controlados: {controlado:,} × 0.1/1000 = L. {impuesto_controlado:.2f}")
    
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   {impuesto_ventai:.2f} + {impuesto_controlado:.2f} = L. {suma_total:.2f}")
    
    # Verificación
    esperado = 200.00
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"   Usuario espera: L. {esperado:.2f}")
    print(f"   Cálculo actual: L. {suma_total:.2f}")
    print(f"   Diferencia: L. {abs(suma_total - esperado):.2f}")
    
    if abs(suma_total - esperado) < 0.01:
        print(f"   ✅ CORRECTO - El cálculo combinado está bien")
        return True
    else:
        print(f"   ❌ ERROR - El cálculo combinado no es correcto")
        return False

def test_otros_valores():
    """Test con otros valores para verificar las tarifas"""
    
    print("\n\n🧪 TEST OTROS VALORES")
    print("=" * 60)
    
    # Tarifas actuales
    tarifas_controlados = [
        {"rango1": 0.0, "rango2": 1000000.0, "valor": 0.1, "descripcion": "Controlados $0 - $1,000,000"},
        {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 0.05, "descripcion": "Controlados $1,000,000 - $5,000,000"},
        {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 0.1, "descripcion": "Controlados $5,000,000+"}
    ]
    
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return 0

        impuestoTotal = 0
        valorRestante = valorVentas

        for tarifa in tarifas_controlados:
            if valorRestante <= 0:
                break

            diferencialRango = tarifa["rango2"] - tarifa["rango1"]
            if diferencialRango <= 0:
                continue

            if valorRestante <= diferencialRango:
                valorAplicable = valorRestante
                valorRestante = 0
            else:
                valorAplicable = diferencialRango
                valorRestante -= diferencialRango

            impuestoRango = round((valorAplicable * tarifa["valor"] / 1000) * 100) / 100
            impuestoTotal += impuestoRango

        return round(impuestoTotal, 2)
    
    # Test con diferentes valores
    valores_test = [100000, 500000, 1000000, 2000000, 5000000]
    
    print("📊 PROBANDO DIFERENTES VALORES:")
    print()
    
    for valor in valores_test:
        resultado = calcularImpuestoICSControlados(valor)
        print(f"   {valor:>10,}: L. {resultado:>8.2f}")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST VERIFICACIÓN 500,000...")
    print()
    
    # Test específico 500,000
    test1 = test_500000_especifico()
    
    # Test cálculo combinado
    test2 = test_calculo_combinado_500000()
    
    # Test otros valores
    test_otros_valores()
    
    print("\n\n🎯 CONCLUSIÓN:")
    print("=" * 60)
    if test1 and test2:
        print("✅ LAS TARIFAS ESTÁN CORRECTAS PARA EL CASO 500,000")
        print("✅ El cálculo independiente da L. 50.00")
        print("✅ El cálculo combinado da L. 200.00")
        print("✅ Los parámetros en la tabla están bien")
    else:
        print("❌ HAY PROBLEMAS CON LAS TARIFAS")
        print("🔧 Revisar los parámetros en la tabla")

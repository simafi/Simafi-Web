#!/usr/bin/env python3
"""
Test detallado para identificar la falla en Productos Controlados
"""

def test_calculo_individual_controlados():
    """Test del cálculo individual de Productos Controlados"""
    
    print("🧪 TEST CÁLCULO INDIVIDUAL - PRODUCTOS CONTROLADOS")
    print("=" * 60)
    
    # Valores de entrada
    valor_controlado = 500000
    
    print(f"📊 VALOR DE ENTRADA: {valor_controlado:,}")
    
    # Simular las tarifas para productos controlados del formulario
    tarifas_controlados = [
        {"rango1": 0.0, "rango2": 1000000.0, "valor": 1.0, "descripcion": "Controlados $0 - $1,000,000"},
        {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 1.5, "descripcion": "Controlados $1,000,000 - $5,000,000"},
        {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 2.0, "descripcion": "Controlados $5,000,000+"}
    ]
    
    print(f"\n📋 TARIFAS APLICABLES:")
    for tarifa in tarifas_controlados:
        print(f"   {tarifa['descripcion']}: {tarifa['valor']}/1000")
    
    # Cálculo paso a paso
    if valor_controlado <= 0:
        impuesto = 0
        print(f"\n❌ Valor inválido: {valor_controlado}")
    else:
        # Aplicar tarifa del primer rango (0 - 1,000,000)
        if valor_controlado <= 1000000:
            tarifa_aplicable = 1.0
            impuesto = valor_controlado * tarifa_aplicable / 1000
            print(f"\n📊 CÁLCULO PASO A PASO:")
            print(f"   Valor: {valor_controlado:,}")
            print(f"   Rango: $0 - $1,000,000")
            print(f"   Tarifa: {tarifa_aplicable}/1000")
            print(f"   Cálculo: {valor_controlado:,} × {tarifa_aplicable} ÷ 1000")
            print(f"   Resultado: {impuesto}")
            print(f"   Redondeado: {round(impuesto, 2)}")
    
    resultado = round(impuesto, 2)
    print(f"\n💰 RESULTADO INDIVIDUAL: L. {resultado:.2f}")
    
    # Verificación con lo que espera el usuario
    esperado_usuario = 50.00
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"   Usuario espera: L. {esperado_usuario:.2f}")
    print(f"   Cálculo actual: L. {resultado:.2f}")
    print(f"   Diferencia: L. {abs(resultado - esperado_usuario):.2f}")
    
    if abs(resultado - esperado_usuario) < 0.01:
        print(f"   ✅ CORRECTO")
    else:
        print(f"   ❌ ERROR - Las tarifas no coinciden con lo esperado")
        print(f"   💡 Para obtener 50.00, la tarifa debería ser: {esperado_usuario * 1000 / valor_controlado:.4f}/1000")
    
    return resultado

def test_calculo_combinado():
    """Test del cálculo combinado"""
    
    print("\n\n🧪 TEST CÁLCULO COMBINADO")
    print("=" * 60)
    
    # Valores de entrada
    ventai = 500000
    controlado = 500000
    
    print(f"📊 VALORES DE ENTRADA:")
    print(f"   Ventas Rubro Producción: {ventai:,}")
    print(f"   Productos Controlados: {controlado:,}")
    
    # Cálculo individual de Ventas Rubro Producción
    impuesto_ventai = ventai * 0.3 / 1000  # 150.00
    print(f"\n📋 VENTAS RUBRO PRODUCCIÓN:")
    print(f"   Cálculo: {ventai:,} × 0.3 ÷ 1000 = {impuesto_ventai}")
    print(f"   Resultado: L. {round(impuesto_ventai, 2):.2f}")
    
    # Cálculo individual de Productos Controlados
    impuesto_controlado = controlado * 1.0 / 1000  # 500.00
    print(f"\n📋 PRODUCTOS CONTROLADOS:")
    print(f"   Cálculo: {controlado:,} × 1.0 ÷ 1000 = {impuesto_controlado}")
    print(f"   Resultado: L. {round(impuesto_controlado, 2):.2f}")
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_controlado
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   {round(impuesto_ventai, 2):.2f} + {round(impuesto_controlado, 2):.2f} = L. {round(suma_total, 2):.2f}")
    
    # Verificación con lo que espera el usuario
    esperado_usuario = 200.00  # 150 + 50
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"   Usuario espera: L. {esperado_usuario:.2f}")
    print(f"   Cálculo actual: L. {round(suma_total, 2):.2f}")
    print(f"   Diferencia: L. {abs(round(suma_total, 2) - esperado_usuario):.2f}")
    
    if abs(round(suma_total, 2) - esperado_usuario) < 0.01:
        print(f"   ✅ CORRECTO")
    else:
        print(f"   ❌ ERROR")
    
    return round(suma_total, 2)

def analizar_tarifas_correctas():
    """Analizar qué tarifas deberían usarse para obtener los resultados esperados"""
    
    print("\n\n🔍 ANÁLISIS DE TARIFAS CORRECTAS")
    print("=" * 60)
    
    valor_controlado = 500000
    resultado_esperado = 50.00
    
    print(f"📊 DATOS:")
    print(f"   Valor: {valor_controlado:,}")
    print(f"   Resultado esperado: L. {resultado_esperado:.2f}")
    
    # Calcular tarifa necesaria
    tarifa_necesaria = resultado_esperado * 1000 / valor_controlado
    print(f"\n🧮 CÁLCULO DE TARIFA NECESARIA:")
    print(f"   Tarifa = Resultado × 1000 ÷ Valor")
    print(f"   Tarifa = {resultado_esperado} × 1000 ÷ {valor_controlado}")
    print(f"   Tarifa = {tarifa_necesaria:.4f}/1000")
    
    # Verificar con la tarifa calculada
    verificacion = valor_controlado * tarifa_necesaria / 1000
    print(f"\n✅ VERIFICACIÓN:")
    print(f"   {valor_controlado:,} × {tarifa_necesaria:.4f} ÷ 1000 = {verificacion:.2f}")
    
    if abs(verificacion - resultado_esperado) < 0.01:
        print(f"   ✅ CORRECTO - La tarifa debería ser {tarifa_necesaria:.4f}/1000")
    else:
        print(f"   ❌ ERROR en el cálculo")

def test_tarifas_alternativas():
    """Test con diferentes tarifas para encontrar la correcta"""
    
    print("\n\n🧪 TEST TARIFAS ALTERNATIVAS")
    print("=" * 60)
    
    valor_controlado = 500000
    resultado_esperado = 50.00
    
    # Probar diferentes tarifas
    tarifas_prueba = [
        0.1,   # 0.1/1000
        0.2,   # 0.2/1000
        0.3,   # 0.3/1000
        0.4,   # 0.4/1000
        0.5,   # 0.5/1000
        1.0,   # 1.0/1000 (actual)
    ]
    
    print(f"📊 PROBANDO DIFERENTES TARIFAS PARA {valor_controlado:,}:")
    print(f"   Resultado esperado: L. {resultado_esperado:.2f}")
    print()
    
    for tarifa in tarifas_prueba:
        resultado = valor_controlado * tarifa / 1000
        diferencia = abs(resultado - resultado_esperado)
        print(f"   Tarifa {tarifa:4.1f}/1000 → L. {resultado:6.2f} (diferencia: {diferencia:6.2f})")
    
    # Encontrar la tarifa más cercana
    mejor_tarifa = min(tarifas_prueba, key=lambda t: abs(valor_controlado * t / 1000 - resultado_esperado))
    mejor_resultado = valor_controlado * mejor_tarifa / 1000
    mejor_diferencia = abs(mejor_resultado - resultado_esperado)
    
    print(f"\n🎯 MEJOR TARIFA:")
    print(f"   Tarifa: {mejor_tarifa}/1000")
    print(f"   Resultado: L. {mejor_resultado:.2f}")
    print(f"   Diferencia: L. {mejor_diferencia:.2f}")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST DETALLADO DE PRODUCTOS CONTROLADOS...")
    print()
    
    # Test individual
    resultado_individual = test_calculo_individual_controlados()
    
    # Test combinado
    resultado_combinado = test_calculo_combinado()
    
    # Análisis de tarifas
    analizar_tarifas_correctas()
    
    # Test tarifas alternativas
    test_tarifas_alternativas()
    
    print("\n\n🎯 CONCLUSIÓN:")
    print("=" * 60)
    print("El problema está en las tarifas de Productos Controlados.")
    print("Para obtener L. 50.00 con 500,000, la tarifa debería ser 0.1/1000, no 1.0/1000.")
    print("Esto explica por qué el usuario espera 200.00 (150 + 50) pero obtiene 650.00 (150 + 500).")

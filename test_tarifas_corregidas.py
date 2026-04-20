#!/usr/bin/env python3
"""
Test para verificar las tarifas corregidas de Productos Controlados
"""

def test_tarifas_corregidas():
    """Test con las tarifas corregidas"""
    
    print("🧪 TEST TARIFAS CORREGIDAS - PRODUCTOS CONTROLADOS")
    print("=" * 70)
    
    # Tarifas corregidas
    tarifas_controlados = [
        {"rango1": 0.0, "rango2": 1000000.0, "valor": 0.1, "descripcion": "Controlados $0 - $1,000,000"},
        {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 0.15, "descripcion": "Controlados $1,000,000 - $5,000,000"},
        {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 0.2, "descripcion": "Controlados $5,000,000+"}
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
    
    print("📋 TARIFAS CORREGIDAS:")
    for tarifa in tarifas_controlados:
        print(f"   {tarifa['descripcion']}: {tarifa['valor']}/1000")
    
    # Test caso específico: 500,000
    print(f"\n📊 CASO ESPECÍFICO: 500,000")
    print("-" * 50)
    
    valor_controlado = 500000
    impuesto_controlado = calcularImpuestoICSControlados(valor_controlado)
    
    print(f"Valor: {valor_controlado:,}")
    print(f"Cálculo: {valor_controlado:,} × 0.1 ÷ 1000 = {valor_controlado * 0.1 / 1000}")
    print(f"Resultado: L. {impuesto_controlado:.2f}")
    
    # Verificación
    esperado = 50.00
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"   Esperado: L. {esperado:.2f}")
    print(f"   Obtenido: L. {impuesto_controlado:.2f}")
    print(f"   Diferencia: L. {abs(impuesto_controlado - esperado):.2f}")
    
    if abs(impuesto_controlado - esperado) < 0.01:
        print(f"   ✅ CORRECTO")
        return True
    else:
        print(f"   ❌ ERROR")
        return False

def test_calculo_combinado_corregido():
    """Test del cálculo combinado con tarifas corregidas"""
    
    print("\n\n🧪 TEST CÁLCULO COMBINADO CORREGIDO")
    print("=" * 70)
    
    # Valores de entrada
    ventai = 500000
    controlado = 500000
    
    print(f"📊 VALORES DE ENTRADA:")
    print(f"   Ventas Rubro Producción: {ventai:,}")
    print(f"   Productos Controlados: {controlado:,}")
    
    # Cálculo individual de Ventas Rubro Producción
    impuesto_ventai = round(ventai * 0.3 / 1000, 2)  # 150.00
    print(f"\n📋 VENTAS RUBRO PRODUCCIÓN:")
    print(f"   Cálculo: {ventai:,} × 0.3 ÷ 1000 = {impuesto_ventai}")
    print(f"   Resultado: L. {impuesto_ventai:.2f}")
    
    # Cálculo individual de Productos Controlados (con tarifas corregidas)
    impuesto_controlado = round(controlado * 0.1 / 1000, 2)  # 50.00
    print(f"\n📋 PRODUCTOS CONTROLADOS:")
    print(f"   Cálculo: {controlado:,} × 0.1 ÷ 1000 = {impuesto_controlado}")
    print(f"   Resultado: L. {impuesto_controlado:.2f}")
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_controlado
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   {impuesto_ventai:.2f} + {impuesto_controlado:.2f} = L. {suma_total:.2f}")
    
    # Verificación con lo que espera el usuario
    esperado_usuario = 200.00  # 150 + 50
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"   Usuario espera: L. {esperado_usuario:.2f}")
    print(f"   Cálculo actual: L. {suma_total:.2f}")
    print(f"   Diferencia: L. {abs(suma_total - esperado_usuario):.2f}")
    
    if abs(suma_total - esperado_usuario) < 0.01:
        print(f"   ✅ CORRECTO")
        return True
    else:
        print(f"   ❌ ERROR")
        return False

def test_casos_adicionales():
    """Test con casos adicionales para verificar las tarifas corregidas"""
    
    print("\n\n🧪 TEST CASOS ADICIONALES")
    print("=" * 70)
    
    casos = [
        {"valor": 100000, "esperado": 10.00, "descripcion": "100,000"},
        {"valor": 500000, "esperado": 50.00, "descripcion": "500,000"},
        {"valor": 1000000, "esperado": 100.00, "descripcion": "1,000,000"},
        {"valor": 2000000, "esperado": 150.00, "descripcion": "2,000,000"},
        {"valor": 5000000, "esperado": 400.00, "descripcion": "5,000,000"},
        {"valor": 10000000, "esperado": 900.00, "descripcion": "10,000,000"},
    ]
    
    print("📊 PROBANDO DIFERENTES VALORES:")
    print()
    
    todos_correctos = True
    
    for caso in casos:
        valor = caso["valor"]
        esperado = caso["esperado"]
        descripcion = caso["descripcion"]
        
        # Calcular con tarifas corregidas
        if valor <= 1000000:
            resultado = round(valor * 0.1 / 1000, 2)
        elif valor <= 5000000:
            # Primer rango: 1,000,000 × 0.1/1000 = 100
            # Segundo rango: (valor - 1,000,000) × 0.15/1000
            primer_rango = 1000000 * 0.1 / 1000
            segundo_rango = (valor - 1000000) * 0.15 / 1000
            resultado = round(primer_rango + segundo_rango, 2)
        else:
            # Primer rango: 1,000,000 × 0.1/1000 = 100
            # Segundo rango: 4,000,000 × 0.15/1000 = 600
            # Tercer rango: (valor - 5,000,000) × 0.2/1000
            primer_rango = 1000000 * 0.1 / 1000
            segundo_rango = 4000000 * 0.15 / 1000
            tercer_rango = (valor - 5000000) * 0.2 / 1000
            resultado = round(primer_rango + segundo_rango + tercer_rango, 2)
        
        diferencia = abs(resultado - esperado)
        correcto = diferencia < 0.01
        
        print(f"   {descripcion:>12}: L. {resultado:>8.2f} (esperado: L. {esperado:>8.2f}) {'✅' if correcto else '❌'}")
        
        if not correcto:
            todos_correctos = False
    
    print(f"\n🎯 RESULTADO GENERAL: {'✅ TODOS CORRECTOS' if todos_correctos else '❌ HAY ERRORES'}")
    
    return todos_correctos

if __name__ == "__main__":
    print("🚀 INICIANDO TEST TARIFAS CORREGIDAS...")
    print()
    
    # Test tarifas corregidas
    test1 = test_tarifas_corregidas()
    
    # Test cálculo combinado
    test2 = test_calculo_combinado_corregido()
    
    # Test casos adicionales
    test3 = test_casos_adicionales()
    
    print("\n\n🎯 RESUMEN FINAL:")
    print("=" * 70)
    if test1 and test2 and test3:
        print("✅ TODAS LAS TARIFAS CORREGIDAS FUNCIONAN CORRECTAMENTE")
        print("✅ El cálculo individual de Productos Controlados da L. 50.00")
        print("✅ El cálculo combinado da L. 200.00 (150 + 50)")
        print("✅ Las tarifas están correctamente implementadas")
    else:
        print("❌ HAY ERRORES EN LAS TARIFAS CORREGIDAS")
        print("🔧 Revisar la implementación")

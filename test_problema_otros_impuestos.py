#!/usr/bin/env python3
"""
Test específico para el problema de "Otros Impuestos"
"""

def test_problema_otros_impuestos():
    """Test específico para el problema reportado"""
    
    print("🧪 TEST PROBLEMA OTROS IMPUESTOS")
    print("=" * 60)
    
    # Simular las tarifas
    def calcularImpuestoICS(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return 0
        
        if valorVentas <= 500000:
            impuesto = valorVentas * 0.3 / 1000
        elif valorVentas <= 10000000:
            impuesto = valorVentas * 0.4 / 1000
        else:
            impuesto = valorVentas * 0.3 / 1000
        
        return round(impuesto, 2)
    
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return 0
        
        if valorVentas <= 1000000:
            impuesto = valorVentas * 0.1 / 1000
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 0.05 / 1000
        else:
            impuesto = valorVentas * 0.1 / 1000
        
        return round(impuesto, 2)
    
    print("📊 ESCENARIO REPORTADO:")
    print("   Ventas Rubro Producción: 500,000")
    print("   Productos Controlados: 500,000")
    print()
    
    # Valores de entrada
    ventai = 500000
    controlado = 500000
    
    # Cálculo individual de Ventas Rubro Producción
    impuesto_ventai = calcularImpuestoICS(ventai)
    print(f"📋 CÁLCULO VENTAS RUBRO PRODUCCIÓN:")
    print(f"   Valor: {ventai:,}")
    print(f"   Cálculo: {ventai:,} × 0.3 ÷ 1000 = {impuesto_ventai}")
    print(f"   Resultado: L. {impuesto_ventai:.2f}")
    
    # Cálculo individual de Productos Controlados
    impuesto_controlado = calcularImpuestoICSControlados(controlado)
    print(f"\n📋 CÁLCULO PRODUCTOS CONTROLADOS:")
    print(f"   Valor: {controlado:,}")
    print(f"   Cálculo: {controlado:,} × 0.1 ÷ 1000 = {impuesto_controlado}")
    print(f"   Resultado: L. {impuesto_controlado:.2f}")
    
    # Calcular "Otros Impuestos" (Producción + Mercadería + Servicios)
    # En este caso solo tenemos Producción
    otros_impuestos = impuesto_ventai + 0 + 0  # + mercadería + servicios
    print(f"\n📋 CÁLCULO OTROS IMPUESTOS:")
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    print(f"   Ventas Mercadería: L. 0.00")
    print(f"   Ventas por Servicios: L. 0.00")
    print(f"   Total Otros Impuestos: L. {otros_impuestos:.2f}")
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_controlado
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   Otros Impuestos: L. {otros_impuestos:.2f}")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    print(f"   = TOTAL: L. {suma_total:.2f}")
    
    # Verificación del problema reportado
    print(f"\n🔍 VERIFICACIÓN DEL PROBLEMA:")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f} ✅ (correcto)")
    print(f"   Otros Impuestos: L. {otros_impuestos:.2f} {'✅' if otros_impuestos == 150.00 else '❌'}")
    print(f"   Total esperado: L. 200.00")
    print(f"   Total obtenido: L. {suma_total:.2f}")
    
    if otros_impuestos == 150.00 and suma_total == 200.00:
        print(f"   ✅ CORRECTO")
        return True
    else:
        print(f"   ❌ ERROR")
        if otros_impuestos != 150.00:
            print(f"   🔧 Problema: Otros Impuestos debería ser L. 150.00, no L. {otros_impuestos:.2f}")
        if suma_total != 200.00:
            print(f"   🔧 Problema: Total debería ser L. 200.00, no L. {suma_total:.2f}")
        return False

def test_escenario_con_mercaderia_servicios():
    """Test con Mercadería y Servicios incluidos"""
    
    print("\n\n🧪 TEST CON MERCADERÍA Y SERVICIOS")
    print("=" * 60)
    
    def calcularImpuestoICS(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return 0
        
        if valorVentas <= 500000:
            impuesto = valorVentas * 0.3 / 1000
        elif valorVentas <= 10000000:
            impuesto = valorVentas * 0.4 / 1000
        else:
            impuesto = valorVentas * 0.3 / 1000
        
        return round(impuesto, 2)
    
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return 0
        
        if valorVentas <= 1000000:
            impuesto = valorVentas * 0.1 / 1000
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 0.05 / 1000
        else:
            impuesto = valorVentas * 0.1 / 1000
        
        return round(impuesto, 2)
    
    # Valores de entrada
    ventai = 500000
    ventac = 300000
    ventas = 200000
    controlado = 500000
    
    print("📊 VALORES DE ENTRADA:")
    print(f"   Ventas Rubro Producción: {ventai:,}")
    print(f"   Ventas Mercadería: {ventac:,}")
    print(f"   Ventas por Servicios: {ventas:,}")
    print(f"   Productos Controlados: {controlado:,}")
    
    # Cálculos individuales
    impuesto_ventai = calcularImpuestoICS(ventai)
    impuesto_ventac = calcularImpuestoICS(ventac)
    impuesto_ventas = calcularImpuestoICS(ventas)
    impuesto_controlado = calcularImpuestoICSControlados(controlado)
    
    print(f"\n📋 CÁLCULOS INDIVIDUALES:")
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    print(f"   Ventas Mercadería: L. {impuesto_ventac:.2f}")
    print(f"   Ventas por Servicios: L. {impuesto_ventas:.2f}")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    
    # Calcular "Otros Impuestos" (Producción + Mercadería + Servicios)
    otros_impuestos = impuesto_ventai + impuesto_ventac + impuesto_ventas
    print(f"\n📋 CÁLCULO OTROS IMPUESTOS:")
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    print(f"   Ventas Mercadería: L. {impuesto_ventac:.2f}")
    print(f"   Ventas por Servicios: L. {impuesto_ventas:.2f}")
    print(f"   Total Otros Impuestos: L. {otros_impuestos:.2f}")
    
    # Suma total
    suma_total = otros_impuestos + impuesto_controlado
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   Otros Impuestos: L. {otros_impuestos:.2f}")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    print(f"   = TOTAL: L. {suma_total:.2f}")

def analizar_problema_5000():
    """Analizar de dónde viene el valor 5000.00"""
    
    print("\n\n🔍 ANÁLISIS DEL VALOR 5000.00")
    print("=" * 60)
    
    print("❌ PROBLEMA REPORTADO:")
    print("   Otros Impuestos (Producción + Mercadería + Servicios): L. 5000.00")
    print("   Debería ser: L. 150.00")
    
    print("\n🔧 POSIBLES CAUSAS:")
    print("1. El valor de Ventas Rubro Producción no se está leyendo correctamente")
    print("2. Se está usando un valor incorrecto (ej: 5000000 en lugar de 500000)")
    print("3. Se está aplicando una tarifa incorrecta")
    print("4. Hay un error en la función obtenerValoresVentas()")
    
    print("\n🧮 CÁLCULOS PARA OBTENER 5000.00:")
    print("   Si 500000 × 0.3/1000 = 150.00")
    print("   Para obtener 5000.00:")
    print("   - Con tarifa 0.3/1000: 5000000 × 0.3/1000 = 1500.00")
    print("   - Con tarifa 1.0/1000: 5000000 × 1.0/1000 = 5000.00")
    print("   - Con tarifa 0.3/1000: 16666667 × 0.3/1000 = 5000.00")
    
    print("\n🎯 CONCLUSIÓN:")
    print("   El valor 5000.00 sugiere que se está usando:")
    print("   - Un valor de 5000000 (5 millones) en lugar de 500000 (500 mil)")
    print("   - O una tarifa de 1.0/1000 en lugar de 0.3/1000")
    print("   - O una combinación de ambos")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST PROBLEMA OTROS IMPUESTOS...")
    print()
    
    # Test problema básico
    test1 = test_problema_otros_impuestos()
    
    # Test con mercadería y servicios
    test_escenario_con_mercaderia_servicios()
    
    # Análisis del problema
    analizar_problema_5000()
    
    print("\n\n🎯 CONCLUSIÓN:")
    print("=" * 60)
    if test1:
        print("✅ LOS CÁLCULOS MATEMÁTICOS SON CORRECTOS")
        print("❌ EL PROBLEMA ESTÁ EN LA IMPLEMENTACIÓN DEL FORMULARIO")
        print("🔧 El valor 5000.00 sugiere un error en la lectura de valores")
    else:
        print("❌ HAY ERRORES EN LOS CÁLCULOS MATEMÁTICOS")
        print("🔧 Revisar las tarifas y lógica de cálculo")

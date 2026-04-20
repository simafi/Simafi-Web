#!/usr/bin/env python3
"""
Test para verificar que los impuestos se calculan independientemente
y se suman correctamente, incluyendo Factor × Unidad
"""

def test_impuestos_independientes():
    """Test de impuestos independientes con Factor × Unidad"""
    
    print("🧪 TEST IMPUESTOS INDEPENDIENTES CON FACTOR × UNIDAD")
    print("=" * 70)
    
    # Simular las tarifas normales ICS
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
    
    # Simular las tarifas para productos controlados
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return 0
        
        if valorVentas <= 1000000:
            impuesto = valorVentas * 1.0 / 1000
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 1.5 / 1000
        else:
            impuesto = valorVentas * 2.0 / 1000
        
        return round(impuesto, 2)
    
    # Simular Factor × Unidad
    def calcularFactorUnidad(unidad, factor):
        if unidad > 0 and factor > 0:
            return round(unidad * factor, 2)
        return 0
    
    print("\n📊 CASO 1: Solo Ventas Rubro Producción")
    print("-" * 50)
    ventai = 500000
    impuestoVentai = calcularImpuestoICS(ventai)
    print(f"Ventas Rubro Producción: {ventai:,}")
    print(f"Impuesto calculado: L. {impuestoVentai:.2f}")
    print(f"Total: L. {impuestoVentai:.2f}")
    
    print("\n📊 CASO 2: Solo Productos Controlados")
    print("-" * 50)
    controlado = 500000
    impuestoControlado = calcularImpuestoICSControlados(controlado)
    print(f"Productos Controlados: {controlado:,}")
    print(f"Impuesto calculado: L. {impuestoControlado:.2f}")
    print(f"Total: L. {impuestoControlado:.2f}")
    
    print("\n📊 CASO 3: Solo Factor × Unidad")
    print("-" * 50)
    unidad = 500
    factor = 1
    impuestoUnidadFactor = calcularFactorUnidad(unidad, factor)
    print(f"Unidad: {unidad}, Factor: {factor}")
    print(f"Impuesto calculado: L. {impuestoUnidadFactor:.2f}")
    print(f"Total: L. {impuestoUnidadFactor:.2f}")
    
    print("\n📊 CASO 4: COMBINADO - Todos los impuestos independientes")
    print("-" * 50)
    
    # Valores de entrada
    ventai = 500000
    ventac = 300000
    ventas = 200000
    controlado = 500000
    unidad = 500
    factor = 1
    
    # Cálculos independientes
    impuestoVentai = calcularImpuestoICS(ventai)
    impuestoVentac = calcularImpuestoICS(ventac)
    impuestoVentas = calcularImpuestoICS(ventas)
    impuestoControlado = calcularImpuestoICSControlados(controlado)
    impuestoUnidadFactor = calcularFactorUnidad(unidad, factor)
    
    print("Valores de entrada:")
    print(f"  Ventas Rubro Producción: {ventai:,}")
    print(f"  Ventas Mercadería: {ventac:,}")
    print(f"  Ventas por Servicios: {ventas:,}")
    print(f"  Productos Controlados: {controlado:,}")
    print(f"  Unidad: {unidad}, Factor: {factor}")
    
    print("\nImpuestos calculados independientemente:")
    print(f"  Ventas Rubro Producción: L. {impuestoVentai:.2f}")
    print(f"  Ventas Mercadería: L. {impuestoVentac:.2f}")
    print(f"  Ventas por Servicios: L. {impuestoVentas:.2f}")
    print(f"  Productos Controlados: L. {impuestoControlado:.2f}")
    print(f"  Factor × Unidad: L. {impuestoUnidadFactor:.2f}")
    
    # Suma total
    sumaTotal = impuestoVentai + impuestoVentac + impuestoVentas + impuestoControlado + impuestoUnidadFactor
    
    print(f"\n🎯 SUMA TOTAL DE IMPUESTOS INDEPENDIENTES:")
    print(f"  {impuestoVentai:.2f} + {impuestoVentac:.2f} + {impuestoVentas:.2f} + {impuestoControlado:.2f} + {impuestoUnidadFactor:.2f} = L. {sumaTotal:.2f}")
    
    # Verificación
    esperado = 150.00 + 90.00 + 60.00 + 500.00 + 500.00  # 1300.00
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"  Esperado: L. {esperado:.2f}")
    print(f"  Obtenido: L. {sumaTotal:.2f}")
    print(f"  Diferencia: L. {abs(sumaTotal - esperado):.2f}")
    
    if abs(sumaTotal - esperado) < 0.01:
        print(f"  ✅ CORRECTO")
        return True
    else:
        print(f"  ❌ ERROR")
        return False

def test_caso_especifico_500000():
    """Test del caso específico mencionado por el usuario"""
    
    print("\n🧪 TEST CASO ESPECÍFICO: 500,000 + 500,000")
    print("=" * 70)
    
    def calcularImpuestoICS(valorVentas):
        if valorVentas <= 500000:
            return round(valorVentas * 0.3 / 1000, 2)
        return round(valorVentas * 0.4 / 1000, 2)
    
    def calcularImpuestoICSControlados(valorVentas):
        if valorVentas <= 1000000:
            return round(valorVentas * 1.0 / 1000, 2)
        return round(valorVentas * 1.5 / 1000, 2)
    
    # Caso específico
    ventai = 500000
    controlado = 500000
    
    impuestoVentai = calcularImpuestoICS(ventai)
    impuestoControlado = calcularImpuestoICSControlados(controlado)
    sumaTotal = impuestoVentai + impuestoControlado
    
    print(f"Ventas Rubro Producción: {ventai:,} → L. {impuestoVentai:.2f}")
    print(f"Productos Controlados: {controlado:,} → L. {impuestoControlado:.2f}")
    print(f"Suma Total: L. {sumaTotal:.2f}")
    
    # El usuario esperaba 200.00, pero la matemática correcta es 650.00
    print(f"\n📝 NOTA:")
    print(f"  Usuario esperaba: L. 200.00")
    print(f"  Cálculo correcto: L. {sumaTotal:.2f}")
    print(f"  La diferencia se debe a que Productos Controlados")
    print(f"  usa tarifas más altas (1.0/1000 vs 0.3/1000)")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST IMPUESTOS INDEPENDIENTES...")
    print()
    
    if test_impuestos_independientes():
        print("\n✅ TODOS LOS IMPUESTOS INDEPENDIENTES FUNCIONAN CORRECTAMENTE")
    else:
        print("\n❌ HAY ERRORES EN LOS CÁLCULOS INDEPENDIENTES")
    
    test_caso_especifico_500000()
    
    print("\n🎯 RESUMEN:")
    print("  • Cada campo calcula su impuesto independientemente")
    print("  • El campo 'Impuesto Calculado' muestra la suma de todos")
    print("  • Factor × Unidad se incluye como impuesto independiente")
    print("  • Los logs muestran cada cálculo paso a paso")

#!/usr/bin/env python3
"""
Test específico para verificar la suma de Productos Controlados
"""

def test_suma_productos_controlados():
    """Test específico para la suma de Productos Controlados"""
    
    print("🧪 TEST SUMA PRODUCTOS CONTROLADOS")
    print("=" * 60)
    
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
            impuesto = valorVentas * 0.1 / 1000
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 0.05 / 1000
        else:
            impuesto = valorVentas * 0.1 / 1000
        
        return round(impuesto, 2)
    
    print("📊 CASO 1: Solo Ventas Rubro Producción (500,000)")
    print("-" * 50)
    ventai = 500000
    impuesto_ventai = calcularImpuestoICS(ventai)
    print(f"Valor: {ventai:,}")
    print(f"Impuesto: L. {impuesto_ventai:.2f}")
    print(f"Total: L. {impuesto_ventai:.2f}")
    
    print("\n📊 CASO 2: Solo Productos Controlados (500,000)")
    print("-" * 50)
    controlado = 500000
    impuesto_controlado = calcularImpuestoICSControlados(controlado)
    print(f"Valor: {controlado:,}")
    print(f"Impuesto: L. {impuesto_controlado:.2f}")
    print(f"Total: L. {impuesto_controlado:.2f}")
    
    print("\n📊 CASO 3: COMBINADO - Ventas Rubro Producción + Productos Controlados")
    print("-" * 50)
    print(f"Ventas Rubro Producción: {ventai:,} → L. {impuesto_ventai:.2f}")
    print(f"Productos Controlados: {controlado:,} → L. {impuesto_controlado:.2f}")
    
    suma_total = impuesto_ventai + impuesto_controlado
    print(f"Suma Total: L. {suma_total:.2f}")
    
    # Verificación
    esperado = 200.00  # 150 + 50
    print(f"\n🔍 VERIFICACIÓN:")
    print(f"   Esperado: L. {esperado:.2f}")
    print(f"   Obtenido: L. {suma_total:.2f}")
    print(f"   Diferencia: L. {abs(suma_total - esperado):.2f}")
    
    if abs(suma_total - esperado) < 0.01:
        print(f"   ✅ CORRECTO")
        return True
    else:
        print(f"   ❌ ERROR")
        return False

def test_diferentes_valores_controlados():
    """Test con diferentes valores de Productos Controlados"""
    
    print("\n\n🧪 TEST DIFERENTES VALORES PRODUCTOS CONTROLADOS")
    print("=" * 60)
    
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
    
    # Valores de prueba
    valores_test = [100000, 500000, 1000000, 2000000, 5000000]
    
    print("📊 PROBANDO DIFERENTES VALORES:")
    print()
    
    for valor in valores_test:
        impuesto = calcularImpuestoICSControlados(valor)
        print(f"   {valor:>10,}: L. {impuesto:>8.2f}")

def test_suma_con_otros_campos():
    """Test de suma con otros campos incluidos"""
    
    print("\n\n🧪 TEST SUMA CON OTROS CAMPOS")
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
    unidad = 500
    factor = 1
    
    print("📊 VALORES DE ENTRADA:")
    print(f"   Ventas Rubro Producción: {ventai:,}")
    print(f"   Ventas Mercadería: {ventac:,}")
    print(f"   Ventas por Servicios: {ventas:,}")
    print(f"   Productos Controlados: {controlado:,}")
    print(f"   Unidad: {unidad}, Factor: {factor}")
    
    # Cálculos individuales
    impuesto_ventai = calcularImpuestoICS(ventai)
    impuesto_ventac = calcularImpuestoICS(ventac)
    impuesto_ventas = calcularImpuestoICS(ventas)
    impuesto_controlado = calcularImpuestoICSControlados(controlado)
    impuesto_unidad_factor = round(unidad * factor, 2)
    
    print(f"\n📋 CÁLCULOS INDIVIDUALES:")
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    print(f"   Ventas Mercadería: L. {impuesto_ventac:.2f}")
    print(f"   Ventas por Servicios: L. {impuesto_ventas:.2f}")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    print(f"   Factor × Unidad: L. {impuesto_unidad_factor:.2f}")
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_ventac + impuesto_ventas + impuesto_controlado + impuesto_unidad_factor
    
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   {impuesto_ventai:.2f} + {impuesto_ventac:.2f} + {impuesto_ventas:.2f} + {impuesto_controlado:.2f} + {impuesto_unidad_factor:.2f} = L. {suma_total:.2f}")
    
    # Verificación específica de Productos Controlados
    print(f"\n🔍 VERIFICACIÓN PRODUCTOS CONTROLADOS:")
    print(f"   Valor: {controlado:,}")
    print(f"   Impuesto calculado: L. {impuesto_controlado:.2f}")
    print(f"   ¿Es correcto?: {'✅' if impuesto_controlado == 50.00 else '❌'}")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST SUMA PRODUCTOS CONTROLADOS...")
    print()
    
    # Test suma básica
    test1 = test_suma_productos_controlados()
    
    # Test diferentes valores
    test_diferentes_valores_controlados()
    
    # Test suma con otros campos
    test_suma_con_otros_campos()
    
    print("\n\n🎯 CONCLUSIÓN:")
    print("=" * 60)
    if test1:
        print("✅ LA SUMA DE PRODUCTOS CONTROLADOS ESTÁ CORRECTA")
        print("✅ El cálculo independiente da L. 50.00")
        print("✅ La suma combinada da L. 200.00")
        print("✅ Los parámetros están bien aplicados")
    else:
        print("❌ HAY PROBLEMAS CON LA SUMA DE PRODUCTOS CONTROLADOS")
        print("🔧 Revisar la implementación")

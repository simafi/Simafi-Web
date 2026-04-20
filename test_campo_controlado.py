#!/usr/bin/env python3
"""
Test específico para verificar el cálculo cuando se ingresa desde Productos Controlados
"""

def test_campo_controlado():
    """Test específico para el campo Productos Controlados"""
    
    print("🧪 TEST CAMPO PRODUCTOS CONTROLADOS")
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
    
    # Simular el escenario: Ventas Rubro Producción ya tiene valor, se ingresa Productos Controlados
    print("📊 ESCENARIO: Ventas Rubro Producción ya tiene valor, se ingresa Productos Controlados")
    print("-" * 60)
    
    # Valores existentes
    ventai_existente = 500000
    controlado_nuevo = 500000
    
    print(f"Valores existentes:")
    print(f"   Ventas Rubro Producción: {ventai_existente:,}")
    print(f"   Productos Controlados (nuevo): {controlado_nuevo:,}")
    
    # Cálculo individual de Ventas Rubro Producción (ya existente)
    impuesto_ventai = calcularImpuestoICS(ventai_existente)
    print(f"\n📋 CÁLCULO VENTAS RUBRO PRODUCCIÓN (existente):")
    print(f"   Valor: {ventai_existente:,}")
    print(f"   Impuesto: L. {impuesto_ventai:.2f}")
    
    # Cálculo individual de Productos Controlados (nuevo)
    impuesto_controlado = calcularImpuestoICSControlados(controlado_nuevo)
    print(f"\n📋 CÁLCULO PRODUCTOS CONTROLADOS (nuevo):")
    print(f"   Valor: {controlado_nuevo:,}")
    print(f"   Impuesto: L. {impuesto_controlado:.2f}")
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_controlado
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    print(f"   = TOTAL: L. {suma_total:.2f}")
    
    # Verificación
    esperado = 200.00
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

def test_escenario_inverso():
    """Test del escenario inverso: Productos Controlados ya tiene valor, se ingresa Ventas Rubro Producción"""
    
    print("\n\n🧪 TEST ESCENARIO INVERSO")
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
    
    # Valores existentes
    controlado_existente = 500000
    ventai_nuevo = 500000
    
    print(f"Valores existentes:")
    print(f"   Productos Controlados: {controlado_existente:,}")
    print(f"   Ventas Rubro Producción (nuevo): {ventai_nuevo:,}")
    
    # Cálculo individual de Productos Controlados (ya existente)
    impuesto_controlado = calcularImpuestoICSControlados(controlado_existente)
    print(f"\n📋 CÁLCULO PRODUCTOS CONTROLADOS (existente):")
    print(f"   Valor: {controlado_existente:,}")
    print(f"   Impuesto: L. {impuesto_controlado:.2f}")
    
    # Cálculo individual de Ventas Rubro Producción (nuevo)
    impuesto_ventai = calcularImpuestoICS(ventai_nuevo)
    print(f"\n📋 CÁLCULO VENTAS RUBRO PRODUCCIÓN (nuevo):")
    print(f"   Valor: {ventai_nuevo:,}")
    print(f"   Impuesto: L. {impuesto_ventai:.2f}")
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_controlado
    print(f"\n🎯 SUMA TOTAL:")
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    print(f"   = TOTAL: L. {suma_total:.2f}")
    
    # Verificación
    esperado = 200.00
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

def test_problema_identificado():
    """Identificar el problema específico"""
    
    print("\n\n🔍 ANÁLISIS DEL PROBLEMA")
    print("=" * 60)
    
    print("❌ PROBLEMA IDENTIFICADO:")
    print("Cuando se ingresa desde el campo 'Productos Controlados',")
    print("la función calcularSumaTotalIndependientes() puede no estar")
    print("obteniendo correctamente el valor de 'Ventas Rubro Producción'.")
    
    print("\n🔧 POSIBLES CAUSAS:")
    print("1. La función obtenerValoresVentas() no está leyendo correctamente")
    print("   el valor de 'Ventas Rubro Producción' cuando se calcula desde 'Productos Controlados'")
    print("2. Puede haber un problema de timing en la actualización de valores")
    print("3. El campo 'Ventas Rubro Producción' puede no estar siendo detectado")
    print("   correctamente en el momento del cálculo")
    
    print("\n🎯 SOLUCIÓN PROPUESTA:")
    print("1. Agregar logs detallados en obtenerValoresVentas()")
    print("2. Verificar que todos los campos se están leyendo correctamente")
    print("3. Asegurar que la función calcularSumaTotalIndependientes()")
    print("   obtiene los valores más recientes de todos los campos")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST CAMPO PRODUCTOS CONTROLADOS...")
    print()
    
    # Test campo controlado
    test1 = test_campo_controlado()
    
    # Test escenario inverso
    test2 = test_escenario_inverso()
    
    # Análisis del problema
    test_problema_identificado()
    
    print("\n\n🎯 CONCLUSIÓN:")
    print("=" * 60)
    if test1 and test2:
        print("✅ LOS CÁLCULOS MATEMÁTICOS SON CORRECTOS")
        print("❌ EL PROBLEMA ESTÁ EN LA IMPLEMENTACIÓN DEL FORMULARIO")
        print("🔧 Necesita revisar la función obtenerValoresVentas()")
    else:
        print("❌ HAY ERRORES EN LOS CÁLCULOS MATEMÁTICOS")
        print("🔧 Revisar las tarifas y lógica de cálculo")

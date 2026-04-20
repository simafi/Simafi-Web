#!/usr/bin/env python3
"""
Test específico para verificar la suma de impuestos
"""

def test_suma_especifica():
    """Test específico para la suma de impuestos"""
    
    print("🧪 TEST SUMA ESPECÍFICA - 500,000 + 500,000")
    print("=" * 60)
    
    # Simular las tarifas normales ICS
    def calcularImpuestoICS(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return { 'impuestoTotal': 0 }
        
        if valorVentas <= 500000:
            impuesto = valorVentas * 0.3 / 1000
        elif valorVentas <= 10000000:
            impuesto = valorVentas * 0.4 / 1000
        else:
            impuesto = valorVentas * 0.3 / 1000
        
        return { 'impuestoTotal': round(impuesto, 2) }
    
    # Simular las tarifas para productos controlados
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return { 'impuestoTotal': 0 }
        
        if valorVentas <= 1000000:
            impuesto = valorVentas * 1.0 / 1000
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 1.5 / 1000
        else:
            impuesto = valorVentas * 2.0 / 1000
        
        return { 'impuestoTotal': round(impuesto, 2) }
    
    # Caso específico: 500,000 + 500,000
    print("\n📊 CASO ESPECÍFICO: 500,000 + 500,000")
    print("-" * 60)
    
    # Cálculo individual de Ventas Rubro Producción
    ventai = calcularImpuestoICS(500000)
    print(f"Ventas Rubro Producción: 500,000")
    print(f"  Cálculo: 500,000 × 0.3/1000 = {500000 * 0.3 / 1000}")
    print(f"  Resultado: L. {ventai['impuestoTotal']:.2f}")
    
    # Cálculo individual de Productos Controlados
    controlados = calcularImpuestoICSControlados(500000)
    print(f"\nProductos Controlados: 500,000")
    print(f"  Cálculo: 500,000 × 1.0/1000 = {500000 * 1.0 / 1000}")
    print(f"  Resultado: L. {controlados['impuestoTotal']:.2f}")
    
    # Suma total
    total = ventai['impuestoTotal'] + controlados['impuestoTotal']
    print(f"\nSuma Total:")
    print(f"  Ventas Rubro Producción: L. {ventai['impuestoTotal']:.2f}")
    print(f"  Productos Controlados: L. {controlados['impuestoTotal']:.2f}")
    print(f"  = TOTAL: L. {total:.2f}")
    
    # Verificación
    esperado = 150.00 + 500.00  # 650.00
    print(f"\nVerificación:")
    print(f"  Esperado: L. {esperado:.2f}")
    print(f"  Obtenido: L. {total:.2f}")
    print(f"  Diferencia: L. {abs(total - esperado):.2f}")
    
    if abs(total - esperado) < 0.01:
        print(f"  ✅ CORRECTO")
        return True
    else:
        print(f"  ❌ ERROR")
        return False

def test_problema_formulario():
    """Test para identificar el problema en el formulario"""
    
    print("\n🔍 ANÁLISIS DEL PROBLEMA EN EL FORMULARIO")
    print("=" * 60)
    
    print("\n❌ PROBLEMA IDENTIFICADO:")
    print("Si los cálculos individuales están bien pero la suma está mal,")
    print("el problema puede estar en:")
    
    print("\n1. 🔢 CONVERSIÓN DE TIPOS:")
    print("   - Los valores pueden estar como strings en lugar de números")
    print("   - parseFloat() puede no estar funcionando correctamente")
    print("   - Puede haber valores undefined o null")
    
    print("\n2. 🔄 ORDEN DE EJECUCIÓN:")
    print("   - Los cálculos pueden ejecutarse en orden incorrecto")
    print("   - Puede haber interferencia entre cálculos")
    print("   - Las variables ocultas pueden no actualizarse correctamente")
    
    print("\n3. 🧮 LÓGICA DE SUMA:")
    print("   - Puede estar sumando valores base en lugar de impuestos")
    print("   - Puede haber duplicación en el cálculo")
    print("   - Puede estar aplicando tarifas incorrectas")
    
    print("\n🎯 SOLUCIÓN PROPUESTA:")
    print("1. Agregar más logs detallados en la función de suma")
    print("2. Verificar que los valores son números antes de sumar")
    print("3. Asegurar que se suman solo los impuestos calculados")
    print("4. Verificar que no hay duplicación en el cálculo")

if __name__ == "__main__":
    print("🧪 INICIANDO TEST SUMA ESPECÍFICA...")
    print()
    
    if test_suma_especifica():
        print("\n✅ LA SUMA MATEMÁTICA ES CORRECTA")
        print("🎯 El problema está en la implementación del formulario")
    else:
        print("\n❌ HAY ERROR EN LA SUMA MATEMÁTICA")
        print("🔧 Necesita corrección")
    
    test_problema_formulario()

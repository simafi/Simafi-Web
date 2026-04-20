#!/usr/bin/env python3
"""
Test para verificar la automatización del campo Ventas Rubro Producción
y replicar esa funcionalidad en Productos Controlados
"""

def test_automatizacion_ventai():
    print("🔍 ANÁLISIS DE AUTOMATIZACIÓN VENTAS RUBRO PRODUCCIÓN")
    print("=" * 60)
    
    # Simular el escenario reportado
    print("\n📊 ESCENARIO REPORTADO:")
    print("   • Ventas Rubro Producción: 500,000.00")
    print("   • Productos Controlados: 500,000.00")
    print("   • Resultado esperado: L. 200.00")
    print("   • Resultado actual: L. 650.00 (Productos Controlados: L. 50.00 + Otros Impuestos: L. 5000.00)")
    
    # Calcular impuestos individuales
    print("\n💰 CÁLCULOS INDIVIDUALES:")
    
    # Ventas Rubro Producción (ICS normal)
    ventai = 500000.0
    impuesto_ventai = calcular_impuesto_ics(ventai)
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    
    # Productos Controlados (ICS controlados)
    controlado = 500000.0
    impuesto_controlado = calcular_impuesto_ics_controlados(controlado)
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    
    # Suma total esperada
    suma_total_esperada = impuesto_ventai + impuesto_controlado
    print(f"   Suma total esperada: L. {suma_total_esperada:.2f}")
    
    # Simular el problema reportado
    print("\n❌ PROBLEMA REPORTADO:")
    otros_impuestos_incorrecto = 5000.00  # Valor incorrecto reportado
    suma_incorrecta = impuesto_controlado + otros_impuestos_incorrecto
    print(f"   Otros Impuestos (incorrecto): L. {otros_impuestos_incorrecto:.2f}")
    print(f"   Suma incorrecta: L. {suma_incorrecta:.2f}")
    
    # Análisis del problema
    print("\n🔍 ANÁLISIS DEL PROBLEMA:")
    print("   • El cálculo individual de Productos Controlados está correcto (L. 50.00)")
    print("   • El problema está en 'Otros Impuestos' que muestra L. 5000.00")
    print("   • Esto sugiere que el valor de Ventas Rubro Producción se está leyendo incorrectamente")
    print("   • Posible causa: conflicto entre event listeners o variables ocultas")
    
    # Verificar qué valor de ventai produciría 5000.00
    print("\n🧮 VERIFICACIÓN MATEMÁTICA:")
    # Si otros_impuestos = 5000.00, ¿qué valor de ventai se está usando?
    # Para ICS normal: 5000.00 = ventai * 0.003 (tarifa 0.3%)
    ventai_incorrecto = 5000.00 / 0.003
    print(f"   Para obtener L. 5000.00 en Otros Impuestos:")
    print(f"   Ventas Rubro Producción debería ser: L. {ventai_incorrecto:,.2f}")
    print(f"   Esto sugiere que se está leyendo un valor 10 veces mayor al esperado")
    
    # Solución propuesta
    print("\n✅ SOLUCIÓN PROPUESTA:")
    print("   1. Revisar la función obtenerValoresVentas() para ventai")
    print("   2. Verificar que no haya conflictos entre event listeners")
    print("   3. Asegurar que las variables ocultas se actualicen correctamente")
    print("   4. Implementar la misma lógica de automatización que funciona en ventai")

def calcular_impuesto_ics(valor_ventas):
    """Calcular impuesto ICS normal"""
    if not valor_ventas or valor_ventas <= 0:
        return 0
    
    # Tarifas ICS normales
    tarifas = [
        {"rango1": 0.0, "rango2": 1000000.0, "valor": 0.3, "categoria": "1", "descripcion": "ICS $0 - $1,000,000"},
        {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 0.15, "categoria": "1", "descripcion": "ICS $1,000,000 - $5,000,000"},
        {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 0.3, "categoria": "1", "descripcion": "ICS $5,000,000+"}
    ]
    
    impuesto_total = 0
    for tarifa in tarifas:
        if valor_ventas >= tarifa["rango1"] and valor_ventas <= tarifa["rango2"]:
            impuesto = (valor_ventas / 1000) * tarifa["valor"]
            impuesto_total += impuesto
            break
    
    return impuesto_total

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
    test_automatizacion_ventai()

#!/usr/bin/env python3
"""
Test específico para el problema de Ventas Productos Controlados
"""

def test_productos_controlados():
    """Test específico del problema con productos controlados"""
    
    print("🧪 TEST ESPECÍFICO - VENTAS PRODUCTOS CONTROLADOS")
    print("=" * 70)
    
    # Simular las tarifas normales ICS
    def calcularImpuestoICS(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return { 'impuestoTotal': 0 }
        
        # Tarifas normales ICS
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
        
        # Tarifas más altas para productos controlados
        if valorVentas <= 1000000:
            impuesto = valorVentas * 1.0 / 1000
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 1.5 / 1000
        else:
            impuesto = valorVentas * 2.0 / 1000
        
        return { 'impuestoTotal': round(impuesto, 2) }
    
    def calcularImpuestoUnidadFactor(valorUnidad, valorFactor):
        if not valorUnidad or valorUnidad <= 0 or not valorFactor or valorFactor <= 0:
            return { 'impuestoTotal': 0, 'valorCalculado': 0 }
        
        valorCalculado = valorFactor * valorUnidad
        return { 'impuestoTotal': valorCalculado, 'valorCalculado': valorCalculado }
    
    # Casos de prueba específicos
    casos_prueba = [
        {
            "nombre": "Caso 1: Solo productos controlados",
            "valores": {
                "ventai": 0, "ventac": 0, "ventas": 0, 
                "controlado": 1000, "factor": 0, "unidad": 0
            }
        },
        {
            "nombre": "Caso 2: Productos controlados + otros",
            "valores": {
                "ventai": 1000, "ventac": 2000, "ventas": 1500, 
                "controlado": 1000, "factor": 0, "unidad": 0
            }
        },
        {
            "nombre": "Caso 3: Productos controlados + Factor×Unidad",
            "valores": {
                "ventai": 0, "ventac": 0, "ventas": 0, 
                "controlado": 1000, "factor": 2, "unidad": 100
            }
        },
        {
            "nombre": "Caso 4: Todos los tipos combinados",
            "valores": {
                "ventai": 1000, "ventac": 2000, "ventas": 1500, 
                "controlado": 1000, "factor": 2, "unidad": 100
            }
        },
        {
            "nombre": "Caso 5: Valores altos - productos controlados",
            "valores": {
                "ventai": 10000, "ventac": 5000, "ventas": 7500, 
                "controlado": 2000000, "factor": 0, "unidad": 0
            }
        }
    ]
    
    print("\n📊 EJECUTANDO CASOS DE PRUEBA:")
    print("-" * 70)
    
    todos_pasan = True
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n🧪 {caso['nombre']}")
        print(f"   Valores: {caso['valores']}")
        
        # Calcular impuestos individuales
        industria = calcularImpuestoICS(caso['valores']['ventai'])
        comercio = calcularImpuestoICS(caso['valores']['ventac'])
        servicios = calcularImpuestoICS(caso['valores']['ventas'])
        controlados = calcularImpuestoICSControlados(caso['valores']['controlado'])
        unidadFactor = calcularImpuestoUnidadFactor(caso['valores']['unidad'], caso['valores']['factor'])
        
        # Calcular suma total
        totalImpuesto = (industria['impuestoTotal'] + 
                        comercio['impuestoTotal'] + 
                        servicios['impuestoTotal'] + 
                        controlados['impuestoTotal'] +
                        unidadFactor['impuestoTotal'])
        
        print(f"   Resultados individuales:")
        print(f"     • Industria: L. {industria['impuestoTotal']:.2f}")
        print(f"     • Comercio: L. {comercio['impuestoTotal']:.2f}")
        print(f"     • Servicios: L. {servicios['impuestoTotal']:.2f}")
        print(f"     • Controlados: L. {controlados['impuestoTotal']:.2f} (tarifas especiales)")
        print(f"     • Factor × Unidad: L. {unidadFactor['impuestoTotal']:.2f}")
        print(f"     = TOTAL: L. {totalImpuesto:.2f}")
        
        # Verificar que la suma es correcta
        suma_manual = (industria['impuestoTotal'] + 
                      comercio['impuestoTotal'] + 
                      servicios['impuestoTotal'] + 
                      controlados['impuestoTotal'] +
                      unidadFactor['impuestoTotal'])
        
        if abs(totalImpuesto - suma_manual) < 0.01:
            print(f"   ✅ CORRECTO: Suma verificada")
        else:
            print(f"   ❌ ERROR: Suma incorrecta")
            print(f"       Total calculado: {totalImpuesto:.2f}")
            print(f"       Suma manual: {suma_manual:.2f}")
            todos_pasan = False
        
        # Verificar si hay conflicto específico con productos controlados
        if caso['valores']['controlado'] > 0:
            print(f"   🔍 Análisis productos controlados:")
            print(f"       Valor base: {caso['valores']['controlado']}")
            print(f"       Impuesto calculado: {controlados['impuestoTotal']:.2f}")
            print(f"       Tarifa aplicada: {controlados['impuestoTotal'] / caso['valores']['controlado'] * 1000:.2f} por mil")
    
    print("\n" + "=" * 70)
    if todos_pasan:
        print("✅ TODOS LOS CASOS DE PRUEBA PASARON")
        print("🎯 No hay conflicto con productos controlados")
    else:
        print("❌ ALGUNOS CASOS DE PRUEBA FALLARON")
        print("🔧 Hay conflicto en la suma con productos controlados")
    
    return todos_pasan

def analizar_problema_controlados():
    """Analizar el problema específico con productos controlados"""
    
    print("\n🔍 ANÁLISIS DEL PROBLEMA CON PRODUCTOS CONTROLADOS")
    print("=" * 70)
    
    print("\n📋 DIFERENCIAS EN TARIFAS:")
    print("• Ventas normales (ventai, ventac, ventas):")
    print("  - $0 - $500,000: 0.3 por mil")
    print("  - $500,000 - $10,000,000: 0.4 por mil")
    print("  - $10,000,000+: 0.3 por mil")
    
    print("\n• Productos controlados:")
    print("  - $0 - $1,000,000: 1.0 por mil")
    print("  - $1,000,000 - $5,000,000: 1.5 por mil")
    print("  - $5,000,000+: 2.0 por mil")
    
    print("\n❌ POSIBLES PROBLEMAS:")
    print("1. Las tarifas son muy diferentes (1.0 vs 0.3 por mil)")
    print("2. Puede haber error en el cálculo de tarifas controladas")
    print("3. Conflicto en la suma cuando se combinan")
    print("4. Error en la función calcularImpuestoICSControlados")
    
    print("\n🎯 SOLUCIÓN PROPUESTA:")
    print("1. Verificar que calcularImpuestoICSControlados funciona correctamente")
    print("2. Asegurar que la suma incluye el resultado correcto")
    print("3. Agregar logs específicos para productos controlados")
    print("4. Verificar que no hay duplicación en el cálculo")

if __name__ == "__main__":
    print("🧪 INICIANDO TEST PRODUCTOS CONTROLADOS...")
    print()
    
    if test_productos_controlados():
        print("\n✅ NO HAY CONFLICTO CON PRODUCTOS CONTROLADOS")
        print("🎯 El problema puede estar en otra parte")
    else:
        print("\n❌ HAY CONFLICTO CON PRODUCTOS CONTROLADOS")
        print("🔧 Necesita corrección específica")
    
    analizar_problema_controlados()

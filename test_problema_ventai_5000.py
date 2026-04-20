#!/usr/bin/env python3
"""
Test específico para verificar por qué Ventas Rubro Producción da L. 5000.00
en lugar de L. 150.00 cuando se combina con Productos Controlados
"""

def test_problema_ventai_5000():
    print("🔍 ANÁLISIS ESPECÍFICO DEL PROBLEMA VENTAI 5000.00")
    print("=" * 60)
    
    # Escenario reportado
    print("\n📊 ESCENARIO REPORTADO:")
    print("   • Ventas Rubro Producción: 500,000.00")
    print("   • Productos Controlados: 500,000.00")
    print("   • Resultado esperado: L. 200.00")
    print("   • Resultado actual: L. 650.00")
    print("   • Desglose actual:")
    print("     - Productos Controlados: L. 50.00 ✅ (correcto)")
    print("     - Otros Impuestos: L. 5000.00 ❌ (incorrecto)")
    
    # Análisis del problema
    print("\n🔍 ANÁLISIS DEL PROBLEMA:")
    print("   • El cálculo individual de Productos Controlados está correcto")
    print("   • El problema está en 'Otros Impuestos' que incluye Ventas Rubro Producción")
    print("   • Si Otros Impuestos = L. 5000.00, significa que ventai se está leyendo como 5,000,000")
    
    # Verificación matemática
    print("\n🧮 VERIFICACIÓN MATEMÁTICA:")
    
    # Calcular qué valor de ventai produciría 5000.00
    tarifa_ics = 0.003  # 0.3% = 0.3/1000
    ventai_incorrecto = 5000.00 / tarifa_ics
    print(f"   Para obtener L. 5000.00 en Otros Impuestos:")
    print(f"   Ventas Rubro Producción debería ser: L. {ventai_incorrecto:,.2f}")
    print(f"   Esto es 10 veces mayor al valor esperado (500,000)")
    
    # Verificar si hay un problema de formato
    print("\n🔍 POSIBLES CAUSAS:")
    print("   1. El valor se está leyendo con formato incorrecto (5,000,000 en lugar de 500,000)")
    print("   2. Hay un conflicto entre event listeners que duplica el valor")
    print("   3. Las variables ocultas se están actualizando incorrectamente")
    print("   4. El campo se está leyendo múltiples veces con valores diferentes")
    
    # Simular el problema
    print("\n🧪 SIMULACIÓN DEL PROBLEMA:")
    
    # Valor correcto
    ventai_correcto = 500000.0
    impuesto_correcto = calcular_impuesto_ics(ventai_correcto)
    print(f"   Valor correcto (500,000): L. {impuesto_correcto:.2f}")
    
    # Valor incorrecto (10 veces mayor)
    ventai_incorrecto = 5000000.0
    impuesto_incorrecto = calcular_impuesto_ics(ventai_incorrecto)
    print(f"   Valor incorrecto (5,000,000): L. {impuesto_incorrecto:.2f}")
    
    # Diferencia
    diferencia = impuesto_incorrecto - impuesto_correcto
    print(f"   Diferencia: L. {diferencia:.2f}")
    
    # Solución propuesta
    print("\n✅ SOLUCIÓN PROPUESTA:")
    print("   1. Agregar logs específicos en obtenerValoresVentas() para ventai")
    print("   2. Verificar que no haya múltiples event listeners conflictivos")
    print("   3. Asegurar que el valor se lea una sola vez y se mantenga consistente")
    print("   4. Implementar validación específica para detectar valores anómalos")
    
    # Código de corrección sugerido
    print("\n🔧 CÓDIGO DE CORRECCIÓN SUGERIDO:")
    print("""
    // En obtenerValoresVentas(), agregar validación específica para ventai
    if (campo === 'ventai') {
        console.log(`🔍 VALIDACIÓN ESPECÍFICA VENTAI:`);
        console.log(`   Valor original: "${input.value}"`);
        console.log(`   Valor limpiado: ${valor}`);
        console.log(`   Valor > 1000000: ${valor > 1000000}`);
        
        // Detectar valores anómalos
        if (valor > 1000000) {
            console.log(`⚠️ ALERTA: Valor de ventai parece anómalo: ${valor}`);
            console.log(`   Posible causa: formato incorrecto o lectura duplicada`);
        }
    }
    """)

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

if __name__ == "__main__":
    test_problema_ventai_5000()

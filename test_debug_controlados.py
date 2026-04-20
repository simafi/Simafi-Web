#!/usr/bin/env python3
"""
Test para debuggear específicamente el problema con Productos Controlados
"""

def test_debug_controlados():
    print("🔍 DEBUG PRODUCTOS CONTROLADOS")
    print("=" * 50)
    
    # Simular el escenario exacto
    print("\n📊 ESCENARIO:")
    print("   • Ventas Rubro Producción: 500,000.00")
    print("   • Productos Controlados: 500,000.00")
    print("   • Resultado esperado: L. 200.00")
    
    # Simular la función calcularImpuestoICSControlados
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return {"impuestoTotal": 0, "detalleCalculo": [], "valorVentas": 0}
        
        # Tarifas controlados (del código actual)
        tarifasControlados = [
            {"rango1": 0.0, "rango2": 1000000.0, "valor": 0.1, "categoria": "2", "descripcion": "Controlados $0 - $1,000,000"},
            {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 0.05, "categoria": "2", "descripcion": "Controlados $1,000,000 - $5,000,000"},
            {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 0.1, "categoria": "2", "descripcion": "Controlados $5,000,000+"}
        ]
        
        impuestoTotal = 0
        valorRestante = valorVentas
        detalleCalculo = []
        
        for tarifa in tarifasControlados:
            if valorRestante <= 0:
                break
            
            rangoAplicable = min(valorRestante, tarifa["rango2"] - tarifa["rango1"] + 0.01)
            impuesto = (rangoAplicable / 1000) * tarifa["valor"]
            
            impuestoTotal += impuesto
            detalleCalculo.append({
                "rango": f"{tarifa['rango1']:,.0f} - {tarifa['rango2']:,.0f}",
                "valor": rangoAplicable,
                "tarifa": tarifa["valor"],
                "impuesto": impuesto
            })
            
            valorRestante -= rangoAplicable
        
        return {
            "impuestoTotal": impuestoTotal,
            "detalleCalculo": detalleCalculo,
            "valorVentas": valorVentas
        }
    
    # Test con valor de 500,000
    valor_controlado = 500000.0
    resultado = calcularImpuestoICSControlados(valor_controlado)
    
    print(f"\n💰 CÁLCULO PRODUCTOS CONTROLADOS:")
    print(f"   Valor ingresado: L. {valor_controlado:,.2f}")
    print(f"   Impuesto calculado: L. {resultado['impuestoTotal']:.2f}")
    print(f"   Detalle: {resultado['detalleCalculo']}")
    
    # Verificar si está funcionando
    if resultado['impuestoTotal'] == 50.0:
        print("   ✅ CORRECTO: El cálculo individual funciona")
    else:
        print(f"   ❌ INCORRECTO: Esperado L. 50.00, obtenido L. {resultado['impuestoTotal']:.2f}")
    
    # Simular el flujo completo
    print(f"\n🔄 SIMULANDO FLUJO COMPLETO:")
    
    # Ventas Rubro Producción
    ventai = 500000.0
    impuesto_ventai = calcularImpuestoICS(ventai)
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    
    # Productos Controlados
    impuesto_controlado = resultado['impuestoTotal']
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    
    # Suma total
    suma_total = impuesto_ventai + impuesto_controlado
    print(f"   Suma total: L. {suma_total:.2f}")
    
    if suma_total == 200.0:
        print("   ✅ CORRECTO: La suma total es L. 200.00")
    else:
        print(f"   ❌ INCORRECTO: Esperado L. 200.00, obtenido L. {suma_total:.2f}")

def calcularImpuestoICS(valor_ventas):
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
            impuesto_total = (valor_ventas / 1000) * tarifa["valor"]
            break
    
    return impuesto_total

if __name__ == "__main__":
    test_debug_controlados()

#!/usr/bin/env python3
"""
Test completo del flujo de cálculos individuales y sumatoria
"""

def test_flujo_completo():
    print("🔍 TEST FLUJO COMPLETO DE CÁLCULOS")
    print("=" * 60)
    
    # Escenario de prueba
    print("\n📊 ESCENARIO DE PRUEBA:")
    print("   • Ventas Rubro Producción: 500,000.00")
    print("   • Productos Controlados: 500,000.00")
    print("   • Resultado esperado: L. 200.00")
    
    # Simular obtenerValoresVentas()
    print("\n🔍 SIMULANDO obtenerValoresVentas():")
    valores_ventas = {
        'ventai': 500000.0,
        'ventac': 0.0,
        'ventas': 0.0,
        'controlado': 500000.0,
        'unidad': 0.0,
        'factor': 0.0
    }
    print(f"   Valores obtenidos: {valores_ventas}")
    
    # Calcular impuestos individuales
    print("\n💰 CÁLCULOS INDIVIDUALES:")
    
    impuesto_ventai = calcular_impuesto_ics(valores_ventas['ventai'])
    impuesto_ventac = calcular_impuesto_ics(valores_ventas['ventac'])
    impuesto_ventas = calcular_impuesto_ics(valores_ventas['ventas'])
    impuesto_controlado = calcular_impuesto_ics_controlados(valores_ventas['controlado'])
    impuesto_unidad_factor = calcular_impuesto_unidad_factor(valores_ventas['unidad'], valores_ventas['factor'])
    
    print(f"   Ventas Rubro Producción: L. {impuesto_ventai:.2f}")
    print(f"   Ventas Mercadería: L. {impuesto_ventac:.2f}")
    print(f"   Ventas por Servicios: L. {impuesto_ventas:.2f}")
    print(f"   Productos Controlados: L. {impuesto_controlado:.2f}")
    print(f"   Factor × Unidad: L. {impuesto_unidad_factor:.2f}")
    
    # Calcular "Otros Impuestos"
    otros_impuestos = impuesto_ventai + impuesto_ventac + impuesto_ventas
    print(f"\n📊 OTROS IMPUESTOS (Producción + Mercadería + Servicios):")
    print(f"   {impuesto_ventai:.2f} + {impuesto_ventac:.2f} + {impuesto_ventas:.2f} = L. {otros_impuestos:.2f}")
    
    # Calcular suma total
    suma_total = impuesto_ventai + impuesto_ventac + impuesto_ventas + impuesto_controlado + impuesto_unidad_factor
    print(f"\n🎯 SUMA TOTAL DE IMPUESTOS INDEPENDIENTES:")
    print(f"   {impuesto_ventai:.2f} + {impuesto_ventac:.2f} + {impuesto_ventas:.2f} + {impuesto_controlado:.2f} + {impuesto_unidad_factor:.2f} = L. {suma_total:.2f}")
    
    # Verificar resultado
    print(f"\n✅ VERIFICACIÓN:")
    if suma_total == 200.0:
        print("   ✅ CORRECTO: La suma total es L. 200.00")
    else:
        print(f"   ❌ INCORRECTO: Esperado L. 200.00, obtenido L. {suma_total:.2f}")
        print(f"   Diferencia: L. {suma_total - 200:.2f}")
    
    # Verificar que no hay problema de 5000.00
    if otros_impuestos >= 5000:
        print(f"\n❌ PROBLEMA DETECTADO: Otros Impuestos = L. {otros_impuestos:.2f}")
        print("   Esto indica que hay un problema con la validación de ventai")
    else:
        print(f"\n✅ CORRECTO: Otros Impuestos = L. {otros_impuestos:.2f}")
        print("   No hay problema de 5000.00")

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

def calcular_impuesto_unidad_factor(valor_unidad, valor_factor):
    """Calcular impuesto Factor × Unidad"""
    if not valor_unidad or valor_unidad <= 0 or not valor_factor or valor_factor <= 0:
        return 0
    
    return valor_unidad * valor_factor

if __name__ == "__main__":
    test_flujo_completo()

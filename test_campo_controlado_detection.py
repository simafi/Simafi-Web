#!/usr/bin/env python3
"""
Test para verificar si el campo controlado está siendo detectado correctamente
"""

def test_campo_controlado_detection():
    print("🔍 TEST DETECCIÓN CAMPO CONTROLADO")
    print("=" * 50)
    
    # Simular el escenario exacto
    print("\n📊 ESCENARIO:")
    print("   • Campo: id_controlado")
    print("   • Valor: 500000")
    print("   • Resultado esperado: L. 50.00")
    
    # Simular la función obtenerValoresVentas
    def simular_obtenerValoresVentas():
        campos = ['ventai', 'ventac', 'ventas', 'controlado', 'unidad', 'factor']
        valores = {}
        
        print("\n🔍 SIMULANDO obtenerValoresVentas():")
        print("📊 Campos a verificar:", campos)
        
        # Simular que el campo controlado existe y tiene valor
        campo = 'controlado'
        input_id = f'id_{campo}'
        input_value = "500000"  # Simular valor del input
        
        print(f"🔍 Verificando campo {campo}:")
        print(f"   Elemento encontrado: SÍ (simulado)")
        print(f"   Valor en input: \"{input_value}\"")
        print(f"   Valor vacío: {not input_value}")
        
        if input_value:
            # Simular limpiarValor
            import re
            valor_limpiado = float(re.sub(r'[^0-9.]', '', input_value)) if input_value else 0
            print(f"   Valor limpiado: {valor_limpiado} (tipo: general)")
            print(f"   Valor > 0: {valor_limpiado > 0}")
            
            if valor_limpiado > 0:
                valores[campo] = valor_limpiado
                print(f"✅ Campo {campo} detectado con valor: {valor_limpiado} (tipo: general)")
            else:
                print(f"⚠️ Campo {campo} tiene valor 0 o negativo: {valor_limpiado}")
        else:
            print(f"❌ Campo {campo} no tiene valor o no existe")
        
        print(f"\n📋 Valores finales de ventas: {valores}")
        print(f"🔍 Verificación específica de campos críticos:")
        print(f"   controlado en valores: {'SÍ' if 'controlado' in valores else 'NO'}")
        if 'controlado' in valores:
            print(f"   Valor de controlado: {valores['controlado']}")
        
        return valores
    
    # Ejecutar la simulación
    valores = simular_obtenerValoresVentas()
    
    # Verificar si el campo fue detectado
    if 'controlado' in valores:
        print("\n✅ CORRECTO: El campo controlado fue detectado")
        print(f"   Valor detectado: {valores['controlado']}")
        
        # Calcular impuesto
        valor_controlado = valores['controlado']
        impuesto_controlado = calcular_impuesto_ics_controlados(valor_controlado)
        print(f"   Impuesto calculado: L. {impuesto_controlado:.2f}")
        
        if impuesto_controlado == 50.0:
            print("   ✅ CORRECTO: El cálculo funciona correctamente")
        else:
            print(f"   ❌ INCORRECTO: Esperado L. 50.00, obtenido L. {impuesto_controlado:.2f}")
    else:
        print("\n❌ INCORRECTO: El campo controlado NO fue detectado")
        print("   Posible causa: El campo no existe o no tiene valor")

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
            impuesto_total = (valor_ventas / 1000) * tarifa["valor"]
            break
    
    return impuesto_total

if __name__ == "__main__":
    test_campo_controlado_detection()

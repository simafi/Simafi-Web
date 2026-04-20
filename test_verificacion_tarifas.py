#!/usr/bin/env python3
"""
Test para verificar las tarifas de productos controlados
"""

def test_verificacion_tarifas():
    """Test específico para verificar las tarifas"""
    
    print("🧪 TEST VERIFICACIÓN DE TARIFAS")
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
    
    # Simular las tarifas para productos controlados (CORREGIDAS)
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return { 'impuestoTotal': 0 }
        
        # Tarifas corregidas para productos controlados
        if valorVentas <= 1000000:
            impuesto = valorVentas * 1.0 / 1000  # 1.0 por mil
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 1.5 / 1000  # 1.5 por mil
        else:
            impuesto = valorVentas * 2.0 / 1000  # 2.0 por mil
        
        return { 'impuestoTotal': round(impuesto, 2) }
    
    # Casos de prueba específicos
    casos_prueba = [
        {
            "nombre": "Ventas Rubro Producción: 500,000.00",
            "valor": 500000,
            "tipo": "normal",
            "esperado": 150.00
        },
        {
            "nombre": "Productos Controlados: 500,000.00",
            "valor": 500000,
            "tipo": "controlados",
            "esperado": 500.00
        },
        {
            "nombre": "Combinado: 500,000 + 500,000",
            "valor_ventai": 500000,
            "valor_controlado": 500000,
            "esperado_total": 650.00
        }
    ]
    
    print("\n📊 EJECUTANDO CASOS DE PRUEBA:")
    print("-" * 60)
    
    todos_pasan = True
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n🧪 {caso['nombre']}")
        
        if caso['tipo'] == 'normal':
            resultado = calcularImpuestoICS(caso['valor'])
            print(f"   Valor: {caso['valor']:,}")
            print(f"   Resultado: L. {resultado['impuestoTotal']:.2f}")
            print(f"   Esperado: L. {caso['esperado']:.2f}")
            
            if abs(resultado['impuestoTotal'] - caso['esperado']) < 0.01:
                print(f"   ✅ CORRECTO")
            else:
                print(f"   ❌ ERROR")
                todos_pasan = False
                
        elif caso['tipo'] == 'controlados':
            resultado = calcularImpuestoICSControlados(caso['valor'])
            print(f"   Valor: {caso['valor']:,}")
            print(f"   Resultado: L. {resultado['impuestoTotal']:.2f}")
            print(f"   Esperado: L. {caso['esperado']:.2f}")
            
            if abs(resultado['impuestoTotal'] - caso['esperado']) < 0.01:
                print(f"   ✅ CORRECTO")
            else:
                print(f"   ❌ ERROR")
                todos_pasan = False
                
        else:  # combinado
            ventai = calcularImpuestoICS(caso['valor_ventai'])
            controlados = calcularImpuestoICSControlados(caso['valor_controlado'])
            total = ventai['impuestoTotal'] + controlados['impuestoTotal']
            
            print(f"   Ventas Rubro Producción: {caso['valor_ventai']:,} → L. {ventai['impuestoTotal']:.2f}")
            print(f"   Productos Controlados: {caso['valor_controlado']:,} → L. {controlados['impuestoTotal']:.2f}")
            print(f"   Total: L. {total:.2f}")
            print(f"   Esperado: L. {caso['esperado_total']:.2f}")
            
            if abs(total - caso['esperado_total']) < 0.01:
                print(f"   ✅ CORRECTO")
            else:
                print(f"   ❌ ERROR")
                todos_pasan = False
    
    print("\n" + "=" * 60)
    if todos_pasan:
        print("✅ TODAS LAS TARIFAS SON CORRECTAS")
        print("🎯 El problema puede estar en la implementación del formulario")
    else:
        print("❌ HAY ERRORES EN LAS TARIFAS")
        print("🔧 Necesita corrección")
    
    return todos_pasan

def verificar_tarifas_formulario():
    """Verificar las tarifas en el formulario"""
    
    print("\n🔍 VERIFICACIÓN DE TARIFAS EN EL FORMULARIO")
    print("=" * 60)
    
    print("\n📋 TARIFAS NORMALES ICS:")
    print("• $0 - $500,000: 0.3 por mil")
    print("• $500,000 - $10,000,000: 0.4 por mil")
    print("• $10,000,000+: 0.3 por mil")
    
    print("\n📋 TARIFAS PRODUCTOS CONTROLADOS:")
    print("• $0 - $1,000,000: 1.0 por mil")
    print("• $1,000,000 - $5,000,000: 1.5 por mil")
    print("• $5,000,000+: 2.0 por mil")
    
    print("\n🧮 CÁLCULOS ESPERADOS:")
    print("• Ventas Rubro Producción: 500,000 × 0.3/1000 = 150.00")
    print("• Productos Controlados: 500,000 × 1.0/1000 = 500.00")
    print("• Total combinado: 150.00 + 500.00 = 650.00")
    
    print("\n❌ PROBLEMA IDENTIFICADO:")
    print("Si productos controlados da 50.00 en lugar de 500.00,")
    print("hay un error en la función calcularImpuestoICSControlados")
    print("o en las tarifas definidas en el formulario.")

if __name__ == "__main__":
    print("🧪 INICIANDO TEST VERIFICACIÓN DE TARIFAS...")
    print()
    
    if test_verificacion_tarifas():
        print("\n✅ LAS TARIFAS ESTÁN CORRECTAS")
        print("🎯 El problema está en la implementación del formulario")
    else:
        print("\n❌ HAY ERRORES EN LAS TARIFAS")
        print("🔧 Necesita corrección")
    
    verificar_tarifas_formulario()

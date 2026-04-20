#!/usr/bin/env python3
"""
Script de prueba para el campo ajuste interanual
"""

def probar_funcionamiento_ajuste():
    """Prueba el funcionamiento del campo ajuste"""
    
    print("🧪 PRUEBA DE FUNCIONAMIENTO - CAMPO AJUSTE")
    print("=" * 50)
    
    print("\n📋 CASOS DE PRUEBA:")
    
    casos_prueba = [
        {
            "descripcion": "Ajuste positivo",
            "ajuste": 1000.00,
            "esperado": "Se suma al total de impuestos"
        },
        {
            "descripcion": "Ajuste negativo",
            "ajuste": -500.00,
            "esperado": "Se resta del total de impuestos"
        },
        {
            "descripcion": "Ajuste cero",
            "ajuste": 0.00,
            "esperado": "No afecta el total de impuestos"
        },
        {
            "descripcion": "Ajuste decimal",
            "ajuste": 123.45,
            "esperado": "Se suma con precisión decimal"
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n{i}. {caso['descripcion']}:")
        print(f"   Valor: L. {caso['ajuste']:,.2f}")
        print(f"   Esperado: {caso['esperado']}")
    
    print("\n🎯 INSTRUCCIONES PARA PROBAR:")
    print("1. Accede al formulario de declaración de volumen")
    print("2. Ingresa valores en los campos de ventas")
    print("3. Ingresa un valor en el campo 'Ajuste Interanual'")
    print("4. Verifica en la consola del navegador (F12) que aparezca:")
    print("   - '📊 Ajuste Interanual: L. X.XX'")
    print("   - '• Ajuste Interanual: L. X.XX' en la sumatoria")
    print("5. Verifica que el total de impuestos incluya el ajuste")
    
    print("\n✅ VERIFICACIONES:")
    print("- El campo debe tener fondo morado distintivo")
    print("- El valor debe sumarse directamente al total")
    print("- Los logs deben mostrar el ajuste correctamente")
    print("- El campo debe ser editable (no readonly)")

if __name__ == "__main__":
    probar_funcionamiento_ajuste()

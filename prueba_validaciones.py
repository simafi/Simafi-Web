#!/usr/bin/env python3
"""
Script de prueba para las validaciones del formulario
"""

def probar_validaciones():
    """Prueba las validaciones implementadas"""
    
    print("🧪 PRUEBA DE VALIDACIONES")
    print("=" * 50)
    
    print("\n📋 CASOS DE PRUEBA:")
    
    casos_prueba = [
        {
            "descripcion": "RTM vacío",
            "rtm": "",
            "expe": "12345",
            "ventas": 1000,
            "esperado": "Error: RTM es obligatorio"
        },
        {
            "descripcion": "EXPE vacío",
            "rtm": "12345",
            "expe": "",
            "ventas": 1000,
            "esperado": "Error: Expediente es obligatorio"
        },
        {
            "descripcion": "Sin valores de ventas",
            "rtm": "12345",
            "expe": "67890",
            "ventas": 0,
            "esperado": "Error: Al menos uno de los campos de ventas debe tener un valor mayor a 0"
        },
        {
            "descripcion": "Impuesto cero",
            "rtm": "12345",
            "expe": "67890",
            "ventas": 1000,
            "impuesto": 0,
            "esperado": "Error: El impuesto calculado debe ser mayor a 0"
        },
        {
            "descripcion": "Formulario válido",
            "rtm": "12345",
            "expe": "67890",
            "ventas": 1000,
            "impuesto": 150,
            "esperado": "Formulario válido - Se puede guardar"
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n{i}. {caso['descripcion']}:")
        print(f"   RTM: '{caso['rtm']}'")
        print(f"   EXPE: '{caso['expe']}'")
        print(f"   Ventas: {caso['ventas']}")
        if 'impuesto' in caso:
            print(f"   Impuesto: {caso['impuesto']}")
        print(f"   Esperado: {caso['esperado']}")
    
    print("\n🎯 INSTRUCCIONES PARA PROBAR:")
    print("1. Accede al formulario de declaración de volumen")
    print("2. Prueba cada caso de prueba:")
    print("   a) Deja RTM vacío y intenta guardar")
    print("   b) Deja EXPE vacío y intenta guardar")
    print("   c) No ingreses valores de ventas y intenta guardar")
    print("   d) Ingresa valores pero no calcules impuesto e intenta guardar")
    print("   e) Completa todo correctamente e intenta guardar")
    print("3. Verifica que aparezcan los mensajes de error apropiados")
    print("4. Verifica que el formulario no se envíe con datos inválidos")
    
    print("\n✅ VERIFICACIONES:")
    print("- Los mensajes de error deben ser claros y específicos")
    print("- El formulario no debe enviarse con datos inválidos")
    print("- Los campos obligatorios deben estar marcados")
    print("- Las validaciones deben funcionar tanto en Django como en JavaScript")

if __name__ == "__main__":
    probar_validaciones()

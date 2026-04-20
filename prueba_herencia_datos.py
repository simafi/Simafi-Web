#!/usr/bin/env python3
"""
Script de prueba para la herencia de datos RTM, EXPE e ID del negocio
"""

def probar_herencia_datos():
    """Prueba que los datos se hereden correctamente"""
    
    print("🧪 PRUEBA DE HERENCIA DE DATOS")
    print("=" * 50)
    
    print("\n📋 CASOS DE PRUEBA:")
    
    casos_prueba = [
        {
            "descripcion": "Acceso con RTM y EXPE válidos",
            "url": "/tributario/declaracion-volumen/?rtm=12345&expe=67890",
            "esperado": "Los campos se llenan automáticamente"
        },
        {
            "descripcion": "Acceso sin RTM y EXPE",
            "url": "/tributario/declaracion-volumen/",
            "esperado": "Los campos aparecen vacíos"
        },
        {
            "descripcion": "Negocio no encontrado",
            "url": "/tributario/declaracion-volumen/?rtm=99999&expe=99999",
            "esperado": "Mensaje de error apropiado"
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n{i}. {caso['descripcion']}:")
        print(f"   URL: {caso['url']}")
        print(f"   Esperado: {caso['esperado']}")
    
    print("\n🎯 INSTRUCCIONES PARA PROBAR:")
    print("1. Accede a la URL con parámetros RTM y EXPE:")
    print("   /tributario/declaracion-volumen/?rtm=12345&expe=67890")
    print("2. Verifica que en la sección 'Información del Negocio' aparezcan:")
    print("   - RTM: 12345")
    print("   - Expediente: 67890")
    print("3. Verifica que en la sección 'Información Básica' aparezcan:")
    print("   - ID Negocio: [ID del negocio]")
    print("   - RTM: 12345")
    print("   - Expediente: 67890")
    print("4. Verifica que los campos estén readonly (no editables)")
    print("5. Verifica que los valores coincidan entre ambas secciones")
    
    print("\n✅ VERIFICACIONES:")
    print("- Los campos deben tener el mismo valor en ambas secciones")
    print("- Los campos deben ser readonly (no editables)")
    print("- El ID del negocio debe ser numérico")
    print("- No debe haber errores en la consola del navegador")

if __name__ == "__main__":
    probar_herencia_datos()

#!/usr/bin/env python3
"""
Script de prueba para verificar datos del negocio
"""

def probar_datos_negocio():
    """Prueba que los datos del negocio se estén pasando correctamente"""
    
    print("🧪 PRUEBA DE DATOS DEL NEGOCIO")
    print("=" * 40)
    
    # Simular datos de prueba
    rtm_prueba = "TEST001"
    expe_prueba = "EXP001"
    
    print(f"RTM de prueba: {rtm_prueba}")
    print(f"Expediente de prueba: {expe_prueba}")
    
    # Simular URL de prueba
    url_prueba = f"/tributario/declaracion-volumen/?rtm={rtm_prueba}&expe={expe_prueba}"
    print(f"URL de prueba: {url_prueba}")
    
    print("\n✅ Para probar:")
    print("1. Accede a la URL de prueba")
    print("2. Verifica que los campos se llenen automáticamente:")
    print("   - ID Negocio: debe mostrar el ID real")
    print("   - RTM: debe mostrar TEST001")
    print("   - Expediente: debe mostrar EXP001")
    print("3. Verifica que la información del negocio se muestre")
    print("4. Prueba el cálculo de productos controlados")

if __name__ == "__main__":
    probar_datos_negocio()

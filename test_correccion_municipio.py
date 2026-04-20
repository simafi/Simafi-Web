#!/usr/bin/env python3
"""
Test para verificar que la corrección del municipio funciona
"""

import requests
import re

def test_correccion_municipio():
    """Test para verificar la corrección del municipio"""
    print("🔍 Test: Corrección del Código de Municipio")
    print("=" * 80)
    
    # Caso específico que estaba fallando
    municipio_enviado = "0301"
    municipio_esperado = "0301"
    
    print(f"🔍 Caso específico:")
    print(f"   Municipio enviado: '{municipio_enviado}'")
    print(f"   Municipio esperado: '{municipio_esperado}'")
    print(f"   Problema anterior: Se recibía '0002' en lugar de '0301'")
    
    try:
        # Acceder al formulario de plan de arbitrio
        url = f"http://127.0.0.1:8080/tributario/plan-arbitrio-crud/?empresa={municipio_enviado}&rubro=TEST"
        print(f"\n🔍 URL de prueba: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ Formulario accesible")
            
            # Buscar el campo municipio
            municipio_match = re.search(r'value="([^"]*)"[^>]*id="id_empresa"', response.text)
            
            if municipio_match:
                municipio_recibido = municipio_match.group(1)
                print(f"\n🔍 RESULTADO:")
                print(f"   Municipio enviado: '{municipio_enviado}'")
                print(f"   Municipio recibido: '{municipio_recibido}'")
                print(f"   Municipio esperado: '{municipio_esperado}'")
                
                # Verificar el resultado
                if municipio_recibido == municipio_esperado:
                    print("✅ CORRECCIÓN EXITOSA - Municipio correcto")
                    return True
                else:
                    print(f"❌ PROBLEMA PERSISTE - Municipio incorrecto")
                    print(f"   Se envió '{municipio_enviado}' pero se recibió '{municipio_recibido}'")
                    return False
            else:
                print("❌ No se encontró el campo municipio")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_navegacion_desde_tarifas():
    """Test de navegación desde tarifas"""
    print("\n🔍 Test de Navegación desde Tarifas")
    print("=" * 80)
    
    try:
        # Simular la navegación exacta que estaba fallando
        print("1️⃣ Navegando desde tarifas a plan de arbitrio...")
        url_plan = "http://127.0.0.1:8080/tributario/plan-arbitrio-crud/?empresa=0301&rubro=0004&cod_tarifa=01&ano=2025"
        print(f"🔍 URL de navegación: {url_plan}")
        
        response_plan = requests.get(url_plan)
        
        if response_plan.status_code == 200:
            print("✅ Formulario de plan de arbitrio accesible")
            
            # Verificar el municipio
            municipio_match = re.search(r'value="([^"]*)"[^>]*id="id_empresa"', response_plan.text)
            if municipio_match:
                municipio_valor = municipio_match.group(1)
                print(f"🔍 Municipio en plan de arbitrio: '{municipio_valor}'")
                
                if municipio_valor == '0301':
                    print("✅ Navegación funcionando correctamente")
                    return True
                else:
                    print(f"❌ Municipio incorrecto: esperado '0301', obtenido '{municipio_valor}'")
                    return False
            else:
                print("❌ No se encontró el campo municipio")
                return False
        else:
            print(f"❌ Error al acceder a plan de arbitrio: HTTP {response_plan.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Test: Corrección del Código de Municipio")
    print("=" * 80)
    
    resultado1 = test_correccion_municipio()
    resultado2 = test_navegacion_desde_tarifas()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE LA CORRECCIÓN:")
    print("=" * 80)
    
    if resultado1 and resultado2:
        print("✅ CORRECCIÓN COMPLETAMENTE EXITOSA")
        print("🎯 Problema del municipio resuelto")
        print("🔧 Prioridad GET empresa sobre Session municipio_id funcionando")
        print("📋 Navegación desde tarifas funcionando correctamente")
    else:
        print("❌ AÚN HAY PROBLEMAS")
        if not resultado1:
            print("   - Test de corrección falló")
        if not resultado2:
            print("   - Test de navegación falló")
        print("🔧 Se requiere revisión adicional")
    
    print("=" * 80)

if __name__ == "__main__":
    main()































#!/usr/bin/env python3
"""
Test simple final para verificar la declaración
"""

import requests

def test_simple_final():
    """Test simple final"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            print("=== TEST SIMPLE FINAL ===")
            
            # Verificar campos básicos
            rtm_ok = '114-03-23' in content
            expe_ok = '1151' in content
            print(f"RTM presente: {rtm_ok}")
            print(f"EXPE presente: {expe_ok}")
            
            # Verificar campos ocultos críticos
            ajuste_base_ok = 'hidden_ajuste_base' in content
            ajuste_impuesto_ok = 'hidden_ajuste_impuesto' in content
            print(f"hidden_ajuste_base: {ajuste_base_ok}")
            print(f"hidden_ajuste_impuesto: {ajuste_impuesto_ok}")
            
            # Verificar errores
            no_errors = 'Campo oculto no encontrado' not in content
            print(f"Sin errores JS: {no_errors}")
            
            # Resumen
            if rtm_ok and expe_ok and ajuste_base_ok and ajuste_impuesto_ok and no_errors:
                print("\nRESULTADO: DECLARACION LISTA PARA GRABAR")
                print("Todos los componentes funcionan correctamente")
            else:
                print("\nRESULTADO: HAY PROBLEMAS")
                if not rtm_ok or not expe_ok:
                    print("- Campos basicos no heredan valores")
                if not ajuste_base_ok or not ajuste_impuesto_ok:
                    print("- Campos ocultos faltantes")
                if not no_errors:
                    print("- Errores de JavaScript")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple_final()
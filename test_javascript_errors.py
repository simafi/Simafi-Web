#!/usr/bin/env python3
"""
Test específico para verificar errores de JavaScript
"""

import requests
import re

def test_javascript_errors():
    """Test específico para verificar errores de JavaScript"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            print("\n=== TEST DE ERRORES JAVASCRIPT ===")
            
            # Buscar errores específicos de JavaScript
            errores_js = [
                'Campo oculto no encontrado',
                'hidden_ajuste_base',
                'hidden_ajuste_impuesto',
                'VariableDoesNotExist',
                'Failed lookup for key',
                'console.warn',
                'console.error'
            ]
            
            print("1. Verificando errores de JavaScript...")
            errores_encontrados = 0
            for error in errores_js:
                if error in content:
                    print(f"   ERROR: {error} encontrado")
                    errores_encontrados += 1
                else:
                    print(f"   OK: {error} no encontrado")
            
            # Verificar que los campos ocultos estén en el HTML
            print("\n2. Verificando campos ocultos en HTML...")
            campos_ocultos = [
                'id="hidden_ajuste_base"',
                'id="hidden_ajuste_impuesto"',
                'id="hidden_ventai_base"',
                'id="hidden_ventai_impuesto"'
            ]
            
            campos_encontrados = 0
            for campo in campos_ocultos:
                if campo in content:
                    print(f"   OK: {campo}")
                    campos_encontrados += 1
                else:
                    print(f"   ERROR: {campo} no encontrado")
            
            # Verificar que no haya errores de template
            print("\n3. Verificando errores de template...")
            if 'VariableDoesNotExist' in content:
                print("   ERROR: Error de template VariableDoesNotExist")
            else:
                print("   OK: No hay errores de template")
            
            # Resumen final
            print("\n=== RESUMEN JAVASCRIPT ===")
            if errores_encontrados == 0 and campos_encontrados == len(campos_ocultos):
                print("RESULTADO: JAVASCRIPT FUNCIONANDO CORRECTAMENTE")
                print("- Sin errores de JavaScript")
                print("- Campos ocultos presentes")
                print("- Sin errores de template")
                print("- Declaración lista para grabar")
            else:
                print("RESULTADO: HAY PROBLEMAS DE JAVASCRIPT")
                if errores_encontrados > 0:
                    print(f"- {errores_encontrados} errores de JavaScript encontrados")
                if campos_encontrados < len(campos_ocultos):
                    print("- Campos ocultos faltantes")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_javascript_errors()



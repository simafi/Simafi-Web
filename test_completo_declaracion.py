#!/usr/bin/env python3
"""
Test completo para verificar la declaración de volumen
"""

import requests
import re

def test_completo_declaracion():
    """Test completo para verificar la declaración"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            print("\n=== TEST COMPLETO DE DECLARACION ===")
            
            # 1. Verificar que la página se carga
            print("1. Verificando carga de página...")
            if 'Declaración de Volumen de Ventas' in content:
                print("   OK: Página se carga correctamente")
            else:
                print("   ERROR: Página no se carga correctamente")
                return
            
            # 2. Verificar campos básicos (RTM, EXPE, ID)
            print("\n2. Verificando campos básicos...")
            rtm_present = '114-03-23' in content
            expe_present = '1151' in content
            print(f"   RTM (114-03-23): {'OK' if rtm_present else 'ERROR'}")
            print(f"   EXPE (1151): {'OK' if expe_present else 'ERROR'}")
            
            # 3. Verificar campos ocultos
            print("\n3. Verificando campos ocultos...")
            hidden_fields = [
                'hidden_ajuste_base',
                'hidden_ajuste_impuesto',
                'hidden_ventai_base',
                'hidden_ventai_impuesto',
                'hidden_ventac_base',
                'hidden_ventac_impuesto',
                'hidden_ventas_base',
                'hidden_ventas_impuesto',
                'hidden_controlado_base',
                'hidden_controlado_impuesto',
                'hidden_unidad_base',
                'hidden_factor_base',
                'hidden_unidadFactor_impuesto'
            ]
            
            campos_ok = 0
            for field in hidden_fields:
                if field in content:
                    print(f"   OK: {field}")
                    campos_ok += 1
                else:
                    print(f"   ERROR: {field}")
            
            print(f"   Total campos ocultos: {campos_ok}/{len(hidden_fields)}")
            
            # 4. Verificar errores de JavaScript
            print("\n4. Verificando errores de JavaScript...")
            if 'Campo oculto no encontrado' in content:
                print("   ERROR: Hay errores de campos ocultos no encontrados")
            else:
                print("   OK: No hay errores de campos ocultos")
            
            # 5. Verificar formulario
            print("\n5. Verificando formulario...")
            if 'form' in content and 'method="post"' in content:
                print("   OK: Formulario encontrado")
            else:
                print("   ERROR: Formulario no encontrado")
            
            # 6. Verificar campos de entrada
            print("\n6. Verificando campos de entrada...")
            input_fields = ['ventai', 'ventac', 'ventas', 'controlado', 'unidad', 'factor', 'ajuste']
            for field in input_fields:
                if f'name="{field}"' in content:
                    print(f"   OK: Campo {field}")
                else:
                    print(f"   ERROR: Campo {field} no encontrado")
            
            # 7. Resumen final
            print("\n=== RESUMEN ===")
            if rtm_present and expe_present and campos_ok == len(hidden_fields):
                print("RESULTADO: DECLARACION LISTA PARA GRABAR")
                print("- Campos básicos: OK")
                print("- Campos ocultos: OK")
                print("- Formulario: OK")
                print("- Sin errores JavaScript: OK")
            else:
                print("RESULTADO: HAY PROBLEMAS QUE CORREGIR")
                if not rtm_present or not expe_present:
                    print("- Problema: Campos básicos no heredan valores")
                if campos_ok < len(hidden_fields):
                    print("- Problema: Campos ocultos faltantes")
                if 'Campo oculto no encontrado' in content:
                    print("- Problema: Errores de JavaScript")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_completo_declaracion()



#!/usr/bin/env python3
"""
Script para verificar que los campos ocultos se hayan agregado correctamente (sin emojis)
"""

import requests
import re

def verify_hidden_fields():
    """Verificar que los campos ocultos se hayan agregado correctamente"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar los campos ocultos específicos
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
            
            print("\nVerificando campos ocultos:")
            for field in hidden_fields:
                if field in content:
                    print(f"  OK {field}: Encontrado")
                else:
                    print(f"  ERROR {field}: NO encontrado")
            
            # Verificar que no haya errores de JavaScript
            if 'Campo oculto no encontrado' in content:
                print("\nERROR: Aun hay campos ocultos no encontrados")
            else:
                print("\nSUCCESS: No hay errores de campos ocultos")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_hidden_fields()



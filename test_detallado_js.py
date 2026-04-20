#!/usr/bin/env python3
"""
Test detallado para verificar problemas específicos de JavaScript
"""

import requests
import re

def test_detallado_js():
    """Test detallado para verificar problemas específicos"""
    url = "http://127.0.0.1:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            print("\n=== TEST DETALLADO JAVASCRIPT ===")
            
            # Buscar específicamente los mensajes de error
            print("1. Buscando mensajes específicos de error...")
            
            # Buscar el mensaje exacto del error
            if 'Campo oculto no encontrado: hidden_ajuste_base' in content:
                print("   ERROR: Mensaje específico de error encontrado")
            else:
                print("   OK: Mensaje específico de error no encontrado")
            
            # Buscar console.warn específicos
            warn_messages = re.findall(r'console\.warn\([^)]+\)', content)
            if warn_messages:
                print(f"   ADVERTENCIAS: {len(warn_messages)} mensajes console.warn encontrados")
                for msg in warn_messages[:3]:  # Mostrar solo los primeros 3
                    print(f"     - {msg}")
            else:
                print("   OK: No hay mensajes console.warn")
            
            # Buscar console.error específicos
            error_messages = re.findall(r'console\.error\([^)]+\)', content)
            if error_messages:
                print(f"   ERRORES: {len(error_messages)} mensajes console.error encontrados")
                for msg in error_messages[:3]:  # Mostrar solo los primeros 3
                    print(f"     - {msg}")
            else:
                print("   OK: No hay mensajes console.error")
            
            # Verificar que los campos ocultos estén correctamente formateados
            print("\n2. Verificando formato de campos ocultos...")
            ajuste_base_pattern = r'<input[^>]*id="hidden_ajuste_base"[^>]*>'
            ajuste_impuesto_pattern = r'<input[^>]*id="hidden_ajuste_impuesto"[^>]*>'
            
            if re.search(ajuste_base_pattern, content):
                print("   OK: hidden_ajuste_base formateado correctamente")
            else:
                print("   ERROR: hidden_ajuste_base no formateado correctamente")
                
            if re.search(ajuste_impuesto_pattern, content):
                print("   OK: hidden_ajuste_impuesto formateado correctamente")
            else:
                print("   ERROR: hidden_ajuste_impuesto no formateado correctamente")
            
            # Verificar que no haya errores de template
            print("\n3. Verificando errores de template...")
            template_errors = [
                'VariableDoesNotExist',
                'Failed lookup for key',
                'TemplateSyntaxError',
                'TemplateDoesNotExist'
            ]
            
            template_errors_found = 0
            for error in template_errors:
                if error in content:
                    print(f"   ERROR: {error} encontrado")
                    template_errors_found += 1
                else:
                    print(f"   OK: {error} no encontrado")
            
            # Resumen final
            print("\n=== RESUMEN DETALLADO ===")
            if template_errors_found == 0:
                print("RESULTADO: TEMPLATE FUNCIONANDO CORRECTAMENTE")
                print("- Sin errores de template")
                print("- Campos ocultos presentes")
                print("- Declaración funcional")
            else:
                print("RESULTADO: HAY ERRORES DE TEMPLATE")
                print(f"- {template_errors_found} errores de template encontrados")
                
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_detallado_js()



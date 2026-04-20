#!/usr/bin/env python3
"""
Test de verificación limpio para el problema del municipio en plan de arbitrio
"""

import requests
import re
import time

def test_municipio_limpio():
    """Test limpio para verificar el municipio"""
    print("🔍 Test Limpio: Verificación del Código de Municipio")
    print("=" * 80)
    
    # Esperar un momento para que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    time.sleep(3)
    
    # Test específico con el problema reportado
    municipio_test = "0301"
    print(f"🔍 Probando municipio: '{municipio_test}'")
    
    try:
        # Acceder directamente al formulario de plan de arbitrio
        url = f"http://127.0.0.1:8080/tributario/plan-arbitrio-crud/?empresa={municipio_test}&rubro=TEST"
        print(f"🔍 URL: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ Formulario accesible")
            
            # Buscar el campo municipio
            municipio_match = re.search(r'value="([^"]*)"[^>]*id="id_empresa"', response.text)
            
            if municipio_match:
                municipio_valor = municipio_match.group(1)
                print(f"🔍 RESULTADO:")
                print(f"   Municipio enviado: '{municipio_test}'")
                print(f"   Municipio recibido: '{municipio_valor}'")
                print(f"   Longitud recibido: {len(municipio_valor)}")
                print(f"   ¿Son iguales?: {municipio_test == municipio_valor}")
                
                if municipio_valor == municipio_test:
                    print("✅ Municipio correcto")
                    return True
                else:
                    print("❌ Municipio incorrecto - PROBLEMA CONFIRMADO")
                    print(f"   Diferencia: '{municipio_test}' vs '{municipio_valor}'")
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

def test_navegacion_desde_tarifas_limpio():
    """Test de navegación limpio desde tarifas"""
    print("\n🔍 Test de Navegación Limpio desde Tarifas")
    print("=" * 80)
    
    try:
        # Paso 1: Acceder a tarifas
        print("1️⃣ Accediendo a formulario de tarifas...")
        response_tarifas = requests.get('http://127.0.0.1:8080/tributario/tarifas-crud/')
        
        if response_tarifas.status_code == 200:
            print("✅ Formulario de tarifas accesible")
            
            # Paso 2: Navegar a plan de arbitrio
            print("2️⃣ Navegando a plan de arbitrio...")
            url_plan = "http://127.0.0.1:8080/tributario/plan-arbitrio-crud/?empresa=0301&rubro=TEST&ano=2024&cod_tarifa=TAR1"
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
        else:
            print(f"❌ Error al acceder a tarifas: HTTP {response_tarifas.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_diferentes_municipios():
    """Test con diferentes municipios para verificar el patrón"""
    print("\n🔍 Test con Diferentes Municipios")
    print("=" * 80)
    
    municipios_test = [
        {'enviado': '0301', 'esperado': '0301', 'desc': 'Municipio reportado'},
        {'enviado': '0002', 'esperado': '0002', 'desc': 'Municipio que aparece'},
        {'enviado': '1', 'esperado': '0001', 'desc': 'Municipio 1 dígito'},
        {'enviado': '12', 'esperado': '0012', 'desc': 'Municipio 2 dígitos'},
    ]
    
    resultados = []
    
    for municipio in municipios_test:
        print(f"\n🔍 Probando: {municipio['desc']}")
        
        try:
            url = f"http://127.0.0.1:8080/tributario/plan-arbitrio-crud/?empresa={municipio['enviado']}&rubro=TEST"
            response = requests.get(url)
            
            if response.status_code == 200:
                match = re.search(r'value="([^"]*)"[^>]*id="id_empresa"', response.text)
                if match:
                    valor_recibido = match.group(1)
                    print(f"   Enviado: '{municipio['enviado']}' → Recibido: '{valor_recibido}' → Esperado: '{municipio['esperado']}'")
                    
                    if valor_recibido == municipio['esperado']:
                        print(f"   ✅ {municipio['desc']}: CORRECTO")
                        resultados.append(True)
                    else:
                        print(f"   ❌ {municipio['desc']}: INCORRECTO")
                        resultados.append(False)
                else:
                    print(f"   ❌ {municipio['desc']}: No encontrado")
                    resultados.append(False)
            else:
                print(f"   ❌ {municipio['desc']}: Error HTTP {response.status_code}")
                resultados.append(False)
        except Exception as e:
            print(f"   ❌ {municipio['desc']}: Error {e}")
            resultados.append(False)
    
    return resultados

def main():
    """Función principal"""
    print("🔍 Test Limpio: Verificación del Código de Municipio")
    print("=" * 80)
    
    resultado1 = test_municipio_limpio()
    resultado2 = test_navegacion_desde_tarifas_limpio()
    resultados3 = test_diferentes_municipios()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE VERIFICACIÓN LIMPIA:")
    print("=" * 80)
    
    exitosos = sum([resultado1, resultado2] + resultados3)
    total = 2 + len(resultados3)
    
    if exitosos == total:
        print("✅ TODOS LOS TESTS EXITOSOS")
        print("🎯 No se encontró el problema reportado")
    else:
        print(f"❌ {total - exitosos} TESTS FALLARON")
        print("🔍 PROBLEMA CONFIRMADO - Revisar logs anteriores")
        
        if not resultado1:
            print("   - Test de municipio limpio falló")
        if not resultado2:
            print("   - Test de navegación limpio falló")
        
        # Mostrar resultados específicos de diferentes municipios
        municipios_test = [
            {'enviado': '0301', 'esperado': '0301', 'desc': 'Municipio reportado'},
            {'enviado': '0002', 'esperado': '0002', 'desc': 'Municipio que aparece'},
            {'enviado': '1', 'esperado': '0001', 'desc': 'Municipio 1 dígito'},
            {'enviado': '12', 'esperado': '0012', 'desc': 'Municipio 2 dígitos'},
        ]
        
        for i, resultado in enumerate(resultados3):
            if not resultado:
                print(f"   - Test de {municipios_test[i]['desc']} falló")
    
    print(f"\n📈 Resultado: {exitosos}/{total} tests exitosos")
    print("=" * 80)

if __name__ == "__main__":
    main()































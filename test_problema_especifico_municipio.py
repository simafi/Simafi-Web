#!/usr/bin/env python3
"""
Test específico para el problema del municipio reportado por el usuario
"""

import requests
import re
import time

def test_problema_especifico():
    """Test específico para el problema reportado"""
    print("🔍 Test Específico: Problema del Municipio Reportado")
    print("=" * 80)
    
    # Esperar que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    time.sleep(5)
    
    # Caso específico reportado por el usuario
    municipio_enviado = "0301"
    municipio_esperado = "0301"
    municipio_problema = "0002"  # El que aparece incorrectamente
    
    print(f"🔍 Caso específico:")
    print(f"   Municipio enviado: '{municipio_enviado}'")
    print(f"   Municipio esperado: '{municipio_esperado}'")
    print(f"   Municipio problema: '{municipio_problema}'")
    
    try:
        # Acceder al formulario de plan de arbitrio
        url = f"http://127.0.0.1:8080/tributario/plan-arbitrio-crud/?empresa={municipio_enviado}&rubro=TEST"
        print(f"\n🔍 URL de prueba: {url}")
        
        response = requests.get(url, timeout=10)
        
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
                print(f"   Municipio problema: '{municipio_problema}'")
                
                # Verificar el resultado
                if municipio_recibido == municipio_esperado:
                    print("✅ Municipio correcto - No hay problema")
                    return True
                elif municipio_recibido == municipio_problema:
                    print("❌ PROBLEMA CONFIRMADO - Municipio incorrecto")
                    print(f"   Se envió '{municipio_enviado}' pero se recibió '{municipio_recibido}'")
                    return False
                else:
                    print(f"❌ PROBLEMA DIFERENTE - Municipio inesperado")
                    print(f"   Se envió '{municipio_enviado}' pero se recibió '{municipio_recibido}'")
                    return False
            else:
                print("❌ No se encontró el campo municipio")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - Servidor no disponible")
        print("   Verificar que el servidor esté corriendo en puerto 8080")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_navegacion_real():
    """Test de navegación real desde tarifas"""
    print("\n🔍 Test de Navegación Real desde Tarifas")
    print("=" * 80)
    
    try:
        # Paso 1: Acceder a tarifas
        print("1️⃣ Accediendo a formulario de tarifas...")
        response_tarifas = requests.get('http://127.0.0.1:8080/tributario/tarifas-crud/', timeout=10)
        
        if response_tarifas.status_code == 200:
            print("✅ Formulario de tarifas accesible")
            
            # Buscar si hay tarifas con municipio 0301
            if '0301' in response_tarifas.text:
                print("✅ Municipio 0301 encontrado en tarifas")
            else:
                print("❌ Municipio 0301 no encontrado en tarifas")
            
            # Paso 2: Navegar a plan de arbitrio
            print("2️⃣ Navegando a plan de arbitrio...")
            url_plan = "http://127.0.0.1:8080/tributario/plan-arbitrio-crud/?empresa=0301&rubro=TEST&ano=2024&cod_tarifa=TAR1"
            print(f"🔍 URL de navegación: {url_plan}")
            
            response_plan = requests.get(url_plan, timeout=10)
            
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
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - Servidor no disponible")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Test Específico: Problema del Municipio")
    print("=" * 80)
    
    resultado1 = test_problema_especifico()
    resultado2 = test_navegacion_real()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DEL PROBLEMA:")
    print("=" * 80)
    
    if resultado1 and resultado2:
        print("✅ NO SE ENCONTRÓ EL PROBLEMA")
        print("🎯 El municipio está funcionando correctamente")
        print("🔍 Verificar si el problema es en el navegador o cache")
    else:
        print("❌ PROBLEMA CONFIRMADO")
        if not resultado1:
            print("   - Test específico falló - Municipio incorrecto")
        if not resultado2:
            print("   - Test de navegación falló")
        print("🔧 Se requiere revisión adicional del código")
    
    print("=" * 80)

if __name__ == "__main__":
    main()































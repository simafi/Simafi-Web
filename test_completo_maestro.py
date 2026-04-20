#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test completo del formulario maestro negocios con datos reales
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test(num, description, func):
    """Ejecutar un test y mostrar resultado"""
    print(f"\n{'='*70}")
    print(f"TEST {num}: {description}")
    print(f"{'='*70}")
    try:
        result = func()
        if result:
            print("✅ PASÓ")
        else:
            print("❌ FALLÓ")
        return result
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test1():
    """Test 1: Buscar identificación por DNI"""
    url = f"{BASE_URL}/tributario/buscar-identificacion-ajax/?identidad=0801199012345"
    print(f"URL: {url}")
    
    response = requests.get(url, timeout=5)
    print(f"Status: {response.status_code}")
    
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    # Verificar que encontró la identificación
    if data.get('encontrado') and data.get('identificacion'):
        nombres = data['identificacion'].get('nombres', '')
        apellidos = data['identificacion'].get('apellidos', '')
        print(f"✓ Nombres: {nombres}")
        print(f"✓ Apellidos: {apellidos}")
        return nombres == 'JUAN CARLOS' and apellidos == 'PEREZ LOPEZ'
    return False

def test2():
    """Test 2: Buscar identificación representante"""
    url = f"{BASE_URL}/tributario/buscar-identificacion-ajax/?identidad=0801198523456"
    print(f"URL: {url}")
    
    response = requests.get(url, timeout=5)
    print(f"Status: {response.status_code}")
    
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    if data.get('encontrado') and data.get('identificacion'):
        nombres = data['identificacion'].get('nombres', '')
        apellidos = data['identificacion'].get('apellidos', '')
        print(f"✓ Nombres: {nombres}")
        print(f"✓ Apellidos: {apellidos}")
        return nombres == 'MARIA ELENA' and apellidos == 'GARCIA MARTINEZ'
    return False

def test3():
    """Test 3: Buscar negocio existente"""
    url = f"{BASE_URL}/tributario/buscar-negocio-ajax/?empresa=0801&rtm=001&expe=00001"
    print(f"URL: {url}")
    
    response = requests.get(url, timeout=5)
    print(f"Status: {response.status_code}")
    
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    if not data.get('error'):
        print(f"✓ Negocio: {data.get('nombrenego', 'N/A')}")
        print(f"✓ Comerciante: {data.get('comerciante', 'N/A')}")
        return True
    return False

def test4():
    """Test 4: Cargar formulario maestro negocios"""
    url = f"{BASE_URL}/tributario/maestro-negocios/"
    print(f"URL: {url}")
    
    response = requests.get(url, timeout=5)
    print(f"Status: {response.status_code}")
    
    # Verificar que contiene el JavaScript correcto
    html = response.text
    
    # Verificar URLs correctas en el JavaScript
    checks = [
        ('/tributario/buscar-identificacion-ajax/', 'URL de búsqueda DNI'),
        ('/tributario/buscar-negocio-ajax/', 'URL de búsqueda negocio'),
        ('/tributario/maestro-negocios/', 'URL de guardado'),
        ('id_comerciante', 'Campo comerciante'),
        ('id_identidad', 'Campo DNI')
    ]
    
    for check, desc in checks:
        if check in html:
            print(f"✓ {desc}: Presente")
        else:
            print(f"✗ {desc}: FALTA")
            return False
    
    return True

# Ejecutar tests
print("EJECUTANDO TESTS COMPLETOS DEL FORMULARIO MAESTRO NEGOCIOS")
print("="*70)

results = []
results.append(test(1, "Buscar identificación por DNI", test1))
results.append(test(2, "Buscar identificación representante", test2))
results.append(test(3, "Buscar negocio existente", test3))
results.append(test(4, "Verificar template HTML/JavaScript", test4))

# Resumen
print(f"\n{'='*70}")
print("RESUMEN DE TESTS")
print(f"{'='*70}")
total = len(results)
pasados = sum(results)
fallados = total - pasados

print(f"Total: {total}")
print(f"✅ Pasados: {pasados}")
print(f"❌ Fallados: {fallados}")

if fallados == 0:
    print("\n🎉 TODOS LOS TESTS PASARON - EL FORMULARIO ESTÁ FUNCIONAL")
    print("\nINSTRUCCIONES PARA EL USUARIO:")
    print("1. Abrir navegador en modo incógnito: Ctrl + Shift + N")
    print("2. Ir a: http://localhost:8080/tributario/maestro-negocios/")
    print("3. Probar con DNI: 0801199012345")
    print("4. Al perder foco del campo DNI, debe llenar: JUAN CARLOS PEREZ LOPEZ")
    print("5. El campo 'Comerciante' debe ser editable manualmente")
else:
    print(f"\n⚠️  HAY {fallados} TEST(S) FALLANDO - REVISAR ARRIBA")



























































#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test completo del formulario maestro negocios
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_url(url, description):
    """Test una URL y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            # Intentar parsear como JSON
            try:
                data = response.json()
                print(f"Response JSON:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except:
                # Si no es JSON, mostrar primeros 500 caracteres
                print(f"Response (primeros 500 chars):")
                print(response.text[:500])
        else:
            print(f"ERROR: {response.text[:200]}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def test_post_url(url, data, description):
    """Test una URL POST y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"TEST POST: {description}")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print(f"{'='*60}")
    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        try:
            data = response.json()
            print(f"Response JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(f"Response (primeros 500 chars):")
            print(response.text[:500])
        
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

# TESTS
print("INICIANDO TESTS DEL FORMULARIO MAESTRO NEGOCIOS")
print("="*60)

# Test 1: Verificar que maestro-negocios carga
test_url(f"{BASE_URL}/tributario/maestro-negocios/", 
         "Cargar formulario maestro negocios")

# Test 2: Buscar identificación por DNI
test_url(f"{BASE_URL}/tributario/buscar-identificacion-ajax/?identidad=0801199012345", 
         "Buscar identificación por DNI (GET)")

# Test 3: Buscar negocio
test_url(f"{BASE_URL}/tributario/buscar-negocio-ajax/?empresa=0801&rtm=001&expe=00001", 
         "Buscar negocio existente")

# Test 4: Intentar guardar (simulado)
print("\n" + "="*60)
print("NOTA: Para test de guardado, necesitas datos reales del formulario")
print("="*60)

# Resumen
print("\n" + "="*60)
print("TESTS COMPLETADOS")
print("="*60)
print("\nSi algún test falló, revisa los detalles arriba.")
print("\nPróximos pasos:")
print("1. Si buscar-identificacion-ajax falla, revisar la vista")
print("2. Si buscar-negocio-ajax falla, revisar la vista")
print("3. Si maestro-negocios carga bien, revisar el JavaScript del template")



























































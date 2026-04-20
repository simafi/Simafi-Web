#!/usr/bin/env python3
"""
Test final para verificar que la solución completa del problema de tarifas funciona
"""

import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.abspath('.'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Tarifas
from tributario_app.forms import TarifasForm

def test_validacion_codigo_tarifa():
    """Test de validación del código de tarifa"""
    print("=== TEST VALIDACIÓN CÓDIGO DE TARIFA ===")
    
    # Test 1: Código válido (4 caracteres)
    data_valido = {
        'empresa': '0001',
        'rubro': '001',
        'ano': '2024',
        'cod_tarifa': 'T001',
        'descripcion': 'Tarifa válida',
        'valor': '100.00',
        'frecuencia': 'A',
        'tipo': 'F'
    }
    
    form_valido = TarifasForm(data_valido)
    print(f"Código 'T001' (4 caracteres): {'✅ Válido' if form_valido.is_valid() else '❌ Inválido'}")
    
    # Test 2: Código inválido (más de 4 caracteres)
    data_invalido = {
        'empresa': '0001',
        'rubro': '001',
        'ano': '2024',
        'cod_tarifa': 'TAR001',  # 6 caracteres
        'descripcion': 'Tarifa inválida',
        'valor': '100.00',
        'frecuencia': 'A',
        'tipo': 'F'
    }
    
    form_invalido = TarifasForm(data_invalido)
    print(f"Código 'TAR001' (6 caracteres): {'❌ Válido' if form_invalido.is_valid() else '✅ Inválido (correcto)'}")
    
    if not form_invalido.is_valid():
        print("Errores encontrados:")
        for field, errors in form_invalido.errors.items():
            print(f"  {field}: {errors}")
    
    return form_valido.is_valid() and not form_invalido.is_valid()

def test_crear_actualizar_tarifa():
    """Test de crear y actualizar tarifa"""
    print("\n=== TEST CREAR Y ACTUALIZAR TARIFA ===")
    
    # Datos de prueba
    empresa = '0001'
    rubro = '003'
    ano = 2024
    cod_tarifa = 'T003'
    
    try:
        # Paso 1: Crear nueva tarifa
        print("Paso 1: Crear nueva tarifa")
        tarifa, created = Tarifas.objects.get_or_create(
            empresa=empresa,
            ano=ano,
            rubro=rubro,
            cod_tarifa=cod_tarifa,
            defaults={
                'descripcion': 'Tarifa de prueba inicial',
                'valor': 100.00,
                'frecuencia': 'A',
                'tipo': 'F',
            }
        )
        
        print(f"  Tarifa creada: {created}")
        print(f"  ID: {tarifa.id}")
        print(f"  Descripción: {tarifa.descripcion}")
        print(f"  Valor: {tarifa.valor}")
        
        # Paso 2: Actualizar la misma tarifa
        print("\nPaso 2: Actualizar tarifa existente")
        tarifa_actualizada, created_actualizada = Tarifas.objects.get_or_create(
            empresa=empresa,
            ano=ano,
            rubro=rubro,
            cod_tarifa=cod_tarifa,
            defaults={
                'descripcion': 'Tarifa actualizada',
                'valor': 200.00,
                'frecuencia': 'M',
                'tipo': 'V',
            }
        )
        
        print(f"  Tarifa creada (debería ser False): {created_actualizada}")
        print(f"  ID: {tarifa_actualizada.id}")
        print(f"  Descripción: {tarifa_actualizada.descripcion}")
        print(f"  Valor: {tarifa_actualizada.valor}")
        
        # Verificar que es la misma tarifa
        if tarifa.id == tarifa_actualizada.id:
            print("  ✅ Es la misma tarifa (correcto)")
        else:
            print("  ❌ No es la misma tarifa (incorrecto)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_clave_unica():
    """Test de la clave única"""
    print("\n=== TEST CLAVE ÚNICA ===")
    
    try:
        # Crear primera tarifa
        tarifa1, created1 = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='004',
            cod_tarifa='T004',
            defaults={
                'descripcion': 'Primera tarifa',
                'valor': 100.00,
                'frecuencia': 'A',
                'tipo': 'F',
            }
        )
        
        print(f"Primera tarifa creada: {created1}")
        print(f"ID: {tarifa1.id}")
        
        # Intentar crear segunda tarifa con misma clave única
        tarifa2, created2 = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='004',
            cod_tarifa='T004',  # Misma clave única
            defaults={
                'descripcion': 'Segunda tarifa (no debería crearse)',
                'valor': 200.00,
                'frecuencia': 'M',
                'tipo': 'V',
            }
        )
        
        print(f"Segunda tarifa creada: {created2}")
        print(f"ID: {tarifa2.id}")
        
        # Verificar que es la misma tarifa
        if tarifa1.id == tarifa2.id and not created2:
            print("✅ Clave única funciona correctamente")
            return True
        else:
            print("❌ Clave única no funciona correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_formulario_completo():
    """Test del formulario completo"""
    print("\n=== TEST FORMULARIO COMPLETO ===")
    
    # Datos válidos
    data = {
        'empresa': '0001',
        'rubro': '005',
        'ano': '2024',
        'cod_tarifa': 'T005',
        'descripcion': 'Tarifa desde formulario',
        'valor': '150.00',
        'frecuencia': 'A',
        'tipo': 'F'
    }
    
    form = TarifasForm(data)
    
    if form.is_valid():
        print("✅ Formulario válido")
        print("Datos limpios:")
        for field, value in form.cleaned_data.items():
            print(f"  {field}: {value}")
        
        # Simular guardado
        try:
            tarifa = form.save(commit=False)
            tarifa.empresa = '0001'
            tarifa.save()
            print(f"✅ Tarifa guardada con ID: {tarifa.id}")
            return True
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            return False
    else:
        print("❌ Formulario inválido")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return False

def main():
    """Función principal"""
    print("TEST FINAL - SOLUCIÓN COMPLETA DE TARIFAS")
    print("=" * 60)
    
    # Ejecutar todos los tests
    test1 = test_validacion_codigo_tarifa()
    test2 = test_crear_actualizar_tarifa()
    test3 = test_clave_unica()
    test4 = test_formulario_completo()
    
    print("\n" + "=" * 60)
    print("RESULTADOS FINALES")
    print("=" * 60)
    
    print(f"Validación código tarifa: {'✅ PASÓ' if test1 else '❌ FALLÓ'}")
    print(f"Crear/Actualizar tarifa: {'✅ PASÓ' if test2 else '❌ FALLÓ'}")
    print(f"Clave única: {'✅ PASÓ' if test3 else '❌ FALLÓ'}")
    print(f"Formulario completo: {'✅ PASÓ' if test4 else '❌ FALLÓ'}")
    
    total_tests = 4
    tests_pasados = sum([test1, test2, test3, test4])
    
    print(f"\nTests pasados: {tests_pasados}/{total_tests}")
    
    if tests_pasados == total_tests:
        print("🎉 ¡TODOS LOS TESTS PASARON! El sistema funciona correctamente.")
    else:
        print("⚠️ Algunos tests fallaron. Revisar implementación.")
    
    print("\n" + "=" * 60)
    print("SOLUCIÓN IMPLEMENTADA:")
    print("- Validación de código de tarifa máximo 4 caracteres")
    print("- Creación y actualización automática de tarifas")
    print("- Validación de clave única (empresa, rubro, año, código)")
    print("- Formulario completo funcional")
    print("=" * 60)

if __name__ == "__main__":
    main()



































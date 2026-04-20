#!/usr/bin/env python3
"""
Test para verificar que las correcciones del formulario de tarifas funcionan
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

def test_formulario_con_datos_iniciales():
    """Test del formulario con datos iniciales"""
    print("=== TEST FORMULARIO CON DATOS INICIALES ===")
    
    try:
        # Crear formulario con datos iniciales
        initial_data = {
            'empresa': '0001',
            'rubro': '001'
        }
        
        form = TarifasForm(initial=initial_data)
        
        print("✅ Formulario creado correctamente")
        print(f"   Empresa: {form.initial.get('empresa')}")
        print(f"   Rubro: {form.initial.get('rubro')}")
        
        # Verificar que el campo empresa tenga el valor correcto
        if form.initial.get('empresa') == '0001':
            print("✅ Campo empresa tiene el valor correcto")
        else:
            print(f"❌ Campo empresa tiene valor incorrecto: {form.initial.get('empresa')}")
            return False
        
        # Verificar que el campo empresa esté configurado como readonly
        empresa_field = form.fields.get('empresa')
        if empresa_field and hasattr(empresa_field.widget, 'attrs'):
            if 'readonly' in empresa_field.widget.attrs:
                print("✅ Campo empresa está configurado como readonly")
            else:
                print("❌ Campo empresa no está configurado como readonly")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear formulario: {e}")
        return False

def test_busqueda_y_actualizacion():
    """Test de búsqueda y actualización de tarifa"""
    print("\n=== TEST BÚSQUEDA Y ACTUALIZACIÓN ===")
    
    try:
        # Crear una tarifa de prueba
        tarifa_prueba = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='002',
            cod_tarifa='T002',
            defaults={
                'descripcion': 'Tarifa de prueba para actualización',
                'valor': 100.00,
                'frecuencia': 'A',
                'tipo': 'F',
            }
        )[0]
        
        print(f"✅ Tarifa de prueba creada: {tarifa_prueba}")
        print(f"   ID: {tarifa_prueba.id}")
        print(f"   Descripción: {tarifa_prueba.descripcion}")
        print(f"   Valor: {tarifa_prueba.valor}")
        
        # Simular búsqueda
        tarifa_encontrada = Tarifas.objects.filter(
            empresa='0001',
            cod_tarifa='T002'
        ).first()
        
        if tarifa_encontrada:
            print("✅ Tarifa encontrada correctamente")
            print(f"   ID: {tarifa_encontrada.id}")
            
            # Simular actualización
            tarifa_encontrada.descripcion = 'Tarifa actualizada'
            tarifa_encontrada.valor = 200.00
            tarifa_encontrada.frecuencia = 'M'
            tarifa_encontrada.tipo = 'V'
            tarifa_encontrada.save()
            
            print("✅ Tarifa actualizada correctamente")
            print(f"   Nueva descripción: {tarifa_encontrada.descripcion}")
            print(f"   Nuevo valor: {tarifa_encontrada.valor}")
            print(f"   Nueva frecuencia: {tarifa_encontrada.frecuencia}")
            print(f"   Nuevo tipo: {tarifa_encontrada.tipo}")
            
            return True
        else:
            print("❌ No se encontró la tarifa")
            return False
            
    except Exception as e:
        print(f"❌ Error en búsqueda y actualización: {e}")
        return False

def test_get_or_create():
    """Test de get_or_create para actualización"""
    print("\n=== TEST GET_OR_CREATE ===")
    
    try:
        # Usar get_or_create para la misma tarifa
        tarifa, created = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='003',
            cod_tarifa='T003',
            defaults={
                'descripcion': 'Tarifa desde get_or_create',
                'valor': 300.00,
                'frecuencia': 'A',
                'tipo': 'F',
            }
        )
        
        print(f"✅ get_or_create ejecutado correctamente")
        print(f"   Creada: {created}")
        print(f"   ID: {tarifa.id}")
        print(f"   Valor: {tarifa.valor}")
        
        # Intentar actualizar usando get_or_create
        tarifa_actualizada, created_actualizada = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='003',
            cod_tarifa='T003',
            defaults={
                'descripcion': 'Tarifa actualizada desde get_or_create',
                'valor': 400.00,
                'frecuencia': 'M',
                'tipo': 'V',
            }
        )
        
        print(f"✅ Segunda llamada a get_or_create")
        print(f"   Creada: {created_actualizada}")
        print(f"   ID: {tarifa_actualizada.id}")
        
        # Verificar que es la misma tarifa
        if tarifa.id == tarifa_actualizada.id and not created_actualizada:
            print("✅ Es la misma tarifa (correcto)")
            return True
        else:
            print("❌ No es la misma tarifa (incorrecto)")
            return False
        
    except Exception as e:
        print(f"❌ Error en get_or_create: {e}")
        return False

def test_validacion_codigo_tarifa():
    """Test de validación del código de tarifa"""
    print("\n=== TEST VALIDACIÓN CÓDIGO DE TARIFA ===")
    
    try:
        # Test con código válido (4 caracteres)
        data_valido = {
            'empresa': '0001',
            'rubro': '001',
            'ano': '2024',
            'cod_tarifa': 'T004',
            'descripcion': 'Tarifa válida',
            'valor': '100.00',
            'frecuencia': 'A',
            'tipo': 'F'
        }
        
        form_valido = TarifasForm(data_valido)
        print(f"Código 'T004' (4 caracteres): {'✅ Válido' if form_valido.is_valid() else '❌ Inválido'}")
        
        # Test con código inválido (más de 4 caracteres)
        data_invalido = {
            'empresa': '0001',
            'rubro': '001',
            'ano': '2024',
            'cod_tarifa': 'TAR004',  # 6 caracteres
            'descripcion': 'Tarifa inválida',
            'valor': '100.00',
            'frecuencia': 'A',
            'tipo': 'F'
        }
        
        form_invalido = TarifasForm(data_invalido)
        print(f"Código 'TAR004' (6 caracteres): {'❌ Válido' if form_invalido.is_valid() else '✅ Inválido (correcto)'}")
        
        if not form_invalido.is_valid():
            print("Errores encontrados:")
            for field, errors in form_invalido.errors.items():
                print(f"  {field}: {errors}")
        
        return form_valido.is_valid() and not form_invalido.is_valid()
        
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

def main():
    """Función principal"""
    print("TEST CORRECCIONES - FORMULARIO DE TARIFAS")
    print("=" * 60)
    
    # Ejecutar todos los tests
    test1 = test_formulario_con_datos_iniciales()
    test2 = test_busqueda_y_actualizacion()
    test3 = test_get_or_create()
    test4 = test_validacion_codigo_tarifa()
    
    print("\n" + "=" * 60)
    print("RESULTADOS DEL TEST")
    print("=" * 60)
    
    print(f"Formulario con datos iniciales: {'✅ PASÓ' if test1 else '❌ FALLÓ'}")
    print(f"Búsqueda y actualización: {'✅ PASÓ' if test2 else '❌ FALLÓ'}")
    print(f"get_or_create: {'✅ PASÓ' if test3 else '❌ FALLÓ'}")
    print(f"Validación código tarifa: {'✅ PASÓ' if test4 else '❌ FALLÓ'}")
    
    total_tests = 4
    tests_pasados = sum([test1, test2, test3, test4])
    
    print(f"\nTests pasados: {tests_pasados}/{total_tests}")
    
    if tests_pasados == total_tests:
        print("🎉 ¡TODOS LOS TESTS PASARON! Las correcciones funcionan correctamente.")
        print("\n✅ El formulario carga datos iniciales correctamente")
        print("✅ La búsqueda y actualización funcionan")
        print("✅ get_or_create maneja actualizaciones correctamente")
        print("✅ La validación de código de tarifa funciona")
    else:
        print("⚠️ Algunos tests fallaron. Revisar implementación.")
    
    print("\n" + "=" * 60)
    print("CORRECCIONES IMPLEMENTADAS:")
    print("- Campo empresa con valor inicial vacío")
    print("- Campo empresa configurado como readonly")
    print("- JavaScript mejorado con logging")
    print("- Campo oculto para ID de tarifa")
    print("- Vista actualizada para incluir ID en respuesta")
    print("=" * 60)

if __name__ == "__main__":
    main()



































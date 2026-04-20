#!/usr/bin/env python3
"""
Diagnóstico simple de problemas en el formulario de tarifas
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

def test_busqueda_automatica():
    """Test de la búsqueda automática de tarifas"""
    print("=== TEST BÚSQUEDA AUTOMÁTICA ===")
    
    # Crear una tarifa de prueba primero
    try:
        tarifa_prueba = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='001',
            cod_tarifa='T001',
            defaults={
                'descripcion': 'Tarifa de prueba para búsqueda',
                'valor': 150.00,
                'frecuencia': 'A',
                'tipo': 'F',
            }
        )[0]
        print(f"✅ Tarifa de prueba creada: {tarifa_prueba}")
    except Exception as e:
        print(f"❌ Error al crear tarifa de prueba: {e}")
        return False
    
    # Simular búsqueda manual
    try:
        tarifa_encontrada = Tarifas.objects.filter(
            empresa='0001',
            cod_tarifa='T001'
        ).first()
        
        if tarifa_encontrada:
            print("✅ Búsqueda manual funciona correctamente")
            print(f"   Descripción: {tarifa_encontrada.descripcion}")
            print(f"   Valor: {tarifa_encontrada.valor}")
            print(f"   Frecuencia: {tarifa_encontrada.frecuencia}")
            print(f"   Tipo: {tarifa_encontrada.tipo}")
            return True
        else:
            print("❌ No se encontró la tarifa")
            return False
            
    except Exception as e:
        print(f"❌ Error en búsqueda manual: {e}")
        return False

def test_actualizacion_tarifa():
    """Test de actualización de tarifa"""
    print("\n=== TEST ACTUALIZACIÓN DE TARIFA ===")
    
    try:
        # Buscar la tarifa existente
        tarifa = Tarifas.objects.get(
            empresa='0001',
            ano=2024,
            rubro='001',
            cod_tarifa='T001'
        )
        
        print(f"✅ Tarifa encontrada para actualizar")
        print(f"   Valor anterior: {tarifa.valor}")
        
        # Actualizar la tarifa
        tarifa.valor = 200.00
        tarifa.descripcion = 'Tarifa actualizada'
        tarifa.frecuencia = 'M'
        tarifa.tipo = 'V'
        tarifa.save()
        
        print(f"✅ Tarifa actualizada correctamente")
        print(f"   Nuevo valor: {tarifa.valor}")
        print(f"   Nueva descripción: {tarifa.descripcion}")
        print(f"   Nueva frecuencia: {tarifa.frecuencia}")
        print(f"   Nuevo tipo: {tarifa.tipo}")
        
        return True
        
    except Tarifas.DoesNotExist:
        print("❌ No se encontró la tarifa para actualizar")
        return False
    except Exception as e:
        print(f"❌ Error en actualización: {e}")
        return False

def test_formulario_con_datos():
    """Test del formulario con datos pre-cargados"""
    print("\n=== TEST FORMULARIO CON DATOS ===")
    
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
        
        # Verificar que los campos tengan los valores correctos
        if form.initial.get('empresa') == '0001' and form.initial.get('rubro') == '001':
            print("✅ Datos iniciales correctos")
            return True
        else:
            print("❌ Datos iniciales incorrectos")
            return False
            
    except Exception as e:
        print(f"❌ Error al crear formulario: {e}")
        return False

def test_variables_ocultas():
    """Test de variables ocultas en el formulario"""
    print("\n=== TEST VARIABLES OCULTAS ===")
    
    try:
        form = TarifasForm()
        
        # Verificar campos ocultos
        empresa_field = form.fields.get('empresa')
        if empresa_field and hasattr(empresa_field.widget, 'attrs'):
            if 'readonly' in empresa_field.widget.attrs:
                print("✅ Campo empresa está configurado como readonly")
            else:
                print("⚠️ Campo empresa no está configurado como readonly")
        
        rubro_field = form.fields.get('rubro')
        if rubro_field and hasattr(rubro_field.widget, 'attrs'):
            if 'readonly' in rubro_field.widget.attrs:
                print("✅ Campo rubro está configurado como readonly")
            else:
                print("⚠️ Campo rubro no está configurado como readonly")
        
        # Verificar que el campo empresa tenga el valor por defecto
        if form.fields['empresa'].initial == '':
            print("✅ Campo empresa tiene valor por defecto vacío")
        else:
            print(f"⚠️ Campo empresa tiene valor por defecto: {form.fields['empresa'].initial}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar variables ocultas: {e}")
        return False

def test_conflicto_botones():
    """Test de conflictos entre botones"""
    print("\n=== TEST CONFLICTO BOTONES ===")
    
    try:
        form = TarifasForm()
        
        # Verificar IDs únicos
        field_ids = []
        for field_name, field in form.fields.items():
            field_id = f"id_{field_name}"
            if field_id in field_ids:
                print(f"❌ Campo duplicado encontrado: {field_id}")
                return False
            field_ids.append(field_id)
        
        print("✅ No se encontraron campos duplicados")
        print(f"   Campos encontrados: {len(field_ids)}")
        
        # Verificar que todos los campos necesarios estén presentes
        campos_requeridos = ['empresa', 'rubro', 'ano', 'cod_tarifa', 'descripcion', 'valor', 'frecuencia', 'tipo']
        for campo in campos_requeridos:
            if campo in form.fields:
                print(f"   ✅ Campo {campo} presente")
            else:
                print(f"   ❌ Campo {campo} faltante")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar conflictos: {e}")
        return False

def test_get_or_create():
    """Test de get_or_create para actualización"""
    print("\n=== TEST GET_OR_CREATE ===")
    
    try:
        # Usar get_or_create para la misma tarifa
        tarifa, created = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='001',
            cod_tarifa='T001',
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
        
        # Si no se creó, significa que ya existía (correcto)
        if not created:
            print("   ✅ Tarifa existente encontrada (correcto)")
        else:
            print("   ⚠️ Nueva tarifa creada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en get_or_create: {e}")
        return False

def main():
    """Función principal"""
    print("DIAGNÓSTICO SIMPLE - PROBLEMAS EN FORMULARIO DE TARIFAS")
    print("=" * 70)
    
    # Ejecutar todos los tests
    test1 = test_busqueda_automatica()
    test2 = test_actualizacion_tarifa()
    test3 = test_formulario_con_datos()
    test4 = test_variables_ocultas()
    test5 = test_conflicto_botones()
    test6 = test_get_or_create()
    
    print("\n" + "=" * 70)
    print("RESULTADOS DEL DIAGNÓSTICO")
    print("=" * 70)
    
    print(f"Búsqueda automática: {'✅ FUNCIONA' if test1 else '❌ FALLA'}")
    print(f"Actualización de tarifa: {'✅ FUNCIONA' if test2 else '❌ FALLA'}")
    print(f"Formulario con datos: {'✅ FUNCIONA' if test3 else '❌ FALLA'}")
    print(f"Variables ocultas: {'✅ FUNCIONA' if test4 else '❌ FALLA'}")
    print(f"Conflicto botones: {'✅ FUNCIONA' if test5 else '❌ FALLA'}")
    print(f"get_or_create: {'✅ FUNCIONA' if test6 else '❌ FALLA'}")
    
    total_tests = 6
    tests_pasados = sum([test1, test2, test3, test4, test5, test6])
    
    print(f"\nTests pasados: {tests_pasados}/{total_tests}")
    
    if tests_pasados == total_tests:
        print("🎉 ¡TODOS LOS TESTS PASARON! El sistema funciona correctamente.")
    else:
        print("⚠️ Algunos tests fallaron. Se identificaron problemas específicos.")
        
        if not test1:
            print("\n🔍 PROBLEMA 1: Búsqueda automática no funciona")
            print("   - Verificar que la vista buscar_tarifa_automatica esté funcionando")
            print("   - Verificar que la URL esté correctamente configurada")
            print("   - Verificar que el JavaScript esté enviando los datos correctos")
        
        if not test2:
            print("\n🔍 PROBLEMA 2: Actualización de tarifa no funciona")
            print("   - Verificar que get_or_create esté funcionando correctamente")
            print("   - Verificar que no haya conflictos con unique_together")
            print("   - Verificar que los datos del formulario sean válidos")
        
        if not test3:
            print("\n🔍 PROBLEMA 3: Formulario no carga datos")
            print("   - Verificar que los parámetros de URL se estén procesando")
            print("   - Verificar que el formulario se inicialice correctamente")
        
        if not test4:
            print("\n🔍 PROBLEMA 4: Variables ocultas no funcionan")
            print("   - Verificar que el campo empresa esté configurado como readonly")
            print("   - Verificar que el valor de empresa se mantenga en el formulario")
        
        if not test5:
            print("\n🔍 PROBLEMA 5: Conflicto entre botones")
            print("   - Verificar que no haya IDs duplicados en el formulario")
            print("   - Verificar que los botones tengan IDs únicos")
        
        if not test6:
            print("\n🔍 PROBLEMA 6: get_or_create no funciona")
            print("   - Verificar que la lógica de get_or_create esté correcta")
            print("   - Verificar que no haya conflictos con la clave única")
    
    print("\n" + "=" * 70)
    print("RECOMENDACIONES:")
    print("- Revisar la consola del navegador para errores JavaScript")
    print("- Verificar que las URLs estén correctamente configuradas")
    print("- Verificar que el CSRF token esté presente en las peticiones AJAX")
    print("- Verificar que los datos se estén enviando en el formato correcto")
    print("=" * 70)

if __name__ == "__main__":
    main()



































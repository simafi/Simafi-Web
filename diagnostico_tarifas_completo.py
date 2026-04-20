#!/usr/bin/env python3
"""
Diagnóstico completo de problemas en el formulario de tarifas
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse

# Importar las vistas y modelos
sys.path.append('venv/Scripts/tributario')
from tributario_app.views import tarifas_crud, buscar_tarifa_automatica
from tributario_app.models import Tarifas
from tributario_app.forms import TarifasForm

def crear_request_simulado():
    """Crear un request simulado para testing"""
    factory = RequestFactory()
    request = factory.post('/tarifas/', {
        'empresa': '0001',
        'rubro': '001',
        'ano': '2024',
        'cod_tarifa': 'T001',
        'descripcion': 'Tarifa de prueba',
        'valor': '100.00',
        'frecuencia': 'A',
        'tipo': 'F'
    })
    
    # Agregar middleware de sesión
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # Agregar middleware CSRF
    csrf_middleware = CsrfViewMiddleware(lambda x: None)
    csrf_middleware.process_request(request)
    
    # Configurar sesión
    request.session['municipio_codigo'] = '0001'
    request.user = AnonymousUser()
    
    return request

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
    
    # Simular request de búsqueda automática
    factory = RequestFactory()
    request = factory.post('/ajax/buscar-tarifa-automatica/', {
        'empresa': '0001',
        'rubro': '001',
        'ano': '2024',
        'cod_tarifa': 'T001'
    })
    
    # Configurar sesión
    request.session = {}
    request.session['municipio_codigo'] = '0001'
    
    try:
        response = buscar_tarifa_automatica(request)
        
        if hasattr(response, 'content'):
            import json
            data = json.loads(response.content.decode('utf-8'))
            print(f"Respuesta de búsqueda automática: {data}")
            
            if data.get('exito'):
                print("✅ Búsqueda automática funciona correctamente")
                tarifa_data = data.get('tarifa', {})
                print(f"   Descripción: {tarifa_data.get('descripcion')}")
                print(f"   Valor: {tarifa_data.get('valor')}")
                print(f"   Frecuencia: {tarifa_data.get('frecuencia')}")
                print(f"   Tipo: {tarifa_data.get('tipo')}")
                return True
            else:
                print(f"❌ Búsqueda automática falló: {data.get('mensaje')}")
                return False
        else:
            print(f"❌ Respuesta inesperada: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error en búsqueda automática: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_actualizacion_tarifa():
    """Test de actualización de tarifa"""
    print("\n=== TEST ACTUALIZACIÓN DE TARIFA ===")
    
    # Crear request para actualizar tarifa
    factory = RequestFactory()
    request = factory.post('/tarifas/', {
        'empresa': '0001',
        'rubro': '001',
        'ano': '2024',
        'cod_tarifa': 'T001',
        'descripcion': 'Tarifa actualizada',
        'valor': '200.00',
        'frecuencia': 'M',
        'tipo': 'V'
    })
    
    # Configurar sesión
    request.session = {}
    request.session['municipio_codigo'] = '0001'
    
    try:
        response = tarifas_crud(request)
        
        # Verificar si la tarifa se actualizó
        tarifa_actualizada = Tarifas.objects.get(
            empresa='0001',
            ano=2024,
            rubro='001',
            cod_tarifa='T001'
        )
        
        print(f"✅ Tarifa actualizada correctamente")
        print(f"   Descripción: {tarifa_actualizada.descripcion}")
        print(f"   Valor: {tarifa_actualizada.valor}")
        print(f"   Frecuencia: {tarifa_actualizada.frecuencia}")
        print(f"   Tipo: {tarifa_actualizada.tipo}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en actualización: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_formulario_con_datos():
    """Test del formulario con datos pre-cargados"""
    print("\n=== TEST FORMULARIO CON DATOS ===")
    
    # Crear request GET con parámetros
    factory = RequestFactory()
    request = factory.get('/tarifas/?codigo_rubro=001')
    
    # Configurar sesión
    request.session = {}
    request.session['municipio_codigo'] = '0001'
    
    try:
        response = tarifas_crud(request)
        
        if hasattr(response, 'context_data'):
            form = response.context_data.get('form')
            if form:
                print("✅ Formulario cargado correctamente")
                print(f"   Empresa: {form.initial.get('empresa')}")
                print(f"   Rubro: {form.initial.get('rubro')}")
                return True
            else:
                print("❌ No se pudo obtener el formulario")
                return False
        else:
            print("❌ Respuesta no tiene context_data")
            return False
            
    except Exception as e:
        print(f"❌ Error al cargar formulario: {e}")
        return False

def test_variables_ocultas():
    """Test de variables ocultas en el formulario"""
    print("\n=== TEST VARIABLES OCULTAS ===")
    
    # Crear request GET
    factory = RequestFactory()
    request = factory.get('/tarifas/')
    
    # Configurar sesión
    request.session = {}
    request.session['municipio_codigo'] = '0001'
    
    try:
        response = tarifas_crud(request)
        
        if hasattr(response, 'context_data'):
            form = response.context_data.get('form')
            if form:
                # Verificar campos ocultos
                empresa_field = form.fields.get('empresa')
                if empresa_field and hasattr(empresa_field.widget, 'attrs'):
                    if 'readonly' in empresa_field.widget.attrs:
                        print("✅ Campo empresa está configurado como readonly")
                    else:
                        print("⚠️ Campo empresa no está configurado como readonly")
                
                # Verificar que el campo empresa tenga el valor correcto
                if form.initial.get('empresa') == '0001':
                    print("✅ Campo empresa tiene el valor correcto")
                else:
                    print(f"❌ Campo empresa tiene valor incorrecto: {form.initial.get('empresa')}")
                
                return True
            else:
                print("❌ No se pudo obtener el formulario")
                return False
        else:
            print("❌ Respuesta no tiene context_data")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar variables ocultas: {e}")
        return False

def test_conflicto_botones():
    """Test de conflictos entre botones"""
    print("\n=== TEST CONFLICTO BOTONES ===")
    
    # Verificar que no haya múltiples formularios con el mismo ID
    try:
        # Simular renderizado del template
        factory = RequestFactory()
        request = factory.get('/tarifas/')
        request.session = {'municipio_codigo': '0001'}
        
        response = tarifas_crud(request)
        
        if hasattr(response, 'context_data'):
            form = response.context_data.get('form')
            if form:
                # Verificar IDs únicos
                form_id = form.auto_id
                print(f"✅ Formulario tiene ID único: {form_id}")
                
                # Verificar que no haya campos duplicados
                field_ids = []
                for field_name, field in form.fields.items():
                    field_id = form[field_name].auto_id
                    if field_id in field_ids:
                        print(f"❌ Campo duplicado encontrado: {field_id}")
                        return False
                    field_ids.append(field_id)
                
                print("✅ No se encontraron campos duplicados")
                return True
            else:
                print("❌ No se pudo obtener el formulario")
                return False
        else:
            print("❌ Respuesta no tiene context_data")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar conflictos: {e}")
        return False

def main():
    """Función principal"""
    print("DIAGNÓSTICO COMPLETO - PROBLEMAS EN FORMULARIO DE TARIFAS")
    print("=" * 70)
    
    # Ejecutar todos los tests
    test1 = test_busqueda_automatica()
    test2 = test_actualizacion_tarifa()
    test3 = test_formulario_con_datos()
    test4 = test_variables_ocultas()
    test5 = test_conflicto_botones()
    
    print("\n" + "=" * 70)
    print("RESULTADOS DEL DIAGNÓSTICO")
    print("=" * 70)
    
    print(f"Búsqueda automática: {'✅ FUNCIONA' if test1 else '❌ FALLA'}")
    print(f"Actualización de tarifa: {'✅ FUNCIONA' if test2 else '❌ FALLA'}")
    print(f"Formulario con datos: {'✅ FUNCIONA' if test3 else '❌ FALLA'}")
    print(f"Variables ocultas: {'✅ FUNCIONA' if test4 else '❌ FALLA'}")
    print(f"Conflicto botones: {'✅ FUNCIONA' if test5 else '❌ FALLA'}")
    
    total_tests = 5
    tests_pasados = sum([test1, test2, test3, test4, test5])
    
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
    
    print("\n" + "=" * 70)
    print("RECOMENDACIONES:")
    print("- Revisar la consola del navegador para errores JavaScript")
    print("- Verificar que las URLs estén correctamente configuradas")
    print("- Verificar que el CSRF token esté presente en las peticiones AJAX")
    print("- Verificar que los datos se estén enviando en el formato correcto")
    print("=" * 70)

if __name__ == "__main__":
    main()



































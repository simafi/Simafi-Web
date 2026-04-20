#!/usr/bin/env python3
"""
Diagnóstico del problema de guardado de tarifas
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

# Importar las vistas y modelos
sys.path.append('venv/Scripts/tributario')
from tributario_app.views import tarifas_crud
from tributario_app.models import Tarifas
from tributario_app.forms import TarifasForm

def crear_request_simulado():
    """Crear un request simulado para testing"""
    factory = RequestFactory()
    request = factory.post('/tarifas/', {
        'empresa': '0001',
        'rubro': '001',
        'ano': '2024',
        'cod_tarifa': 'TAR001',
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

def probar_formulario():
    """Probar el formulario directamente"""
    print("=== PRUEBA DEL FORMULARIO ===")
    
    # Datos de prueba
    data = {
        'empresa': '0001',
        'rubro': '001',
        'ano': '2024',
        'cod_tarifa': 'TAR001',
        'descripcion': 'Tarifa de prueba',
        'valor': '100.00',
        'frecuencia': 'A',
        'tipo': 'F'
    }
    
    form = TarifasForm(data)
    
    print(f"Formulario válido: {form.is_valid()}")
    if not form.is_valid():
        print("Errores del formulario:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    else:
        print("Datos limpios:")
        for field, value in form.cleaned_data.items():
            print(f"  {field}: {value}")

def probar_modelo():
    """Probar el modelo directamente"""
    print("\n=== PRUEBA DEL MODELO ===")
    
    # Verificar si existe una tarifa con los criterios
    try:
        tarifa_existente = Tarifas.objects.get(
            empresa='0001',
            rubro='001',
            ano=2024,
            cod_tarifa='TAR001'
        )
        print(f"Tarifa existente encontrada: {tarifa_existente}")
        return tarifa_existente
    except Tarifas.DoesNotExist:
        print("No existe tarifa con esos criterios")
        return None
    except Exception as e:
        print(f"Error al buscar tarifa: {e}")
        return None

def probar_get_or_create():
    """Probar get_or_create directamente"""
    print("\n=== PRUEBA GET_OR_CREATE ===")
    
    try:
        tarifa, created = Tarifas.objects.get_or_create(
            empresa='0001',
            ano=2024,
            rubro='001',
            cod_tarifa='TAR001',
            defaults={
                'descripcion': 'Tarifa de prueba actualizada',
                'valor': 150.00,
                'frecuencia': 'A',
                'tipo': 'F',
            }
        )
        
        print(f"Tarifa creada: {created}")
        print(f"Tarifa: {tarifa}")
        print(f"ID: {tarifa.id}")
        print(f"Descripción: {tarifa.descripcion}")
        print(f"Valor: {tarifa.valor}")
        
        return tarifa
    except Exception as e:
        print(f"Error en get_or_create: {e}")
        return None

def probar_vista():
    """Probar la vista directamente"""
    print("\n=== PRUEBA DE LA VISTA ===")
    
    try:
        request = crear_request_simulado()
        response = tarifas_crud(request)
        
        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.get('Content-Type', 'N/A')}")
        
        # Si es una respuesta de redirección
        if hasattr(response, 'url'):
            print(f"Redirect URL: {response.url}")
        
        return response
    except Exception as e:
        print(f"Error en la vista: {e}")
        import traceback
        traceback.print_exc()
        return None

def verificar_estructura_bd():
    """Verificar la estructura de la base de datos"""
    print("\n=== VERIFICACIÓN DE ESTRUCTURA BD ===")
    
    try:
        # Verificar que la tabla existe
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'tarifas'
                ORDER BY ORDINAL_POSITION
            """)
            
            columns = cursor.fetchall()
            print("Estructura de la tabla tarifas:")
            for column in columns:
                print(f"  {column[1]}: {column[2]} (NULL: {column[3]}, DEFAULT: {column[4]})")
        
        # Verificar índices únicos
        cursor.execute("""
            SELECT INDEX_NAME, COLUMN_NAME
            FROM INFORMATION_SCHEMA.STATISTICS 
            WHERE TABLE_NAME = 'tarifas' AND NON_UNIQUE = 0
        """)
        
        unique_indexes = cursor.fetchall()
        print("\nÍndices únicos:")
        for index in unique_indexes:
            print(f"  {index[0]}: {index[1]}")
            
    except Exception as e:
        print(f"Error al verificar estructura BD: {e}")

def main():
    """Función principal"""
    print("DIAGNÓSTICO DEL PROBLEMA DE GUARDADO DE TARIFAS")
    print("=" * 50)
    
    # Verificar estructura de BD
    verificar_estructura_bd()
    
    # Probar formulario
    probar_formulario()
    
    # Probar modelo
    tarifa_existente = probar_modelo()
    
    # Probar get_or_create
    tarifa = probar_get_or_create()
    
    # Probar vista
    response = probar_vista()
    
    print("\n" + "=" * 50)
    print("DIAGNÓSTICO COMPLETADO")
    
    if response and response.status_code == 200:
        print("✅ La vista funciona correctamente")
    else:
        print("❌ Hay un problema con la vista")
    
    if tarifa:
        print("✅ El modelo funciona correctamente")
    else:
        print("❌ Hay un problema con el modelo")

if __name__ == "__main__":
    main()



































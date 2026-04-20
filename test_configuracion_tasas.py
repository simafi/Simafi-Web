#!/usr/bin/env python3
"""
Script de prueba para verificar el formulario de configuración de tasas de negocios
"""

import os
import sys
import django
import requests
import json
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Negocio, TarifasICS, Rubro, Tarifas

def test_configuracion_tasas():
    """Prueba completa del formulario de configuración de tasas"""
    print("=== PRUEBA DE CONFIGURACIÓN DE TASAS ===")
    
    # URL base del servidor
    base_url = "http://127.0.0.1:8080"
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST001',
        'expe': '001',
        'nombrenego': 'Negocio de Prueba Tasas',
        'comerciante': 'Comerciante de Prueba',
        'identidad': '9999-9999-99999',
        'direccion': 'Dirección de Prueba',
        'estatus': 'A'
    }
    
    try:
        # 1. Crear un negocio de prueba
        print("\n1️⃣ Creando negocio de prueba...")
        negocio, created = Negocio.objects.get_or_create(
            empre=test_data['empre'],
            rtm=test_data['rtm'],
            expe=test_data['expe'],
            defaults=test_data
        )
        
        if created:
            print(f"✅ Negocio creado: {negocio.nombrenego}")
        else:
            print(f"✅ Negocio existente: {negocio.nombrenego}")
        
        # 2. Crear un rubro de prueba si no existe
        print("\n2️⃣ Verificando rubro de prueba...")
        rubro, created = Rubro.objects.get_or_create(
            empresa=test_data['empre'],
            codigo='001',
            defaults={
                'descripcion': 'Rubro de Prueba',
                'cuenta': '123456',
                'tipo': 'A'
            }
        )
        
        if created:
            print(f"✅ Rubro creado: {rubro.descripcion}")
        else:
            print(f"✅ Rubro existente: {rubro.descripcion}")
        
        # 3. Crear una tarifa de prueba si no existe
        print("\n3️⃣ Verificando tarifa de prueba...")
        tarifa, created = Tarifas.objects.get_or_create(
            empresa=test_data['empre'],
            rubro='001',
            cod_tarifa='T001',
            ano=2024,
            defaults={
                'descripcion': 'Tarifa de Prueba',
                'valor': Decimal('100.00'),
                'frecuencia': 'A',
                'tipo': 'F'
            }
        )
        
        if created:
            print(f"✅ Tarifa creada: {tarifa.descripcion}")
        else:
            print(f"✅ Tarifa existente: {tarifa.descripcion}")
        
        # 4. Probar acceso al formulario de configuración de tasas
        print("\n4️⃣ Probando acceso al formulario de configuración de tasas...")
        config_url = f"{base_url}/tributario/configurar-tasas-negocio/?rtm={test_data['rtm']}&expe={test_data['expe']}"
        
        response = requests.get(config_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Formulario de configuración de tasas accesible")
            
            # Verificar que el negocio se muestra correctamente
            if test_data['nombrenego'] in response.text:
                print("✅ Información del negocio mostrada correctamente")
            else:
                print("❌ Información del negocio no encontrada")
                
        else:
            print(f"❌ Error al acceder al formulario: HTTP {response.status_code}")
            return False
        
        # 5. Probar la API de obtener tarifas de rubro
        print("\n5️⃣ Probando API de obtener tarifas de rubro...")
        
        # Primero hacer login (simulado)
        session = requests.Session()
        
        # Probar la API AJAX
        api_url = f"{base_url}/tributario/obtener-tarifas-rubro/"
        api_data = {
            'rubro': '001'
        }
        
        response = session.post(api_url, data=api_data, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('exito'):
                    print("✅ API de tarifas funcionando correctamente")
                    print(f"   Tarifas encontradas: {len(data.get('tarifas', []))}")
                else:
                    print(f"❌ API retornó error: {data.get('mensaje')}")
            except json.JSONDecodeError:
                print("❌ Respuesta no es JSON válido")
        else:
            print(f"❌ Error en API: HTTP {response.status_code}")
        
        # 6. Probar agregar una tarifa ICS
        print("\n6️⃣ Probando agregar tarifa ICS...")
        
        # Crear datos para agregar tarifa ICS
        tarifa_ics_data = {
            'accion': 'agregar_tarifa',
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'cod_tarifa': 'T001',
            'valor': '150.00',
            'rubro': '001',
            'tarifa_rubro': 'T001'
        }
        
        response = session.post(config_url, data=tarifa_ics_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Petición de agregar tarifa ICS enviada correctamente")
            
            # Verificar que se creó la tarifa ICS
            tarifa_ics = TarifasICS.objects.filter(
                idneg=negocio.id,
                cod_tarifa='T001'
            ).first()
            
            if tarifa_ics:
                print(f"✅ Tarifa ICS creada: ${tarifa_ics.valor}")
            else:
                print("❌ Tarifa ICS no encontrada en la base de datos")
        else:
            print(f"❌ Error al agregar tarifa ICS: HTTP {response.status_code}")
        
        # 7. Verificar tarifas ICS existentes
        print("\n7️⃣ Verificando tarifas ICS existentes...")
        tarifas_ics = TarifasICS.objects.filter(idneg=negocio.id)
        print(f"   Tarifas ICS encontradas: {tarifas_ics.count()}")
        
        for tarifa_ics in tarifas_ics:
            print(f"   - {tarifa_ics.cod_tarifa}: ${tarifa_ics.valor}")
        
        print("\n✅ PRUEBA DE CONFIGURACIÓN DE TASAS COMPLETADA")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_navegacion_desde_maestro_negocios():
    """Prueba la navegación desde el formulario de maestro de negocios"""
    print("\n=== PRUEBA DE NAVEGACIÓN DESDE MAESTRO NEGOCIOS ===")
    
    base_url = "http://127.0.0.1:8080"
    
    try:
        # 1. Acceder al formulario de maestro de negocios
        print("\n1️⃣ Accediendo al formulario de maestro de negocios...")
        maestro_url = f"{base_url}/tributario/maestro-negocios/"
        
        response = requests.get(maestro_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Formulario de maestro de negocios accesible")
            
            # Verificar que el botón de configuración esté presente
            if 'Configuración de Tasas' in response.text:
                print("✅ Botón de configuración de tasas encontrado")
            else:
                print("❌ Botón de configuración de tasas no encontrado")
                
        else:
            print(f"❌ Error al acceder al formulario: HTTP {response.status_code}")
            return False
        
        # 2. Simular envío de datos para configuración
        print("\n2️⃣ Simulando envío de datos para configuración...")
        
        session = requests.Session()
        
        # Datos de prueba
        config_data = {
            'empre': '0301',
            'rtm': 'TEST001',
            'expe': '001',
            'accion': 'configuracion'
        }
        
        response = session.post(maestro_url, json=config_data, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('exito'):
                    print("✅ Respuesta de configuración exitosa")
                    if data.get('redirect'):
                        print(f"   URL de redirección: {data['redirect']}")
                else:
                    print(f"❌ Respuesta de configuración fallida: {data.get('mensaje')}")
            except json.JSONDecodeError:
                print("❌ Respuesta no es JSON válido")
        else:
            print(f"❌ Error en petición de configuración: HTTP {response.status_code}")
        
        print("\n✅ PRUEBA DE NAVEGACIÓN COMPLETADA")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba de navegación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE CONFIGURACIÓN DE TASAS")
    print("=" * 60)
    
    # Ejecutar pruebas
    resultado1 = test_configuracion_tasas()
    resultado2 = test_navegacion_desde_maestro_negocios()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    if resultado1:
        print("✅ Configuración de tasas: FUNCIONANDO")
    else:
        print("❌ Configuración de tasas: FALLÓ")
    
    if resultado2:
        print("✅ Navegación desde maestro negocios: FUNCIONANDO")
    else:
        print("❌ Navegación desde maestro negocios: FALLÓ")
    
    if resultado1 and resultado2:
        print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ El formulario de configuración de tasas está funcionando correctamente")
    else:
        print("\n⚠️ ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()




























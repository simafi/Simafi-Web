#!/usr/bin/env python
"""
Test para verificar la funcionalidad de búsqueda asíncrona de rubros
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_rubro_async_search():
    """Test de la funcionalidad de búsqueda asíncrona de rubros"""
    print("🔍 TEST DE BÚSQUEDA ASÍNCRONA DE RUBROS")
    print("=" * 50)
    
    try:
        from tributario_app.models import Rubro, Actividad
        
        # Crear datos de prueba
        empresa_test = "001"
        codigo_rubro = "R001"
        descripcion_rubro = "Impuesto Predial"
        
        print("   📋 Creando datos de prueba...")
        
        # Crear actividad de prueba
        actividad = Actividad.objects.create(
            empresa=empresa_test,
            codigo="A001",
            descripcion="Actividad de Prueba",
            estado="A"
        )
        
        # Crear rubro de prueba
        rubro = Rubro.objects.create(
            empresa=empresa_test,
            codigo=codigo_rubro,
            descripcion=descripcion_rubro,
            cuenta="A001",
            cuntarez="A001",
            tipo="I"
        )
        
        print(f"   ✅ Rubro creado: {rubro.codigo} - {rubro.descripcion}")
        
        # Test del endpoint AJAX
        print("\n   🌐 Probando endpoint AJAX...")
        
        client = Client()
        
        # Simular petición AJAX
        response = client.post('/tributario/buscar-rubro/', {
            'empresa': empresa_test,
            'codigo': codigo_rubro
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Respuesta AJAX exitosa: {response.status_code}")
            
            if data.get('exito'):
                print(f"   ✅ Rubro encontrado: {data['rubro']['descripcion']}")
                print(f"   📄 Datos del rubro:")
                for key, value in data['rubro'].items():
                    print(f"      {key}: {value}")
            else:
                print(f"   ❌ Error en búsqueda: {data.get('mensaje')}")
                return False
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            return False
        
        # Test de búsqueda con código inexistente
        print("\n   🔍 Probando búsqueda con código inexistente...")
        
        response = client.post('/tributario/buscar-rubro/', {
            'empresa': empresa_test,
            'codigo': 'R999'
        })
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('exito'):
                print(f"   ✅ Correctamente no encontrado: {data.get('mensaje')}")
            else:
                print(f"   ❌ Error: Debería no encontrar el rubro")
                return False
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            return False
        
        # Test del formulario principal
        print("\n   📝 Probando acceso al formulario de rubros...")
        
        response = client.get('/tributario/rubros-crud/')
        
        if response.status_code == 200:
            print("   ✅ Formulario de rubros accesible")
            
            # Verificar que el JavaScript esté presente
            content = response.content.decode('utf-8')
            if 'buscarRubroAsincrono' in content:
                print("   ✅ Función JavaScript de búsqueda asíncrona encontrada")
            else:
                print("   ❌ Función JavaScript de búsqueda asíncrona NO encontrada")
                return False
                
            if 'rubro-description' in content:
                print("   ✅ Elemento de descripción encontrado")
            else:
                print("   ❌ Elemento de descripción NO encontrado")
                return False
        else:
            print(f"   ❌ Error al acceder al formulario: {response.status_code}")
            return False
        
        print("\n   🧹 Limpiando datos de prueba...")
        rubro.delete()
        actividad.delete()
        
        print("\n✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_rubro_async_search()
    if success:
        print("\n🎉 La funcionalidad de búsqueda asíncrona de rubros está funcionando correctamente!")
    else:
        print("\n💥 Hay problemas con la funcionalidad de búsqueda asíncrona de rubros.")




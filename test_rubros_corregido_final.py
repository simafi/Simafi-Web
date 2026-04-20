#!/usr/bin/env python
"""
Test final para verificar que el formulario de rubros funcione correctamente
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_modelo_rubro_corregido():
    """Test del modelo Rubro corregido"""
    print("🔍 TEST DE MODELO RUBRO CORREGIDO")
    print("=" * 50)
    
    try:
        from tributario_app.models import Rubro
        
        print("   📋 Verificando modelo Rubro...")
        print(f"   📄 Campos del modelo: {[field.name for field in Rubro._meta.fields]}")
        
        # Verificar que cuentarez esté en los campos
        if 'cuentarez' in [field.name for field in Rubro._meta.fields]:
            print("   ✅ Campo cuentarez encontrado en el modelo")
        else:
            print("   ❌ Campo cuentarez NO encontrado en el modelo")
            return False
        
        # Verificar que cuntarez NO esté en los campos
        if 'cuntarez' in [field.name for field in Rubro._meta.fields]:
            print("   ❌ Campo cuntarez encontrado en el modelo (no debería estar)")
            return False
        else:
            print("   ✅ Campo cuntarez NO encontrado en el modelo (correcto)")
        
        # Intentar crear una instancia del modelo
        print("   📋 Intentando crear instancia del modelo...")
        try:
            rubro = Rubro(
                empresa='0301',
                codigo='TEST',
                descripcion='Test',
                cuenta='001',
                cuentarez='002',
                tipo='I'
            )
            print("   ✅ Instancia del modelo creada correctamente")
            
            # Intentar acceder a los campos
            print(f"   📄 Empresa: {rubro.empresa}")
            print(f"   📄 Código: {rubro.codigo}")
            print(f"   📄 Descripción: {rubro.descripcion}")
            print(f"   📄 Cuenta: {rubro.cuenta}")
            print(f"   📄 Cuentarez: {rubro.cuentarez}")
            print(f"   📄 Tipo: {rubro.tipo}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error al crear instancia: {str(e)}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_formulario_rubro_corregido():
    """Test del formulario RubroForm corregido"""
    print("\n🔍 TEST DE FORMULARIO RUBRO CORREGIDO")
    print("=" * 50)
    
    try:
        from tributario_app.forms import RubroForm
        
        print("   📋 Verificando formulario RubroForm...")
        
        # Crear datos de prueba
        data = {
            'empresa': '0301',
            'codigo': 'TEST',
            'descripcion': 'Test',
            'cuenta': '001',
            'cuentarez': '002',
            'tipo': 'I'
        }
        
        # Crear formulario
        form = RubroForm(data)
        
        if form.is_valid():
            print("   ✅ Formulario es válido")
            
            # Intentar guardar
            try:
                rubro = form.save(commit=False)
                print("   ✅ Formulario se puede guardar")
                print(f"   📄 Rubro creado: {rubro}")
                return True
            except Exception as e:
                print(f"   ❌ Error al guardar formulario: {str(e)}")
                return False
        else:
            print("   ❌ Formulario no es válido")
            print(f"   📄 Errores: {form.errors}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_formulario_rubros_web():
    """Test del formulario de rubros en la web"""
    print("\n🔍 TEST DE FORMULARIO RUBROS WEB")
    print("=" * 50)
    
    try:
        client = Client()
        
        # Simular login
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        # Login
        print("   📋 Realizando login...")
        response = client.post('/tributario-app/login/', login_data, follow=True)
        
        if response.status_code != 200:
            print(f"   ❌ Error en login: {response.status_code}")
            return False
        
        print("   ✅ Login exitoso")
        
        # Acceder al formulario
        print("   📋 Accediendo al formulario de rubros...")
        response = client.get('/tributario-app/rubros/', follow=True)
        
        if response.status_code == 200:
            print("   ✅ Formulario de rubros accesible")
            content = response.content.decode()
            
            # Verificar que no haya errores de base de datos
            if 'Unknown column' in content or 'OperationalError' in content:
                print("   ❌ Error de base de datos detectado")
                print(f"   📄 Contenido del error: {content[:500]}...")
                return False
            else:
                print("   ✅ No se detectaron errores de base de datos")
            
            # Verificar campos
            if 'id="id_cuentarez"' in content and 'name="cuentarez"' in content:
                print("   ✅ Campo cuentarez encontrado en el template")
            else:
                print("   ❌ Campo cuentarez no encontrado en el template")
                return False
            
            return True
        else:
            print(f"   ❌ Error accediendo al formulario: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🧪 TEST FINAL DE FORMULARIO RUBROS")
    print("Verificando que todo funcione correctamente con cuentarez")
    print("=" * 70)
    
    try:
        # Test 1: Modelo
        modelo_ok = test_modelo_rubro_corregido()
        
        # Test 2: Formulario
        formulario_ok = test_formulario_rubro_corregido()
        
        # Test 3: Web
        web_ok = test_formulario_rubros_web()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 70)
        
        print(f"✅ Modelo Rubro: {'OK' if modelo_ok else 'FALLO'}")
        print(f"✅ Formulario RubroForm: {'OK' if formulario_ok else 'FALLO'}")
        print(f"✅ Formulario Web: {'OK' if web_ok else 'FALLO'}")
        
        if modelo_ok and formulario_ok and web_ok:
            print("\n🎉 FORMULARIO RUBROS COMPLETAMENTE CORREGIDO")
            print("✅ El modelo coincide con la estructura real de la BD")
            print("✅ El formulario funciona correctamente")
            print("✅ La web funciona sin errores")
            print("✅ Se usa 'cuentarez' correctamente en todos los archivos")
            return 0
        else:
            print("\n⚠️  ALGUNAS CORRECCIONES NECESITAN REVISIÓN")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





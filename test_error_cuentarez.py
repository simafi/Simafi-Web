#!/usr/bin/env python
"""
Test para verificar el error específico de cuentarez
"""

import os
import sys
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def test_error_cuentarez():
    """Test para verificar el error específico de cuentarez"""
    print("🔍 TEST DE ERROR CUENTAREZ")
    print("=" * 50)
    
    try:
        # Verificar el modelo directamente
        from tributario_app.models import Rubro
        
        print("   📋 Verificando modelo Rubro...")
        print(f"   📄 Campos del modelo: {[field.name for field in Rubro._meta.fields]}")
        
        # Verificar si cuntarez está en los campos
        if 'cuntarez' in [field.name for field in Rubro._meta.fields]:
            print("   ✅ Campo cuntarez encontrado en el modelo")
        else:
            print("   ❌ Campo cuntarez NO encontrado en el modelo")
            return False
        
        # Verificar si cuentarez está en los campos (no debería estar)
        if 'cuentarez' in [field.name for field in Rubro._meta.fields]:
            print("   ❌ Campo cuentarez encontrado en el modelo (no debería estar)")
            return False
        else:
            print("   ✅ Campo cuentarez NO encontrado en el modelo (correcto)")
        
        # Intentar crear una instancia del modelo
        print("   📋 Intentando crear instancia del modelo...")
        try:
            rubro = Rubro(
                empresa='0301',
                codigo='TEST',
                descripcion='Test',
                cuenta='001',
                cuntarez='002',
                tipo='I'
            )
            print("   ✅ Instancia del modelo creada correctamente")
            
            # Intentar acceder a los campos
            print(f"   📄 Empresa: {rubro.empresa}")
            print(f"   📄 Código: {rubro.codigo}")
            print(f"   📄 Descripción: {rubro.descripcion}")
            print(f"   📄 Cuenta: {rubro.cuenta}")
            print(f"   📄 Cuntarez: {rubro.cuntarez}")
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

def test_formulario_rubro():
    """Test del formulario RubroForm"""
    print("\n🔍 TEST DE FORMULARIO RUBRO")
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
            'cuntarez': '002',
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

def main():
    """Función principal"""
    print("🧪 TEST DE ERROR CUENTAREZ")
    print("Verificando el error específico de la columna")
    print("=" * 60)
    
    try:
        # Test 1: Modelo
        modelo_ok = test_error_cuentarez()
        
        # Test 2: Formulario
        formulario_ok = test_formulario_rubro()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        print(f"✅ Modelo Rubro: {'OK' if modelo_ok else 'FALLO'}")
        print(f"✅ Formulario RubroForm: {'OK' if formulario_ok else 'FALLO'}")
        
        if modelo_ok and formulario_ok:
            print("\n🎉 MODELO Y FORMULARIO FUNCIONAN CORRECTAMENTE")
            print("✅ El error debe estar en otra parte")
            return 0
        else:
            print("\n⚠️  HAY PROBLEMAS EN EL MODELO O FORMULARIO")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





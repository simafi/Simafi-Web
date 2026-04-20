#!/usr/bin/env python3
"""
Script de prueba para verificar que la corrección del error EMPTY_VALUES funciona correctamente
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Negocio, TarifasICS, Rubro, Tarifas
from tributario_app.forms import TarifasICSForm, DynamicChoiceField

def test_correccion_empty_values():
    """Prueba que la corrección del error EMPTY_VALUES funciona correctamente"""
    print("=== PRUEBA DE CORRECCIÓN DEL ERROR EMPTY_VALUES ===")
    
    try:
        # 1. Verificar que el campo DynamicChoiceField se puede crear sin errores
        print("\n1️⃣ Verificando que DynamicChoiceField se puede crear...")
        
        campo = DynamicChoiceField(
            label="Test Field",
            required=True,
            choices=[('', 'Seleccione')]
        )
        print("✅ DynamicChoiceField creado exitosamente")
        
        # 2. Verificar que la validación funciona correctamente
        print("\n2️⃣ Verificando validación del campo...")
        
        # Probar con valor válido
        try:
            campo.clean('test_value')
            print("✅ Validación con valor válido: OK")
        except Exception as e:
            print(f"❌ Error en validación con valor válido: {e}")
            return False
        
        # Probar con valor vacío (debería fallar si es requerido)
        try:
            campo.clean('')
            print("❌ Validación con valor vacío debería haber fallado")
            return False
        except forms.ValidationError:
            print("✅ Validación con valor vacío: Correctamente rechazado")
        except Exception as e:
            print(f"❌ Error inesperado en validación con valor vacío: {e}")
            return False
        
        # 3. Verificar que el formulario TarifasICSForm funciona
        print("\n3️⃣ Verificando que TarifasICSForm funciona...")
        
        # Crear datos de prueba mínimos
        form_data = {
            'idneg': 1,
            'rtm': 'TEST',
            'expe': '001',
            'rubro': '001',
            'tarifa_rubro': '01',
            'valor_personalizado': '100.00'
        }
        
        form = TarifasICSForm(data=form_data)
        
        # Solo verificar que no hay errores de importación o creación
        print("✅ TarifasICSForm creado exitosamente")
        
        # 4. Verificar que el campo tarifa_rubro es del tipo correcto
        print("\n4️⃣ Verificando tipo del campo tarifa_rubro...")
        
        campo_tarifa = form.fields['tarifa_rubro']
        if isinstance(campo_tarifa, DynamicChoiceField):
            print("✅ Campo tarifa_rubro es DynamicChoiceField")
        else:
            print(f"❌ Campo tarifa_rubro no es DynamicChoiceField, es: {type(campo_tarifa)}")
            return False
        
        # 5. Probar validación del formulario completo
        print("\n5️⃣ Probando validación del formulario completo...")
        
        # Crear negocio de prueba para datos reales
        negocio, created = Negocio.objects.get_or_create(
            empre='0301',
            rtm='TEST008',
            expe='008',
            defaults={
                'nombrenego': 'Negocio de Prueba Empty Values',
                'comerciante': 'Comerciante de Prueba',
                'identidad': '6666-6666-66666',
                'direccion': 'Dirección de Prueba',
                'estatus': 'A'
            }
        )
        
        # Crear rubro de prueba
        rubro, created = Rubro.objects.get_or_create(
            empresa='0301',
            codigo='008',
            defaults={
                'descripcion': 'Rubro de Prueba Empty Values',
                'cuenta': '555555',
                'tipo': 'A'
            }
        )
        
        # Datos de formulario válidos
        form_data_valido = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '008',
            'tarifa_rubro': '02',  # Este valor debería ser aceptado
            'valor_personalizado': '200.00'
        }
        
        form_valido = TarifasICSForm(data=form_data_valido)
        
        if form_valido.is_valid():
            print("✅ Formulario válido con tarifa_rubro '02'")
            print(f"   Rubro: {form_valido.cleaned_data.get('rubro')}")
            print(f"   Tarifa: {form_valido.cleaned_data.get('tarifa_rubro')}")
        else:
            print("❌ Formulario inválido con tarifa_rubro '02'")
            print("   Errores:", form_valido.errors)
            return False
        
        # 6. Probar con diferentes valores de tarifa_rubro
        print("\n6️⃣ Probando con diferentes valores de tarifa_rubro...")
        
        valores_tarifa = ['01', '02', '03', 'ABC', 'XYZ123']
        
        for valor in valores_tarifa:
            form_data_test = {
                'idneg': negocio.id,
                'rtm': negocio.rtm,
                'expe': negocio.expe,
                'rubro': '008',
                'tarifa_rubro': valor,
                'valor_personalizado': '300.00'
            }
            
            form_test = TarifasICSForm(data=form_data_test)
            
            if form_test.is_valid():
                print(f"✅ Formulario válido con tarifa_rubro '{valor}'")
            else:
                print(f"❌ Formulario inválido con tarifa_rubro '{valor}'")
                print(f"   Errores: {form_test.errors}")
                return False
        
        # 7. Probar con tarifa_rubro vacío (debería fallar)
        print("\n7️⃣ Probando con tarifa_rubro vacío (debería fallar)...")
        
        form_data_vacio = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '008',
            'tarifa_rubro': '',  # Vacío
            'valor_personalizado': '400.00'
        }
        
        form_vacio = TarifasICSForm(data=form_data_vacio)
        
        if not form_vacio.is_valid():
            print("✅ Formulario correctamente inválido con tarifa_rubro vacío")
            print("   Errores esperados:", form_vacio.errors)
        else:
            print("❌ Formulario debería ser inválido con tarifa_rubro vacío")
            return False
        
        print("\n✅ PRUEBA DE CORRECCIÓN DEL ERROR EMPTY_VALUES COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE CORRECCIÓN DEL ERROR EMPTY_VALUES")
    print("=" * 60)
    
    resultado = test_correccion_empty_values()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Corrección del error EMPTY_VALUES: FUNCIONANDO CORRECTAMENTE")
        print("✅ DynamicChoiceField se crea sin errores")
        print("✅ Validación funciona correctamente")
        print("✅ Campo tarifa_rubro acepta cualquier valor válido")
        print("✅ No valida contra opciones estáticas del formulario")
        print("✅ Solo valida que no esté vacío")
    else:
        print("❌ Corrección del error EMPTY_VALUES: FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()




























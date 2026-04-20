#!/usr/bin/env python3
"""
Script de prueba para verificar que la corrección del campo tarifa_rubro funciona correctamente
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
from tributario_app.forms import TarifasICSForm

def test_correccion_tarifa_rubro():
    """Prueba que la corrección del campo tarifa_rubro funciona correctamente"""
    print("=== PRUEBA DE CORRECCIÓN DEL CAMPO TARIFA_RUBRO ===")
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST007',
        'expe': '007',
        'nombrenego': 'Negocio de Prueba Tarifa Rubro',
        'comerciante': 'Comerciante de Prueba',
        'identidad': '5555-5555-55555',
        'direccion': 'Dirección de Prueba',
        'estatus': 'A'
    }
    
    try:
        # 1. Crear negocio de prueba
        print("\n1️⃣ Creando negocio de prueba...")
        negocio, created = Negocio.objects.get_or_create(
            empre=test_data['empre'],
            rtm=test_data['rtm'],
            expe=test_data['expe'],
            defaults=test_data
        )
        
        if created:
            print(f"✅ Negocio creado: {negocio.nombrenego} (ID: {negocio.id})")
        else:
            print(f"✅ Negocio existente: {negocio.nombrenego} (ID: {negocio.id})")
        
        # 2. Crear rubro de prueba
        print("\n2️⃣ Creando rubro de prueba...")
        rubro, created = Rubro.objects.get_or_create(
            empresa=test_data['empre'],
            codigo='007',
            defaults={
                'descripcion': 'Rubro de Prueba Tarifa Rubro',
                'cuenta': '444444',
                'tipo': 'A'
            }
        )
        
        if created:
            print(f"✅ Rubro creado: {rubro.descripcion}")
        else:
            print(f"✅ Rubro existente: {rubro.descripcion}")
        
        # 3. Crear tarifa de prueba
        print("\n3️⃣ Creando tarifa de prueba...")
        ano_vigente = datetime.now().year
        
        tarifa, created = Tarifas.objects.get_or_create(
            empresa=test_data['empre'],
            rubro='007',
            cod_tarifa='TR001',
            ano=ano_vigente,
            defaults={
                'descripcion': 'Tarifa de Prueba Tarifa Rubro',
                'valor': Decimal('400.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            }
        )
        
        if created:
            print(f"✅ Tarifa creada: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        else:
            print(f"✅ Tarifa existente: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 4. Probar formulario con tarifa_rubro válido
        print("\n4️⃣ Probando formulario con tarifa_rubro válido...")
        
        form_data = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '007',
            'tarifa_rubro': 'TR001',  # Este valor debería ser aceptado
            'valor_personalizado': '450.00'
        }
        
        form = TarifasICSForm(data=form_data)
        
        if form.is_valid():
            print("✅ Formulario válido con tarifa_rubro 'TR001'")
            print(f"   Rubro: {form.cleaned_data.get('rubro')}")
            print(f"   Tarifa: {form.cleaned_data.get('tarifa_rubro')}")
            print(f"   Valor personalizado: {form.cleaned_data.get('valor_personalizado')}")
        else:
            print("❌ Formulario inválido con tarifa_rubro 'TR001'")
            print("   Errores:", form.errors)
            return False
        
        # 5. Probar formulario con otro valor de tarifa_rubro
        print("\n5️⃣ Probando formulario con otro valor de tarifa_rubro...")
        
        form_data_2 = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '007',
            'tarifa_rubro': '02',  # Este valor también debería ser aceptado
            'valor_personalizado': '500.00'
        }
        
        form_2 = TarifasICSForm(data=form_data_2)
        
        if form_2.is_valid():
            print("✅ Formulario válido con tarifa_rubro '02'")
            print(f"   Rubro: {form_2.cleaned_data.get('rubro')}")
            print(f"   Tarifa: {form_2.cleaned_data.get('tarifa_rubro')}")
            print(f"   Valor personalizado: {form_2.cleaned_data.get('valor_personalizado')}")
        else:
            print("❌ Formulario inválido con tarifa_rubro '02'")
            print("   Errores:", form_2.errors)
            return False
        
        # 6. Probar formulario sin tarifa_rubro (debería fallar)
        print("\n6️⃣ Probando formulario sin tarifa_rubro (debería fallar)...")
        
        form_data_sin_tarifa = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '007',
            # Sin tarifa_rubro
            'valor_personalizado': '600.00'
        }
        
        form_sin_tarifa = TarifasICSForm(data=form_data_sin_tarifa)
        
        if not form_sin_tarifa.is_valid():
            print("✅ Formulario correctamente inválido sin tarifa_rubro")
            print("   Errores esperados:", form_sin_tarifa.errors)
        else:
            print("❌ Formulario debería ser inválido sin tarifa_rubro")
            return False
        
        # 7. Probar formulario con tarifa_rubro vacío (debería fallar)
        print("\n7️⃣ Probando formulario con tarifa_rubro vacío (debería fallar)...")
        
        form_data_tarifa_vacia = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '007',
            'tarifa_rubro': '',  # Vacío
            'valor_personalizado': '700.00'
        }
        
        form_tarifa_vacia = TarifasICSForm(data=form_data_tarifa_vacia)
        
        if not form_tarifa_vacia.is_valid():
            print("✅ Formulario correctamente inválido con tarifa_rubro vacío")
            print("   Errores esperados:", form_tarifa_vacia.errors)
        else:
            print("❌ Formulario debería ser inválido con tarifa_rubro vacío")
            return False
        
        # 8. Simular el proceso completo de creación de tarifa ICS
        print("\n8️⃣ Simulando creación completa de tarifa ICS...")
        
        # Usar el primer formulario válido
        rubro = form.cleaned_data.get('rubro')
        tarifa_rubro = form.cleaned_data.get('tarifa_rubro')
        valor_personalizado = form.cleaned_data.get('valor_personalizado')
        
        # Buscar la tarifa con año vigente
        tarifa_bd = Tarifas.objects.get(
            empresa=test_data['empre'],
            rubro=rubro,
            cod_tarifa=tarifa_rubro,
            ano=ano_vigente
        )
        
        # Usar valor personalizado si se proporciona, sino usar el valor de la tarifa
        valor_final = valor_personalizado if valor_personalizado else tarifa_bd.valor
        
        print(f"   Valor de tarifa en BD: {tarifa_bd.valor}")
        print(f"   Valor personalizado: {valor_personalizado}")
        print(f"   Valor final a usar: {valor_final}")
        
        # Crear la tarifa ICS
        tarifa_ics = TarifasICS(
            idneg=negocio.id,
            rtm=negocio.rtm,
            expe=negocio.expe,
            cod_tarifa=tarifa_rubro,
            valor=valor_final
        )
        tarifa_ics.save()
        
        print(f"✅ Tarifa ICS creada exitosamente")
        print(f"   ID: {tarifa_ics.id}")
        print(f"   ID Negocio: {tarifa_ics.idneg}")
        print(f"   RTM: '{tarifa_ics.rtm}'")
        print(f"   Expediente: '{tarifa_ics.expe}'")
        print(f"   Código Tarifa: '{tarifa_ics.cod_tarifa}'")
        print(f"   Valor: ${tarifa_ics.valor}")
        
        # 9. Verificar que se guardó correctamente en la base de datos
        print("\n9️⃣ Verificando que se guardó en la base de datos...")
        
        tarifa_ics_guardada = TarifasICS.objects.get(id=tarifa_ics.id)
        print(f"✅ Tarifa ICS recuperada de la base de datos")
        print(f"   Código Tarifa: '{tarifa_ics_guardada.cod_tarifa}'")
        print(f"   Valor: ${tarifa_ics_guardada.valor}")
        
        # 10. Probar con diferentes valores de tarifa_rubro
        print("\n🔟 Probando con diferentes valores de tarifa_rubro...")
        
        valores_tarifa = ['01', '02', '03', 'TR001', 'TR002', 'ABC123']
        
        for valor in valores_tarifa:
            form_data_test = {
                'idneg': negocio.id,
                'rtm': negocio.rtm,
                'expe': negocio.expe,
                'rubro': '007',
                'tarifa_rubro': valor,
                'valor_personalizado': '800.00'
            }
            
            form_test = TarifasICSForm(data=form_data_test)
            
            if form_test.is_valid():
                print(f"✅ Formulario válido con tarifa_rubro '{valor}'")
            else:
                print(f"❌ Formulario inválido con tarifa_rubro '{valor}'")
                print(f"   Errores: {form_test.errors}")
                return False
        
        print("\n✅ PRUEBA DE CORRECCIÓN DEL CAMPO TARIFA_RUBRO COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE CORRECCIÓN DEL CAMPO TARIFA_RUBRO")
    print("=" * 60)
    
    resultado = test_correccion_tarifa_rubro()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Corrección del campo tarifa_rubro: FUNCIONANDO CORRECTAMENTE")
        print("✅ Campo tarifa_rubro acepta cualquier valor válido")
        print("✅ No valida contra opciones estáticas del formulario")
        print("✅ Solo valida que no esté vacío")
        print("✅ Se puede grabar correctamente en la tabla tarifasics")
    else:
        print("❌ Corrección del campo tarifa_rubro: FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()




























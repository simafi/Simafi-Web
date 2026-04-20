#!/usr/bin/env python3
"""
Script de prueba específico para el formulario de configuración de tasas
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Negocio, TarifasICS, Rubro, Tarifas
from tributario_app.forms import TarifasICSForm

def test_formulario_tasas():
    """Prueba específica del formulario de tasas"""
    print("=== PRUEBA DEL FORMULARIO DE TASAS ===")
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST001',
        'expe': '001',
        'nombrenego': 'Negocio de Prueba Formulario',
        'comerciante': 'Comerciante de Prueba',
        'identidad': '9999-9999-99999',
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
            codigo='001',
            defaults={
                'descripcion': 'Rubro de Prueba Formulario',
                'cuenta': '123456',
                'tipo': 'A'
            }
        )
        
        if created:
            print(f"✅ Rubro creado: {rubro.descripcion}")
        else:
            print(f"✅ Rubro existente: {rubro.descripcion}")
        
        # 3. Crear tarifa de prueba
        print("\n3️⃣ Creando tarifa de prueba...")
        from datetime import datetime
        ano_vigente = datetime.now().year
        
        tarifa, created = Tarifas.objects.get_or_create(
            empresa=test_data['empre'],
            rubro='001',
            cod_tarifa='T001',
            ano=ano_vigente,
            defaults={
                'descripcion': 'Tarifa de Prueba Formulario',
                'valor': Decimal('100.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            }
        )
        
        if created:
            print(f"✅ Tarifa creada: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        else:
            print(f"✅ Tarifa existente: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 4. Probar formulario con datos válidos
        print("\n4️⃣ Probando formulario con datos válidos...")
        
        form_data = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '001',
            'tarifa_rubro': 'T001',
            'valor_personalizado': '150.00'
        }
        
        form = TarifasICSForm(data=form_data)
        
        if form.is_valid():
            print("✅ Formulario válido")
            print(f"   Rubro: {form.cleaned_data.get('rubro')}")
            print(f"   Tarifa: {form.cleaned_data.get('tarifa_rubro')}")
            print(f"   Valor personalizado: {form.cleaned_data.get('valor_personalizado')}")
        else:
            print("❌ Formulario inválido")
            print("   Errores:", form.errors)
            return False
        
        # 5. Probar formulario sin valor personalizado
        print("\n5️⃣ Probando formulario sin valor personalizado...")
        
        form_data_sin_valor = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '001',
            'tarifa_rubro': 'T001'
        }
        
        form_sin_valor = TarifasICSForm(data=form_data_sin_valor)
        
        if form_sin_valor.is_valid():
            print("✅ Formulario sin valor personalizado válido")
        else:
            print("❌ Formulario sin valor personalizado inválido")
            print("   Errores:", form_sin_valor.errors)
            return False
        
        # 6. Probar formulario con datos faltantes
        print("\n6️⃣ Probando formulario con datos faltantes...")
        
        form_data_incompleto = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '',  # Rubro faltante
            'tarifa_rubro': 'T001'
        }
        
        form_incompleto = TarifasICSForm(data=form_data_incompleto)
        
        if not form_incompleto.is_valid():
            print("✅ Formulario detecta datos faltantes correctamente")
            print("   Errores esperados:", form_incompleto.errors)
        else:
            print("❌ Formulario no detecta datos faltantes")
            return False
        
        # 7. Probar creación de tarifa ICS
        print("\n7️⃣ Probando creación de tarifa ICS...")
        
        # Simular el proceso de la vista
        if form.is_valid():
            rubro = form.cleaned_data.get('rubro')
            tarifa_rubro = form.cleaned_data.get('tarifa_rubro')
            valor_personalizado = form.cleaned_data.get('valor_personalizado')
            
            # Buscar la tarifa
            tarifa = Tarifas.objects.get(
                empresa=test_data['empre'],
                rubro=rubro,
                cod_tarifa=tarifa_rubro
            )
            
            # Usar valor personalizado o valor por defecto
            valor_final = valor_personalizado if valor_personalizado else tarifa.valor
            
            # Crear tarifa ICS
            tarifa_ics = TarifasICS(
                idneg=negocio.id,
                rtm=negocio.rtm,
                expe=negocio.expe,
                cod_tarifa=tarifa_rubro,
                valor=valor_final
            )
            tarifa_ics.save()
            
            print(f"✅ Tarifa ICS creada exitosamente")
            print(f"   ID Negocio: {tarifa_ics.idneg}")
            print(f"   RTM: {tarifa_ics.rtm}")
            print(f"   Expediente: {tarifa_ics.expe}")
            print(f"   Código Tarifa: {tarifa_ics.cod_tarifa}")
            print(f"   Valor: ${tarifa_ics.valor}")
        
        # 8. Verificar tarifa ICS en base de datos
        print("\n8️⃣ Verificando tarifa ICS en base de datos...")
        
        tarifas_ics = TarifasICS.objects.filter(idneg=negocio.id)
        print(f"   Tarifas ICS encontradas: {tarifas_ics.count()}")
        
        for tarifa_ics in tarifas_ics:
            print(f"   - {tarifa_ics.cod_tarifa}: ${tarifa_ics.valor}")
        
        print("\n✅ PRUEBA DEL FORMULARIO COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DEL FORMULARIO DE TASAS")
    print("=" * 60)
    
    resultado = test_formulario_tasas()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Formulario de tasas: FUNCIONANDO CORRECTAMENTE")
        print("✅ Todas las validaciones funcionan")
        print("✅ La creación de tarifas ICS funciona")
    else:
        print("❌ Formulario de tasas: FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()

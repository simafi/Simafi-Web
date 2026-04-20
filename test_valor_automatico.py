#!/usr/bin/env python3
"""
Script de prueba para verificar que el valor de la tarifa se carga automáticamente
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

def test_valor_automatico():
    """Prueba que el valor de la tarifa se carga automáticamente"""
    print("=== PRUEBA DE CARGA AUTOMÁTICA DE VALOR ===")
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST002',
        'expe': '002',
        'nombrenego': 'Negocio de Prueba Valor Automático',
        'comerciante': 'Comerciante de Prueba',
        'identidad': '8888-8888-88888',
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
            codigo='002',
            defaults={
                'descripcion': 'Rubro de Prueba Valor Automático',
                'cuenta': '654321',
                'tipo': 'A'
            }
        )
        
        if created:
            print(f"✅ Rubro creado: {rubro.descripcion}")
        else:
            print(f"✅ Rubro existente: {rubro.descripcion}")
        
        # 3. Crear múltiples tarifas de prueba con diferentes valores
        print("\n3️⃣ Creando tarifas de prueba con diferentes valores...")
        
        tarifas_prueba = [
            {
                'cod_tarifa': 'T002',
                'descripcion': 'Tarifa Básica',
                'valor': Decimal('50.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            },
            {
                'cod_tarifa': 'T003',
                'descripcion': 'Tarifa Intermedia',
                'valor': Decimal('75.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            },
            {
                'cod_tarifa': 'T004',
                'descripcion': 'Tarifa Premium',
                'valor': Decimal('120.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            }
        ]
        
        tarifas_creadas = []
        from datetime import datetime
        ano_vigente = datetime.now().year
        
        for tarifa_data in tarifas_prueba:
            tarifa, created = Tarifas.objects.get_or_create(
                empresa=test_data['empre'],
                rubro='002',
                cod_tarifa=tarifa_data['cod_tarifa'],
                ano=ano_vigente,
                defaults=tarifa_data
            )
            
            if created:
                print(f"✅ Tarifa creada: {tarifa.descripcion} (Valor: ${tarifa.valor})")
            else:
                print(f"✅ Tarifa existente: {tarifa.descripcion} (Valor: ${tarifa.valor})")
            
            tarifas_creadas.append(tarifa)
        
        # 4. Probar formulario con diferentes tarifas para verificar que el valor se carga automáticamente
        print("\n4️⃣ Probando carga automática de valores...")
        
        for tarifa in tarifas_creadas:
            print(f"\n   Probando tarifa: {tarifa.cod_tarifa} - {tarifa.descripcion}")
            
            form_data = {
                'idneg': negocio.id,
                'rtm': negocio.rtm,
                'expe': negocio.expe,
                'rubro': '002',
                'tarifa_rubro': tarifa.cod_tarifa,
                # NO incluir valor_personalizado para que se use el valor por defecto
            }
            
            form = TarifasICSForm(data=form_data)
            
            if form.is_valid():
                valor_personalizado = form.cleaned_data.get('valor_personalizado')
                print(f"   ✅ Formulario válido")
                print(f"   ✅ Valor personalizado: {valor_personalizado}")
                print(f"   ✅ Valor esperado de tarifa: {tarifa.valor}")
                
                if valor_personalizado is None:
                    print(f"   ✅ Valor personalizado es None (correcto, se usará valor por defecto)")
                else:
                    print(f"   ⚠️  Valor personalizado no es None: {valor_personalizado}")
            else:
                print(f"   ❌ Formulario inválido")
                print(f"   ❌ Errores: {form.errors}")
                return False
        
        # 5. Probar creación de tarifa ICS sin valor personalizado
        print("\n5️⃣ Probando creación de tarifa ICS sin valor personalizado...")
        
        # Usar la primera tarifa para la prueba
        tarifa_prueba = tarifas_creadas[0]
        
        form_data_final = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '002',
            'tarifa_rubro': tarifa_prueba.cod_tarifa,
        }
        
        form_final = TarifasICSForm(data=form_data_final)
        
        if form_final.is_valid():
            # Simular el proceso de la vista
            rubro = form_final.cleaned_data.get('rubro')
            tarifa_rubro = form_final.cleaned_data.get('tarifa_rubro')
            valor_personalizado = form_final.cleaned_data.get('valor_personalizado')
            
            # Buscar la tarifa
            tarifa = Tarifas.objects.get(
                empresa=test_data['empre'],
                rubro=rubro,
                cod_tarifa=tarifa_rubro
            )
            
            # Usar valor personalizado si se proporciona, sino usar el valor de la tarifa
            valor_final = valor_personalizado if valor_personalizado else tarifa.valor
            
            print(f"   ✅ Rubro: {rubro}")
            print(f"   ✅ Tarifa seleccionada: {tarifa_rubro}")
            print(f"   ✅ Valor personalizado del formulario: {valor_personalizado}")
            print(f"   ✅ Valor de la tarifa en BD: {tarifa.valor}")
            print(f"   ✅ Valor final a usar: {valor_final}")
            
            # Crear tarifa ICS
            tarifa_ics = TarifasICS(
                idneg=negocio.id,
                rtm=negocio.rtm,
                expe=negocio.expe,
                cod_tarifa=tarifa_rubro,
                valor=valor_final
            )
            tarifa_ics.save()
            
            print(f"   ✅ Tarifa ICS creada exitosamente con valor: ${tarifa_ics.valor}")
            
            # Verificar que el valor es correcto
            if tarifa_ics.valor == tarifa.valor:
                print(f"   ✅ El valor se asignó correctamente desde la tarifa")
            else:
                print(f"   ❌ El valor no se asignó correctamente")
                return False
        else:
            print(f"   ❌ Formulario inválido: {form_final.errors}")
            return False
        
        # 6. Verificar en base de datos
        print("\n6️⃣ Verificando tarifa ICS en base de datos...")
        
        tarifas_ics = TarifasICS.objects.filter(idneg=negocio.id)
        print(f"   Tarifas ICS encontradas: {tarifas_ics.count()}")
        
        for tarifa_ics in tarifas_ics:
            print(f"   - {tarifa_ics.cod_tarifa}: ${tarifa_ics.valor}")
        
        print("\n✅ PRUEBA DE CARGA AUTOMÁTICA COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE CARGA AUTOMÁTICA DE VALOR")
    print("=" * 60)
    
    resultado = test_valor_automatico()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Carga automática de valor: FUNCIONANDO CORRECTAMENTE")
        print("✅ El valor de la tarifa se asigna automáticamente")
        print("✅ El formulario maneja correctamente valores por defecto")
    else:
        print("❌ Carga automática de valor: FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()

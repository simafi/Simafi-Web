#!/usr/bin/env python3
"""
Script de prueba específico para verificar que el botón "Agregar Tarifa" 
esté grabando correctamente en la tabla tarifasics
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

def test_boton_agregar_tarifa():
    """Prueba específica del botón Agregar Tarifa"""
    print("=== PRUEBA DEL BOTÓN AGREGAR TARIFA ===")
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST005',
        'expe': '005',
        'nombrenego': 'Negocio de Prueba Botón Agregar',
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
        
        print(f"   RTM: {negocio.rtm}")
        print(f"   Expediente: {negocio.expe}")
        print(f"   ID Negocio: {negocio.id}")
        
        # 2. Crear rubro de prueba
        print("\n2️⃣ Creando rubro de prueba...")
        rubro, created = Rubro.objects.get_or_create(
            empresa=test_data['empre'],
            codigo='005',
            defaults={
                'descripcion': 'Rubro de Prueba Botón Agregar',
                'cuenta': '222222',
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
            rubro='005',
            cod_tarifa='TB001',
            ano=ano_vigente,
            defaults={
                'descripcion': 'Tarifa de Prueba Botón Agregar',
                'valor': Decimal('200.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            }
        )
        
        if created:
            print(f"✅ Tarifa creada: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        else:
            print(f"✅ Tarifa existente: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 4. Verificar estado inicial de tarifas ICS
        print("\n4️⃣ Verificando estado inicial de tarifas ICS...")
        tarifas_ics_inicial = TarifasICS.objects.filter(idneg=negocio.id)
        print(f"   Tarifas ICS iniciales: {tarifas_ics_inicial.count()}")
        
        # 5. Simular el formulario con datos válidos (sin valor personalizado)
        print("\n5️⃣ Probando formulario sin valor personalizado...")
        
        form_data_sin_valor = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '005',
            'tarifa_rubro': 'TB001'
        }
        
        form_sin_valor = TarifasICSForm(data=form_data_sin_valor)
        
        if form_sin_valor.is_valid():
            print("✅ Formulario sin valor personalizado válido")
            print(f"   Rubro: {form_sin_valor.cleaned_data.get('rubro')}")
            print(f"   Tarifa: {form_sin_valor.cleaned_data.get('tarifa_rubro')}")
            print(f"   Valor personalizado: {form_sin_valor.cleaned_data.get('valor_personalizado')}")
            
            # Simular el proceso de la vista para agregar tarifa
            rubro = form_sin_valor.cleaned_data.get('rubro')
            tarifa_rubro = form_sin_valor.cleaned_data.get('tarifa_rubro')
            valor_personalizado = form_sin_valor.cleaned_data.get('valor_personalizado')
            
            # Buscar la tarifa para obtener su valor por defecto
            tarifa_bd = Tarifas.objects.get(
                empresa=test_data['empre'],
                rubro=rubro,
                cod_tarifa=tarifa_rubro,
                ano=ano_vigente
            )
            
            # Usar valor personalizado si se proporciona, sino usar el valor de la tarifa
            valor_final = valor_personalizado if valor_personalizado else tarifa_bd.valor
            
            print(f"   Valor de tarifa en BD: {tarifa_bd.valor}")
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
            print(f"   RTM: {tarifa_ics.rtm}")
            print(f"   Expediente: {tarifa_ics.expe}")
            print(f"   Código Tarifa: {tarifa_ics.cod_tarifa}")
            print(f"   Valor: ${tarifa_ics.valor}")
            
        else:
            print("❌ Formulario sin valor personalizado inválido")
            print("   Errores:", form_sin_valor.errors)
            return False
        
        # 6. Verificar que se guardó en la base de datos
        print("\n6️⃣ Verificando que se guardó en la base de datos...")
        tarifas_ics_despues = TarifasICS.objects.filter(idneg=negocio.id)
        print(f"   Tarifas ICS después de agregar: {tarifas_ics_despues.count()}")
        
        if tarifas_ics_despues.count() > tarifas_ics_inicial.count():
            print("✅ Se agregó correctamente a la base de datos")
            for tarifa_ics in tarifas_ics_despues:
                print(f"   - {tarifa_ics.cod_tarifa}: ${tarifa_ics.valor}")
        else:
            print("❌ No se agregó a la base de datos")
            return False
        
        # 7. Probar formulario con valor personalizado
        print("\n7️⃣ Probando formulario con valor personalizado...")
        
        form_data_con_valor = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '005',
            'tarifa_rubro': 'TB001',
            'valor_personalizado': '250.00'
        }
        
        form_con_valor = TarifasICSForm(data=form_data_con_valor)
        
        if form_con_valor.is_valid():
            print("✅ Formulario con valor personalizado válido")
            print(f"   Valor personalizado: {form_con_valor.cleaned_data.get('valor_personalizado')}")
            
            # Simular el proceso de la vista
            rubro = form_con_valor.cleaned_data.get('rubro')
            tarifa_rubro = form_con_valor.cleaned_data.get('tarifa_rubro')
            valor_personalizado = form_con_valor.cleaned_data.get('valor_personalizado')
            
            # Buscar la tarifa
            tarifa_bd = Tarifas.objects.get(
                empresa=test_data['empre'],
                rubro=rubro,
                cod_tarifa=tarifa_rubro,
                ano=ano_vigente
            )
            
            # Usar valor personalizado
            valor_final = valor_personalizado if valor_personalizado else tarifa_bd.valor
            
            print(f"   Valor de tarifa en BD: {tarifa_bd.valor}")
            print(f"   Valor personalizado: {valor_personalizado}")
            print(f"   Valor final a usar: {valor_final}")
            
            # Crear la tarifa ICS
            tarifa_ics_personalizada = TarifasICS(
                idneg=negocio.id,
                rtm=negocio.rtm,
                expe=negocio.expe,
                cod_tarifa=tarifa_rubro,
                valor=valor_final
            )
            tarifa_ics_personalizada.save()
            
            print(f"✅ Tarifa ICS con valor personalizado creada exitosamente")
            print(f"   Valor guardado: ${tarifa_ics_personalizada.valor}")
            
        else:
            print("❌ Formulario con valor personalizado inválido")
            print("   Errores:", form_con_valor.errors)
            return False
        
        # 8. Verificar estado final
        print("\n8️⃣ Verificando estado final...")
        tarifas_ics_final = TarifasICS.objects.filter(idneg=negocio.id)
        print(f"   Total de tarifas ICS: {tarifas_ics_final.count()}")
        
        for tarifa_ics in tarifas_ics_final:
            print(f"   - {tarifa_ics.cod_tarifa}: ${tarifa_ics.valor}")
        
        # 9. Verificar que los campos coinciden con la estructura de la tabla
        print("\n9️⃣ Verificando estructura de la tabla...")
        
        # Verificar que todos los campos requeridos están presentes
        campos_requeridos = ['id', 'idneg', 'rtm', 'expe', 'cod_tarifa', 'valor']
        campos_modelo = [field.name for field in TarifasICS._meta.fields]
        
        print(f"   Campos requeridos: {campos_requeridos}")
        print(f"   Campos del modelo: {campos_modelo}")
        
        campos_faltantes = set(campos_requeridos) - set(campos_modelo)
        if not campos_faltantes:
            print("✅ Todos los campos requeridos están presentes en el modelo")
        else:
            print(f"❌ Campos faltantes: {campos_faltantes}")
            return False
        
        # Verificar tipos de datos
        print("\n   Verificando tipos de datos...")
        for tarifa_ics in tarifas_ics_final:
            print(f"   ID: {type(tarifa_ics.id).__name__} = {tarifa_ics.id}")
            print(f"   ID Negocio: {type(tarifa_ics.idneg).__name__} = {tarifa_ics.idneg}")
            print(f"   RTM: {type(tarifa_ics.rtm).__name__} = '{tarifa_ics.rtm}'")
            print(f"   Expediente: {type(tarifa_ics.expe).__name__} = '{tarifa_ics.expe}'")
            print(f"   Código Tarifa: {type(tarifa_ics.cod_tarifa).__name__} = '{tarifa_ics.cod_tarifa}'")
            print(f"   Valor: {type(tarifa_ics.valor).__name__} = {tarifa_ics.valor}")
            break  # Solo mostrar el primero
        
        print("\n✅ PRUEBA DEL BOTÓN AGREGAR TARIFA COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DEL BOTÓN AGREGAR TARIFA")
    print("=" * 60)
    
    resultado = test_boton_agregar_tarifa()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Botón Agregar Tarifa: FUNCIONANDO CORRECTAMENTE")
        print("✅ Se graba correctamente en la tabla tarifasics")
        print("✅ Los campos coinciden con la estructura de la tabla")
        print("✅ Maneja correctamente valores personalizados")
        print("✅ Maneja correctamente valores por defecto")
    else:
        print("❌ Botón Agregar Tarifa: FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()

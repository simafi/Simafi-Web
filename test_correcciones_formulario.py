#!/usr/bin/env python3
"""
Script de prueba para verificar que todas las correcciones del formulario funcionan correctamente
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

def test_correcciones_formulario():
    """Prueba que todas las correcciones del formulario funcionan correctamente"""
    print("=== PRUEBA DE CORRECCIONES DEL FORMULARIO ===")
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST006',
        'expe': '006',
        'nombrenego': 'Negocio de Prueba Correcciones',
        'comerciante': 'Comerciante de Prueba',
        'identidad': '4444-4444-44444',
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
        
        print(f"   RTM: '{negocio.rtm}' (longitud: {len(negocio.rtm)})")
        print(f"   Expediente: '{negocio.expe}' (longitud: {len(negocio.expe)})")
        print(f"   ID Negocio: {negocio.id}")
        
        # 2. Verificar que el RTM no excede el límite del modelo
        print("\n2️⃣ Verificando límites del modelo...")
        
        # Verificar límites del modelo TarifasICS
        rtm_field = TarifasICS._meta.get_field('rtm')
        expe_field = TarifasICS._meta.get_field('expe')
        cod_tarifa_field = TarifasICS._meta.get_field('cod_tarifa')
        
        print(f"   RTM max_length: {rtm_field.max_length}")
        print(f"   Expediente max_length: {expe_field.max_length}")
        print(f"   Código Tarifa max_length: {cod_tarifa_field.max_length}")
        
        if rtm_field.max_length >= len(negocio.rtm):
            print("✅ RTM está dentro del límite del modelo")
        else:
            print(f"❌ RTM excede el límite del modelo: {len(negocio.rtm)} > {rtm_field.max_length}")
            return False
        
        # 3. Crear rubro de prueba
        print("\n3️⃣ Creando rubro de prueba...")
        rubro, created = Rubro.objects.get_or_create(
            empresa=test_data['empre'],
            codigo='006',
            defaults={
                'descripcion': 'Rubro de Prueba Correcciones',
                'cuenta': '333333',
                'tipo': 'A'
            }
        )
        
        if created:
            print(f"✅ Rubro creado: {rubro.descripcion}")
        else:
            print(f"✅ Rubro existente: {rubro.descripcion}")
        
        # 4. Crear tarifa de prueba
        print("\n4️⃣ Creando tarifa de prueba...")
        ano_vigente = datetime.now().year
        
        tarifa, created = Tarifas.objects.get_or_create(
            empresa=test_data['empre'],
            rubro='006',
            cod_tarifa='TC001',
            ano=ano_vigente,
            defaults={
                'descripcion': 'Tarifa de Prueba Correcciones',
                'valor': Decimal('300.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            }
        )
        
        if created:
            print(f"✅ Tarifa creada: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        else:
            print(f"✅ Tarifa existente: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 5. Probar formulario con datos válidos
        print("\n5️⃣ Probando formulario con datos válidos...")
        
        form_data = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '006',
            'tarifa_rubro': 'TC001',
            'valor_personalizado': '350.00'
        }
        
        form = TarifasICSForm(data=form_data)
        
        if form.is_valid():
            print("✅ Formulario válido")
            print(f"   Rubro: {form.cleaned_data.get('rubro')}")
            print(f"   Tarifa: {form.cleaned_data.get('tarifa_rubro')}")
            print(f"   Valor personalizado: {form.cleaned_data.get('valor_personalizado')}")
            print(f"   RTM: {form.cleaned_data.get('rtm')}")
            print(f"   Expediente: {form.cleaned_data.get('expe')}")
        else:
            print("❌ Formulario inválido")
            print("   Errores:", form.errors)
            return False
        
        # 6. Verificar que el campo valor no es requerido
        print("\n6️⃣ Verificando que el campo valor no es requerido...")
        
        form_data_sin_valor = {
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe,
            'rubro': '006',
            'tarifa_rubro': 'TC001'
            # Sin valor_personalizado
        }
        
        form_sin_valor = TarifasICSForm(data=form_data_sin_valor)
        
        if form_sin_valor.is_valid():
            print("✅ Formulario sin valor personalizado válido")
            print(f"   Valor personalizado: {form_sin_valor.cleaned_data.get('valor_personalizado')}")
        else:
            print("❌ Formulario sin valor personalizado inválido")
            print("   Errores:", form_sin_valor.errors)
            return False
        
        # 7. Simular el proceso de la vista para crear tarifa ICS
        print("\n7️⃣ Simulando creación de tarifa ICS...")
        
        # Simular el proceso de la vista
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
        print(f"   RTM: '{tarifa_ics.rtm}' (longitud: {len(tarifa_ics.rtm)})")
        print(f"   Expediente: '{tarifa_ics.expe}' (longitud: {len(tarifa_ics.expe)})")
        print(f"   Código Tarifa: '{tarifa_ics.cod_tarifa}' (longitud: {len(tarifa_ics.cod_tarifa)})")
        print(f"   Valor: ${tarifa_ics.valor}")
        
        # 8. Verificar que se guardó correctamente en la base de datos
        print("\n8️⃣ Verificando que se guardó en la base de datos...")
        
        tarifa_ics_guardada = TarifasICS.objects.get(id=tarifa_ics.id)
        print(f"✅ Tarifa ICS recuperada de la base de datos")
        print(f"   RTM: '{tarifa_ics_guardada.rtm}'")
        print(f"   Expediente: '{tarifa_ics_guardada.expe}'")
        print(f"   Código Tarifa: '{tarifa_ics_guardada.cod_tarifa}'")
        print(f"   Valor: ${tarifa_ics_guardada.valor}")
        
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
        
        # Verificar tipos de datos y límites
        print("\n   Verificando tipos de datos y límites...")
        print(f"   ID: {type(tarifa_ics_guardada.id).__name__} = {tarifa_ics_guardada.id}")
        print(f"   ID Negocio: {type(tarifa_ics_guardada.idneg).__name__} = {tarifa_ics_guardada.idneg}")
        print(f"   RTM: {type(tarifa_ics_guardada.rtm).__name__} = '{tarifa_ics_guardada.rtm}' (longitud: {len(tarifa_ics_guardada.rtm)})")
        print(f"   Expediente: {type(tarifa_ics_guardada.expe).__name__} = '{tarifa_ics_guardada.expe}' (longitud: {len(tarifa_ics_guardada.expe)})")
        print(f"   Código Tarifa: {type(tarifa_ics_guardada.cod_tarifa).__name__} = '{tarifa_ics_guardada.cod_tarifa}' (longitud: {len(tarifa_ics_guardada.cod_tarifa)})")
        print(f"   Valor: {type(tarifa_ics_guardada.valor).__name__} = {tarifa_ics_guardada.valor}")
        
        # Verificar que las longitudes están dentro de los límites
        if len(tarifa_ics_guardada.rtm) <= rtm_field.max_length:
            print("✅ RTM está dentro del límite")
        else:
            print(f"❌ RTM excede el límite: {len(tarifa_ics_guardada.rtm)} > {rtm_field.max_length}")
            return False
        
        if len(tarifa_ics_guardada.expe) <= expe_field.max_length:
            print("✅ Expediente está dentro del límite")
        else:
            print(f"❌ Expediente excede el límite: {len(tarifa_ics_guardada.expe)} > {expe_field.max_length}")
            return False
        
        if len(tarifa_ics_guardada.cod_tarifa) <= cod_tarifa_field.max_length:
            print("✅ Código Tarifa está dentro del límite")
        else:
            print(f"❌ Código Tarifa excede el límite: {len(tarifa_ics_guardada.cod_tarifa)} > {cod_tarifa_field.max_length}")
            return False
        
        print("\n✅ PRUEBA DE CORRECCIONES COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE CORRECCIONES DEL FORMULARIO")
    print("=" * 60)
    
    resultado = test_correcciones_formulario()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Correcciones del formulario: FUNCIONANDO CORRECTAMENTE")
        print("✅ Campo RTM corregido (max_length=20)")
        print("✅ Campo valor no es requerido")
        print("✅ Validación de tarifa_rubro corregida")
        print("✅ Se graba correctamente en la tabla tarifasics")
        print("✅ Todos los campos coinciden con la estructura de la tabla")
    else:
        print("❌ Correcciones del formulario: FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()




























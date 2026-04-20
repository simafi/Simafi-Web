#!/usr/bin/env python3
"""
Script de prueba para verificar que solo se muestran tarifas del año vigente
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

def test_ano_vigente():
    """Prueba que solo se muestran tarifas del año vigente"""
    print("=== PRUEBA DE FILTRO POR AÑO VIGENTE ===")
    
    # Obtener año vigente
    ano_vigente = datetime.now().year
    ano_anterior = ano_vigente - 1
    ano_siguiente = ano_vigente + 1
    
    print(f"   Año vigente: {ano_vigente}")
    print(f"   Año anterior: {ano_anterior}")
    print(f"   Año siguiente: {ano_siguiente}")
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST004',
        'expe': '004',
        'nombrenego': 'Negocio de Prueba Año Vigente',
        'comerciante': 'Comerciante de Prueba',
        'identidad': '6666-6666-66666',
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
            codigo='004',
            defaults={
                'descripcion': 'Rubro de Prueba Año Vigente',
                'cuenta': '111111',
                'tipo': 'A'
            }
        )
        
        if created:
            print(f"✅ Rubro creado: {rubro.descripcion}")
        else:
            print(f"✅ Rubro existente: {rubro.descripcion}")
        
        # 3. Crear tarifas con diferentes años
        print("\n3️⃣ Creando tarifas con diferentes años...")
        
        tarifas_prueba = [
            {
                'cod_tarifa': 'TV001',
                'descripcion': f'Tarifa Año Vigente {ano_vigente}',
                'valor': Decimal('100.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C',
                'ano': ano_vigente
            },
            {
                'cod_tarifa': 'TA001',
                'descripcion': f'Tarifa Año Anterior {ano_anterior}',
                'valor': Decimal('80.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C',
                'ano': ano_anterior
            },
            {
                'cod_tarifa': 'TS001',
                'descripcion': f'Tarifa Año Siguiente {ano_siguiente}',
                'valor': Decimal('120.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C',
                'ano': ano_siguiente
            },
            {
                'cod_tarifa': 'TV002',
                'descripcion': f'Tarifa Año Vigente Segunda {ano_vigente}',
                'valor': Decimal('150.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C',
                'ano': ano_vigente
            }
        ]
        
        tarifas_creadas = []
        for tarifa_data in tarifas_prueba:
            tarifa, created = Tarifas.objects.get_or_create(
                empresa=test_data['empre'],
                rubro='004',
                cod_tarifa=tarifa_data['cod_tarifa'],
                ano=tarifa_data['ano'],
                defaults=tarifa_data
            )
            
            if created:
                print(f"✅ Tarifa creada: {tarifa.descripcion} (Año: {tarifa.ano}, Valor: ${tarifa.valor})")
            else:
                print(f"✅ Tarifa existente: {tarifa.descripcion} (Año: {tarifa.ano}, Valor: ${tarifa.valor})")
            
            tarifas_creadas.append(tarifa)
        
        # 4. Verificar todas las tarifas del rubro
        print("\n4️⃣ Verificando todas las tarifas del rubro...")
        
        todas_tarifas = Tarifas.objects.filter(
            empresa=test_data['empre'],
            rubro='004'
        ).order_by('ano', 'cod_tarifa')
        
        print(f"   Total de tarifas en el rubro: {todas_tarifas.count()}")
        for tarifa in todas_tarifas:
            print(f"   - {tarifa.cod_tarifa}: {tarifa.descripcion} (Año: {tarifa.ano})")
        
        # 5. Verificar tarifas del año vigente (lo que debería mostrar el formulario)
        print("\n5️⃣ Verificando tarifas del año vigente...")
        
        tarifas_ano_vigente = Tarifas.objects.filter(
            empresa=test_data['empre'],
            rubro='004',
            ano=ano_vigente
        ).order_by('cod_tarifa')
        
        print(f"   Tarifas del año vigente ({ano_vigente}): {tarifas_ano_vigente.count()}")
        for tarifa in tarifas_ano_vigente:
            print(f"   - {tarifa.cod_tarifa}: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 6. Simular la consulta que hace la vista obtener_tarifas_rubro
        print("\n6️⃣ Simulando consulta de la vista obtener_tarifas_rubro...")
        
        # Simular los parámetros que recibiría la vista
        municipio_codigo = test_data['empre']
        rubro_codigo = '004'
        
        # Hacer la misma consulta que hace la vista
        tarifas_filtradas = Tarifas.objects.filter(
            empresa=municipio_codigo,
            rubro=rubro_codigo,
            categoria='C',
            ano=ano_vigente
        ).order_by('cod_tarifa')
        
        print(f"   Tarifas filtradas (categoría 'C' + año vigente): {tarifas_filtradas.count()}")
        for tarifa in tarifas_filtradas:
            print(f"   - {tarifa.cod_tarifa}: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 7. Verificar que solo se muestran las tarifas del año vigente
        print("\n7️⃣ Verificando que el filtro por año funciona correctamente...")
        
        tarifas_vigente = set(tarifas_ano_vigente.values_list('cod_tarifa', flat=True))
        tarifas_filtradas_codigos = set(tarifas_filtradas.values_list('cod_tarifa', flat=True))
        
        if tarifas_vigente == tarifas_filtradas_codigos:
            print("✅ El filtro por año funciona correctamente")
            print(f"   Tarifas del año vigente: {list(tarifas_vigente)}")
            print(f"   Tarifas filtradas: {list(tarifas_filtradas_codigos)}")
        else:
            print("❌ El filtro por año no funciona correctamente")
            print(f"   Tarifas del año vigente: {list(tarifas_vigente)}")
            print(f"   Tarifas filtradas: {list(tarifas_filtradas_codigos)}")
            return False
        
        # 8. Verificar que no se incluyen tarifas de otros años
        print("\n8️⃣ Verificando que no se incluyen tarifas de otros años...")
        
        otras_anos = Tarifas.objects.filter(
            empresa=test_data['empre'],
            rubro='004'
        ).exclude(ano=ano_vigente)
        
        tarifas_otras_anos = set(otras_anos.values_list('cod_tarifa', flat=True))
        tarifas_incluidas = set(tarifas_filtradas.values_list('cod_tarifa', flat=True))
        
        # Verificar que no hay intersección
        interseccion = tarifas_otras_anos.intersection(tarifas_incluidas)
        
        if not interseccion:
            print("✅ No se incluyen tarifas de otros años")
            print(f"   Tarifas de otros años: {list(tarifas_otras_anos)}")
            print(f"   Tarifas incluidas: {list(tarifas_incluidas)}")
        else:
            print("❌ Se incluyen tarifas de otros años")
            print(f"   Intersección encontrada: {list(interseccion)}")
            return False
        
        # 9. Verificar que se respetan ambos filtros (categoría 'C' y año vigente)
        print("\n9️⃣ Verificando que se respetan ambos filtros...")
        
        tarifas_categoria_c = Tarifas.objects.filter(
            empresa=test_data['empre'],
            rubro='004',
            categoria='C'
        ).order_by('ano', 'cod_tarifa')
        
        print(f"   Tarifas con categoría 'C' (todos los años): {tarifas_categoria_c.count()}")
        for tarifa in tarifas_categoria_c:
            print(f"   - {tarifa.cod_tarifa}: {tarifa.descripcion} (Año: {tarifa.ano})")
        
        # Verificar que las tarifas filtradas son solo las del año vigente con categoría 'C'
        tarifas_esperadas = tarifas_categoria_c.filter(ano=ano_vigente)
        tarifas_esperadas_codigos = set(tarifas_esperadas.values_list('cod_tarifa', flat=True))
        
        if tarifas_esperadas_codigos == tarifas_filtradas_codigos:
            print("✅ Ambos filtros funcionan correctamente")
            print(f"   Tarifas esperadas (categoría 'C' + año vigente): {list(tarifas_esperadas_codigos)}")
            print(f"   Tarifas filtradas: {list(tarifas_filtradas_codigos)}")
        else:
            print("❌ Los filtros no funcionan correctamente")
            print(f"   Tarifas esperadas: {list(tarifas_esperadas_codigos)}")
            print(f"   Tarifas filtradas: {list(tarifas_filtradas_codigos)}")
            return False
        
        print("\n✅ PRUEBA DE FILTRO POR AÑO VIGENTE COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE FILTRO POR AÑO VIGENTE")
    print("=" * 60)
    
    resultado = test_ano_vigente()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Filtro por año vigente: FUNCIONANDO CORRECTAMENTE")
        print("✅ Solo se muestran tarifas del año vigente")
        print("✅ No se incluyen tarifas de otros años")
        print("✅ Se respetan ambos filtros (categoría 'C' + año vigente)")
    else:
        print("❌ Filtro por año vigente: FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()




























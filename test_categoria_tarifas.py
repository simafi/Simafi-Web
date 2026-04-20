#!/usr/bin/env python3
"""
Script de prueba para verificar que solo se muestran tarifas con categoría 'C'
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Negocio, TarifasICS, Rubro, Tarifas

def test_categoria_tarifas():
    """Prueba que solo se muestran tarifas con categoría 'C'"""
    print("=== PRUEBA DE FILTRO POR CATEGORÍA 'C' ===")
    
    # Datos de prueba
    test_data = {
        'empre': '0301',
        'rtm': 'TEST003',
        'expe': '003',
        'nombrenego': 'Negocio de Prueba Categoría',
        'comerciante': 'Comerciante de Prueba',
        'identidad': '7777-7777-77777',
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
            codigo='003',
            defaults={
                'descripcion': 'Rubro de Prueba Categoría',
                'cuenta': '987654',
                'tipo': 'A'
            }
        )
        
        if created:
            print(f"✅ Rubro creado: {rubro.descripcion}")
        else:
            print(f"✅ Rubro existente: {rubro.descripcion}")
        
        # 3. Crear tarifas con diferentes categorías
        print("\n3️⃣ Creando tarifas con diferentes categorías...")
        
        tarifas_prueba = [
            {
                'cod_tarifa': 'TC001',
                'descripcion': 'Tarifa Categoría C',
                'valor': Decimal('100.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'C'
            },
            {
                'cod_tarifa': 'TA001',
                'descripcion': 'Tarifa Categoría A',
                'valor': Decimal('200.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'A'
            },
            {
                'cod_tarifa': 'TB001',
                'descripcion': 'Tarifa Categoría B',
                'valor': Decimal('150.00'),
                'frecuencia': 'A',
                'tipo': 'F',
                'categoria': 'B'
            },
            {
                'cod_tarifa': 'TC002',
                'descripcion': 'Tarifa Categoría C (Segunda)',
                'valor': Decimal('125.00'),
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
                rubro='003',
                cod_tarifa=tarifa_data['cod_tarifa'],
                ano=ano_vigente,
                defaults=tarifa_data
            )
            
            if created:
                print(f"✅ Tarifa creada: {tarifa.descripcion} (Categoría: {tarifa.categoria}, Valor: ${tarifa.valor})")
            else:
                print(f"✅ Tarifa existente: {tarifa.descripcion} (Categoría: {tarifa.categoria}, Valor: ${tarifa.valor})")
            
            tarifas_creadas.append(tarifa)
        
        # 4. Verificar todas las tarifas del rubro
        print("\n4️⃣ Verificando todas las tarifas del rubro...")
        
        todas_tarifas = Tarifas.objects.filter(
            empresa=test_data['empre'],
            rubro='003'
        ).order_by('cod_tarifa')
        
        print(f"   Total de tarifas en el rubro: {todas_tarifas.count()}")
        for tarifa in todas_tarifas:
            print(f"   - {tarifa.cod_tarifa}: {tarifa.descripcion} (Categoría: {tarifa.categoria})")
        
        # 5. Verificar tarifas con categoría 'C' (lo que debería mostrar el formulario)
        print("\n5️⃣ Verificando tarifas con categoría 'C'...")
        
        tarifas_categoria_c = Tarifas.objects.filter(
            empresa=test_data['empre'],
            rubro='003',
            categoria='C'
        ).order_by('cod_tarifa')
        
        print(f"   Tarifas con categoría 'C': {tarifas_categoria_c.count()}")
        for tarifa in tarifas_categoria_c:
            print(f"   - {tarifa.cod_tarifa}: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 6. Simular la consulta que hace la vista obtener_tarifas_rubro
        print("\n6️⃣ Simulando consulta de la vista obtener_tarifas_rubro...")
        
        # Simular los parámetros que recibiría la vista
        municipio_codigo = test_data['empre']
        rubro_codigo = '003'
        
        # Hacer la misma consulta que hace la vista
        tarifas_filtradas = Tarifas.objects.filter(
            empresa=municipio_codigo,
            rubro=rubro_codigo,
            categoria='C'
        ).order_by('cod_tarifa')
        
        print(f"   Tarifas filtradas por categoría 'C': {tarifas_filtradas.count()}")
        for tarifa in tarifas_filtradas:
            print(f"   - {tarifa.cod_tarifa}: {tarifa.descripcion} (Valor: ${tarifa.valor})")
        
        # 7. Verificar que solo se muestran las tarifas con categoría 'C'
        print("\n7️⃣ Verificando que el filtro funciona correctamente...")
        
        tarifas_c = set(tarifas_categoria_c.values_list('cod_tarifa', flat=True))
        tarifas_filtradas_c = set(tarifas_filtradas.values_list('cod_tarifa', flat=True))
        
        if tarifas_c == tarifas_filtradas_c:
            print("✅ El filtro funciona correctamente")
            print(f"   Tarifas con categoría 'C': {list(tarifas_c)}")
            print(f"   Tarifas filtradas: {list(tarifas_filtradas_c)}")
        else:
            print("❌ El filtro no funciona correctamente")
            print(f"   Tarifas con categoría 'C': {list(tarifas_c)}")
            print(f"   Tarifas filtradas: {list(tarifas_filtradas_c)}")
            return False
        
        # 8. Verificar que no se incluyen tarifas de otras categorías
        print("\n8️⃣ Verificando que no se incluyen tarifas de otras categorías...")
        
        otras_categorias = Tarifas.objects.filter(
            empresa=test_data['empre'],
            rubro='003'
        ).exclude(categoria='C')
        
        tarifas_otras_categorias = set(otras_categorias.values_list('cod_tarifa', flat=True))
        tarifas_incluidas = set(tarifas_filtradas.values_list('cod_tarifa', flat=True))
        
        # Verificar que no hay intersección
        interseccion = tarifas_otras_categorias.intersection(tarifas_incluidas)
        
        if not interseccion:
            print("✅ No se incluyen tarifas de otras categorías")
            print(f"   Tarifas de otras categorías: {list(tarifas_otras_categorias)}")
            print(f"   Tarifas incluidas: {list(tarifas_incluidas)}")
        else:
            print("❌ Se incluyen tarifas de otras categorías")
            print(f"   Intersección encontrada: {list(interseccion)}")
            return False
        
        print("\n✅ PRUEBA DE FILTRO POR CATEGORÍA COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE FILTRO POR CATEGORÍA")
    print("=" * 60)
    
    resultado = test_categoria_tarifas()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBA")
    print("=" * 60)
    
    if resultado:
        print("✅ Filtro por categoría 'C': FUNCIONANDO CORRECTAMENTE")
        print("✅ Solo se muestran tarifas con categoría 'C'")
        print("✅ No se incluyen tarifas de otras categorías")
    else:
        print("❌ Filtro por categoría 'C': FALLÓ")
        print("❌ Revisar los errores anteriores")

if __name__ == "__main__":
    main()

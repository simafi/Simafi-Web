#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import PlanArbitrio

def create_test_data():
    print("=== CREANDO DATOS DE PRUEBA PARA PLAN ARBITRIO ===")
    
    # Datos de prueba
    test_data = [
        {
            'empresa': '0301',
            'rubro': '0004', 
            'cod_tarifa': '01',
            'ano': 2025,
            'codigo': 'LIC001',
            'descripcion': 'Licencia Comercial Pequeña',
            'minimo': 1000000,
            'maximo': 5000000,
            'valor': 2500000
        },
        {
            'empresa': '0301',
            'rubro': '0004',
            'cod_tarifa': '01', 
            'ano': 2025,
            'codigo': 'LIC002',
            'descripcion': 'Licencia Comercial Mediana',
            'minimo': 5000000,
            'maximo': 15000000,
            'valor': 7500000
        },
        {
            'empresa': '0301',
            'rubro': '0005',
            'cod_tarifa': '02',
            'ano': 2025, 
            'codigo': 'IND001',
            'descripcion': 'Licencia Industrial',
            'minimo': 2000000,
            'maximo': 10000000,
            'valor': 5000000
        }
    ]
    
    created_count = 0
    
    for data in test_data:
        try:
            # Verificar si ya existe
            existing = PlanArbitrio.objects.filter(
                empresa=data['empresa'],
                rubro=data['rubro'],
                cod_tarifa=data['cod_tarifa'],
                ano=data['ano'],
                codigo=data['codigo']
            ).first()
            
            if existing:
                print(f"⚠️  Ya existe: {data['empresa']}-{data['rubro']}-{data['cod_tarifa']}-{data['ano']}-{data['codigo']}")
            else:
                plan = PlanArbitrio.objects.create(**data)
                print(f"✅ Creado: {plan}")
                created_count += 1
                
        except Exception as e:
            print(f"❌ Error creando {data['codigo']}: {e}")
    
    print(f"\n📊 Resumen:")
    print(f"   - Registros creados: {created_count}")
    print(f"   - Total en base de datos: {PlanArbitrio.objects.count()}")
    
    print(f"\n🧪 DATOS DE PRUEBA DISPONIBLES:")
    print(f"   Para probar la validación, usa estos datos:")
    print(f"   - Empresa: 0301")
    print(f"   - Rubro: 0004") 
    print(f"   - Código Tarifa: 01")
    print(f"   - Año: 2025")
    print(f"   - Código: LIC001 o LIC002")

if __name__ == "__main__":
    create_test_data()

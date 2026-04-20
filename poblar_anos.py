#!/usr/bin/env python3
"""
Script para poblar la tabla anos con años de ejemplo
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')

try:
    django.setup()
    from tributario_app.models import Anos
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def poblar_anos():
    """Poblar tabla anos con años de ejemplo"""
    
    # Años a crear (últimos 10 años + próximos 2)
    ano_actual = 2024
    anos_crear = list(range(ano_actual - 8, ano_actual + 3))  # 2016-2026
    
    print(f"Creando años: {anos_crear}")
    
    for ano in anos_crear:
        try:
            ano_obj, created = Anos.objects.get_or_create(ano=ano)
            if created:
                print(f"✅ Año {ano} creado")
            else:
                print(f"ℹ️  Año {ano} ya existe")
        except Exception as e:
            print(f"❌ Error creando año {ano}: {e}")
    
    # Mostrar resumen
    total_anos = Anos.objects.count()
    print(f"\n📊 Total años en base de datos: {total_anos}")
    
    anos_existentes = Anos.objects.all().order_by('-ano')
    print("Años disponibles:")
    for ano in anos_existentes:
        print(f"  - {ano.ano}")

if __name__ == "__main__":
    poblar_anos()

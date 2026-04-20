#!/usr/bin/env python3
"""
Script para poblar la tabla anos con datos de ejemplo
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

def poblar_tabla_anos():
    """Poblar tabla anos con años relevantes"""
    
    # Crear años desde 2015 hasta 2026
    anos_crear = list(range(2015, 2027))
    
    print(f"Poblando tabla anos con años: {anos_crear[0]} - {anos_crear[-1]}")
    
    creados = 0
    existentes = 0
    
    for ano in anos_crear:
        try:
            ano_obj, created = Anos.objects.get_or_create(ano=ano)
            if created:
                print(f"✅ Año {ano} creado")
                creados += 1
            else:
                print(f"ℹ️  Año {ano} ya existe")
                existentes += 1
        except Exception as e:
            print(f"❌ Error creando año {ano}: {e}")
    
    print(f"\n📊 Resumen:")
    print(f"   - Años creados: {creados}")
    print(f"   - Años existentes: {existentes}")
    print(f"   - Total en BD: {Anos.objects.count()}")
    
    # Mostrar todos los años ordenados
    print("\n📅 Años disponibles (más recientes primero):")
    anos_existentes = Anos.objects.all().order_by('-ano')
    for ano in anos_existentes:
        print(f"   - {int(ano.ano)}")

if __name__ == "__main__":
    poblar_tabla_anos()

#!/usr/bin/env python
"""
Script para crear años de prueba en la tabla anos.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Anos

def crear_anos_prueba():
    """Crear años de prueba en la tabla anos"""
    print("=== CREANDO AÑOS DE PRUEBA ===")
    
    # Lista de años a crear (2020-2030)
    anos_a_crear = list(range(2020, 2031))
    
    for ano in anos_a_crear:
        try:
            # Verificar si el año ya existe
            ano_obj, created = Anos.objects.get_or_create(ano=ano)
            
            if created:
                print(f"✅ Año {ano} creado exitosamente")
            else:
                print(f"ℹ️  Año {ano} ya existe")
                
        except Exception as e:
            print(f"❌ Error al crear año {ano}: {e}")
    
    print("\n=== RESUMEN ===")
    total_anos = Anos.objects.count()
    print(f"Total de años en la base de datos: {total_anos}")
    
    # Mostrar todos los años
    anos_existentes = Anos.objects.all().order_by('ano')
    print("Años disponibles:")
    for ano in anos_existentes:
        print(f"  - {ano.ano}")

if __name__ == "__main__":
    crear_anos_prueba()






































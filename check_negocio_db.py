#!/usr/bin/env python3
"""
Script para verificar si el negocio existe en la base de datos
"""

import os
import sys
import django

# Configurar Django
sys.path.append('venv/Scripts')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import Negocio

def check_negocio_db():
    """Verificar si el negocio existe en la base de datos"""
    try:
        # Buscar el negocio
        negocio = Negocio.objects.get(
            empre='0301',
            rtm='114-03-23',
            expe='1151'
        )
        
        print(f"Negocio encontrado: {negocio}")
        print(f"ID: {negocio.id}")
        print(f"RTM: {negocio.rtm}")
        print(f"EXPE: {negocio.expe}")
        print(f"Nombre: {getattr(negocio, 'nombrenego', 'N/A')}")
        
    except Negocio.DoesNotExist:
        print("Negocio NO encontrado en la base de datos")
        
        # Buscar negocios similares
        print("\nBuscando negocios similares:")
        negocios_similares = Negocio.objects.filter(empre='0301')
        print(f"Total de negocios en empresa 0301: {negocios_similares.count()}")
        
        if negocios_similares.exists():
            print("Primeros 5 negocios:")
            for negocio in negocios_similares[:5]:
                print(f"  - RTM: {negocio.rtm}, EXPE: {negocio.expe}, ID: {negocio.id}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_negocio_db()



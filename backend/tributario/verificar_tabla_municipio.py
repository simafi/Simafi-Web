#!/usr/bin/env python
"""
Script para verificar la estructura de la tabla municipio
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.db import connection

def verificar_estructura_municipio():
    """Verificar estructura de la tabla municipio"""
    
    print("Verificando estructura de la tabla municipio...")
    
    try:
        with connection.cursor() as cursor:
            # Verificar estructura de la tabla
            cursor.execute("DESCRIBE mod_core_municipio")
            columns = cursor.fetchall()
            
            print("\n=== ESTRUCTURA DE LA TABLA mod_core_municipio ===")
            for column in columns:
                print(f"Campo: {column[0]}, Tipo: {column[1]}, Null: {column[2]}, Key: {column[3]}, Default: {column[4]}")
            print("=" * 60)
            
            # Verificar si existe el municipio 0301
            cursor.execute("SELECT * FROM mod_core_municipio WHERE codigo = '0301'")
            municipio = cursor.fetchone()
            
            if municipio:
                print(f"\nMunicipio 0301 encontrado: {municipio}")
            else:
                print("\nMunicipio 0301 no encontrado")
                
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == '__main__':
    verificar_estructura_municipio()


































#!/usr/bin/env python
"""
Script para crear datos de prueba necesarios para el funcionamiento del sistema
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.core.models import Municipio
from modules.usuarios.models import Usuario
import hashlib

def crear_datos_prueba():
    """Crear datos de prueba para el sistema"""
    
    print("Creando datos de prueba...")
    
    # Crear municipio de prueba
    municipio, created = Municipio.objects.get_or_create(
        codigo='001',
        defaults={
            'descripcion': 'Municipio de Prueba',
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ Municipio creado: {municipio.descripcion}")
    else:
        print(f"✓ Municipio existente: {municipio.descripcion}")
    
    # Crear usuario de prueba para catastro
    password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    
    usuario, created = Usuario.objects.get_or_create(
        usuario='catastro',
        empresa='001',
        defaults={
            'nombre': 'Usuario Catastro',
            'password': password_hash,
            'is_active': True,
            'municipio': municipio
        }
    )
    
    if created:
        print(f"✓ Usuario creado: {usuario.nombre} (catastro/admin123)")
    else:
        print(f"✓ Usuario existente: {usuario.nombre}")
    
    print("\nDatos de prueba creados exitosamente!")
    print("Puedes usar las siguientes credenciales para acceder al módulo de catastro:")
    print("Usuario: catastro")
    print("Contraseña: admin123")
    print("Municipio: Municipio de Prueba")

if __name__ == '__main__':
    crear_datos_prueba()

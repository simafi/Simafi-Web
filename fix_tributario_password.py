#!/usr/bin/env python
"""
Script para corregir la contraseña del usuario tributario
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
import hashlib

def fix_tributario_password():
    try:
        # Buscar el usuario tributario
        user = Usuario.objects.get(usuario='tributario', municipio_id=2)
        print(f"Usuario encontrado: {user.usuario}")
        print(f"Empresa: {user.empresa}")
        print(f"Municipio ID: {user.municipio_id}")
        
        # Generar el hash SHA256 correcto para 'admin123'
        password = 'admin123'
        correct_hash = hashlib.sha256(password.encode()).hexdigest()
        
        print(f"\nActualizando contraseña...")
        print(f"Hash SHA256 de '{password}': {correct_hash}")
        
        # Actualizar la contraseña
        user.password = correct_hash
        user.save()
        
        print("✅ Contraseña actualizada correctamente")
        
        # Verificar que funciona
        print("\nVerificando...")
        user.refresh_from_db()
        test_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user.password == test_hash:
            print("✅ Verificación exitosa: la contraseña ahora funciona")
            print(f"Hash en BD: {user.password}")
        else:
            print("❌ Error en la verificación")
            
    except Usuario.DoesNotExist:
        print("❌ Usuario 'tributario' no encontrado")
        print("Usuarios disponibles:")
        for u in Usuario.objects.all():
            print(f"  - {u.usuario} (empresa: {u.empresa}, municipio: {u.municipio_id})")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    fix_tributario_password()






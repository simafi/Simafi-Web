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

def fix_password():
    try:
        user = Usuario.objects.get(usuario='tributario', municipio_id=2)
        print(f"Usuario encontrado: {user.usuario}")
        
        # Generar el hash SHA256 correcto para admin123
        password = 'admin123'
        correct_hash = hashlib.sha256(password.encode()).hexdigest()
        
        print(f"Hash correcto para '{password}': {correct_hash}")
        
        # Actualizar la contraseña
        user.password = correct_hash
        user.save()
        
        print("✅ Contraseña actualizada correctamente")
        
        # Verificar que funciona
        test_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password == test_hash:
            print("✅ Verificación exitosa: la contraseña ahora funciona")
        else:
            print("❌ Error en la verificación")
            
    except Usuario.DoesNotExist:
        print("❌ Usuario no encontrado")

if __name__ == '__main__':
    fix_password()

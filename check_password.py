#!/usr/bin/env python
"""
Script para verificar la contraseña del usuario tributario
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
import hashlib

def check_password():
    try:
        user = Usuario.objects.get(usuario='tributario', municipio_id=2)
        print(f"Usuario: {user.usuario}")
        print(f"Empresa: {user.empresa}")
        print(f"Municipio: {user.municipio_id}")
        print(f"Password en BD: {user.password}")
        
        # Probar diferentes contraseñas
        passwords_to_test = ['admin123', 'admin', '123456', 'tributario', 'password']
        
        for pwd in passwords_to_test:
            hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()
            if user.password == hash_pwd:
                print(f"✅ CONTRASEÑA CORRECTA: {pwd}")
                return pwd
            else:
                print(f"❌ {pwd} -> {hash_pwd}")
        
        print("❌ Ninguna contraseña coincide")
        return None
        
    except Usuario.DoesNotExist:
        print("❌ Usuario no encontrado")
        return None

if __name__ == '__main__':
    check_password()






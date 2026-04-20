#!/usr/bin/env python
"""
Script para resetear todas las contraseñas a admin123
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
import hashlib

def reset_all_passwords():
    print("=== RESETEO DE CONTRASEÑAS ===")
    print("Estableciendo todas las contraseñas a: admin123")
    print()
    
    # Hash SHA256 de admin123
    password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    print(f"Hash SHA256 de admin123: {password_hash}")
    print()
    
    try:
        # Obtener todos los usuarios
        usuarios = Usuario.objects.all()
        print(f"Usuarios encontrados: {usuarios.count()}")
        print()
        
        for user in usuarios:
            print(f"Reseteando contraseña para:")
            print(f"  - Usuario: {user.usuario}")
            print(f"  - Empresa: {user.empresa}")
            print(f"  - Municipio: {user.municipio_id}")
            print(f"  - Nombre: {user.nombre}")
            
            # Actualizar contraseña
            user.password = password_hash
            user.save()
            
            print(f"  ✅ Contraseña actualizada")
            print()
        
        print("=== VERIFICACIÓN ===")
        print("Verificando que todas las contraseñas funcionan...")
        
        for user in usuarios:
            user.refresh_from_db()
            if user.password == password_hash:
                print(f"✅ {user.usuario} - Contraseña correcta")
            else:
                print(f"❌ {user.usuario} - Error en contraseña")
        
        print()
        print("=== CREDENCIALES DE ACCESO ===")
        print("Ahora puedes acceder con:")
        print()
        
        for user in usuarios:
            municipio_codigo = "0301" if user.municipio_id == 2 else "001"
            print(f"Usuario: {user.usuario}")
            print(f"Contraseña: admin123")
            print(f"Municipio: {municipio_codigo}")
            print(f"Módulo: {'Tributario' if user.usuario == 'tributario' else 'Catastro' if user.usuario == 'catastro' else 'Otros'}")
            print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    reset_all_passwords()






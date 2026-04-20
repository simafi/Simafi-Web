#!/usr/bin/env python
"""
Script directo para resetear contraseñas usando SQL
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.db import connection
import hashlib

def reset_passwords_direct():
    print("=== RESETEO DIRECTO DE CONTRASEÑAS ===")
    
    # Hash SHA256 de admin123
    password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    print(f"Hash SHA256 de admin123: {password_hash}")
    print()
    
    try:
        with connection.cursor() as cursor:
            # Actualizar todas las contraseñas
            cursor.execute("""
                UPDATE mod_usuarios_usuario 
                SET password = %s
            """, [password_hash])
            
            updated_count = cursor.rowcount
            print(f"✅ {updated_count} usuarios actualizados")
            
            # Verificar usuarios actualizados
            cursor.execute("""
                SELECT usuario, empresa, municipio_id, nombre 
                FROM mod_usuarios_usuario
                ORDER BY usuario
            """)
            
            users = cursor.fetchall()
            print(f"\n=== USUARIOS ACTUALIZADOS ===")
            for user in users:
                usuario, empresa, municipio_id, nombre = user
                municipio_codigo = "0301" if municipio_id == 2 else "001"
                print(f"Usuario: {usuario}")
                print(f"Empresa: {empresa}")
                print(f"Municipio: {municipio_codigo}")
                print(f"Nombre: {nombre}")
                print("-" * 40)
            
            print(f"\n=== CREDENCIALES DE ACCESO ===")
            print("Ahora puedes acceder con:")
            print("Usuario: tributario")
            print("Contraseña: admin123")
            print("Municipio: 0301")
            print("URL: http://127.0.0.1:8080/")
            print()
            print("Para Catastro:")
            print("Usuario: catastro")
            print("Contraseña: admin123")
            print("Municipio: 0301")
            print("URL: http://127.0.0.1:8080/catastro/")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    reset_passwords_direct()






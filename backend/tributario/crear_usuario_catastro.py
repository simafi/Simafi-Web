#!/usr/bin/env python
"""
Script para crear usuario catastro específico
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.db import connection
import hashlib

def crear_usuario_catastro():
    """Crear usuario catastro con contraseña admin123"""
    
    print("Creando usuario catastro...")
    
    # Hash de la contraseña
    password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    
    # Fecha actual para created_at y updated_at
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with connection.cursor() as cursor:
            # Verificar si el municipio existe
            cursor.execute("""
                SELECT id, descripcion FROM mod_core_municipio 
                WHERE codigo = '001' LIMIT 1
            """)
            municipio_result = cursor.fetchone()
            
            if not municipio_result:
                # Crear municipio si no existe
                cursor.execute("""
                    INSERT INTO mod_core_municipio 
                    (codigo, descripcion, is_active, created_at, updated_at) 
                    VALUES ('001', 'Municipio de Prueba', 1, %s, %s)
                """, (now, now))
                municipio_id = cursor.lastrowid
                print("✓ Municipio creado: Municipio de Prueba")
            else:
                municipio_id = municipio_result[0]
                print(f"✓ Municipio existente: {municipio_result[1]}")
            
            # Verificar si el usuario catastro existe
            cursor.execute("""
                SELECT id, nombre FROM mod_usuarios_usuario 
                WHERE usuario = 'catastro' AND empresa = '001' LIMIT 1
            """)
            usuario_result = cursor.fetchone()
            
            if not usuario_result:
                # Crear usuario catastro con todos los campos requeridos
                cursor.execute("""
                    INSERT INTO mod_usuarios_usuario 
                    (empresa, usuario, password, nombre, email, is_active, last_login, 
                     failed_login_attempts, locked_until, municipio_id, created_at, updated_at) 
                    VALUES ('001', 'catastro', %s, 'Usuario Catastro', NULL, 1, NULL, 0, NULL, %s, %s, %s)
                """, (password_hash, municipio_id, now, now))
                print("✓ Usuario creado: Usuario Catastro (catastro/admin123)")
            else:
                # Actualizar contraseña si el usuario existe
                cursor.execute("""
                    UPDATE mod_usuarios_usuario 
                    SET password = %s, nombre = 'Usuario Catastro', is_active = 1, updated_at = %s
                    WHERE usuario = 'catastro' AND empresa = '001'
                """, (password_hash, now))
                print(f"✓ Usuario actualizado: {usuario_result[1]} (catastro/admin123)")
            
            connection.commit()
            
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        return False
    
    print("\nUsuario catastro creado exitosamente!")
    print("Credenciales para acceder al módulo de catastro:")
    print("Usuario: catastro")
    print("Contraseña: admin123")
    print("Municipio: Municipio de Prueba")
    print("\nURL de acceso: http://127.0.0.1:8080/catastro/login/")
    
    return True

if __name__ == '__main__':
    crear_usuario_catastro()

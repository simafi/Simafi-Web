#!/usr/bin/env python
"""
Script para crear usuarios de prueba para el sistema modular
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

def crear_usuarios_sistema_modular():
    """Crear usuarios para todos los módulos del sistema"""
    
    print("=== CREANDO USUARIOS PARA EL SISTEMA MODULAR ===")
    
    # Hash de la contraseña
    password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    
    # Fecha actual
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Usuarios a crear
    usuarios = [
        {
            'usuario': 'admin',
            'empresa': '001',
            'nombre': 'Administrador General',
            'empresa': '001'
        },
        {
            'usuario': 'catastro',
            'empresa': '0301',
            'nombre': 'Usuario Catastro',
            'empresa': '0301'
        },
        {
            'usuario': 'tributario',
            'empresa': '0301',
            'nombre': 'Usuario Tributario',
            'empresa': '0301'
        },
        {
            'usuario': 'administrativo',
            'empresa': '0301',
            'nombre': 'Usuario Administrativo',
            'empresa': '0301'
        }
    ]
    
    try:
        with connection.cursor() as cursor:
            for user_data in usuarios:
                # Obtener el ID del municipio
                cursor.execute("""
                    SELECT id FROM mod_core_municipio 
                    WHERE codigo = %s
                """, [user_data['empresa']])
                
                municipio_result = cursor.fetchone()
                if not municipio_result:
                    print(f"❌ Municipio {user_data['empresa']} no encontrado")
                    continue
                
                municipio_id = municipio_result[0]
                
                # Verificar si el usuario ya existe
                cursor.execute("""
                    SELECT id FROM mod_usuarios_usuario 
                    WHERE usuario = %s AND empresa = %s
                """, [user_data['usuario'], user_data['empresa']])
                
                existing_user = cursor.fetchone()
                
                if existing_user:
                    # Actualizar usuario existente
                    cursor.execute("""
                        UPDATE mod_usuarios_usuario 
                        SET nombre = %s, municipio_id = %s, password = %s, updated_at = %s
                        WHERE usuario = %s AND empresa = %s
                    """, [
                        user_data['nombre'],
                        municipio_id,
                        password_hash,
                        now,
                        user_data['usuario'],
                        user_data['empresa']
                    ])
                    print(f"✅ Usuario {user_data['usuario']} actualizado")
                else:
                    # Crear nuevo usuario con todos los campos requeridos
                    cursor.execute("""
                        INSERT INTO mod_usuarios_usuario 
                        (empresa, usuario, nombre, password, municipio_id, is_active, 
                         failed_login_attempts, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        user_data['empresa'],
                        user_data['usuario'],
                        user_data['nombre'],
                        password_hash,
                        municipio_id,
                        1,
                        0,  # failed_login_attempts
                        now,
                        now
                    ])
                    print(f"✅ Usuario {user_data['usuario']} creado")
        
        print("\n=== RESUMEN DE USUARIOS ===")
        print("Todos los usuarios tienen la contraseña: admin123")
        print("\nCredenciales de acceso:")
        print("1. Administrador General:")
        print("   - Usuario: admin")
        print("   - Municipio: 001")
        print("   - Contraseña: admin123")
        print("\n2. Usuario Catastro:")
        print("   - Usuario: catastro")
        print("   - Municipio: 0301")
        print("   - Contraseña: admin123")
        print("\n3. Usuario Tributario:")
        print("   - Usuario: tributario")
        print("   - Municipio: 0301")
        print("   - Contraseña: admin123")
        print("\n4. Usuario Administrativo:")
        print("   - Usuario: administrativo")
        print("   - Municipio: 0301")
        print("   - Contraseña: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    crear_usuarios_sistema_modular()

#!/usr/bin/env python
"""
Script para crear usuario catastro con empresa 0301
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

def crear_usuario_catastro_0301():
    """Crear usuario catastro con empresa 0301"""
    
    print("Creando usuario catastro con empresa 0301...")
    
    # Hash de la contraseña
    password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    
    # Fecha actual
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with connection.cursor() as cursor:
            # Obtener el ID del municipio 0301
            cursor.execute("SELECT id FROM mod_core_municipio WHERE codigo = '0301'")
            municipio_result = cursor.fetchone()
            
            if not municipio_result:
                print("❌ Municipio 0301 no encontrado")
                return False
            
            municipio_id = municipio_result[0]
            print(f"✓ Municipio 0301 encontrado con ID: {municipio_id}")
            
            # Verificar si ya existe el usuario
            cursor.execute("SELECT id FROM mod_usuarios_usuario WHERE usuario = 'catastro' AND empresa = '0301'")
            usuario_existente = cursor.fetchone()
            
            if usuario_existente:
                print("✓ Usuario catastro con empresa 0301 ya existe")
                # Actualizar contraseña
                cursor.execute("""
                    UPDATE mod_usuarios_usuario 
                    SET password = %s, nombre = 'Usuario Catastro', is_active = 1, municipio_id = %s, updated_at = %s
                    WHERE usuario = 'catastro' AND empresa = '0301'
                """, (password_hash, municipio_id, now))
                print("✓ Contraseña actualizada")
            else:
                # Crear nuevo usuario
                cursor.execute("""
                    INSERT INTO mod_usuarios_usuario 
                    (empresa, usuario, password, nombre, email, is_active, last_login, 
                     failed_login_attempts, locked_until, municipio_id, created_at, updated_at) 
                    VALUES ('0301', 'catastro', %s, 'Usuario Catastro', NULL, 1, NULL, 0, NULL, %s, %s, %s)
                """, (password_hash, municipio_id, now, now))
                print("✓ Usuario catastro creado con empresa 0301")
            
            connection.commit()
            
            # Verificar que se creó correctamente
            cursor.execute("""
                SELECT u.id, u.empresa, u.usuario, u.nombre, m.codigo, m.descripcion 
                FROM mod_usuarios_usuario u 
                INNER JOIN mod_core_municipio m ON u.municipio_id = m.id 
                WHERE u.usuario = 'catastro' AND u.empresa = '0301'
            """)
            usuario_verificado = cursor.fetchone()
            
            if usuario_verificado:
                print(f"\n✅ USUARIO CREADO EXITOSAMENTE:")
                print(f"   - ID: {usuario_verificado[0]}")
                print(f"   - Empresa: {usuario_verificado[1]}")
                print(f"   - Usuario: {usuario_verificado[2]}")
                print(f"   - Nombre: {usuario_verificado[3]}")
                print(f"   - Municipio: {usuario_verificado[4]} - {usuario_verificado[5]}")
                print(f"\nCredenciales de acceso:")
                print(f"   - Usuario: catastro")
                print(f"   - Contraseña: admin123")
                print(f"   - Municipio: Municipio 0301")
                print(f"   - URL: http://127.0.0.1:8080/catastro/login/")
                return True
            else:
                print("❌ Error: Usuario no se creó correctamente")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        return False

if __name__ == '__main__':
    crear_usuario_catastro_0301()


































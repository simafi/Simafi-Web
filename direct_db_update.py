#!/usr/bin/env python
"""
Script para actualizar directamente la contraseña en la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.db import connection

def update_password():
    # Hash SHA256 de 'admin123'
    correct_hash = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE mod_usuarios_usuario 
                SET password = %s 
                WHERE usuario = 'tributario' AND municipio_id = 2
            """, [correct_hash])
            
            if cursor.rowcount > 0:
                print("✅ Contraseña actualizada correctamente")
                print(f"Hash aplicado: {correct_hash}")
            else:
                print("❌ No se encontró el usuario para actualizar")
                
    except Exception as e:
        print(f"❌ Error al actualizar: {e}")

if __name__ == '__main__':
    update_password()






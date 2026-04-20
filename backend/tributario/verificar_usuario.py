#!/usr/bin/env python
"""
Script para verificar información del usuario catastro
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.db import connection

def verificar_usuario_catastro():
    """Verificar información del usuario catastro"""
    
    print("Verificando usuario catastro...")
    
    try:
        with connection.cursor() as cursor:
            # Consultar información del usuario catastro
            cursor.execute("""
                SELECT u.usuario, u.empresa, u.nombre, m.codigo, m.descripcion 
                FROM mod_usuarios_usuario u 
                LEFT JOIN mod_core_municipio m ON u.municipio_id = m.id 
                WHERE u.usuario = 'catastro'
            """)
            result = cursor.fetchone()
            
            if result:
                print(f"\n=== INFORMACIÓN DEL USUARIO CATASTRO ===")
                print(f"Usuario: {result[0]}")
                print(f"Código de Empresa: {result[1]}")
                print(f"Nombre: {result[2]}")
                print(f"Código de Municipio: {result[3]}")
                print(f"Descripción del Municipio: {result[4]}")
                print("=" * 45)
                
                # Verificar si el usuario está activo
                cursor.execute("""
                    SELECT is_active FROM mod_usuarios_usuario 
                    WHERE usuario = 'catastro'
                """)
                is_active_result = cursor.fetchone()
                if is_active_result:
                    print(f"Usuario Activo: {'Sí' if is_active_result[0] else 'No'}")
                
            else:
                print("Usuario catastro no encontrado")
                
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == '__main__':
    verificar_usuario_catastro()

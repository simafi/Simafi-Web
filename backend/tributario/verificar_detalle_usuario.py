#!/usr/bin/env python
"""
Script para verificar información detallada del usuario catastro
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.db import connection

def verificar_detalle_usuario():
    """Verificar información detallada del usuario catastro"""
    
    print("Verificando información detallada del usuario catastro...")
    
    try:
        with connection.cursor() as cursor:
            # Verificar todos los usuarios catastro
            cursor.execute("""
                SELECT id, empresa, usuario, nombre, municipio_id 
                FROM mod_usuarios_usuario 
                WHERE usuario = 'catastro'
            """)
            usuarios = cursor.fetchall()
            
            print(f"\n=== USUARIOS CATASTRO ENCONTRADOS: {len(usuarios)} ===")
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Empresa: {usuario[1]}, Usuario: {usuario[2]}, Nombre: {usuario[3]}, Municipio ID: {usuario[4]}")
            
            # Verificar municipios
            cursor.execute("""
                SELECT id, codigo, descripcion 
                FROM mod_core_municipio 
                WHERE codigo IN ('001', '0301')
            """)
            municipios = cursor.fetchall()
            
            print(f"\n=== MUNICIPIOS DISPONIBLES ===")
            for municipio in municipios:
                print(f"ID: {municipio[0]}, Código: {municipio[1]}, Descripción: {municipio[2]}")
            
            # Verificar la relación específica
            cursor.execute("""
                SELECT u.usuario, u.empresa, u.nombre, m.codigo, m.descripcion 
                FROM mod_usuarios_usuario u 
                INNER JOIN mod_core_municipio m ON u.municipio_id = m.id 
                WHERE u.usuario = 'catastro' AND u.empresa = '0301'
            """)
            relacion = cursor.fetchone()
            
            if relacion:
                print(f"\n=== RELACIÓN USUARIO-MUNICIPIO ===")
                print(f"Usuario: {relacion[0]}")
                print(f"Empresa: {relacion[1]}")
                print(f"Nombre: {relacion[2]}")
                print(f"Código Municipio: {relacion[3]}")
                print(f"Descripción Municipio: {relacion[4]}")
            else:
                print("\n❌ No se encontró relación entre usuario catastro y municipio 0301")
                
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == '__main__':
    verificar_detalle_usuario()


































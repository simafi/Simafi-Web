#!/usr/bin/env python
"""
Script de diagnóstico para el login de catastro
"""
import os
import sys
import django
import hashlib

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from django.db import connection
from modules.usuarios.models import Usuario
from modules.core.models import Municipio

def diagnostico_login_catastro():
    """Diagnóstico completo del login de catastro"""
    
    print("=== DIAGNÓSTICO DEL LOGIN DE CATASTRO ===")
    
    try:
        # 1. Verificar municipios disponibles
        print("\n1. MUNICIPIOS DISPONIBLES:")
        municipios = Municipio.objects.all()
        for municipio in municipios:
            print(f"   - Código: {municipio.codigo}, Descripción: {municipio.descripcion}")
        
        # 2. Verificar usuarios catastro
        print("\n2. USUARIOS CATASTRO:")
        usuarios = Usuario.objects.filter(usuario='catastro')
        for usuario in usuarios:
            print(f"   - ID: {usuario.id}")
            print(f"   - Usuario: {usuario.usuario}")
            print(f"   - Empresa: {usuario.empresa}")
            print(f"   - Nombre: {usuario.nombre}")
            print(f"   - Activo: {usuario.is_active}")
            print(f"   - Municipio ID: {usuario.municipio_id}")
            print(f"   - Contraseña (primeros 20 chars): {usuario.password[:20]}...")
            
            # Verificar municipio asociado
            if usuario.municipio_id:
                try:
                    municipio = Municipio.objects.get(id=usuario.municipio_id)
                    print(f"   - Municipio Asociado: {municipio.codigo} - {municipio.descripcion}")
                except Municipio.DoesNotExist:
                    print(f"   - ❌ Municipio ID {usuario.municipio_id} no existe")
            else:
                print(f"   - ❌ No tiene municipio asociado")
        
        # 3. Verificar contraseña específica
        print("\n3. VERIFICACIÓN DE CONTRASEÑA:")
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        print(f"   - Hash esperado para 'admin123': {password_hash}")
        
        # 4. Simular búsqueda de usuario
        print("\n4. SIMULACIÓN DE BÚSQUEDA:")
        
        # Buscar usuario con empresa 0301
        try:
            user_0301 = Usuario.objects.get(usuario='catastro', empresa='0301')
            print(f"   - Usuario encontrado con empresa 0301: {user_0301.nombre}")
            print(f"   - Contraseña almacenada: {user_0301.password}")
            print(f"   - ¿Coincide con hash esperado?: {user_0301.password == password_hash}")
            
            # Verificar municipio
            if user_0301.municipio_id:
                try:
                    municipio = Municipio.objects.get(id=user_0301.municipio_id)
                    print(f"   - Municipio asociado: {municipio.codigo} - {municipio.descripcion}")
                except Municipio.DoesNotExist:
                    print(f"   - ❌ Municipio no encontrado")
            else:
                print(f"   - ❌ No tiene municipio asociado")
                
        except Usuario.DoesNotExist:
            print(f"   - ❌ Usuario catastro con empresa 0301 no encontrado")
        
        # 5. Verificar configuración de URLs
        print("\n5. VERIFICACIÓN DE URLS:")
        print(f"   - URL de login esperada: http://127.0.0.1:8080/catastro/login/")
        
        # 6. Verificar que el servidor esté ejecutándose
        print("\n6. ESTADO DEL SERVIDOR:")
        print(f"   - Verificar que el servidor esté ejecutándose en puerto 8080")
        print(f"   - Comando: python manage.py runserver 8080")
        
    except Exception as e:
        print(f"Error en diagnóstico: {e}")
    
    print("\n=== FIN DEL DIAGNÓSTICO ===")

if __name__ == '__main__':
    diagnostico_login_catastro()


































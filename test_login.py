#!/usr/bin/env python
"""
Script de test para verificar el login del sistema modular
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from catastro.usuarios.models import Usuario
from catastro.core.models import Municipio

def test_login():
    """Test del sistema de login"""
    print("=== TEST DE LOGIN DEL SISTEMA MODULAR ===")
    print()
    
    # Verificar que hay municipios
    municipios = Municipio.objects.all()
    print(f"Municipios disponibles: {municipios.count()}")
    for municipio in municipios[:5]:  # Mostrar solo los primeros 5
        print(f"  - {municipio.codigo}: {municipio.descripcion}")
    print()
    
    # Verificar que hay usuarios
    usuarios = Usuario.objects.all()
    print(f"Usuarios disponibles: {usuarios.count()}")
    for usuario in usuarios[:5]:  # Mostrar solo los primeros 5
        print(f"  - Usuario: {usuario.usuario}, Empresa: {usuario.empresa}, Nombre: {usuario.nombre}")
    print()
    
    # Test de autenticación con usuario común
    test_users = [
        {'usuario': 'admin', 'empresa': '0001'},
        {'usuario': 'test', 'empresa': '0001'},
        {'usuario': 'user', 'empresa': '0001'},
    ]
    
    for test_user in test_users:
        print(f"Probando usuario: {test_user['usuario']} con empresa: {test_user['empresa']}")
        try:
            user = Usuario.objects.get(
                usuario=test_user['usuario'],
                empresa=test_user['empresa']
            )
            print(f"  ✅ Usuario encontrado: {user.nombre}")
            print(f"  - Password hash: {user.password[:20]}...")
            
            # Test de verificación de contraseña
            from django.contrib.auth.hashers import check_password
            test_passwords = ['admin', '123456', 'password', 'test', 'user']
            
            for pwd in test_passwords:
                if check_password(pwd, user.password):
                    print(f"  ✅ Contraseña correcta: '{pwd}'")
                    break
            else:
                print(f"  ❌ Ninguna contraseña de prueba funcionó")
                
        except Usuario.DoesNotExist:
            print(f"  ❌ Usuario no encontrado")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()

if __name__ == "__main__":
    test_login()

































































#!/usr/bin/env python
"""
Script para corregir la contraseña del usuario tributario a admin123
"""

import os
import sys
import django
from django.contrib.auth.hashers import make_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario

def corregir_password_tributario():
    """Corregir la contraseña del usuario tributario"""
    print("🔧 CORRIGIENDO CONTRASEÑA DEL USUARIO TRIBUTARIO")
    print("=" * 60)
    
    try:
        # Buscar usuario tributario
        usuario = Usuario.objects.get(usuario='tributario')
        print(f"✅ Usuario encontrado: {usuario.usuario}")
        print(f"✅ Empresa: {usuario.empresa}")
        print(f"✅ Municipio ID: {usuario.municipio_id}")
        print(f"✅ Nombre: {usuario.nombre}")
        
        # Mostrar contraseña actual
        print(f"\n🔍 Contraseña actual: {usuario.password[:50]}...")
        
        # Establecer nueva contraseña admin123
        print("\n🔧 Estableciendo nueva contraseña 'admin123'...")
        usuario.password = make_password('admin123')
        usuario.save()
        
        print("✅ Contraseña actualizada exitosamente")
        print(f"✅ Nueva contraseña hash: {usuario.password[:50]}...")
        
        # Verificar que la contraseña funciona
        print("\n🔍 Verificando nueva contraseña...")
        if usuario.check_password('admin123'):
            print("✅ Verificación exitosa - La contraseña 'admin123' funciona")
        else:
            print("❌ Error en la verificación de la contraseña")
            return False
        
        print("\n🎉 CONTRASEÑA CORREGIDA EXITOSAMENTE")
        print("✅ Ahora puedes acceder con:")
        print("   Usuario: tributario")
        print("   Contraseña: admin123")
        print("   Municipio: 0301")
        print("   URL: http://127.0.0.1:8080/login/")
        
        return True
        
    except Usuario.DoesNotExist:
        print("❌ Usuario 'tributario' no encontrado")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_todos_los_usuarios():
    """Verificar todos los usuarios y sus contraseñas"""
    print("\n" + "=" * 60)
    print("📋 VERIFICACIÓN DE TODOS LOS USUARIOS")
    print("=" * 60)
    
    try:
        usuarios = Usuario.objects.all()
        print(f"Total de usuarios: {usuarios.count()}\n")
        
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i:2d}. Usuario: {usuario.usuario}")
            print(f"    Empresa: {usuario.empresa}")
            print(f"    Municipio ID: {usuario.municipio_id}")
            print(f"    Nombre: {usuario.nombre}")
            print(f"    Activo: {usuario.is_active}")
            print(f"    Password Hash: {usuario.password[:30]}...")
            
            # Verificar si la contraseña es admin123
            if usuario.check_password('admin123'):
                print("    ✅ Contraseña 'admin123' VERIFICADA")
            else:
                print("    ❌ Contraseña 'admin123' NO funciona")
            print()
            
    except Exception as e:
        print(f"Error al verificar usuarios: {str(e)}")

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN DE CONTRASEÑA - SISTEMA SIMAFIWEB")
    print("Estableciendo contraseña 'admin123' para usuario 'tributario'")
    print("=" * 60)
    
    try:
        # Corregir contraseña
        exito = corregir_password_tributario()
        
        if exito:
            # Verificar todos los usuarios
            verificar_todos_los_usuarios()
            
            print("\n✅ CORRECCIÓN COMPLETADA EXITOSAMENTE")
            return 0
        else:
            print("\n❌ CORRECCIÓN FALLÓ")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

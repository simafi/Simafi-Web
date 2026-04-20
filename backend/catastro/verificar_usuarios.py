#!/usr/bin/env python
"""
Script para verificar usuarios disponibles en el módulo catastro
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catastro.settings')
django.setup()

from usuarios.models import Usuario
from core.models import Municipio

def mostrar_usuarios_disponibles():
    """Muestra los usuarios disponibles para el login"""
    print("=" * 60)
    print("    USUARIOS DISPONIBLES PARA MÓDULO CATASTRO")
    print("=" * 60)
    print()
    
    # Obtener todos los usuarios
    usuarios = Usuario.objects.all().order_by('empresa', 'usuario')
    
    if not usuarios.exists():
        print("❌ No hay usuarios registrados en la tabla 'usuarios'")
        print()
        print("Para crear un usuario de prueba, ejecuta:")
        print("python crear_usuario_prueba.py")
        return
    
    print(f"✅ Se encontraron {usuarios.count()} usuarios:")
    print()
    
    # Agrupar por empresa/municipio
    empresas = {}
    for usuario in usuarios:
        empresa = usuario.empresa or 'SIN_EMPRESA'
        if empresa not in empresas:
            empresas[empresa] = []
        empresas[empresa].append(usuario)
    
    for empresa, usuarios_empresa in empresas.items():
        print(f"🏢 EMPRESA/MUNICIPIO: {empresa}")
        print("-" * 40)
        
        for usuario in usuarios_empresa:
            nombre_completo = usuario.get_full_name()
            print(f"👤 Usuario: {usuario.usuario}")
            print(f"   Nombre: {nombre_completo}")
            print(f"   Cargo: {usuario.cargo or 'No especificado'}")
            print(f"   Celular: {usuario.celular or 'No especificado'}")
            
            # Verificar si la contraseña está hasheada
            if usuario.password.startswith('pbkdf2_sha256'):
                print(f"   Contraseña: [HASHEADA - Usar contraseña original]")
            else:
                print(f"   Contraseña: {usuario.password}")
            
            print()
    
    print("=" * 60)
    print("📋 INSTRUCCIONES PARA EL LOGIN:")
    print("=" * 60)
    print("1. Ve a: http://127.0.0.1:8080/")
    print("2. Selecciona el municipio en el combobox")
    print("3. Ingresa el usuario y contraseña de la lista anterior")
    print("4. Si la contraseña aparece como [HASHEADA], usa la contraseña original")
    print()
    print("💡 CONSEJOS:")
    print("- El campo 'empresa' debe coincidir con el código del municipio seleccionado")
    print("- Si no recuerdas la contraseña, puedes crear un nuevo usuario")
    print("- Para crear un usuario de prueba: python crear_usuario_prueba.py")

def mostrar_municipios_disponibles():
    """Muestra los municipios disponibles"""
    print("=" * 60)
    print("    MUNICIPIOS DISPONIBLES")
    print("=" * 60)
    print()
    
    municipios = Municipio.objects.all().order_by('codigo')
    
    if not municipios.exists():
        print("❌ No hay municipios registrados en la tabla 'municipio'")
        return
    
    print(f"✅ Se encontraron {municipios.count()} municipios:")
    print()
    
    for municipio in municipios:
        print(f"🏛️  {municipio.codigo} - {municipio.descripcion}")
    
    print()

if __name__ == '__main__':
    try:
        mostrar_municipios_disponibles()
        print()
        mostrar_usuarios_disponibles()
    except Exception as e:
        print(f"❌ Error al verificar usuarios: {str(e)}")
        print("Asegúrate de que el servidor de base de datos esté ejecutándose")









































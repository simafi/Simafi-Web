#!/usr/bin/env python
"""
Script para crear un usuario de prueba para el módulo catastro
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catastro.settings')
django.setup()

from usuarios.models import Usuario
from core.models import Municipio

def crear_usuario_prueba():
    """Crea un usuario de prueba para el módulo catastro"""
    print("=" * 60)
    print("    CREANDO USUARIO DE PRUEBA PARA CATASTRO")
    print("=" * 60)
    print()
    
    # Obtener el primer municipio disponible
    try:
        municipio = Municipio.objects.first()
        if not municipio:
            print("❌ No hay municipios disponibles. Crea primero un municipio.")
            return
        
        print(f"🏛️  Municipio seleccionado: {municipio.codigo} - {municipio.descripcion}")
        print()
        
        # Credenciales del usuario de prueba
        usuario_prueba = {
            'empresa': municipio.codigo,
            'usuario': 'catastro',
            'password': 'catastro123',
            'nombre': 'Usuario',
            'apellidos': 'Catastro',
            'cargo': 'Administrador Catastro',
            'celular': '9999-9999'
        }
        
        # Verificar si el usuario ya existe
        usuario_existente = Usuario.objects.filter(
            empresa=usuario_prueba['empresa'],
            usuario=usuario_prueba['usuario']
        ).first()
        
        if usuario_existente:
            print(f"⚠️  El usuario '{usuario_prueba['usuario']}' ya existe para el municipio {usuario_prueba['empresa']}")
            print("Actualizando información...")
            
            # Actualizar información
            usuario_existente.nombre = usuario_prueba['nombre']
            usuario_existente.apellidos = usuario_prueba['apellidos']
            usuario_existente.cargo = usuario_prueba['cargo']
            usuario_existente.celular = usuario_prueba['celular']
            usuario_existente.password = usuario_prueba['password']  # Se hasheará automáticamente
            usuario_existente.save()
            
            print("✅ Usuario actualizado exitosamente")
        else:
            # Crear nuevo usuario
            nuevo_usuario = Usuario.objects.create(
                empresa=usuario_prueba['empresa'],
                usuario=usuario_prueba['usuario'],
                password=usuario_prueba['password'],  # Se hasheará automáticamente
                nombre=usuario_prueba['nombre'],
                apellidos=usuario_prueba['apellidos'],
                cargo=usuario_prueba['cargo'],
                celular=usuario_prueba['celular']
            )
            
            print("✅ Usuario creado exitosamente")
        
        print()
        print("=" * 60)
        print("📋 CREDENCIALES DE ACCESO:")
        print("=" * 60)
        print(f"🌐 URL: http://127.0.0.1:8080/")
        print(f"🏛️  Municipio: {municipio.codigo} - {municipio.descripcion}")
        print(f"👤 Usuario: {usuario_prueba['usuario']}")
        print(f"🔑 Contraseña: {usuario_prueba['password']}")
        print()
        print("💡 INSTRUCCIONES:")
        print("1. Ve a http://127.0.0.1:8080/")
        print("2. Selecciona el municipio en el combobox")
        print("3. Ingresa las credenciales mostradas arriba")
        print("4. ¡Listo! Ya puedes acceder al módulo catastro")
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {str(e)}")
        print("Asegúrate de que el servidor de base de datos esté ejecutándose")

if __name__ == '__main__':
    crear_usuario_prueba()









































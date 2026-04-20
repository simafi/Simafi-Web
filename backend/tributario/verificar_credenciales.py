#!/usr/bin/env python
"""
Script para verificar las credenciales del usuario tributario
"""

import os
import sys
import django
import hashlib

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
from modules.core.models import Municipio

def main():
    print("🔍 VERIFICACIÓN DE CREDENCIALES - SISTEMA SIMAFIWEB")
    print("=" * 60)
    
    try:
        # 1. Verificar conexión
        print("1. Verificando conexión a base de datos...")
        total_usuarios = Usuario.objects.count()
        total_municipios = Municipio.objects.count()
        print(f"   ✅ Usuarios en BD: {total_usuarios}")
        print(f"   ✅ Municipios en BD: {total_municipios}")
        
        # 2. Buscar usuario tributario
        print("\n2. Buscando usuario 'tributario'...")
        try:
            usuario = Usuario.objects.get(usuario='tributario')
            print(f"   ✅ Usuario encontrado: {usuario.usuario}")
            print(f"   ✅ Empresa: {usuario.empresa}")
            print(f"   ✅ Municipio ID: {usuario.municipio_id}")
            print(f"   ✅ Nombre: {usuario.nombre}")
            print(f"   ✅ Activo: {usuario.is_active}")
            print(f"   ✅ Password Hash: {usuario.password[:30]}...")
        except Usuario.DoesNotExist:
            print("   ❌ Usuario 'tributario' NO encontrado")
            return False
        
        # 3. Buscar municipio 0301
        print("\n3. Buscando municipio '0301'...")
        try:
            municipio = Municipio.objects.get(codigo='0301')
            print(f"   ✅ Municipio encontrado: {municipio.descripcion}")
            print(f"   ✅ Código: {municipio.codigo}")
            print(f"   ✅ ID: {municipio.id}")
        except Municipio.DoesNotExist:
            print("   ❌ Municipio '0301' NO encontrado")
            print("   📋 Municipios disponibles:")
            for m in Municipio.objects.all():
                print(f"      - Código: {m.codigo}, Descripción: {m.descripcion}, ID: {m.id}")
            return False
        
        # 4. Verificar contraseña admin123
        print("\n4. Verificando contraseña 'admin123'...")
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        print(f"   🔍 Hash SHA256 de 'admin123': {password_hash}")
        print(f"   🔍 Hash en BD: {usuario.password}")
        
        if usuario.password == password_hash:
            print("   ✅ Contraseña 'admin123' VERIFICADA")
            password_correcta = True
        else:
            print("   ❌ Contraseña 'admin123' NO coincide")
            password_correcta = False
        
        # 5. Verificar asociación usuario-municipio
        print("\n5. Verificando asociación usuario-municipio...")
        if usuario.municipio_id == municipio.id:
            print("   ✅ Usuario asociado al municipio correcto")
            municipio_correcto = True
        else:
            print(f"   ❌ Usuario asociado a municipio {usuario.municipio_id}, esperado {municipio.id}")
            municipio_correcto = False
        
        # 6. Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE VERIFICACIÓN")
        print("=" * 60)
        
        resultados = [
            ("Conexión BD", True),
            ("Usuario tributario", True),
            ("Municipio 0301", True),
            ("Contraseña admin123", password_correcta),
            ("Asociación usuario-municipio", municipio_correcto)
        ]
        
        for test, resultado in resultados:
            status = "✅ ÉXITO" if resultado else "❌ FALLO"
            print(f"{test:30s}: {status}")
        
        todos_correctos = all(resultado for _, resultado in resultados)
        
        if todos_correctos:
            print("\n🎉 ¡TODAS LAS CREDENCIALES ESTÁN CORRECTAS!")
            print("✅ El usuario puede acceder al sistema con:")
            print("   Usuario: tributario")
            print("   Contraseña: admin123")
            print("   Municipio: 0301")
            print("   URL: http://127.0.0.1:8080/login/")
        else:
            print("\n⚠️  ALGUNAS CREDENCIALES TIENEN PROBLEMAS")
            print("❌ Revisar los elementos marcados como FALLO")
        
        # 7. Mostrar todos los usuarios
        print("\n" + "=" * 60)
        print("📋 TODOS LOS USUARIOS EN EL SISTEMA")
        print("=" * 60)
        
        usuarios = Usuario.objects.all()
        for i, u in enumerate(usuarios, 1):
            municipio_codigo = u.municipio.codigo if u.municipio else "Sin municipio"
            municipio_desc = u.municipio.descripcion if u.municipio else "N/A"
            
            print(f"{i:2d}. Usuario: {u.usuario}")
            print(f"    Empresa: {u.empresa}")
            print(f"    Municipio: {municipio_codigo} ({municipio_desc})")
            print(f"    ID Municipio: {u.municipio_id}")
            print(f"    Nombre: {u.nombre}")
            print(f"    Activo: {u.is_active}")
            print()
        
        # 8. Mostrar todos los municipios
        print("📋 TODOS LOS MUNICIPIOS EN EL SISTEMA")
        print("=" * 60)
        
        municipios = Municipio.objects.all()
        for i, m in enumerate(municipios, 1):
            print(f"{i:2d}. Código: {m.codigo}")
            print(f"    Descripción: {m.descripcion}")
            print(f"    ID: {m.id}")
            print()
        
        return todos_correctos
        
    except Exception as e:
        print(f"\n💥 Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    exito = main()
    if exito:
        print("\n✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
        sys.exit(0)
    else:
        print("\n❌ VERIFICACIÓN FALLÓ - REVISAR CREDENCIALES")
        sys.exit(1)

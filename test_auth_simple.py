#!/usr/bin/env python
"""
Test simple de autenticación - Verificar credenciales en base de datos
"""

import os
import sys
import django
import hashlib

# Cambiar al directorio correcto
os.chdir(r'C:\simafiweb\venv\Scripts\tributario')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
from modules.core.models import Municipio

def test_credenciales_tributario():
    """Test de las credenciales específicas del usuario tributario"""
    print("🔍 VERIFICANDO CREDENCIALES DEL USUARIO TRIBUTARIO")
    print("=" * 60)
    
    try:
        # 1. Verificar conexión a base de datos
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
        
        # 3. Verificar municipio 0301
        print("\n3. Verificando municipio 0301...")
        try:
            municipio = Municipio.objects.get(codigo='0301')
            print(f"   ✅ Municipio encontrado: {municipio.nombre}")
            print(f"   ✅ Código: {municipio.codigo}")
            print(f"   ✅ ID: {municipio.id}")
        except Municipio.DoesNotExist:
            print("   ❌ Municipio '0301' NO encontrado")
            # Mostrar municipios disponibles
            print("   📋 Municipios disponibles:")
            for m in Municipio.objects.all():
                print(f"      - Código: {m.codigo}, Nombre: {m.nombre}, ID: {m.id}")
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
        
        # 5. Verificar que el usuario pertenece al municipio correcto
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
        
        return todos_correctos
        
    except Exception as e:
        print(f"\n💥 Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def mostrar_todos_los_usuarios():
    """Mostrar todos los usuarios en el sistema"""
    print("\n" + "=" * 60)
    print("📋 TODOS LOS USUARIOS EN EL SISTEMA")
    print("=" * 60)
    
    try:
        usuarios = Usuario.objects.all()
        print(f"Total de usuarios: {usuarios.count()}\n")
        
        for i, usuario in enumerate(usuarios, 1):
            municipio_codigo = usuario.municipio.codigo if usuario.municipio else "Sin municipio"
            municipio_nombre = usuario.municipio.nombre if usuario.municipio else "N/A"
            
            print(f"{i:2d}. Usuario: {usuario.usuario}")
            print(f"    Empresa: {usuario.empresa}")
            print(f"    Municipio: {municipio_codigo} ({municipio_nombre})")
            print(f"    ID Municipio: {usuario.municipio_id}")
            print(f"    Nombre: {usuario.nombre}")
            print(f"    Activo: {usuario.is_active}")
            print(f"    Password Hash: {usuario.password[:30]}...")
            print()
            
    except Exception as e:
        print(f"Error al obtener usuarios: {str(e)}")

def mostrar_todos_los_municipios():
    """Mostrar todos los municipios en el sistema"""
    print("\n" + "=" * 60)
    print("📋 TODOS LOS MUNICIPIOS EN EL SISTEMA")
    print("=" * 60)
    
    try:
        municipios = Municipio.objects.all()
        print(f"Total de municipios: {municipios.count()}\n")
        
        for i, municipio in enumerate(municipios, 1):
            print(f"{i:2d}. Código: {municipio.codigo}")
            print(f"    Nombre: {municipio.nombre}")
            print(f"    ID: {municipio.id}")
            print()
            
    except Exception as e:
        print(f"Error al obtener municipios: {str(e)}")

def main():
    """Función principal"""
    print("🧪 TEST DE AUTENTICACIÓN - SISTEMA SIMAFIWEB")
    print("Verificando credenciales: tributario / admin123 / municipio 0301")
    print("=" * 60)
    
    try:
        # Ejecutar test principal
        exito = test_credenciales_tributario()
        
        # Mostrar información adicional
        mostrar_todos_los_usuarios()
        mostrar_todos_los_municipios()
        
        if exito:
            print("\n✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
            return 0
        else:
            print("\n❌ VERIFICACIÓN FALLÓ - REVISAR CREDENCIALES")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





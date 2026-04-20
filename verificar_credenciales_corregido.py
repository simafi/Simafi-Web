#!/usr/bin/env python
"""
Script corregido para verificar las credenciales del usuario tributario
Usa el método correcto de Django para verificar contraseñas PBKDF2
"""

import os
import sys
import django
from django.contrib.auth.hashers import check_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
from modules.core.models import Municipio

def main():
    print("🔍 VERIFICACIÓN DE CREDENCIALES - SISTEMA SIMAFIWEB (CORREGIDO)")
    print("=" * 70)
    
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
            print(f"   ✅ Password Hash: {usuario.password[:50]}...")
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
        
        # 4. Verificar contraseña admin123 usando el método correcto de Django
        print("\n4. Verificando contraseña 'admin123' (método Django)...")
        if check_password('admin123', usuario.password):
            print("   ✅ Contraseña 'admin123' VERIFICADA con método Django")
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
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE VERIFICACIÓN")
        print("=" * 70)
        
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
        
        # 7. Test de login real
        print("\n" + "=" * 70)
        print("🧪 TEST DE LOGIN REAL")
        print("=" * 70)
        
        print("Para probar el login real, ejecuta:")
        print("1. Inicia el servidor: python manage.py runserver 127.0.0.1:8080")
        print("2. Ve a: http://127.0.0.1:8080/login/")
        print("3. Ingresa las credenciales:")
        print("   - Usuario: tributario")
        print("   - Contraseña: admin123")
        print("   - Municipio: 0301")
        
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
        print("🎯 Las credenciales están listas para usar")
        sys.exit(0)
    else:
        print("\n❌ VERIFICACIÓN FALLÓ - REVISAR CREDENCIALES")
        sys.exit(1)





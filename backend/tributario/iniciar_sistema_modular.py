#!/usr/bin/env python
"""
Script para iniciar el sistema modular
"""
import os
import sys
import subprocess
import time

def iniciar_sistema_modular():
    """Iniciar el sistema modular"""
    
    print("=== INICIANDO SISTEMA MUNICIPAL MODULAR ===")
    print("Configurando entorno...")
    
    # Verificar que estamos en el directorio correcto
    current_dir = os.getcwd()
    print(f"Directorio actual: {current_dir}")
    
    # Verificar que existe manage.py
    if not os.path.exists('manage.py'):
        print("❌ Error: No se encontró manage.py en el directorio actual")
        print("Asegúrate de estar en el directorio correcto del proyecto")
        return
    
    print("✅ manage.py encontrado")
    
    # Verificar configuración de Django
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
        django.setup()
        print("✅ Configuración de Django verificada")
    except Exception as e:
        print(f"❌ Error en configuración de Django: {e}")
        return
    
    # Verificar conexión a base de datos
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a base de datos verificada")
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return
    
    # Verificar módulos
    modulos_requeridos = [
        'modules.core',
        'modules.catastro',
        'modules.tributario',
        'modules.administrativo'
    ]
    
    for modulo in modulos_requeridos:
        try:
            __import__(modulo)
            print(f"✅ Módulo {modulo} verificado")
        except ImportError as e:
            print(f"❌ Error en módulo {modulo}: {e}")
    
    print("\n=== INICIANDO SERVIDOR ===")
    print("URL de acceso: http://127.0.0.1:8080")
    print("Presiona Ctrl+C para detener el servidor")
    print("\nCredenciales de prueba:")
    print("- Usuario: catastro, Contraseña: admin123, Municipio: 0301")
    print("- Usuario: tributario, Contraseña: admin123, Municipio: 0301")
    print("- Usuario: administrativo, Contraseña: admin123, Municipio: 0301")
    print("- Usuario: admin, Contraseña: admin123, Municipio: 001")
    
    try:
        # Iniciar servidor
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8080'])
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")

if __name__ == '__main__':
    iniciar_sistema_modular()


































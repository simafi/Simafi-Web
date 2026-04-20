#!/usr/bin/env python
"""
Test para verificar y corregir el error 'Cannot resolve keyword 'municipio_codigo' into field'
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.hashers import check_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario_app.models import usuario, Municipio

def test_error_municipio_codigo():
    """Test para verificar el error de municipio_codigo"""
    print("🔍 VERIFICANDO ERROR: Cannot resolve keyword 'municipio_codigo'")
    print("=" * 70)
    
    try:
        # 1. Verificar que el campo municipio_codigo NO existe
        print("1. Verificando estructura del modelo usuario...")
        user = usuario.objects.first()
        if user:
            campos_disponibles = [field.name for field in user._meta.fields]
            print(f"   ✅ Campos disponibles: {campos_disponibles}")
            
            if 'municipio_codigo' in campos_disponibles:
                print("   ❌ ERROR: El campo 'municipio_codigo' SÍ existe (no debería)")
            else:
                print("   ✅ CORRECTO: El campo 'municipio_codigo' NO existe")
                print("   ✅ El campo correcto es 'empresa'")
        else:
            print("   ❌ No hay usuarios en la base de datos")
            return False
        
        # 2. Verificar que el campo empresa SÍ existe
        print("\n2. Verificando campo 'empresa'...")
        if 'empresa' in campos_disponibles:
            print("   ✅ Campo 'empresa' existe correctamente")
        else:
            print("   ❌ ERROR: Campo 'empresa' no existe")
            return False
        
        # 3. Mostrar la diferencia entre los dos sistemas
        print("\n3. Comparando sistemas:")
        print("   📋 SISTEMA MODULAR (modules.usuarios):")
        print("      - Campo: municipio_id (ForeignKey)")
        print("      - Campo: municipio_codigo (CharField)")
        print("   📋 SISTEMA LEGACY (tributario_app):")
        print("      - Campo: empresa (CharField)")
        print("      - NO tiene municipio_codigo")
        
        # 4. Test de login que debería fallar
        print("\n4. Probando login que debería generar el error...")
        client = Client()
        login_data = {
            'usuario': 'tributario',
            'password': 'admin123',
            'municipio': '0301'
        }
        
        print(f"   🔍 Datos de login: {login_data}")
        
        try:
            response = client.post('/tributario-app/login/', login_data, follow=True)
            print(f"   🔍 Status code: {response.status_code}")
            
            if response.status_code == 500:
                print("   ❌ ERROR 500: El sistema está fallando (esperado)")
                print("   🔍 Esto confirma que hay un error en el código")
                return True
            elif response.status_code == 200:
                print("   ✅ Status 200: El login funcionó (inesperado)")
                return False
            else:
                print(f"   ⚠️  Status {response.status_code}: Comportamiento inesperado")
                return False
                
        except Exception as e:
            print(f"   ❌ Excepción capturada: {str(e)}")
            if 'municipio_codigo' in str(e):
                print("   ✅ CONFIRMADO: Error relacionado con 'municipio_codigo'")
                return True
            else:
                print("   ⚠️  Error diferente al esperado")
                return False
        
    except Exception as e:
        print(f"\n💥 Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_login_corregido():
    """Test de login con la lógica corregida"""
    print("\n" + "=" * 70)
    print("🔧 TEST DE LOGIN CORREGIDO")
    print("=" * 70)
    
    try:
        # Simular el login correcto usando el campo 'empresa'
        print("1. Simulando login correcto con campo 'empresa'...")
        
        # Buscar usuario tributario
        user = usuario.objects.get(usuario='tributario')
        municipio = Municipio.objects.get(codigo='0301')
        
        print(f"   ✅ Usuario: {user.usuario}")
        print(f"   ✅ Empresa: {user.empresa}")
        print(f"   ✅ Municipio: {municipio.codigo} - {municipio.descripcion}")
        
        # Verificar contraseña
        if check_password('admin123', user.password):
            print("   ✅ Contraseña verificada")
            
            # Verificar que empresa coincide con municipio
            if user.empresa == municipio.codigo:
                print("   ✅ Empresa coincide con municipio")
                print("   ✅ LOGIN CORRECTO SIMULADO")
                return True
            else:
                print(f"   ❌ Empresa {user.empresa} no coincide con municipio {municipio.codigo}")
                return False
        else:
            print("   ❌ Contraseña incorrecta")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en login corregido: {str(e)}")
        return False

def mostrar_solucion():
    """Mostrar la solución al problema"""
    print("\n" + "=" * 70)
    print("🔧 SOLUCIÓN AL PROBLEMA")
    print("=" * 70)
    
    print("📋 PROBLEMA IDENTIFICADO:")
    print("   El código está buscando 'municipio_codigo' pero en tributario_app")
    print("   el campo se llama 'empresa'")
    
    print("\n📋 CÓDIGO QUE ESTÁ FALLANDO:")
    print("   user = usuario.objects.get(")
    print("       usuario=usuario_input,")
    print("       municipio_codigo=municipio_input.codigo  # ❌ CAMPO INCORRECTO")
    print("   )")
    
    print("\n📋 CÓDIGO CORREGIDO:")
    print("   user = usuario.objects.get(")
    print("       usuario=usuario_input,")
    print("       empresa=municipio_input.codigo  # ✅ CAMPO CORRECTO")
    print("   )")
    
    print("\n📋 ARCHIVO A CORREGIR:")
    print("   C:\\simafiweb\\venv\\Scripts\\tributario\\tributario_app\\views.py")
    print("   Línea donde está el login_view()")
    
    print("\n📋 PASOS PARA CORREGIR:")
    print("   1. Abrir el archivo views.py de tributario_app")
    print("   2. Buscar la función login_view()")
    print("   3. Cambiar 'municipio_codigo' por 'empresa'")
    print("   4. Guardar el archivo")
    print("   5. Probar el login nuevamente")
    
    print("\n🎯 CREDENCIALES QUE DEBERÍAN FUNCIONAR:")
    print("   URL: http://127.0.0.1:8080/tributario-app/")
    print("   Usuario: tributario")
    print("   Contraseña: admin123")
    print("   Municipio: 0301")

def main():
    """Función principal"""
    print("🧪 TEST DE ERROR: Cannot resolve keyword 'municipio_codigo'")
    print("Verificando credenciales: tributario / admin123 / municipio 0301")
    print("URL: http://127.0.0.1:8080/tributario-app/")
    print("=" * 70)
    
    try:
        # Test 1: Verificar el error
        error_confirmado = test_error_municipio_codigo()
        
        # Test 2: Simular login corregido
        login_corregido = test_login_corregido()
        
        # Mostrar solución
        mostrar_solucion()
        
        if error_confirmado and login_corregido:
            print("\n✅ DIAGNÓSTICO COMPLETADO")
            print("🎯 El problema está identificado y la solución está lista")
            return 0
        else:
            print("\n⚠️  DIAGNÓSTICO INCOMPLETO")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)





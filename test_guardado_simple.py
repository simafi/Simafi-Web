#!/usr/bin/env python3
"""
Test de Guardado Simple
=======================

Este script simula el envío de datos al servidor para probar
si el guardado funciona correctamente.
"""

import requests
import json

def test_guardado_negocio():
    """Prueba el guardado de un negocio"""
    
    print("🧪 TEST DE GUARDADO DE NEGOCIO")
    print("=" * 50)
    
    # URL del servidor (ajustar según tu configuración)
    url = "http://localhost:8000/maestro_negocios/"
    
    # Datos de prueba para un nuevo negocio
    datos_prueba = {
        'accion': 'salvar',
        'empre': '0301',  # Municipio
        'rtm': '114-03-23',  # RTM
        'expe': '1151',  # Expediente
        'nombrenego': 'Negocio de Prueba',
        'comerciante': 'Juan Pérez',
        'identidad': '0801-1990-12345',
        'rtnpersonal': '0801-1990-12345',
        'rtnnego': '0801-1990-12345',
        'catastral': '123456789',
        'identidadrep': '0801-1990-12345',
        'representante': 'Juan Pérez',
        'direccion': 'Calle Principal #123',
        'actividad': 'A001',
        'estatus': 'A',
        'fecha_ini': '2024-01-01',
        'fecha_can': '',
        'telefono': '1234-5678',
        'celular': '9999-9999',
        'socios': 'Juan Pérez',
        'correo': 'juan@ejemplo.com',
        'pagweb': 'www.ejemplo.com',
        'comentario': 'Negocio de prueba para testing',
        'usuario': 'admin',
        'cx': '0.0000000',
        'cy': '0.0000000',
    }
    
    print("📤 Enviando datos de prueba:")
    for key, value in datos_prueba.items():
        print(f"   {key}: {value}")
    
    try:
        # Headers para simular petición AJAX
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        print(f"\n🌐 URL: {url}")
        print(f"📋 Headers: {headers}")
        
        # Hacer la petición POST
        response = requests.post(url, data=datos_prueba, headers=headers)
        
        print(f"\n📥 RESPUESTA DEL SERVIDOR:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'No especificado')}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        # Intentar parsear como JSON
        try:
            data = response.json()
            print(f"\n📋 RESPUESTA JSON:")
            print(f"   éxito: {data.get('exito', 'No especificado')}")
            print(f"   mensaje: {data.get('mensaje', 'No especificado')}")
            print(f"   requiere_confirmacion: {data.get('requiere_confirmacion', 'No especificado')}")
            print(f"   existe: {data.get('existe', 'No especificado')}")
            
            if data.get('exito'):
                print("\n✅ ¡GUARDADO EXITOSO!")
                print("✅ El servidor procesó la petición correctamente")
            else:
                print("\n❌ GUARDADO FALLIDO")
                print(f"❌ Error: {data.get('mensaje', 'Error desconocido')}")
                
        except json.JSONDecodeError:
            print(f"\n⚠️  RESPUESTA NO JSON:")
            print(f"   Contenido: {response.text[:500]}...")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR DE CONEXIÓN")
        print("❌ No se pudo conectar al servidor")
        print("❌ Verificar que el servidor Django esté ejecutándose")
        print("❌ Verificar la URL del servidor")
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")

def test_guardado_negocio_existente():
    """Prueba el guardado de un negocio que ya existe"""
    
    print("\n🧪 TEST DE GUARDADO DE NEGOCIO EXISTENTE")
    print("=" * 50)
    
    # URL del servidor
    url = "http://localhost:8000/maestro_negocios/"
    
    # Datos de prueba para un negocio que ya existe
    datos_prueba = {
        'accion': 'salvar',
        'empre': '0301',  # Municipio
        'rtm': '114-03-23',  # RTM
        'expe': '1151',  # Expediente
        'nombrenego': 'Negocio Actualizado',
        'comerciante': 'María García',
        'identidad': '0801-1990-54321',
        'rtnpersonal': '0801-1990-54321',
        'rtnnego': '0801-1990-54321',
        'catastral': '987654321',
        'identidadrep': '0801-1990-54321',
        'representante': 'María García',
        'direccion': 'Avenida Nueva #456',
        'actividad': 'A002',
        'estatus': 'A',
        'fecha_ini': '2024-01-01',
        'fecha_can': '',
        'telefono': '8765-4321',
        'celular': '8888-8888',
        'socios': 'María García',
        'correo': 'maria@ejemplo.com',
        'pagweb': 'www.maria.com',
        'comentario': 'Negocio actualizado para testing',
        'usuario': 'admin',
        'cx': '0.0000000',
        'cy': '0.0000000',
    }
    
    print("📤 Enviando datos de prueba (negocio existente):")
    for key, value in datos_prueba.items():
        print(f"   {key}: {value}")
    
    try:
        # Headers para simular petición AJAX
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        # Hacer la petición POST
        response = requests.post(url, data=datos_prueba, headers=headers)
        
        print(f"\n📥 RESPUESTA DEL SERVIDOR:")
        print(f"   Status Code: {response.status_code}")
        
        # Intentar parsear como JSON
        try:
            data = response.json()
            print(f"\n📋 RESPUESTA JSON:")
            print(f"   éxito: {data.get('exito', 'No especificado')}")
            print(f"   mensaje: {data.get('mensaje', 'No especificado')}")
            print(f"   requiere_confirmacion: {data.get('requiere_confirmacion', 'No especificado')}")
            print(f"   existe: {data.get('existe', 'No especificado')}")
            
            if data.get('requiere_confirmacion'):
                print("\n✅ ¡CONFIRMACIÓN REQUERIDA!")
                print("✅ El servidor detectó un negocio existente")
                print("✅ Se requiere confirmación para actualizar")
                
                # Simular confirmación
                datos_confirmacion = datos_prueba.copy()
                datos_confirmacion['confirmar_actualizacion'] = '1'
                
                print("\n📤 Enviando confirmación de actualización...")
                response_confirmacion = requests.post(url, data=datos_confirmacion, headers=headers)
                
                try:
                    data_confirmacion = response_confirmacion.json()
                    print(f"\n📋 RESPUESTA DE CONFIRMACIÓN:")
                    print(f"   éxito: {data_confirmacion.get('exito', 'No especificado')}")
                    print(f"   mensaje: {data_confirmacion.get('mensaje', 'No especificado')}")
                    
                    if data_confirmacion.get('exito'):
                        print("\n✅ ¡ACTUALIZACIÓN EXITOSA!")
                    else:
                        print("\n❌ ACTUALIZACIÓN FALLIDA")
                        print(f"❌ Error: {data_confirmacion.get('mensaje', 'Error desconocido')}")
                        
                except json.JSONDecodeError:
                    print(f"\n⚠️  RESPUESTA DE CONFIRMACIÓN NO JSON:")
                    print(f"   Contenido: {response_confirmacion.text[:500]}...")
            else:
                print("\n❌ NO SE REQUIRIÓ CONFIRMACIÓN")
                print("❌ El servidor no detectó un negocio existente")
                
        except json.JSONDecodeError:
            print(f"\n⚠️  RESPUESTA NO JSON:")
            print(f"   Contenido: {response.text[:500]}...")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR DE CONEXIÓN")
        print("❌ No se pudo conectar al servidor")
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")

def main():
    """Función principal"""
    
    print("🚀 INICIANDO TESTS DE GUARDADO")
    print("=" * 60)
    
    # Test 1: Guardar nuevo negocio
    test_guardado_negocio()
    
    # Test 2: Guardar negocio existente
    test_guardado_negocio_existente()
    
    print("\n📋 INSTRUCCIONES:")
    print("1. Asegúrate de que el servidor Django esté ejecutándose")
    print("2. Verifica que la URL sea correcta")
    print("3. Revisa los logs del servidor para más detalles")
    print("4. Si hay errores, verifica la configuración de la base de datos")

if __name__ == "__main__":
    main() 
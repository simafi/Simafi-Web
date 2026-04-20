#!/usr/bin/env python3
"""
Test de Confirmación de Actualización
====================================

Este script prueba específicamente la funcionalidad de confirmación
para actualizar negocios existentes.
"""

import requests
import json

def test_confirmacion_actualizacion():
    """Prueba la confirmación de actualización de un negocio existente"""
    
    print("🧪 TEST DE CONFIRMACIÓN DE ACTUALIZACIÓN")
    print("=" * 50)
    
    # URL del servidor (ajustar al puerto correcto)
    url = "http://localhost:8080/maestro_negocios/"
    
    # Datos de prueba para un negocio que ya existe
    datos_prueba = {
        'accion': 'salvar',
        'empre': '0301',  # Municipio
        'rtm': 'SANDRES',  # RTM (como en el ejemplo del usuario)
        'expe': '1',  # Expediente (como en el ejemplo del usuario)
        'nombrenego': 'Negocio de Prueba - Confirmación',
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
        'comentario': 'Negocio de prueba para testing de confirmación',
        'usuario': 'admin',
        'cx': '0.0000000',
        'cy': '0.0000000',
    }
    
    print("📤 Enviando datos de prueba (negocio existente):")
    print(f"   Empresa: {datos_prueba['empre']}")
    print(f"   RTM: {datos_prueba['rtm']}")
    print(f"   Expediente: {datos_prueba['expe']}")
    
    try:
        # Headers para simular petición AJAX
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        print(f"\n🌐 URL: {url}")
        print(f"📋 Headers: {headers}")
        
        # Hacer la petición POST inicial
        response = requests.post(url, data=datos_prueba, headers=headers, timeout=10)
        
        print(f"\n📥 RESPUESTA INICIAL DEL SERVIDOR:")
        print(f"   Status Code: {response.status_code}")
        
        # Intentar parsear como JSON
        try:
            data = response.json()
            print(f"\n📋 RESPUESTA JSON INICIAL:")
            print(f"   éxito: {data.get('exito', 'No especificado')}")
            print(f"   mensaje: {data.get('mensaje', 'No especificado')}")
            print(f"   requiere_confirmacion: {data.get('requiere_confirmacion', 'No especificado')}")
            print(f"   existe: {data.get('existe', 'No especificado')}")
            
            if data.get('requiere_confirmacion'):
                print("\n✅ ¡CONFIRMACIÓN REQUERIDA!")
                print("✅ El servidor detectó un negocio existente")
                print("✅ Se requiere confirmación para actualizar")
                print(f"✅ Mensaje esperado: {data.get('mensaje', 'No especificado')}")
                
                # Verificar que el mensaje contenga la información correcta
                mensaje = data.get('mensaje', '')
                if 'SANDRES' in mensaje and '1' in mensaje:
                    print("✅ El mensaje contiene la información correcta del negocio")
                else:
                    print("❌ El mensaje no contiene la información correcta del negocio")
                
                # Simular confirmación
                datos_confirmacion = datos_prueba.copy()
                datos_confirmacion['confirmar_actualizacion'] = '1'
                
                print("\n📤 Enviando confirmación de actualización...")
                response_confirmacion = requests.post(url, data=datos_confirmacion, headers=headers, timeout=10)
                
                print(f"\n📥 RESPUESTA DE CONFIRMACIÓN:")
                print(f"   Status Code: {response_confirmacion.status_code}")
                
                try:
                    data_confirmacion = response_confirmacion.json()
                    print(f"\n📋 RESPUESTA JSON DE CONFIRMACIÓN:")
                    print(f"   éxito: {data_confirmacion.get('exito', 'No especificado')}")
                    print(f"   mensaje: {data_confirmacion.get('mensaje', 'No especificado')}")
                    print(f"   actualizado: {data_confirmacion.get('actualizado', 'No especificado')}")
                    
                    if data_confirmacion.get('exito'):
                        print("\n✅ ¡ACTUALIZACIÓN EXITOSA!")
                        print("✅ El negocio fue actualizado correctamente")
                        return True
                    else:
                        print("\n❌ ACTUALIZACIÓN FALLIDA")
                        print(f"❌ Error: {data_confirmacion.get('mensaje', 'Error desconocido')}")
                        return False
                        
                except json.JSONDecodeError:
                    print(f"\n⚠️  RESPUESTA DE CONFIRMACIÓN NO JSON:")
                    print(f"   Contenido: {response_confirmacion.text[:500]}...")
                    return False
            else:
                print("\n❌ NO SE REQUIRIÓ CONFIRMACIÓN")
                print("❌ El servidor no detectó un negocio existente")
                print("❌ Verificar que el negocio exista en la base de datos")
                return False
                
        except json.JSONDecodeError:
            print(f"\n⚠️  RESPUESTA INICIAL NO JSON:")
            print(f"   Contenido: {response.text[:500]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR DE CONEXIÓN")
        print("❌ No se pudo conectar al servidor")
        print("❌ Verificar que Django esté ejecutándose en http://localhost:8080")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        return False

def test_mensaje_confirmacion():
    """Prueba que el mensaje de confirmación sea interactivo"""
    
    print("\n🧪 TEST DE MENSAJE DE CONFIRMACIÓN")
    print("=" * 50)
    
    # URL del servidor
    url = "http://localhost:8080/maestro_negocios/"
    
    # Datos de prueba
    datos_prueba = {
        'accion': 'salvar',
        'empre': '0301',
        'rtm': 'SANDRES',
        'expe': '1',
        'nombrenego': 'Test Mensaje',
        'comerciante': 'Test User',
        'identidad': '0801-1990-12345',
        'rtnpersonal': '0801-1990-12345',
        'rtnnego': '0801-1990-12345',
        'catastral': '123456789',
        'identidadrep': '0801-1990-12345',
        'representante': 'Test User',
        'direccion': 'Test Address',
        'actividad': 'A001',
        'estatus': 'A',
        'fecha_ini': '2024-01-01',
        'fecha_can': '',
        'telefono': '1234-5678',
        'celular': '9999-9999',
        'socios': 'Test User',
        'correo': 'test@ejemplo.com',
        'pagweb': 'www.test.com',
        'comentario': 'Test de mensaje',
        'usuario': 'admin',
        'cx': '0.0000000',
        'cy': '0.0000000',
    }
    
    try:
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.post(url, data=datos_prueba, headers=headers, timeout=10)
        
        try:
            data = response.json()
            
            if data.get('requiere_confirmacion'):
                mensaje = data.get('mensaje', '')
                print(f"✅ Mensaje de confirmación recibido: {mensaje}")
                
                # Verificar que el mensaje sea interactivo
                if '¿Desea actualizar' in mensaje:
                    print("✅ El mensaje es interactivo y solicita confirmación")
                    return True
                else:
                    print("❌ El mensaje no es interactivo")
                    return False
            else:
                print("❌ No se solicitó confirmación")
                return False
                
        except json.JSONDecodeError:
            print(f"⚠️  Respuesta no JSON: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error en test de mensaje: {str(e)}")
        return False

def main():
    """Función principal"""
    
    print("🚀 INICIANDO TESTS DE CONFIRMACIÓN")
    print("=" * 60)
    
    # Test 1: Confirmación de actualización
    confirmacion_ok = test_confirmacion_actualizacion()
    
    # Test 2: Mensaje de confirmación
    mensaje_ok = test_mensaje_confirmacion()
    
    print("\n📊 RESUMEN DE TESTS:")
    print(f"   🔄 Confirmación de actualización: {'✅ OK' if confirmacion_ok else '❌ FALLÓ'}")
    print(f"   💬 Mensaje de confirmación: {'✅ OK' if mensaje_ok else '❌ FALLÓ'}")
    
    if confirmacion_ok and mensaje_ok:
        print("\n🎉 ¡CONFIRMACIÓN FUNCIONA CORRECTAMENTE!")
        print("✅ El mensaje es interactivo y permite confirmar")
        print("✅ La actualización se procesa correctamente")
    else:
        print("\n⚠️  PROBLEMAS EN LA CONFIRMACIÓN")
        print("❌ Revisar la implementación del modal de confirmación")

if __name__ == "__main__":
    main() 
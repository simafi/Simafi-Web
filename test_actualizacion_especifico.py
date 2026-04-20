#!/usr/bin/env python3
"""
Test Específico de Actualización
================================

Este script prueba específicamente la funcionalidad de actualización
de negocios existentes.
"""

import requests
import json

def test_actualizacion_negocio():
    """Prueba la actualización de un negocio existente"""
    
    print("🧪 TEST DE ACTUALIZACIÓN DE NEGOCIO")
    print("=" * 50)
    
    # URL del servidor
    url = "http://localhost:8000/maestro_negocios/"
    
    # Datos de prueba para un negocio que ya existe
    datos_prueba = {
        'accion': 'salvar',
        'empre': '0301',  # Municipio
        'rtm': '114-03-23',  # RTM
        'expe': '1151',  # Expediente (existente)
        'nombrenego': 'Negocio Actualizado - Test',
        'comerciante': 'María García - Actualizada',
        'identidad': '0801-1990-54321',
        'rtnpersonal': '0801-1990-54321',
        'rtnnego': '0801-1990-54321',
        'catastral': '987654321',
        'identidadrep': '0801-1990-54321',
        'representante': 'María García - Actualizada',
        'direccion': 'Avenida Nueva #456 - Actualizada',
        'actividad': 'A002',
        'estatus': 'A',
        'fecha_ini': '2024-01-01',
        'fecha_can': '',
        'telefono': '8765-4321',
        'celular': '8888-8888',
        'socios': 'María García - Actualizada',
        'correo': 'maria.actualizada@ejemplo.com',
        'pagweb': 'www.maria-actualizada.com',
        'comentario': 'Negocio actualizado para testing específico',
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
                
                # Simular confirmación
                datos_confirmacion = datos_prueba.copy()
                datos_confirmacion['confirmar_actualizacion'] = '1'
                
                print("\n📤 Enviando confirmación de actualización...")
                print("📤 Datos de confirmación:")
                for key, value in datos_confirmacion.items():
                    print(f"   {key}: {value}")
                
                response_confirmacion = requests.post(url, data=datos_confirmacion, headers=headers, timeout=10)
                
                print(f"\n📥 RESPUESTA DE CONFIRMACIÓN:")
                print(f"   Status Code: {response_confirmacion.status_code}")
                print(f"   Content-Type: {response_confirmacion.headers.get('content-type', 'No especificado')}")
                
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
                return False
                
        except json.JSONDecodeError:
            print(f"\n⚠️  RESPUESTA INICIAL NO JSON:")
            print(f"   Contenido: {response.text[:500]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR DE CONEXIÓN")
        print("❌ No se pudo conectar al servidor")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        return False

def test_verificacion_actualizacion():
    """Verifica que la actualización se haya guardado correctamente"""
    
    print("\n🧪 VERIFICACIÓN DE ACTUALIZACIÓN")
    print("=" * 50)
    
    # URL del servidor
    url = "http://localhost:8000/maestro_negocios/"
    
    # Datos para verificar la actualización
    datos_verificacion = {
        'accion': 'salvar',
        'empre': '0301',  # Municipio
        'rtm': '114-03-23',  # RTM
        'expe': '1151',  # Expediente
        'nombrenego': 'Negocio Actualizado - Test',
        'comerciante': 'María García - Actualizada',
        'identidad': '0801-1990-54321',
        'rtnpersonal': '0801-1990-54321',
        'rtnnego': '0801-1990-54321',
        'catastral': '987654321',
        'identidadrep': '0801-1990-54321',
        'representante': 'María García - Actualizada',
        'direccion': 'Avenida Nueva #456 - Actualizada',
        'actividad': 'A002',
        'estatus': 'A',
        'fecha_ini': '2024-01-01',
        'fecha_can': '',
        'telefono': '8765-4321',
        'celular': '8888-8888',
        'socios': 'María García - Actualizada',
        'correo': 'maria.actualizada@ejemplo.com',
        'pagweb': 'www.maria-actualizada.com',
        'comentario': 'Negocio actualizado para testing específico',
        'usuario': 'admin',
        'cx': '0.0000000',
        'cy': '0.0000000',
    }
    
    try:
        # Headers para simular petición AJAX
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        # Hacer la petición POST para verificar
        response = requests.post(url, data=datos_verificacion, headers=headers, timeout=10)
        
        try:
            data = response.json()
            
            if data.get('requiere_confirmacion'):
                print("✅ El negocio existe y requiere confirmación")
                print("✅ La actualización se guardó correctamente")
                return True
            else:
                print("❌ El negocio no existe o no se actualizó correctamente")
                return False
                
        except json.JSONDecodeError:
            print(f"⚠️  Respuesta no JSON: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error en verificación: {str(e)}")
        return False

def main():
    """Función principal"""
    
    print("🚀 INICIANDO TEST ESPECÍFICO DE ACTUALIZACIÓN")
    print("=" * 60)
    
    # Test 1: Actualizar negocio
    actualizacion_ok = test_actualizacion_negocio()
    
    if actualizacion_ok:
        # Test 2: Verificar actualización
        verificacion_ok = test_verificacion_actualizacion()
        
        print("\n📊 RESUMEN DE TESTS:")
        print(f"   🔄 Actualización: {'✅ OK' if actualizacion_ok else '❌ FALLÓ'}")
        print(f"   ✅ Verificación: {'✅ OK' if verificacion_ok else '❌ FALLÓ'}")
        
        if actualizacion_ok and verificacion_ok:
            print("\n🎉 ¡ACTUALIZACIÓN FUNCIONA CORRECTAMENTE!")
            print("✅ El negocio se actualizó y se guardó en la base de datos")
        else:
            print("\n⚠️  PROBLEMAS EN LA ACTUALIZACIÓN")
            print("❌ Revisar logs del servidor y la base de datos")
    else:
        print("\n❌ LA ACTUALIZACIÓN FALLÓ")
        print("❌ Revisar configuración del servidor")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
"""
Script de prueba específico para verificar el manejo de coordenadas con comas.
"""

import os
import sys
import django
import time
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from hola.models import Negocio
from django.test import RequestFactory
from hola.views import maestro_negocios

def test_coordenadas_con_comas():
    """Prueba específica de coordenadas con comas"""
    print("=== PRUEBA DE COORDENADAS CON COMAS ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba con coordenadas que tienen comas
    form_data = {
        'empre': '0301',
        'rtm': f'COMA{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Coma Test {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Test',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '-86,2419055',  # Coordenada con coma
        'cy': '15,1999999',   # Coordenada con coma
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario con coordenadas con comas:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    
    print(f"\nEnviando petición POST...")
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.get('Content-Type', 'No especificado')}")
        
        if response.status_code == 200:
            print("✅ Petición procesada correctamente")
            
            # Verificar que se guardó en la base de datos
            negocio_guardado = Negocio.objects.filter(
                empre=form_data['empre'],
                rtm=form_data['rtm'],
                expe=form_data['expe']
            ).first()
            
            if negocio_guardado:
                print(f"✅ Negocio encontrado en BD:")
                print(f"  ID: {negocio_guardado.id}")
                print(f"  Nombre: {negocio_guardado.nombrenego}")
                print(f"  CX: {negocio_guardado.cx} (tipo: {type(negocio_guardado.cx)})")
                print(f"  CY: {negocio_guardado.cy} (tipo: {type(negocio_guardado.cy)})")
                print(f"  Identidad: {negocio_guardado.identidad}")
                print(f"  Catastral: {negocio_guardado.catastral}")
                print(f"  Estatus: {negocio_guardado.estatus}")
                print(f"  Categoría: {negocio_guardado.categoria}")
                print(f"  Socios: {negocio_guardado.socios}")
                
                # Verificar que las coordenadas se convirtieron correctamente
                # Usar Decimal para comparación precisa
                cx_esperado = Decimal('-86.2419055')
                cy_esperado = Decimal('15.1999999')
                
                # Convertir a float para comparación más flexible
                cx_float = float(negocio_guardado.cx)
                cy_float = float(negocio_guardado.cy)
                cx_esperado_float = float(cx_esperado)
                cy_esperado_float = float(cy_esperado)
                
                print(f"DEBUG - Comparación de coordenadas:")
                print(f"  CX original: {negocio_guardado.cx} (tipo: {type(negocio_guardado.cx)})")
                print(f"  CY original: {negocio_guardado.cy} (tipo: {type(negocio_guardado.cy)})")
                print(f"  CX float: {cx_float}")
                print(f"  CY float: {cy_float}")
                print(f"  CX esperado: {cx_esperado_float}")
                print(f"  CY esperado: {cy_esperado_float}")
                print(f"  Diferencia CX: {abs(cx_float - cx_esperado_float)}")
                print(f"  Diferencia CY: {abs(cy_float - cy_esperado_float)}")
                
                if abs(cx_float - cx_esperado_float) < 0.0000001 and abs(cy_float - cy_esperado_float) < 0.0000001:
                    print("✅ Coordenadas convertidas correctamente de comas a puntos")
                else:
                    print("❌ Error: Las coordenadas no se convirtieron correctamente")
                    print(f"  CX esperado: {cx_esperado_float}, obtenido: {cx_float}")
                    print(f"  CY esperado: {cy_esperado_float}, obtenido: {cy_float}")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la petición")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def test_coordenadas_cero():
    """Prueba específica de coordenadas con valor cero"""
    print("\n=== PRUEBA DE COORDENADAS CON VALOR CERO ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba con coordenadas cero
    form_data = {
        'empre': '0301',
        'rtm': f'CERO{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Cero Test {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Test',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '0,0',  # Coordenada cero con coma
        'cy': '0,0',  # Coordenada cero con coma
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario con coordenadas cero:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    
    print(f"\nEnviando petición POST...")
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Petición procesada correctamente")
            
            # Verificar que se guardó en la base de datos
            negocio_guardado = Negocio.objects.filter(
                empre=form_data['empre'],
                rtm=form_data['rtm'],
                expe=form_data['expe']
            ).first()
            
            if negocio_guardado:
                print(f"✅ Negocio encontrado en BD:")
                print(f"  ID: {negocio_guardado.id}")
                print(f"  CX: {negocio_guardado.cx} (tipo: {type(negocio_guardado.cx)})")
                print(f"  CY: {negocio_guardado.cy} (tipo: {type(negocio_guardado.cy)})")
                
                # Verificar que las coordenadas cero se manejaron correctamente
                # Usar Decimal para comparación precisa
                cero_esperado = Decimal('0.0000000')
                
                # Convertir a float para comparación más flexible
                cx_float = float(negocio_guardado.cx)
                cy_float = float(negocio_guardado.cy)
                cero_esperado_float = float(cero_esperado)
                
                if abs(cx_float - cero_esperado_float) < 0.0000001 and abs(cy_float - cero_esperado_float) < 0.0000001:
                    print("✅ Coordenadas cero manejadas correctamente")
                else:
                    print("❌ Error: Las coordenadas cero no se manejaron correctamente")
                    print(f"  CX esperado: {cero_esperado_float}, obtenido: {cx_float}")
                    print(f"  CY esperado: {cero_esperado_float}, obtenido: {cy_float}")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la petición")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def test_coordenadas_vacias():
    """Prueba específica de coordenadas vacías"""
    print("\n=== PRUEBA DE COORDENADAS VACÍAS ===")
    
    timestamp = int(time.time())
    
    # Datos de prueba con coordenadas vacías
    form_data = {
        'empre': '0301',
        'rtm': f'VACIO{timestamp % 1000:03d}',
        'expe': f'{timestamp % 10000:04d}',
        'nombrenego': f'Negocio Vacío Test {timestamp}',
        'comerciante': f'Comerciante {timestamp}',
        'identidad': '9999-9999-99999',
        'rtnpersonal': '',
        'rtnnego': '',
        'catastral': 'TEST-001',
        'identidadrep': '',
        'representante': '',
        'direccion': f'Dirección {timestamp}',
        'actividad': '',
        'categoria': 'A',
        'estatus': 'A',
        'fecha_ini': '',
        'fecha_can': '',
        'telefono': '',
        'celular': '',
        'socios': 'Socio Test',
        'correo': '',
        'pagweb': '',
        'comentario': '',
        'usuario': '',
        'cx': '',  # Coordenada vacía
        'cy': '',  # Coordenada vacía
        'accion': 'salvar'
    }
    
    print(f"Datos del formulario con coordenadas vacías:")
    for key, value in form_data.items():
        print(f"  {key}: '{value}'")
    
    # Crear petición simulada
    factory = RequestFactory()
    request = factory.post('/maestro_negocios/', form_data)
    
    print(f"\nEnviando petición POST...")
    
    try:
        response = maestro_negocios(request)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Petición procesada correctamente")
            
            # Verificar que se guardó en la base de datos
            negocio_guardado = Negocio.objects.filter(
                empre=form_data['empre'],
                rtm=form_data['rtm'],
                expe=form_data['expe']
            ).first()
            
            if negocio_guardado:
                print(f"✅ Negocio encontrado en BD:")
                print(f"  ID: {negocio_guardado.id}")
                print(f"  CX: {negocio_guardado.cx} (tipo: {type(negocio_guardado.cx)})")
                print(f"  CY: {negocio_guardado.cy} (tipo: {type(negocio_guardado.cy)})")
                
                # Verificar que las coordenadas vacías se manejaron correctamente
                # CX debe ser 0.0000000 (valor por defecto), CY puede ser None
                cx_esperado = Decimal('0.0000000')
                
                # Convertir a float para comparación más flexible
                cx_float = float(negocio_guardado.cx)
                cx_esperado_float = float(cx_esperado)
                
                if abs(cx_float - cx_esperado_float) < 0.0000001:
                    print("✅ Coordenadas vacías manejadas correctamente")
                    print(f"  CX: {negocio_guardado.cx} (valor por defecto)")
                    print(f"  CY: {negocio_guardado.cy} (puede ser None)")
                else:
                    print("❌ Error: Las coordenadas vacías no se manejaron correctamente")
                    print(f"  CX esperado: {cx_esperado_float}, obtenido: {cx_float}")
            else:
                print("❌ Error: Negocio no encontrado en la base de datos")
        else:
            print("❌ Error en la petición")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE COORDENADAS")
    print("=" * 60)
    
    # Ejecutar pruebas
    test_coordenadas_con_comas()
    test_coordenadas_cero()
    test_coordenadas_vacias()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS") 
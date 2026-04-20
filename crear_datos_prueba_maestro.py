#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crear datos de prueba para maestro negocios
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, r'C:\simafiweb\venv\Scripts')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.tributario_app.settings')
django.setup()

from tributario.models import Identificacion, Negocio, Actividad, Municipio

def crear_datos():
    print("Creando datos de prueba...")
    
    # 1. Crear municipio si no existe
    municipio, created = Municipio.objects.get_or_create(
        codigo='0801',
        defaults={'nombre': 'DISTRITO CENTRAL'}
    )
    print(f"✅ Municipio: {municipio.codigo} - {municipio.nombre}")
    
    # 2. Crear identificación de prueba
    identificacion, created = Identificacion.objects.get_or_create(
        identidad='0801199012345',
        defaults={
            'nombres': 'JUAN CARLOS',
            'apellidos': 'PEREZ LOPEZ',
            'fechanac': '1990-05-15'
        }
    )
    print(f"✅ Identificación: {identificacion.identidad} - {identificacion.nombres} {identificacion.apellidos}")
    
    # 3. Crear otra identificación para representante
    identificacion2, created = Identificacion.objects.get_or_create(
        identidad='0801198523456',
        defaults={
            'nombres': 'MARIA ELENA',
            'apellidos': 'GARCIA MARTINEZ',
            'fechanac': '1985-08-20'
        }
    )
    print(f"✅ Identificación 2: {identificacion2.identidad} - {identificacion2.nombres} {identificacion2.apellidos}")
    
    # 4. Crear actividad económica si no existe
    actividad, created = Actividad.objects.get_or_create(
        empresa='0801',
        codigo='001',
        defaults={'descripcion': 'VENTA AL POR MENOR DE ALIMENTOS'}
    )
    print(f"✅ Actividad: {actividad.codigo} - {actividad.descripcion}")
    
    # 5. Crear negocio de prueba
    negocio, created = Negocio.objects.get_or_create(
        empresa='0801',
        rtm='001',
        expe='00001',
        defaults={
            'nombrenego': 'PULPERIA DON JUAN',
            'comerciante': 'JUAN CARLOS PEREZ LOPEZ',
            'identidad': '0801199012345',
            'representante': 'MARIA ELENA GARCIA MARTINEZ',
            'identidadrep': '0801198523456',
            'actividad': '001',
            'direccion': 'BARRIO LA GRANJA, CASA 123',
            'telefono': '22123456',
            'estatus': 'A',
            'rtnpersonal': '08011990123456',
            'rtnnego': '08019901234567'
        }
    )
    
    if created:
        print(f"✅ Negocio creado: {negocio.empresa}-{negocio.rtm}-{negocio.expe}")
        print(f"   Nombre: {negocio.nombrenego}")
        print(f"   Comerciante: {negocio.comerciante}")
    else:
        print(f"ℹ️  Negocio ya existía: {negocio.empresa}-{negocio.rtm}-{negocio.expe}")
    
    print("\n" + "="*60)
    print("DATOS DE PRUEBA CREADOS EXITOSAMENTE")
    print("="*60)
    print("\nPuedes usar estos datos para probar:")
    print(f"  DNI: 0801199012345 (para buscar nombre: JUAN CARLOS PEREZ LOPEZ)")
    print(f"  DNI Rep: 0801198523456 (para buscar nombre: MARIA ELENA GARCIA MARTINEZ)")
    print(f"  Negocio: Empresa=0801, RTM=001, EXPE=00001")

if __name__ == '__main__':
    try:
        crear_datos()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()



























































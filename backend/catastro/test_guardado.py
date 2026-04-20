#!/usr/bin/env python
"""
Script de prueba para verificar el guardado de bienes inmuebles
Ejecutar: python manage.py shell < test_guardado.py
O desde shell de Django: exec(open('test_guardado.py').read())
"""
from catastro.models import BDCata1
from django.utils import timezone
from datetime import datetime
from decimal import Decimal

def test_guardado():
    """Prueba el guardado de un bien inmueble con datos reales"""
    print("=" * 80)
    print("=== TEST DE GUARDADO DE BIEN INMUEBLE ===")
    print("=" * 80)
    
    # Datos de prueba proporcionados por el usuario
    datos = {
        'id': 14,
        'empresa': '0301',
        'cocata1': 'CL11-0B-01-10',
        'ficha': '2',
        'claveant': '',
        'mapa': 'CL11-0B',
        'bloque': '01',
        'predio': '10',
        'depto': '03',
        'municipio': '01',
        'barrio': '',
        'caserio': '',
        'sitio': 'EF',
        'nombres': 'GERMAN',
        'apellidos': 'SANCHEZ',
        'identidad': '0401-1974-00258',
        'rtn': '',
        'ubicacion': 'ALDEA BELEN',
        'nacionalidad': '205',
        'uso': '0',
        'subuso': '1',
        'constru': '0',
        'comentario': 'VENDIO UNA  AREA DE TERRENO EN ESTA FECHA 09-02-15',
        'nofichas': '0',
        'bvl2tie': 653976.25,
        'conedi': 0,
        'mejoras': 348504.5,
        'cedif': 1,
        'detalle': 13601.75,
        'impuesto': 2607.98,
        'grabable': 1133905.91,
        'cultivo': 0,
        'declarado': 0,
        'condetalle': 1,
        'exencion': 20000,
        'usuario': 'MAURICIO',
        'fechasys': datetime.strptime('9/2/2015 09:52:00', '%d/%m/%Y %H:%M:%S'),
        'st': '0',
        'codhab': '0',
        'codprop': '01',
        'bexenc': 1,
        'tasaimpositiva': 0,
        'declaimpto': 0,
        'sexo': '',
        'telefono': '0',
        'tipopropiedad': '1',
        'estado': 'A',
        'clavesure': '',
        'cx': 0,
        'cy': 0,
        'zonificacion': '',
    }
    
    print("\n1. Verificando si ya existe un registro con estos datos...")
    try:
        existing = BDCata1.objects.filter(
            empresa=datos['empresa'],
            cocata1=datos['cocata1']
        ).first()
        
        if existing:
            print(f"   ✓ Registro existente encontrado: ID={existing.id}")
            print(f"   ¿Desea actualizarlo? (S/N): ", end='')
            respuesta = input().strip().upper()
            if respuesta == 'S':
                bien = existing
                print("   Actualizando registro existente...")
            else:
                print("   Creando nuevo registro con código catastral diferente...")
                datos['cocata1'] = datos['cocata1'] + '-TEST'
                bien = BDCata1()
        else:
            print("   ✓ No existe, creando nuevo registro...")
            bien = BDCata1()
    except Exception as e:
        print(f"   ✗ Error al buscar: {str(e)}")
        bien = BDCata1()
    
    print("\n2. Asignando valores a los campos...")
    campos_asignados = 0
    for campo, valor in datos.items():
        if campo == 'id':
            continue  # No asignar ID manualmente
        try:
            if hasattr(bien, campo):
                # Convertir valores vacíos a None o valores por defecto
                if valor == '' or valor is None:
                    if campo in ['bvl2tie', 'conedi', 'mejoras', 'cedif', 'detalle', 'impuesto', 'grabable', 'cultivo', 'declarado', 'exencion', 'bexenc', 'tasaimpositiva', 'declaimpto', 'cx', 'cy']:
                        setattr(bien, campo, 0)
                    else:
                        setattr(bien, campo, None if campo not in ['ficha', 'nofichas'] else '0')
                else:
                    setattr(bien, campo, valor)
                campos_asignados += 1
                print(f"   ✓ {campo}: {str(valor)[:50]}")
            else:
                print(f"   ⚠ Campo '{campo}' no existe en el modelo")
        except Exception as e:
            print(f"   ✗ Error al asignar {campo}: {str(e)}")
    
    print(f"\n   Total de campos asignados: {campos_asignados}")
    
    # Asignar valores adicionales
    print("\n3. Asignando valores adicionales (usuario, fecha, empresa)...")
    bien.usuario = 'TEST_USER'
    bien.fechasys = timezone.now()
    if not bien.empresa:
        bien.empresa = '0301'
    print(f"   ✓ usuario: {bien.usuario}")
    print(f"   ✓ fechasys: {bien.fechasys}")
    print(f"   ✓ empresa: {bien.empresa}")
    
    print("\n4. Validando datos antes de guardar...")
    print(f"   cocata1: {bien.cocata1}")
    print(f"   empresa: {bien.empresa}")
    print(f"   nombres: {bien.nombres}")
    print(f"   apellidos: {bien.apellidos}")
    print(f"   identidad: {bien.identidad}")
    
    print("\n5. Intentando guardar en la base de datos...")
    try:
        bien.save()
        print("=" * 80)
        print(f"✓✓✓ GUARDADO EXITOSO - ID: {bien.id} ✓✓✓")
        print("=" * 80)
        
        print("\n6. Verificando que se guardó correctamente...")
        bien_verificado = BDCata1.objects.get(id=bien.id)
        print(f"   ✓ ID: {bien_verificado.id}")
        print(f"   ✓ cocata1: {bien_verificado.cocata1}")
        print(f"   ✓ empresa: {bien_verificado.empresa}")
        print(f"   ✓ nombres: {bien_verificado.nombres}")
        print(f"   ✓ apellidos: {bien_verificado.apellidos}")
        print(f"   ✓ usuario: {bien_verificado.usuario}")
        print(f"   ✓ fechasys: {bien_verificado.fechasys}")
        print(f"   ✓ bvl2tie: {bien_verificado.bvl2tie}")
        print(f"   ✓ impuesto: {bien_verificado.impuesto}")
        
        print("\n" + "=" * 80)
        print("✓✓✓ TEST COMPLETADO EXITOSAMENTE ✓✓✓")
        print("=" * 80)
        return True
        
    except Exception as e:
        print("=" * 80)
        print(f"✗✗✗ ERROR AL GUARDAR ✗✗✗")
        print("=" * 80)
        print(f"Error: {str(e)}")
        import traceback
        print("\nTraceback completo:")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_guardado()


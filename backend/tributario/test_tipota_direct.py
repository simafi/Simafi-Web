#!/usr/bin/env python
"""
Script directo para verificar el campo tipota en la base de datos
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla

def test_tipota_direct():
    print("🔍 TESTEO DIRECTO DEL CAMPO TIPOTA")
    print("=" * 50)
    
    # Parámetros específicos del negocio
    empresa = "0301"
    rtm = "114-03-23"
    expe = "1151"
    
    try:
        # Consulta directa con los mismos parámetros que usa la vista
        tasas = TasasDecla.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe
        ).order_by('rubro', 'cod_tarifa')
        
        print(f"📊 Registros encontrados: {tasas.count()}")
        
        if tasas.count() == 0:
            print("❌ No se encontraron registros")
            return
        
        print("\n🔍 DETALLES DE CADA REGISTRO:")
        for i, tasa in enumerate(tasas, 1):
            print(f"\n{i}. ID: {tasa.id}")
            print(f"   RTM: {tasa.rtm}")
            print(f"   Expediente: {tasa.expe}")
            print(f"   Rubro: {tasa.rubro}")
            print(f"   Valor: {tasa.valor}")
            print(f"   Frecuencia: {tasa.frecuencia}")
            
            # Verificar campo tipota
            print(f"   🔍 TIPOTA:")
            print(f"      - Valor: '{tasa.tipota}'")
            print(f"      - Tipo: {type(tasa.tipota)}")
            print(f"      - Longitud: {len(str(tasa.tipota))}")
            print(f"      - Repr: {repr(tasa.tipota)}")
            print(f"      - Es vacío: {tasa.tipota == ''}")
            print(f"      - Es None: {tasa.tipota is None}")
            
            # Verificar si tiene el campo
            if hasattr(tasa, 'tipota'):
                print(f"      - Campo existe: ✅")
            else:
                print(f"      - Campo existe: ❌")
            
            # Verificar si tiene el campo tipo (antiguo)
            if hasattr(tasa, 'tipo'):
                print(f"      - Campo tipo (antiguo): '{tasa.tipo}'")
            else:
                print(f"      - Campo tipo (antiguo): No existe")
        
        # Consulta SQL directa
        print(f"\n🔍 CONSULTA SQL DIRECTA:")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, rtm, expe, rubro, tipota, valor 
                FROM tasasdecla 
                WHERE empresa = %s AND rtm = %s AND expe = %s
                ORDER BY rubro, cod_tarifa
            """, [empresa, rtm, expe])
            
            rows = cursor.fetchall()
            print(f"   Registros SQL: {len(rows)}")
            
            for i, row in enumerate(rows, 1):
                print(f"   {i}. ID: {row[0]}, RTM: {row[1]}, Expe: {row[2]}, Rubro: {row[3]}")
                print(f"      TIPOTA SQL: '{row[4]}' (tipo: {type(row[4])})")
                print(f"      Valor: {row[5]}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tipota_direct()










































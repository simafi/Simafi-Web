#!/usr/bin/env python
"""
Script para verificar y corregir el problema del campo tipota
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla
from django.db import connection

def test_and_fix_tipota():
    print("🔧 VERIFICACIÓN Y CORRECCIÓN DEL CAMPO TIPOTA")
    print("=" * 60)
    
    # Parámetros específicos
    empresa = "0301"
    rtm = "114-03-23"
    expe = "1151"
    
    try:
        # 1. Verificar estructura de la tabla
        print("1. VERIFICANDO ESTRUCTURA DE LA TABLA:")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE, COLUMN_DEFAULT
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'tasasdecla'
                AND COLUMN_NAME IN ('tipota', 'tipo')
                ORDER BY COLUMN_NAME;
            """)
            
            columns = cursor.fetchall()
            print(f"   Columnas encontradas: {len(columns)}")
            for col in columns:
                print(f"   - {col[0]}: {col[1]}({col[2]}) - Nullable: {col[3]} - Default: {col[4]}")
        
        # 2. Consulta SQL directa
        print("\n2. CONSULTA SQL DIRECTA:")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, rtm, expe, rubro, tipota, valor 
                FROM tasasdecla 
                WHERE empresa = %s AND rtm = %s AND expe = %s
                ORDER BY rubro, cod_tarifa
            """, [empresa, rtm, expe])
            
            sql_rows = cursor.fetchall()
            print(f"   Registros SQL: {len(sql_rows)}")
            for i, row in enumerate(sql_rows, 1):
                print(f"   {i}. ID: {row[0]}, Rubro: {row[3]}, TIPOTA: '{row[4]}' (tipo: {type(row[4])})")
        
        # 3. Consulta Django ORM
        print("\n3. CONSULTA DJANGO ORM:")
        tasas = TasasDecla.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe
        ).order_by('rubro', 'cod_tarifa')
        
        print(f"   Registros Django: {tasas.count()}")
        for i, tasa in enumerate(tasas, 1):
            print(f"   {i}. ID: {tasa.id}, Rubro: {tasa.rubro}, TIPOTA: '{tasa.tipota}' (tipo: {type(tasa.tipota)})")
        
        # 4. Verificar si hay diferencia
        print("\n4. COMPARACIÓN:")
        if len(sql_rows) == len(tasas):
            print("   ✅ Mismo número de registros")
            for i, (sql_row, django_tasa) in enumerate(zip(sql_rows, tasas), 1):
                sql_tipota = sql_row[4]
                django_tipota = django_tasa.tipota
                if sql_tipota == django_tipota:
                    print(f"   ✅ Registro {i}: Coincide - '{sql_tipota}' == '{django_tipota}'")
                else:
                    print(f"   ❌ Registro {i}: NO coincide - SQL: '{sql_tipota}' vs Django: '{django_tipota}'")
        else:
            print(f"   ❌ Diferente número de registros - SQL: {len(sql_rows)}, Django: {tasas.count()}")
        
        # 5. Intentar forzar la recarga del modelo
        print("\n5. INTENTANDO FORZAR RECARGA DEL MODELO:")
        try:
            # Limpiar la caché del modelo
            from django.db.models import loading
            loading.cache.clear()
            
            # Recargar el modelo
            from importlib import reload
            import tributario.models
            reload(tributario.models)
            
            # Nueva consulta
            tasas_reloaded = TasasDecla.objects.filter(
                empresa=empresa,
                rtm=rtm,
                expe=expe
            ).order_by('rubro', 'cod_tarifa')
            
            print(f"   Registros después de recarga: {tasas_reloaded.count()}")
            for i, tasa in enumerate(tasas_reloaded, 1):
                print(f"   {i}. ID: {tasa.id}, Rubro: {tasa.rubro}, TIPOTA: '{tasa.tipota}' (tipo: {type(tasa.tipota)})")
                
        except Exception as e:
            print(f"   ❌ Error en recarga: {e}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_and_fix_tipota()










































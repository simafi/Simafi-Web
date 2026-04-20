#!/usr/bin/env python
"""
Script de depuración para verificar la búsqueda de descripciones de rubros
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simafiweb.settings')
django.setup()

from django.db import connection

def debug_rubros():
    """Verifica la búsqueda de rubros en la base de datos"""
    
    # Obtener un ejemplo de transacción
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT empresa, rubro 
            FROM transaccionesics 
            WHERE rubro IS NOT NULL 
            AND rubro != '' 
            LIMIT 5
        """)
        transacciones = cursor.fetchall()
        
        print("=" * 80)
        print("TRANSACCIONES ENCONTRADAS:")
        print("=" * 80)
        for empresa, rubro in transacciones:
            print(f"Empresa: '{empresa}' (tipo: {type(empresa)}, len: {len(str(empresa)) if empresa else 0})")
            print(f"Rubro: '{rubro}' (tipo: {type(rubro)}, len: {len(str(rubro)) if rubro else 0})")
            
            # Buscar el rubro en la tabla rubros
            cursor.execute("""
                SELECT empresa, codigo, descripcion 
                FROM rubros 
                WHERE empresa = %s AND codigo = %s
            """, [empresa, rubro])
            
            rubro_encontrado = cursor.fetchone()
            
            if rubro_encontrado:
                emp_r, cod_r, desc_r = rubro_encontrado
                print(f"✅ RUBRO ENCONTRADO:")
                print(f"   Empresa: '{emp_r}'")
                print(f"   Codigo: '{cod_r}'")
                print(f"   Descripcion: '{desc_r}'")
            else:
                print(f"❌ RUBRO NO ENCONTRADO")
                
                # Intentar búsqueda flexible
                cursor.execute("""
                    SELECT empresa, codigo, descripcion 
                    FROM rubros 
                    WHERE TRIM(empresa) = TRIM(%s) AND TRIM(codigo) = TRIM(%s)
                """, [str(empresa).strip(), str(rubro).strip()])
                
                rubro_flexible = cursor.fetchone()
                if rubro_flexible:
                    print(f"⚠️  ENCONTRADO CON TRIM:")
                    emp_r, cod_r, desc_r = rubro_flexible
                    print(f"   Empresa: '{emp_r}'")
                    print(f"   Codigo: '{cod_r}'")
                    print(f"   Descripcion: '{desc_r}'")
                
                # Mostrar rubros disponibles para esa empresa
                cursor.execute("""
                    SELECT codigo, descripcion 
                    FROM rubros 
                    WHERE empresa = %s
                    LIMIT 10
                """, [empresa])
                
                rubros_disponibles = cursor.fetchall()
                if rubros_disponibles:
                    print(f"📋 RUBROS DISPONIBLES PARA EMPRESA '{empresa}':")
                    for cod, desc in rubros_disponibles:
                        print(f"   - Codigo: '{cod}', Descripcion: '{desc}'")
            
            print("-" * 80)

if __name__ == "__main__":
    debug_rubros()


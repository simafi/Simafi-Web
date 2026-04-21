import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get('DIRECT_URL')

tables_to_disable_rls = [
    # Tablas núcleo
    'negocios', 'negocio', 'actividad', 'oficina', 'rubros', 'transaccionesics',
    
    # Tablas de configuración y parámetros
    'parametros_tributarios',
    
    # Tablas de procesos
    'pagovariostemp', 'declara', 'planarbitio', 'tarifas', 'tasasdecla', 'tarifasics',
    'identificacion', 'norecibos',
    
    # Módulo de Contabilidad
    'cont_ejercicio_fiscal', 'cont_periodo_contable', 'cont_grupo_cuenta', 'cont_cuenta_contable',
    'cont_centro_costo', 'cont_moneda', 'cont_tipo_cambio', 'cont_tipo_asiento', 'cont_asiento_contable',
    'cont_detalle_asiento', 'cont_libro_mayor', 'cont_activo_fijo', 'cont_depreciacion', 'cont_tipo_inventario',
    'cont_inventario', 'cont_provision', 'cont_activo_intangible', 'cont_instrumento_financiero', 'cont_impuesto_diferido'
]

def disable_rls():
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Disabling RLS for critical tables...")
        for table in tables_to_disable_rls:
            try:
                cur.execute(f'ALTER TABLE "{table}" DISABLE ROW LEVEL SECURITY;')
                print(f"SUCCESS: RLS Disabled for table: {table}")
            except Exception as e:
                print(f"WARNING: Could not disable RLS for {table}: {e}")
                
        cur.close()
        conn.close()
        print("\nRLS process completed.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    disable_rls()

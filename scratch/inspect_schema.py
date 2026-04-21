import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get('DIRECT_URL')

def inspect_schema():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        print("--- Table: cont_ejercicio_fiscal ---")
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'cont_ejercicio_fiscal'
            ORDER BY ordinal_position
        """)
        for r in cur.fetchall():
            print(f"Column: {r[0]}, Type: {r[1]}, Nullable: {r[2]}, Default: {r[3]}")
            
        print("\n--- Constraints: cont_ejercicio_fiscal ---")
        cur.execute("""
            SELECT conname, pg_get_constraintdef(c.oid)
            FROM pg_constraint c
            JOIN pg_namespace n ON n.oid = c.connamespace
            WHERE conrelid = 'cont_ejercicio_fiscal'::regclass;
        """)
        for r in cur.fetchall():
            print(f"Name: {r[0]}, Def: {r[1]}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    inspect_schema()

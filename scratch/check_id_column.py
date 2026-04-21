import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get('DIRECT_URL')

def check_id_column():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        print("--- ID Column Check: cont_ejercicio_fiscal ---")
        cur.execute("""
            SELECT column_name, is_identity, identity_generation, column_default
            FROM information_schema.columns 
            WHERE table_name = 'cont_ejercicio_fiscal' AND column_name = 'id'
        """)
        r = cur.fetchone()
        if r:
            print(f"Column: {r[0]}, Is Identity: {r[1]}, Generation: {r[2]}, Default: {r[3]}")
        else:
            print("id column NOT FOUND in information_schema.columns")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_id_column()

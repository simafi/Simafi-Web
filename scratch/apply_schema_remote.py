import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get('DIRECT_URL')

def apply_sql(sql_file):
    if not db_url:
        print("ERROR: DIRECT_URL not found in environment.")
        return

    try:
        print(f"Connecting to Supabase to apply {sql_file}...")
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read()
            
        print("Executing SQL script...")
        cur.execute(sql)
        print("SUCCESS: SQL script applied correctly.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    import sys
    sql_file = sys.argv[1] if len(sys.argv) > 1 else r'c:\simafiweb\scratch\contabilidad_schema.sql'
    apply_sql(sql_file)

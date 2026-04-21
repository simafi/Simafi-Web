import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get('DIRECT_URL')

def list_exercises():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT anio, empresa, descripcion FROM cont_ejercicio_fiscal")
        rows = cur.fetchall()
        print(f"Total exercises: {len(rows)}")
        for r in rows:
            print(f"Año: {r[0]}, Empresa: {r[1]}, Desc: {r[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    list_exercises()

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get('DIRECT_URL')

def check_policies():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check policies for negocios and negocio tables
        query = """
        SELECT schemaname, tablename, policyname, roles, cmd, qual, with_check 
        FROM pg_policies 
        WHERE tablename IN ('negocios', 'negocio', 'actividad', 'oficina', 'pagovariostemp');
        """
        cur.execute(query)
        policies = cur.fetchall()
        
        print("Policies:")
        if not policies:
            print("No policies found for these tables.")
        for p in policies:
            print(f"Table: {p[1]}, Policy: {p[2]}, Command: {p[4]}, Roles: {p[3]}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_policies()

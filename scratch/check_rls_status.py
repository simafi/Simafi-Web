import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get('DIRECT_URL')

def check_rls():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check tables RLS status
        query = """
        SELECT tablename, relrowsecurity 
        FROM pg_tables t
        JOIN pg_class c ON c.relname = t.tablename
        WHERE schemaname = 'public';
        """
        cur.execute(query)
        tables = cur.fetchall()
        
        print("Table RLS Status:")
        for table, rls_enabled in tables:
            print(f"Table: {table}, RLS Enabled: {rls_enabled}")
            
        # Check current user permissions
        cur.execute("SELECT current_user;")
        user = cur.fetchone()[0]
        print(f"\nCurrent User: {user}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_rls()

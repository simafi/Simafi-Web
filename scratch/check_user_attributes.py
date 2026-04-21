import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get('DIRECT_URL')

def check_user_attributes():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check current user attributes
        query = "SELECT rolname, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolcanlogin, rolbypassrls FROM pg_roles WHERE rolname = current_user;"
        cur.execute(query)
        user_info = cur.fetchone()
        
        if user_info:
            print(f"User: {user_info[0]}")
            print(f"Superuser: {user_info[1]}")
            print(f"Bypass RLS: {user_info[6]}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_user_attributes()

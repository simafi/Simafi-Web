import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get('DIRECT_URL')

def check_tables():
    if not db_url:
        print("ERROR: DIRECT_URL not found.")
        return

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check for cont_* tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'cont_%'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"Tables found: {len(tables)}")
        for t in sorted(tables):
            print(f" - {t}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_tables()

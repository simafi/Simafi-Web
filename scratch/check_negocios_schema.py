import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get('DIRECT_URL')

def check_schema():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check columns for 'negocios' table
        query = """
        SELECT column_name, data_type, character_maximum_length, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'negocios'
        ORDER BY ordinal_position;
        """
        cur.execute(query)
        columns = cur.fetchall()
        
        print("Schema for 'negocios':")
        if not columns:
            print("Table 'negocios' NOT FOUND!")
        for col in columns:
            print(f"Column: {col[0]}, Type: {col[1]}, Length: {col[2]}, Nullable: {col[3]}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_schema()

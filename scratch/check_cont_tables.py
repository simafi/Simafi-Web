import os
import django
import sys

# Añadir el backend al path
sys.path.append(r'c:\simafiweb\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catastro.config.settings')
django.setup()

from django.db import connection

def list_tables():
    print("Listing tables in the current database...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'cont_%';")
        tables = cursor.fetchall()
        print(f"Found {len(tables)} tables starting with 'cont_':")
        for table in tables:
            print(f"- {table[0]}")
            
        # Check RLS
        cursor.execute("SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'cont_%';")
        rls_status = cursor.fetchall()
        print("\nRLS Status for 'cont_' tables:")
        for table, rls in rls_status:
            print(f"- {table}: {'Enabled' if rls else 'Disabled'}")

if __name__ == "__main__":
    list_tables()

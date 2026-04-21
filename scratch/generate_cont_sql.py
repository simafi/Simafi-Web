import os
import sys
import django
from io import StringIO
from django.core.management import call_command

# Añadir el backend al path
sys.path.append(r'c:\simafiweb\backend')
sys.path.append(r'c:\simafiweb\backend\tributario')

# Usar el settings de tributario_app que es el más completo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

def generate_sql():
    print("Generating SQL for contabilidad migrations...")
    out = StringIO()
    migrations = ['0001', '0002', '0003']
    all_sql = []
    
    for m in migrations:
        try:
            print(f"Migrating {m}...")
            call_command('sqlmigrate', 'contabilidad', m, stdout=out)
            all_sql.append(f"-- MIGRATION {m}\n" + out.getvalue())
            out.truncate(0)
            out.seek(0)
        except Exception as e:
            print(f"Error in migration {m}: {str(e)}")
            
    with open(r'c:\simafiweb\scratch\contabilidad_schema.sql', 'w', encoding='utf-8') as f:
        f.write("\n".join(all_sql))
        
    print(f"SQL saved to c:\\simafiweb\\scratch\\contabilidad_schema.sql")

if __name__ == "__main__":
    generate_sql()

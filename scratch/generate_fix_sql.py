import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get('DIRECT_URL')

def get_cont_tables():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'cont_%'")
        tables = [t[0] for t in cur.fetchall()]
        cur.close()
        conn.close()
        return tables
    except Exception as e:
        print(f"ERROR: {e}")
        return []

def generate_alter_script():
    tables = get_cont_tables()
    lines = []
    lines.append("-- SQL Script to fix defaults and identities for Contabilidad tables")
    lines.append("BEGIN;")
    
    for table in tables:
        lines.append(f"\n-- Fixing table: {table}")
        
        # 1. Primary Key Sequence Fix
        # Create sequence if none exists and set as default for id
        seq_name = f"{table}_id_seq"
        lines.append(f"CREATE SEQUENCE IF NOT EXISTS \"{seq_name}\";")
        lines.append(f"ALTER TABLE \"{table}\" ALTER COLUMN \"id\" SET DEFAULT nextval('\"{seq_name}\"');")
        lines.append(f"ALTER SEQUENCE \"{seq_name}\" OWNED BY \"{table}\".\"id\";")
        # Ensure the sequence starts after any existing records (though currently 0)
        lines.append(f"SELECT setval('\"{seq_name}\"', COALESCE(max(\"id\"), 0) + 1, false) FROM \"{table}\";")
        
        # 2. Defaults for audit fields
        lines.append(f"ALTER TABLE \"{table}\" ALTER COLUMN \"created_at\" SET DEFAULT now();")
        lines.append(f"ALTER TABLE \"{table}\" ALTER COLUMN \"updated_at\" SET DEFAULT now();")
        lines.append(f"ALTER TABLE \"{table}\" ALTER COLUMN \"is_active\" SET DEFAULT true;")
        
    if 'cont_ejercicio_fiscal' in tables:
        lines.append("\n-- Fixing EjercicioFiscal uniqueness (Idempotent)")
        lines.append("ALTER TABLE \"cont_ejercicio_fiscal\" DROP CONSTRAINT IF EXISTS \"cont_ejercicio_fiscal_anio_key\";")
        lines.append("DO $$")
        lines.append("BEGIN")
        lines.append("    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cont_ejercicio_fiscal_anio_empresa_uniq') THEN")
        lines.append("        ALTER TABLE \"cont_ejercicio_fiscal\" ADD CONSTRAINT \"cont_ejercicio_fiscal_anio_empresa_uniq\" UNIQUE (\"anio\", \"empresa\");")
        lines.append("    END IF;")
        lines.append("END $$;")
        
    lines.append("\nCOMMIT;")
    return "\n".join(lines)

if __name__ == "__main__":
    script = generate_alter_script()
    output_file = os.path.join('scratch', 'fix_schema.sql')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script)
    print(f"SUCCESS: SQL script generated at {output_file}")

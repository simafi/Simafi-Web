import sys
import psycopg2

# Usar DIRECT_URL para verificacion (psycopg2 no soporta pgbouncer=true en DSN)
DATABASE_URL = "postgresql://postgres.inzasugoozqqnelcvrwd:Sandres0318$$@aws-1-us-west-2.pooler.supabase.com:5432/postgres"

def main():
    print("Verificando tabla cdd_solicitud_tramite en Supabase...")
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=20, sslmode="require")
        cur = conn.cursor()

        # Verificar que la tabla existe y es accesible
        cur.execute("SELECT COUNT(*) FROM cdd_solicitud_tramite WHERE is_active = TRUE")
        count = cur.fetchone()[0]
        print(f"  OK - Registros activos: {count}")

        # Verificar todas las columnas clave
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'cdd_solicitud_tramite'
            ORDER BY ordinal_position
        """)
        cols = [r[0] for r in cur.fetchall()]
        print(f"  Columnas ({len(cols)}): {', '.join(cols)}")

        # Verificar indices
        cur.execute("SELECT indexname FROM pg_indexes WHERE tablename = 'cdd_solicitud_tramite'")
        idxs = [r[0] for r in cur.fetchall()]
        print(f"  Indices: {', '.join(idxs)}")

        # Verificar migraciones
        cur.execute("SELECT name FROM django_migrations WHERE app='ciudadano' ORDER BY id")
        migs = [r[0] for r in cur.fetchall()]
        print(f"  Migraciones Django registradas: {migs}")

        conn.close()
        print("\nTODO OK - La tabla esta lista. El formulario deberia funcionar en produccion.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

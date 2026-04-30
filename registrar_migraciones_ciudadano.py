import sys
import psycopg2

DATABASE_URL = "postgresql://postgres.inzasugoozqqnelcvrwd:Sandres0318$$@aws-1-us-west-2.pooler.supabase.com:5432/postgres"

MIGRACIONES = [
    ("ciudadano", "0001_initial"),
    ("ciudadano", "0002_solicitud_respuesta_municipal"),
    ("ciudadano", "0003_solicitud_adjunto_notificaciones"),
]

def main():
    print("Conectando a Supabase...")
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=20, sslmode="require")
    conn.autocommit = True
    cur = conn.cursor()
    print("  Conectado OK")

    # Verificar estructura de django_migrations
    print("\nEstructura de django_migrations:")
    cur.execute("SELECT column_name, column_default FROM information_schema.columns WHERE table_name='django_migrations' ORDER BY ordinal_position")
    for row in cur.fetchall():
        print(f"  {row[0]}: default={row[1]}")

    # Insertar con id explicito usando NEXTVAL o SEQUENCE
    print("\nRegistrando migraciones...")
    for app, name in MIGRACIONES:
        try:
            # Verificar si ya existe
            cur.execute("SELECT COUNT(*) FROM django_migrations WHERE app=%s AND name=%s", (app, name))
            if cur.fetchone()[0] > 0:
                print(f"  Ya existe: {app}/{name}")
                continue
            # Obtener el proximo id
            cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM django_migrations")
            next_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO django_migrations (id, app, name, applied) VALUES (%s, %s, %s, NOW())",
                (next_id, app, name)
            )
            print(f"  Insertado id={next_id}: {app}/{name}")
        except Exception as e:
            print(f"  ERROR {name}: {e}")

    # Estado final
    print("\nVerificando migraciones ciudadano:")
    cur.execute("SELECT id, app, name, applied FROM django_migrations WHERE app='ciudadano' ORDER BY id")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}/{row[2]} -> {row[3]}")

    # Verificar tabla
    cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'cdd_solicitud_tramite'")
    cols = cur.fetchone()[0]
    print(f"\nColumnas en cdd_solicitud_tramite: {cols} (esperado: 21)")

    if cols >= 20:
        print("EXITO: La tabla esta lista. El formulario /ciudadano/solicitud/nueva/ deberia funcionar.")
    else:
        print("ADVERTENCIA: Pocas columnas. Revisar manualmente en Supabase.")

    conn.close()

if __name__ == "__main__":
    main()

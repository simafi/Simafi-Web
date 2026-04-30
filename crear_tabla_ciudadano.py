import sys

try:
    import psycopg2
except ImportError:
    print("Instalando psycopg2...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary", "-q"])
    import psycopg2

# Usar DIRECT_URL (puerto 5432) para DDL — no pgBouncer
DATABASE_URL = "postgresql://postgres.inzasugoozqqnelcvrwd:Sandres0318$$@aws-1-us-west-2.pooler.supabase.com:5432/postgres"

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS cdd_solicitud_tramite (
    id              BIGSERIAL PRIMARY KEY,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    empresa         VARCHAR(10) NOT NULL,
    tipo_tramite    VARCHAR(30) NOT NULL,
    identificacion  VARCHAR(20) NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    telefono        VARCHAR(40),
    email           VARCHAR(254),
    numero_expediente_negocio VARCHAR(40),
    detalle         TEXT NOT NULL,
    estado          VARCHAR(20) NOT NULL DEFAULT 'RECIBIDA',
    referencia      VARCHAR(24) NOT NULL,
    respuesta_municipal   TEXT NOT NULL DEFAULT '',
    fecha_respuesta       TIMESTAMPTZ,
    funcionario_respuesta VARCHAR(200) NOT NULL DEFAULT '',
    nota_interna          TEXT NOT NULL DEFAULT '',
    archivo_respuesta     VARCHAR(200),
    fecha_envio_correo    TIMESTAMPTZ,
    fecha_envio_whatsapp  TIMESTAMPTZ,
    CONSTRAINT cdd_solicitud_tramite_referencia_key UNIQUE (referencia)
);
"""

INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_cdd_sol_empresa ON cdd_solicitud_tramite (empresa);",
    "CREATE INDEX IF NOT EXISTS idx_cdd_sol_empresa_identif ON cdd_solicitud_tramite (empresa, identificacion);",
    "CREATE INDEX IF NOT EXISTS idx_cdd_sol_estado ON cdd_solicitud_tramite (estado);",
    "CREATE INDEX IF NOT EXISTS idx_cdd_sol_is_active ON cdd_solicitud_tramite (is_active);",
]

TRIGGER_FUNC = """
CREATE OR REPLACE FUNCTION update_cdd_solicitud_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

TRIGGER = """
DROP TRIGGER IF EXISTS trg_cdd_solicitud_updated_at ON cdd_solicitud_tramite;
CREATE TRIGGER trg_cdd_solicitud_updated_at
    BEFORE UPDATE ON cdd_solicitud_tramite
    FOR EACH ROW EXECUTE FUNCTION update_cdd_solicitud_updated_at();
"""

MIGRACIONES = [
    ("ciudadano", "0001_initial"),
    ("ciudadano", "0002_solicitud_respuesta_municipal"),
    ("ciudadano", "0003_solicitud_adjunto_notificaciones"),
]

def main():
    print("Conectando a Supabase...")
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=20, sslmode="require")
        conn.autocommit = True
        cur = conn.cursor()
        print("  Conectado OK")
    except Exception as e:
        print(f"  ERROR conectando: {e}")
        sys.exit(1)

    # Crear tabla
    print("\nCreando tabla cdd_solicitud_tramite...")
    try:
        cur.execute(SQL_CREATE)
        print("  Tabla creada (o ya existia)")
    except Exception as e:
        print(f"  ERROR creando tabla: {e}")
        conn.close()
        sys.exit(1)

    # Crear indices
    print("\nCreando indices...")
    for idx_sql in INDICES:
        try:
            cur.execute(idx_sql)
            print(f"  OK: {idx_sql[:60]}...")
        except Exception as e:
            print(f"  WARN indices: {e}")

    # Trigger updated_at
    print("\nCreando trigger updated_at...")
    try:
        cur.execute(TRIGGER_FUNC)
        cur.execute(TRIGGER)
        print("  Trigger creado OK")
    except Exception as e:
        print(f"  WARN trigger: {e}")

    # Registrar migraciones Django
    print("\nRegistrando migraciones Django...")
    for app, name in MIGRACIONES:
        try:
            cur.execute(
                "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW()) ON CONFLICT DO NOTHING",
                (app, name)
            )
            print(f"  OK: {app} / {name}")
        except Exception as e:
            print(f"  WARN migracion {name}: {e}")

    # Verificar
    print("\nVerificando tabla...")
    cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'cdd_solicitud_tramite'")
    cols = cur.fetchone()[0]
    print(f"  Columnas en cdd_solicitud_tramite: {cols}")

    if cols >= 20:
        print("\n✅ EXITO: La tabla tiene todas las columnas necesarias.")
        print("   El formulario /ciudadano/solicitud/nueva/ deberia funcionar ahora.")
    else:
        print(f"\n⚠️  Solo {cols} columnas detectadas. Revisar manualmente.")

    conn.close()

if __name__ == "__main__":
    main()

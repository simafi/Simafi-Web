-- ============================================================
-- CREAR TABLA cdd_solicitud_tramite en Supabase
-- Módulo: Portal Ciudadano (ciudadano)
-- Ejecutar en: Supabase SQL Editor
-- ============================================================

-- 1. Tabla principal de solicitudes
CREATE TABLE IF NOT EXISTS cdd_solicitud_tramite (
    id              BIGSERIAL PRIMARY KEY,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    -- Datos del municipio/empresa
    empresa         VARCHAR(10) NOT NULL,

    -- Datos del trámite
    tipo_tramite    VARCHAR(30) NOT NULL,
    identificacion  VARCHAR(20) NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    telefono        VARCHAR(40),
    email           VARCHAR(254),
    numero_expediente_negocio VARCHAR(40),
    detalle         TEXT NOT NULL,

    -- Estado y folio
    estado          VARCHAR(20) NOT NULL DEFAULT 'RECIBIDA',
    referencia      VARCHAR(24) NOT NULL UNIQUE,

    -- Respuesta municipal
    respuesta_municipal  TEXT NOT NULL DEFAULT '',
    fecha_respuesta      TIMESTAMPTZ,
    funcionario_respuesta VARCHAR(200) NOT NULL DEFAULT '',
    nota_interna         TEXT NOT NULL DEFAULT '',

    -- Adjunto y notificaciones
    archivo_respuesta    VARCHAR(200),
    fecha_envio_correo   TIMESTAMPTZ,
    fecha_envio_whatsapp TIMESTAMPTZ
);

-- 2. Índices útiles para búsqueda por empresa e identificación
CREATE INDEX IF NOT EXISTS idx_cdd_sol_empresa
    ON cdd_solicitud_tramite (empresa);

CREATE INDEX IF NOT EXISTS idx_cdd_sol_empresa_identif
    ON cdd_solicitud_tramite (empresa, identificacion);

CREATE INDEX IF NOT EXISTS idx_cdd_sol_estado
    ON cdd_solicitud_tramite (estado);

CREATE INDEX IF NOT EXISTS idx_cdd_sol_is_active
    ON cdd_solicitud_tramite (is_active);

-- 3. Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_cdd_solicitud_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_cdd_solicitud_updated_at ON cdd_solicitud_tramite;
CREATE TRIGGER trg_cdd_solicitud_updated_at
    BEFORE UPDATE ON cdd_solicitud_tramite
    FOR EACH ROW EXECUTE FUNCTION update_cdd_solicitud_updated_at();

-- 4. Registro de migración en django_migrations (para evitar conflictos con las migraciones Django)
INSERT INTO django_migrations (app, name, applied)
VALUES
    ('ciudadano', '0001_initial',                         NOW()),
    ('ciudadano', '0002_solicitud_respuesta_municipal',    NOW()),
    ('ciudadano', '0003_solicitud_adjunto_notificaciones', NOW())
ON CONFLICT DO NOTHING;

-- Verificación final
SELECT 'TABLA CREADA OK' AS resultado, COUNT(*) AS columnas
FROM information_schema.columns
WHERE table_name = 'cdd_solicitud_tramite';

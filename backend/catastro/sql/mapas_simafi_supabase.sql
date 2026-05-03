-- =============================================================================
-- Mapas Simafi: tablas PostgreSQL / Supabase (equiv. Django catastro 0020_mapas_simafi).
--
-- Un solo paso en Supabase: Dashboard -> SQL Editor -> pegar ESTE archivo completo -> Run.
--
-- O desde PC (carpeta backend): DATABASE_URL en .env.supabase_prod (raiz repo) y:
--   python catastro/scripts/apply_mapas_sql.py
--   .\crear_tablas_mapas_supabase.ps1
--
-- Requisito: no deben existir ya estas tablas con otro esquema incompatible.
-- =============================================================================

BEGIN;

CREATE TABLE IF NOT EXISTS catastro_mapa_proyecto (
    id BIGSERIAL PRIMARY KEY,
    empresa VARCHAR(4) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    srid INTEGER NOT NULL DEFAULT 4326 CHECK (srid >= 0),
    usuario_creacion VARCHAR(80) NOT NULL DEFAULT '',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS catastro_mapa_proj_emp_act
    ON catastro_mapa_proyecto (empresa, activo);

CREATE TABLE IF NOT EXISTS catastro_mapa_capa (
    id BIGSERIAL PRIMARY KEY,
    proyecto_id BIGINT NOT NULL REFERENCES catastro_mapa_proyecto (id) ON DELETE CASCADE,
    nombre VARCHAR(120) NOT NULL,
    orden SMALLINT NOT NULL DEFAULT 0 CHECK (orden >= 0),
    color_linea VARCHAR(32) NOT NULL DEFAULT '#2563eb',
    color_relleno VARCHAR(32) NOT NULL DEFAULT '#2563eb',
    opacidad_relleno DOUBLE PRECISION NOT NULL DEFAULT 0.25,
    visible BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS catastro_mapa_elemento (
    id BIGSERIAL PRIMARY KEY,
    capa_id BIGINT NOT NULL REFERENCES catastro_mapa_capa (id) ON DELETE CASCADE,
    etiqueta VARCHAR(200) NOT NULL DEFAULT '',
    geometria JSONB NOT NULL,
    propiedades JSONB NOT NULL DEFAULT '{}'::jsonb,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS catastro_mapa_elem_capa
    ON catastro_mapa_elemento (capa_id);

COMMIT;

-- -----------------------------------------------------------------------------
-- Opcional: si en el mismo proyecto usás `manage.py migrate` con la app
-- `catastro` y Django intentara volver a aplicar 0020, podrías registrar la
-- migración (solo si entendés el estado de django_migrations de tu proyecto):
--
-- INSERT INTO django_migrations (app, name, applied)
-- SELECT 'catastro', '0020_mapas_simafi', NOW()
-- WHERE NOT EXISTS (
--     SELECT 1 FROM django_migrations
--     WHERE app = 'catastro' AND name = '0020_mapas_simafi'
-- );
-- -----------------------------------------------------------------------------

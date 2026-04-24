# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ciudadano", "0003_solicitud_adjunto_notificaciones"),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
            DO $$
            DECLARE
              _tbl text := 'cdd_solicitud_tramite';
              _col text := 'id';
              _seq text;
              _has_default boolean;
              _is_identity text;
            BEGIN
              SELECT c.column_default IS NOT NULL, c.is_identity
                INTO _has_default, _is_identity
              FROM information_schema.columns c
              WHERE c.table_schema='public'
                AND c.table_name=_tbl
                AND c.column_name=_col;

              -- Si ya es IDENTITY o ya tiene default, no tocar.
              IF COALESCE(_is_identity, 'NO') = 'YES' OR _has_default THEN
                RETURN;
              END IF;

              -- Asegurar secuencia estándar y default nextval
              _seq := format('%s_%s_seq', _tbl, _col);

              EXECUTE format('CREATE SEQUENCE IF NOT EXISTS %I', _seq);
              EXECUTE format('ALTER SEQUENCE %I OWNED BY %I.%I', _seq, _tbl, _col);
              EXECUTE format('ALTER TABLE %I ALTER COLUMN %I SET DEFAULT nextval(%L)', _tbl, _col, _seq);

              -- Sincronizar con el máximo id existente (si hay filas importadas)
              EXECUTE format(
                'SELECT setval(%L, GREATEST(1, COALESCE(MAX(%I),0)), true) FROM %I',
                _seq, _col, _tbl
              );
            END $$;
            """,
            reverse_sql=r"""
            -- No revertimos: quitar default/sequence puede romper inserts.
            """,
        )
    ]


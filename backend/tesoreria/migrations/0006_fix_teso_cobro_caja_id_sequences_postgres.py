from django.db import migrations


def fix_teso_cobro_caja_sequences(apps, schema_editor):
    """Postgres/Supabase: secuencias para id en teso_cobro_caja y teso_cobro_caja_metodo."""
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            DO $fix$
            DECLARE
                max_id bigint;
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'teso_cobro_caja'
                ) THEN
                    CREATE SEQUENCE IF NOT EXISTS public.teso_cobro_caja_id_seq AS bigint;
                    SELECT COALESCE(MAX(id), 0) INTO max_id FROM public.teso_cobro_caja;
                    IF max_id = 0 THEN
                        PERFORM setval('public.teso_cobro_caja_id_seq', 1, false);
                    ELSE
                        PERFORM setval('public.teso_cobro_caja_id_seq', max_id, true);
                    END IF;
                    ALTER TABLE public.teso_cobro_caja
                        ALTER COLUMN id SET DEFAULT nextval(
                            'public.teso_cobro_caja_id_seq'::regclass
                        );
                    ALTER SEQUENCE public.teso_cobro_caja_id_seq OWNED BY public.teso_cobro_caja.id;
                END IF;
            END
            $fix$;
            """
        )
        cursor.execute(
            """
            DO $fix2$
            DECLARE
                max_id bigint;
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'teso_cobro_caja_metodo'
                ) THEN
                    CREATE SEQUENCE IF NOT EXISTS public.teso_cobro_caja_metodo_id_seq AS bigint;
                    SELECT COALESCE(MAX(id), 0) INTO max_id FROM public.teso_cobro_caja_metodo;
                    IF max_id = 0 THEN
                        PERFORM setval('public.teso_cobro_caja_metodo_id_seq', 1, false);
                    ELSE
                        PERFORM setval('public.teso_cobro_caja_metodo_id_seq', max_id, true);
                    END IF;
                    ALTER TABLE public.teso_cobro_caja_metodo
                        ALTER COLUMN id SET DEFAULT nextval(
                            'public.teso_cobro_caja_metodo_id_seq'::regclass
                        );
                    ALTER SEQUENCE public.teso_cobro_caja_metodo_id_seq OWNED BY public.teso_cobro_caja_metodo.id;
                END IF;
            END
            $fix2$;
            """
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tesoreria", "0005_cobrocaja_cobrocajametodo"),
    ]

    operations = [
        migrations.RunPython(fix_teso_cobro_caja_sequences, noop_reverse),
    ]

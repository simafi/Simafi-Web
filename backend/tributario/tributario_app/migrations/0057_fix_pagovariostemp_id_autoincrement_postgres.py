from django.db import migrations


def fix_pagovariostemp_id_sequence(apps, schema_editor):
    """Supabase/Postgres: asegura que `pagovariostemp.id` tenga secuencia (autoincrement)."""
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            DO $fix$
            DECLARE
                max_id bigint;
            BEGIN
                CREATE SEQUENCE IF NOT EXISTS public.pagovariostemp_id_seq AS bigint;

                SELECT COALESCE(MAX(id), 0) INTO max_id FROM public.pagovariostemp;

                IF max_id = 0 THEN
                    PERFORM setval('public.pagovariostemp_id_seq', 1, false);
                ELSE
                    PERFORM setval('public.pagovariostemp_id_seq', max_id, true);
                END IF;

                ALTER TABLE public.pagovariostemp
                    ALTER COLUMN id SET DEFAULT nextval(
                        'public.pagovariostemp_id_seq'::regclass
                    );

                ALTER SEQUENCE public.pagovariostemp_id_seq OWNED BY public.pagovariostemp.id;
            END
            $fix$;
            """
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tributario_app", "0056_state_sync_declara_transaccionesics"),
    ]

    operations = [
        migrations.RunPython(fix_pagovariostemp_id_sequence, noop_reverse),
    ]

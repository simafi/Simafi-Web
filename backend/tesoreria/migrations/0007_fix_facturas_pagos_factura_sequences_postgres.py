# Generated manually — secuencias de id desfasadas tras import (duplicate key en resumen caja).

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tesoreria", "0006_fix_teso_cobro_caja_id_sequences_postgres"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
DO $$
DECLARE
  mx bigint;
  seq text;
BEGIN
  IF to_regclass('public.facturas') IS NOT NULL THEN
    seq := pg_get_serial_sequence('public.facturas', 'id');
    IF seq IS NOT NULL THEN
      SELECT COALESCE(MAX(id), 0) INTO mx FROM public.facturas;
      IF mx <= 0 THEN
        PERFORM setval(seq::regclass, 1, false);
      ELSE
        PERFORM setval(seq::regclass, mx, true);
      END IF;
    END IF;
  END IF;
  IF to_regclass('public.pagos_factura') IS NOT NULL THEN
    seq := pg_get_serial_sequence('public.pagos_factura', 'id');
    IF seq IS NOT NULL THEN
      SELECT COALESCE(MAX(id), 0) INTO mx FROM public.pagos_factura;
      IF mx <= 0 THEN
        PERFORM setval(seq::regclass, 1, false);
      ELSE
        PERFORM setval(seq::regclass, mx, true);
      END IF;
    END IF;
  END IF;
END $$;
""",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

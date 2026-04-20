# -*- coding: utf-8 -*-
from django.db import migrations, models


def _rellenar_fecha_compra(apps, schema_editor):
    MovimientoBodega = apps.get_model("compras", "MovimientoBodega")
    for m in MovimientoBodega.objects.filter(fecha_compra__isnull=True).only("id", "fecha"):
        m.fecha_compra = m.fecha
        m.save(update_fields=["fecha_compra"])


class Migration(migrations.Migration):

    dependencies = [
        ("compras", "0004_solicitud_cotizacion_detalle_oncae"),
    ]

    operations = [
        migrations.AddField(
            model_name="movimientobodega",
            name="fecha_compra",
            field=models.DateField(
                blank=True,
                help_text="Fecha del documento de compra o factura del proveedor.",
                null=True,
                verbose_name="Fecha de la compra",
            ),
        ),
        migrations.AlterField(
            model_name="movimientobodega",
            name="fecha",
            field=models.DateField(
                help_text="Fecha en que se registra el movimiento en kardex (puede ser distinta a la fecha de la compra).",
                verbose_name="Fecha de registro en bodega",
            ),
        ),
        migrations.RunPython(_rellenar_fecha_compra, migrations.RunPython.noop),
    ]

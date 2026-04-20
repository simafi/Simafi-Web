# Generated manually for SIMAFI — tipo de inventario y nomenclatura (bodega / catálogo)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contabilidad", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventario",
            name="tipo_inventario",
            field=models.CharField(
                choices=[
                    ("MATERIA_PRIMA", "Materia prima e insumos"),
                    ("SUMINISTROS", "Suministros de oficina y operación"),
                    ("REPUESTOS", "Repuestos y accesorios"),
                    ("MERCADERIA", "Mercadería para reventa"),
                    ("PRODUCTO_TERMINADO", "Producto terminado"),
                    ("EMBALAJE", "Embalajes y envases"),
                    ("SERVICIOS_ALMACENADOS", "Servicios almacenables / pendientes"),
                    ("OTROS", "Otros / diversos"),
                ],
                default="OTROS",
                help_text="Clasificación del bien para bodega, informes y políticas de abastecimiento.",
                max_length=30,
                verbose_name="Tipo de inventario",
            ),
        ),
        migrations.AddField(
            model_name="inventario",
            name="nomenclatura",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Código de catálogo (p. ej. UNSPSC, CPV u homologación interna) para estandarizar el material.",
                max_length=120,
                verbose_name="Nomenclatura / clasificación del material",
            ),
        ),
    ]

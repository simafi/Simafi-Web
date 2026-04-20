# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrativo_main", "0003_alter_proveedor_nit_verbose_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proveedor",
            name="nit",
            field=models.CharField(
                blank=True,
                default="",
                max_length=20,
                verbose_name="RTN / DNI / NIT",
            ),
        ),
    ]

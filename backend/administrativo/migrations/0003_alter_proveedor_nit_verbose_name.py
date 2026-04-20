# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrativo_main", "0002_adm_gestion_models"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proveedor",
            name="nit",
            field=models.CharField(
                blank=True,
                default="",
                max_length=20,
                verbose_name="RTN / DNI",
            ),
        ),
    ]

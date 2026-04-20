# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ciudadano", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="solicitudtramite",
            name="respuesta_municipal",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Texto visible para el ciudadano en el portal cuando se registre.",
                verbose_name="Respuesta oficial al contribuyente",
            ),
        ),
        migrations.AddField(
            model_name="solicitudtramite",
            name="fecha_respuesta",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Fecha y hora de la respuesta"),
        ),
        migrations.AddField(
            model_name="solicitudtramite",
            name="funcionario_respuesta",
            field=models.CharField(
                blank=True,
                default="",
                max_length=200,
                verbose_name="Funcionario que responde",
            ),
        ),
        migrations.AddField(
            model_name="solicitudtramite",
            name="nota_interna",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Uso administrativo: seguimiento, archivo o instrucciones internas.",
                verbose_name="Nota interna (no visible al ciudadano)",
            ),
        ),
    ]

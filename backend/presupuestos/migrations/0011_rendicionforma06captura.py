# Forma 06 — Arqueo Caja Chica / Fondo rotatorio (declaración y firmas)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("presupuestos", "0010_rendicionforma05ajuste_salidamanual"),
    ]

    operations = [
        migrations.CreateModel(
            name="RendicionForma06Captura",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                (
                    "municipal_arqueo_nombre",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=200,
                        verbose_name="Municipal que realiza el arqueo (nombre completo)",
                    ),
                ),
                (
                    "empleado_municipal_nombre",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=200,
                        verbose_name="Empleado(a) Municipal que realiza el arqueo",
                    ),
                ),
                (
                    "responsable_nombre",
                    models.CharField(blank=True, default="", max_length=200, verbose_name="Responsable"),
                ),
                (
                    "numero_arqueo",
                    models.CharField(blank=True, max_length=50, null=True, verbose_name="No. de arqueo / acta"),
                ),
                (
                    "fecha_arqueo",
                    models.DateField(blank=True, null=True, verbose_name="Fecha del arqueo"),
                ),
                (
                    "ejercicio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rendicion_f06_capturas",
                        to="contabilidad.ejerciciofiscal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Rendición Forma 06 - Captura",
                "verbose_name_plural": "Rendición Forma 06 - Capturas",
                "db_table": "presu_rendicion_f06_captura",
                "unique_together": {("empresa", "ejercicio")},
            },
        ),
    ]

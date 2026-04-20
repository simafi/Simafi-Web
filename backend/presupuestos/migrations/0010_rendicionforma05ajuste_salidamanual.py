# Forma 05 — captura manual y ajustes

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("presupuestos", "0009_rendicionforma04ajuste"),
    ]

    operations = [
        migrations.CreateModel(
            name="RendicionForma05Ajuste",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                (
                    "extra_entradas_efectivo",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=18,
                        verbose_name="Ajuste entradas efectivo (cobros caja)",
                    ),
                ),
                (
                    "extra_salidas_efectivo",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=18,
                        verbose_name="Ajuste salidas efectivo (sumatoria)",
                    ),
                ),
                (
                    "extra_cheques",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=18,
                        verbose_name="Ajuste sumatoria cheques",
                    ),
                ),
                ("alcalde_nombre", models.CharField(blank=True, max_length=200, null=True)),
                ("tesorero_nombre", models.CharField(blank=True, max_length=200, null=True)),
                ("contador_nombre", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "ejercicio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rendicion_f05_ajustes",
                        to="contabilidad.ejerciciofiscal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Rendición Forma 05 - Ajustes",
                "verbose_name_plural": "Rendición Forma 05 - Ajustes",
                "db_table": "presu_rendicion_f05_ajuste",
                "unique_together": {("empresa", "ejercicio")},
            },
        ),
        migrations.CreateModel(
            name="RendicionForma05SalidaManual",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("fecha", models.DateField(verbose_name="Fecha del documento")),
                ("descripcion", models.CharField(max_length=500, verbose_name="Descripción")),
                (
                    "documento",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=80,
                        verbose_name="No. documento / referencia",
                    ),
                ),
                ("monto", models.DecimalField(decimal_places=2, max_digits=18, verbose_name="Valor")),
                ("orden", models.PositiveSmallIntegerField(default=0, verbose_name="Orden")),
                (
                    "ejercicio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rendicion_f05_salidas_manuales",
                        to="contabilidad.ejerciciofiscal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Rendición Forma 05 - Salida manual",
                "verbose_name_plural": "Rendición Forma 05 - Salidas manuales",
                "db_table": "presu_rendicion_f05_salida_manual",
                "ordering": ["orden", "fecha", "id"],
            },
        ),
    ]

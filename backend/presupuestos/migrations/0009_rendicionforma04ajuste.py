# Generated manually for Forma 04 ajustes

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("presupuestos", "0008_rendicionforma07ajuste"),
    ]

    operations = [
        migrations.CreateModel(
            name="RendicionForma04Ajuste",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                (
                    "ajuste_por_ingreso",
                    models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name="Ajuste por ingreso"),
                ),
                (
                    "ajuste_por_egreso",
                    models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name="Ajuste por egreso"),
                ),
                ("alcalde_nombre", models.CharField(blank=True, max_length=200, null=True)),
                ("tesorero_nombre", models.CharField(blank=True, max_length=200, null=True)),
                ("contador_nombre", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "ejercicio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rendicion_f04_ajustes",
                        to="contabilidad.ejerciciofiscal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Rendición Forma 04 - Ajustes",
                "verbose_name_plural": "Rendición Forma 04 - Ajustes",
                "db_table": "presu_rendicion_f04_ajuste",
                "unique_together": {("empresa", "ejercicio")},
            },
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("presupuestos", "0007_operacionmanual_delete_gastomanual"),
        ("contabilidad", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RendicionForma07Ajuste",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("entradas_extra_efectivo", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("entradas_extra_bancos", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("pagos_extra_efectivo", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("pagos_extra_bancos", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("alcalde_nombre", models.CharField(blank=True, max_length=200, null=True)),
                ("tesorero_nombre", models.CharField(blank=True, max_length=200, null=True)),
                ("contador_nombre", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "ejercicio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rendicion_f07_ajustes",
                        to="contabilidad.ejerciciofiscal",
                    ),
                ),
            ],
            options={
                "db_table": "presu_rendicion_f07_ajuste",
                "verbose_name": "Rendición Forma 07 - Ajustes",
                "verbose_name_plural": "Rendición Forma 07 - Ajustes",
                "unique_together": {("empresa", "ejercicio")},
            },
        ),
    ]


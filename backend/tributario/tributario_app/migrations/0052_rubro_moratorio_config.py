from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ("tributario_app", "0051_add_parametros_tributarios"),
    ]

    operations = [
        migrations.CreateModel(
            name="RubroMoratorioConfig",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("empresa", models.CharField(db_collation="utf8mb4_0900_ai_ci", default="", max_length=4, verbose_name="Empresa")),
                ("rubro_codigo", models.CharField(db_collation="utf8mb4_0900_ai_ci", default="", max_length=6, verbose_name="Rubro Moratorio")),
                ("rubro_padre_codigo", models.CharField(db_collation="utf8mb4_0900_ai_ci", default="", max_length=6, verbose_name="Rubro Padre")),
                ("tasa_recargo_mensual", models.DecimalField(decimal_places=4, default=Decimal("0.0000"), max_digits=7, verbose_name="Tasa Recargo Mensual (%)")),
                ("tasa_interes_mensual", models.DecimalField(decimal_places=4, default=Decimal("0.0000"), max_digits=7, verbose_name="Tasa Interés Mensual (%)")),
                (
                    "aplica_modulo",
                    models.CharField(
                        choices=[("BI", "Bienes Inmuebles"), ("ICS", "Negocios (ICS)"), ("AMBOS", "Ambos")],
                        default="AMBOS",
                        max_length=5,
                        verbose_name="Aplica a",
                    ),
                ),
                ("activo", models.BooleanField(default=True, verbose_name="Activo")),
                ("usuario_crea", models.CharField(blank=True, db_collation="latin1_swedish_ci", default="", max_length=50, verbose_name="Usuario crea")),
                ("fecha_crea", models.DateTimeField(auto_now_add=True)),
                ("usuario_modifica", models.CharField(blank=True, db_collation="latin1_swedish_ci", default="", max_length=50, verbose_name="Usuario modifica")),
                ("fecha_modifica", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "rubro_moratorio_config",
                "verbose_name": "Config Rubro Moratorio",
                "verbose_name_plural": "Config Rubros Moratorios",
            },
        ),
        migrations.AddConstraint(
            model_name="rubromoratorioconfig",
            constraint=models.UniqueConstraint(fields=("empresa", "rubro_codigo"), name="uniq_rubro_moratorio_por_empresa"),
        ),
        migrations.AddIndex(
            model_name="rubromoratorioconfig",
            index=models.Index(fields=["empresa", "rubro_padre_codigo"], name="idx_rubromora_emp_padre"),
        ),
        migrations.AddIndex(
            model_name="rubromoratorioconfig",
            index=models.Index(fields=["empresa", "rubro_codigo"], name="idx_rubromora_emp_rubro"),
        ),
    ]


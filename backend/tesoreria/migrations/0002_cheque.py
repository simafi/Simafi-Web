from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tesoreria", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cheque",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("numero", models.CharField(max_length=30, verbose_name="Número de cheque")),
                ("fecha", models.DateField(verbose_name="Fecha")),
                ("beneficiario", models.CharField(max_length=200, verbose_name="Beneficiario")),
                ("concepto", models.TextField(blank=True, null=True, verbose_name="Concepto")),
                ("monto_total", models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name="Monto total")),
                ("estado", models.CharField(choices=[("EMITIDO", "Emitido"), ("ANULADO", "Anulado")], default="EMITIDO", max_length=10)),
                ("cuenta_tesoreria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="cheques", to="tesoreria.cuentatesoreria", verbose_name="Cuenta de cheques")),
            ],
            options={
                "db_table": "teso_cheque",
                "verbose_name": "Cheque",
                "verbose_name_plural": "Cheques",
                "ordering": ["-fecha", "-numero"],
                "unique_together": {("empresa", "numero")},
            },
        ),
    ]


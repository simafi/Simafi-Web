from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):
    """
    Sincroniza el estado de Django con la BD legacy.
    No ejecuta DDL porque ya se aplicó vía migraciones defensivas (RunPython / SQL).
    """

    dependencies = [
        ("tributario_app", "0055_fix_declara_valor_base_default"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name="declaracionvolumen",
                    name="valor_base",
                    field=models.DecimalField(
                        max_digits=16,
                        decimal_places=2,
                        default=Decimal("0.00"),
                        verbose_name="Valor Base",
                        db_column="valor_base",
                    ),
                ),
                migrations.AddField(
                    model_name="transaccionesics",
                    name="vencimiento",
                    field=models.DateField(blank=True, null=True, verbose_name="Vencimiento"),
                ),
            ],
        )
    ]


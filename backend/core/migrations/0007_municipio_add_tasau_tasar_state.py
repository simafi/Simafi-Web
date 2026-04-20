# Campos tasau / tasar ya existen en MySQL; se actualiza solo el estado del modelo.

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_municipio_tasau_tasar'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='municipio',
                    name='tasau',
                    field=models.DecimalField(
                        blank=True,
                        db_column='tasau',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=7,
                        null=True,
                        verbose_name='Tasa urbana',
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='tasar',
                    field=models.DecimalField(
                        blank=True,
                        db_column='tasar',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=7,
                        null=True,
                        verbose_name='Tasa rural',
                    ),
                ),
                migrations.AlterField(
                    model_name='municipio',
                    name='fesqui',
                    field=models.DecimalField(
                        blank=True,
                        db_column='fesqui',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=5,
                        null=True,
                        verbose_name='Factor esquina',
                    ),
                ),
                migrations.AlterField(
                    model_name='municipio',
                    name='por_concer',
                    field=models.DecimalField(
                        db_column='por_concer',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=7,
                        verbose_name='Porcentaje de concertación',
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]

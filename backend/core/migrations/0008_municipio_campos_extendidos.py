# Columnas ya existen en MySQL; solo se actualiza el estado del modelo (managed=False).

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_municipio_add_tasau_tasar_state'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='municipio',
                    name='alcalde',
                    field=models.CharField(
                        blank=True, db_column='alcalde', max_length=50, null=True, verbose_name='Alcalde'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='auditor',
                    field=models.CharField(
                        blank=True, db_column='auditor', max_length=50, null=True, verbose_name='Auditor'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='presupuestos',
                    field=models.CharField(
                        blank=True, db_column='presupuestos', max_length=50, null=True, verbose_name='Presupuestos'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='contador',
                    field=models.CharField(
                        blank=True, db_column='contador', max_length=50, null=True, verbose_name='Contador'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='tesorero',
                    field=models.CharField(
                        blank=True, db_column='tesorero', max_length=50, null=True, verbose_name='Tesorero'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='secretario',
                    field=models.CharField(
                        blank=True, db_column='secretario', max_length=50, null=True, verbose_name='Secretario'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='proyecto',
                    field=models.CharField(
                        blank=True, db_column='proyecto', max_length=50, null=True, verbose_name='Proyecto'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='activo',
                    field=models.CharField(
                        blank=True, db_column='activo', max_length=7, null=True, verbose_name='Activo'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='financiero',
                    field=models.CharField(
                        blank=True, db_column='financiero', max_length=50, null=True, verbose_name='Financiero'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='tesorera',
                    field=models.CharField(
                        blank=True, db_column='tesorera', max_length=50, null=True, verbose_name='Tesorera'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='tributacion',
                    field=models.CharField(
                        blank=True,
                        db_column='tributacion',
                        default='',
                        max_length=100,
                        verbose_name='Tributación',
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='gerentefin',
                    field=models.CharField(
                        blank=True,
                        db_column='gerentefin',
                        max_length=100,
                        null=True,
                        verbose_name='Gerente financiero',
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='gerentegeneral',
                    field=models.CharField(
                        blank=True,
                        db_column='gerentegeneral',
                        max_length=100,
                        null=True,
                        verbose_name='Gerente general',
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='porce_condo1',
                    field=models.DecimalField(
                        blank=True,
                        db_column='porce_condo1',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=7,
                        null=True,
                        verbose_name='% condonación 1',
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='porce_condo2',
                    field=models.DecimalField(
                        blank=True,
                        db_column='porce_condo2',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=12,
                        null=True,
                        verbose_name='% condonación 2',
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='fecondona1',
                    field=models.DateField(
                        blank=True, db_column='fecondona1', null=True, verbose_name='Fecha condonación 1'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='fecondona2',
                    field=models.DateField(
                        blank=True, db_column='fecondona2', null=True, verbose_name='Fecha condonación 2'
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='interes',
                    field=models.DecimalField(
                        blank=True,
                        db_column='interes',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=7,
                        null=True,
                        verbose_name='Interés',
                    ),
                ),
                migrations.AddField(
                    model_name='municipio',
                    name='desc_tercera',
                    field=models.DecimalField(
                        blank=True,
                        db_column='desc_tercera',
                        decimal_places=2,
                        default=Decimal('0.00'),
                        max_digits=12,
                        null=True,
                        verbose_name='Descuento tercera',
                    ),
                ),
            ],
        ),
    ]

# Sustituye en el estado de migraciones los modelos genéricos Subuso/Topografia (codigo+descripcion)
# por CfgSubuso / CfgTopografia alineados a las columnas reales de MySQL.

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0005_catalogos_predio'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name='Subuso'),
                migrations.CreateModel(
                    name='CfgSubuso',
                    fields=[
                        ('id', models.AutoField(primary_key=True, serialize=False)),
                        ('uso', models.CharField(db_column='uso', max_length=3, verbose_name='Uso')),
                        (
                            'codsubuso',
                            models.CharField(
                                blank=True,
                                db_column='codsubuso',
                                max_length=5,
                                null=True,
                                verbose_name='Cód. subuso',
                            ),
                        ),
                        (
                            'descripcion',
                            models.CharField(db_column='des_subuso', max_length=34, verbose_name='Descripción'),
                        ),
                    ],
                    options={
                        'db_table': 'subuso',
                        'managed': False,
                        'ordering': ['uso', 'codsubuso'],
                        'verbose_name': 'Sub uso del predio',
                        'verbose_name_plural': 'Sub usos del predio',
                    },
                ),
                migrations.DeleteModel(name='Topografia'),
                migrations.CreateModel(
                    name='CfgTopografia',
                    fields=[
                        ('id', models.AutoField(primary_key=True, serialize=False)),
                        (
                            'empresa',
                            models.CharField(
                                blank=True,
                                db_column='empresa',
                                max_length=4,
                                null=True,
                                verbose_name='Empresa',
                            ),
                        ),
                        (
                            'cotopo',
                            models.CharField(db_column='cotopo', max_length=2, verbose_name='Cód. topografía'),
                        ),
                        (
                            'descritopo',
                            models.CharField(db_column='descritopo', max_length=40, verbose_name='Descripción'),
                        ),
                        (
                            'factopo',
                            models.DecimalField(
                                db_column='factopo',
                                decimal_places=2,
                                default=Decimal('0.00'),
                                max_digits=5,
                                verbose_name='Factor',
                            ),
                        ),
                    ],
                    options={
                        'db_table': 'topografia',
                        'managed': False,
                        'ordering': ['empresa', 'cotopo'],
                        'verbose_name': 'Topografía del predio',
                        'verbose_name_plural': 'Topografías del predio',
                    },
                ),
            ],
        ),
    ]

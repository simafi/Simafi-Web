# Estado de migraciones alineado con tablas legacy: PK = codigo, sin id, managed=False.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_departamento'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='Departamento'),
                migrations.CreateModel(
                    name='Departamento',
                    fields=[
                        (
                            'codigo',
                            models.CharField(
                                db_collation='latin1_swedish_ci',
                                default='',
                                max_length=3,
                                primary_key=True,
                                serialize=False,
                                verbose_name='Código',
                            ),
                        ),
                        (
                            'descripcion',
                            models.CharField(
                                db_collation='latin1_swedish_ci',
                                db_column='DESCRIPCION',
                                default='',
                                max_length=29,
                                verbose_name='Descripción',
                            ),
                        ),
                        (
                            'departamento_field1',
                            models.IntegerField(blank=True, null=True, verbose_name='Campo Adicional'),
                        ),
                    ],
                    options={
                        'verbose_name': 'Departamento',
                        'verbose_name_plural': 'Departamentos',
                        'db_table': 'departamento',
                        'ordering': ['codigo'],
                        'managed': False,
                    },
                ),
            ],
            database_operations=[],
        ),
    ]

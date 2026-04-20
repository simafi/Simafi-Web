# Alineación con tabla real: id (PK), depto (UNI), descripcion — sin codigo ni departamento_field1.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_departamento_codigo_pk_unmanaged'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='Departamento'),
                migrations.CreateModel(
                    name='Departamento',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        (
                            'depto',
                            models.CharField(
                                db_column='depto',
                                db_collation='latin1_swedish_ci',
                                max_length=3,
                                unique=True,
                                verbose_name='Código departamento',
                            ),
                        ),
                        (
                            'descripcion',
                            models.CharField(
                                db_column='descripcion',
                                db_collation='latin1_swedish_ci',
                                max_length=29,
                                verbose_name='Descripción',
                            ),
                        ),
                    ],
                    options={
                        'verbose_name': 'Departamento',
                        'verbose_name_plural': 'Departamentos',
                        'db_table': 'departamento',
                        'ordering': ['depto'],
                        'managed': False,
                    },
                ),
            ],
            database_operations=[],
        ),
    ]

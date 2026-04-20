# Generated manually on 2025-08-14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=3, verbose_name='Código')),
                ('descripcion', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=29, verbose_name='Descripción')),
                ('departamento_field1', models.IntegerField(blank=True, null=True, verbose_name='Campo Adicional')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'departamento',
                'ordering': ['codigo'],
            },
        ),
        migrations.AddIndex(
            model_name='departamento',
            index=models.Index(fields=['codigo'], name='departamento_codigo_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='departamento',
            unique_together={('codigo',)},
        ),
    ]








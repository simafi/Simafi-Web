# Generated migration to create UsoEdifica model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0006_create_tipodetalle'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsoEdifica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(db_collation='latin1_swedish_ci', max_length=3, unique=True, verbose_name='Código')),
                ('descripcion', models.CharField(db_collation='latin1_swedish_ci', max_length=50, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Uso de Edificación',
                'verbose_name_plural': 'Usos de Edificación',
                'db_table': 'usoedifica',
                'ordering': ['codigo'],
            },
        ),
        migrations.AddConstraint(
            model_name='usoedifica',
            constraint=models.UniqueConstraint(fields=['codigo'], name='codigo'),
        ),
    ]





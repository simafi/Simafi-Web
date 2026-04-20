from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0010_update_edificacion_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiTipologia',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('uso', models.CharField(db_collation='latin1_swedish_ci', default='0', max_length=2, verbose_name='Uso')),
                ('clase', models.CharField(db_collation='latin1_swedish_ci', default='0', max_length=1, verbose_name='Clase')),
                ('tipo', models.CharField(blank=True, db_collation='latin1_swedish_ci', default=None, max_length=2, null=True, verbose_name='Tipo')),
                ('categoria', models.CharField(blank=True, db_collation='latin1_swedish_ci', default=None, max_length=1, null=True, verbose_name='Categoría')),
                ('descripcion', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=100, verbose_name='Descripción')),
                ('peso', models.DecimalField(decimal_places=0, default=0, max_digits=7, verbose_name='Peso')),
            ],
            options={
                'verbose_name': 'Configuración de Tipología',
                'verbose_name_plural': 'Configuraciones de Tipología',
                'db_table': 'confi_tipologia',
                'ordering': ['uso', 'clase', 'tipo'],
            },
        ),
    ]





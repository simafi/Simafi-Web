# Generated migration for Edificacion model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edificacion',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('clave', models.CharField(db_collation='latin1_swedish_ci', default='0', max_length=14, verbose_name='Clave Catastral')),
                ('edifino', models.DecimalField(decimal_places=0, default=0, max_digits=3, verbose_name='Número de Edificación')),
                ('piso', models.CharField(blank=True, db_collation='latin1_swedish_ci', default=None, max_length=1, null=True, verbose_name='Piso')),
                ('area', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Área')),
                ('uso', models.CharField(blank=True, db_collation='latin1_swedish_ci', default=None, max_length=1, null=True, verbose_name='Uso')),
                ('clase', models.CharField(blank=True, db_collation='latin1_swedish_ci', default=None, max_length=2, null=True, verbose_name='Clase')),
                ('calidad', models.CharField(blank=True, db_collation='latin1_swedish_ci', default=None, max_length=2, null=True, verbose_name='Calidad')),
                ('costo', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Costo')),
                ('bueno', models.DecimalField(decimal_places=0, default=0, max_digits=3, verbose_name='Bueno')),
                ('totedi', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='Total Edificación')),
                ('usuario', models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=50, verbose_name='Usuario')),
                ('fechasys', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Fecha de Registro')),
            ],
            options={
                'verbose_name': 'Edificación',
                'verbose_name_plural': 'Edificaciones',
                'db_table': 'edificacion',
                'ordering': ['clave', 'edifino'],
            },
        ),
        migrations.AddIndex(
            model_name='edificacion',
            index=models.Index(fields=['clave'], name='edificacion_idx1'),
        ),
        migrations.AddIndex(
            model_name='edificacion',
            index=models.Index(fields=['clave', 'edifino', 'piso'], name='edificacion_idx2'),
        ),
    ]


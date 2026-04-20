# Generated migration for Costos model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0002_create_edificacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Costos',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('empresa', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=4, verbose_name='Empresa')),
                ('uso', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=2, verbose_name='Uso')),
                ('clase', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=1, verbose_name='Clase')),
                ('calidad', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=3, verbose_name='Calidad')),
                ('costo', models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='Costo')),
            ],
            options={
                'verbose_name': 'Costo',
                'verbose_name_plural': 'Costos',
                'db_table': 'costos',
            },
        ),
        migrations.AlterUniqueTogether(
            name='costos',
            unique_together={('empresa', 'uso', 'clase', 'calidad')},
        ),
        migrations.AddIndex(
            model_name='costos',
            index=models.Index(fields=['empresa', 'uso', 'clase', 'calidad'], name='costos_idx1'),
        ),
    ]








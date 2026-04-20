# Generated migration to create TipoDetalle model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0005_update_detalleadicionales'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDetalle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('empresa', models.CharField(db_collation='latin1_swedish_ci', default=None, max_length=4, null=True, blank=True, verbose_name='Empresa')),
                ('codigo', models.CharField(db_collation='latin1_swedish_ci', default='0', max_length=4, verbose_name='Código')),
                ('descripcion', models.CharField(db_collation='latin1_swedish_ci', default='0', max_length=30, verbose_name='Descripción')),
                ('costo', models.DecimalField(decimal_places=3, default=0.000, max_digits=12, verbose_name='Costo')),
            ],
            options={
                'verbose_name': 'Tipo de Detalle',
                'verbose_name_plural': 'Tipos de Detalle',
                'db_table': 'tipodetalle',
                'ordering': ['codigo'],
            },
        ),
        migrations.AddIndex(
            model_name='tipodetalle',
            index=models.Index(fields=['empresa'], name='tipodetalle_idx1'),
        ),
        migrations.AddIndex(
            model_name='tipodetalle',
            index=models.Index(fields=['codigo'], name='tipodetalle_idx2'),
        ),
    ]







from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0013_update_costos_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoMaterial',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID')),
                ('No', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=2, verbose_name='Número')),
                ('descripcion', models.CharField(db_collation='latin1_swedish_ci', default='', max_length=45, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Tipo de Material',
                'verbose_name_plural': 'Tipos de Material',
                'db_table': 'tipomaterial',
                'ordering': ['No'],
            },
        ),
    ]


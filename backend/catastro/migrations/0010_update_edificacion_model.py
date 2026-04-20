# Generated migration to update Edificacion model according to SQL schema

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0009_add_edifino_piso_to_detalleadicionales'),
    ]

    operations = [
        # Cambiar piso de CharField a DecimalField
        migrations.AlterField(
            model_name='edificacion',
            name='piso',
            field=models.DecimalField(decimal_places=0, default=None, max_digits=2, null=True, blank=True, verbose_name='Piso'),
        ),
        # Agregar campo edificacion_field1
        migrations.AddField(
            model_name='edificacion',
            name='edificacion_field1',
            field=models.IntegerField(null=True, blank=True, default=None, verbose_name='Edificacion Field1'),
        ),
        # Actualizar campos para permitir null según SQL
        migrations.AlterField(
            model_name='edificacion',
            name='area',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=12, null=True, blank=True, verbose_name='Área'),
        ),
        migrations.AlterField(
            model_name='edificacion',
            name='costo',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=12, null=True, blank=True, verbose_name='Costo'),
        ),
        migrations.AlterField(
            model_name='edificacion',
            name='bueno',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3, null=True, blank=True, verbose_name='Bueno'),
        ),
        migrations.AlterField(
            model_name='edificacion',
            name='totedi',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=14, null=True, blank=True, verbose_name='Total Edificación'),
        ),
        # Actualizar empresa para permitir blank
        migrations.AlterField(
            model_name='edificacion',
            name='empresa',
            field=models.CharField(blank=True, db_collation='latin1_swedish_ci', default='', max_length=4, verbose_name='Empresa'),
        ),
    ]






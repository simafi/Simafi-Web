# Generated migration to add edifino and piso fields to DetalleAdicionales model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0008_add_fraccion_valoredi_to_detalleadicionales'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleadicionales',
            name='edifino',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3, null=True, blank=True, verbose_name='Edif. No.'),
        ),
        migrations.AddField(
            model_name='detalleadicionales',
            name='piso',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, null=True, blank=True, verbose_name='Piso'),
        ),
    ]






# Generated migration to add fraccion and valoredi fields to DetalleAdicionales model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0007_create_usoedifica'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleadicionales',
            name='fraccion',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=12, null=True, blank=True, verbose_name='Fracción'),
        ),
        migrations.AddField(
            model_name='detalleadicionales',
            name='valoredi',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=12, null=True, blank=True, verbose_name='Valor Unit Edif. M2', db_column='valoredi'),
        ),
    ]






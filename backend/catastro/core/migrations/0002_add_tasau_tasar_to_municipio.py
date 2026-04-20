# Generated migration to add tasau and tasar fields to Municipio model
# These fields already exist in the database table, this migration just updates the Django model

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipio',
            name='tasau',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0.00'),
                max_digits=7,
                null=True,
                blank=True,
                verbose_name='Tasa Urbana'
            ),
        ),
        migrations.AddField(
            model_name='municipio',
            name='tasar',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0.00'),
                max_digits=7,
                null=True,
                blank=True,
                verbose_name='Tasa Rural'
            ),
        ),
    ]














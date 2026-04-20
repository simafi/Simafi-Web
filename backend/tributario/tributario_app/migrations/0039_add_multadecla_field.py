# Generated manually for multadecla field
# Generated on 2025-09-16 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0036_declaracionvolumen_tarifasics_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaracionvolumen',
            name='multadecla',
            field=models.DecimalField(
                blank=True, 
                decimal_places=2, 
                default=0.0, 
                max_digits=12, 
                null=True, 
                verbose_name='Multa Declaración Tardía'
            ),
        ),
    ]

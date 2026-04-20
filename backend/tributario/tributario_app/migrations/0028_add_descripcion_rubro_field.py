# Generated manually on 2025-08-14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0027_anos_alter_planarbitrio_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='planarbitrio',
            name='descripcion_rubro',
            field=models.CharField(
                blank=True, 
                db_collation='utf8mb4_0900_ai_ci', 
                default='', 
                max_length=200, 
                null=True, 
                verbose_name='Descripción del Rubro'
            ),
        ),
    ]






































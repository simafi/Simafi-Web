# Migración Django para agregar campo cocontrolado
# Ejecutar: python manage.py makemigrations
# Luego: python manage.py migrate

from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [
        ('tributario_app', '0037_tarifasimptoics_alter_planarbitrio_options_and_more'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='declara',
            name='cocontrolado',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
        ),
    ]

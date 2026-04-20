# Migración Django para renombrar campo cocontrolado -> controlado
# Archivo: XXXX_rename_cocontrolado_to_controlado.py

from django.db import migrations

class Migration(migrations.Migration):
    
    dependencies = [
        ('tributario_app', '0037_tarifasimptoics_alter_planarbitrio_options_and_more'),
    ]
    
    operations = [
        # Renombrar campo en el modelo (si existe cocontrolado)
        migrations.RenameField(
            model_name='declara',
            old_name='cocontrolado',
            new_name='controlado',
        ),
        
        # O agregar el campo si no existe
        # migrations.AddField(
        #     model_name='declara',
        #     name='controlado',
        #     field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
        # ),
    ]
    
# NOTA: Esta migración puede no ser necesaria si la tabla ya tiene el campo 'controlado'
# En ese caso, solo actualizar el modelo Django para que coincida con la BD

# Elimina el modelo Departamento del estado de migraciones de esta app:
# la tabla y el modelo viven en `core`; la app configuracion solo reexporta.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='Departamento'),
            ],
            database_operations=[],
        ),
    ]

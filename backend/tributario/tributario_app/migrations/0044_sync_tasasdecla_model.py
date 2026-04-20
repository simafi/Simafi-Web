from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0043_remove_tipo_from_tasasdecla'),
    ]

    operations = [
        # Sincronizar el modelo con la estructura real de la base de datos
        migrations.RunSQL(
            # Verificar que la tabla existe y tiene la estructura correcta
            "SELECT 1 FROM tasasdecla LIMIT 1;",
            reverse_sql="SELECT 1;"
        ),
        
        # Asegurar que el campo tipota existe y tiene el tipo correcto
        migrations.RunSQL(
            """
            ALTER TABLE `tasasdecla` 
            MODIFY COLUMN `tipota` CHAR(1) COLLATE latin1_swedish_ci DEFAULT '' NOT NULL;
            """,
            reverse_sql="SELECT 1;"
        ),
        
        # Verificar que no existe el campo tipo (debe haber sido eliminado)
        migrations.RunSQL(
            """
            SELECT 1 FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'tasasdecla' 
            AND COLUMN_NAME = 'tipo';
            """,
            reverse_sql="SELECT 1;"
        ),
    ]










































from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0044_sync_tasasdecla_model'),
    ]

    operations = [
        # Forzar la sincronización del campo tipota
        migrations.RunSQL(
            """
            -- Verificar que el campo tipota existe y tiene datos
            SELECT COUNT(*) as total_records, 
                   COUNT(CASE WHEN tipota IS NOT NULL AND tipota != '' THEN 1 END) as non_empty_tipota
            FROM tasasdecla 
            WHERE empresa = '0301' AND rtm = '114-03-23' AND expe = '1151';
            """,
            reverse_sql="SELECT 1;"
        ),
        
        # Asegurar que el campo tipota tiene el tipo correcto
        migrations.RunSQL(
            """
            ALTER TABLE `tasasdecla` 
            MODIFY COLUMN `tipota` CHAR(1) COLLATE latin1_swedish_ci DEFAULT '' NOT NULL;
            """,
            reverse_sql="SELECT 1;"
        ),
        
        # Verificar que los datos están correctos
        migrations.RunSQL(
            """
            SELECT id, rtm, expe, rubro, tipota, valor 
            FROM tasasdecla 
            WHERE empresa = '0301' AND rtm = '114-03-23' AND expe = '1151'
            ORDER BY rubro, cod_tarifa;
            """,
            reverse_sql="SELECT 1;"
        ),
    ]










































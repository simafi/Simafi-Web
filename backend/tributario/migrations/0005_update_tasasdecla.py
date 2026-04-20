# Generated manually to update tasasdecla table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tributario', '0004_tasasdecla'),
    ]

    operations = [
        # Agregar campo frecuencia si no existe
        migrations.RunSQL(
            sql="""
                SET @col_exists = 0;
                SELECT COUNT(*) INTO @col_exists 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                  AND TABLE_NAME = 'tasasdecla' 
                  AND COLUMN_NAME = 'frecuencia';

                SET @sql = IF(@col_exists = 0,
                    "ALTER TABLE `tasasdecla` ADD COLUMN `frecuencia` CHAR(1) COLLATE latin1_swedish_ci DEFAULT '' AFTER `cod_tarifa`",
                    "SELECT 'Column frecuencia already exists' AS message");
                    
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="ALTER TABLE `tasasdecla` DROP COLUMN IF EXISTS `frecuencia`;"
        ),
        # Eliminar constraint antiguo si existe
        migrations.RunSQL(
            sql="""
                SET @index_exists = 0;
                SELECT COUNT(*) INTO @index_exists
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'tasasdecla'
                  AND INDEX_NAME = 'tasasdecla_idx4';

                SET @sql = IF(@index_exists > 0,
                    "ALTER TABLE `tasasdecla` DROP INDEX `tasasdecla_idx4`",
                    "SELECT 'Index tasasdecla_idx4 does not exist' AS message");
                    
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="SELECT 1;"
        ),
        # Crear nuevo constraint único
        migrations.RunSQL(
            sql="""
                ALTER TABLE `tasasdecla` 
                ADD UNIQUE KEY `tasasdecla_idx4` (`empresa`, `rtm`, `expe`, `nodecla`, `ano`);
            """,
            reverse_sql="ALTER TABLE `tasasdecla` DROP INDEX IF EXISTS `tasasdecla_idx4`;"
        ),
    ]


# Generated manually to add nudecla field to anoemprenu table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tributario', '0005_update_tasasdecla'),
    ]

    operations = [
        # Agregar campo nudecla a la tabla anoemprenu si no existe
        migrations.RunSQL(
            sql="""
                SET @col_exists = 0;
                SELECT COUNT(*) INTO @col_exists 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                  AND TABLE_NAME = 'anoemprenu' 
                  AND COLUMN_NAME = 'nudecla';

                SET @sql = IF(@col_exists = 0,
                    "ALTER TABLE `anoemprenu` ADD COLUMN `nudecla` DECIMAL(11,0) DEFAULT 0 AFTER `ano`",
                    "SELECT 'Column nudecla already exists' AS message");
                    
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="ALTER TABLE `anoemprenu` DROP COLUMN IF EXISTS `nudecla`;"
        ),
    ]



















































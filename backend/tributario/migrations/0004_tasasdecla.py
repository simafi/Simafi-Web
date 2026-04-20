# Generated manually for tasasdecla table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tributario', '0003_fix_anoemprenu_autoincrement'),
    ]

    operations = [
        # Crear tabla tasasdecla solo si no existe
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS `tasasdecla` (
                  `id` INTEGER NOT NULL AUTO_INCREMENT,
                  `empresa` CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL,
                  `idneg` INTEGER NOT NULL DEFAULT 0,
                  `rtm` CHAR(20) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
                  `expe` CHAR(10) COLLATE latin1_swedish_ci DEFAULT '',
                  `nodecla` CHAR(20) COLLATE latin1_swedish_ci DEFAULT '',
                  `ano` DECIMAL(4,0) DEFAULT 0,
                  `rubro` CHAR(6) COLLATE latin1_swedish_ci DEFAULT '',
                  `cod_tarifa` VARCHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL,
                  `frecuencia` CHAR(1) COLLATE latin1_swedish_ci DEFAULT '',
                  `valor` DECIMAL(12,2) DEFAULT 0.00,
                  `cuenta` CHAR(20) COLLATE latin1_swedish_ci DEFAULT '',
                  `cuentarez` CHAR(20) COLLATE latin1_swedish_ci DEFAULT '',
                  PRIMARY KEY USING BTREE (`id`),
                  UNIQUE KEY `tasasdecla_idx4` USING BTREE (`empresa`, `rtm`, `expe`, `nodecla`, `ano`),
                  KEY `tasasdecla_idx1` USING BTREE (`rtm`),
                  KEY `tasasdecla_idx2` USING BTREE (`expe`),
                  KEY `tasasdecla_idx3` USING BTREE (`cod_tarifa`),
                  KEY `tasasdecla_idx5` USING BTREE (`idneg`)
                ) ENGINE=MyISAM AUTO_INCREMENT=99 ROW_FORMAT=FIXED 
                  CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci';
            """,
            reverse_sql="DROP TABLE IF EXISTS `tasasdecla`;"
        ),
        # Agregar campo frecuencia si la tabla ya existía sin este campo
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
            reverse_sql="SELECT 1;"
        ),
    ]


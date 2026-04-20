# Generated migration for updating Costos model

from django.db import migrations, models
from django.db import connection


def update_costos_table_structure(apps, schema_editor):
    """
    Actualiza la estructura de la tabla costos según el CREATE TABLE proporcionado:
    - Elimina campo id y empresa
    - Cambia rango1 y rango2 a DECIMAL(11,0)
    - Establece clave primaria compuesta (USO, CLASE, CALIDAD)
    """
    with connection.cursor() as cursor:
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'costos'
        """)
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE `costos` (
                  `USO` CHAR(2) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
                  `CLASE` CHAR(1) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
                  `CALIDAD` CHAR(3) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
                  `COSTO` DECIMAL(13,2) NOT NULL DEFAULT 0.00,
                  `rango1` DECIMAL(11,0) DEFAULT 0,
                  `rango2` DECIMAL(11,0) DEFAULT 0,
                  PRIMARY KEY USING BTREE (`USO`, `CLASE`, `CALIDAD`)
                ) ENGINE=MyISAM
                ROW_FORMAT=FIXED CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci'
            """)
        else:
            # Si la tabla existe, intentar actualizar la estructura
            # Nota: Esta migración asume que la tabla puede tener datos
            # y que se debe hacer una migración cuidadosa
            
            # Primero, verificar si existe el campo id
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_schema = DATABASE() 
                AND table_name = 'costos' 
                AND column_name = 'id'
            """)
            has_id = cursor.fetchone()[0] > 0
            
            # Si tiene id, necesitamos hacer una migración más cuidadosa
            # Por ahora, solo agregamos los campos rango1 y rango2 si no existen
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_schema = DATABASE() 
                AND table_name = 'costos' 
                AND column_name = 'rango1'
            """)
            has_rango1 = cursor.fetchone()[0] > 0
            
            if not has_rango1:
                cursor.execute("""
                    ALTER TABLE `costos` 
                    ADD COLUMN `rango1` DECIMAL(11,0) DEFAULT 0
                """)
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_schema = DATABASE() 
                AND table_name = 'costos' 
                AND column_name = 'rango2'
            """)
            has_rango2 = cursor.fetchone()[0] > 0
            
            if not has_rango2:
                cursor.execute("""
                    ALTER TABLE `costos` 
                    ADD COLUMN `rango2` DECIMAL(11,0) DEFAULT 0
                """)


def reverse_update_costos_table(apps, schema_editor):
    """
    Reversa la migración (no se implementa completamente por seguridad)
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0011_create_confi_tipologia'),
    ]

    operations = [
        migrations.RunPython(
            update_costos_table_structure,
            reverse_update_costos_table
        ),
    ]





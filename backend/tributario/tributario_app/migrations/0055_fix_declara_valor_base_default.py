from django.db import migrations, connection


def _fix_valor_base(apps, schema_editor):
    with connection.cursor() as cursor:
        # Si la columna existe pero permite NULL o no tiene default,
        # normalizar a NOT NULL DEFAULT 0.00 y setear nulos a 0.00.
        try:
            cursor.execute("SHOW COLUMNS FROM `declara` LIKE %s", ["valor_base"])
            col = cursor.fetchone()
        except Exception:
            col = None

        if not col:
            # Si no existe por cualquier razón, crearla.
            cursor.execute(
                "ALTER TABLE `declara` "
                "ADD COLUMN `valor_base` DECIMAL(16,2) NOT NULL DEFAULT 0.00 "
                "AFTER `controlado`"
            )
        else:
            # Asegurar estructura correcta
            cursor.execute(
                "ALTER TABLE `declara` "
                "MODIFY COLUMN `valor_base` DECIMAL(16,2) NOT NULL DEFAULT 0.00"
            )
            # Normalizar datos existentes
            cursor.execute("UPDATE `declara` SET `valor_base` = 0.00 WHERE `valor_base` IS NULL")


class Migration(migrations.Migration):
    dependencies = [
        ("tributario_app", "0054_merge_20260416_0940"),
    ]

    operations = [
        migrations.RunPython(_fix_valor_base, reverse_code=migrations.RunPython.noop),
    ]


from django.db import migrations, connection


def _column_exists(table_name: str, column_name: str) -> bool:
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE %s", [column_name])
            return cursor.fetchone() is not None
    except Exception:
        return False


def _ensure_columns(apps, schema_editor):
    # 1) declara.valor_base (NOT NULL, default 0.00)
    if not _column_exists("declara", "valor_base"):
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER TABLE `declara` "
                "ADD COLUMN `valor_base` DECIMAL(16,2) NOT NULL DEFAULT 0.00 "
                "AFTER `controlado`"
            )

    # 2) transaccionesics.vencimiento (NULL)
    if not _column_exists("transaccionesics", "vencimiento"):
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER TABLE `transaccionesics` "
                "ADD COLUMN `vencimiento` DATE NULL DEFAULT NULL "
                "AFTER `fecha`"
            )


class Migration(migrations.Migration):
    dependencies = [
        ("tributario_app", "0052_rubro_moratorio_config"),
    ]

    operations = [
        migrations.RunPython(_ensure_columns, reverse_code=migrations.RunPython.noop),
    ]


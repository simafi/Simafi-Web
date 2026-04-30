from django.db import migrations, models, connection

def _ensure_columns_cross_platform(apps, schema_editor):
    """
    Asegura que las columnas críticas existan en declara y transaccionesics,
    compatible con MySQL y Postgres (Supabase).
    """
    with connection.cursor() as cursor:
        # 1) Verificar declara.valor_base
        table_name = "declara"
        column_name = "valor_base"
        
        # Obtener descripción de la tabla de forma agnóstica
        columns = [col.name.lower() for col in connection.introspection.get_table_description(cursor, table_name)]
        
        if column_name not in columns:
            print(f"Agregando columna {column_name} a la tabla {table_name}...")
            # Usar SQL estándar (compatible con ambos para ADD COLUMN)
            # Nota: Postgres no soporta AFTER, así que lo omitimos o lo manejamos por DB
            if connection.vendor == 'postgresql':
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" DECIMAL(16,2) NOT NULL DEFAULT 0.00')
            else:
                cursor.execute(f'ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` DECIMAL(16,2) NOT NULL DEFAULT 0.00 AFTER `controlado`')
        else:
            # Si existe, asegurar que sea NOT NULL y tenga el tipo correcto (MODIFY en MySQL, ALTER COLUMN en Postgres)
            if connection.vendor == 'postgresql':
                cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" SET NOT NULL')
                cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" SET DEFAULT 0.00')
            else:
                cursor.execute(f'ALTER TABLE `{table_name}` MODIFY COLUMN `{column_name}` DECIMAL(16,2) NOT NULL DEFAULT 0.00')

        # 2) Verificar transaccionesics.vencimiento
        table_name = "transaccionesics"
        column_name = "vencimiento"
        
        columns = [col.name.lower() for col in connection.introspection.get_table_description(cursor, table_name)]
        
        if column_name not in columns:
            print(f"Agregando columna {column_name} a la tabla {table_name}...")
            if connection.vendor == 'postgresql':
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" DATE NULL')
            else:
                cursor.execute(f'ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` DATE NULL AFTER `fecha`')

class Migration(migrations.Migration):
    dependencies = [
        ('tributario_app', '0058_permisooperacionrequisito'),
    ]

    operations = [
        migrations.RunPython(_ensure_columns_cross_platform, reverse_code=migrations.RunPython.noop),
    ]

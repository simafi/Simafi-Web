# Generated manually to fix AUTO_INCREMENT in anoemprenu table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tributario', '0002_add_nodecla_and_anoemprenu'),
    ]

    operations = [
        # Asegurar que el campo id tenga AUTO_INCREMENT
        migrations.RunSQL(
            sql="""
                ALTER TABLE `anoemprenu` 
                MODIFY COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT;
            """,
            reverse_sql="SELECT 1;"  # No hacer nada en reverse
        ),
    ]


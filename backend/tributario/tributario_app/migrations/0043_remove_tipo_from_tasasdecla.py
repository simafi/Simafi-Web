# Generated manually to remove tipo field from tasasdecla table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0042_add_tipota_to_tasasdecla'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE `tasasdecla` DROP COLUMN `tipo`;",
            reverse_sql="ALTER TABLE `tasasdecla` ADD COLUMN `tipo` CHAR(1) COLLATE latin1_swedish_ci DEFAULT NULL;"
        ),
    ]










































from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0009_alter_pagovariostemp_id'),
    ]

    operations = [
        migrations.RunSQL(
            # SQL simple para corregir el campo id
            sql="ALTER TABLE pagovariostemp MODIFY COLUMN id BIGINT NOT NULL AUTO_INCREMENT;",
            reverse_sql="ALTER TABLE pagovariostemp MODIFY COLUMN id BIGINT NOT NULL;"
        ),
    ] 

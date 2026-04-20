from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0010_fix_pagovariostemp_id_simple'),
    ]

    operations = [
        migrations.RunSQL(
            # Agregar AUTO_INCREMENT al campo id
            sql="ALTER TABLE pagovariostemp MODIFY id BIGINT NOT NULL AUTO_INCREMENT;",
            reverse_sql="ALTER TABLE pagovariostemp MODIFY id BIGINT NOT NULL;"
        ),
    ] 

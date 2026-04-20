from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("servicios_publicos", "0006_catastro_coord_xy"),
    ]

    operations = [
        migrations.RemoveField(model_name="spcatastrousuario", name="coord_x"),
        migrations.RemoveField(model_name="spcatastrousuario", name="coord_y"),
    ]


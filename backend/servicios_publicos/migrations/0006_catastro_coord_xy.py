from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("servicios_publicos", "0005_responsable_asignado"),
    ]

    operations = [
        migrations.AddField(
            model_name="spcatastrousuario",
            name="coord_x",
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name="Coordenada X (UTM/Local)"),
        ),
        migrations.AddField(
            model_name="spcatastrousuario",
            name="coord_y",
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=14, null=True, verbose_name="Coordenada Y (UTM/Local)"),
        ),
    ]


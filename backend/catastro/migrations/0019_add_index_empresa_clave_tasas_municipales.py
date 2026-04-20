# Generated migration for adding index on (empresa, clave) to TasasMunicipales

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0018_update_bdcata1_indexes'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='tasasmunicipales',
            index=models.Index(fields=['empresa', 'clave'], name='tarifasics_idx_empresa_clave'),
        ),
    ]














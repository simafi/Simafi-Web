from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0017_add_indexes_legales'),
    ]

    operations = [
        # Agregar índices en bdcata1 según la estructura SQL
        migrations.AddIndex(
            model_name='bdcata1',
            index=models.Index(fields=['barrio'], name='bdcata1_idx2'),
        ),
        migrations.AddIndex(
            model_name='bdcata1',
            index=models.Index(fields=['uso'], name='bdcata1_idx3'),
        ),
        migrations.AddIndex(
            model_name='bdcata1',
            index=models.Index(fields=['subuso'], name='bdcata1_idx4'),
        ),
    ]


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0016_create_detespecificacion'),
    ]

    operations = [
        # Los índices simples (legales_idx2, legales_idx3, legales_idx4) ya existen en la BD
        # Solo agregamos los índices compuestos con empresa para optimizar las consultas
        migrations.AddIndex(
            model_name='legales',
            index=models.Index(fields=['empresa', 'naturaleza'], name='legales_idx_naturaleza'),
        ),
        migrations.AddIndex(
            model_name='legales',
            index=models.Index(fields=['empresa', 'dominio'], name='legales_idx_dominio'),
        ),
        migrations.AddIndex(
            model_name='legales',
            index=models.Index(fields=['empresa', 'tipo'], name='legales_idx_tipo'),
        ),
    ]


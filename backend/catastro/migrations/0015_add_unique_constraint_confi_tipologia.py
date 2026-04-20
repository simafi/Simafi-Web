from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0014_create_tipomaterial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='confitipologia',
            constraint=models.UniqueConstraint(
                fields=['uso', 'clase', 'tipo', 'categoria'],
                name='confi_tipologia_idx1'
            ),
        ),
    ]


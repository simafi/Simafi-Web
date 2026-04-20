# Generated migration to add empresa field to Edificacion model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0003_create_costos'),
    ]

    operations = [
        migrations.AddField(
            model_name='edificacion',
            name='empresa',
            field=models.CharField(db_collation='latin1_swedish_ci', default='', max_length=4, verbose_name='Empresa'),
        ),
    ]








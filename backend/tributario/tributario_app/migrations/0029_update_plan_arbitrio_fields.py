# Generated manually on 2025-08-14

from django.db import migrations, models


def set_default_ano(apps, schema_editor):
    """Establecer año por defecto para registros existentes"""
    PlanArbitrio = apps.get_model('tributario_app', 'PlanArbitrio')
    # Establecer año 2025 para registros existentes sin año
    PlanArbitrio.objects.filter(ano__isnull=True).update(ano=2025)


class Migration(migrations.Migration):

    dependencies = [
        ('tributario_app', '0028_add_descripcion_rubro_field'),
    ]

    operations = [
        # Primero establecer valores por defecto para registros existentes
        migrations.RunPython(set_default_ano, reverse_code=migrations.RunPython.noop),
        
        # Hacer el campo año requerido
        migrations.AlterField(
            model_name='planarbitrio',
            name='ano',
            field=models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Año'),
        ),
        
        # Hacer el campo valor requerido (sin valor por defecto)
        migrations.AlterField(
            model_name='planarbitrio',
            name='valor',
            field=models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor'),
        ),
        
        # Actualizar unique_together para incluir año
        migrations.AlterUniqueTogether(
            name='planarbitrio',
            unique_together={('empresa', 'codigo', 'ano')},
        ),
    ]






































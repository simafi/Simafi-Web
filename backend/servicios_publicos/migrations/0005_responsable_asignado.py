from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("servicios_publicos", "0004_responsables_conceptos_ot"),
    ]

    operations = [
        migrations.AddField(
            model_name="spordentrabajo",
            name="responsable_asignado",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="ordenes_asignadas",
                to="servicios_publicos.spresponsable",
                verbose_name="Responsable (asignado)",
            ),
        ),
    ]


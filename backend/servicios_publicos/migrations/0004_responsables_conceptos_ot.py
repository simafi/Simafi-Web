from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("servicios_publicos", "0003_sp_proceso_calendario"),
    ]

    operations = [
        migrations.CreateModel(
            name="SPResponsable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("empresa", models.CharField(max_length=4, verbose_name="Municipio/Empresa")),
                ("codigo", models.CharField(max_length=20, verbose_name="Código")),
                ("nombre", models.CharField(max_length=200, verbose_name="Nombre")),
                ("telefono", models.CharField(blank=True, max_length=30, null=True)),
                ("activo", models.BooleanField(default=True)),
                ("observacion", models.TextField(blank=True, null=True)),
                ("usuario", models.CharField(blank=True, max_length=50, null=True)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Responsable (Fontanero)",
                "verbose_name_plural": "Responsables (Fontaneros)",
                "db_table": "sp_responsable",
                "ordering": ["empresa", "codigo"],
                "unique_together": {("empresa", "codigo")},
            },
        ),
        migrations.CreateModel(
            name="SPConceptoOT",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("empresa", models.CharField(max_length=4, verbose_name="Municipio/Empresa")),
                ("codigo", models.CharField(max_length=20, verbose_name="Código")),
                ("descripcion", models.CharField(max_length=200, verbose_name="Descripción")),
                ("activo", models.BooleanField(default=True)),
                ("usuario", models.CharField(blank=True, max_length=50, null=True)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Concepto de Orden (Reclamo)",
                "verbose_name_plural": "Conceptos de Orden (Reclamos)",
                "db_table": "sp_concepto_ot",
                "ordering": ["empresa", "codigo"],
                "unique_together": {("empresa", "codigo")},
            },
        ),
        migrations.AddField(
            model_name="spordentrabajo",
            name="concepto",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="ordenes", to="servicios_publicos.spconceptoot", verbose_name="Concepto/Reclamo"),
        ),
        migrations.AddField(
            model_name="spordentrabajo",
            name="responsable_cierre",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="ordenes_cerradas", to="servicios_publicos.spresponsable", verbose_name="Responsable (cierre)"),
        ),
    ]


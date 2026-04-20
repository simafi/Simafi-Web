from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("servicios_publicos", "0002_alter_splectura_foto_medidor_filefield"),
    ]

    operations = [
        migrations.CreateModel(
            name="SPProcesoCalendario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("empresa", models.CharField(max_length=4, verbose_name="Municipio/Empresa")),
                (
                    "tipo",
                    models.CharField(
                        choices=[("L", "Lecturas"), ("F", "Facturación"), ("C", "Cortes/Reconexiones"), ("R", "Reporte"), ("O", "Otro")],
                        default="O",
                        max_length=1,
                    ),
                ),
                ("titulo", models.CharField(max_length=200, verbose_name="Título")),
                ("descripcion", models.TextField(blank=True, null=True, verbose_name="Descripción")),
                ("inicio", models.DateTimeField(verbose_name="Inicio")),
                ("fin", models.DateTimeField(blank=True, null=True, verbose_name="Fin")),
                ("todo_el_dia", models.BooleanField(default=False, verbose_name="Todo el día")),
                ("color", models.CharField(blank=True, max_length=20, null=True, verbose_name="Color (CSS/HEX)")),
                ("usuario", models.CharField(blank=True, max_length=50, null=True)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_modificacion", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Proceso (Calendario)",
                "verbose_name_plural": "Calendario de Procesos",
                "db_table": "sp_proceso_calendario",
                "ordering": ["-inicio"],
            },
        ),
    ]


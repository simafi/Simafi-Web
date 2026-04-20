# Generated manually for ciudadano app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SolicitudTramite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio (código)")),
                (
                    "tipo_tramite",
                    models.CharField(
                        choices=[
                            ("CERT_SOLVENCIA", "Certificado de solvencia / no adeudo"),
                            ("ACTUALIZ_DATOS", "Actualización de datos de inscripción"),
                            ("DECLARACION", "Declaración o rectificación tributaria (referencia)"),
                            ("PQRD", "Petición, queja, reclamo o denuncia"),
                            ("INFO_PUBLICA", "Solicitud de información pública (referencia IAIP)"),
                            ("CITA", "Solicitud de cita de orientación tributaria"),
                            ("OTRO", "Otro trámite"),
                        ],
                        max_length=30,
                        verbose_name="Tipo de trámite",
                    ),
                ),
                ("identificacion", models.CharField(max_length=20, verbose_name="RTN / Identificación")),
                ("nombre_completo", models.CharField(max_length=200, verbose_name="Nombre completo")),
                ("telefono", models.CharField(blank=True, max_length=40, null=True, verbose_name="Teléfono")),
                ("email", models.EmailField(blank=True, max_length=254, null=True, verbose_name="Correo electrónico")),
                (
                    "numero_expediente_negocio",
                    models.CharField(
                        blank=True,
                        max_length=40,
                        null=True,
                        verbose_name="No. expediente / RTM (si aplica)",
                    ),
                ),
                ("detalle", models.TextField(verbose_name="Detalle de la solicitud")),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("RECIBIDA", "Recibida"),
                            ("EN_REVISION", "En revisión"),
                            ("RESPONDIDA", "Respondida / gestionada"),
                            ("CERRADA", "Cerrada"),
                        ],
                        default="RECIBIDA",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                ("referencia", models.CharField(max_length=24, unique=True, verbose_name="Folio interno")),
            ],
            options={
                "verbose_name": "Solicitud de trámite (ciudadano)",
                "verbose_name_plural": "Solicitudes de trámites",
                "db_table": "cdd_solicitud_tramite",
                "ordering": ["-created_at"],
            },
        ),
    ]

# -*- coding: utf-8 -*-
from django.core.validators import FileExtensionValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ciudadano", "0002_solicitud_respuesta_municipal"),
    ]

    operations = [
        migrations.AddField(
            model_name="solicitudtramite",
            name="archivo_respuesta",
            field=models.FileField(
                blank=True,
                help_text="PDF u ofimática — se puede enviar por correo y el ciudadano lo descarga en el portal.",
                null=True,
                upload_to="ciudadano/respuestas/%Y/%m/",
                validators=[FileExtensionValidator(["pdf", "png", "jpg", "jpeg", "doc", "docx"])],
                verbose_name="Constancia o documento (adjunto)",
            ),
        ),
        migrations.AddField(
            model_name="solicitudtramite",
            name="fecha_envio_correo",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Último envío por correo"),
        ),
        migrations.AddField(
            model_name="solicitudtramite",
            name="fecha_envio_whatsapp",
            field=models.DateTimeField(
                blank=True,
                help_text="Se registra cuando el funcionario solicita abrir el enlace de WhatsApp con el mensaje sugerido.",
                null=True,
                verbose_name="Última notificación WhatsApp registrada",
            ),
        ),
    ]

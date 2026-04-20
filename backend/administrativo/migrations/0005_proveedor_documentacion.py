# -*- coding: utf-8 -*-
import os

import django.core.validators
from django.db import migrations, models
from django.utils.text import get_valid_filename


def _proveedor_documentacion_upload_to(instance, filename):
    safe = get_valid_filename(os.path.basename(filename)) or "documento"
    emp = (instance.empresa or "na").strip()[:10]
    pk_part = instance.pk if instance.pk else "nuevo"
    return f"adm_proveedores/{emp}/{pk_part}/{safe}"


class Migration(migrations.Migration):

    dependencies = [
        ("administrativo_main", "0004_alter_proveedor_nit_verbose_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="proveedor",
            name="documentacion_descripcion",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Breve descripción del archivo (ej. RTN, constancia, convenio).",
                max_length=255,
                verbose_name="Referencia del documento",
            ),
        ),
        migrations.AddField(
            model_name="proveedor",
            name="documentacion",
            field=models.FileField(
                blank=True,
                help_text="PDF u ofimática. El archivo se guarda en carpeta exclusiva del municipio en sesión.",
                null=True,
                upload_to=_proveedor_documentacion_upload_to,
                validators=[
                    django.core.validators.FileExtensionValidator(["pdf", "png", "jpg", "jpeg", "doc", "docx"])
                ],
                verbose_name="Documentación digital",
            ),
        ),
    ]

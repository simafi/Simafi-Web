# -*- coding: utf-8 -*-
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models import BaseModel


class SolicitudTramite(BaseModel):
    """
    Solicitud de trámite en línea presentada por el contribuyente.
    Referencia: obligaciones de transparencia y atención municipal (Ley de Municipalidades, Honduras).
    """

    TIPO_CHOICES = [
        ("CERT_SOLVENCIA", "Certificado de solvencia / no adeudo"),
        ("ACTUALIZ_DATOS", "Actualización de datos de inscripción"),
        ("DECLARACION", "Declaración o rectificación tributaria (referencia)"),
        ("PQRD", "Petición, queja, reclamo o denuncia"),
        ("INFO_PUBLICA", "Solicitud de información pública (referencia IAIP)"),
        ("CITA", "Solicitud de cita de orientación tributaria"),
        ("OTRO", "Otro trámite"),
    ]

    ESTADO_CHOICES = [
        ("RECIBIDA", "Recibida"),
        ("EN_REVISION", "En revisión"),
        ("RESPONDIDA", "Respondida / gestionada"),
        ("CERRADA", "Cerrada"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio (código)")
    tipo_tramite = models.CharField(max_length=30, choices=TIPO_CHOICES, verbose_name="Tipo de trámite")
    identificacion = models.CharField(max_length=20, verbose_name="RTN / Identificación")
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre completo")
    telefono = models.CharField(max_length=40, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo electrónico")
    numero_expediente_negocio = models.CharField(
        max_length=40, blank=True, null=True, verbose_name="No. expediente / RTM (si aplica)"
    )
    detalle = models.TextField(verbose_name="Detalle de la solicitud")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="RECIBIDA", verbose_name="Estado")
    referencia = models.CharField(max_length=24, unique=True, verbose_name="Folio interno")

    # Respuesta de la municipalidad (ciclo completo ciudadano ↔ ente)
    respuesta_municipal = models.TextField(
        blank=True,
        default="",
        verbose_name="Respuesta oficial al contribuyente",
        help_text="Texto visible para el ciudadano en el portal cuando se registre.",
    )
    fecha_respuesta = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha y hora de la respuesta",
    )
    funcionario_respuesta = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Funcionario que responde",
    )
    nota_interna = models.TextField(
        blank=True,
        default="",
        verbose_name="Nota interna (no visible al ciudadano)",
        help_text="Uso administrativo: seguimiento, archivo o instrucciones internas.",
    )
    archivo_respuesta = models.FileField(
        upload_to="ciudadano/respuestas/%Y/%m/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["pdf", "png", "jpg", "jpeg", "doc", "docx"])],
        verbose_name="Constancia o documento (adjunto)",
        help_text="PDF u ofimática — se puede enviar por correo y el ciudadano lo descarga en el portal.",
    )
    fecha_envio_correo = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último envío por correo",
    )
    fecha_envio_whatsapp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última notificación WhatsApp registrada",
        help_text="Se registra cuando el funcionario solicita abrir el enlace de WhatsApp con el mensaje sugerido.",
    )

    class Meta:
        db_table = "cdd_solicitud_tramite"
        verbose_name = "Solicitud de trámite (ciudadano)"
        verbose_name_plural = "Solicitudes de trámites"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.referencia} — {self.get_tipo_tramite_display()}"

# -*- coding: utf-8 -*-
"""Notificaciones al contribuyente: correo electrónico y enlace WhatsApp (Honduras +504)."""
import logging
from urllib.parse import quote

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def normalizar_telefono_whatsapp(numero):
    """Devuelve solo dígitos; si hay 8 dígitos locales, antepone 504."""
    if not numero:
        return ""
    digits = "".join(c for c in str(numero) if c.isdigit())
    if digits.startswith("504"):
        return digits
    if len(digits) == 8:
        return "504" + digits
    if len(digits) == 9 and digits.startswith("9"):
        return "504" + digits
    return digits


def construir_mensaje_whatsapp(solicitud, url_portal):
    """Texto sugerido para informar al contribuyente por WhatsApp Web/App."""
    nombre = (solicitud.nombre_completo or "estimado contribuyente").split()[0]
    lines = [
        f"Hola {nombre},",
        f"Le informamos sobre su solicitud *{solicitud.referencia}* en el portal ciudadano del municipio.",
        "",
        solicitud.respuesta_municipal[:500] if solicitud.respuesta_municipal else "Tiene respuesta y/o documento disponible en el portal.",
        "",
        f"Portal: {url_portal}",
        "Puede iniciar sesión y revisar «Mis solicitudes» para descargar constancias o archivos adjuntos.",
    ]
    return "\n".join(lines)


def construir_url_whatsapp(telefono, mensaje):
    n = normalizar_telefono_whatsapp(telefono)
    if len(n) < 11:
        return None
    return f"https://wa.me/{n}?text={quote(mensaje)}"


def enviar_correo_con_adjunto(solicitud):
    """
    Envía correo al contribuyente con el texto de respuesta y, si existe, el archivo adjunto.
    Requiere configuración SMTP válida en settings (EMAIL_HOST, etc.) o backend consola en desarrollo.
    Retorna (ok: bool, mensaje: str).
    """
    destino = (solicitud.email or "").strip()
    if not destino:
        return False, "El contribuyente no tiene correo electrónico en la solicitud."

    subject = f"[Municipio {solicitud.empresa}] Respuesta a su trámite {solicitud.referencia}"
    body = (
        f"Estimado(a) {solicitud.nombre_completo},\n\n"
        f"Referencia: {solicitud.referencia}\n\n"
        f"{solicitud.respuesta_municipal or 'Se adjunta documento relacionado a su solicitud.'}\n\n"
        f"--\nMensaje generado desde el sistema municipal SIMAFI.\n"
        f"También puede consultar el estado en el portal ciudadano."
    )

    try:
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "noreply@localhost"
        email = EmailMessage(subject, body, from_email, [destino])
        if solicitud.archivo_respuesta:
            field = solicitud.archivo_respuesta
            if field.name:
                email.attach_file(field.path)
        email.send()
        return True, "Correo enviado correctamente."
    except Exception as exc:
        logger.exception("Fallo envío correo ciudadano")
        return False, f"No se pudo enviar el correo: {exc}"

# -*- coding: utf-8 -*-
from django import forms

from .models import SolicitudTramite


class AccesoContribuyenteForm(forms.Form):
    identificacion = forms.CharField(
        label="RTN o identificación",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. 08011990123456"}),
    )
    nombre_completo = forms.CharField(
        label="Nombre completo o razón social",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    telefono = forms.CharField(
        label="Teléfono de contacto",
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )


class SolicitudTramiteForm(forms.ModelForm):
    class Meta:
        model = SolicitudTramite
        fields = ("tipo_tramite", "numero_expediente_negocio", "detalle")
        widgets = {
            "tipo_tramite": forms.Select(attrs={"class": "form-select"}),
            "numero_expediente_negocio": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Opcional — expediente en Tributario"}
            ),
            "detalle": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class GestionSolicitudForm(forms.ModelForm):
    """Formulario para funcionarios: estado, respuesta, adjunto y notificación al contribuyente."""

    enviar_correo = forms.BooleanField(
        required=False,
        initial=False,
        label="Enviar notificación por correo electrónico",
        help_text="Envía el texto de respuesta y, si subió un archivo, lo adjunta al correo del contribuyente.",
    )
    enviar_whatsapp = forms.BooleanField(
        required=False,
        initial=False,
        label="Preparar mensaje para WhatsApp",
        help_text="Tras guardar, se mostrará un enlace para abrir WhatsApp Web/App con el texto sugerido (teléfono de la solicitud).",
    )

    class Meta:
        model = SolicitudTramite
        fields = ("estado", "respuesta_municipal", "nota_interna", "archivo_respuesta")
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select"}),
            "respuesta_municipal": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Respuesta que verá el contribuyente en el portal (texto oficial o instructivo).",
                }
            ),
            "nota_interna": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Solo uso interno — no se muestra al ciudadano.",
                }
            ),
            "archivo_respuesta": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".pdf,.png,.jpg,.jpeg,.doc,.docx"}
            ),
        }

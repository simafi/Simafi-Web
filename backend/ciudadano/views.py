# -*- coding: utf-8 -*-
import os
import uuid

from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .forms import AccesoContribuyenteForm, GestionSolicitudForm, SolicitudTramiteForm
from .models import SolicitudTramite
from .notificaciones import construir_mensaje_whatsapp, construir_url_whatsapp, enviar_correo_con_adjunto


def _requiere_sesion_sistema(request):
    if not request.session.get("user_id"):
        messages.warning(request, "Inicie sesión en el sistema para acceder al portal ciudadano.")
        return False
    return True


def _empresa_sesion(request):
    return request.session.get("empresa") or ""


def _contribuyente_sesion_ok(request):
    return bool(request.session.get("ciudadano_identificado"))


def portal_inicio(request):
    """Página pública de bienvenida (puede mostrarse sin sesión con mensaje para acceder)."""
    ctx = {
        "tiene_sesion": bool(request.session.get("user_id")),
        "empresa": _empresa_sesion(request),
        "puede_gestion": bool(request.session.get("user_id") and _empresa_sesion(request)),
    }
    return render(request, "ciudadano/portal.html", ctx)


def acceso_contribuyente(request):
    """Identificación del contribuyente para trámites en línea (sesión de sistema requerida)."""
    if not _requiere_sesion_sistema(request):
        return redirect("modules_core:login_principal")

    if request.method == "POST":
        form = AccesoContribuyenteForm(request.POST)
        if form.is_valid():
            request.session["ciudadano_identificado"] = True
            request.session["ciudadano_rtn"] = form.cleaned_data["identificacion"].strip()
            request.session["ciudadano_nombre"] = form.cleaned_data["nombre_completo"].strip()
            request.session["ciudadano_telefono"] = (form.cleaned_data.get("telefono") or "").strip()
            request.session["ciudadano_email"] = (form.cleaned_data.get("email") or "").strip()
            messages.success(request, "Datos registrados para sus trámites en línea.")
            return redirect("ciudadano:menu_ciudadano")
    else:
        initial = {}
        if request.session.get("ciudadano_identificado"):
            initial = {
                "identificacion": request.session.get("ciudadano_rtn", ""),
                "nombre_completo": request.session.get("ciudadano_nombre", ""),
                "telefono": request.session.get("ciudadano_telefono", ""),
                "email": request.session.get("ciudadano_email", ""),
            }
        form = AccesoContribuyenteForm(initial=initial)

    return render(
        request,
        "ciudadano/acceso.html",
        {"form": form, "empresa": _empresa_sesion(request)},
    )


def menu_ciudadano(request):
    if not _requiere_sesion_sistema(request):
        return redirect("modules_core:login_principal")
    if not _contribuyente_sesion_ok(request):
        messages.info(request, "Identifíquese como contribuyente para usar los trámites en línea.")
        return redirect("ciudadano:acceso_contribuyente")

    return render(
        request,
        "ciudadano/menu.html",
        {
            "empresa": _empresa_sesion(request),
            "usuario": request.session.get("nombre", ""),
        },
    )


def nueva_solicitud(request):
    if not _requiere_sesion_sistema(request):
        return redirect("modules_core:login_principal")
    if not _contribuyente_sesion_ok(request):
        return redirect("ciudadano:acceso_contribuyente")

    empresa = _empresa_sesion(request)
    if not empresa:
        messages.error(request, "No se detectó el código de empresa/municipio en sesión.")
        return redirect("ciudadano:menu_ciudadano")

    if request.method == "POST":
        form = SolicitudTramiteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = empresa
            obj.identificacion = request.session.get("ciudadano_rtn", "")
            obj.nombre_completo = request.session.get("ciudadano_nombre", "")
            obj.telefono = request.session.get("ciudadano_telefono") or None
            obj.email = request.session.get("ciudadano_email") or None
            obj.referencia = _generar_folio()
            obj.save()
            messages.success(request, f"Solicitud registrada. Su folio es: {obj.referencia}")
            return redirect("ciudadano:mis_solicitudes")
    else:
        form = SolicitudTramiteForm()

    return render(
        request,
        "ciudadano/solicitud_form.html",
        {"form": form, "empresa": empresa},
    )


def _generar_folio():
    return f"C{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


def mis_solicitudes(request):
    if not _requiere_sesion_sistema(request):
        return redirect("modules_core:login_principal")
    if not _contribuyente_sesion_ok(request):
        return redirect("ciudadano:acceso_contribuyente")

    empresa = _empresa_sesion(request)
    rtn = request.session.get("ciudadano_rtn", "")
    items = SolicitudTramite.objects.filter(empresa=empresa, identificacion=rtn, is_active=True).order_by(
        "-created_at"
    )[:100]
    return render(
        request,
        "ciudadano/mis_solicitudes.html",
        {"items": items, "empresa": empresa},
    )


def detalle_solicitud(request, pk):
    if not _requiere_sesion_sistema(request):
        return redirect("modules_core:login_principal")
    if not _contribuyente_sesion_ok(request):
        return redirect("ciudadano:acceso_contribuyente")

    empresa = _empresa_sesion(request)
    rtn = request.session.get("ciudadano_rtn", "")
    obj = get_object_or_404(SolicitudTramite, pk=pk, empresa=empresa, identificacion=rtn)
    return render(request, "ciudadano/detalle_solicitud.html", {"s": obj})


def marco_legal(request):
    return render(request, "ciudadano/marco_legal.html", {"empresa": _empresa_sesion(request)})


def salir_ciudadano(request):
    """Limpia solo datos de contribuyente en sesión."""
    for k in (
        "ciudadano_identificado",
        "ciudadano_rtn",
        "ciudadano_nombre",
        "ciudadano_telefono",
        "ciudadano_email",
    ):
        request.session.pop(k, None)
    messages.info(request, "Se cerró la sesión de contribuyente en este módulo.")
    return redirect("ciudadano:portal_inicio")


# --- Gestión municipal (funcionarios): respuesta y cierre del ciclo ---


def _requiere_gestion(request):
    if not _requiere_sesion_sistema(request):
        return False
    if not _empresa_sesion(request):
        messages.error(request, "Se requiere empresa/municipio en sesión para la bandeja de gestión.")
        return False
    return True


def _puede_descargar_adjunto_respuesta(request, obj):
    """Funcionario del municipio (misma empresa) o contribuyente con RTN coincidente."""
    if not request.session.get("user_id"):
        return False
    if _empresa_sesion(request) != obj.empresa:
        return False
    if _contribuyente_sesion_ok(request):
        return obj.identificacion == request.session.get("ciudadano_rtn")
    return True


def gestion_bandeja(request):
    """
    Listado de solicitudes del municipio (empresa en sesión) para asignar estado y respuesta oficial.
    No requiere perfil 'ciudadano' — solo usuario del sistema municipal.
    """
    if not _requiere_gestion(request):
        return redirect("modules_core:login_principal")

    empresa = _empresa_sesion(request)
    estado_f = request.GET.get("estado", "")
    qs = SolicitudTramite.objects.filter(empresa=empresa, is_active=True).order_by("-created_at")
    if estado_f and estado_f in dict(SolicitudTramite.ESTADO_CHOICES):
        qs = qs.filter(estado=estado_f)

    return render(
        request,
        "ciudadano/gestion_bandeja.html",
        {
            "items": qs[:500],
            "empresa": empresa,
            "usuario": request.session.get("nombre", ""),
            "estado_filtro": estado_f,
            "estados": SolicitudTramite.ESTADO_CHOICES,
        },
    )


def gestion_solicitud(request, pk):
    """Editar estado, respuesta visible al ciudadano y nota interna."""
    if not _requiere_gestion(request):
        return redirect("modules_core:login_principal")

    empresa = _empresa_sesion(request)
    obj = get_object_or_404(SolicitudTramite, pk=pk, empresa=empresa, is_active=True)
    link_whatsapp = None

    if request.method == "POST":
        form = GestionSolicitudForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            texto = (inst.respuesta_municipal or "").strip()
            if texto:
                inst.fecha_respuesta = timezone.now()
                inst.funcionario_respuesta = (request.session.get("nombre") or request.session.get("usuario") or "")[
                    :200
                ]
            enviar_correo = form.cleaned_data.get("enviar_correo")
            enviar_wa = form.cleaned_data.get("enviar_whatsapp")
            inst.save()
            inst.refresh_from_db()

            msgs = ["Solicitud actualizada. El contribuyente verá la respuesta en su portal."]
            if enviar_correo:
                ok, msg_mail = enviar_correo_con_adjunto(inst)
                if ok:
                    SolicitudTramite.objects.filter(pk=inst.pk).update(fecha_envio_correo=timezone.now())
                    msgs.append(msg_mail)
                else:
                    messages.warning(request, msg_mail)
            if enviar_wa:
                SolicitudTramite.objects.filter(pk=inst.pk).update(fecha_envio_whatsapp=timezone.now())
                messages.success(request, " ".join(msgs))
                return redirect(f"{reverse('ciudadano:gestion_solicitud', args=[pk])}?wa=1")

            messages.success(request, " ".join(msgs))
            return redirect("ciudadano:gestion_bandeja")
    else:
        form = GestionSolicitudForm(instance=obj)
        if request.GET.get("wa") == "1":
            portal = request.build_absolute_uri(reverse("ciudadano:portal_inicio"))
            mensaje = construir_mensaje_whatsapp(obj, portal)
            link_whatsapp = construir_url_whatsapp(obj.telefono, mensaje)

    return render(
        request,
        "ciudadano/gestion_solicitud.html",
        {
            "form": form,
            "s": obj,
            "empresa": empresa,
            "usuario": request.session.get("nombre", ""),
            "link_whatsapp": link_whatsapp,
        },
    )


def descargar_adjunto_respuesta(request, pk):
    """Descarga segura del archivo de respuesta (funcionario o contribuyente dueño del trámite)."""
    if not _requiere_sesion_sistema(request):
        return redirect("modules_core:login_principal")

    empresa = _empresa_sesion(request)
    obj = get_object_or_404(SolicitudTramite, pk=pk, empresa=empresa, is_active=True)
    if not _puede_descargar_adjunto_respuesta(request, obj):
        raise Http404()
    if not obj.archivo_respuesta or not obj.archivo_respuesta.name:
        raise Http404()
    try:
        path = obj.archivo_respuesta.path
    except NotImplementedError:
        path = None
    if path and os.path.isfile(path):
        fh = open(path, "rb")
    else:
        fh = obj.archivo_respuesta.open("rb")
    filename = os.path.basename(obj.archivo_respuesta.name)
    return FileResponse(fh, as_attachment=True, filename=filename)

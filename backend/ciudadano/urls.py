# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "ciudadano"

urlpatterns = [
    path("", views.portal_inicio, name="portal_inicio"),
    path("acceso/", views.acceso_contribuyente, name="acceso_contribuyente"),
    path("menu/", views.menu_ciudadano, name="menu_ciudadano"),
    path("solicitud/nueva/", views.nueva_solicitud, name="nueva_solicitud"),
    path("solicitudes/", views.mis_solicitudes, name="mis_solicitudes"),
    path("solicitudes/<int:pk>/", views.detalle_solicitud, name="detalle_solicitud"),
    path("solicitudes/<int:pk>/adjunto/", views.descargar_adjunto_respuesta, name="descargar_adjunto_respuesta"),
    path("marco-legal/", views.marco_legal, name="marco_legal"),
    path("salir-contribuyente/", views.salir_ciudadano, name="salir_ciudadano"),
    # Gestión municipal (funcionarios)
    path("gestion/", views.gestion_bandeja, name="gestion_bandeja"),
    path("gestion/solicitud/<int:pk>/", views.gestion_solicitud, name="gestion_solicitud"),
]

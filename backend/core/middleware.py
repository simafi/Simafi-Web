# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from core.module_access import (
    modulo_desde_ruta,
    sincronizar_privilegios_modular_desde_bd,
    sincronizar_sesion_catastro,
    usuario_puede_acceso_modulo,
)


class ModuloAccesoMiddleware:
    """
    Tras el login modular (usuario + municipio + contraseña), el acceso a cada módulo
    queda cubierto por esa sesión; no se pide una segunda contraseña por módulo.
    No aplica a ciudadano ni a rutas públicas del núcleo.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path or '/'
        codigo = modulo_desde_ruta(path)
        if codigo is None:
            return self.get_response(request)

        if path.startswith('/ciudadano/'):
            return self.get_response(request)

        exentas = (
            '/admin/',
            '/static/',
            '/media/',
            '/favicon.ico',
        )
        if any(path.startswith(p) for p in exentas):
            return self.get_response(request)

        # Núcleo modular: menú, login, logout, verificación; acceso-modulo solo redirige si hay sesión
        core_ok = (
            path in ('/', '/login/', '/menu/', '/logout/', '/verificar-sesion/')
            or path.startswith('/acceso-modulo/')
        )
        if core_ok:
            return self.get_response(request)

        if not request.session.get('user_id'):
            # Evitar NoReverseMatch si el namespace aún no está registrado en ciertas cargas.
            return redirect(f'/login/?next={path}')

        if not sincronizar_privilegios_modular_desde_bd(request):
            return redirect(f'/login/?next={path}')

        if not usuario_puede_acceso_modulo(request, codigo):
            messages.error(
                request,
                'No tiene permiso para acceder a este módulo. '
                'Si necesita acceso, un superusuario debe asignárselo en Usuarios del sistema.',
            )
            return redirect('modules_core:menu_principal')

        if codigo == 'catastro' and path.startswith('/catastro/'):
            sincronizar_sesion_catastro(request)
        return self.get_response(request)

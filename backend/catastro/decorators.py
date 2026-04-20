# -*- coding: utf-8 -*-
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from usuarios.permisos import usuario_tiene_permiso


def catastro_require_permiso(codigo_permiso):
    """
    Debe usarse *debajo* de @catastro_require_auth (auth primero, permiso después).
    Puede ser un código str o una tupla/lista de códigos (basta con tener uno).
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            codes = (
                codigo_permiso
                if isinstance(codigo_permiso, (list, tuple))
                else (codigo_permiso,)
            )
            if not any(usuario_tiene_permiso(request, c) for c in codes):
                messages.error(
                    request,
                    "No tiene permiso para acceder a esta función. "
                    "Solicite el rol adecuado al administrador (Roles / Usuarios del sistema).",
                )
                return redirect("catastro:catastro_menu_principal")

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator

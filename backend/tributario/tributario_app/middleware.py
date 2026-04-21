# -*- coding: utf-8 -*-
"""
Solo desarrollo (DEBUG=True): permite formularios POST vía túneles ngrok sin fijar
cada subdominio en CSRF_TRUSTED_ORIGINS. No activar en producción.
"""
from django.conf import settings

_NGROK_SUFFIXES = ('.ngrok-free.dev', '.ngrok.io', '.ngrok.app', '.loca.lt')


class NgrokCsrfTrustMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'DEBUG', False):
            host = request.get_host()
            hostname = host.split(':')[0].lower()
            if any(hostname.endswith(suf) for suf in _NGROK_SUFFIXES):
                trusted = getattr(settings, 'CSRF_TRUSTED_ORIGINS', None)
                if trusted is None:
                    settings.CSRF_TRUSTED_ORIGINS = []
                elif isinstance(trusted, tuple):
                    settings.CSRF_TRUSTED_ORIGINS = list(trusted)
                for scheme in ('https', 'http'):
                    origin = f'{scheme}://{host}'
                    if origin not in settings.CSRF_TRUSTED_ORIGINS:
                        settings.CSRF_TRUSTED_ORIGINS.append(origin)
        return self.get_response(request)


class SessionSyncMiddleware:
    """
    Middleware para sincronizar claves de sesión de multitenencia.
    Asegura que 'empresa', 'municipio_codigo' y 'catastro_empresa' tengan el mismo valor.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, 'session'):
            return self.get_response(request)

        # Buscar el código de empresa en las distintas claves posibles
        empresa = request.session.get('empresa') or \
                  request.session.get('municipio_codigo') or \
                  request.session.get('catastro_empresa')

        if empresa:
            # Sincronizar todas las claves para que todas las vistas vean lo mismo
            modified = False
            for key in ['empresa', 'municipio_codigo', 'catastro_empresa']:
                if request.session.get(key) != empresa:
                    request.session[key] = empresa
                    modified = True
            
            # Si se modificó la sesión, asegurar que se guarde
            if modified:
                request.session.modified = True

        return self.get_response(request)

"""
URL configuration for simafiweb modular system.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, FileResponse, JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.db import connection
from django.db.utils import DatabaseError, OperationalError
import os

def serve_favicon(request):
    """Servir el favicon desde los archivos estáticos"""
    favicon_path = None
    
    # Buscar favicon en diferentes ubicaciones
    possible_paths = [
        os.path.join(settings.BASE_DIR, 'venv', 'Scripts', 'core', 'static', 'favicon.ico'),
        os.path.join(settings.BASE_DIR, 'modules', 'core', 'static', 'favicon.ico'),
        os.path.join(settings.BASE_DIR, 'static', 'favicon.ico'),
    ]
    
    for path_option in possible_paths:
        if os.path.exists(path_option):
            favicon_path = path_option
            break
    
    if favicon_path and os.path.exists(favicon_path):
        try:
            return FileResponse(open(favicon_path, 'rb'), content_type='image/x-icon')
        except Exception:
            pass
    
    # Si no se encuentra, retornar respuesta vacía (204 No Content)
    return HttpResponse(status=204)


def healthz(request):
    """
    Endpoint liviano para validar despliegues en Vercel sin depender del menú principal
    (que puede tocar DB/sesiones y ocultar el error real detrás de FUNCTION_INVOCATION_FAILED).
    """
    db = getattr(settings, "DATABASES", {}).get("default", {})
    db_name = (db.get("NAME") or "").strip()
    db_host = (db.get("HOST") or "").strip()
    db_user = (db.get("USER") or "").strip()
    db_port = str(db.get("PORT") or "").strip()
    db_url_source = getattr(settings, "DATABASE_URL_SOURCE", "") or None

    return JsonResponse(
        {
            "ok": True,
            "debug": bool(settings.DEBUG),
            "allowed_hosts_configured": bool(getattr(settings, "ALLOWED_HOSTS", [])),
            "session_engine": getattr(settings, "SESSION_ENGINE", None),
            "database_url_source": db_url_source,
            "database": {
                "engine": db.get("ENGINE"),
                "name_set": bool(db_name),
                "host_set": bool(db_host),
                "user_set": bool(db_user),
                "port": db_port or None,
            },
        }
    )


def dbcheck(request):
    """
    Prueba real de conectividad a Postgres (SELECT 1).
    No expone passwords ni URLs completas.
    """
    db = getattr(settings, "DATABASES", {}).get("default", {})
    info = {
        "ok": False,
        "database_url_source": getattr(settings, "DATABASE_URL_SOURCE", "") or None,
        "host": (db.get("HOST") or None),
        "port": str(db.get("PORT") or "") or None,
        "name": (db.get("NAME") or None),
        "user": (db.get("USER") or None),
        "sslmode": (db.get("OPTIONS") or {}).get("sslmode"),
    }
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            one = cursor.fetchone()
            info["ok"] = bool(one and one[0] == 1)

            # Opcional: verificar existencia de tablas (Postgres) sin exponer datos.
            # Uso: /__dbcheck?tables=1
            if (request.GET.get("tables") or "").strip() in ("1", "true", "yes", "on"):
                tables = [
                    # Catastro
                    "bdcata1",
                    "tasassmunicipales",
                    # Tributario BI
                    "transaccionesbienesinmuebles",
                    "rubros",
                    "norecibos",
                    "pagovariostemp",
                    # Django session (si se usa DB sessions)
                    "django_session",
                ]
                regclass = {}
                for t in tables:
                    cursor.execute("SELECT to_regclass(%s)", [t])
                    regclass[t] = cursor.fetchone()[0]
                info["table_regclass"] = regclass

        return JsonResponse(info)
    except (OperationalError, DatabaseError) as exc:
        info["error"] = str(exc)
        return JsonResponse(info, status=500)


urlpatterns = [
    path("__healthz", healthz, name="healthz"),
    path("__dbcheck", dbcheck, name="dbcheck"),
    # Favicon - debe estar antes de otras rutas para evitar 404
    path('favicon.ico', serve_favicon, name='favicon'),
    
    path('admin/', admin.site.urls),
    
    # Sistema modular - Ruta raíz desde Scripts
    path('', include('core.urls', namespace='modules_core')),
    
    # Sistema tributario
    path('tributario/', include('tributario.tributario_urls', namespace='tributario')),
    
    # Aplicaciones legacy dentro de tributario - Habilitado para compatibilidad
    path('tributario/', include('tributario.tributario_app.urls', namespace='tributario_app')),
    
    # Módulos principales (ubicados en C:\simafiweb\venv\Scripts\)
    path('catastro/', include('catastro.urls', namespace='catastro')),
    path('administrativo/', include('administrativo.urls', namespace='administrativo')),
    path('compras/', include('compras.urls', namespace='compras')),
    path('configuracion/', include('configuracion.urls', namespace='configuracion')),
    path('contabilidad/', include('contabilidad.urls', namespace='contabilidad')),
    path('presupuestos/', include('presupuestos.urls', namespace='presupuestos')),
    path('tesoreria/', include('tesoreria.urls', namespace='tesoreria')),
    path('ciudadano/', include('ciudadano.urls', namespace='ciudadano')),
    path('servicios-publicos/', include('servicios_publicos.urls', namespace='servicios_publicos')),
    
    # path('administrativo-app/', include('tributario.administrativo_app.urls', namespace='administrativo_app')),
]

# Configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

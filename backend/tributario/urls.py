"""
URL configuration for simafiweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.http import HttpResponse, FileResponse, JsonResponse
from django.db import connection
from django.db.utils import DatabaseError, OperationalError
import os

def serve_favicon(request):
    """Servir el favicon desde los archivos estáticos"""
    favicon_path = None
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
    return HttpResponse(status=204)

def healthz(request):
    """Endpoint liviano para validar despliegues en Vercel"""
    db = getattr(settings, "DATABASES", {}).get("default", {})
    return JsonResponse({
        "ok": True,
        "debug": bool(settings.DEBUG),
        "database": {"engine": db.get("ENGINE"), "host": db.get("HOST")},
    })

def dbcheck(request):
    """Prueba real de conectividad a Postgres (SELECT 1)"""
    info = {"ok": False}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            one = cursor.fetchone()
        info["ok"] = bool(one and one[0] == 1)
        return JsonResponse(info)
    except Exception as exc:
        info["error"] = str(exc)
        return JsonResponse(info, status=500)

urlpatterns = [
    path("__healthz", healthz, name="healthz"),
    path("__dbcheck", dbcheck, name="dbcheck"),
    path('favicon.ico', serve_favicon, name='favicon'),
    path('admin/', admin.site.urls),
    
    # Sistema modular - Ruta raíz
    path('', include('core.urls', namespace='modules_core')),
    
    # Ruta tributario - Sistema tributario específico
    path('tributario/', include('tributario.tributario_urls', namespace='tributario')),
    
    # Módulos principales (ubicados en C:\simafiweb\venv\Scripts\)
    path('catastro/', include('catastro.urls', namespace='catastro')),
    path('administrativo/', include('administrativo.urls', namespace='administrativo')),
    path('compras/', include('compras.urls', namespace='compras')),
    path('configuracion/', include('configuracion.urls', namespace='configuracion')),
    path('contabilidad/', include('contabilidad.urls', namespace='contabilidad')),
    path('presupuestos/', include('presupuestos.urls', namespace='presupuestos')),
    path('tesoreria/', include('tesoreria.urls', namespace='tesoreria')),
    path('ciudadano/', include('ciudadano.urls', namespace='ciudadano')),
    
    # Módulo de Facturación de Servicios Públicos (Agua Potable, Alcantarillado)
    path('servicios-publicos/', include('servicios_publicos.urls')),
    
    # Aplicaciones legacy dentro de tributario
    path('administrativo-app/', include('administrativo_app.urls', namespace='administrativo_app')),
]

if getattr(settings, "DEBUG", False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for catastro project.

Este archivo es el punto de entrada principal de URLs.
Las URLs específicas del módulo están en el urls.py del directorio padre.
"""
from django.contrib import admin
from django.urls import path, include
import sys
import os

# Agregar el directorio padre al path para importar el urls.py del módulo
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Importar directamente las URLs del módulo catastro desde el directorio padre
# Esto permite que Django encuentre las URLs del módulo
try:
    # Importar el módulo urls del directorio padre
    import importlib.util
    urls_file = os.path.join(parent_dir, 'urls.py')
    if os.path.exists(urls_file):
        spec = importlib.util.spec_from_file_location("catastro_urls_module", urls_file)
        catastro_urls_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(catastro_urls_module)
        # Usar las URL patterns del módulo
        urlpatterns = [
            path('admin/', admin.site.urls),
        ] + getattr(catastro_urls_module, 'urlpatterns', [])
    else:
        raise ImportError("No se encontró urls.py en el directorio padre")
except Exception as e:
    # Fallback: usar include (requiere que catastro esté en INSTALLED_APPS)
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('catastro.urls')),
    ]


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

urlpatterns = [
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

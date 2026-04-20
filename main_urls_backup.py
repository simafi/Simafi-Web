from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Test Calculadora ICS
    path('test-calculadora-ics/', lambda request: HttpResponse(open(r'C:\simafiweb\test_calculadora_ics.html', 'r', encoding='utf-8').read(), content_type='text/html'), name='test_calculadora_ics'),
    path('admin/', admin.site.urls),
    path('', include('modules.core.urls')),  # Sistema principal (login y menú)
    path('catastro/', include('modules.catastro.urls')),  # Módulo de catastro
    path('tributario/', include('modules.tributario.urls', namespace='tributario')),  # Módulo tributario
    path('administrativo/', include('modules.administrativo.urls')),  # Módulo administrativo
    path('contabilidad/', include('modules.contabilidad.urls')),  # Módulo contabilidad
    path('tesoreria/', include('modules.tesoreria.urls')),  # Módulo tesorería
    path('presupuestos/', include('modules.presupuestos.urls')),  # Módulo presupuestos
    path('ambiental/', include('modules.ambiental.urls')),  # Módulo ambiental
    path('servicios-publicos/', include('modules.servicios_publicos.urls')),  # Módulo servicios públicos
    path('convenios-pagos/', include('modules.conveniopagos.urls')),  # Módulo convenios de pagos
    path('configuracion/', include('modules.configuracion.urls')),  # Módulo configuración
    path('reportes/', include('modules.reportes.urls')),  # Módulo reportes
    path('api/', include('modules.api.urls')),  # API
]

# Configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

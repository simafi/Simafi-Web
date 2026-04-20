from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'administrativo_app'

urlpatterns = [
    # Raíz legacy: el módulo vive en /administrativo/ (hub de gestión)
    path(
        '',
        RedirectView.as_view(url='/administrativo/', permanent=False),
        name='administrativo_app_redirect',
    ),
    path('departamento/', views.departamento_crud, name='departamento_crud'),
    path('ajax/buscar-departamento/', views.buscar_departamento, name='buscar_departamento'),
]

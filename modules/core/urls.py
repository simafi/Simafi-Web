from django.urls import path
from django.http import HttpResponse
from django.views.generic import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.login_principal, name='login_principal'),
    path('login/', views.login_principal, name='login_principal'),
    path('menu/', views.menu_principal, name='menu_principal'),
    path('logout/', views.logout_principal, name='logout_principal'),
    path('verificar-sesion/', views.verificar_sesion, name='verificar_sesion'),
    
    # Favicon - retornar respuesta vacía para evitar error 404
    path('favicon.ico', lambda request: HttpResponse(status=204), name='favicon'),
]


































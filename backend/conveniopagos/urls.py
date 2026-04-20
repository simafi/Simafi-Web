from django.urls import path
from . import views

app_name = 'conveniopagos'

urlpatterns = [
    path('', views.conveniopagos_login, name='conveniopagos_login'),
    path('login/', views.conveniopagos_login, name='conveniopagos_login'),
    path('logout/', views.conveniopagos_logout, name='conveniopagos_logout'),
    path('menu/', views.conveniopagos_menu_principal, name='conveniopagos_menu_principal'),
]


































from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.reportes_login, name='reportes_login'),
    path('login/', views.reportes_login, name='reportes_login'),
    path('logout/', views.reportes_logout, name='reportes_logout'),
    path('menu/', views.reportes_menu_principal, name='reportes_menu_principal'),
]


































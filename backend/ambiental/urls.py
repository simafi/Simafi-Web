from django.urls import path
from . import views

app_name = 'ambiental'

urlpatterns = [
    path('', views.ambiental_login, name='ambiental_login'),
    path('login/', views.ambiental_login, name='ambiental_login'),
    path('logout/', views.ambiental_logout, name='ambiental_logout'),
    path('menu/', views.ambiental_menu_principal, name='ambiental_menu_principal'),
]


































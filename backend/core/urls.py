from django.urls import path
from . import views

app_name = 'modules_core'

urlpatterns = [
    # Menú modular público (sin sesión); login solo en /login/ antes de entrar a módulos protegidos
    path('', views.menu_principal, name='menu_principal'),
    path('menu/', views.menu_principal, name='menu_principal_menu'),
    path('login/', views.login_principal, name='login_principal'),
    path('logout/', views.logout_principal, name='logout_principal'),
    path('verificar-sesion/', views.verificar_sesion, name='verificar_sesion'),
    path('acceso-modulo/<str:codigo>/', views.acceso_modulo, name='acceso_modulo'),
    # Rutas bajo menu/* antes que menu/ para evitar ambigüedad en el resolvedor
    path('menu/usuarios-sistema/', views.usuarios_sistema_list, name='usuarios_sistema_list'),
    path('menu/usuarios-sistema/nuevo/', views.usuarios_sistema_create, name='usuarios_sistema_create'),
    path('menu/usuarios-sistema/<int:pk>/editar/', views.usuarios_sistema_update, name='usuarios_sistema_update'),
    path('menu/roles/', views.roles_list, name='roles_list'),
    path('menu/roles/nuevo/', views.roles_create, name='roles_create'),
    path('menu/roles/<int:pk>/editar/', views.roles_update, name='roles_update'),
    path('menu/roles/<int:pk>/eliminar/', views.roles_delete, name='roles_delete'),
]


































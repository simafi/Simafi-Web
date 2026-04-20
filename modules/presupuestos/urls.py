from django.urls import path
from . import views

app_name = 'presupuestos'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_presupuestos, name='dashboard'),

    # Presupuesto de Ingresos
    path('ingresos/', views.lista_ingresos, name='lista_ingresos'),
    path('ingresos/crear/', views.crear_ingreso, name='crear_ingreso'),
    path('ingresos/<int:pk>/editar/', views.editar_ingreso, name='editar_ingreso'),

    # Presupuesto de Gastos
    path('gastos/', views.lista_gastos, name='lista_gastos'),
    path('gastos/crear/', views.crear_gasto, name='crear_gasto'),
    path('gastos/<int:pk>/editar/', views.editar_gasto, name='editar_gasto'),

    # Ejecución Presupuestaria
    path('ejecucion/', views.lista_ejecucion, name='lista_ejecucion'),
    path('ejecucion/crear/', views.crear_ejecucion, name='crear_ejecucion'),

    # Modificaciones Presupuestarias
    path('modificaciones/', views.lista_modificaciones, name='lista_modificaciones'),
    path('modificaciones/crear/', views.crear_modificacion, name='crear_modificacion'),

    # API endpoints
    path('api/ingresos/<int:ano>/', views.api_ingresos_por_ano, name='api_ingresos_por_ano'),
    path('api/gastos/<int:ano>/', views.api_gastos_por_ano, name='api_gastos_por_ano'),
]
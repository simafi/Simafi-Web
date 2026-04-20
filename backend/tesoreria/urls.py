from django.urls import path
from . import views

app_name = 'tesoreria'

urlpatterns = [
    path('', views.tesoreria_login, name='tesoreria_login'),
    path('login/', views.tesoreria_login, name='tesoreria_login'),
    path('logout/', views.tesoreria_logout, name='tesoreria_logout'),
    path('menu/', views.tesoreria_menu_principal, name='tesoreria_menu_principal'),
    path('caja/', views.caja_cobros, name='caja_cobros'),
    path('caja/cierre-diario/', views.cierre_diario_caja, name='cierre_diario_caja'),
    path('caja/resumen-facturas/', views.resumen_facturas_caja, name='resumen_facturas_caja'),
    # Configuración de cuentas de Caja/Banco/Chequera
    path('cuentas-tesoreria/', views.cuentas_tesoreria, name='cuentas_tesoreria'),
    path('cuentas-tesoreria/crear/', views.cuenta_tesoreria_crear, name='cuenta_tesoreria_crear'),
    path('cuentas-tesoreria/<int:pk>/editar/', views.cuenta_tesoreria_editar, name='cuenta_tesoreria_editar'),
    # Emisión de pagos vinculando órdenes de pago
    path("pagos/", views.pagos_tesoreria, name="pagos_tesoreria"),
    # Control de Cheques (Entregas y Anulaciones)
    path("cheques-control/", views.gestionar_cheques, name="gestionar_cheques"),
    # Depósitos y Notas
    path("depositos/", views.depositos_tesoreria, name="depositos_tesoreria"),
    # Notas Bancarias
    path("notas/", views.notas_tesoreria, name="notas_tesoreria"),
    # Conciliación Bancaria
    path("conciliacion/", views.conciliacion_bancaria, name="conciliacion_bancaria"),
    path("conciliacion/<int:pk>/detalle/", views.detalle_conciliacion, name="detalle_conciliacion"),
    # Consultas y Reportes
    path("consultar-ordenes-pago/", views.consultar_ordenes_pago, name="consultar_ordenes_pago"),
]


































from django.urls import path
from . import views
from . import rendicion_views

app_name = 'presupuestos'

urlpatterns = [
    path('', views.presupuestos_login, name='presupuestos_root'),
    path('login/', views.presupuestos_login, name='presupuestos_login'),
    path('logout/', views.presupuestos_logout, name='presupuestos_logout'),
    path('menu/', views.presupuestos_menu_principal, name='presupuestos_menu_principal'),
    path('fondos/', views.fondos, name='fondos'),
    path('ingresos/', views.catalogo_presupuestario, {'tipo': 'ingreso'}, name='cuentas_ingresos'),
    path('egresos/', views.catalogo_presupuestario, {'tipo': 'egreso'}, name='cuentas_egresos'),
    path('presupuesto-anual/', views.presupuesto_anual, name='presupuesto_anual'),
    path("reformas/", views.reformas_listado, name="reformas_listado"),
    path("reformas/nueva/<str:tipo_reforma>/", views.gestionar_reforma, name="gestionar_reforma"),
    path('proyectos-inversion/', views.proyectos_inversion, name='proyectos_inversion'),
    path('ordenes-pago/', views.ordenes_pago, name='ordenes_pago'),
    # Nuevas opciones del menú modular
    path("compromisos/", views.gestionar_compromisos, name="gestionar_compromisos"),
    path("operaciones-manuales/", views.gestionar_operacion_manual, name="gestionar_operacion_manual"),
    path("informes/", views.informes_presupuestarios, name="informes_presupuestarios"),
    path("informes/ingresos/", views.informes_ingresos_hub, name="informes_ingresos_hub"),
    path("informes/ingresos/ejecucion-general/", views.reporte_ejecucion_general, name="reporte_ejecucion_general"),
    path("informes/ingresos/ejecucion-periodo/", views.reporte_ejecucion_periodo, name="reporte_ejecucion_periodo"),
    path("informes/ingresos/resumen-mensual/", views.reporte_mensual_ingresos, name="reporte_mensual_ingresos"),
    path("informes/ingresos/reformas-ampliaciones/", views.reporte_reformas_ampliaciones, name="reporte_reformas_ampliaciones"),
    path("informes/ingresos/reformas-traspasos/", views.reporte_reformas_traspasos, name="reporte_reformas_traspasos"),
    path("informes/ingresos/liquidacion-f01/", views.reporte_liquidacion_f01, name="reporte_liquidacion_f01"),
    path("informes/ingresos/consulta-cuenta/", views.consulta_por_cuenta, name="consulta_por_cuenta"),
    path("rendicion-cuentas/", rendicion_views.rendicion_cuentas_hub, name="rendicion_cuentas_hub"),
    path("rendicion-cuentas/forma/<int:num>/", rendicion_views.rendicion_forma, name="rendicion_forma"),
    path("rendicion-cuentas/iaip/<int:num>/", rendicion_views.rendicion_iaip_forma, name="rendicion_iaip_forma"),
    path(
        "rendicion-cuentas/cgr/<int:num>/",
        rendicion_views.redirect_cgr_a_contabilidad,
        name="rendicion_cgr_forma",
    ),
]















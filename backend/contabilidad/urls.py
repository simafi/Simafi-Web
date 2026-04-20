from django.urls import path
from . import views
from . import cgr_views

app_name = 'contabilidad'

urlpatterns = [
    # Login / Menú
    path('', views.contabilidad_login, name='contabilidad_login'),
    path('login/', views.contabilidad_login, name='contabilidad_login_page'),
    path('logout/', views.contabilidad_logout, name='contabilidad_logout'),
    path('menu/', views.contabilidad_menu_principal, name='contabilidad_menu_principal'),
    path('configuracion-inicial/', views.configuracion_inicial, name='configuracion_inicial'),

    # Plan de Cuentas (Marco Conceptual / NIC 1)
    path('plan-cuentas/', views.plan_cuentas, name='plan_cuentas'),
    path('plan-cuentas/crear/', views.cuenta_crear, name='cuenta_crear'),
    path('plan-cuentas/<int:pk>/editar/', views.cuenta_editar, name='cuenta_editar'),
    path('plan-cuentas/<int:pk>/eliminar/', views.cuenta_eliminar, name='cuenta_eliminar'),

    # Asientos Contables (NIC 1 - Libro Diario)
    path('asientos/', views.asientos_lista, name='asientos_lista'),
    path('asientos/crear/', views.asiento_crear, name='asiento_crear'),
    path('asientos/<int:pk>/', views.asiento_ver, name='asiento_ver'),
    path('asientos/<int:pk>/aprobar/', views.asiento_aprobar, name='asiento_aprobar'),
    path('asientos/<int:pk>/contabilizar/', views.asiento_contabilizar, name='asiento_contabilizar'),

    # Libro Mayor
    path('libro-mayor/', views.libro_mayor, name='libro_mayor'),

    # Estados Financieros (NIC 1)
    path('estados-financieros/', views.estados_financieros, name='estados_financieros'),
    path('estados-financieros/balance-general-comparativo/', views.balance_general_comparativo, name='balance_general_comparativo'),
    path('estados-financieros/estado-resultados-comparativo/', views.estado_resultados_comparativo, name='estado_resultados_comparativo'),
    path('balanza-comprobacion/', views.balanza_comprobacion, name='balanza_comprobacion'),

    # Activos Fijos (NIC 16)
    path('activos-fijos/', views.activos_fijos, name='activos_fijos'),
    path('activos-fijos/crear/', views.activo_fijo_crear, name='activo_fijo_crear'),

    # Inventarios (NIC 2)
    path('inventarios/', views.inventarios, name='inventarios'),
    path('inventarios/nuevo/', views.inventario_crear, name='inventario_crear'),
    path('inventarios/<int:pk>/editar/', views.inventario_editar, name='inventario_editar'),
    path('inventarios/tipos/', views.tipo_inventario_list, name='tipo_inventario_list'),
    path('inventarios/tipos/nuevo/', views.tipo_inventario_crear, name='tipo_inventario_crear'),
    path('inventarios/tipos/<int:pk>/editar/', views.tipo_inventario_editar, name='tipo_inventario_editar'),
    path('inventarios/tipos/referencias-cargar/', views.tipo_inventario_referencias_cargar, name='tipo_inventario_referencias_cargar'),

    # Ejercicios Fiscales
    path('ejercicios/', views.ejercicios_fiscales, name='ejercicios_fiscales'),
    path('ejercicios/crear/', views.ejercicio_crear, name='ejercicio_crear'),

    # Centros de Costo
    path('centros-costo/', views.centros_costo, name='centros_costo'),

    # AJAX
    path('ajax/buscar-cuentas/', views.ajax_buscar_cuentas, name='ajax_buscar_cuentas'),
    path('ajax/saldo-cuenta/', views.ajax_saldo_cuenta, name='ajax_saldo_cuenta'),
    path('ajax/cuenta-por-codigo/', views.ajax_cuenta_por_codigo, name='ajax_cuenta_por_codigo'),

    # Informes CGR (Contraloría General de la República) — datos desde presupuestos
    path('informes-cgr/', cgr_views.cgr_informes_hub, name='cgr_informes_hub'),
    path('informes-cgr/<int:num>/', cgr_views.cgr_informe_forma, name='cgr_informe_forma'),
]

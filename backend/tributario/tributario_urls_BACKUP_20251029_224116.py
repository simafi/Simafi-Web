from django.urls import path
from . import views
# Importación ABSOLUTA para evitar que Django registre modelos como tributario.tributario_app
from tributario_app import views as tributario_app_views
from . import simple_views
from . import ajax_views

app_name = 'tributario'

urlpatterns = [
    # Login del módulo tributario
    path('', views.tributario_login, name='tributario_login'),
    path('login/', views.tributario_login, name='tributario_login'),
    
    # Menú principal del módulo tributario
    path('menu/', views.tributario_menu_principal, name='tributario_menu_principal'),
    
    # Logout del módulo tributario
    path('logout/', views.tributario_logout, name='tributario_logout'),
    
    # Vistas del sistema tributario
    path('test-simple/', views.test_simple, name='test_simple'),
    path('maestro-negocios/', views.maestro_negocios, name='maestro_negocios'),
    path('buscar-negocio-ajax/', views.buscar_negocio_ajax, name='buscar_negocio_ajax'),
    path('buscar-identificacion-ajax/', views.buscar_identificacion, name='buscar_identificacion_ajax'),
    path('tarifas/', views.tarifas_crud, name='tarifas'),
    path('declaraciones/', simple_views.declaracion_volumen, name='declaracion_volumen'),
    path('api/buscar-declaracion/', simple_views.buscar_declaracion_existente, name='buscar_declaracion_existente'),
    path('reportes/', views.informes, name='informes'),
    
    # URLs adicionales requeridas por el template
    path('cierre-anual/', views.cierre_anual, name='cierre_anual'),
    path('cargo-anual/', views.cargo_anual, name='cargo_anual'),
    path('recargos-moratorios/', views.recargos_moratorios, name='recargos_moratorios'),
    path('miscelaneos/', views.miscelaneos, name='miscelaneos'),
    path('convenios-pagos/', views.convenios_pagos, name='convenios_pagos'),
    path('actividad-crud/', views.actividad_crud, name='actividad_crud'),
    path('oficina-crud/', views.oficina_crud, name='oficina_crud'),
    path('rubros-crud/', tributario_app_views.rubros_crud, name='rubros_crud'),
    path('tarifas-crud/', views.tarifas_crud, name='tarifas_crud'),
    path('configurar-tasas-negocio/', simple_views.configurar_tasas_negocio, name='configurar_tasas_negocio'),
    
    # URLs AJAX para funcionalidades específicas
    path('obtener-tarifas-rubro/', simple_views.obtener_tarifas_rubro, name='obtener_tarifas_rubro'),
    path('obtener-datos-rubro/', simple_views.obtener_datos_rubro, name='obtener_datos_rubro'),
    path('obtener-actividades-ajax/', simple_views.obtener_actividades_ajax, name='obtener_actividades_ajax'),
    path('obtener-cuenta-rezago/', views.obtener_cuenta_rezago, name='obtener_cuenta_rezago'),
    path('verificar-tarifa-existente/', views.verificar_tarifa_existente, name='verificar_tarifa_existente'),
    path('buscar-identificacion-representante/', views.buscar_identificacion_representante, name='buscar_identificacion_representante'),
    path('api-tarifas-ics/', views.api_tarifas_ics, name='api_tarifas_ics'),
    path('calcular-tasas-ajax/', views.calcular_tasas_ajax, name='calcular_tasas_ajax'),
    path('obtener-tarifas-rubro-ajax/', views.obtener_tarifas_rubro_ajax, name='obtener_tarifas_rubro_ajax'),
    path('obtener-tarifas-escalonadas/', views.obtener_tarifas_escalonadas, name='obtener_tarifas_escalonadas'),
    
    # URLs para Plan Arbitrio
    path('plan-arbitrio/', views.plan_arbitrio, name='plan_arbitrio'),
    path('plan-arbitrio-crud/', views.plan_arbitrio_crud, name='plan_arbitrio_crud'),
    path('buscar-plan-arbitrio/', views.buscar_plan_arbitrio, name='buscar_plan_arbitrio'),
    path('buscar-plan-arbitrio-por-codigo/', views.buscar_plan_arbitrio_por_codigo, name='buscar_plan_arbitrio_por_codigo'),
    path('buscar-rubro-plan-arbitrio/', views.buscar_rubro_plan_arbitrio, name='buscar_rubro_plan_arbitrio'),
    path('buscar-tarifa-plan-arbitrio/', views.buscar_tarifa_plan_arbitrio, name='buscar_tarifa_plan_arbitrio'),
    
    # URLs para búsquedas específicas
    path('buscar-tarifa/', views.buscar_tarifa, name='buscar_tarifa'),
    path('buscar-tarifa-automatica/', views.buscar_tarifa_automatica, name='buscar_tarifa_automatica'),
    path('buscar-rubro/', views.buscar_rubro, name='buscar_rubro'),
    
    # URLs para misceláneos
    path('buscar-actividad/', views.buscar_actividad, name='buscar_actividad'),
    path('cargar-actividades/', views.cargar_actividades, name='cargar_actividades'),
    path('buscar-oficina/', views.buscar_oficina_ajax, name='buscar_oficina'),
    path('buscar-concepto-miscelaneos/', views.buscar_concepto_miscelaneos, name='buscar_concepto_miscelaneos'),
    path('enviar-a-caja/', tributario_app_views.enviar_a_caja, name='enviar_a_caja'),
    path('generar-soporte-transaccion/', views.generar_soporte_transaccion, name='generar_soporte_transaccion'),
    path('soporte/<str:numero_recibo>/', views.ver_soporte, name='ver_soporte'),
    
    # URL para cálculo temporal de tasas según plan de arbitrios
    path('ajax/calcular-tasas-plan-arbitrio/', ajax_views.calcular_tasas_plan_arbitrio, name='calcular_tasas_plan_arbitrio'),
]

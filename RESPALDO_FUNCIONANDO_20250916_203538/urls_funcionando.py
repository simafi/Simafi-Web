from django.urls import path
from . import views
from . import ajax_views
from . import tarifas_ajax
from . import tarifas_ajax_simple
from . import tarifas_reales
from . import simple_views

app_name = 'tributario'

urlpatterns = [
    path('', views.tributario_menu_principal, name='tributario_login'),
    path('login/', views.tributario_menu_principal, name='tributario_login_alt'),
    path('logout/', views.tributario_logout, name='tributario_logout'),
    path('menu/', views.tributario_menu_principal, name='tributario_menu_principal'),
    
    # URLs para las funcionalidades del menugeneral.html
    path('maestro-negocios/', views.maestro_negocios, name='maestro_negocios'),
    path('buscar-negocio/', views.buscar_negocio_ajax, name='buscar_negocio_ajax'),
    path('cierre-anual/', simple_views.cierre_anual, name='cierre_anual'),
    path('cargo-anual/', simple_views.cargo_anual, name='cargo_anual'),
    path('recargos-moratorios/', simple_views.recargos_moratorios, name='recargos_moratorios'),
    path('informes/', simple_views.informes, name='informes'),
    path('declaracion-volumen/', simple_views.declaracion_volumen, name='declaracion_volumen'),
    path('miscelaneos/', simple_views.miscelaneos, name='miscelaneos'),
    path('convenios-pagos/', simple_views.convenios_pagos, name='convenios_pagos'),
    path('actividad-crud/', simple_views.actividad_crud, name='actividad_crud'),
    path('oficina-crud/', simple_views.oficina_crud, name='oficina_crud'),
    path('rubros-crud/', views.rubros_crud, name='rubros_crud'),
    path('tarifas-crud/', simple_views.tarifas_crud, name='tarifas_crud'),
    # URLs de plan de arbitrio eliminadas - usar tributario_app en su lugar
    # path('plan-arbitrio-crud/', simple_views.plan_arbitrio_crud, name='plan_arbitrio_crud'),
    # path('buscar-rubro-plan-arbitrio/', simple_views.simple_ajax, name='buscar_rubro_plan_arbitrio'),
    # path('buscar-tarifa-plan-arbitrio/', simple_views.simple_ajax, name='buscar_tarifa_plan_arbitrio'),
    # path('plan-arbitrio/', simple_views.plan_arbitrio, name='plan_arbitrio'),
    path('buscar-tarifa/', views.buscar_tarifa, name='buscar_tarifa'),
    path('buscar-tarifa-automatica/', simple_views.simple_ajax, name='buscar_tarifa_automatica'),
    path('buscar-plan-arbitrio/', views.buscar_plan_arbitrio_por_codigo, name='buscar_plan_arbitrio'),
    path('buscar-plan-arbitrio-por-codigo/', simple_views.simple_ajax, name='buscar_plan_arbitrio_por_codigo'),
    path('buscar-rubro/', views.buscar_rubro, name='buscar_rubro'),
    
    # URLs para búsqueda de identificación
    path('buscar-identificacion/', simple_views.buscar_identificacion, name='buscar_identificacion'),
    path('buscar-identificacion-representante/', simple_views.simple_ajax, name='buscar_identificacion_representante'),
    
    # URL para búsqueda de actividades AJAX
    path('ajax/buscar-actividad/', ajax_views.buscar_actividad_ajax, name='buscar_actividad_ajax'),
    
    # URL para búsqueda de oficinas AJAX
    path('ajax/buscar-oficina/', ajax_views.buscar_oficina_ajax, name='buscar_oficina_ajax'),
    
    # URL para cargar actividades por empresa AJAX
    path('ajax/cargar-actividades/', ajax_views.cargar_actividades_ajax, name='cargar_actividades_ajax'),
    
    # URLs para configuración de tasas de negocios
    path('configurar-tasas-negocio/', simple_views.configurar_tasas_negocio, name='configurar_tasas_negocio'),
    path('obtener-tarifas-rubro/', simple_views.obtener_tarifas_rubro, name='obtener_tarifas_rubro'),
    path('obtener-tarifas-escalonadas/', tarifas_ajax_simple.obtener_tarifas_escalonadas_simple, name='obtener_tarifas_escalonadas'),
    path('obtener-tarifas-reales/', tarifas_reales.obtener_tarifas_reales, name='obtener_tarifas_reales'),
    
    # URL para validación de plan de arbitrio
    path('validar-plan-arbitrio/', simple_views.validar_plan_arbitrio, name='validar_plan_arbitrio'),
    
    # API para obtener tarifas ICS desde tabla tarifasimptoics
    path('api/tarifas-ics/', views.api_tarifas_ics, name='api_tarifas_ics'),
]

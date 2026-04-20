from django.urls import path
from django.http import HttpResponse
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
    path('cierre-anual/', simple_views.simple_render, name='cierre_anual'),
    path('cargo-anual/', simple_views.simple_render, name='cargo_anual'),
    path('recargos-moratorios/', simple_views.simple_render, name='recargos_moratorios'),
    path('informes/', simple_views.simple_render, name='informes'),
    path('declaracion-volumen/', simple_views.declaracion_volumen, name='declaracion_volumen'),
    path('declaraciones/', simple_views.declaracion_volumen, name='declaraciones'),
    path('eliminar_declaracion/<int:declaracion_id>/', simple_views.eliminar_declaracion, name='eliminar_declaracion'),
    path('miscelaneos/', simple_views.simple_render, name='miscelaneos'),
    path('convenios-pagos/', simple_views.simple_render, name='convenios_pagos'),
    path('actividad-crud/', views.actividad_crud, name='actividad_crud'),
    path('oficina-crud/', views.oficina_crud, name='oficina_crud'),
    path('rubros-crud/', views.rubros_crud, name='rubros_crud'),
    path('tarifas-crud/', simple_views.simple_render, name='tarifas_crud'),
    path('plan-arbitrio-crud/', simple_views.simple_render, name='plan_arbitrio_crud'),
    path('buscar-rubro-plan-arbitrio/', simple_views.simple_ajax, name='buscar_rubro_plan_arbitrio'),
    path('buscar-tarifa-plan-arbitrio/', simple_views.simple_ajax, name='buscar_tarifa_plan_arbitrio'),
    path('plan-arbitrio/', simple_views.simple_render, name='plan_arbitrio'),
    path('buscar-tarifa/', simple_views.simple_ajax, name='buscar_tarifa'),
    path('buscar-tarifa-automatica/', simple_views.simple_ajax, name='buscar_tarifa_automatica'),
    path('buscar-plan-arbitrio/', simple_views.simple_ajax, name='buscar_plan_arbitrio'),
    path('buscar-plan-arbitrio-por-codigo/', simple_views.simple_ajax, name='buscar_plan_arbitrio_por_codigo'),
    path('buscar-rubro/', simple_views.simple_ajax, name='buscar_rubro'),
    
    # URLs para búsqueda de identificación
    path('buscar-identificacion/', simple_views.simple_ajax, name='buscar_identificacion'),
    path('buscar-identificacion-representante/', simple_views.simple_ajax, name='buscar_identificacion_representante'),
    
    # URL para búsqueda de actividades AJAX
    path('ajax/buscar-actividad/', ajax_views.buscar_actividad_ajax, name='buscar_actividad_ajax'),
    path('buscar-actividad/', ajax_views.buscar_actividad_ajax, name='buscar_actividad'),  # Ruta alternativa
    
    # URL para búsqueda de oficinas AJAX
    path('ajax/buscar-oficina/', ajax_views.buscar_oficina_ajax, name='buscar_oficina_ajax'),
    
    # URL para búsqueda de rubros AJAX
    path('ajax/buscar-rubro/', ajax_views.buscar_rubro_ajax, name='buscar_rubro_ajax'),
    path('buscar-oficina/', ajax_views.buscar_oficina_ajax, name='buscar_oficina'),
    
    # URL para cargar actividades por empresa AJAX
    path('ajax/cargar-actividades/', ajax_views.cargar_actividades_ajax, name='cargar_actividades_ajax'),
    
    # URL para búsqueda de actividades por descripción/nombre
    path('ajax/buscar-actividades-descripcion/', ajax_views.buscar_actividades_por_descripcion_ajax, name='buscar_actividades_descripcion_ajax'),
    
    # URLs para configuración de tasas de negocios
    path('configurar-tasas-negocio/', simple_views.configurar_tasas_negocio, name='configurar_tasas_negocio'),
    path('obtener-tarifas-rubro/', simple_views.obtener_tarifas_rubro, name='obtener_tarifas_rubro'),
    path('obtener-tarifas-escalonadas/', tarifas_ajax_simple.obtener_tarifas_escalonadas_simple, name='obtener_tarifas_escalonadas'),
    path('obtener-tarifas-reales/', tarifas_reales.obtener_tarifas_reales, name='obtener_tarifas_reales'),
    
    # URL para validación de plan de arbitrio
    path('validar-plan-arbitrio/', simple_views.validar_plan_arbitrio, name='validar_plan_arbitrio'),
    
    # URL para cálculo temporal de tasas según plan de arbitrios
    path('ajax/calcular-tasas-plan-arbitrio/', ajax_views.calcular_tasas_plan_arbitrio, name='calcular_tasas_plan_arbitrio'),
    path('estado-cuenta/', views.estado_cuenta, name='estado_cuenta'),
    path('buscar-negocios-listado/', views.buscar_negocios_listado, name='buscar_negocios_listado'),
    path('calcular-transaccion-pago/', views.calcular_transaccion_pago, name='calcular_transaccion_pago'),
    path('guardar-transaccion-pago/', views.guardar_transaccion_pago, name='guardar_transaccion_pago'),
    
    # Favicon - retornar respuesta vacía para evitar error 404
    path('favicon.ico', lambda request: HttpResponse(status=204), name='favicon'),
]

from django.http import JsonResponse
# Negocio model moved to modular system
from django.urls import path, include
from tributario_app import views
from tributario import views as mod_trib_views

# Definir el nombre de la aplicación para el namespace
app_name = 'tributario_app'

from tributario_app.views import (
    login_view, menu_general,
    bienes_inmuebles, industria_comercio_servicios,
    miscelaneos, convenios_pagos, utilitarios,
    maestro_negocios, maestro_negocios_simple, maestro_negocios_corregido, maestro_negocios_simple_v2, declaracion_volumen,
    cierre_anual, cargo_anual, recargos_moratorios,
    informes, logout_view, enviar_a_caja,
    generar_soporte_transaccion, oficina_crud, buscar_oficina,
    buscar_negocio, cargar_actividades, buscar_identificacion,
    rubros_crud, buscar_rubro, plan_arbitrio_crud, buscar_plan_arbitrio, buscar_plan_arbitrio_por_codigo,
    tipocategoria_crud, grabar_plan_arbitrio_ajax,
    buscar_rubro_plan_arbitrio, tarifas_crud, buscar_tarifa, buscar_tarifa_automatica,
    buscar_tarifa_plan_arbitrio, buscar_concepto_miscelaneos, configurar_tasas_negocio, obtener_tarifas_rubro,
    calcular_impuesto_productos_controlados_ajax, gestionar_mora_bienes
)

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def parse_fecha(fecha_str):
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except Exception:
        return None


urlpatterns = [
    path('', login_view, name='tributario_login'),
    path('login/', login_view, name='login'),
    path('menu/', menu_general, name='tributario_menu_principal'),
    path('menu-general/', menu_general, name='menu_general'),
    # Alias para acceder a Servicios Públicos desde /tributario/
    path('servicios-publicos/', include('servicios_publicos.urls', namespace='servicios_publicos')),
    path('impuesto-personal/', include('tributario.impuesto_personal.urls', namespace='impuesto_personal')),
    path('bienes-inmuebles/', bienes_inmuebles, name='bienes_inmuebles'),
    path('gestionar-mora-bienes/', gestionar_mora_bienes, name='gestionar_mora_bienes'),
    path('industria-comercio-servicios/', industria_comercio_servicios, name='industria_comercio_servicios'),
    path('miscelaneos/', miscelaneos, name='miscelaneos'),
    path('convenios-pagos/', convenios_pagos, name='convenios_pagos'),
    path('utilitarios/', utilitarios, name='utilitarios'),
    path('maestro_negocios/', maestro_negocios, name='maestro_negocios'),
    path('maestro_negocios_simple/', maestro_negocios_simple, name='maestro_negocios_simple'),
    path('maestro_negocios_corregido/', maestro_negocios_corregido, name='maestro_negocios_corregido'),
    path('maestro_negocios_simple_v2/', maestro_negocios_simple_v2, name='maestro_negocios_simple_v2'),
    path('declaracion-volumen/', declaracion_volumen, name='declaracion_volumen'),
    path('cierre-anual/', cierre_anual, name='cierre_anual'),
    path('cargo-anual/', cargo_anual, name='cargo_anual'),
    path('recargos-moratorios/', recargos_moratorios, name='recargos_moratorios'),
    path('informes/', informes, name='informes'),
    path('logout/', logout_view, name='tributario_logout'),
    path('ajax/buscar-negocio/', views.buscar_negocio, name='buscar_negocio'),
    path('ajax/convertir-utm-a-latlng/', views.convertir_utm_a_latlng, name='convertir_utm_a_latlng'),
    path('ajax/cargar-actividades/', views.cargar_actividades, name='cargar_actividades'),
    path('ajax/buscar-identificacion/', views.buscar_identificacion, name='buscar_identificacion'),
    path('ajax/enviar-a-caja/', views.enviar_a_caja, name='enviar_a_caja'),
    path('enviar-a-caja-bienes/', views.enviar_a_caja_bienes, name='enviar_a_caja_bienes'),
    # Diagnóstico rápido (producción): Bienes Inmuebles / Supabase
    path('__diag/bienes-inmuebles/', views.diag_bienes_inmuebles, name='diag_bienes_inmuebles'),
    path('ajax/generar-soporte-transaccion/', views.generar_soporte_transaccion, name='generar_soporte_transaccion'),
    path('soporte-transaccion/', views.generar_soporte_transaccion, name='soporte_transaccion_directo'),
    path('actividad/', views.actividad_crud, name='actividad_crud'),
    path('ajax/buscar-actividad/', views.buscar_actividad, name='buscar_actividad'),
    path('oficina/', views.oficina_crud, name='oficina_crud'),
    path('ajax/buscar-oficina/', views.buscar_oficina, name='buscar_oficina'),
    path('rubros/', views.rubros_crud, name='rubros_crud'),
    path('ajax/buscar-rubro/', views.buscar_rubro, name='buscar_rubro'),
    path('tipocategoria/', views.tipocategoria_crud, name='tipocategoria_crud'),
    path('ajax/grabar-plan-arbitrio/', views.grabar_plan_arbitrio_ajax, name='grabar_plan_arbitrio_ajax'),
    path('plan-arbitrio/', views.plan_arbitrio_crud, name='plan_arbitrio_crud'),
    path('ajax/buscar-plan-arbitrio/', views.buscar_plan_arbitrio, name='buscar_plan_arbitrio'),
    path('ajax/buscar-plan-arbitrio-por-codigo/', views.buscar_plan_arbitrio_por_codigo, name='buscar_plan_arbitrio_por_codigo'),
    path('ajax/buscar-rubro-plan-arbitrio/', views.buscar_rubro_plan_arbitrio, name='buscar_rubro_plan_arbitrio'),
    path('ajax/buscar-tarifa-plan-arbitrio/', views.buscar_tarifa_plan_arbitrio, name='buscar_tarifa_plan_arbitrio'),
    path('ajax/obtener-tipomodulo-tarifa/', views.obtener_tipomodulo_tarifa, name='obtener_tipomodulo_tarifa'),
    path('tarifas/', views.tarifas_crud, name='tarifas_crud'),
    path('ajax/buscar-tarifa/', views.buscar_tarifa, name='buscar_tarifa'),
    path('ajax/buscar-tarifa-automatica/', views.buscar_tarifa_automatica, name='buscar_tarifa_automatica'),
    path('ajax/buscar-concepto-miscelaneos/', views.buscar_concepto_miscelaneos, name='buscar_concepto_miscelaneos'),
    # path('calcular-tasas/', calcular_tasas_ajax, name='calcular_tasas_ajax'),  # Deshabilitado para evitar conflictos
    path('ajax/obtener-tarifas-rubro/', views.obtener_tarifas_rubro, name='obtener_tarifas_rubro_ajax'),
    path('obtener-tarifas-escalonadas/', views.obtener_tarifas_escalonadas, name='obtener_tarifas_escalonadas'),
    path('ajax/calcular-impuesto-productos-controlados/', views.calcular_impuesto_productos_controlados_ajax, name='calcular_impuesto_productos_controlados'),
    path('configurar-tasas-negocio/', views.configurar_tasas_negocio, name='configurar_tasas_negocio'),
    path('obtener-cuenta-rezago/', views.obtener_cuenta_rezago, name='obtener_cuenta_rezago'),
    path('verificar-tarifa-existente/', views.verificar_tarifa_existente, name='verificar_tarifa_existente'),
    # Compatibilidad Estado de Cuenta
    path('estado-cuenta/', mod_trib_views.estado_cuenta, name='estado_cuenta_compat'),
    
#    path('api/buscar_negocio/', views.buscar_negocio, name='buscar_negocio')

]


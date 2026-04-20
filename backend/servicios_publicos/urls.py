"""
URLs para el módulo de Servicios Públicos / Facturación de Agua
"""
from django.urls import path
from django.http import HttpResponse
from . import views

app_name = 'servicios_publicos'

urlpatterns = [
    # ── Dashboard ──────────────────────────────────────────────────────
    path('', views.sp_dashboard, name='dashboard'),
    path('menu/', views.sp_dashboard, name='menu_principal'),

    # ── Calendario de Procesos ─────────────────────────────────────────
    path('calendario/', views.sp_calendario, name='calendario'),
    path('calendario/eventos/', views.sp_calendario_eventos, name='calendario_eventos'),
    path('calendario/crear/', views.sp_calendario_crear, name='calendario_crear'),

    # ── Rubros y Tarifas ───────────────────────────────────────────────
    path('rubros/', views.rubros_lista, name='rubros_lista'),
    path('rubros/nuevo/', views.rubro_form, name='rubro_nuevo'),
    path('rubros/<int:pk>/editar/', views.rubro_form, name='rubro_editar'),
    path('rubros/<int:pk>/eliminar/', views.rubro_eliminar, name='rubro_eliminar'),

    path('tarifas/', views.tarifas_lista, name='tarifas_lista'),
    path('tarifas/nueva/', views.tarifa_form, name='tarifa_nueva'),
    path('tarifas/<int:pk>/editar/', views.tarifa_form, name='tarifa_editar'),
    path('tarifas/<int:pk>/tramos/', views.tarifa_tramos, name='tarifa_tramos'),

    # ── Catastro de Usuarios (Abonados) ───────────────────────────────
    path('catastro/', views.catastro_lista, name='catastro_lista'),
    path('catastro/nuevo/', views.catastro_form, name='catastro_nuevo'),
    path('catastro/mapa/', views.catastro_mapa, name='catastro_mapa'),
    path('catastro/<int:pk>/', views.catastro_detalle, name='catastro_detalle'),
    path('catastro/<int:pk>/editar/', views.catastro_form, name='catastro_editar'),
    path('catastro/<int:pk>/eliminar/', views.catastro_eliminar, name='catastro_eliminar'),

    # ── Medidores ─────────────────────────────────────────────────────
    path('medidores/', views.medidores_lista, name='medidores_lista'),
    path('medidores/nuevo/', views.medidor_form, name='medidor_nuevo'),
    path('medidores/<int:pk>/editar/', views.medidor_form, name='medidor_editar'),

    # ── Ciclos y Rutas ────────────────────────────────────────────────
    path('ciclos/', views.ciclos_lista, name='ciclos_lista'),
    path('ciclos/nuevo/', views.ciclo_form, name='ciclo_nuevo'),
    path('ciclos/<int:pk>/editar/', views.ciclo_form, name='ciclo_editar'),

    # ── Lecturas ──────────────────────────────────────────────────────
    path('lecturas/', views.lecturas_lista, name='lecturas_lista'),
    path('lecturas/nueva/', views.lectura_form, name='lectura_nueva'),
    path('lecturas/<int:pk>/editar/', views.lectura_form, name='lectura_editar'),
    path('lecturas/cargar-ciclo/', views.lecturas_cargar_ciclo, name='lecturas_cargar_ciclo'),

    # ── Facturación ───────────────────────────────────────────────────
    path('facturacion/enviar-a-caja/', views.facturacion_enviar_a_caja, name='facturacion_enviar_a_caja'),
    path('facturacion/', views.facturacion_lista, name='facturacion_lista'),
    path('facturacion/generar/', views.facturacion_generar, name='facturacion_generar'),
    path('facturacion/<int:pk>/', views.factura_detalle, name='factura_detalle'),
    path('facturacion/<int:pk>/anular/', views.factura_anular, name='factura_anular'),
    path('facturacion/estado-cuenta/', views.estado_cuenta_abonado, name='estado_cuenta'),

    # ── Órdenes de Trabajo ────────────────────────────────────────────
    path('ordenes/', views.ordenes_lista, name='ordenes_lista'),
    path('ordenes/nueva/', views.orden_form, name='orden_nueva'),
    path('ordenes/<int:pk>/', views.orden_detalle, name='orden_detalle'),
    path('ordenes/<int:pk>/editar/', views.orden_form, name='orden_editar'),
    path('ordenes/<int:pk>/cerrar/', views.orden_cerrar, name='orden_cerrar'),

    # ── Catálogos OT ──────────────────────────────────────────────────
    path('responsables/', views.responsables_lista, name='responsables_lista'),
    path('responsables/nuevo/', views.responsable_form, name='responsable_nuevo'),
    path('responsables/<int:pk>/editar/', views.responsable_form, name='responsable_editar'),

    path('conceptos-ot/', views.conceptos_ot_lista, name='conceptos_ot_lista'),
    path('conceptos-ot/nuevo/', views.concepto_ot_form, name='concepto_ot_nuevo'),
    path('conceptos-ot/<int:pk>/editar/', views.concepto_ot_form, name='concepto_ot_editar'),

    # ── Cortes y Reconexiones ─────────────────────────────────────────
    path('cortes/', views.cortes_lista, name='cortes_lista'),
    path('cortes/nuevo/', views.corte_form, name='corte_nuevo'),

    # ── Reportes ──────────────────────────────────────────────────────
    path('reportes/', views.reportes_dashboard, name='reportes'),
    path('reportes/morosos/', views.reporte_morosos, name='reporte_morosos'),
    path('reportes/consumos/', views.reporte_consumos, name='reporte_consumos'),
    path('reportes/facturacion-ciclo/', views.reporte_facturacion_ciclo, name='reporte_facturacion_ciclo'),
    path('reportes/reclamos-concepto/', views.reporte_reclamos_por_concepto, name='reporte_reclamos_concepto'),

    # ── AJAX ──────────────────────────────────────────────────────────
    path('ajax/buscar-abonado/', views.ajax_buscar_abonado, name='ajax_buscar_abonado'),
    path('ajax/calcular-factura/', views.ajax_calcular_factura, name='ajax_calcular_factura'),
    path('ajax/guardar-tramo/', views.ajax_guardar_tramo, name='ajax_guardar_tramo'),
    path('ajax/eliminar-tramo/<int:pk>/', views.ajax_eliminar_tramo, name='ajax_eliminar_tramo'),

    # Favicon
    path('favicon.ico', lambda request: HttpResponse(status=204), name='favicon'),
]

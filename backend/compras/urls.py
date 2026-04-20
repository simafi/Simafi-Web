from django.urls import path

from . import procesos
from . import views

app_name = "compras"

urlpatterns = [
    path("", views.compras_menu_principal, name="compras_menu_principal"),
    path("menu/", views.compras_menu_principal, name="compras_menu"),
    path("requisiciones/", views.requisicion_list, name="requisicion_list"),
    path("requisiciones/nueva/", views.requisicion_create, name="requisicion_create"),
    path("requisiciones/<int:pk>/editar/", views.requisicion_edit, name="requisicion_edit"),
    path("requisiciones/<int:pk>/estado/<str:nuevo_estado>/", views.requisicion_cambiar_estado, name="requisicion_cambiar_estado"),
    path("ordenes-compra/", views.orden_compra_list, name="orden_compra_list"),
    path("ordenes-compra/nueva/", views.orden_compra_create, name="orden_compra_create"),
    path("ordenes-compra/<int:pk>/editar/", views.orden_compra_edit, name="orden_compra_edit"),
    path("ordenes-compra/<int:pk>/estado/<str:nuevo_estado>/", views.orden_compra_cambiar_estado, name="orden_compra_cambiar_estado"),
    path(
        "ordenes-compra/<int:pk>/imprimir/",
        views.orden_compra_imprimir,
        name="orden_compra_imprimir",
    ),
    path(
        "ordenes-compra/<int:pk>/recibir/",
        procesos.orden_compra_recibir,
        name="orden_compra_recibir",
    ),
    path("materiales-bodega/", procesos.materiales_bodega_list, name="materiales_bodega_list"),
    path("cotizaciones/", procesos.solicitud_cotizacion_list, name="solicitud_cotizacion_list"),
    path("cotizaciones/nueva/", procesos.solicitud_cotizacion_create, name="solicitud_cotizacion_create"),
    path("cotizaciones/<int:pk>/editar/", procesos.solicitud_cotizacion_edit, name="solicitud_cotizacion_edit"),
    path(
        "cotizaciones/<int:pk>/generar-oc/",
        procesos.generar_oc_desde_oferta,
        name="generar_oc_desde_oferta",
    ),
    path(
        "cotizaciones/<int:pk>/imprimir-oncae/",
        procesos.solicitud_cotizacion_imprimir_oncae,
        name="solicitud_cotizacion_imprimir_oncae",
    ),
    path(
        "invitaciones/<int:pk>/oferta/",
        procesos.invitacion_oferta_edit,
        name="invitacion_oferta_edit",
    ),
    path("bodega/movimientos/", procesos.movimiento_bodega_list, name="movimiento_bodega_list"),
    path("bodega/entrada/", procesos.movimiento_bodega_entrada, name="movimiento_bodega_entrada"),
    path(
        "ajax/buscar-inventario-entrada/",
        procesos.ajax_buscar_inventario_entrada,
        name="ajax_buscar_inventario_entrada",
    ),
]

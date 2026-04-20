from django.urls import path
from django.views.generic import RedirectView
from . import views
# Importar vistas avanzadas del módulo 'catastro' (BDCata1 + Terreno)
from catastro.views import BDCata1CreateView, terreno_rural_form, guardar_areas_rurales, obtener_factor_riego

app_name = 'catastro'

urlpatterns = [
    # Dashboard principal
    path('', views.catastro_dashboard, name='dashboard'),
    
    # Propiedades Inmuebles
    path('propiedades/', views.propiedades_list, name='propiedades_list'),
    path('propiedades/nueva/', views.propiedad_create, name='propiedad_create'),
    path('propiedades/<int:pk>/', views.propiedad_detail, name='propiedad_detail'),
    path('propiedades/<int:pk>/editar/', views.propiedad_update, name='propiedad_update'),
    path('propiedades/<int:pk>/eliminar/', views.propiedad_delete, name='propiedad_delete'),
    
    # Terrenos
    path('terrenos/', views.terrenos_list, name='terrenos_list'),
    path('terrenos/nuevo/', views.terreno_create, name='terreno_create'),
    path('terrenos/<int:pk>/', views.terreno_detail, name='terreno_detail'),
    path('terrenos/<int:pk>/editar/', views.terreno_update, name='terreno_update'),
    path('terrenos/<int:pk>/eliminar/', views.terreno_delete, name='terreno_delete'),
    
    # Construcciones
    path('construcciones/', views.construcciones_list, name='construcciones_list'),
    path('construcciones/nueva/', views.construccion_create, name='construccion_create'),
    path('construcciones/<int:pk>/', views.construccion_detail, name='construccion_detail'),
    path('construcciones/<int:pk>/editar/', views.construccion_update, name='construccion_update'),
    path('construcciones/<int:pk>/eliminar/', views.construccion_delete, name='construccion_delete'),
    
    # Vehículos
    path('vehiculos/', views.vehiculos_list, name='vehiculos_list'),
    path('vehiculos/nuevo/', views.vehiculo_create, name='vehiculo_create'),
    path('vehiculos/<int:pk>/', views.vehiculo_detail, name='vehiculo_detail'),
    path('vehiculos/<int:pk>/editar/', views.vehiculo_update, name='vehiculo_update'),
    path('vehiculos/<int:pk>/eliminar/', views.vehiculo_delete, name='vehiculo_delete'),
    
    # Establecimientos Comerciales
    path('establecimientos/', views.establecimientos_list, name='establecimientos_list'),
    path('establecimientos/nuevo/', views.establecimiento_create, name='establecimiento_create'),
    path('establecimientos/<int:pk>/', views.establecimiento_detail, name='establecimiento_detail'),
    path('establecimientos/<int:pk>/editar/', views.establecimiento_update, name='establecimiento_update'),
    path('establecimientos/<int:pk>/eliminar/', views.establecimiento_delete, name='establecimiento_delete'),
    
    # Reportes
    path('reportes/', views.reportes_catastro, name='reportes'),
    
    # Avalúo Catastral - Rubros
    path('avaluo-catastral/rubros/', views.rubros_tasas, name='rubros_tasas'),
    # Avalúo Catastral - Detalle Avalúo (placeholder)
    path('avaluo-catastral/detalle-avaluo/', views.reportes_catastro, name='detalle_avaluo'),
    # Avalúo Catastral - Tasas e Impuestos Municipales (tabla tasassmunicipales)
    path('avaluo-catastral/tasas-municipales/', views.tasas_municipales, name='tasas_municipales'),
    # Avalúo Catastral - Tasas e Impuestos Municipales (tabla tasasdecla - mantenida por compatibilidad)
    path('avaluo-catastral/tasas-impuestos/', views.tasas_impuestos, name='tasas_impuestos'),
    
    # APIs para AJAX
    path('api/buscar-propiedad/', views.api_buscar_propiedad, name='api_buscar_propiedad'),
    path('api/buscar-vehiculo/', views.api_buscar_vehiculo, name='api_buscar_vehiculo'),
    path('api/factor-riego/<str:codigo>/', obtener_factor_riego, name='api_factor_riego'),
    path('api/guardar-areas-rurales/', guardar_areas_rurales, name='api_guardar_areas_rurales'),
    path('ajax/tasas-municipales/', views.ajax_tasas_municipales, name='ajax_tasas_municipales'),
    path('ajax/guardar-tasa-municipal/', views.ajax_guardar_tasa_municipal, name='ajax_guardar_tasa_municipal'),

    # Registro de Bienes Inmuebles (rutas nuevas)
    path('bienes-inmuebles/registrar/', RedirectView.as_view(pattern_name='catastro:bienes_registrar_urbano', permanent=False), name='bienes_registrar'),
    path('bienes-inmuebles/registrar/urbano/', BDCata1CreateView.as_view(), {'ficha': '1'}, name='bienes_registrar_urbano'),
    path('bienes-inmuebles/registrar/rural/', BDCata1CreateView.as_view(), {'ficha': '2'}, name='bienes_registrar_rural'),
    path('bienes-inmuebles/registrar/urbano', BDCata1CreateView.as_view(), {'ficha': '1'}),
    path('bienes-inmuebles/registrar/rural', BDCata1CreateView.as_view(), {'ficha': '2'}),

    # Formulario dedicado Terreno Rural por clave
    path('bienes-inmuebles/terreno/rural/<str:cocata1>/', terreno_rural_form, name='terreno_rural_form'),
]





























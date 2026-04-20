from django.urls import path
from . import views
from . import sistema_general_views
from . import catalog_views

app_name = 'configuracion'

urlpatterns = [
    # Legacy (formulario único departamento)
    path('departamento/', views.departamento_crud, name='departamento_crud'),
    path('ajax/buscar-departamento/', views.buscar_departamento, name='buscar_departamento'),
    # Configuración general del sistema (menú modular; multi-municipio)
    path('catalogo/departamentos/', sistema_general_views.departamentos_list, name='departamentos_list'),
    path('catalogo/departamentos/nuevo/', sistema_general_views.departamento_create, name='departamento_create'),
    path('catalogo/departamentos/<str:codigo>/editar/', sistema_general_views.departamento_update, name='departamento_update'),
    path('catalogo/departamentos/<str:codigo>/eliminar/', sistema_general_views.departamento_delete, name='departamento_delete'),
    path('catalogo/departamentos/exportar/excel/', sistema_general_views.departamentos_export_excel, name='departamentos_export_excel'),
    path('catalogo/departamentos/exportar/pdf/', sistema_general_views.departamentos_export_pdf, name='departamentos_export_pdf'),
    path('catalogo/municipios/', sistema_general_views.municipios_list, name='municipios_list'),
    path('catalogo/municipios/nuevo/', sistema_general_views.municipio_create, name='municipio_create'),
    path('catalogo/municipios/<int:pk>/editar/', sistema_general_views.municipio_update, name='municipio_update'),
    path('catalogo/municipios/<int:pk>/eliminar/', sistema_general_views.municipio_delete, name='municipio_delete'),
    path('catalogo/municipios/exportar/excel/', sistema_general_views.municipios_export_excel, name='municipios_export_excel'),
    path('catalogo/municipios/exportar/pdf/', sistema_general_views.municipios_export_pdf, name='municipios_export_pdf'),
    path('catalogo/caserios/', sistema_general_views.caserios_list, name='caserios_list'),
    path('catalogo/caserios/nuevo/', sistema_general_views.caserio_create, name='caserio_create'),
    path('catalogo/caserios/<int:pk>/editar/', sistema_general_views.caserio_update, name='caserio_update'),
    path('catalogo/caserios/<int:pk>/eliminar/', sistema_general_views.caserio_delete, name='caserio_delete'),
    path('catalogo/caserios/exportar/excel/', sistema_general_views.caserios_export_excel, name='caserios_export_excel'),
    path('catalogo/caserios/exportar/pdf/', sistema_general_views.caserios_export_pdf, name='caserios_export_pdf'),
    path('catalogo/nacionalidades/', sistema_general_views.nacionalidades_list, name='nacionalidades_list'),
    path('catalogo/nacionalidades/nuevo/', sistema_general_views.nacionalidad_create, name='nacionalidad_create'),
    path('catalogo/nacionalidades/<int:pk>/editar/', sistema_general_views.nacionalidad_update, name='nacionalidad_update'),
    path('catalogo/nacionalidades/<int:pk>/eliminar/', sistema_general_views.nacionalidad_delete, name='nacionalidad_delete'),
    path('catalogo/nacionalidades/exportar/excel/', sistema_general_views.nacionalidades_export_excel, name='nacionalidades_export_excel'),
    path('catalogo/nacionalidades/exportar/pdf/', sistema_general_views.nacionalidades_export_pdf, name='nacionalidades_export_pdf'),
    path('catalogo/sitios/', sistema_general_views.sitios_list, name='sitios_list'),
    path('catalogo/sitios/nuevo/', sistema_general_views.sitio_create, name='sitio_create'),
    path('catalogo/sitios/<int:pk>/editar/', sistema_general_views.sitio_update, name='sitio_update'),
    path('catalogo/sitios/<int:pk>/eliminar/', sistema_general_views.sitio_delete, name='sitio_delete'),
    path('catalogo/sitios/exportar/excel/', sistema_general_views.sitios_export_excel, name='sitios_export_excel'),
    path('catalogo/sitios/exportar/pdf/', sistema_general_views.sitios_export_pdf, name='sitios_export_pdf'),
    path('catalogo/catastro/<slug:clave>/exportar/excel/', catalog_views.catalogo_catastro_export_excel, name='catalogo_catastro_export_excel'),
    path('catalogo/catastro/<slug:clave>/exportar/pdf/', catalog_views.catalogo_catastro_export_pdf, name='catalogo_catastro_export_pdf'),
    path('catalogo/catastro/<slug:clave>/', catalog_views.catalogo_catastro_list, name='catalogo_catastro_list'),
    path('catalogo/catastro/<slug:clave>/nuevo/', catalog_views.catalogo_catastro_create, name='catalogo_catastro_create'),
    path('catalogo/catastro/<slug:clave>/<int:pk>/editar/', catalog_views.catalogo_catastro_update, name='catalogo_catastro_update'),
    path('catalogo/catastro/<slug:clave>/<int:pk>/eliminar/', catalog_views.catalogo_catastro_delete, name='catalogo_catastro_delete'),
    path('api/lookup/departamento/', sistema_general_views.api_lookup_departamento, name='api_lookup_departamento'),
    path('api/lookup/municipio/', sistema_general_views.api_lookup_municipio, name='api_lookup_municipio'),
    path('api/lookup/nacionalidad/', sistema_general_views.api_lookup_nacionalidad, name='api_lookup_nacionalidad'),
    path('api/lookup/caserio/', sistema_general_views.api_lookup_caserio, name='api_lookup_caserio'),
    path('api/lookup/sitio/', sistema_general_views.api_lookup_sitio, name='api_lookup_sitio'),
    path('api/lookup/catastro/<slug:clave>/', catalog_views.api_lookup_catalogo_catastro, name='api_lookup_catalogo_catastro'),
    path('', sistema_general_views.sistema_general_menu, name='sistema_general_menu'),
]

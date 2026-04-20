from django.urls import path

from . import views

app_name = 'administrativo'

urlpatterns = [
    path('', views.menu_principal, name='menu_principal'),
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/exportar/excel/', views.proveedor_export_excel, name='proveedor_export_excel'),
    path('proveedores/exportar/pdf/', views.proveedor_export_pdf, name='proveedor_export_pdf'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/documentacion/', views.proveedor_documentacion_descargar, name='proveedor_documentacion_descargar'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_delete'),
    path('contratos/', views.contrato_list, name='contrato_list'),
    path('contratos/exportar/excel/', views.contrato_export_excel, name='contrato_export_excel'),
    path('contratos/exportar/pdf/', views.contrato_export_pdf, name='contrato_export_pdf'),
    path('contratos/nuevo/', views.contrato_create, name='contrato_create'),
    path('contratos/<int:pk>/editar/', views.contrato_update, name='contrato_update'),
    path('contratos/<int:pk>/eliminar/', views.contrato_delete, name='contrato_delete'),
    path('expedientes/', views.expediente_list, name='expediente_list'),
    path('expedientes/exportar/excel/', views.expediente_export_excel, name='expediente_export_excel'),
    path('expedientes/exportar/pdf/', views.expediente_export_pdf, name='expediente_export_pdf'),
    path('expedientes/nuevo/', views.expediente_create, name='expediente_create'),
    path('expedientes/<int:pk>/editar/', views.expediente_update, name='expediente_update'),
    path('expedientes/<int:pk>/eliminar/', views.expediente_delete, name='expediente_delete'),
    # Legacy
    path('departamento/', views.departamento_crud, name='departamento_crud'),
    path('ajax/buscar-departamento/', views.buscar_departamento, name='buscar_departamento'),
]

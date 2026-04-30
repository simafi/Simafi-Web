from django.urls import path
from . import views

app_name = 'impuesto_personal'

urlpatterns = [
    path('declaraciones/', views.DeclaracionListView.as_view(), name='declaracion_list'),
    path('declaraciones/nueva/<str:identidad>/', views.crear_declaracion, name='crear_declaracion'),
    path('planillas/', views.PlanillaListView.as_view(), name='planilla_list'),
    path('planillas/importar/', views.importar_planilla, name='importar_planilla'),
    path('solvencia/verificar/<str:identidad>/', views.verificar_solvencia, name='verificar_solvencia'),
    path('solvencia/imprimir/<str:identidad>/', views.generar_pdf_solvencia, name='generar_pdf_solvencia'),
]

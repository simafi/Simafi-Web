from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'catastro'

urlpatterns = [
    # URL raíz - redirige al login
    path('', views.catastro_login_view, name='catastro_home'),
    
    # Login y autenticación
    path('login/', views.catastro_login_view, name='catastro_login'),
    path('logout/', views.catastro_logout_view, name='catastro_logout'),
    
    # Menú principal
    path('menu/', views.catastro_menu_principal, name='catastro_menu_principal'),
    
    # Funcionalidades principales
    path('bienes-inmuebles/', views.catastro_bienes_inmuebles, name='catastro_bienes_inmuebles'),
    path('bienes-inmuebles/registrar/', views.registrar_bien_inmueble, name='bienes_inmuebles_registrar'),
    path('bienes-inmuebles/eliminar/', views.eliminar_bien_inmueble, name='eliminar_bien_inmueble'),
    path('bienes-inmuebles/buscar/', views.buscar_bien_inmueble, name='buscar_bien_inmueble'),
    path('bienes-inmuebles/buscar/exportar/excel/', views.buscar_bien_inmueble_export_excel, name='buscar_bien_inmueble_export_excel'),
    path('bienes-inmuebles/buscar/exportar/pdf/', views.buscar_bien_inmueble_export_pdf, name='buscar_bien_inmueble_export_pdf'),
    path('mapa-georreferenciado/', views.mapa_georreferenciado_view, name='mapa_georreferenciado_view'),
    # Redirección de vehiculos/ a miscelaneoscat/ para mantener compatibilidad
    path('vehiculos/', RedirectView.as_view(pattern_name='catastro:catastro_miscelaneos', permanent=False), name='catastro_vehiculos_redirect'),
    path('miscelaneoscat/', views.catastro_miscelaneos, name='catastro_miscelaneos'),
    path('terrenos/', views.catastro_terrenos, name='catastro_terrenos'),
    path('construcciones/', views.catastro_construcciones, name='catastro_construcciones'),
    path('notificaciones-avaluo/', views.notificaciones_avaluo, name='notificaciones_avaluo'),
    path('notificacion-avaluo-catastral/', views.notificacion_avaluo_catastral, name='notificacion_avaluo_catastral'),
    path('generacion-graficos/', views.generacion_graficos, name='generacion_graficos'),
    path('generar-graficos/', views.generar_graficos, name='generar_graficos'),
    path('emision-documentos/', views.emision_documentos, name='emision_documentos'),
    path('generar-constancia/<str:tipo>/', views.generar_constancia, name='generar_constancia'),
    
    # Reportes y configuración
    path('reportes/', views.catastro_reportes, name='catastro_reportes'),
    path('menu-reportes/', views.catastro_menu_reportes, name='catastro_menu_reportes'),
    path('listado-avaluos-catastrales/', views.listado_avaluos_catastrales, name='listado_avaluos_catastrales'),
    path('listados-catastrales/', views.listados_catastrales, name='listados_catastrales'),
    path('generar-listado-catastral/', views.generar_listado_catastral, name='generar_listado_catastral'),
    path('generar-informe-avaluos/', views.generar_informe_avaluos, name='generar_informe_avaluos'),
    path('sumarial-avaluos-catastrales/', views.sumarial_avaluos_catastrales, name='sumarial_avaluos_catastrales'),
    path('generar-sumarial-avaluos/', views.generar_sumarial_avaluos, name='generar_sumarial_avaluos'),
    path('exportar-sumarial-excel/', views.exportar_sumarial_excel, name='exportar_sumarial_excel'),
    path('exportar-sumarial-pdf/', views.exportar_sumarial_pdf, name='exportar_sumarial_pdf'),
    path('exportar-informe-avaluos-excel/', views.exportar_informe_avaluos_excel, name='exportar_informe_avaluos_excel'),
    path('exportar-informe-avaluos-pdf/', views.exportar_informe_avaluos_pdf, name='exportar_informe_avaluos_pdf'),
    path('informes-dinamicos/', views.informes_dinamicos, name='informes_dinamicos'),
    path('generar-informe-dinamico/', views.generar_informe_dinamico, name='generar_informe_dinamico'),
    path('generar-informe-dinamico/excel/', views.generar_informe_dinamico_excel, name='generar_informe_dinamico_excel'),
    path('generar-informe-dinamico/pdf/', views.generar_informe_dinamico_pdf, name='generar_informe_dinamico_pdf'),
    path('configuracion/', views.catastro_configuracion, name='catastro_configuracion'),
    path('configurar-tasas-municipales/', views.configurar_tasas_municipales, name='configurar_tasas_municipales'),
    path('obtener-tarifas-rubro-bienes/', views.obtener_tarifas_rubro_bienes, name='obtener_tarifas_rubro_bienes'),
    
    # TEST - Solo para pruebas
    path('test-guardado/', views.test_guardado_datos, name='test_guardado_datos'),
    
    # Formularios de terreno
    path('terreno/urbano/<str:cocata1>/', views.terreno_urbano_form, name='terreno_urbano_form'),
    path('terreno/rural/<str:cocata1>/', views.terreno_rural_form, name='terreno_rural_form'),
    
    # Formulario de edificaciones
    path('edificaciones/<str:clave>/', views.edificaciones_form, name='edificaciones_form'),
    path('edificaciones/<str:clave>/especial/', views.edificacion_especial_create, name='edificacion_especial_create'),
    path('edificaciones/<str:clave>/eliminar/', views.eliminar_edificacion, name='eliminar_edificacion'),
    # Comentarios de catastro
    path('comentarios/<str:clave>/nuevo/', views.comentario_catastro_create, name='comentario_catastro_create'),
    path('api/comentarios/', views.api_comentarios_catastro, name='api_comentarios_catastro'),
    path('edificaciones/<str:clave>/exportar/excel/', views.edificaciones_export_excel, name='edificaciones_export_excel'),
    path('edificaciones/<str:clave>/exportar/pdf/', views.edificaciones_export_pdf, name='edificaciones_export_pdf'),
    
    # Costos Básicos Unitarios
    path('costos/', views.costos_list, name='costos_list'),
    path('costos/nuevo/', views.costo_create, name='costo_create'),
    path('costos/<int:pk>/editar/', views.costo_update, name='costo_update'),
    path('costos/<int:pk>/eliminar/', views.costo_delete, name='costo_delete'),
    path('costos/clasificacion-pesos/<str:uso>/<str:clase>/', views.costos_clasificacion_pesos, name='costos_clasificacion_pesos'),
    path('costos/clasificacion-pesos/<str:uso>/<str:clase>/exportar/excel/', views.costos_clasificacion_pesos_export_excel, name='costos_clasificacion_pesos_export_excel'),
    path('costos/clasificacion-pesos/<str:uso>/<str:clase>/exportar/pdf/', views.costos_clasificacion_pesos_export_pdf, name='costos_clasificacion_pesos_export_pdf'),
    path('costos/exportar/excel/', views.costos_export_excel, name='costos_export_excel'),
    path('costos/exportar/pdf/', views.costos_export_pdf, name='costos_export_pdf'),
    
    # Detalles Adicionales
    path('detalles-adicionales/', views.detalles_adicionales_list, name='detalles_adicionales_list'),
    path('detalles-adicionales/<str:clave>/', views.detalles_adicionales_list, name='detalles_adicionales_list_clave'),
    path('detalles-adicionales/nuevo/', views.detalle_adicional_create, name='detalle_adicional_create'),
    path('detalles-adicionales/<str:clave>/nuevo/', views.detalle_adicional_create, name='detalle_adicional_create_clave'),
    path('detalles-adicionales/nuevo-especial/', views.detalle_adicional_especial_create, name='detalle_adicional_especial_create'),
    path('detalles-adicionales/<str:empresa>/<str:cocata1>/nuevo-especial/', views.detalle_adicional_especial_create, name='detalle_adicional_especial_create_clave'),
    path('detalles-adicionales/<int:pk>/editar/', views.detalle_adicional_update, name='detalle_adicional_update'),
    path('detalles-adicionales/<int:pk>/eliminar/', views.detalle_adicional_delete, name='detalle_adicional_delete'),
    # Exportación de Detalles Adicionales
    path('detalles-adicionales/exportar/excel/', views.detalles_adicionales_export_excel, name='detalles_adicionales_export_excel'),
    path('detalles-adicionales/<str:clave>/exportar/excel/', views.detalles_adicionales_export_excel, name='detalles_adicionales_export_excel_clave'),
    path('detalles-adicionales/exportar/pdf/', views.detalles_adicionales_export_pdf, name='detalles_adicionales_export_pdf'),
    path('detalles-adicionales/<str:clave>/exportar/pdf/', views.detalles_adicionales_export_pdf, name='detalles_adicionales_export_pdf_clave'),
    
    # Colindantes
    path('colindantes/<str:empresa>/<str:cocata1>/', views.colindantes_list, name='colindantes_list'),
    path('colindantes/<str:empresa>/<str:cocata1>/nuevo/', views.colindante_create, name='colindante_create'),
    path('colindantes/<str:empresa>/<str:cocata1>/<int:pk>/editar/', views.colindante_update, name='colindante_update'),
    path('colindantes/<str:empresa>/<str:cocata1>/<int:pk>/eliminar/', views.colindante_delete, name='colindante_delete'),
    path('colindantes/<str:empresa>/<str:cocata1>/exportar/excel/', views.colindantes_export_excel, name='colindantes_export_excel'),
    path('colindantes/<str:empresa>/<str:cocata1>/exportar/pdf/', views.colindantes_export_pdf, name='colindantes_export_pdf'),
    
    # URLs para Copropietarios
    path('copropietarios/<str:empresa>/<str:cocata1>/', views.copropietarios_list, name='copropietarios_list'),
    path('copropietarios/<str:empresa>/<str:cocata1>/nuevo/', views.copropietario_create, name='copropietario_create'),
    path('copropietarios/<str:empresa>/<str:cocata1>/<int:pk>/editar/', views.copropietario_update, name='copropietario_update'),
    path('copropietarios/<str:empresa>/<str:cocata1>/<int:pk>/eliminar/', views.copropietario_delete, name='copropietario_delete'),
    path('api/buscar-identidad-copropietario/', views.buscar_identidad_copropietario_ajax, name='buscar_identidad_copropietario_ajax'),
    
    # Tipos de Detalle (Catálogo)
    path('tipos-detalle/', views.tipos_detalle_list, name='tipos_detalle_list'),
    path('tipos-detalle/nuevo/', views.tipo_detalle_create, name='tipo_detalle_create'),
    path('tipos-detalle/<int:pk>/editar/', views.tipo_detalle_update, name='tipo_detalle_update'),
    path('tipos-detalle/<int:pk>/eliminar/', views.tipo_detalle_delete, name='tipo_detalle_delete'),
    
    # Usos de Edificación (Catálogo)
    path('usos-edifica/', views.usos_edifica_list, name='usos_edifica_list'),
    path('usos-edifica/nuevo/', views.uso_edifica_create, name='uso_edifica_create'),
    path('usos-edifica/<int:pk>/editar/', views.uso_edifica_update, name='uso_edifica_update'),
    path('usos-edifica/<int:pk>/eliminar/', views.uso_edifica_delete, name='uso_edifica_delete'),
    
    # Barrios / Aldeas
    path('barrios/', views.barrios_list, name='barrios_list'),
    path('barrios/nuevo/', views.barrio_create, name='barrio_create'),
    path('barrios/<int:pk>/editar/', views.barrio_update, name='barrio_update'),
    path('barrios/<int:pk>/eliminar/', views.barrio_delete, name='barrio_delete'),
    path('barrios/exportar/excel/', views.barrios_export_excel, name='barrios_export_excel'),
    path('barrios/exportar/pdf/', views.barrios_export_pdf, name='barrios_export_pdf'),
    
    # Usos del predio (tabla usos: CRUD + enlace a sub usos en Configuración general)
    path('usos-predio/', views.usos_predio_list, name='usos_predio_list'),
    path('usos-predio/nuevo/', views.usos_predio_create, name='usos_predio_create'),
    path('usos-predio/<int:pk>/editar/', views.usos_predio_update, name='usos_predio_update'),
    path('usos-predio/<int:pk>/eliminar/', views.usos_predio_delete, name='usos_predio_delete'),

    # Topografía del Predio
    path('topografia/', views.topografia_list, name='topografia_list'),
    path('topografia/nuevo/', views.topografia_create, name='topografia_create'),
    path('topografia/<int:pk>/editar/', views.topografia_update, name='topografia_update'),
    path('topografia/<int:pk>/eliminar/', views.topografia_delete, name='topografia_delete'),
    path('topografia/exportar/excel/', views.topografia_export_excel, name='topografia_export_excel'),
    path('topografia/exportar/pdf/', views.topografia_export_pdf, name='topografia_export_pdf'),
    
    # Tipos de Material
    path('tipos-material/', views.tipo_material_list, name='tipo_material_list'),
    path('tipos-material/nuevo/', views.tipo_material_create, name='tipo_material_create'),
    path('tipos-material/<int:pk>/editar/', views.tipo_material_update, name='tipo_material_update'),
    path('tipos-material/<int:pk>/eliminar/', views.tipo_material_delete, name='tipo_material_delete'),
    
    # API Endpoints
    path('api/guardar-areas-rurales/', views.guardar_areas_rurales, name='api_guardar_areas_rurales'),
    path('api/eliminar-area-rural/', views.eliminar_area_rural, name='api_eliminar_area_rural'),
    path('api/eliminar-avaluo-terreno/', views.eliminar_avaluo_terreno, name='api_eliminar_avaluo_terreno'),
    path('api/buscar-bien-inmueble/', views.api_buscar_bien_inmueble, name='api_bien_inmueble'),
    path('api/barrios/', views.api_barrios, name='api_barrios'),
    path('api/identificacion/', views.api_identificacion, name='api_identificacion'),
    path('api/tipos-sexo/', views.api_tipos_sexo, name='api_tipos_sexo'),
    path('api/usos/', views.api_usos, name='api_usos'),
    path('api/subusos/', views.api_subusos, name='api_subusos'),
    path('api/habitacional/', views.api_habitacional, name='api_habitacional'),
    path('api/naturalezas/', views.api_naturalezas, name='api_naturalezas'),
    path('api/dominios/', views.api_dominios, name='api_dominios'),
    path('api/tipos-documento/', views.api_tipos_documento, name='api_tipos_documento'),
    path('api/propietarios/', views.api_propietarios, name='api_propietarios'),
    path('api/zonasusos/', views.api_zonasusos, name='api_zonasusos'),
    path('api/nacionalidad/', views.api_nacionalidad, name='api_nacionalidad'),
    path('api/caserio/', views.api_caserio, name='api_caserio'),
    path('api/avaluo-terreno/', views.api_avaluo_terreno, name='api_avaluo_terreno'),
    path('api/buscar-costo/', views.api_buscar_costo, name='api_buscar_costo'),
    path('api/buscar-edificacion/', views.api_buscar_edificacion, name='api_buscar_edificacion'),
    path('api/buscar-tipo-detalle/', views.api_buscar_tipo_detalle, name='api_buscar_tipo_detalle'),
    path('api/listar-edificaciones/', views.api_listar_edificaciones, name='api_listar_edificaciones'),
    path('api/buscar-barrio/', views.api_buscar_barrio, name='api_buscar_barrio'),
    path('api/buscar-topografia/', views.api_buscar_topografia, name='api_buscar_topografia'),
    path('api/buscar-uso-edifica/', views.api_buscar_uso_edifica, name='api_buscar_uso_edifica'),
    path('api/buscar-confi-tipologia/', views.api_buscar_confi_tipologia, name='api_buscar_confi_tipologia'),
    path('api/calcular-calidad/', views.api_calcular_calidad, name='api_calcular_calidad'),
    path('api/listar-fundiciones/', views.api_listar_fundiciones, name='api_listar_fundiciones'),
    path('api/listar-pisos/', views.api_listar_pisos, name='api_listar_pisos'),
    path('api/listar-paredes-exteriores/', views.api_listar_paredes_exteriores, name='api_listar_paredes_exteriores'),
    path('api/listar-techos/', views.api_listar_techos, name='api_listar_techos'),
    path('api/listar-paredes-interiores/', views.api_listar_paredes_interiores, name='api_listar_paredes_interiores'),
    path('api/listar-cielo-falso/', views.api_listar_cielo_falso, name='api_listar_cielo_falso'),
    path('api/listar-carpinteria/', views.api_listar_carpinteria, name='api_listar_carpinteria'),
    path('api/listar-electricidad/', views.api_listar_electricidad, name='api_listar_electricidad'),
    path('api/listar-plomeria/', views.api_listar_plomeria, name='api_listar_plomeria'),
    path('api/listar-otros-detalles/', views.api_listar_otros_detalles, name='api_listar_otros_detalles'),
    
    # Configuración de Tipología
    path('confi-tipologia/', views.confi_tipologia_list, name='confi_tipologia_list'),
    path('confi-tipologia/nuevo/', views.confi_tipologia_create, name='confi_tipologia_create'),
    path('confi-tipologia/<int:pk>/editar/', views.confi_tipologia_update, name='confi_tipologia_update'),
    path('confi-tipologia/<int:pk>/eliminar/', views.confi_tipologia_delete, name='confi_tipologia_delete'),
    # Configuración de Tipología desde Clasificación de Pesos
    path('confi-tipologia/clasificacion/<str:uso>/<str:clase>/nuevo/', views.confi_tipologia_create_clasificacion, name='confi_tipologia_create_clasificacion'),
    path('confi-tipologia/clasificacion/<str:uso>/<str:clase>/<int:pk>/editar/', views.confi_tipologia_update_clasificacion, name='confi_tipologia_update_clasificacion'),
    
    # Especificaciones
    path('especificaciones/calcular-calidad/', views.especificaciones_calcular_calidad, name='especificaciones_calcular_calidad'),
    path('especificaciones/', views.especificaciones_list, name='especificaciones_list'),
    path('especificaciones/<int:pk>/editar/', views.especificaciones_update, name='especificaciones_update'),
    path('especificaciones/<int:pk>/eliminar/', views.especificaciones_delete, name='especificaciones_delete'),
    
    # Detalles de Especificaciones
    path('det-especificaciones/', views.det_especificacion_list, name='det_especificacion_list'),
    path('det-especificaciones/nuevo/', views.det_especificacion_create, name='det_especificacion_create'),
    path('det-especificaciones/desde-edificacion/', views.det_especificacion_create_from_edificacion, name='det_especificacion_create_from_edificacion'),
    path('det-especificaciones/<int:pk>/editar/', views.det_especificacion_update, name='det_especificacion_update'),
    path('det-especificaciones/<int:pk>/eliminar/', views.det_especificacion_delete, name='det_especificacion_delete'),
    
    # Valor Árbol (Clase y Variedad de Cultivo)
    path('valor-arbol/', views.valor_arbol_list, name='valor_arbol_list'),
    path('valor-arbol/nuevo/', views.valor_arbol_create, name='valor_arbol_create'),
    path('valor-arbol/<int:pk>/editar/', views.valor_arbol_update, name='valor_arbol_update'),
    path('valor-arbol/<int:pk>/eliminar/', views.valor_arbol_delete, name='valor_arbol_delete'),
    path('valor-arbol/exportar/excel/', views.valor_arbol_export_excel, name='valor_arbol_export_excel'),
    path('valor-arbol/exportar/pdf/', views.valor_arbol_export_pdf, name='valor_arbol_export_pdf'),
    path('api/buscar-valor-arbol/', views.buscar_valor_arbol_ajax, name='buscar_valor_arbol_ajax'),
    
    # Valores de Tierra Rural
    path('tierra-rural/', views.tierra_rural_list, name='tierra_rural_list'),
    path('tierra-rural/nuevo/', views.tierra_rural_create, name='tierra_rural_create'),
    path('tierra-rural/<int:pk>/editar/', views.tierra_rural_update, name='tierra_rural_update'),
    path('tierra-rural/<int:pk>/eliminar/', views.tierra_rural_delete, name='tierra_rural_delete'),
    path('api/buscar-tierra-rural/', views.buscar_tierra_rural_ajax, name='buscar_tierra_rural_ajax'),
    
    # Cultivo Permanente
    # URLs de cultivo permanente
    path('cultivo-permanente/<str:empresa>/<str:cocata1>/<int:pk>/editar/', views.cultivo_permanente_update, name='cultivo_permanente_update'),
    path('cultivo-permanente/<str:empresa>/<str:cocata1>/<int:pk>/eliminar/', views.cultivo_permanente_delete, name='cultivo_permanente_delete'),
    path('cultivo-permanente/<str:empresa>/<str:cocata1>/exportar-excel/', views.cultivo_permanente_export_excel, name='cultivo_permanente_export_excel'),
    path('cultivo-permanente/<str:empresa>/<str:cocata1>/exportar-pdf/', views.cultivo_permanente_export_pdf, name='cultivo_permanente_export_pdf'),
    path('cultivo-permanente/<str:empresa>/<str:clave>/nuevo/', views.cultivo_permanente_create, name='cultivo_permanente_create'),
    path('cultivo-permanente/<str:empresa>/<str:cocata1>/', views.cultivo_permanente_list, name='cultivo_permanente_list'),
    path('cultivo-permanente/exportar-excel/', views.cultivo_permanente_export_excel, name='cultivo_permanente_export_excel_simple'),
    path('cultivo-permanente/exportar-pdf/', views.cultivo_permanente_export_pdf, name='cultivo_permanente_export_pdf_simple'),
    path('cultivo-permanente/', views.cultivo_permanente_list, name='cultivo_permanente_list'),
    path('api/buscar-clase-cultivo/', views.buscar_clase_cultivo_ajax, name='buscar_clase_cultivo_ajax'),
    path('api/buscar-factor-cultivo/', views.buscar_factor_cultivo_ajax, name='buscar_factor_cultivo_ajax'),
    
    # Información Legal del Predio (formulario único - relación uno a uno)
    path('informacion-legal/<str:empresa>/<str:cocata1>/', views.informacion_legal_form, name='informacion_legal_form'),
    path('caracteristicas/<str:empresa>/<str:cocata1>/', views.caracteristicas_form, name='caracteristicas_form'),
    path('complemento/<str:empresa>/<str:cocata1>/', views.complemento_form, name='complemento_form'),
    
    # Factor Cultivo
    path('factor-cultivo/<str:empresa>/<str:codigo>/', views.factor_cultivo, name='factor_cultivo'),
    path('factor-cultivo/<str:empresa>/<str:codigo>/nuevo/', views.factor_cultivo_create, name='factor_cultivo_create'),
    path('factor-cultivo/<str:empresa>/<str:codigo>/<int:pk>/editar/', views.factor_cultivo_update, name='factor_cultivo_update'),
    path('factor-cultivo/<str:empresa>/<str:codigo>/<int:pk>/eliminar/', views.factor_cultivo_delete, name='factor_cultivo_delete'),
    path('api/buscar-factor-cultivo/', views.buscar_factor_cultivo_ajax, name='buscar_factor_cultivo_ajax'),
    
    # URLs AJAX para Misceláneos
    path('api/buscar-concepto-miscelaneos/', views.buscar_concepto_miscelaneos_ajax, name='buscar_concepto_miscelaneos_ajax'),
    path('api/cargar-actividades/', views.cargar_actividades_ajax, name='cargar_actividades_ajax'),
    path('api/obtener-tarifas-rubro/', views.obtener_tarifas_rubro_ajax, name='obtener_tarifas_rubro_ajax'),
    path('api/buscar-actividad/', views.buscar_actividad_ajax, name='buscar_actividad_ajax'),
    path('api/enviar-a-caja/', views.enviar_a_caja_ajax, name='enviar_a_caja_ajax'),
    path('api/soporte/<str:numero_recibo>/', views.ver_soporte, name='ver_soporte'),
    
    # AJAX para Tasas Municipales
    path('ajax/tasas-municipales/', views.ajax_tasas_municipales, name='ajax_tasas_municipales'),
    path('ajax/guardar-tasa-municipal/', views.ajax_guardar_tasa_municipal, name='ajax_guardar_tasa_municipal'),
    path('ajax/calcular-tasas-municipales/', views.ajax_calcular_tasas_municipales, name='ajax_calcular_tasas_municipales'),
    path('ajax/obtener-tasa-impositiva/', views.ajax_obtener_tasa_impositiva, name='ajax_obtener_tasa_impositiva'),
    path('ajax/obtener-datos-municipio/', views.ajax_obtener_datos_municipio, name='ajax_obtener_datos_municipio'),
    path('ajax/verificar-registro-guardado/', views.ajax_verificar_registro_guardado, name='ajax_verificar_registro_guardado'),
    
    # AJAX para conversión de coordenadas
    path('ajax/convertir-latlng-a-utm/', views.ajax_convertir_latlng_a_utm, name='ajax_convertir_latlng_a_utm'),
    path('ajax/convertir-utm-a-latlng/', views.ajax_convertir_utm_a_latlng, name='ajax_convertir_utm_a_latlng'),
]







































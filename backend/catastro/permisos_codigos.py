# -*- coding: utf-8 -*-
"""
Códigos de permiso de aplicación para el módulo Catastro (tabla mod_usuarios_permiso).
Deben coincidir con lo insertado por: python manage.py seed_catastro_permisos
"""

MODULO_CATASTRO = "catastro"

# Menú y áreas funcionales
CATASTRO_PERM_MENU_VER = "catastro.menu.ver"
CATASTRO_PERM_BIENES_VER = "catastro.bienes_inmuebles.ver"
CATASTRO_PERM_BIENES_EDITAR = "catastro.bienes_inmuebles.editar"
CATASTRO_PERM_MAPA_VER = "catastro.mapa.ver"
CATASTRO_PERM_MISC_VER = "catastro.miscelaneos.ver"
CATASTRO_PERM_NOTIFICACIONES_VER = "catastro.notificaciones.ver"
CATASTRO_PERM_GRAFICOS_VER = "catastro.graficos.ver"
CATASTRO_PERM_REPORTES_VER = "catastro.reportes.ver"
CATASTRO_PERM_EMISION_VER = "catastro.emision_documentos.ver"
CATASTRO_PERM_CONFIG_VER = "catastro.configuracion.ver"

# (codigo, nombre descriptivo, modulo)
CATASTRO_PERMISOS_SEED = (
    (CATASTRO_PERM_MENU_VER, "Menú principal Catastro", MODULO_CATASTRO),
    (CATASTRO_PERM_BIENES_VER, "Consultar bienes inmuebles", MODULO_CATASTRO),
    (CATASTRO_PERM_BIENES_EDITAR, "Registrar y editar bienes inmuebles", MODULO_CATASTRO),
    (CATASTRO_PERM_MAPA_VER, "Mapa georreferenciado", MODULO_CATASTRO),
    (CATASTRO_PERM_MISC_VER, "Misceláneos", MODULO_CATASTRO),
    (CATASTRO_PERM_NOTIFICACIONES_VER, "Notificaciones de avalúo", MODULO_CATASTRO),
    (CATASTRO_PERM_GRAFICOS_VER, "Generación de gráficos", MODULO_CATASTRO),
    (CATASTRO_PERM_REPORTES_VER, "Reportes catastrales", MODULO_CATASTRO),
    (CATASTRO_PERM_EMISION_VER, "Emisión de documentos", MODULO_CATASTRO),
    (CATASTRO_PERM_CONFIG_VER, "Configuración Catastro", MODULO_CATASTRO),
)

ROL_CATASTRO_COMPLETO_NOMBRE = "Catastro — acceso completo"

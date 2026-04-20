# -*- coding: utf-8 -*-
"""
Permisos de aplicación del módulo Tributario (tabla mod_usuarios_permiso).
Cargar con: python manage.py seed_tributario_permisos
"""

MODULO_TRIBUTARIO = "tributario"

TRIBUTARIO_PERM_MENU_VER = "tributario.menu.ver"
TRIBUTARIO_PERM_MAESTRO_NEGOCIOS = "tributario.maestro_negocios.ver"
TRIBUTARIO_PERM_TARIFAS = "tributario.tarifas.ver"
TRIBUTARIO_PERM_DECLARACIONES = "tributario.declaraciones.ver"
TRIBUTARIO_PERM_REPORTES = "tributario.reportes.ver"
TRIBUTARIO_PERM_ESTADO_CUENTA = "tributario.estado_cuenta.ver"
TRIBUTARIO_PERM_PLAN_ARBITRIO = "tributario.plan_arbitrio.ver"
TRIBUTARIO_PERM_MISC = "tributario.miscelaneos.ver"
TRIBUTARIO_PERM_CONVENIOS = "tributario.convenios.ver"
TRIBUTARIO_PERM_CATALOGOS = "tributario.catalogos.ver"
TRIBUTARIO_PERM_PROCESOS_ANUALES = "tributario.procesos_anuales.ver"
TRIBUTARIO_PERM_CONFIG = "tributario.configuracion.ver"

# (codigo, nombre, modulo)
TRIBUTARIO_PERMISOS_SEED = (
    (TRIBUTARIO_PERM_MENU_VER, "Menú principal Tributario", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_MAESTRO_NEGOCIOS, "Maestro de negocios", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_TARIFAS, "Tarifas y tasas", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_DECLARACIONES, "Declaraciones de volumen / operaciones", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_REPORTES, "Informes y reportes", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_ESTADO_CUENTA, "Estado de cuenta", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_PLAN_ARBITRIO, "Plan de arbitrio", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_MISC, "Misceláneos", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_CONVENIOS, "Convenios de pago", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_CATALOGOS, "Catálogos (actividad, oficina, rubros, tarifas CRUD)", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_PROCESOS_ANUALES, "Cierre anual, cargo anual y recargos moratorios", MODULO_TRIBUTARIO),
    (TRIBUTARIO_PERM_CONFIG, "Configuración (tasas por negocio, etc.)", MODULO_TRIBUTARIO),
)

ROL_TRIBUTARIO_COMPLETO_NOMBRE = "Tributario — acceso completo"

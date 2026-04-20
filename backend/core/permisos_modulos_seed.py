# -*- coding: utf-8 -*-
"""
Catálogo de permisos por módulo (aplicación) para Administrativo, Contabilidad, Tesorería,
Presupuestos y Configuración.

Cargar con: python manage.py seed_modulos_restantes_permisos

Catastro y Tributario tienen comandos propios (seed_catastro_permisos, seed_tributario_permisos).
"""

# --- Administrativo ---
ADMINISTRATIVO_ROL_COMPLETO = "Administrativo — acceso completo"
ADMINISTRATIVO_PERMISOS = (
    ("administrativo.menu.ver", "Menú principal Administrativo"),
    ("administrativo.proveedores.ver", "Proveedores (CRUD y exportaciones)"),
    ("administrativo.contratos.ver", "Contratos (CRUD y exportaciones)"),
    ("administrativo.expedientes.ver", "Expedientes (CRUD y exportaciones)"),
    ("administrativo.departamentos.ver", "Catálogo departamentos (legacy)"),
)

# --- Contabilidad ---
CONTABILIDAD_ROL_COMPLETO = "Contabilidad — acceso completo"
CONTABILIDAD_PERMISOS = (
    ("contabilidad.menu.ver", "Menú principal Contabilidad"),
    ("contabilidad.plan_cuentas.ver", "Plan de cuentas"),
    ("contabilidad.asientos.ver", "Asientos contables"),
    ("contabilidad.libro_mayor.ver", "Libro mayor"),
    ("contabilidad.estados_financieros.ver", "Estados financieros y balanza"),
    ("contabilidad.activos_fijos.ver", "Activos fijos"),
    ("contabilidad.inventarios.ver", "Inventarios"),
    ("contabilidad.configuracion.ver", "Configuración inicial / parámetros"),
)

# --- Tesorería ---
TESORERIA_ROL_COMPLETO = "Tesorería — acceso completo"
TESORERIA_PERMISOS = (
    ("tesoreria.menu.ver", "Menú principal Tesorería"),
    ("tesoreria.caja.ver", "Caja y cobros"),
    ("tesoreria.cuentas.ver", "Cuentas de tesorería (caja/banco/chequera)"),
    ("tesoreria.pagos.ver", "Emisión de pagos"),
    ("tesoreria.cheques.ver", "Control de cheques"),
    ("tesoreria.depositos_notas.ver", "Depósitos y notas bancarias"),
    ("tesoreria.conciliacion.ver", "Conciliación bancaria"),
    ("tesoreria.consultas.ver", "Consultas y órdenes de pago"),
)

# --- Presupuestos ---
PRESUPUESTOS_ROL_COMPLETO = "Presupuestos — acceso completo"
PRESUPUESTOS_PERMISOS = (
    ("presupuestos.menu.ver", "Menú principal Presupuestos"),
    ("presupuestos.catalogo.ver", "Catálogo presupuestario (ingresos/egresos/fondos)"),
    ("presupuestos.presupuesto_anual.ver", "Presupuesto anual"),
    ("presupuestos.reformas.ver", "Reformas presupuestarias"),
    ("presupuestos.proyectos.ver", "Proyectos de inversión"),
    ("presupuestos.ordenes_pago.ver", "Órdenes de pago"),
    ("presupuestos.compromisos.ver", "Compromisos y operaciones manuales"),
    ("presupuestos.informes.ver", "Informes presupuestarios"),
    ("presupuestos.rendicion.ver", "Rendición de cuentas"),
)

# --- Configuración (catálogos generales) ---
CONFIGURACION_ROL_COMPLETO = "Configuración — acceso completo"
CONFIGURACION_PERMISOS = (
    ("configuracion.menu.ver", "Menú / acceso general al módulo Configuración"),
    ("configuracion.departamentos.ver", "Departamentos"),
    ("configuracion.municipios.ver", "Municipios"),
    ("configuracion.caserios.ver", "Caseríos"),
    ("configuracion.nacionalidades.ver", "Nacionalidades"),
    ("configuracion.sitios.ver", "Sitios / ubicaciones"),
    ("configuracion.catalogos.ver", "Otros catálogos del sistema"),
)

# --- Compras (públicas, bodega, vínculo presupuesto / contabilidad / tesorería) ---
COMPRAS_ROL_COMPLETO = "Compras — acceso completo"
COMPRAS_PERMISOS = (
    ("compras.menu.ver", "Menú principal Compras"),
    ("compras.requisiciones.ver", "Requisiciones de materiales/bienes"),
    ("compras.cotizaciones.ver", "Solicitudes de cotización y formatos a proveedores"),
    ("compras.evaluacion.ver", "Evaluación y selección de ofertas"),
    ("compras.ordenes_compra.ver", "Órdenes de compra"),
    ("compras.bodega.ver", "Bodega, kardex y control de existencias"),
    ("compras.presupuesto.ver", "Vínculo codificación presupuestaria"),
    ("compras.contabilidad.ver", "Integración inventario / asientos (NIC 2)"),
    ("compras.tesoreria.ver", "Interfaz hacia orden de pago"),
    ("compras.reportes.ver", "Reportes y auditoría del proceso"),
)

# (código_modulo, lista permisos, nombre rol completo)
MODULOS_RESTANTES_SEED = (
    ("administrativo", ADMINISTRATIVO_PERMISOS, ADMINISTRATIVO_ROL_COMPLETO),
    ("contabilidad", CONTABILIDAD_PERMISOS, CONTABILIDAD_ROL_COMPLETO),
    ("tesoreria", TESORERIA_PERMISOS, TESORERIA_ROL_COMPLETO),
    ("presupuestos", PRESUPUESTOS_PERMISOS, PRESUPUESTOS_ROL_COMPLETO),
    ("configuracion", CONFIGURACION_PERMISOS, CONFIGURACION_ROL_COMPLETO),
    ("compras", COMPRAS_PERMISOS, COMPRAS_ROL_COMPLETO),
)

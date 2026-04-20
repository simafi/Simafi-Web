# -*- coding: utf-8 -*-
"""
Catálogo de formas de rendición de cuentas presupuestaria (municipal).
Referencia normativa Honduras: Ley Orgánica del TSC (control fiscal), Ley de Municipalidades,
marco de transparencia y liquidación presupuestaria (SEFIN / prácticas de rendición al Congreso
y entes de fiscalización). Las plantillas deben ajustarse a formatos oficiales vigentes
publicados por TSC/SEFIN cuando correspondan.
"""

FORMAS_RENDICION = [
    {
        "codigo": "F-01",
        "titulo": "Liquidación del Presupuesto de Ingresos",
        "categoria": "Presupuesto",
        "normativa": "Contiene el total de los Ingresos Corrientes y de Capital desde el presupuesto inicial hasta determinar el total de ingresos pendientes de cobro durante el periodo fiscal.",
    },
    {
        "codigo": "F-02",
        "titulo": "Liquidación del Presupuesto de Egresos por cada Programa",
        "categoria": "Presupuesto",
        "normativa": "Se llena con los valores por cada uno de los programas contenidos en el presupuesto municipal, el cual es de obligatorio cumplimiento (Art. 92, Ley de Municipalidades) de acuerdo a su estructura organizacional.",
    },
    {
        "codigo": "F-03",
        "titulo": "Liquidación del Presupuesto de Egresos Consolidado",
        "categoria": "Presupuesto",
        "normativa": "Es el resumen consolidado de los programas por grupo, 100, 200, 300 y otros.",
    },
    {
        "codigo": "F-04",
        "titulo": "Liquidación del Presupuesto",
        "categoria": "Presupuesto",
        "normativa": "Determina el resultado presupuestario, es decir la suma total de los ingresos devengados, menos la suma total de obligaciones contraídas en el año. Según cifras establecidas en las Formas 01 y 03 respectivamente.",
    },
    {
        "codigo": "F-05",
        "titulo": "Arqueo de Caja General",
        "categoria": "Tesorería",
        "normativa": "Con esta forma se harán los arqueos de caja a los tesoreros municipales o cajeros generales, a los encargados de las cajas receptoras de fondos y colectores de fondos municipales. Presenta el saldo del efectivo existente en tesorería al 31 de diciembre del año que se está liquidando.",
    },
    {
        "codigo": "F-06",
        "titulo": "Arqueo de Caja Chica o Fondo Rotatorio",
        "categoria": "Tesorería",
        "normativa": "Con esta forma se harán los arqueos al o los empleados (as) municipales que manejan el fondo de caja chica o fondos rotatorios (reembolsables). Presenta el saldo del efectivo existente y de los gastos menores al 31 de diciembre del año que se está liquidando.",
    },
    {
        "codigo": "F-07",
        "titulo": "Cuenta de Tesorería",
        "categoria": "Tesorería",
        "normativa": "Documento del movimiento de efectivo y bancos en el período fiscal. Incluye: A) Efectivo y Bancos; B) Existencias en caja; C) Saldos según constancias; D) Conciliación bancaria consolidada; anexos de depósitos en tránsito y cheques no cobrados. Criterios según Manual de Rendición TSC.",
    },
    {
        "codigo": "F-08",
        "titulo": "Control de Financiamiento",
        "categoria": "Tesorería",
        "normativa": "Presenta un detalle de los préstamos adquiridos por la municipalidad con entes financieros nacionales e internacionales y la fuente de pago.",
    },
    {
        "codigo": "F-09",
        "titulo": "Control de Bienes Muebles e Inmuebles",
        "categoria": "Activos",
        "normativa": "Se describen todos los Bienes Muebles e Inmuebles propiedad de la Municipalidad, Empresas Municipales y Mancomunidades (inventario de Propiedad, Planta y Equipo).",
    },
    {
        "codigo": "F-10",
        "titulo": "Informe Anual de Proyectos",
        "categoria": "Inversión",
        "normativa": "Describe los proyectos ejecutados y en proceso de ejecución al 31 de diciembre del año que se está liquidando.",
    },
    {
        "codigo": "F-11",
        "titulo": "Estado de Ingresos y Egresos",
        "categoria": "Estados",
        "normativa": "Es la diferencia entre los ingresos recaudados y los egresos ejecutados, sin considerar el saldo efectivo del año anterior y los montos de préstamos entre otros, resultando un Superávit (utilidad) o un Déficit (pérdida).",
    },
    {
        "codigo": "F-12",
        "titulo": "Balance General",
        "categoria": "Estados",
        "normativa": "Muestra la situación financiera de la Municipalidad al 31 de diciembre del año que se está liquidando, reportando el total de los Activos, Pasivos y del Patrimonio Municipal.",
    },
    {
        "codigo": "F-13",
        "titulo": "Estado de Ingresos y Egresos Comparativos",
        "categoria": "Comparativos",
        "normativa": "Compara los resultados del año que se está liquidando con el año anterior para observar variaciones.",
    },
    {
        "codigo": "F-14",
        "titulo": "Balances Generales Comparativos",
        "categoria": "Comparativos",
        "normativa": "Compara Activo, Pasivo y Patrimonio del año actual vs año anterior, con variaciones monetarias y porcentuales.",
    },
]


def get_forma_by_index(num):
    """num: 1..14"""
    if num < 1 or num > len(FORMAS_RENDICION):
        return None
    return FORMAS_RENDICION[num - 1]


# --- IAIP (Instituto de Acceso a la Información Pública) — publicación proactiva ---
# Referencia: Ley de Acceso a la Información Pública y normativa de transparencia municipal.
# Ajustar textos y numeración a lineamientos/circulares oficiales del IAIP cuando se publiquen.

FORMAS_IAIP = [
    {
        "codigo": "IAIP-P01",
        "titulo": "Oficial de Información Pública (OIP) y datos del Portal de Transparencia",
        "categoria": "OIP / Portal Único",
        "normativa": "Ley de Transparencia y Acceso a la Información Pública (Honduras) y lineamientos IAIP: identificación del ente, responsable OIP y referencia al Portal Único de Transparencia.",
    },
    {
        "codigo": "IAIP-P02",
        "titulo": "Finanzas — Presupuesto y ejecución (resumen publicable)",
        "categoria": "Finanzas",
        "normativa": "Publicación activa de información financiera y presupuestaria (presupuesto vigente vs ejecución; montos agregados y comprensibles).",
    },
    {
        "codigo": "IAIP-P03",
        "titulo": "Finanzas — Modificaciones presupuestarias (reformas del período)",
        "categoria": "Finanzas",
        "normativa": "Publicación de reformas presupuestarias (ampliaciones, reducciones y traspasos) con referencia documental, conforme práctica de transparencia municipal.",
    },
    {
        "codigo": "IAIP-P04",
        "titulo": "Finanzas — Ejecución por fuente de financiamiento (fondos)",
        "categoria": "Finanzas",
        "normativa": "Transparencia en el uso de fondos/fuentes de financiamiento y sus saldos (vigente, ejecutado, saldo).",
    },
    {
        "codigo": "IAIP-P05",
        "titulo": "Adquisiciones, contrataciones y órdenes de pago",
        "categoria": "Compras / Contrataciones",
        "normativa": "Publicación activa de contrataciones y obligaciones (según lineamientos IAIP y resguardos de datos personales cuando aplique).",
    },
    {
        "codigo": "IAIP-P06",
        "titulo": "Proyectos e inversión pública municipal",
        "categoria": "Inversión",
        "normativa": "Publicación activa de programas, proyectos e inversión municipal (avance y ejecución publicable).",
    },
    {
        "codigo": "IAIP-P07",
        "titulo": "Finanzas — Operaciones manuales y ajustes registrados",
        "categoria": "Finanzas",
        "normativa": "Movimientos manuales y ajustes registrados (ingresos/egresos) para transparencia del registro.",
    },
    {
        "codigo": "IAIP-P08",
        "titulo": "Índice de cumplimiento de publicación activa (checklist)",
        "categoria": "Cumplimiento",
        "normativa": "Checklist interno para verificar publicación en el Portal Único de Transparencia (IAIP), según apartados aplicables a municipalidades.",
    },
]


def get_iaip_by_index(num):
    """num: 1..len(FORMAS_IAIP)"""
    if num < 1 or num > len(FORMAS_IAIP):
        return None
    return FORMAS_IAIP[num - 1]

# -*- coding: utf-8 -*-
"""
Contraloría General de la República (CGR) — informes de rendición / fiscalización.
Referencia: Ley Orgánica de la Contraloría; ajustar a circulares oficiales vigentes.
"""

FORMAS_CGR = [
    {
        "codigo": "CGR-01",
        "titulo": "Identificación del ente sujeto a control y periodo fiscal",
        "categoria": "Identificación",
        "normativa": "Datos del ente fiscalizado, ejercicio y alcance del informe (marco CGR).",
    },
    {
        "codigo": "CGR-02",
        "titulo": "Estado consolidado de ejecución presupuestaria",
        "categoria": "Ejecución",
        "normativa": "Síntesis de ejecución de ingresos y egresos por estructura programática.",
    },
    {
        "codigo": "CGR-03",
        "titulo": "Informe de reformas presupuestarias",
        "categoria": "Reformas",
        "normativa": "Relación cronológica de reformas con montos y cuentas afectadas.",
    },
    {
        "codigo": "CGR-04",
        "titulo": "Compromisos de gasto y órdenes de pago",
        "categoria": "Gasto",
        "normativa": "Trazabilidad entre reserva presupuestaria y liquidación de obligaciones.",
    },
    {
        "codigo": "CGR-05",
        "titulo": "Proyectos de inversión y focalización del gasto",
        "categoria": "Inversión",
        "normativa": "Relación de proyectos y coherencia con el plan de inversión.",
    },
    {
        "codigo": "CGR-06",
        "titulo": "Ejecución mensual acumulada (ingresos y egresos)",
        "categoria": "Seguimiento",
        "normativa": "Comportamiento mensual para análisis de ritmo de ejecución.",
    },
    {
        "codigo": "CGR-07",
        "titulo": "Control interno, hallazgos y observaciones",
        "categoria": "Control",
        "normativa": "Espacio para observaciones del órgano interno y medidas (plantilla base).",
    },
    {
        "codigo": "CGR-08",
        "titulo": "Declaración jurada, anexos y responsable del informe",
        "categoria": "Cierre",
        "normativa": "Declaración bajo gravedad de juramento y lista de anexos (según requerimiento CGR).",
    },
]


def get_cgr_by_index(num):
    """num: 1..len(FORMAS_CGR)"""
    if num < 1 or num > len(FORMAS_CGR):
        return None
    return FORMAS_CGR[num - 1]

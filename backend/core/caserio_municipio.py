# -*- coding: utf-8 -*-
"""
Relación municipio (tabla municipio.codigo) ↔ caserío (tabla caserio).

Regla: los dos primeros dígitos de municipio.codigo = caserio.depto;
los dos últimos dígitos de municipio.codigo = caserio.codmuni.
"""


def depto_y_codmuni_desde_codigo_municipio(codigo):
    """
    Devuelve (depto, codmuni) para filtrar caseríos, o (None, None) si el código es demasiado corto.
    Usa los dos primeros y los dos últimos caracteres del código de municipio (p. ej. '0601' → '06', '01').
    """
    c = (codigo or '').strip()
    if len(c) < 4:
        return None, None
    return c[:2], c[-2:]

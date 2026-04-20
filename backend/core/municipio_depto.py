# -*- coding: utf-8 -*-
"""
Regla de negocio: el código de municipio (tabla `municipio`) debe comenzar con el mismo
prefijo de 2 caracteres que el código del departamento (tabla `departamento`).
Usado por el modelo, formularios y vistas.
"""


def municipio_prefijo_codigo(codigo):
    """Primeros 2 caracteres del código de municipio (prefijo de departamento)."""
    c = (codigo or '').strip()
    return c[:2] if len(c) >= 2 else ''


def dos_digitos_codigo_departamento(depto_val):
    """Normaliza `departamento.depto` a 2 caracteres para comparar con codigo[:2] del municipio."""
    d = (depto_val or '').strip()
    if not d:
        return ''
    if len(d) >= 2:
        return d[:2]
    return d.zfill(2)


def departamento_para_codigo_municipio(codigo):
    """Departamento que corresponde al prefijo del código de municipio, o None."""
    from core.models import Departamento

    pref = municipio_prefijo_codigo(codigo)
    if len(pref) < 2:
        return None
    exact = Departamento.objects.filter(depto=pref).first()
    if exact:
        return exact
    for dep in Departamento.objects.order_by('depto'):
        if pref == dos_digitos_codigo_departamento(dep.depto):
            return dep
    return None


def codigo_municipio_tiene_departamento_valido(codigo):
    """True si existe un departamento cuyo código encaja con los dos primeros dígitos del municipio."""
    return departamento_para_codigo_municipio(codigo) is not None


def municipio_codigo_coincide_departamento(codigo_municipio, departamento):
    """True si el código de municipio coincide con el departamento elegido."""
    if not departamento:
        return False
    pref = municipio_prefijo_codigo(codigo_municipio)
    if len(pref) < 2:
        return False
    return pref == dos_digitos_codigo_departamento(departamento.depto)

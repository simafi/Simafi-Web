# -*- coding: utf-8 -*-
"""
Permisos de aplicación (Rol → Permiso → Usuario), no privilegios del motor SQL.
"""
from core.module_access import MODULO_CODES
from usuarios.models import Usuario, Rol, Permiso


def catalogo_modulo_configurado(modulo: str) -> bool:
    """True si ya existen permisos activos para ese código de módulo (columna modulo)."""
    return Permiso.objects.filter(modulo=modulo, is_active=True).exists()


def usuario_tiene_permiso(request, codigo_permiso: str) -> bool:
    """
    True si el usuario de la sesión modular tiene el permiso vía algún rol activo.
    Los superusuarios siempre pasan.
    Si el catálogo de un módulo (catastro, tributario, administrativo, …) aún no tiene filas
    en `Permiso`, se permite cualquier código `modulo.*` de ese módulo (compatibilidad).
    """
    uid = request.session.get("user_id")
    if not uid:
        return False
    try:
        user = Usuario.objects.get(pk=uid, is_active=True)
    except Usuario.DoesNotExist:
        return False

    if getattr(user, "es_superusuario", False):
        return True

    codigo = (codigo_permiso or "").strip()
    if not codigo:
        return False

    prefijo_mod = codigo.split(".", 1)[0] if "." in codigo else ""
    if prefijo_mod in MODULO_CODES and not catalogo_modulo_configurado(prefijo_mod):
        return True

    return Rol.objects.filter(
        is_active=True,
        permisos__codigo=codigo,
        permisos__is_active=True,
        usuarios_asignados__usuario_id=user.pk,
        usuarios_asignados__is_active=True,
    ).exists()


def permisos_catastro_menu_context(request):
    """Flags para ocultar tarjetas del menú Catastro según roles."""
    from catastro.permisos_codigos import (
        CATASTRO_PERM_BIENES_VER,
        CATASTRO_PERM_BIENES_EDITAR,
        CATASTRO_PERM_MAPA_VER,
        CATASTRO_PERM_MISC_VER,
        CATASTRO_PERM_NOTIFICACIONES_VER,
        CATASTRO_PERM_GRAFICOS_VER,
        CATASTRO_PERM_REPORTES_VER,
        CATASTRO_PERM_EMISION_VER,
        CATASTRO_PERM_CONFIG_VER,
    )

    return {
        "perm_catastro_bienes": usuario_tiene_permiso(request, CATASTRO_PERM_BIENES_VER)
        or usuario_tiene_permiso(request, CATASTRO_PERM_BIENES_EDITAR),
        "perm_catastro_bienes_editar": usuario_tiene_permiso(request, CATASTRO_PERM_BIENES_EDITAR),
        "perm_catastro_mapa": usuario_tiene_permiso(request, CATASTRO_PERM_MAPA_VER),
        "perm_catastro_misc": usuario_tiene_permiso(request, CATASTRO_PERM_MISC_VER),
        "perm_catastro_notif": usuario_tiene_permiso(request, CATASTRO_PERM_NOTIFICACIONES_VER),
        "perm_catastro_graficos": usuario_tiene_permiso(request, CATASTRO_PERM_GRAFICOS_VER),
        "perm_catastro_reportes": usuario_tiene_permiso(request, CATASTRO_PERM_REPORTES_VER),
        "perm_catastro_emision": usuario_tiene_permiso(request, CATASTRO_PERM_EMISION_VER),
        "perm_catastro_config": usuario_tiene_permiso(request, CATASTRO_PERM_CONFIG_VER),
    }

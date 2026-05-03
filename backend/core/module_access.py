# -*- coding: utf-8 -*-
"""
Control de acceso por módulo: prefijos URL, sesión y sincronización con Catastro.
"""
import logging
from django.contrib.auth.hashers import check_password
from urllib.parse import quote

from django.db import DatabaseError, OperationalError, ProgrammingError

from usuarios.models import Permiso, Rol, Usuario, UsuarioAccesoModulo

logger = logging.getLogger(__name__)


def codigos_empresa_equivalentes(codigo_municipio):
    """
    Variantes de Municipio.codigo para comparar con Usuario.empresa (login, búsquedas).
    Evita credenciales «incorrectas» cuando el catálogo tiene 0502 y el usuario se guardó como 502.
    """
    c = (codigo_municipio or '').strip()
    if not c:
        return []
    out = {c}
    if c.isdigit():
        out.add(c.zfill(4))
        short = c.lstrip('0') or '0'
        out.add(short)
        out.add(short.zfill(4))
    return list(out)


def canon_empresa_desde_municipio(municipio):
    """Formato estable al guardar Usuario.empresa (códigos numéricos en 4 dígitos)."""
    if not municipio:
        return ''
    c = (getattr(municipio, 'codigo', None) or '').strip()
    if c.isdigit():
        return c.zfill(4)
    return c


def catalogo_modulo_tiene_permisos(codigo):
    """True si existe al menos un permiso activo del módulo (columna `modulo`)."""
    return Permiso.objects.filter(modulo=codigo, is_active=True).exists()

# Orden mostrado en formularios de administración
MODULOS_SISTEMA = (
    ('catastro', 'Catastro'),
    ('tributario', 'Tributario'),
    ('administrativo', 'Administrativo'),
    ('compras', 'Compras'),
    ('contabilidad', 'Contabilidad'),
    ('tesoreria', 'Tesorería'),
    ('presupuestos', 'Presupuestos'),
    ('configuracion', 'Configuración'),
    ('servicios-publicos', 'Servicios Públicos'),
)

MODULO_CODES = {code for code, _ in MODULOS_SISTEMA}


def sincronizar_privilegios_modular_desde_bd(request):
    """
    Alinea la sesión modular con el usuario en BD (fuente de verdad).
    Corrige desfaces de es_superusuario / empresa tras navegar módulos o sesiones mezcladas.
    Devuelve True si la sesión sigue válida; False si se hizo flush (usuario inexistente o inactivo).
    """
    uid = request.session.get('user_id')
    if not uid:
        return True
    try:
        user = Usuario.objects.filter(pk=uid, is_active=True).first()
    except (ProgrammingError, OperationalError, DatabaseError) as exc:
        logger.warning("No se pudo sincronizar privilegios (¿migraciones pendientes?): %s", exc)
        request.session.flush()
        return False
    if not user:
        request.session.flush()
        return False
    request.session['es_superusuario'] = bool(getattr(user, 'es_superusuario', False))
    request.session['empresa'] = user.empresa or ''
    request.session['municipio_id'] = user.municipio_id
    request.session['nombre'] = user.nombre or user.usuario
    request.session['usuario'] = user.usuario
    request.session.modified = True
    return True


# Prefijo de URL → código interno del módulo
_PREFIXES = (
    ('/catastro/', 'catastro'),
    ('/tributario/', 'tributario'),
    ('/administrativo/', 'administrativo'),
    ('/compras/', 'compras'),
    ('/contabilidad/', 'contabilidad'),
    ('/tesoreria/', 'tesoreria'),
    ('/presupuestos/', 'presupuestos'),
    ('/configuracion/', 'configuracion'),
    ('/servicios-publicos/', 'servicios-publicos'),
)


def modulo_desde_ruta(path):
    """Devuelve el código de módulo si la ruta está protegida, o None."""
    if not path:
        return None
    if not path.startswith('/'):
        path = '/' + path
    for prefix, code in _PREFIXES:
        if path.startswith(prefix):
            return code
    return None


def usuario_puede_acceso_modulo(request, codigo):
    """
    True si el usuario de la sesión modular puede usar ese módulo.
    - Superusuario: todos.
    - Fila activa en UsuarioAccesoModulo (checkbox + clave por módulo en «Usuarios del sistema»).
    - O rol(es) con algún Permiso cuyo campo `modulo` coincide con el código del módulo.
    - Si el módulo no tiene permisos en catálogo, mismo criterio amplio que `usuario_tiene_permiso`
      (acceso a pantallas del módulo sin bloquear por middleware).
    """
    if codigo not in MODULO_CODES:
        return True
    uid = request.session.get('user_id')
    if not uid:
        return False
    if request.session.get('es_superusuario'):
        return True
    try:
        if UsuarioAccesoModulo.objects.filter(
            usuario_id=uid,
            codigo_modulo=codigo,
            is_active=True,
        ).exists():
            return True
    except (ProgrammingError, OperationalError, DatabaseError) as exc:
        logger.warning("No se pudo verificar acceso al módulo (¿migraciones pendientes?): %s", exc)
        return False

    try:
        if Rol.objects.filter(
            is_active=True,
            permisos__modulo=codigo,
            permisos__is_active=True,
            usuarios_asignados__usuario_id=uid,
            usuarios_asignados__is_active=True,
        ).exists():
            return True
    except (ProgrammingError, OperationalError, DatabaseError) as exc:
        logger.warning("No se pudo verificar acceso por rol al módulo: %s", exc)
        return False

    if not catalogo_modulo_tiene_permisos(codigo):
        return True

    return False


def session_key_modulo(codigo):
    return f'mod_auth_{codigo}'


def limpiar_accesos_modulo_en_sesion(request):
    """Quita todas las banderas mod_auth_* de la sesión (p. ej. al cerrar sesión modular)."""
    keys = [k for k in list(request.session.keys()) if k.startswith('mod_auth_')]
    for k in keys:
        del request.session[k]


def verificar_password_modulo(usuario, codigo_modulo, password_plano):
    """
    Valida la contraseña del módulo. Los superusuarios no usan esta tabla.
    """
    if not usuario or not usuario.is_active:
        return False
    if getattr(usuario, 'es_superusuario', False):
        return True
    if codigo_modulo not in MODULO_CODES:
        return False
    try:
        acc = UsuarioAccesoModulo.objects.get(
            usuario=usuario,
            codigo_modulo=codigo_modulo,
            is_active=True,
        )
    except UsuarioAccesoModulo.DoesNotExist:
        return False
    if not password_plano:
        return False
    if acc.password.startswith('pbkdf2_sha256'):
        return check_password(password_plano, acc.password)
    return acc.password == password_plano


def marcar_acceso_modulo_ok(request, codigo_modulo):
    request.session[session_key_modulo(codigo_modulo)] = True
    request.session.modified = True


def tiene_acceso_modulo_sesion(request, codigo_modulo):
    if request.session.get('es_superusuario'):
        return True
    return bool(request.session.get(session_key_modulo(codigo_modulo)))


def sincronizar_sesion_catastro(request):
    """
    Tras autorizar el módulo Catastro, copia datos de la sesión modular a las claves que usa catastro.
    """
    uid = request.session.get('user_id')
    empresa = (request.session.get('empresa') or '').strip()
    nombre = request.session.get('nombre') or ''
    municipio_id = request.session.get('municipio_id')
    descripcion = ''
    if municipio_id:
        from core.models import Municipio
        m = Municipio.objects.filter(id=municipio_id).first()
        if m:
            descripcion = m.descripcion or ''
    if uid:
        if empresa:
            request.session['catastro_empresa'] = empresa
        else:
            request.session.pop('catastro_empresa', None)
        request.session['catastro_usuario_id'] = uid
        request.session['catastro_usuario_nombre'] = nombre
        request.session['catastro_municipio_descripcion'] = descripcion
        request.session.modified = True


def url_acceso_modulo(codigo_modulo, siguiente_ruta):
    """URL interna hacia la pantalla de contraseña del módulo."""
    from django.urls import reverse
    base = reverse('modules_core:acceso_modulo', kwargs={'codigo': codigo_modulo})
    if siguiente_ruta:
        return f'{base}?next={quote(siguiente_ruta, safe="/")}'
    return base

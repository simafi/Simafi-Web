import hashlib
from urllib.parse import quote

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.db.models import Prefetch

from core.models import Municipio
from core.module_access import (
    MODULO_CODES,
    limpiar_accesos_modulo_en_sesion,
    sincronizar_privilegios_modular_desde_bd,
    sincronizar_sesion_catastro,
    usuario_puede_acceso_modulo,
)

from core.forms_modular import UsuarioSistemaForm, RolForm
from usuarios.models import Usuario, UsuarioRol, Rol


def _password_login_valida(plain: str, stored: str) -> bool:
    """Acepta hash Django (pbkdf2) y, por compatibilidad, SHA256 hex legado."""
    if not plain or stored is None:
        return False
    if stored.startswith("pbkdf2_") or stored.startswith("argon2"):
        return check_password(plain, stored)
    try:
        if len(stored) == 64 and all(c in "0123456789abcdefABCDEF" for c in stored):
            return stored.lower() == hashlib.sha256(plain.encode()).hexdigest()
    except Exception:
        pass
    return check_password(plain, stored)


def _siguiente_seguro(raw_next):
    if not raw_next or not isinstance(raw_next, str):
        return ''
    raw_next = raw_next.strip()
    if raw_next.startswith('/') and not raw_next.startswith('//'):
        return raw_next
    return ''


def login_principal(request):
    """
    Acceso al sistema modular: usuario y contraseña obligatorios.
    Municipio obligatorio para usuarios normales; los superusuarios únicos pueden omitirlo
    (varios superusuarios con el mismo nombre deben elegir municipio para desambiguar).
    """
    if request.method == 'POST':
        usuario = (request.POST.get('usuario') or '').strip()
        municipio_id = (request.POST.get('municipio') or '').strip()
        password = request.POST.get('password') or ''
        next_raw = request.POST.get('next') or request.GET.get('next')

        if not (usuario and password):
            messages.error(request, 'Usuario y contraseña son obligatorios')
        else:
            user = None
            err = None
            if municipio_id:
                try:
                    municipio = Municipio.objects.get(id=municipio_id)
                except Municipio.DoesNotExist:
                    err = 'Municipio no válido'
                else:
                    user = Usuario.objects.filter(
                        usuario=usuario,
                        empresa=municipio.codigo,
                        is_active=True,
                    ).first()
                    if not user:
                        err = 'Credenciales incorrectas o usuario no pertenece a ese municipio.'
            else:
                sup = Usuario.objects.filter(usuario=usuario, es_superusuario=True, is_active=True)
                n = sup.count()
                if n == 1:
                    user = sup.first()
                elif n > 1:
                    err = (
                        'Hay más de un superusuario con ese nombre. Seleccione el municipio '
                        'en el desplegable para indicar la cuenta correcta.'
                    )
                else:
                    err = 'Seleccione el municipio (los usuarios municipales deben indicar su municipio).'

            if err:
                messages.error(request, err)
            elif user:
                if user.is_locked():
                    messages.error(
                        request,
                        'Esta cuenta está temporalmente bloqueada por intentos fallidos. Intente más tarde.',
                    )
                elif not _password_login_valida(password, user.password):
                    try:
                        user.record_failed_login()
                    except Exception:
                        pass
                    messages.error(request, 'Credenciales incorrectas.')
                else:
                    request.session['user_id'] = user.id
                    request.session['usuario'] = user.usuario
                    request.session['empresa'] = user.empresa or ''
                    request.session['municipio_id'] = user.municipio_id
                    request.session['nombre'] = user.nombre or user.usuario
                    request.session['es_superusuario'] = bool(getattr(user, 'es_superusuario', False))
                    limpiar_accesos_modulo_en_sesion(request)

                    try:
                        user.record_successful_login()
                    except Exception:
                        pass

                    messages.success(request, f'Bienvenido {user.nombre or user.usuario}')
                    dest = _siguiente_seguro(next_raw)
                    if dest:
                        return redirect(dest)
                    return redirect('modules_core:menu_principal')

    municipios = Municipio.objects.all()
    next_url = _siguiente_seguro(request.GET.get('next'))
    return render(request, 'core/login.html', {'municipios': municipios, 'next': next_url})


def acceso_modulo(request, codigo):
    """
    Compatibilidad: enlaces antiguos a /acceso-modulo/<codigo>/ redirigen al módulo.
    El acceso real se controla solo con el login modular (sin segunda contraseña por módulo).
    """
    codigo = (codigo or '').strip().lower()
    if codigo not in MODULO_CODES:
        raise Http404('Módulo no válido')

    if not request.session.get('user_id'):
        login_url = reverse('modules_core:login_principal')
        return redirect(f'{login_url}?next={quote(request.get_full_path(), safe="/")}')

    if not sincronizar_privilegios_modular_desde_bd(request):
        login_url = reverse('modules_core:login_principal')
        return redirect(f'{login_url}?next={quote(request.get_full_path(), safe="/")}')

    get_object_or_404(Usuario, pk=request.session['user_id'], is_active=True)

    if not usuario_puede_acceso_modulo(request, codigo):
        messages.error(
            request,
            'No tiene permiso para acceder a este módulo.',
        )
        return redirect('modules_core:menu_principal')

    if codigo == 'catastro':
        sincronizar_sesion_catastro(request)

    dest = _siguiente_seguro(request.POST.get('next') or request.GET.get('next')) or f'/{codigo}/'
    return redirect(dest)


def _hay_superusuario_en_bd():
    return Usuario.objects.filter(es_superusuario=True, is_active=True).exists()


def _requiere_acceso_admin_usuarios(request):
    """
    Superusuarios: acceso completo.
    Si no hay ningún superusuario en BD, cualquier sesión modular puede administrar
    (primer arranque: crear o marcar el primer superusuario).
    """
    if not request.session.get('user_id'):
        return redirect('modules_core:login_principal')
    if not sincronizar_privilegios_modular_desde_bd(request):
        return redirect('modules_core:login_principal')
    if _hay_superusuario_en_bd() and not request.session.get('es_superusuario'):
        messages.error(request, 'Solo los superusuarios pueden configurar usuarios del sistema.')
        return redirect('modules_core:menu_principal')
    return None


def _ctx_config_inicial():
    return {
        'configuracion_inicial': not _hay_superusuario_en_bd(),
    }


def _sincronizar_superusuario_sesion(request, user):
    if user and user.pk == request.session.get('user_id'):
        request.session['es_superusuario'] = bool(user.es_superusuario)


def _requiere_superusuario_para_alta_usuario(request):
    """
    Crear usuario nuevo: solo superusuario (o modo arranque sin ningún superusuario en BD).
    """
    if not request.session.get('user_id'):
        return redirect('modules_core:login_principal')
    if not sincronizar_privilegios_modular_desde_bd(request):
        return redirect('modules_core:login_principal')
    if _hay_superusuario_en_bd() and not request.session.get('es_superusuario'):
        messages.error(request, 'Solo un superusuario puede crear nuevos usuarios.')
        return redirect('modules_core:usuarios_sistema_list')
    return None


def _puede_mostrar_gestion_usuarios_en_menu(request):
    """Tarjetas Usuarios/Roles: requiere sesión; primer arranque o superusuario."""
    uid = request.session.get('user_id')
    if not uid:
        return False
    if not _hay_superusuario_en_bd():
        return True
    return bool(request.session.get('es_superusuario'))


def _filtrar_modulos_menu_por_privilegio(request, modulos):
    """
    Con sesión modular, oculta tarjetas de módulos no asignados en UsuarioAccesoModulo.
    Invitado y superusuario: sin filtrar.
    """
    if not request.session.get('user_id') or request.session.get('es_superusuario'):
        return modulos
    out = []
    for m in modulos:
        url = (m.get('url') or '').strip()
        if url == '#' or url.startswith('ciudadano'):
            out.append(m)
            continue
        if m.get('url_name'):
            out.append(m)
            continue
        part = url.strip('/').split('/')[0]
        if part not in MODULO_CODES:
            out.append(m)
            continue
        if usuario_puede_acceso_modulo(request, part):
            out.append(m)
    return out


def usuarios_sistema_list(request):
    redir = _requiere_acceso_admin_usuarios(request)
    if redir:
        return redir
    qs = (
        Usuario.objects.all()
        .order_by('empresa', 'usuario')
        .prefetch_related(
            Prefetch(
                'roles_asignados',
                queryset=UsuarioRol.objects.filter(is_active=True).select_related('rol'),
            )
        )
    )
    ctx = {
        'object_list': qs,
        'usuario': request.session.get('nombre'),
        'empresa': request.session.get('empresa'),
        'puede_crear_usuario': (not _hay_superusuario_en_bd())
        or bool(request.session.get('es_superusuario')),
    }
    ctx.update(_ctx_config_inicial())
    return render(request, 'core/usuarios_sistema_list.html', ctx)


def usuarios_sistema_create(request):
    redir = _requiere_superusuario_para_alta_usuario(request)
    if redir:
        return redir
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            editor = get_object_or_404(Usuario, pk=request.session['user_id'])
            user = form.save(asignado_por=editor)
            _sincronizar_superusuario_sesion(request, user)
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('modules_core:usuarios_sistema_list')
    else:
        form = UsuarioSistemaForm()
    ctx = {
        'form': form,
        'titulo': 'Nuevo usuario del sistema',
        'usuario': request.session.get('nombre'),
        'empresa': request.session.get('empresa'),
    }
    ctx.update(_ctx_config_inicial())
    return render(request, 'core/usuarios_sistema_form.html', ctx)


def roles_list(request):
    redir = _requiere_acceso_admin_usuarios(request)
    if redir:
        return redir
    qs = Rol.objects.all().order_by('nombre').prefetch_related('permisos')
    ctx = {
        'object_list': qs,
        'usuario': request.session.get('nombre'),
    }
    ctx.update(_ctx_config_inicial())
    return render(request, 'core/roles_list.html', ctx)


def roles_create(request):
    redir = _requiere_acceso_admin_usuarios(request)
    if redir:
        return redir
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol creado correctamente.')
            return redirect('modules_core:roles_list')
    else:
        form = RolForm()
    ctx = {
        'form': form,
        'titulo': 'Nuevo rol',
        'usuario': request.session.get('nombre'),
    }
    ctx.update(_ctx_config_inicial())
    return render(request, 'core/roles_form.html', ctx)


def roles_update(request, pk):
    redir = _requiere_acceso_admin_usuarios(request)
    if redir:
        return redir
    inst = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol actualizado.')
            return redirect('modules_core:roles_list')
    else:
        form = RolForm(instance=inst)
    ctx = {
        'form': form,
        'titulo': f'Editar rol: {inst.nombre}',
        'usuario': request.session.get('nombre'),
        'edit_instance': inst,
    }
    ctx.update(_ctx_config_inicial())
    return render(request, 'core/roles_form.html', ctx)


def roles_delete(request, pk):
    """Elimina un rol y las asignaciones a usuarios (UsuarioRol en cascada)."""
    redir = _requiere_acceso_admin_usuarios(request)
    if redir:
        return redir
    if request.method != 'POST':
        messages.error(request, 'Use el botón eliminar en el listado de roles.')
        return redirect('modules_core:roles_list')
    rol = get_object_or_404(Rol, pk=pk)
    n_asignaciones = UsuarioRol.objects.filter(rol=rol).count()
    nombre = rol.nombre
    rol.delete()
    msg = f'Rol «{nombre}» eliminado correctamente.'
    if n_asignaciones:
        msg += f' Se desasignó de {n_asignaciones} usuario(s).'
    messages.success(request, msg)
    return redirect('modules_core:roles_list')


def usuarios_sistema_update(request, pk):
    redir = _requiere_acceso_admin_usuarios(request)
    if redir:
        return redir
    inst = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST, instance=inst)
        if form.is_valid():
            editor = get_object_or_404(Usuario, pk=request.session['user_id'])
            user = form.save(asignado_por=editor)
            _sincronizar_superusuario_sesion(request, user)
            messages.success(request, 'Usuario actualizado.')
            return redirect('modules_core:usuarios_sistema_list')
    else:
        form = UsuarioSistemaForm(instance=inst)
    ctx = {
        'form': form,
        'titulo': f'Editar usuario: {inst.usuario}',
        'usuario': request.session.get('nombre'),
        'empresa': request.session.get('empresa'),
        'edit_instance': inst,
    }
    ctx.update(_ctx_config_inicial())
    return render(request, 'core/usuarios_sistema_form.html', ctx)


def menu_principal(request):
    """Menú modular: accesible sin login. Los módulos (salvo ciudadano) piden sesión y clave al entrar."""
    if request.session.get('user_id') and not sincronizar_privilegios_modular_desde_bd(request):
        return redirect('modules_core:login_principal')

    modulos = [
        {
            'nombre': 'Ciudadano',
            'descripcion': 'Portal del contribuyente: trámites en línea (no pide clave de módulo)',
            'url': 'ciudadano/',
            'icono': 'fas fa-user-check',
            'color': 'dark',
        },
        {
            'nombre': 'Catastro',
            'descripcion': 'Gestión de bienes inmuebles, vehículos y terrenos',
            'url': 'catastro/',
            'icono': 'fas fa-building',
            'color': 'primary',
        },
        {
            'nombre': 'Tributario',
            'descripcion': 'Gestión de impuestos y tasas municipales',
            'url': 'tributario/',
            'icono': 'fas fa-calculator',
            'color': 'success',
        },
        {
            'nombre': 'Administrativo',
            'descripcion': 'Gestión administrativa y financiera',
            'url': 'administrativo/',
            'icono': 'fas fa-briefcase',
            'color': 'info',
        },
        {
            'nombre': 'Compras',
            'descripcion': 'Requisiciones, cotizaciones (ONCAE), órdenes de compra y bodega',
            'url': 'compras/',
            'icono': 'fas fa-shopping-cart',
            'color': 'success',
        },
        {
            'nombre': 'Contabilidad',
            'descripcion': 'Sistema Contable NIC/IAS',
            'url': 'contabilidad/',
            'icono': 'fas fa-book',
            'color': 'warning',
        },
        {
            'nombre': 'Tesorería',
            'descripcion': 'Gestión de tesorería y caja',
            'url': 'tesoreria/',
            'icono': 'fas fa-cash-register',
            'color': 'secondary',
        },
        {
            'nombre': 'Presupuestos',
            'descripcion': 'Planificación y control presupuestario',
            'url': 'presupuestos/',
            'icono': 'fas fa-chart-pie',
            'color': 'danger',
        },
        {
            'nombre': 'Ambiental',
            'descripcion': 'Gestión ambiental y recursos naturales',
            'url': '#',
            'icono': 'fas fa-leaf',
            'color': 'success',
        },
        {
            'nombre': 'Servicios Públicos',
            'descripcion': 'Facturación de agua potable, alcantarillado y otros servicios municipales',
            'url': 'servicios-publicos/',
            'icono': 'fas fa-tint',
            'color': 'info',
        },
        {
            'nombre': 'Convenios de Pagos',
            'descripcion': 'Gestión de convenios y acuerdos de pago',
            'url': '#',
            'icono': 'fas fa-handshake',
            'color': 'info',
        },
        {
            'nombre': 'Configuración',
            'descripcion': 'Catálogos generales: departamentos, municipios, caseríos, nacionalidades',
            'url': 'configuracion/',
            'icono': 'fas fa-cog',
            'color': 'secondary',
        },
        {
            'nombre': 'Reportes',
            'descripcion': 'Generación de reportes y estadísticas',
            'url': '#',
            'icono': 'fas fa-chart-bar',
            'color': 'warning',
        },
    ]

    if _puede_mostrar_gestion_usuarios_en_menu(request):
        modulos.insert(
            0,
            {
                'nombre': 'Roles y permisos',
                'descripcion': 'Definir roles y permisos (solo superusuario)',
                'url': 'menu/roles/',
                'url_name': 'modules_core:roles_list',
                'icono': 'fas fa-user-shield',
                'color': 'info',
            },
        )
        modulos.insert(
            0,
            {
                'nombre': 'Usuarios del sistema',
                'descripcion': 'Crear usuarios y contraseña por módulo, p. ej. Tributario (solo superusuario)',
                'url': 'menu/usuarios-sistema/',
                'url_name': 'modules_core:usuarios_sistema_list',
                'icono': 'fas fa-users-cog',
                'color': 'primary',
            },
        )

    uid = request.session.get('user_id')
    mostrar_gestion = _puede_mostrar_gestion_usuarios_en_menu(request)
    emp = (request.session.get('empresa') or '').strip()
    es_sup = bool(request.session.get('es_superusuario'))
    modulos = _filtrar_modulos_menu_por_privilegio(request, modulos)
    context = {
        'usuario': request.session.get('nombre') or request.session.get('usuario'),
        'empresa': emp,
        'es_superusuario': es_sup,
        'superusuario_global': bool(uid and es_sup and not emp),
        'hay_superusuario_bd': _hay_superusuario_en_bd(),
        'sesion_modular': bool(uid),
        'mostrar_gestion_usuarios_menu': mostrar_gestion,
        'modulos': modulos,
    }
    if not uid:
        context['usuario'] = ''
    return render(request, 'core/menu_principal.html', context)


def logout_principal(request):
    """Cerrar sesión del sistema"""
    logout(request)
    request.session.flush()
    messages.success(request, 'Sesión cerrada. Puede seguir usando el menú modular; al entrar a un módulo se le pedirá identificación.')
    return redirect('modules_core:menu_principal')


def verificar_sesion(request):
    """Verificar si el usuario tiene sesión activa"""
    if request.session.get('user_id'):
        return JsonResponse({
            'autenticado': True,
            'usuario': request.session.get('nombre'),
            'empresa': request.session.get('empresa'),
            'es_superusuario': bool(request.session.get('es_superusuario')),
        })
    return JsonResponse({'autenticado': False})

import hashlib

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse
from .models import Municipio
from modules.usuarios.models import Usuario


def _password_login_valida(plain: str, stored: str) -> bool:
    """Misma lógica que venv/Scripts/core: Django hash o SHA256 hex legado."""
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


def login_principal(request):
    """
    Login menú modular: usuario + municipio (código empresa = municipio.codigo) + contraseña
    almacenada con hash Django (create usuario en /menu/usuarios-sistema/).
    """
    if request.method == 'POST':
        usuario = (request.POST.get('usuario') or '').strip()
        password = request.POST.get('password') or ''
        municipio_id = (request.POST.get('municipio') or '').strip()

        if not (usuario and password and municipio_id):
            messages.error(request, 'Usuario, contraseña y municipio son obligatorios.')
        else:
            try:
                municipio = Municipio.objects.get(id=municipio_id)
            except Municipio.DoesNotExist:
                messages.error(request, 'Municipio no válido.')
            else:
                user = Usuario.objects.filter(
                    usuario=usuario,
                    empresa=municipio.codigo,
                    is_active=True,
                ).first()
                if not user:
                    messages.error(
                        request,
                        'Usuario no encontrado para ese municipio. Verifique que el municipio en el login '
                        'sea el mismo asignado al usuario (código de empresa = código del municipio).',
                    )
                elif not _password_login_valida(password, user.password):
                    messages.error(request, 'Contraseña incorrecta.')
                else:
                    request.session['user_id'] = user.id
                    request.session['usuario'] = user.usuario
                    request.session['empresa'] = user.empresa or ''
                    request.session['municipio_id'] = user.municipio_id
                    request.session['nombre'] = user.nombre or user.usuario
                    request.session['es_superusuario'] = bool(getattr(user, 'es_superusuario', False))
                    messages.success(request, f'Bienvenido {user.nombre or user.usuario}')
                    return redirect('core:menu_principal')

    municipios = Municipio.objects.all()
    return render(request, 'core/login.html', {'municipios': municipios})


@login_required
def menu_principal(request):
    """Menú principal del sistema"""
    if not request.session.get('user_id'):
        return redirect('core:login_principal')
    
    context = {
        'usuario': request.session.get('nombre'),
        'empresa': request.session.get('empresa'),
        'modulos': [
            {
                'nombre': 'Catastro',
                'descripcion': 'Gestión de bienes inmuebles, vehículos y terrenos',
                'url': 'catastro:catastro_menu_principal',
                'icono': 'fas fa-building',
                'color': 'primary'
            },
            {
                'nombre': 'Tributario',
                'descripcion': 'Gestión de impuestos y tasas municipales',
                'url': 'tributario:tributario_login',
                'icono': 'fas fa-calculator',
                'color': 'success'
            },
            {
                'nombre': 'Administrativo',
                'descripcion': 'Gestión administrativa y financiera',
                'url': 'administrativo:administrativo_login',
                'icono': 'fas fa-chart-line',
                'color': 'info'
            }
        ]
    }
    return render(request, 'core/menu_principal.html', context)


def logout_principal(request):
    """Cerrar sesión del sistema"""
    logout(request)
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('core:login_principal')


def verificar_sesion(request):
    """Verificar si el usuario tiene sesión activa"""
    if request.session.get('user_id'):
        return JsonResponse({
            'autenticado': True,
            'usuario': request.session.get('nombre'),
            'empresa': request.session.get('empresa')
        })
    return JsonResponse({'autenticado': False})




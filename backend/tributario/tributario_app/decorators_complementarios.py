"""
Decoradores complementarios para tributario_app
Decoradores adicionales que no interfieren con el código principal
"""

from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

def require_municipio(view_func):
    """
    Decorador que requiere que haya un municipio en la sesión
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'empresa' not in request.session:
            messages.error(request, 'Debe seleccionar un municipio para continuar')
            return redirect('tributario:tributario_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def ajax_required(view_func):
    """
    Decorador que requiere que la petición sea AJAX
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Esta vista solo acepta peticiones AJAX'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper

def handle_exceptions(view_func):
    """
    Decorador para manejar excepciones de forma consistente
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error interno: {str(e)}'
                }, status=500)
            else:
                messages.error(request, f'Error interno: {str(e)}')
                return redirect(request.META.get('HTTP_REFERER', '/'))
    return wrapper

def log_activity(view_func):
    """
    Decorador para registrar actividad
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Registrar la actividad
        print(f"[ACTIVIDAD] Usuario: {request.user if hasattr(request, 'user') else 'Anónimo'}")
        print(f"[ACTIVIDAD] Vista: {view_func.__name__}")
        print(f"[ACTIVIDAD] Método: {request.method}")
        print(f"[ACTIVIDAD] Path: {request.path}")
        
        return view_func(request, *args, **kwargs)
    return wrapper




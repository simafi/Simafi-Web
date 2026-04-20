from django.shortcuts import render, redirect
from django.contrib import messages

def ambiental_login(request):
    """Vista de login del módulo Ambiental"""
    return render(request, 'ambiental/login.html', {
        'modulo': 'Ambiental',
        'descripcion': 'Gestión ambiental y recursos naturales'
    })

def ambiental_logout(request):
    """Vista de logout del módulo Ambiental"""
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('modules_core:menu_principal')

def ambiental_menu_principal(request):
    """Menú principal del módulo Ambiental"""
    return render(request, 'ambiental/menu_principal.html', {
        'modulo': 'Ambiental',
        'descripcion': 'Gestión ambiental y recursos naturales'
    })

from django.shortcuts import render, redirect
from django.contrib import messages

def reportes_login(request):
    """Vista de login del módulo Reportes"""
    return render(request, 'reportes/login.html', {
        'modulo': 'Reportes',
        'descripcion': 'Generación de reportes y estadísticas'
    })

def reportes_logout(request):
    """Vista de logout del módulo Reportes"""
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('modules_core:menu_principal')

def reportes_menu_principal(request):
    """Menú principal del módulo Reportes"""
    return render(request, 'reportes/menu_principal.html', {
        'modulo': 'Reportes',
        'descripcion': 'Generación de reportes y estadísticas'
    })

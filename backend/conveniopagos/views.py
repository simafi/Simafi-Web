from django.shortcuts import render, redirect
from django.contrib import messages

def conveniopagos_login(request):
    """Vista de login del módulo Convenios de Pagos"""
    return render(request, 'conveniopagos/login.html', {
        'modulo': 'Convenios de Pagos',
        'descripcion': 'Acuerdos y convenios de pago'
    })

def conveniopagos_logout(request):
    """Vista de logout del módulo Convenios de Pagos"""
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('modules_core:menu_principal')

def conveniopagos_menu_principal(request):
    """Menú principal del módulo Convenios de Pagos"""
    return render(request, 'conveniopagos/menu_principal.html', {
        'modulo': 'Convenios de Pagos',
        'descripcion': 'Acuerdos y convenios de pago'
    })

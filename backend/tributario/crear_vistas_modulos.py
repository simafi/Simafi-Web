#!/usr/bin/env python
"""
Script para crear vistas básicas para todos los módulos
"""
import os

# Lista de módulos y sus descripciones
modulos = [
    ('tesoreria', 'Tesorería', 'Gestión de tesorería y caja'),
    ('presupuestos', 'Presupuestos', 'Planificación y control presupuestario'),
    ('ambiental', 'Ambiental', 'Gestión ambiental y recursos naturales'),
    ('servicios_publicos', 'Servicios Públicos', 'Gestión de servicios municipales'),
    ('conveniopagos', 'Convenios de Pagos', 'Acuerdos y convenios de pago'),
    ('configuracion', 'Configuración', 'Configuración del sistema'),
    ('reportes', 'Reportes', 'Generación de reportes y estadísticas'),
    ('api', 'API', 'Interfaz de programación de aplicaciones'),
]

# Plantilla para las vistas
vista_template = '''from django.shortcuts import render, redirect
from django.contrib import messages

def {modulo}_login(request):
    """Vista de login del módulo {nombre}"""
    return render(request, '{modulo}/login.html', {{
        'modulo': '{nombre}',
        'descripcion': '{descripcion}'
    }})

def {modulo}_logout(request):
    """Vista de logout del módulo {nombre}"""
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('modules_core:menu_principal')

def {modulo}_menu_principal(request):
    """Menú principal del módulo {nombre}"""
    return render(request, '{modulo}/menu_principal.html', {{
        'modulo': '{nombre}',
        'descripcion': '{descripcion}'
    }})
'''

# Plantilla para vistas especiales (API)
api_vista_template = '''from django.shortcuts import render
from django.http import JsonResponse

def api_home(request):
    """Vista principal de la API"""
    return JsonResponse({{
        'status': 'success',
        'message': 'API del Sistema Municipal Modular',
        'version': '1.0.0'
    }})

def api_health(request):
    """Vista de salud de la API"""
    return JsonResponse({{
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z'
    }})
'''

def crear_vistas_modulo(modulo, nombre, descripcion):
    """Crear vistas para un módulo específico"""
    views_path = f'modules/{modulo}/views.py'
    
    if modulo == 'api':
        contenido = api_vista_template
    else:
        contenido = vista_template.format(
            modulo=modulo,
            nombre=nombre,
            descripcion=descripcion
        )
    
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Vistas creadas para {nombre}")

def main():
    """Función principal"""
    print("=== CREANDO VISTAS PARA TODOS LOS MÓDULOS ===")
    
    for modulo, nombre, descripcion in modulos:
        try:
            crear_vistas_modulo(modulo, nombre, descripcion)
        except Exception as e:
            print(f"❌ Error creando vistas para {nombre}: {e}")
    
    print("\n=== VISTAS CREADAS EXITOSAMENTE ===")

if __name__ == '__main__':
    main()


































#!/usr/bin/env python
"""
Vista para servir la página de prueba de la calculadora ICS
"""

from django.shortcuts import render
from django.http import HttpResponse
import os

def test_calculadora_ics(request):
    """
    Vista para mostrar la página de prueba de la calculadora ICS
    """
    # Ruta al archivo HTML de prueba
    html_file = os.path.join(os.path.dirname(__file__), 'test_calculadora_ics.html')
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Reemplazar la ruta del JavaScript para que funcione correctamente
        contenido = contenido.replace(
            'src="declaracion_volumen_calculator.js"',
            'src="/static/js/declaracion_volumen_calculator.js"'
        )
        
        return HttpResponse(contenido, content_type='text/html')
        
    except FileNotFoundError:
        return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Archivo no encontrado</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-danger">
                    <h4>Error 404</h4>
                    <p>No se encontró el archivo test_calculadora_ics.html</p>
                    <p>Asegúrese de que el archivo esté en la misma carpeta que este script.</p>
                </div>
            </div>
        </body>
        </html>
        """, content_type='text/html')

# Función alternativa usando template
def test_calculadora_template(request):
    """
    Vista alternativa usando el sistema de templates de Django
    """
    context = {
        'titulo': 'Test - Calculadora ICS',
        'descripcion': 'Prueba del sistema de cálculo automático para declaración de volumen'
    }
    return render(request, 'test_calculadora_ics.html', context)

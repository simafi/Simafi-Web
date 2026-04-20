#!/usr/bin/env python
"""
Instalación permanente de la calculadora ICS en el sistema Django
"""

import os
import shutil
from pathlib import Path

def instalar_calculadora_permanente():
    """
    Instala la calculadora ICS de forma permanente en el sistema Django
    """
    print("🚀 INSTALACIÓN PERMANENTE DE CALCULADORA ICS")
    print("=" * 55)
    
    # Rutas base
    base_dir = Path("c:/simafiweb")
    tributario_dir = Path("c:/simafiweb/venv/Scripts/tributario/tributario_app")
    
    # 1. Crear directorios necesarios
    templates_dir = tributario_dir / "templates"
    static_js_dir = tributario_dir / "static" / "js"
    
    templates_dir.mkdir(parents=True, exist_ok=True)
    static_js_dir.mkdir(parents=True, exist_ok=True)
    
    print("✅ Directorios creados:")
    print(f"   📁 {templates_dir}")
    print(f"   📁 {static_js_dir}")
    
    # 2. Copiar archivos
    archivos_a_copiar = [
        {
            'origen': base_dir / "test_calculadora_ics.html",
            'destino': templates_dir / "test_calculadora_ics.html",
            'descripcion': "Template HTML"
        },
        {
            'origen': base_dir / "declaracion_volumen_calculator.js",
            'destino': static_js_dir / "declaracion_volumen_calculator.js",
            'descripcion': "JavaScript calculadora"
        }
    ]
    
    for archivo in archivos_a_copiar:
        if archivo['origen'].exists():
            shutil.copy2(archivo['origen'], archivo['destino'])
            print(f"✅ {archivo['descripcion']}: {archivo['destino']}")
        else:
            print(f"❌ No encontrado: {archivo['origen']}")
    
    # 3. Crear vista en views.py
    views_file = tributario_dir / "views.py"
    vista_codigo = '''

def test_calculadora_ics(request):
    """
    Vista para la calculadora de prueba ICS
    """
    return render(request, 'test_calculadora_ics.html', {
        'titulo': 'Test - Calculadora ICS',
        'descripcion': 'Sistema de cálculo automático para declaración de volumen'
    })
'''
    
    if views_file.exists():
        with open(views_file, 'r', encoding='utf-8') as f:
            contenido_views = f.read()
        
        if 'test_calculadora_ics' not in contenido_views:
            with open(views_file, 'a', encoding='utf-8') as f:
                f.write(vista_codigo)
            print("✅ Vista agregada a views.py")
        else:
            print("⚠️  Vista ya existe en views.py")
    else:
        print("❌ No se encontró views.py")
    
    # 4. Crear código para urls.py
    url_codigo = '''
# Agregar al final de urlpatterns:
path('test-calculadora-ics/', views.test_calculadora_ics, name='test_calculadora_ics'),
'''
    
    # 5. Actualizar template HTML para usar rutas Django correctas
    template_file = templates_dir / "test_calculadora_ics.html"
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            contenido_html = f.read()
        
        # Actualizar ruta del JavaScript
        contenido_html = contenido_html.replace(
            'src="declaracion_volumen_calculator.js"',
            '{% load static %}\n    <script src="{% static \'js/declaracion_volumen_calculator.js\' %}"></script>'
        )
        
        # Agregar load static al inicio
        if '{% load static %}' not in contenido_html:
            contenido_html = '{% load static %}\n' + contenido_html
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(contenido_html)
        
        print("✅ Template actualizado con rutas Django")
    
    # 6. Mostrar instrucciones finales
    print("\n📋 PASOS FINALES MANUALES:")
    print("-" * 35)
    print("1. Abra el archivo:")
    print(f"   {tributario_dir}/urls.py")
    print()
    print("2. Agregue esta línea en urlpatterns:")
    print("   path('test-calculadora-ics/', views.test_calculadora_ics, name='test_calculadora_ics'),")
    print()
    print("3. Asegúrese que el import esté presente:")
    print("   from . import views")
    print()
    print("4. Reinicie el servidor Django")
    print()
    print("5. Acceda a:")
    print("   http://localhost:8080/tributario/test-calculadora-ics/")
    
    return True

def crear_template_django():
    """
    Crea un template optimizado para Django
    """
    template_content = '''{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo|default:"Test - Calculadora ICS" }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .resultado-calculo {
            background: #f8f9fa;
            border: 2px solid #28a745;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .campo-calculado {
            background: #e7f3ff;
            font-weight: bold;
            color: #0066cc;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h2>🧮 {{ titulo|default:"Test - Calculadora ICS" }}</h2>
        <p class="text-muted">{{ descripcion|default:"Prueba del sistema de cálculo automático" }}</p>

        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📊 Formulario de Declaración</h5>
                    </div>
                    <div class="card-body">
                        <form>
                            <div class="mb-3">
                                <label for="id_ventai" class="form-label">Ventas Industria</label>
                                <input type="text" class="form-control" id="id_ventai" placeholder="0">
                                <small class="text-muted">Ingrese el valor sin puntos ni comas</small>
                            </div>

                            <div class="mb-3">
                                <label for="id_ventac" class="form-label">Ventas Comercio</label>
                                <input type="text" class="form-control" id="id_ventac" placeholder="0">
                                <small class="text-muted">Ingrese el valor sin puntos ni comas</small>
                            </div>

                            <div class="mb-3">
                                <label for="id_ventas" class="form-label">Ventas Servicios</label>
                                <input type="text" class="form-control" id="id_ventas" placeholder="0">
                                <small class="text-muted">Ingrese el valor sin puntos ni comas</small>
                            </div>

                            <hr>

                            <!-- CAMPO IMPUESTO CALCULADO - RESULTADO PRINCIPAL -->
                            <div class="mb-3">
                                <label for="id_impuesto_calculado" class="form-label">
                                    <strong>💰 Impuesto Calculado</strong>
                                </label>
                                <input type="text" class="form-control campo-calculado" 
                                       id="id_impuesto_calculado" 
                                       readonly 
                                       placeholder="0.00">
                                <small class="text-success">Este campo se actualiza automáticamente</small>
                            </div>

                            <button type="button" class="btn btn-primary" id="btn-calcular">
                                🔢 Calcular Manualmente
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📈 Resultados del Cálculo</h5>
                    </div>
                    <div class="card-body">
                        <!-- Resumen Visual -->
                        <div id="resumen-visual">
                            <div class="alert alert-info">
                                <i class="fas fa-info-circle"></i>
                                Ingrese valores en el formulario para ver los cálculos
                            </div>
                        </div>

                        <!-- Detalles del Cálculo -->
                        <div id="tabla-detalles-calculo">
                            <!-- Se llena automáticamente con JavaScript -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <script src="{% static 'js/declaracion_volumen_calculator.js' %}"></script>
</body>
</html>'''
    
    return template_content

if __name__ == "__main__":
    print("🔧 INSTALADOR DE CALCULADORA ICS")
    print()
    
    exito = instalar_calculadora_permanente()
    
    if exito:
        print("\n🎉 INSTALACIÓN COMPLETADA")
        print("   ✅ Archivos copiados a ubicaciones Django")
        print("   ✅ Vista creada en views.py")
        print("   ✅ Template actualizado")
        print("   📋 Complete los pasos manuales mostrados arriba")
    else:
        print("\n❌ ERROR EN LA INSTALACIÓN")
    
    print("\n" + "=" * 60)

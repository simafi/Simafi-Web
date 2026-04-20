#!/usr/bin/env python
"""
Solución para agregar URL de test calculadora ICS
"""

def mostrar_solucion():
    print("🔧 SOLUCIÓN PARA ERROR 404 - TEST CALCULADORA")
    print("=" * 55)
    
    print("\n📁 OPCIÓN 1: Servir archivo HTML directamente")
    print("-" * 45)
    print("1. Copie test_calculadora_ics.html a:")
    print("   C:\\simafiweb\\venv\\Scripts\\tributario\\tributario_app\\templates\\")
    print()
    print("2. Agregue esta línea al urls.py principal:")
    print("   path('test-calculadora/', TemplateView.as_view(template_name='test_calculadora_ics.html'), name='test_calculadora'),")
    print()
    print("3. Agregue el import:")
    print("   from django.views.generic import TemplateView")
    
    print("\n📁 OPCIÓN 2: URL simple (más fácil)")
    print("-" * 35)
    print("Agregue estas líneas al archivo urls.py del módulo tributario:")
    print()
    print("# Import adicional")
    print("from django.http import HttpResponse")
    print("import os")
    print()
    print("# Función de vista")
    print("def test_calculadora(request):")
    print("    html_path = r'C:\\simafiweb\\test_calculadora_ics.html'")
    print("    if os.path.exists(html_path):")
    print("        with open(html_path, 'r', encoding='utf-8') as f:")
    print("            return HttpResponse(f.read(), content_type='text/html')")
    print("    return HttpResponse('Archivo no encontrado', status=404)")
    print()
    print("# En urlpatterns agregar:")
    print("path('test-calculadora/', test_calculadora, name='test_calculadora'),")
    
    print("\n🌐 ACCESO:")
    print("http://localhost:8080/test-calculadora/")
    
    print("\n📋 ARCHIVOS NECESARIOS:")
    print("✅ test_calculadora_ics.html (ya creado)")
    print("✅ declaracion_volumen_calculator.js (ya creado)")
    print("⚠️  Copiar JS a carpeta static/js/ del proyecto")

if __name__ == "__main__":
    mostrar_solucion()

#!/usr/bin/env python
"""
Paso final: Agregar URL a urls.py del módulo tributario
"""

import os
import glob

def encontrar_urls_tributario():
    """
    Encuentra y muestra el contenido necesario para urls.py
    """
    print("🔍 PASO FINAL: CONFIGURAR URL")
    print("=" * 40)
    
    # Buscar archivos urls.py en tributario
    posibles_urls = [
        r"C:\simafiweb\venv\Scripts\tributario\tributario_app\urls.py",
        r"C:\simafiweb\venv\Scripts\tributario\tributario\urls.py"
    ]
    
    archivo_encontrado = None
    for archivo in posibles_urls:
        if os.path.exists(archivo):
            archivo_encontrado = archivo
            break
    
    print(f"📁 Archivo a modificar:")
    print(f"   {archivo_encontrado or 'NO ENCONTRADO'}")
    print()
    
    print("📝 AGREGAR ESTAS LÍNEAS:")
    print("-" * 25)
    print()
    print("1️⃣ Al inicio del archivo (imports):")
    print("from . import views")
    print()
    print("2️⃣ En urlpatterns (dentro de la lista):")
    print("path('test-calculadora-ics/', views.test_calculadora_ics, name='test_calculadora_ics'),")
    print()
    
    print("🌐 URL FINAL:")
    print("http://localhost:8080/tributario/test-calculadora-ics/")
    print()
    
    print("✅ ARCHIVOS YA INSTALADOS:")
    print("   📄 Template: tributario_app/templates/test_calculadora_ics.html")
    print("   📜 JavaScript: tributario_app/static/js/declaracion_volumen_calculator.js")
    print("   🔧 Vista: Agregada a views.py")
    
    return archivo_encontrado

if __name__ == "__main__":
    encontrar_urls_tributario()
    print("\n🚀 Después de agregar la URL, reinicie el servidor Django")

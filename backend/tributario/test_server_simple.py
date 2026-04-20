#!/usr/bin/env python
"""
Script simple para probar el servidor Django
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')

try:
    django.setup()
    print("✅ Django configurado correctamente")
    
    # Probar importación de la vista
    from simple_views import declaracion_volumen
    print("✅ Vista declaracion_volumen importada correctamente")
    
    # Probar importación del formulario
    from tributario_app.forms import DeclaracionVolumenForm
    print("✅ Formulario DeclaracionVolumenForm importado correctamente")
    
    # Probar importación del modelo
    from tributario.models import DeclaracionVolumen
    print("✅ Modelo DeclaracionVolumen importado correctamente")
    
    print("\n🎉 Todas las importaciones exitosas. El servidor debería funcionar.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()































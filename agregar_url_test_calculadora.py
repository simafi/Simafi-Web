#!/usr/bin/env python
"""
Script para agregar la URL de prueba de la calculadora ICS al sistema Django
"""

import os
import shutil

def agregar_url_test_calculadora():
    """
    Agrega la URL para acceder a test_calculadora_ics
    """
    print("🔧 CONFIGURANDO URL PARA TEST CALCULADORA ICS")
    print("=" * 50)
    
    # Buscar el archivo urls.py principal del módulo tributario
    posibles_urls = [
        r"C:\simafiweb\venv\Scripts\tributario\tributario\urls.py",
        r"C:\simafiweb\venv\Scripts\tributario\tributario_app\urls.py",
        r"C:\simafiweb\modules\core\urls.py"
    ]
    
    archivo_urls = None
    for ruta in posibles_urls:
        if os.path.exists(ruta):
            archivo_urls = ruta
            print(f"✅ Archivo URLs encontrado: {ruta}")
            break
    
    if not archivo_urls:
        print("❌ No se encontró archivo urls.py")
        return False
    
    try:
        # Crear backup
        backup_file = archivo_urls + ".backup_test"
        shutil.copy2(archivo_urls, backup_file)
        print(f"✅ Backup creado: {backup_file}")
        
        # Leer contenido actual
        with open(archivo_urls, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar si ya existe la URL
        if 'test-calculadora-ics' in contenido:
            print("⚠️  La URL ya existe en el archivo")
            return True
        
        # Agregar import si no existe
        if 'from django.http import HttpResponse' not in contenido:
            contenido = contenido.replace(
                'from django.urls import path',
                'from django.urls import path\nfrom django.http import HttpResponse'
            )
        
        # Buscar el patrón urlpatterns y agregar la nueva URL
        if 'urlpatterns = [' in contenido:
            # Encontrar la posición después de urlpatterns = [
            pos = contenido.find('urlpatterns = [') + len('urlpatterns = [')
            
            # Insertar la nueva URL
            nueva_url = """
    # Test Calculadora ICS
    path('test-calculadora-ics/', lambda request: HttpResponse(open(r'C:\\simafiweb\\test_calculadora_ics.html', 'r', encoding='utf-8').read(), content_type='text/html'), name='test_calculadora_ics'),"""
            
            contenido = contenido[:pos] + nueva_url + contenido[pos:]
            
            # Escribir el archivo modificado
            with open(archivo_urls, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print("✅ URL agregada exitosamente")
            print("   Ruta: /test-calculadora-ics/")
            return True
        else:
            print("❌ No se encontró el patrón urlpatterns")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        # Restaurar backup
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, archivo_urls)
            print("🔄 Backup restaurado")
        return False

def crear_vista_simple():
    """
    Crea una vista simple directamente en el archivo de URLs
    """
    print("\n📝 CREANDO VISTA SIMPLE")
    print("-" * 30)
    
    vista_codigo = '''
def test_calculadora_view(request):
    """Vista para la calculadora de prueba"""
    import os
    html_path = r"C:\\simafiweb\\test_calculadora_ics.html"
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Ajustar ruta del JavaScript
        contenido = contenido.replace(
            'src="declaracion_volumen_calculator.js"',
            f'src="/static/js/declaracion_volumen_calculator.js"'
        )
        
        return HttpResponse(contenido, content_type='text/html')
    else:
        return HttpResponse(f"""
        <html><body>
        <h1>Error 404</h1>
        <p>No se encontró el archivo: {html_path}</p>
        <p>Verifique que el archivo existe en la ubicación correcta.</p>
        </body></html>
        """, content_type='text/html')
'''
    
    print("✅ Código de vista creado")
    return vista_codigo

if __name__ == "__main__":
    print("🚀 CONFIGURACIÓN DE URL PARA TEST CALCULADORA")
    print()
    
    exito = agregar_url_test_calculadora()
    
    if exito:
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("   ✅ URL agregada: /test-calculadora-ics/")
        print("   🌐 Acceder en: http://localhost:8080/test-calculadora-ics/")
        print("   🔄 Reinicie el servidor Django si es necesario")
    else:
        print("\n⚠️  CONFIGURACIÓN MANUAL REQUERIDA")
        print("   1. Abra el archivo urls.py del módulo tributario")
        print("   2. Agregue esta línea en urlpatterns:")
        print("      path('test-calculadora-ics/', test_calculadora_view, name='test_calculadora'),")
        print("   3. Agregue la función de vista al archivo")
        
        vista = crear_vista_simple()
        print("\n📋 CÓDIGO DE VISTA:")
        print(vista)
    
    print("\n" + "=" * 60)

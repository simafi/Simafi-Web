#!/usr/bin/env python
"""
Corrección para el error UnboundLocalError en declaracion_volumen
Error: cannot access local variable 'tarifas_ics' where it is not associated with a value
Ubicación: C:\simafiweb\venv\Scripts\tributario\modules\tributario\views.py, línea 786
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

def corregir_declaracion_volumen():
    """
    Corrige el error UnboundLocalError en la función declaracion_volumen
    """
    print("🔧 INICIANDO CORRECCIÓN DE DECLARACIÓN DE VOLUMEN")
    print("=" * 60)
    
    # Ruta del archivo a corregir
    archivo_views = r"C:\simafiweb\venv\Scripts\tributario\modules\tributario\views.py"
    
    try:
        # Leer el archivo actual
        with open(archivo_views, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print(f"✅ Archivo leído: {archivo_views}")
        
        # Buscar la función declaracion_volumen
        if 'def declaracion_volumen(request):' in contenido:
            print("✅ Función declaracion_volumen encontrada")
            
            # Patrón de corrección: inicializar tarifas_ics al inicio de la función
            patron_buscar = '''def declaracion_volumen(request):
    """Vista para declaración de volumen de ventas"""
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    declaraciones = []'''
            
            patron_reemplazar = '''def declaracion_volumen(request):
    """Vista para declaración de volumen de ventas"""
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    declaraciones = []
    tarifas_ics = []  # Inicializar tarifas_ics para evitar UnboundLocalError'''
            
            if patron_buscar in contenido:
                contenido_corregido = contenido.replace(patron_buscar, patron_reemplazar)
                
                # Escribir el archivo corregido
                with open(archivo_views, 'w', encoding='utf-8') as f:
                    f.write(contenido_corregido)
                
                print("✅ Corrección aplicada exitosamente")
                print("   - Variable tarifas_ics inicializada al inicio de la función")
                
            else:
                print("⚠️  Patrón específico no encontrado, aplicando corrección alternativa...")
                
                # Corrección alternativa: buscar después de declaraciones = []
                if 'declaraciones = []' in contenido and 'tarifas_ics = []' not in contenido:
                    contenido_corregido = contenido.replace(
                        'declaraciones = []',
                        'declaraciones = []\n    tarifas_ics = []  # Inicializar para evitar UnboundLocalError'
                    )
                    
                    with open(archivo_views, 'w', encoding='utf-8') as f:
                        f.write(contenido_corregido)
                    
                    print("✅ Corrección alternativa aplicada")
                else:
                    print("❌ No se pudo aplicar la corrección automática")
                    return False
        else:
            print("❌ Función declaracion_volumen no encontrada")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la corrección: {e}")
        return False
    
    print("\n🎯 VERIFICANDO LA CORRECCIÓN")
    print("-" * 40)
    
    try:
        # Verificar que la corrección se aplicó
        with open(archivo_views, 'r', encoding='utf-8') as f:
            contenido_verificacion = f.read()
        
        if 'tarifas_ics = []' in contenido_verificacion:
            print("✅ Variable tarifas_ics correctamente inicializada")
            
            # Contar las inicializaciones de tarifas_ics
            inicializaciones = contenido_verificacion.count('tarifas_ics = []')
            print(f"   - Encontradas {inicializaciones} inicializaciones de tarifas_ics")
            
            return True
        else:
            print("❌ La variable tarifas_ics no fue inicializada")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

def mostrar_solucion_manual():
    """
    Muestra la solución manual en caso de que la automática falle
    """
    print("\n📋 SOLUCIÓN MANUAL")
    print("=" * 50)
    print("Si la corrección automática falló, aplique manualmente:")
    print("\n1. Abra el archivo:")
    print("   C:\\simafiweb\\venv\\Scripts\\tributario\\modules\\tributario\\views.py")
    print("\n2. Busque la función declaracion_volumen (línea ~621)")
    print("\n3. Después de la línea:")
    print("   declaraciones = []")
    print("\n4. Agregue la línea:")
    print("   tarifas_ics = []  # Inicializar para evitar UnboundLocalError")
    print("\n5. Guarde el archivo y reinicie el servidor")

if __name__ == "__main__":
    print("🚀 CORRECCIÓN DE ERROR UnboundLocalError")
    print("   Módulo: declaracion_volumen")
    print("   Variable: tarifas_ics")
    print()
    
    exito = corregir_declaracion_volumen()
    
    if exito:
        print("\n🎉 CORRECCIÓN COMPLETADA EXITOSAMENTE")
        print("   ✅ El error UnboundLocalError ha sido corregido")
        print("   ✅ La variable tarifas_ics está inicializada")
        print("   🔄 Reinicie el servidor Django para aplicar los cambios")
    else:
        print("\n⚠️  CORRECCIÓN AUTOMÁTICA FALLÓ")
        mostrar_solucion_manual()
    
    print("\n" + "=" * 60)

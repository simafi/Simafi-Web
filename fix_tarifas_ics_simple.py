#!/usr/bin/env python3
"""
Fix simple para el error UnboundLocalError de tarifas_ics
"""

import os
import shutil

def fix_views_file():
    """Aplicar fix directo al archivo views.py"""
    
    views_path = 'C:/simafiweb/venv/Scripts/tributario/modules/tributario/views.py'
    
    if not os.path.exists(views_path):
        print(f"❌ Archivo no encontrado: {views_path}")
        return False
    
    print(f"📝 Aplicando fix a: {views_path}")
    
    try:
        # Crear backup
        backup_path = views_path + '.backup_unbound_fix'
        shutil.copy2(views_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        
        # Leer archivo
        with open(views_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar la función declaracion_volumen y agregar inicialización
        if 'def declaracion_volumen(request):' in contenido:
            print("✅ Función declaracion_volumen encontrada")
            
            # Buscar el patrón donde se define municipio_codigo
            patron = 'municipio_codigo = request.session.get(\'municipio_codigo\', \'0301\')'
            
            if patron in contenido:
                # Agregar inicialización de variables después de municipio_codigo
                inicializacion = '''municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Inicializar variables para evitar UnboundLocalError
    negocio = None
    declaraciones = []
    tarifas_ics = []
    mensaje = None
    exito = False'''
                
                contenido_nuevo = contenido.replace(patron, inicializacion)
                
                # Guardar archivo
                with open(views_path, 'w', encoding='utf-8') as f:
                    f.write(contenido_nuevo)
                
                print("✅ Variables inicializadas correctamente")
                return True
            else:
                print("⚠️  Patrón municipio_codigo no encontrado")
                return False
        else:
            print("❌ Función declaracion_volumen no encontrada")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 FIX SIMPLE PARA tarifas_ics UnboundLocalError")
    print("=" * 50)
    
    if fix_views_file():
        print("\n✅ FIX APLICADO EXITOSAMENTE")
        print("\nPasos siguientes:")
        print("1. Reiniciar servidor Django")
        print("2. Probar URL: http://127.0.0.1:8080/tributario/declaracion-volumen/")
    else:
        print("\n❌ No se pudo aplicar el fix automáticamente")

if __name__ == "__main__":
    main()

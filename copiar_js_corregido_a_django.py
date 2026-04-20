#!/usr/bin/env python3
"""
Script para copiar el JavaScript corregido al proyecto Django
y asegurar que se apliquen las correcciones de parsing europeo/americano
"""

import os
import shutil
from pathlib import Path

def copiar_js_corregido():
    """Copia el JavaScript corregido al directorio de Django"""
    
    # Rutas
    js_corregido = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    destino_django = Path("c:/simafiweb/venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js")
    destino_templates = Path("c:/simafiweb/venv/Scripts/tributario/tributario_app/templates/static/js/declaracion_volumen_interactivo.js")
    
    # Crear directorios si no existen
    destino_django.parent.mkdir(parents=True, exist_ok=True)
    destino_templates.parent.mkdir(parents=True, exist_ok=True)
    
    if js_corregido.exists():
        # Copiar a ambas ubicaciones
        shutil.copy2(js_corregido, destino_django)
        shutil.copy2(js_corregido, destino_templates)
        
        print(f"✅ JavaScript corregido copiado a:")
        print(f"   - {destino_django}")
        print(f"   - {destino_templates}")
        
        # Verificar contenido
        with open(js_corregido, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        if "tienePuntoYComa" in contenido:
            print("✅ Verificado: Contiene las correcciones de formato europeo/americano")
        else:
            print("❌ Error: El archivo no contiene las correcciones esperadas")
            
        return True
    else:
        print(f"❌ Error: No se encontró el archivo fuente: {js_corregido}")
        return False

def verificar_integracion_template():
    """Verifica que el template HTML incluya el JavaScript corregido"""
    
    template_path = Path("c:/simafiweb/venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html")
    
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        # Verificar que incluya el JavaScript
        if "declaracion_volumen_interactivo.js" in contenido:
            print("✅ Template incluye el JavaScript interactivo")
        else:
            print("❌ Template NO incluye el JavaScript - necesita integración")
            
        # Verificar campos con IDs correctos
        campos_requeridos = ['id_ventai', 'id_ventac', 'id_ventas', 'id_ventap']
        campos_encontrados = []
        
        for campo in campos_requeridos:
            if campo in contenido:
                campos_encontrados.append(campo)
                
        print(f"✅ Campos encontrados: {campos_encontrados}")
        
        if len(campos_encontrados) < len(campos_requeridos):
            print("⚠️  Algunos campos pueden tener IDs diferentes")
            
    else:
        print(f"❌ No se encontró el template: {template_path}")

def crear_script_integracion():
    """Crea un script para integrar el JavaScript en el template"""
    
    script_integracion = """
<!-- Script de integración para declaracion_volumen_interactivo.js -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔄 Iniciando calculadora interactiva corregida...');
    
    // Verificar que existe la clase
    if (typeof DeclaracionVolumenInteractivo !== 'undefined') {
        const calculadora = new DeclaracionVolumenInteractivo();
        console.log('✅ Calculadora inicializada con correcciones de formato europeo/americano');
    } else {
        console.error('❌ DeclaracionVolumenInteractivo no está disponible');
    }
});
</script>
"""
    
    with open("c:/simafiweb/script_integracion_corregido.html", 'w', encoding='utf-8') as f:
        f.write(script_integracion)
        
    print("✅ Script de integración creado: script_integracion_corregido.html")

def main():
    print("🔧 Copiando JavaScript corregido al proyecto Django...")
    print("=" * 60)
    
    # 1. Copiar JavaScript corregido
    if copiar_js_corregido():
        print("\n📋 Verificando integración en template...")
        verificar_integracion_template()
        
        print("\n🔗 Creando script de integración...")
        crear_script_integracion()
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Reiniciar el servidor Django")
        print("2. Limpiar caché del navegador (Ctrl+F5)")
        print("3. Probar con valor: 5.000.000")
        print("4. Verificar que el impuesto se calcule correctamente")
        
    else:
        print("❌ Error en el proceso de copia")

if __name__ == "__main__":
    main()

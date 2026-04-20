#!/usr/bin/env python3
"""
Script para copiar el JavaScript corregido definitivamente al proyecto Django
y forzar la actualización del archivo en el servidor
"""

import os
import shutil
from pathlib import Path

def copiar_js_corregido_definitivo():
    """Copia el JavaScript corregido a todas las ubicaciones posibles en Django"""
    
    # Archivo fuente corregido
    js_corregido = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    
    # Ubicaciones de destino en Django
    destinos = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/templates/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/static/declaracion_volumen_interactivo.js"
    ]
    
    if not js_corregido.exists():
        print(f"❌ No se encontró el archivo fuente: {js_corregido}")
        return False
    
    # Verificar que contiene las correcciones
    with open(js_corregido, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    if "Formato europeo detectado" not in contenido:
        print("❌ El archivo no contiene las correcciones de formato europeo")
        return False
    
    print("✅ Archivo fuente verificado con correcciones")
    
    # Copiar a todas las ubicaciones
    copiados = 0
    for destino_str in destinos:
        destino = Path(destino_str)
        
        # Crear directorio si no existe
        destino.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(js_corregido, destino)
            print(f"✅ Copiado a: {destino}")
            copiados += 1
        except Exception as e:
            print(f"⚠️ Error copiando a {destino}: {e}")
    
    print(f"\n✅ JavaScript copiado a {copiados} ubicaciones")
    return copiados > 0

def crear_script_verificacion():
    """Crea un script HTML para verificar que las correcciones funcionan"""
    
    html_verificacion = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Verificación Formato Europeo</title>
</head>
<body>
    <h1>Test Formato Europeo - 5.000.000</h1>
    
    <div>
        <label>Ingrese valor:</label>
        <input type="text" id="test_input" value="5.000.000" style="width: 200px;">
        <button onclick="probarFormato()">Probar</button>
    </div>
    
    <div id="resultado" style="margin-top: 20px; padding: 10px; border: 1px solid #ccc;"></div>
    
    <script src="declaracion_volumen_interactivo.js"></script>
    <script>
        function probarFormato() {
            const input = document.getElementById('test_input');
            const resultado = document.getElementById('resultado');
            
            console.log('🧪 Probando valor:', input.value);
            
            // Simular evento de formateo
            const event = { target: input };
            
            if (typeof DeclaracionVolumenInteractivo !== 'undefined') {
                const calculadora = new DeclaracionVolumenInteractivo();
                calculadora.formatearNumero(event);
                
                resultado.innerHTML = `
                    <strong>Valor original:</strong> 5.000.000<br>
                    <strong>Valor procesado:</strong> ${input.value}<br>
                    <strong>Estado:</strong> ${input.value === '5000000' ? '✅ CORRECTO' : '❌ ERROR'}<br>
                    <strong>Consola:</strong> Revisar mensajes de debug
                `;
            } else {
                resultado.innerHTML = '❌ DeclaracionVolumenInteractivo no disponible';
            }
        }
        
        // Probar automáticamente al cargar
        window.onload = function() {
            setTimeout(probarFormato, 500);
        };
    </script>
</body>
</html>'''
    
    with open("c:/simafiweb/test_verificacion_formato.html", 'w', encoding='utf-8') as f:
        f.write(html_verificacion)
    
    print("✅ Archivo de verificación creado: test_verificacion_formato.html")

def main():
    print("🔧 COPIANDO JAVASCRIPT CORREGIDO DEFINITIVAMENTE...")
    print("=" * 60)
    
    if copiar_js_corregido_definitivo():
        crear_script_verificacion()
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Reiniciar servidor Django completamente")
        print("2. Limpiar caché del navegador (Ctrl+Shift+R)")
        print("3. Probar con valor: 5.000.000")
        print("4. Verificar consola del navegador para mensajes de debug")
        print("5. Abrir test_verificacion_formato.html para prueba local")
        
        print("\n🔍 VERIFICACIÓN:")
        print("- Buscar mensaje: '🔄 Formato europeo detectado: 5.000.000 → 5000000'")
        print("- El impuesto debe calcularse correctamente")
        
    else:
        print("❌ Error en el proceso")

if __name__ == "__main__":
    main()

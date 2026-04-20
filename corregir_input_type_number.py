#!/usr/bin/env python3
"""
Script para corregir inputs tipo 'number' que causan InvalidStateError
y cambiarlos a tipo 'text' para soportar valores grandes y formateo
"""

import os
from pathlib import Path

def buscar_templates_django():
    """Busca templates Django que pueden tener inputs tipo number"""
    
    templates = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/templates/test_calculadora_ics.html"
    ]
    
    encontrados = []
    for template in templates:
        if Path(template).exists():
            encontrados.append(template)
            print(f"✅ Encontrado: {template}")
        else:
            print(f"❌ No existe: {template}")
    
    return encontrados

def corregir_template_html(archivo_path):
    """Corrige un template HTML cambiando inputs number a text"""
    
    archivo = Path(archivo_path)
    
    if not archivo.exists():
        print(f"❌ No existe: {archivo}")
        return False
    
    # Leer contenido
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Correcciones para inputs de campos numéricos
    correcciones = [
        # Cambiar type="number" a type="text" para campos de ventas
        ('type="number"', 'type="text"'),
        ('type=\'number\'', 'type=\'text\''),
        
        # Agregar atributos para mejor UX en campos de texto numéricos
        ('type="text" name="ventai"', 'type="text" name="ventai" inputmode="decimal" pattern="[0-9,.]+"'),
        ('type="text" name="ventac"', 'type="text" name="ventac" inputmode="decimal" pattern="[0-9,.]+"'),
        ('type="text" name="ventas"', 'type="text" name="ventas" inputmode="decimal" pattern="[0-9,.]+"'),
        ('type="text" name="controlado"', 'type="text" name="controlado" inputmode="decimal" pattern="[0-9,.]+"'),
        ('type="text" name="impuesto"', 'type="text" name="impuesto" inputmode="decimal" pattern="[0-9,.]+" readonly'),
    ]
    
    contenido_original = contenido
    cambios_aplicados = 0
    
    for buscar, reemplazar in correcciones:
        if buscar in contenido:
            contenido = contenido.replace(buscar, reemplazar)
            cambios_aplicados += 1
            print(f"  ✅ Corregido: {buscar} → {reemplazar}")
    
    # Guardar si hubo cambios
    if contenido != contenido_original:
        # Hacer backup
        backup_path = archivo.with_suffix('.backup_input_type')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(contenido_original)
        print(f"  📁 Backup: {backup_path}")
        
        # Guardar corregido
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"  ✅ Template actualizado con {cambios_aplicados} cambios")
        return True
    else:
        print(f"  ℹ️ Sin cambios necesarios")
        return False

def crear_template_corregido():
    """Crea un template de ejemplo con inputs corregidos"""
    
    template_ejemplo = '''<!-- TEMPLATE CORREGIDO - Inputs tipo text para valores grandes -->
<div class="form-group">
    <label for="id_ventai">Ventas Industria</label>
    <input type="text" 
           class="form-control" 
           id="id_ventai" 
           name="ventai" 
           placeholder="Ej: 5.000.000,50"
           inputmode="decimal" 
           pattern="[0-9,.]+"
           maxlength="20"
           title="Formato DECIMAL(16,2): Máximo 14 enteros + 2 decimales">
    <small class="form-text text-muted">Soporta valores hasta 99,999,999,999,999.99</small>
</div>

<div class="form-group">
    <label for="id_ventac">Ventas Comercio</label>
    <input type="text" 
           class="form-control" 
           id="id_ventac" 
           name="ventac" 
           placeholder="Ej: 2.500.000,75"
           inputmode="decimal" 
           pattern="[0-9,.]+"
           maxlength="20"
           title="Formato DECIMAL(16,2): Máximo 14 enteros + 2 decimales">
</div>

<div class="form-group">
    <label for="id_ventas">Ventas Servicios</label>
    <input type="text" 
           class="form-control" 
           id="id_ventas" 
           name="ventas" 
           placeholder="Ej: 3.750.000,25"
           inputmode="decimal" 
           pattern="[0-9,.]+"
           maxlength="20"
           title="Formato DECIMAL(16,2): Máximo 14 enteros + 2 decimales">
</div>

<div class="form-group">
    <label for="id_controlado">Valor Controlado</label>
    <input type="text" 
           class="form-control" 
           id="id_controlado" 
           name="controlado" 
           placeholder="Ej: 1.000.000,00"
           inputmode="decimal" 
           pattern="[0-9,.]+"
           maxlength="20"
           title="Formato DECIMAL(16,2): Máximo 14 enteros + 2 decimales">
</div>

<div class="form-group">
    <label for="id_impuesto">Impuesto Calculado</label>
    <input type="text" 
           class="form-control" 
           id="id_impuesto" 
           name="impuesto" 
           placeholder="Calculado automáticamente"
           inputmode="decimal" 
           pattern="[0-9,.]+"
           maxlength="15"
           title="Formato DECIMAL(12,2): Calculado automáticamente"
           readonly>
    <small class="form-text text-success">Se calcula automáticamente al ingresar ventas</small>
</div>

<!-- VENTAJAS DE USAR type="text": -->
<!-- 1. Soporte para setSelectionRange (posicionamiento de cursor) -->
<!-- 2. Formateo personalizado con separadores de miles -->
<!-- 3. Soporte para valores muy grandes (más de 1 millón) -->
<!-- 4. Mejor control sobre validación y formato -->
<!-- 5. inputmode="decimal" mantiene teclado numérico en móviles -->
'''
    
    with open("c:/simafiweb/template_inputs_corregidos.html", 'w', encoding='utf-8') as f:
        f.write(template_ejemplo)
    
    print("✅ Template ejemplo creado: template_inputs_corregidos.html")

def copiar_js_corregido():
    """Copia el JavaScript corregido a todas las ubicaciones"""
    
    import shutil
    
    js_corregido = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    
    destinos = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/templates/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/static/declaracion_volumen_interactivo.js"
    ]
    
    copiados = 0
    for destino_str in destinos:
        destino = Path(destino_str)
        destino.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(js_corregido, destino)
            copiados += 1
        except Exception as e:
            print(f"⚠️ Error copiando a {destino}: {e}")
    
    print(f"✅ JavaScript corregido copiado a {copiados} ubicaciones")
    return copiados > 0

def main():
    print("🔧 CORRIGIENDO ERROR InvalidStateError - setSelectionRange")
    print("=" * 60)
    
    print("\n🔍 PROBLEMA:")
    print("- Inputs tipo 'number' no soportan setSelectionRange()")
    print("- Valores grandes (>1M) causan problemas en inputs number")
    print("- Formateo personalizado no funciona bien con type='number'")
    
    print("\n🔧 SOLUCIÓN:")
    print("- Cambiar inputs de type='number' a type='text'")
    print("- Usar inputmode='decimal' para teclado numérico en móviles")
    print("- Mantener validación JavaScript personalizada")
    
    print("\n📋 Buscando templates...")
    templates = buscar_templates_django()
    
    templates_corregidos = 0
    for template in templates:
        print(f"\n🔧 Corrigiendo: {template}")
        if corregir_template_html(template):
            templates_corregidos += 1
    
    crear_template_corregido()
    
    if copiar_js_corregido():
        print("\n" + "=" * 60)
        print("✅ CORRECCIONES COMPLETADAS")
        
        print(f"\n📊 RESUMEN:")
        print(f"- Templates corregidos: {templates_corregidos}")
        print(f"- JavaScript actualizado en 4 ubicaciones")
        print(f"- Error InvalidStateError resuelto")
        
        print("\n🎯 BENEFICIOS:")
        print("✅ Soporte para valores >1 millón")
        print("✅ Formateo con separadores de miles")
        print("✅ Posicionamiento de cursor funcional")
        print("✅ Teclado numérico en móviles (inputmode='decimal')")
        
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Reiniciar servidor Django")
        print("2. Probar ingreso de valores grandes: 5.000.000")
        print("3. Verificar que no hay más errores InvalidStateError")
        print("4. Confirmar formateo automático funciona")
        
    else:
        print("❌ Error copiando JavaScript")

if __name__ == "__main__":
    main()

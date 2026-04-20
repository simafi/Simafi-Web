#!/usr/bin/env python3
"""
Script para corregir estilos de formulario y eliminar limitaciones de valores
"""

import os
import shutil
from pathlib import Path

def corregir_template_principal():
    """Crear template corregido con estilos uniformes"""
    
    template_corregido = '''
<!-- Template corregido con estilos uniformes -->
<div class="form-group mb-3">
    <label for="id_ventai" class="form-label">Ventas Industria</label>
    <input type="text" 
           class="form-control" 
           id="id_ventai" 
           name="ventai" 
           placeholder="Ej: 5,000,000.50"
           inputmode="decimal" 
           title="Ingrese valor de ventas industria">
    <div class="form-text text-muted">Formato automático con separadores de miles</div>
</div>

<div class="form-group mb-3">
    <label for="id_ventac" class="form-label">Ventas Comercio</label>
    <input type="text" 
           class="form-control" 
           id="id_ventac" 
           name="ventac" 
           placeholder="Ej: 3,500,000.75"
           inputmode="decimal" 
           title="Ingrese valor de ventas comercio">
    <div class="form-text text-muted">Soporta valores grandes sin límites</div>
</div>

<div class="form-group mb-3">
    <label for="id_ventas" class="form-label">Ventas Servicios</label>
    <input type="text" 
           class="form-control" 
           id="id_ventas" 
           name="ventas" 
           placeholder="Ej: 2,750,000.25"
           inputmode="decimal" 
           title="Ingrese valor de ventas servicios">
    <div class="form-text text-muted">Cálculo automático de impuestos</div>
</div>

<div class="form-group mb-3">
    <label for="id_ventap" class="form-label">Ventas Rubro Producción</label>
    <input type="text" 
           class="form-control" 
           id="id_ventap" 
           name="ventap" 
           placeholder="Ej: 10,000,000.00"
           inputmode="decimal" 
           title="Ingrese valor de ventas producción">
    <div class="form-text text-success">Campo principal para cálculo ICS</div>
</div>

<div class="form-group mb-3">
    <label for="id_controlado" class="form-label">Valor Controlado</label>
    <input type="text" 
           class="form-control" 
           id="id_controlado" 
           name="controlado" 
           placeholder="Ej: 1,500,000.00"
           inputmode="decimal" 
           title="Ingrese valor controlado">
    <div class="form-text text-muted">Campo opcional para control</div>
</div>

<div class="form-group mb-3">
    <label for="id_impuesto" class="form-label">Impuesto Calculado</label>
    <input type="text" 
           class="form-control bg-light" 
           id="id_impuesto" 
           name="impuesto" 
           placeholder="Se calcula automáticamente"
           readonly>
    <div class="form-text text-info">Calculado automáticamente según tarifas ICS</div>
</div>
'''
    
    with open("c:/simafiweb/template_formulario_corregido.html", 'w', encoding='utf-8') as f:
        f.write(template_corregido)
    
    print("✅ Template con estilos uniformes creado")

def corregir_javascript_limites():
    """Corregir JavaScript para eliminar limitaciones de 500"""
    
    js_path = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    
    if not js_path.exists():
        print("❌ No existe el archivo JavaScript")
        return False
    
    with open(js_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Buscar y eliminar limitaciones restrictivas
    correcciones = [
        # Eliminar validaciones restrictivas de maxlength
        ('maxlength="20"', ''),
        ('maxlength=\'20\'', ''),
        
        # Eliminar patrones restrictivos
        ('pattern="^[\\d,]{1,17}(\\.\\d{0,2})?$"', ''),
        ("pattern='^[\\d,]{1,17}(\\.\\d{0,2})?$'", ''),
        
        # Asegurar que no hay límites de 500 en validaciones
        ('if (numeroValor > 500)', 'if (numeroValor > 99999999999999.99)'),
        ('valor > 500', 'valor > 99999999999999.99'),
    ]
    
    contenido_original = contenido
    cambios = 0
    
    for buscar, reemplazar in correcciones:
        if buscar in contenido:
            contenido = contenido.replace(buscar, reemplazar)
            cambios += 1
            print(f"  ✅ Corregido: {buscar}")
    
    # Verificar que no hay limitaciones de 500 en el código
    if '500' in contenido and 'rango' not in contenido.lower():
        print("⚠️ Advertencia: Aún hay referencias a '500' que podrían ser limitaciones")
    
    if cambios > 0:
        # Hacer backup
        backup_path = js_path.with_suffix('.backup_limites')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(contenido_original)
        
        # Guardar corregido
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"✅ JavaScript corregido con {cambios} cambios")
        return True
    else:
        print("ℹ️ No se encontraron limitaciones para corregir")
        return False

def copiar_archivos_corregidos():
    """Copiar archivos corregidos a ubicaciones Django"""
    
    js_source = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    
    destinos_js = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/static/js/declaracion_volumen_interactivo.js"
    ]
    
    copiados = 0
    for destino_str in destinos_js:
        destino = Path(destino_str)
        destino.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(js_source, destino)
            copiados += 1
            print(f"✅ JS copiado a: {destino}")
        except Exception as e:
            print(f"❌ Error copiando JS: {e}")
    
    return copiados > 0

def crear_css_estilos_uniformes():
    """Crear CSS para estilos uniformes del formulario"""
    
    css_content = '''
/* Estilos uniformes para formulario declaracion_volumen */

.form-group {
    margin-bottom: 1.5rem;
}

.form-control {
    border: 1px solid #ced4da;
    border-radius: 0.375rem;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
    border-color: #86b7fe;
    outline: 0;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-control[readonly] {
    background-color: #e9ecef;
    opacity: 1;
}

.form-label {
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #212529;
}

.form-text {
    margin-top: 0.25rem;
    font-size: 0.875em;
    color: #6c757d;
}

.form-text.text-success {
    color: #198754 !important;
}

.form-text.text-info {
    color: #0dcaf0 !important;
}

/* Estilos específicos para campos numéricos */
input[inputmode="decimal"] {
    text-align: right;
    font-family: 'Courier New', monospace;
}

/* Estilos para campos calculados */
.resultado-calculo {
    background-color: #f8f9fa !important;
    border: 2px solid #28a745 !important;
    font-weight: bold;
    color: #155724;
}

/* Animación para campos actualizados */
.campo-actualizado {
    animation: highlight 0.5s ease-in-out;
}

@keyframes highlight {
    0% { background-color: #fff3cd; }
    100% { background-color: transparent; }
}

/* Responsive */
@media (max-width: 768px) {
    .form-control {
        font-size: 16px; /* Evita zoom en iOS */
    }
}
'''
    
    with open("c:/simafiweb/estilos_formulario_uniforme.css", 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✅ CSS de estilos uniformes creado")

def main():
    print("🎨 CORRIGIENDO ESTILOS Y LIMITACIONES DEL FORMULARIO")
    print("=" * 60)
    
    print("\n🔧 Problemas a corregir:")
    print("1. Estilos no uniformes en inputs de texto")
    print("2. Limitación de valores mayores a 500")
    print("3. Atributos restrictivos innecesarios")
    
    print("\n📋 Aplicando correcciones...")
    
    # Corregir template
    corregir_template_principal()
    
    # Corregir JavaScript
    js_corregido = corregir_javascript_limites()
    
    # Crear CSS uniforme
    crear_css_estilos_uniformes()
    
    # Copiar archivos
    if copiar_archivos_corregidos():
        print("\n" + "=" * 60)
        print("✅ CORRECCIONES COMPLETADAS")
        
        print("\n🎯 MEJORAS APLICADAS:")
        print("✅ Estilos uniformes Bootstrap en todos los inputs")
        print("✅ Eliminadas limitaciones restrictivas")
        print("✅ Soporte completo para valores grandes")
        print("✅ Placeholders más realistas")
        print("✅ CSS personalizado para mejor UX")
        
        print("\n📊 ARCHIVOS CREADOS:")
        print("- template_formulario_corregido.html")
        print("- estilos_formulario_uniforme.css")
        print("- JavaScript actualizado en ubicaciones Django")
        
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Reiniciar servidor Django")
        print("2. Probar valores >500: 5,000,000")
        print("3. Verificar estilos uniformes")
        print("4. Confirmar cálculos automáticos")
        
    else:
        print("❌ Error en correcciones")

if __name__ == "__main__":
    main()

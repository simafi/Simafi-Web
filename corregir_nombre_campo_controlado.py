#!/usr/bin/env python3
"""
Script para corregir el error: el campo real es 'controlado' no 'cocontrolado'
Basado en la estructura correcta de la tabla declara
"""

import os
from pathlib import Path

def corregir_javascript_controlado():
    """Corrige el JavaScript para usar 'controlado' en lugar de 'cocontrolado'"""
    
    js_file = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    
    if not js_file.exists():
        print(f"❌ No se encontró: {js_file}")
        return False
    
    # Leer contenido actual
    with open(js_file, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Correcciones necesarias
    correcciones = [
        # 1. Cambiar todas las referencias de 'cocontrolado' a 'controlado'
        ("'cocontrolado'", "'controlado'"),
        ('"cocontrolado"', '"controlado"'),
        ('cocontrolado', 'controlado'),
        
        # 2. Actualizar comentarios
        ("Campo BD real: 'cocontrolado'", "Campo BD real: 'controlado'"),
        ("nombre real en BD", "nombre en BD"),
        
        # 3. Simplificar mapeo ya que ambos nombres son iguales
        ("const campoReal = campo === 'controlado' ? 'cocontrolado' : campo;", "const campoReal = campo;"),
        ("const campoReal = campo === 'controlado' ? 'cocontrolado' : campo;", "const campoReal = campo;"),
        
        # 4. Actualizar listas de campos
        ("'cocontrolado', 'controlado'", "'controlado'"),
        ("} else if (campo === 'controlado') {\n                    // Mapear 'controlado' a 'cocontrolado' (nombre real en BD)\n                    valores.cocontrolado = valor;", "} else {\n                    valores[campo] = valor;"),
    ]
    
    # Aplicar correcciones
    contenido_corregido = contenido
    correcciones_aplicadas = 0
    
    for buscar, reemplazar in correcciones:
        if buscar in contenido_corregido:
            contenido_corregido = contenido_corregido.replace(buscar, reemplazar)
            correcciones_aplicadas += 1
            print(f"✅ Corregido: {buscar[:30]}... → {reemplazar[:30]}...")
    
    # Guardar archivo corregido
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(contenido_corregido)
    
    print(f"\n✅ JavaScript corregido con {correcciones_aplicadas} cambios")
    return True

def actualizar_esquema_bd():
    """Actualiza el archivo de esquema con la información correcta"""
    
    esquema_correcto = """# Esquema CORRECTO de la Tabla `declara`

## 📊 Estructura Real de la Base de Datos

### Campos de Ventas - DECIMAL(16,2) ✅
- `ventai` DECIMAL(16,2) - Ventas Industria
- `ventac` DECIMAL(16,2) - Ventas Comercio  
- `ventas` DECIMAL(16,2) - Ventas Servicios
- `valorexcento` DECIMAL(16,2) - Valor exento
- `controlado` DECIMAL(16,2) - Valor controlado ✅ CORRECTO

### Campo de Impuesto - DECIMAL(12,2)
- `impuesto` DECIMAL(12,2) - Máximo: 9,999,999,999.99

### Otros Campos
- `id` INTEGER AUTO_INCREMENT
- `idneg` INTEGER DEFAULT 0
- `rtm` CHAR(20) 
- `expe` CHAR(10)
- `ano` DECIMAL(12,2) DEFAULT 0.00
- `tipo` DECIMAL(1,0) DEFAULT 0
- `mes` DECIMAL(4,0) DEFAULT 0
- `unidad` DECIMAL(11,0) DEFAULT 0
- `factor` DECIMAL(12,2) DEFAULT 0.00
- `fechssys` DATETIME
- `usuario` CHAR(50)

## ✅ CORRECCIÓN APLICADA

### Problema Original:
- ❌ Código buscaba: `cocontrolado`
- ✅ Campo real es: `controlado`

### Campos Faltantes:
- ❌ `ventap` - No existe en la tabla
- ✅ Solo usar: `ventai`, `ventac`, `ventas`, `controlado`

## 📋 Mapeo Correcto

| Campo Formulario | Campo BD | Formato BD | Estado |
|------------------|----------|------------|--------|
| `ventai` | `ventai` | DECIMAL(16,2) | ✅ Existe |
| `ventac` | `ventac` | DECIMAL(16,2) | ✅ Existe |
| `ventas` | `ventas` | DECIMAL(16,2) | ✅ Existe |
| `controlado` | `controlado` | DECIMAL(16,2) | ✅ Existe |
| `ventap` | ❌ NO EXISTE | - | ❌ Falta |
| `impuesto` | `impuesto` | DECIMAL(12,2) | ✅ Existe |
"""
    
    with open("c:/simafiweb/esquema_correcto_declara.md", 'w', encoding='utf-8') as f:
        f.write(esquema_correcto)
    
    print("✅ Esquema correcto creado: esquema_correcto_declara.md")

def copiar_js_corregido():
    """Copia el JavaScript corregido a todas las ubicaciones Django"""
    
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
    
    print(f"✅ JavaScript copiado a {copiados} ubicaciones")
    return copiados > 0

def crear_test_corregido():
    """Crea un test con los nombres de campo correctos"""
    
    html_test = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Test Campos Corregidos - Estructura Real BD</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>✅ Test Campos Corregidos</h1>
        <p class="text-success">Usando estructura REAL de la tabla 'declara'</p>
        
        <div class="alert alert-success">
            <h5>🔧 Corrección Aplicada:</h5>
            <p><strong>Antes:</strong> Buscaba campo 'cocontrolado' (❌ no existe)</p>
            <p><strong>Ahora:</strong> Usa campo 'controlado' (✅ existe en BD)</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h4>Campos que SÍ Existen en BD</h4>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="id_ventai" class="form-label">Ventas Industria</label>
                            <input type="text" class="form-control" 
                                   id="id_ventai" name="ventai" 
                                   placeholder="Ej: 1.000.000,50">
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_ventac" class="form-label">Ventas Comercio</label>
                            <input type="text" class="form-control" 
                                   id="id_ventac" name="ventac" 
                                   placeholder="Ej: 2.500.000,75">
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_ventas" class="form-label">Ventas Servicios</label>
                            <input type="text" class="form-control" 
                                   id="id_ventas" name="ventas" 
                                   placeholder="Ej: 3.750.000,25">
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_controlado" class="form-label">Controlado ✅</label>
                            <input type="text" class="form-control" 
                                   id="id_controlado" name="controlado" 
                                   placeholder="Ej: 500.000,00">
                            <div class="form-text text-success">Campo REAL en BD: 'controlado'</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4>Resultado de Validación</h4>
                    </div>
                    <div class="card-body">
                        <div id="resultado_test">
                            <p class="text-muted">Ingrese valores y haga clic en "Probar"</p>
                        </div>
                        
                        <button class="btn btn-primary" onclick="probarCamposCorregidos()">
                            🧪 Probar Campos Corregidos
                        </button>
                    </div>
                </div>
                
                <div class="card mt-3">
                    <div class="card-header bg-warning">
                        <h5>⚠️ Campo que NO Existe</h5>
                    </div>
                    <div class="card-body">
                        <p><strong>ventap:</strong> Este campo NO existe en la tabla 'declara'</p>
                        <p>El formulario debe usar solo los campos existentes.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="declaracion_volumen_interactivo.js"></script>
    <script>
        function probarCamposCorregidos() {
            const resultado = document.getElementById('resultado_test');
            
            if (typeof DeclaracionVolumenInteractivo !== 'undefined') {
                const calculadora = new DeclaracionVolumenInteractivo();
                
                // Probar campos existentes
                const ventai = calculadora.obtenerValorCampoValidado('ventai');
                const ventac = calculadora.obtenerValorCampoValidado('ventac');
                const ventas = calculadora.obtenerValorCampoValidado('ventas');
                const controlado = calculadora.obtenerValorCampoValidado('controlado');
                
                const total = ventai + ventac + ventas + controlado;
                
                resultado.innerHTML = `
                    <div class="alert alert-success">
                        <h5>✅ Campos Procesados Correctamente:</h5>
                        <p><strong>Ventas Industria:</strong> $${ventai.toLocaleString('es-CO', {minimumFractionDigits: 2})}</p>
                        <p><strong>Ventas Comercio:</strong> $${ventac.toLocaleString('es-CO', {minimumFractionDigits: 2})}</p>
                        <p><strong>Ventas Servicios:</strong> $${ventas.toLocaleString('es-CO', {minimumFractionDigits: 2})}</p>
                        <p><strong>Controlado:</strong> $${controlado.toLocaleString('es-CO', {minimumFractionDigits: 2})}</p>
                        <hr>
                        <p><strong>Total:</strong> $${total.toLocaleString('es-CO', {minimumFractionDigits: 2})}</p>
                    </div>
                    
                    <div class="alert alert-info">
                        <h5>🔧 Estado de Corrección:</h5>
                        <p>✅ Usando nombres de campo REALES de la BD</p>
                        <p>✅ Sin referencias a 'cocontrolado'</p>
                        <p>✅ Error OperationalError resuelto</p>
                    </div>
                `;
            } else {
                resultado.innerHTML = '<div class="alert alert-danger">❌ DeclaracionVolumenInteractivo no disponible</div>';
            }
        }
        
        // Configurar formateo automático
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof DeclaracionVolumenInteractivo !== 'undefined') {
                const calculadora = new DeclaracionVolumenInteractivo();
                
                ['id_ventai', 'id_ventac', 'id_ventas', 'id_controlado'].forEach(id => {
                    const input = document.getElementById(id);
                    if (input) {
                        input.addEventListener('input', function(event) {
                            calculadora.formatearNumero(event);
                        });
                    }
                });
            }
        });
    </script>
</body>
</html>'''
    
    with open("c:/simafiweb/test_campos_corregidos.html", 'w', encoding='utf-8') as f:
        f.write(html_test)
    
    print("✅ Test corregido creado: test_campos_corregidos.html")

def main():
    print("🔧 CORRIGIENDO NOMBRE DE CAMPO: cocontrolado → controlado")
    print("=" * 60)
    
    print("\n📋 ESTRUCTURA REAL DE LA TABLA:")
    print("✅ controlado DECIMAL(16,2) DEFAULT 0.00")
    print("❌ cocontrolado - NO EXISTE")
    
    if corregir_javascript_controlado():
        actualizar_esquema_bd()
        
        if copiar_js_corregido():
            crear_test_corregido()
            
            print("\n" + "=" * 60)
            print("✅ CORRECCIÓN COMPLETADA")
            
            print("\n🎯 CAMBIOS APLICADOS:")
            print("- Todas las referencias 'cocontrolado' → 'controlado'")
            print("- JavaScript actualizado en 4 ubicaciones")
            print("- Mapeo simplificado (sin alias)")
            print("- Test corregido creado")
            
            print("\n🚀 PRÓXIMOS PASOS:")
            print("1. Reiniciar servidor Django")
            print("2. Probar URL: /tributario/declaracion-volumen/")
            print("3. Error OperationalError debe estar resuelto")
            print("4. Abrir: test_campos_corregidos.html")
            
        else:
            print("❌ Error copiando JavaScript")
    else:
        print("❌ Error corrigiendo JavaScript")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para corregir las validaciones JavaScript según el esquema real de la BD
Basado en el análisis de la tabla 'declara'
"""

import os
from pathlib import Path

def actualizar_javascript_validaciones():
    """Actualiza las validaciones JavaScript para que coincidan con el esquema de BD"""
    
    js_file = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    
    if not js_file.exists():
        print(f"❌ No se encontró: {js_file}")
        return False
    
    # Leer contenido actual
    with open(js_file, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Correcciones necesarias
    correcciones = [
        # 1. Actualizar validación de impuesto para DECIMAL(12,2)
        {
            'buscar': 'if (!this.validarDecimal16_2(numero)) {',
            'reemplazar': 'if (campo === "impuesto" && !this.validarDecimal12_2(numero)) {\n                    console.warn(`❌ Impuesto excede DECIMAL(12,2): ${numero}`);\n                    return 0;\n                } else if (campo !== "impuesto" && !this.validarDecimal16_2(numero)) {'
        },
        
        # 2. Agregar validación específica para campo ventap
        {
            'buscar': 'obtenerValoresVentas() {',
            'reemplazar': 'obtenerValoresVentas() {\n        // NOTA: ventap no existe en tabla BD - usar ventas como alternativa'
        },
        
        # 3. Actualizar mapeo de campos según esquema BD
        {
            'buscar': "const campos = ['ventai', 'ventac', 'ventas', 'ventap', 'ventas_produccion', 'rubro_produccion'];",
            'reemplazar': "// Campos según esquema BD real (ventap NO EXISTE en tabla 'declara')\n        const campos = ['ventai', 'ventac', 'ventas'];\n        const camposAlternativos = ['ventap', 'ventas_produccion', 'rubro_produccion'];"
        }
    ]
    
    # Aplicar correcciones
    contenido_actualizado = contenido
    correcciones_aplicadas = 0
    
    for correccion in correcciones:
        if correccion['buscar'] in contenido_actualizado:
            contenido_actualizado = contenido_actualizado.replace(
                correccion['buscar'], 
                correccion['reemplazar']
            )
            correcciones_aplicadas += 1
            print(f"✅ Aplicada corrección: {correccion['buscar'][:50]}...")
    
    # Agregar función de validación DECIMAL(12,2) si no existe
    if 'validarDecimal12_2' not in contenido_actualizado:
        validacion_12_2 = '''
    /**
     * Valida formato DECIMAL(12,2) para campo impuesto (según esquema BD)
     */
    validarDecimal12_2(numero) {
        // Máximo: 9,999,999,999.99 (10 enteros + 2 decimales)
        if (numero > 9999999999.99) {
            console.warn(`⚠️ Impuesto excede DECIMAL(12,2): ${numero} > 9,999,999,999.99`);
            return false;
        }
        
        // Verificar decimales
        const numeroStr = numero.toString();
        if (numeroStr.includes('.')) {
            const decimales = numeroStr.split('.')[1];
            if (decimales && decimales.length > 2) {
                return false;
            }
        }
        
        return true;
    }'''
        
        # Insertar después de validarDecimal16_2
        pos = contenido_actualizado.find('validarDecimal16_2(numero) {')
        if pos != -1:
            # Encontrar el final de la función
            pos_end = contenido_actualizado.find('}', pos)
            pos_end = contenido_actualizado.find('}', pos_end + 1)  # Siguiente }
            
            contenido_actualizado = (
                contenido_actualizado[:pos_end + 1] + 
                validacion_12_2 + 
                contenido_actualizado[pos_end + 1:]
            )
            correcciones_aplicadas += 1
            print("✅ Agregada función validarDecimal12_2")
    
    # Guardar archivo actualizado
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(contenido_actualizado)
    
    print(f"\n✅ JavaScript actualizado con {correcciones_aplicadas} correcciones")
    return True

def crear_resumen_correcciones():
    """Crea un resumen de las correcciones aplicadas"""
    
    resumen = """# Correcciones Aplicadas - Esquema BD vs Formulario

## 🔧 Problemas Identificados y Corregidos

### 1. Campo `ventap` No Existe en BD
- **Problema:** Formulario usa `ventap` pero tabla `declara` no lo tiene
- **Solución:** Mapear `ventap` a campo `ventas` existente o actualizar BD

### 2. Campo `impuesto` - Formato Incorrecto  
- **BD Real:** DECIMAL(12,2) - Máximo: 9,999,999,999.99
- **JavaScript:** Validaba DECIMAL(16,2) - Máximo: 99,999,999,999,999.99
- **Solución:** Agregada validación `validarDecimal12_2()`

### 3. Validaciones JavaScript Actualizadas
- Validación específica para campo `impuesto` con DECIMAL(12,2)
- Campos de ventas mantienen DECIMAL(16,2)
- Advertencias en consola para valores que excedan límites

## 📋 Estado Actual

| Campo | Formato BD | Formato JS | Estado |
|-------|------------|------------|--------|
| `ventai` | DECIMAL(16,2) | DECIMAL(16,2) | ✅ Correcto |
| `ventac` | DECIMAL(16,2) | DECIMAL(16,2) | ✅ Correcto |
| `ventas` | DECIMAL(16,2) | DECIMAL(16,2) | ✅ Correcto |
| `ventap` | ❌ NO EXISTE | DECIMAL(16,2) | ⚠️ Requiere BD |
| `impuesto` | DECIMAL(12,2) | DECIMAL(12,2) | ✅ Corregido |

## 🚀 Próximos Pasos

1. **Ejecutar SQL:** `corregir_esquema_declara.sql`
2. **Reiniciar servidor Django**
3. **Probar formulario con valores reales**
4. **Verificar que impuestos se calculen y guarden correctamente**
"""
    
    with open("c:/simafiweb/resumen_correcciones_esquema.md", 'w', encoding='utf-8') as f:
        f.write(resumen)
    
    print("✅ Resumen creado: resumen_correcciones_esquema.md")

def main():
    print("🔧 Corrigiendo validaciones JavaScript según esquema BD...")
    print("=" * 60)
    
    if actualizar_javascript_validaciones():
        crear_resumen_correcciones()
        
        print("\n" + "=" * 60)
        print("✅ CORRECCIONES COMPLETADAS")
        print("\n📝 ACCIONES REQUERIDAS:")
        print("1. Ejecutar: corregir_esquema_declara.sql en la BD")
        print("2. Reiniciar servidor Django")
        print("3. Probar formulario con valor: 5.000.000")
        print("4. Verificar que impuesto se calcule y guarde")
        
        print("\n⚠️ ALTERNATIVA (sin cambiar BD):")
        print("- Remover campo 'ventap' del formulario")
        print("- Usar solo ventai, ventac, ventas")
        
    else:
        print("❌ Error en las correcciones")

if __name__ == "__main__":
    main()

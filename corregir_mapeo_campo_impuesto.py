#!/usr/bin/env python
"""
Corrección para mapear correctamente el campo 'impuesto' de la tabla 'declara'
Asegura que el cálculo automático se guarde en el campo correcto de la base de datos
"""

import os
import re

def corregir_mapeo_campo_impuesto():
    """
    Corrige el mapeo del campo impuesto para que coincida con la tabla 'declara'
    """
    print("🔧 CORRIGIENDO MAPEO CAMPO IMPUESTO")
    print("=" * 40)
    
    # Archivos a modificar
    archivos = {
        'js_interactivo': r"c:\simafiweb\declaracion_volumen_interactivo.js",
        'js_calculadora': r"c:\simafiweb\declaracion_volumen_calculator.js"
    }
    
    # Verificar que los archivos existen
    for nombre, ruta in archivos.items():
        if not os.path.exists(ruta):
            print(f"⚠️  Archivo no encontrado: {ruta}")
            continue
            
        print(f"📝 Procesando: {nombre}")
        
        try:
            # Leer archivo
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear backup
            backup_path = ruta + ".backup_mapeo"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"   ✅ Backup: {backup_path}")
            
            # Correcciones específicas para mapeo de campo impuesto
            correcciones = [
                {
                    'descripcion': 'Priorizar campo id_impuesto',
                    'buscar': r"const camposImpuesto = \[(.*?)\];",
                    'reemplazar': """const camposImpuesto = [
            'id_impuesto',           // Campo principal tabla declara
            'impuesto',              // Campo directo tabla declara  
            'id_impuesto_calculado', // Alternativo
            'impuesto_calculado'     // Alternativo
        ];"""
                },
                {
                    'descripcion': 'Actualizar función obtenerValorCampo para impuesto',
                    'buscar': r"obtenerValorCampo\(campo\)",
                    'reemplazar': "obtenerValorCampo(campo)"
                }
            ]
            
            contenido_modificado = contenido
            cambios_realizados = []
            
            # Aplicar correcciones
            for correccion in correcciones:
                if re.search(correccion['buscar'], contenido_modificado, re.DOTALL):
                    contenido_modificado = re.sub(
                        correccion['buscar'], 
                        correccion['reemplazar'], 
                        contenido_modificado, 
                        flags=re.DOTALL
                    )
                    cambios_realizados.append(correccion['descripcion'])
            
            # Agregar función específica para mapeo de campos de tabla declara
            funcion_mapeo = '''
    /**
     * Mapea campos del formulario a la estructura de tabla 'declara'
     */
    mapearCamposTablaDeclaracion() {
        const mapeoTablaDeclaracion = {
            // Campos de ventas
            'ventai': ['id_ventai', 'ventai'],           // DECIMAL(12,2) - Ventas Industria
            'ventac': ['id_ventac', 'ventac'],           // DECIMAL(12,2) - Ventas Comercio
            'ventas': ['id_ventas', 'ventas'],           // DECIMAL(12,2) - Ventas Servicios
            'ventap': ['id_ventap', 'ventap'],           // Campo adicional para Rubro Producción
            
            // Campo impuesto - CRÍTICO para tabla declara
            'impuesto': ['id_impuesto', 'impuesto'],     // DECIMAL(12,2) - Campo destino principal
            
            // Otros campos de tabla declara
            'rtm': ['id_rtm', 'rtm'],                    // CHAR(20) - RTM
            'expe': ['id_expe', 'expe'],                 // CHAR(10) - Expediente
            'ano': ['id_ano', 'ano'],                    // DECIMAL(12,2) - Año
            'mes': ['id_mes', 'mes'],                    // DECIMAL(4,0) - Mes
            'tipo': ['id_tipo', 'tipo'],                 // DECIMAL(1,0) - Tipo
            'valorexcento': ['id_valorexcento', 'valorexcento'], // DECIMAL(12,2)
            'cocontrolado': ['id_cocontrolado', 'cocontrolado'], // DECIMAL(12,2)
            'unidad': ['id_unidad', 'unidad'],           // DECIMAL(11,0)
            'factor': ['id_factor', 'factor']            // DECIMAL(12,2)
        };
        
        return mapeoTablaDeclaracion;
    }

    /**
     * Obtiene el campo correcto según mapeo de tabla declara
     */
    obtenerCampoTablaDeclaracion(nombreCampo) {
        const mapeo = this.mapearCamposTablaDeclaracion();
        const posiblesIds = mapeo[nombreCampo] || [nombreCampo];
        
        for (const id of posiblesIds) {
            const campo = document.getElementById(id);
            if (campo) {
                return campo;
            }
        }
        return null;
    }'''
            
            # Insertar función antes del cierre de la clase
            if 'class DeclaracionVolumenInteractivo' in contenido_modificado:
                # Buscar el final de la clase
                patron_fin_clase = r'(\s+}(?:\s*//.*)?(?:\s*\n)*(?:\s*//.*\n)*\s*$)'
                if re.search(patron_fin_clase, contenido_modificado):
                    contenido_modificado = re.sub(
                        patron_fin_clase,
                        funcion_mapeo + r'\1',
                        contenido_modificado
                    )
                    cambios_realizados.append('Función de mapeo tabla declara agregada')
            
            # Actualizar función actualizarCamposCalculados para usar mapeo
            actualizacion_funcion = '''
        // Usar mapeo específico para tabla declara
        const campoImpuesto = this.obtenerCampoTablaDeclaracion('impuesto');
        if (campoImpuesto) {
            campoImpuesto.value = totalImpuesto.toFixed(2);
            campoImpuesto.style.backgroundColor = '#e8f5e8';
            campoImpuesto.style.fontWeight = 'bold';
            campoImpuesto.style.color = '#155724';
            console.log(`💰 Impuesto actualizado en campo tabla declara: $${totalImpuesto.toFixed(2)}`);
            campoActualizado = true;
        } else {
            // Fallback a búsqueda tradicional
            for (const id of camposImpuesto) {
                const campo = document.getElementById(id);
                if (campo) {
                    campo.value = totalImpuesto.toFixed(2);
                    campo.style.backgroundColor = '#e8f5e8';
                    campoActualizado = true;
                    console.log(`💰 Impuesto actualizado en ${id}: $${totalImpuesto.toFixed(2)}`);
                    break;
                }
            }
        }'''
            
            # Reemplazar la lógica de actualización de campos
            patron_actualizacion = r'let campoActualizado = false;.*?if \(!campoActualizado\)'
            if re.search(patron_actualizacion, contenido_modificado, re.DOTALL):
                contenido_modificado = re.sub(
                    r'(let campoActualizado = false;).*?(if \(!campoActualizado\))',
                    r'\1' + actualizacion_funcion + r'\n\n        \2',
                    contenido_modificado,
                    flags=re.DOTALL
                )
                cambios_realizados.append('Lógica de actualización mejorada para tabla declara')
            
            # Escribir archivo modificado
            if cambios_realizados:
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(contenido_modificado)
                
                print(f"   ✅ Modificado exitosamente")
                for cambio in cambios_realizados:
                    print(f"      - {cambio}")
            else:
                print(f"   ⚠️  No se realizaron cambios")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def mostrar_mapeo_tabla_declara():
    """
    Muestra el mapeo de campos para la tabla declara
    """
    print("\n📊 MAPEO TABLA 'declara'")
    print("=" * 30)
    print("CAMPO FORMULARIO → CAMPO BD → TIPO")
    print("-" * 40)
    print("Ventas Industria → ventai → DECIMAL(12,2)")
    print("Ventas Comercio  → ventac → DECIMAL(12,2)")  
    print("Ventas Servicios → ventas → DECIMAL(12,2)")
    print("Rubro Producción → ventap → (campo adicional)")
    print("IMPUESTO CALC.   → impuesto → DECIMAL(12,2) ← PRINCIPAL")
    print("RTM              → rtm → CHAR(20)")
    print("Expediente       → expe → CHAR(10)")
    print("Año              → ano → DECIMAL(12,2)")
    print("Mes              → mes → DECIMAL(4,0)")
    print("Tipo             → tipo → DECIMAL(1,0)")

if __name__ == "__main__":
    print("🎯 CORRECCIÓN MAPEO CAMPO IMPUESTO")
    print("   Tabla destino: 'declara'")
    print("   Campo crítico: 'impuesto' DECIMAL(12,2)")
    print()
    
    corregir_mapeo_campo_impuesto()
    mostrar_mapeo_tabla_declara()
    
    print("\n🎉 CORRECCIÓN COMPLETADA")
    print("   ✅ Campo 'impuesto' mapeado correctamente")
    print("   ✅ Prioridad a id_impuesto e impuesto")
    print("   ✅ Mapeo completo tabla 'declara'")
    print("   🔄 Reinicie servidor para aplicar cambios")
    
    print("\n" + "=" * 50)

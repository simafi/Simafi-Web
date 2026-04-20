#!/usr/bin/env python
"""
Corrige específicamente el JavaScript para DECIMAL(16,2)
"""

import os
import re

def corregir_javascript_decimal_16_2():
    """
    Corrige el JavaScript para formato DECIMAL(16,2) - 14 enteros + 2 decimales
    """
    print("🔧 CORRIGIENDO JAVASCRIPT PARA DECIMAL(16,2)")
    print("=" * 45)
    
    archivo = 'declaracion_volumen_interactivo.js'
    
    if not os.path.exists(archivo):
        print(f"❌ Archivo no encontrado: {archivo}")
        return False
    
    try:
        # Leer archivo
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        backup_path = archivo + ".backup_js_fix"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"✅ Backup creado: {backup_path}")
        
        # Reemplazar función formatearNumero completa
        nueva_funcion_formateo = '''    /**
     * Formatea números para DECIMAL(16,2) - 14 enteros + 2 decimales
     */
    formatearNumero(event) {
        const input = event.target;
        let valor = input.value;
        
        // Remover caracteres no numéricos excepto punto decimal
        valor = valor.replace(/[^0-9.]/g, '');
        
        // Permitir solo un punto decimal
        const partes = valor.split('.');
        if (partes.length > 2) {
            valor = partes[0] + '.' + partes.slice(1).join('');
        }
        
        // Limitar a 14 enteros
        if (partes[0] && partes[0].length > 14) {
            partes[0] = partes[0].substring(0, 14);
            valor = partes.join('.');
        }
        
        // Limitar a 2 decimales
        if (partes[1] && partes[1].length > 2) {
            partes[1] = partes[1].substring(0, 2);
            valor = partes[0] + '.' + partes[1];
        }
        
        // Validar rango máximo DECIMAL(16,2)
        const numeroValor = parseFloat(valor);
        if (numeroValor > 99999999999999.99) {
            valor = '99999999999999.99';
        }
        
        input.value = valor;
        
        // Formatear con separadores de miles para visualización
        if (valor && !valor.includes('.') && valor.length > 3) {
            const numeroFormateado = parseInt(valor).toLocaleString('es-CO');
            // Solo aplicar formato si no está editando
            if (document.activeElement !== input) {
                input.value = numeroFormateado;
            }
        }
    }'''
        
        # Buscar y reemplazar función formatearNumero
        patron_funcion = r'formatearNumero\(event\)\s*\{[^}]*\}'
        contenido_nuevo = re.sub(
            patron_funcion,
            nueva_funcion_formateo.strip(),
            contenido,
            flags=re.DOTALL
        )
        
        # Agregar validación DECIMAL(16,2)
        validacion_16_2 = '''
    /**
     * Valida formato DECIMAL(16,2) - 14 enteros + 2 decimales
     */
    validarDecimal16_2(valor) {
        if (!valor) return true;
        
        const valorStr = valor.toString();
        const partes = valorStr.split('.');
        
        // Verificar enteros (máximo 14)
        if (partes[0] && partes[0].length > 14) {
            return false;
        }
        
        // Verificar decimales (máximo 2)
        if (partes[1] && partes[1].length > 2) {
            return false;
        }
        
        // Verificar rango máximo
        const numero = parseFloat(valorStr);
        if (numero > 99999999999999.99) {
            return false;
        }
        
        return true;
    }
    
    /**
     * Obtiene valor validado para DECIMAL(16,2)
     */
    obtenerValorCampoValidado(campo) {
        const posiblesIds = [`id_${campo}`, campo, `${campo}_input`];
        
        for (const id of posiblesIds) {
            const input = document.getElementById(id);
            if (input && input.value) {
                let valor = input.value.replace(/[^0-9.]/g, '');
                const numero = parseFloat(valor) || 0;
                
                // Validar formato DECIMAL(16,2)
                if (!this.validarDecimal16_2(numero)) {
                    console.warn(`⚠️ Valor excede DECIMAL(16,2): ${numero}`);
                    return 0;
                }
                
                return numero;
            }
        }
        return 0;
    }'''
        
        # Insertar validación antes del cierre de la clase
        patron_fin_clase = r'(\s+}(?:\s*\n)*(?=//\s*Inicializar|document\.addEventListener))'
        if re.search(patron_fin_clase, contenido_nuevo):
            contenido_nuevo = re.sub(
                patron_fin_clase,
                validacion_16_2 + r'\1',
                contenido_nuevo
            )
        else:
            # Insertar antes de las últimas líneas
            contenido_nuevo = contenido_nuevo.replace(
                '    recalcular() {',
                validacion_16_2 + '\n\n    recalcular() {'
            )
        
        # Actualizar obtenerValorCampo para usar validación
        contenido_nuevo = contenido_nuevo.replace(
            'const valor = this.obtenerValorCampo(campo);',
            'const valor = this.obtenerValorCampoValidado(campo);'
        )
        
        # Corregir regex en obtenerValorCampo original
        contenido_nuevo = contenido_nuevo.replace(
            "const valor = input.value.replace(/[^\\d]/g, '');",
            "const valor = input.value.replace(/[^0-9]/g, '');"
        )
        
        # Escribir archivo corregido
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print("✅ JavaScript corregido para DECIMAL(16,2)")
        print("   • Función formatearNumero actualizada")
        print("   • Validación DECIMAL(16,2) agregada")
        print("   • Regex corregidos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    corregir_javascript_decimal_16_2()
    print("\n🔄 JavaScript listo para DECIMAL(16,2)")
    print("   Máximo: 99,999,999,999,999.99 (14 enteros + 2 decimales)")

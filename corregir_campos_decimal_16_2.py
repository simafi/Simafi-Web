#!/usr/bin/env python
"""
Corrige campos para DECIMAL(16,2) = 14 enteros + 2 decimales
Máximo: 99,999,999,999,999.99
"""

import os
import re

def corregir_campos_decimal_16_2():
    """
    Corrige configuración para DECIMAL(16,2) - 14 enteros + 2 decimales
    """
    print("🔧 CORRIGIENDO CAMPOS PARA DECIMAL(16,2)")
    print("=" * 45)
    print("Formato: DECIMAL(16,2) = 14 enteros + 2 decimales")
    print("Máximo: 99,999,999,999,999.99")
    print()
    
    # Configuración corregida
    config = {
        'max_enteros': 14,
        'max_decimales': 2,
        'maxlength': '18',  # 14 enteros + 1 punto + 2 decimales + 1 buffer
        'pattern': r'^\d{1,14}(\.\d{0,2})?$',
        'max_value': '99999999999999.99',
        'placeholder_examples': {
            'ventai': '12345678901234.56',
            'ventac': '98765432109876.54', 
            'ventas': '55555555555555.55',
            'ventap': '88888888888888.88'
        }
    }
    
    # Archivos a corregir
    archivos = [
        'declaracion_volumen_interactivo.js',
        'test_calculo_automatico.html'
    ]
    
    for archivo in archivos:
        if not os.path.exists(archivo):
            print(f"⚠️  Archivo no encontrado: {archivo}")
            continue
            
        print(f"📝 Corrigiendo: {archivo}")
        
        try:
            # Leer archivo
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear backup
            backup_path = archivo + ".backup_16_2"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"   ✅ Backup: {backup_path}")
            
            if archivo.endswith('.js'):
                contenido = corregir_javascript_16_2(contenido, config)
            elif archivo.endswith('.html'):
                contenido = corregir_html_16_2(contenido, config)
            
            # Escribir archivo corregido
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print(f"   ✅ Corregido exitosamente")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def corregir_javascript_16_2(contenido, config):
    """
    Corrige JavaScript para DECIMAL(16,2)
    """
    # Nueva función formatearNumero corregida
    nueva_funcion = '''    /**
     * Formatea números para DECIMAL(16,2) - 14 enteros + 2 decimales
     */
    formatearNumero(event) {
        const input = event.target;
        let valor = input.value;
        
        // Remover caracteres no numéricos excepto punto decimal
        valor = valor.replace(/[^\\d.]/g, '');
        
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
    
    # Reemplazar función formatearNumero
    patron_funcion = r'formatearNumero\(event\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
    contenido = re.sub(
        patron_funcion,
        nueva_funcion.strip(),
        contenido,
        flags=re.DOTALL
    )
    
    # Agregar/actualizar validación DECIMAL(16,2)
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
                let valor = input.value.replace(/[^\\d.]/g, '');
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
    
    # Reemplazar validaciones anteriores
    if 'validarDecimal18_2' in contenido:
        contenido = re.sub(
            r'validarDecimal18_2.*?return 0;\s*}',
            validacion_16_2.strip().split('obtenerValorCampoValidado')[1].strip(),
            contenido,
            flags=re.DOTALL
        )
    else:
        # Insertar antes del cierre de clase
        patron_fin = r'(\s+}(?:\s*\n)*(?=//\s*Inicializar|document\.addEventListener))'
        contenido = re.sub(
            patron_fin,
            validacion_16_2 + r'\1',
            contenido
        )
    
    # Actualizar referencias a validación
    contenido = contenido.replace('validarDecimal18_2', 'validarDecimal16_2')
    contenido = contenido.replace('9999999999999999.99', '99999999999999.99')
    
    return contenido

def corregir_html_16_2(contenido, config):
    """
    Corrige HTML para DECIMAL(16,2)
    """
    # Actualizar placeholders
    placeholders = {
        'placeholder="Ej: 1234567890123456.78"': f'placeholder="Ej: {config["placeholder_examples"]["ventai"]}"',
        'placeholder="Ej: 9876543210987654.32"': f'placeholder="Ej: {config["placeholder_examples"]["ventac"]}"',
        'placeholder="Ej: 5555555555555555.55"': f'placeholder="Ej: {config["placeholder_examples"]["ventas"]}"',
        'placeholder="Ej: 8888888888888888.88"': f'placeholder="Ej: {config["placeholder_examples"]["ventap"]}"'
    }
    
    for viejo, nuevo in placeholders.items():
        contenido = contenido.replace(viejo, nuevo)
    
    # Actualizar atributos maxlength y pattern
    contenido = contenido.replace('maxlength="21"', f'maxlength="{config["maxlength"]}"')
    contenido = contenido.replace('pattern="^\\d{1,16}(\\\.\\d{0,2})?$"', f'pattern="{config["pattern"]}"')
    
    # Actualizar información de formato
    contenido = contenido.replace(
        '16 enteros + 2 decimales',
        '14 enteros + 2 decimales'
    )
    contenido = contenido.replace(
        '9,999,999,999,999,999.99',
        '99,999,999,999,999.99'
    )
    contenido = contenido.replace(
        'DECIMAL(18,2)',
        'DECIMAL(16,2)'
    )
    
    # Actualizar casos de prueba
    contenido = contenido.replace(
        'Caso 3: Rango Alto<br>\n                        <small>$25,000,000</small>',
        'Caso 3: Rango Alto<br>\n                        <small>$25,000,000,000,000</small>'
    )
    
    return contenido

def corregir_template_real():
    """
    Corrige el template real de Django
    """
    template_path = r"C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html"
    
    if not os.path.exists(template_path):
        print("⚠️  Template real no encontrado")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        backup_path = template_path + ".backup_16_2"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Actualizar atributos para DECIMAL(16,2)
        contenido = contenido.replace('maxlength="21"', 'maxlength="18"')
        contenido = contenido.replace('pattern="^\\\\d{1,16}(\\\\.\\\\d{0,2})?$"', 'pattern="^\\\\d{1,14}(\\\\.\\\\d{0,2})?$"')
        contenido = contenido.replace('16 enteros + 2 decimales', '14 enteros + 2 decimales')
        
        # Escribir template corregido
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("✅ Template real corregido para DECIMAL(16,2)")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo template real: {e}")
        return False

def mostrar_resumen_correccion():
    """
    Muestra resumen de la corrección
    """
    print("\n🎉 CORRECCIÓN DECIMAL(16,2) COMPLETADA")
    print("=" * 45)
    print("📊 FORMATO CORREGIDO:")
    print("   • Tipo: DECIMAL(16,2)")
    print("   • Enteros: Máximo 14 dígitos")
    print("   • Decimales: Máximo 2 dígitos")
    print("   • Valor máximo: 99,999,999,999,999.99")
    print()
    print("✅ VALIDACIONES CORREGIDAS:")
    print("   • Longitud máxima: 18 caracteres")
    print("   • Patrón: ^\\d{1,14}(\\.\\d{0,2})?$")
    print("   • Rango máximo actualizado")
    print("   • Ejemplos de placeholders actualizados")
    print()
    print("🎯 CAMPOS AFECTADOS:")
    print("   • ventai - Ventas Industria")
    print("   • ventac - Ventas Comercio")
    print("   • ventas - Ventas Servicios")
    print("   • ventap - Ventas Rubro Producción")
    print("   • valorexcento - Valor Excento")
    print("   • cocontrolado - Co-controlado")

if __name__ == "__main__":
    print("🎯 CORRECCIÓN PARA DECIMAL(16,2)")
    print("   Formato: 14 enteros + 2 decimales")
    print("   Máximo: 99,999,999,999,999.99")
    print()
    
    corregir_campos_decimal_16_2()
    corregir_template_real()
    mostrar_resumen_correccion()
    
    print("\n🔄 REINICIE EL SERVIDOR PARA APLICAR CAMBIOS")
    print("=" * 45)

#!/usr/bin/env python
"""
Configura campos de volumen de ventas para formato DECIMAL(18,2)
16 enteros + 2 decimales = máximo 9,999,999,999,999,999.99
"""

import os
import re

def configurar_campos_volumen_ventas():
    """
    Configura campos de ventas para formato DECIMAL(18,2)
    """
    print("🔧 CONFIGURANDO CAMPOS VOLUMEN VENTAS")
    print("=" * 45)
    print("Formato: DECIMAL(18,2) = 16 enteros + 2 decimales")
    print("Máximo: 9,999,999,999,999,999.99")
    print()
    
    # Archivos a modificar
    archivos = {
        'js_interactivo': r"c:\simafiweb\declaracion_volumen_interactivo.js",
        'template_test': r"c:\simafiweb\test_calculo_automatico.html"
    }
    
    # Configuración de campos
    config_campos = {
        'maxlength': '21',  # 16 enteros + 1 punto + 2 decimales + 2 separadores
        'pattern': r'^\d{1,16}(\.\d{0,2})?$',
        'max_value': '9999999999999999.99',
        'placeholder_examples': {
            'ventai': '1234567890123456.78',
            'ventac': '9876543210987654.32', 
            'ventas': '5555555555555555.55',
            'ventap': '8888888888888888.88'
        }
    }
    
    for nombre, ruta in archivos.items():
        if not os.path.exists(ruta):
            print(f"⚠️  Archivo no encontrado: {ruta}")
            continue
            
        print(f"📝 Configurando: {nombre}")
        
        try:
            # Leer archivo
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear backup
            backup_path = ruta + ".backup_campos"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"   ✅ Backup: {backup_path}")
            
            contenido_modificado = contenido
            
            if nombre == 'js_interactivo':
                contenido_modificado = configurar_javascript(contenido_modificado, config_campos)
            elif nombre == 'template_test':
                contenido_modificado = configurar_template_test(contenido_modificado, config_campos)
            
            # Escribir archivo modificado
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido_modificado)
            
            print(f"   ✅ Configurado exitosamente")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def configurar_javascript(contenido, config):
    """
    Configura el JavaScript para manejar DECIMAL(18,2)
    """
    # Actualizar función formatearNumero
    nueva_funcion_formateo = '''
    /**
     * Formatea números para DECIMAL(18,2) - 16 enteros + 2 decimales
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
        
        // Limitar a 16 enteros
        if (partes[0] && partes[0].length > 16) {
            partes[0] = partes[0].substring(0, 16);
            valor = partes.join('.');
        }
        
        // Limitar a 2 decimales
        if (partes[1] && partes[1].length > 2) {
            partes[1] = partes[1].substring(0, 2);
            valor = partes[0] + '.' + partes[1];
        }
        
        // Validar rango máximo
        const numeroValor = parseFloat(valor);
        if (numeroValor > 9999999999999999.99) {
            valor = '9999999999999999.99';
        }
        
        input.value = valor;
        
        // Formatear con separadores de miles solo para visualización
        if (valor && !valor.includes('.') && valor.length > 3) {
            const numeroFormateado = parseInt(valor).toLocaleString('es-CO');
            // Solo aplicar formato si no está editando decimales
            if (document.activeElement !== input) {
                input.value = numeroFormateado;
            }
        }
    }'''
    
    # Reemplazar función existente
    patron_funcion = r'formatearNumero\(event\)\s*{[^}]*}'
    contenido = re.sub(
        patron_funcion, 
        nueva_funcion_formateo.strip().split('{', 1)[1].rstrip('}'), 
        contenido, 
        flags=re.DOTALL
    )
    
    # Agregar validación específica para DECIMAL(18,2)
    validacion_decimal = '''
    
    /**
     * Valida formato DECIMAL(18,2)
     */
    validarDecimal18_2(valor) {
        if (!valor) return true;
        
        const valorStr = valor.toString();
        const partes = valorStr.split('.');
        
        // Verificar enteros (máximo 16)
        if (partes[0] && partes[0].length > 16) {
            return false;
        }
        
        // Verificar decimales (máximo 2)
        if (partes[1] && partes[1].length > 2) {
            return false;
        }
        
        // Verificar rango máximo
        const numero = parseFloat(valorStr);
        if (numero > 9999999999999999.99) {
            return false;
        }
        
        return true;
    }
    
    /**
     * Obtiene el valor numérico validado para DECIMAL(18,2)
     */
    obtenerValorCampoValidado(campo) {
        const posiblesIds = [`id_${campo}`, campo, `${campo}_input`];
        
        for (const id of posiblesIds) {
            const input = document.getElementById(id);
            if (input && input.value) {
                let valor = input.value.replace(/[^\\d.]/g, '');
                const numero = parseFloat(valor) || 0;
                
                // Validar formato DECIMAL(18,2)
                if (!this.validarDecimal18_2(numero)) {
                    console.warn(`⚠️ Valor excede DECIMAL(18,2): ${numero}`);
                    return 0;
                }
                
                return numero;
            }
        }
        return 0;
    }'''
    
    # Insertar validación antes del cierre de la clase
    patron_fin_clase = r'(\s+}(?:\s*//.*)?(?:\s*\n)*(?:\s*//.*\n)*\s*(?=//\s*Inicializar|$))'
    contenido = re.sub(
        patron_fin_clase,
        validacion_decimal + r'\1',
        contenido
    )
    
    # Actualizar obtenerValorCampo para usar la versión validada
    contenido = contenido.replace(
        'obtenerValorCampo(campo)',
        'obtenerValorCampoValidado(campo)'
    )
    
    return contenido

def configurar_template_test(contenido, config):
    """
    Configura el template de test para DECIMAL(18,2)
    """
    # Actualizar placeholders con ejemplos de 16 dígitos
    placeholders = {
        'placeholder="Ej: 1500000"': f'placeholder="Ej: {config["placeholder_examples"]["ventai"]}"',
        'placeholder="Ej: 2500000"': f'placeholder="Ej: {config["placeholder_examples"]["ventac"]}"',
        'placeholder="Ej: 3000000"': f'placeholder="Ej: {config["placeholder_examples"]["ventas"]}"',
        'placeholder="Ej: 8000000"': f'placeholder="Ej: {config["placeholder_examples"]["ventap"]}"'
    }
    
    for viejo, nuevo in placeholders.items():
        contenido = contenido.replace(viejo, nuevo)
    
    # Agregar atributos de validación a inputs
    patron_input = r'(<input[^>]*class="[^"]*campo-calculado[^"]*"[^>]*)'
    
    def agregar_atributos(match):
        input_tag = match.group(1)
        if 'maxlength=' not in input_tag:
            input_tag = input_tag.rstrip('>') + f' maxlength="{config["maxlength"]}"'
        if 'pattern=' not in input_tag:
            input_tag = input_tag.rstrip('>') + f' pattern="{config["pattern"]}"'
        if 'title=' not in input_tag:
            input_tag = input_tag.rstrip('>') + ' title="Formato: 16 enteros + 2 decimales (máx: 9,999,999,999,999,999.99)"'
        return input_tag + '>'
    
    contenido = re.sub(patron_input, agregar_atributos, contenido)
    
    # Actualizar información de formato en la página
    info_formato = '''
                        <div class="alert alert-info mt-2">
                            <strong>📏 Formato de Campos:</strong><br>
                            • Máximo: 16 enteros + 2 decimales<br>
                            • Ejemplo: 9,999,999,999,999,999.99<br>
                            • Formato: DECIMAL(18,2)
                        </div>'''
    
    # Insertar después de la sección de tarifas
    if 'Tarifas ICS Configuradas' in contenido:
        contenido = contenido.replace(
            '</div>\n        </div>',
            '</div>' + info_formato + '\n        </div>',
            1
        )
    
    return contenido

def configurar_template_real():
    """
    Configura el template real de Django
    """
    template_path = r"C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html"
    
    if not os.path.exists(template_path):
        print("⚠️  Template real no encontrado")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        backup_path = template_path + ".backup_decimal18_2"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Agregar atributos a campos de ventas
        campos_ventas = ['ventai', 'ventac', 'ventas', 'ventap', 'impuesto']
        
        for campo in campos_ventas:
            # Buscar inputs por name
            patron = f'(<input[^>]*name="{campo}"[^>]*)'
            
            def agregar_atributos_decimal(match):
                input_tag = match.group(1)
                
                if campo != 'impuesto':  # Campos de entrada
                    if 'maxlength=' not in input_tag:
                        input_tag = input_tag.rstrip('>') + ' maxlength="21"'
                    if 'pattern=' not in input_tag:
                        input_tag = input_tag.rstrip('>') + ' pattern="^\\d{1,16}(\\.\\d{0,2})?$"'
                    if 'title=' not in input_tag:
                        input_tag = input_tag.rstrip('>') + ' title="Máximo: 16 enteros + 2 decimales"'
                    if 'step=' not in input_tag:
                        input_tag = input_tag.rstrip('>') + ' step="0.01"'
                else:  # Campo resultado
                    if 'readonly' not in input_tag:
                        input_tag = input_tag.rstrip('>') + ' readonly'
                
                return input_tag + '>'
            
            contenido = re.sub(patron, agregar_atributos_decimal, contenido)
        
        # Escribir template modificado
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("✅ Template real configurado para DECIMAL(18,2)")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando template real: {e}")
        return False

def mostrar_resumen_configuracion():
    """
    Muestra resumen de la configuración
    """
    print("\n🎉 CONFIGURACIÓN DECIMAL(18,2) COMPLETADA")
    print("=" * 45)
    print("📊 FORMATO CONFIGURADO:")
    print("   • Tipo: DECIMAL(18,2)")
    print("   • Enteros: Máximo 16 dígitos")
    print("   • Decimales: Máximo 2 dígitos")
    print("   • Valor máximo: 9,999,999,999,999,999.99")
    print()
    print("✅ VALIDACIONES AGREGADAS:")
    print("   • Longitud máxima de entrada")
    print("   • Patrón de formato numérico")
    print("   • Validación de rango máximo")
    print("   • Formateo automático con separadores")
    print()
    print("🎯 CAMPOS CONFIGURADOS:")
    print("   • Ventas Industria (ventai)")
    print("   • Ventas Comercio (ventac)")
    print("   • Ventas Servicios (ventas)")
    print("   • Ventas Rubro Producción (ventap)")
    print("   • Impuesto Calculado (solo lectura)")

if __name__ == "__main__":
    print("🎯 CONFIGURACIÓN CAMPOS VOLUMEN VENTAS")
    print("   Formato: DECIMAL(18,2) = 16 enteros + 2 decimales")
    print()
    
    configurar_campos_volumen_ventas()
    configurar_template_real()
    mostrar_resumen_configuracion()
    
    print("\n🔄 REINICIE EL SERVIDOR PARA APLICAR CAMBIOS")
    print("=" * 45)

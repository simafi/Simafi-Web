#!/usr/bin/env python3
"""
Script para probar los formatos específicos de Unidad y Factor
"""

def crear_test_formatos():
    """Crea un test HTML para verificar los formatos de Unidad y Factor"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test - Formatos Unidad y Factor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; border-radius: 8px; }
        .success { background-color: #d4edda; border-color: #c3e6cb; }
        .error { background-color: #f8d7da; border-color: #f5c6cb; }
        .info { background-color: #d1ecf1; border-color: #bee5eb; }
        .warning { background-color: #fff3cd; border-color: #ffeaa7; }
        input { margin: 5px; padding: 8px; width: 200px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .form-text { font-size: 0.875em; color: #6c757d; margin-top: 0.25rem; }
        .form-text i { margin-right: 0.3rem; }
        .log { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; font-family: monospace; font-size: 0.9em; }
        .test-case { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
        .test-result { font-weight: bold; margin-top: 5px; }
        .pass { color: #28a745; }
        .fail { color: #dc3545; }
    </style>
</head>
<body>
    <h1>🧪 Test - Formatos Unidad y Factor</h1>
    
    <div class="test-section info">
        <h3>📋 Especificaciones de Formato</h3>
        <ul>
            <li><strong>Unidad:</strong> Solo números enteros (máximo 10 dígitos)</li>
            <li><strong>Factor:</strong> DECIMAL(10,2) - 10 enteros, 2 decimales (ej: 1234567890.99)</li>
        </ul>
    </div>
    
    <div class="test-section">
        <h3>🧮 Campos de Prueba</h3>
        
        <div class="test-case">
            <label><strong>Unidad (Solo Enteros):</strong></label>
            <input type="text" id="id_unidad" placeholder="Ej: 1000" oninput="validarUnidad()">
            <div class="form-text">
                <i class="fas fa-info-circle"></i> Solo números enteros (máximo 10 dígitos)
            </div>
            <div id="resultado_unidad" class="test-result"></div>
        </div>
        
        <div class="test-case">
            <label><strong>Factor (DECIMAL 10,2):</strong></label>
            <input type="text" id="id_factor" placeholder="Ej: 1.50" oninput="validarFactor()">
            <div class="form-text">
                <i class="fas fa-info-circle"></i> Formato: 10 enteros, 2 decimales (ej: 1234567890.99)
            </div>
            <div id="resultado_factor" class="test-result"></div>
        </div>
        
        <button onclick="probarCasos()">🧪 Probar Casos de Prueba</button>
        <button onclick="limpiarCampos()">🧹 Limpiar Campos</button>
    </div>
    
    <div class="test-section">
        <h3>📊 Casos de Prueba</h3>
        <div id="casos_prueba"></div>
    </div>
    
    <div class="test-section">
        <h3>📝 Logs del Sistema</h3>
        <div id="logs">Los logs del sistema aparecerán aquí...</div>
    </div>

    <script>
        // Función para limpiar valor según tipo
        function limpiarValor(valor, tipo = 'general') {
            if (!valor) return 0;
            
            // Limpiar caracteres no numéricos excepto punto decimal
            let valorLimpio = valor.toString().replace(/[^0-9.]/g, '');
            
            if (tipo === 'unidad') {
                // Para Unidad: solo enteros (sin decimales)
                valorLimpio = valorLimpio.split('.')[0]; // Remover parte decimal
                const numero = parseInt(valorLimpio) || 0;
                return numero;
            } else if (tipo === 'factor') {
                // Para Factor: 10 enteros, 2 decimales (DECIMAL(10,2))
                const partes = valorLimpio.split('.');
                let parteEntera = partes[0] || '0';
                let parteDecimal = partes[1] || '00';
                
                // Limitar a 10 enteros
                if (parteEntera.length > 10) {
                    parteEntera = parteEntera.substring(0, 10);
                }
                
                // Limitar a 2 decimales
                if (parteDecimal.length > 2) {
                    parteDecimal = parteDecimal.substring(0, 2);
                }
                
                const numero = parseFloat(parteEntera + '.' + parteDecimal) || 0;
                return numero;
            } else {
                // Para otros campos: comportamiento general
                const numero = parseFloat(valorLimpio) || 0;
                return numero;
            }
        }

        function validarUnidad() {
            const campo = document.getElementById('id_unidad');
            const valorOriginal = campo.value;
            
            // Aplicar validación de solo enteros
            let valor = valorOriginal.replace(/[^0-9]/g, '');
            
            // Limitar a 10 dígitos
            if (valor.length > 10) {
                valor = valor.substring(0, 10);
            }
            
            campo.value = valor;
            
            const valorLimpio = limpiarValor(valor, 'unidad');
            const resultado = document.getElementById('resultado_unidad');
            
            if (valorOriginal !== valor) {
                resultado.innerHTML = `<span class="warning">⚠️ Valor corregido: "${valorOriginal}" → "${valor}"</span>`;
            } else if (valorLimpio > 0) {
                resultado.innerHTML = `<span class="pass">✅ Valor válido: ${valorLimpio}</span>`;
            } else {
                resultado.innerHTML = `<span class="fail">❌ Valor inválido</span>`;
            }
            
            log(`Campo Unidad: "${valorOriginal}" → "${valor}" → ${valorLimpio}`);
        }

        function validarFactor() {
            const campo = document.getElementById('id_factor');
            const valorOriginal = campo.value;
            
            // Limpiar caracteres no numéricos excepto punto decimal
            let valor = valorOriginal.replace(/[^0-9.]/g, '');
            
            // Asegurar solo un punto decimal
            const partes = valor.split('.');
            if (partes.length > 2) {
                valor = partes[0] + '.' + partes.slice(1).join('');
            }
            
            // Recalcular partes después de la limpieza
            const partesLimpias = valor.split('.');
            
            // Limitar a 10 enteros
            if (partesLimpias[0].length > 10) {
                partesLimpias[0] = partesLimpias[0].substring(0, 10);
            }
            
            // Limitar a 2 decimales
            if (partesLimpias.length === 2 && partesLimpias[1].length > 2) {
                partesLimpias[1] = partesLimpias[1].substring(0, 2);
            }
            
            // Reconstruir el valor
            valor = partesLimpias[0] + (partesLimpias.length === 2 ? '.' + partesLimpias[1] : '');
            
            campo.value = valor;
            
            const valorLimpio = limpiarValor(valor, 'factor');
            const resultado = document.getElementById('resultado_factor');
            
            if (valorOriginal !== valor) {
                resultado.innerHTML = `<span class="warning">⚠️ Valor corregido: "${valorOriginal}" → "${valor}"</span>`;
            } else if (valorLimpio > 0) {
                resultado.innerHTML = `<span class="pass">✅ Valor válido: ${valorLimpio}</span>`;
            } else {
                resultado.innerHTML = `<span class="fail">❌ Valor inválido</span>`;
            }
            
            log(`Campo Factor: "${valorOriginal}" → "${valor}" → ${valorLimpio}`);
        }

        function probarCasos() {
            const casos = [
                // Casos para Unidad (solo enteros)
                { input: '1000', tipo: 'unidad', esperado: 1000, descripcion: 'Número entero válido' },
                { input: '1000.50', tipo: 'unidad', esperado: 1000, descripcion: 'Decimal convertido a entero' },
                { input: '12345678901', tipo: 'unidad', esperado: 1234567890, descripcion: 'Más de 10 dígitos truncado' },
                { input: 'abc123def', tipo: 'unidad', esperado: 123, descripcion: 'Caracteres no numéricos removidos' },
                { input: '', tipo: 'unidad', esperado: 0, descripcion: 'Campo vacío' },
                
                // Casos para Factor (DECIMAL 10,2)
                { input: '1.50', tipo: 'factor', esperado: 1.5, descripcion: 'Decimal válido' },
                { input: '1234567890.99', tipo: 'factor', esperado: 1234567890.99, descripcion: 'Máximo permitido' },
                { input: '12345678901.999', tipo: 'factor', esperado: 1234567890.99, descripcion: 'Más de 10 enteros y 2 decimales' },
                { input: '1.123', tipo: 'factor', esperado: 1.12, descripcion: 'Más de 2 decimales truncado' },
                { input: 'abc1.50def', tipo: 'factor', esperado: 1.5, descripcion: 'Caracteres no numéricos removidos' },
                { input: '1000', tipo: 'factor', esperado: 1000, descripcion: 'Entero sin decimales' },
                { input: '', tipo: 'factor', esperado: 0, descripcion: 'Campo vacío' }
            ];
            
            const resultados = document.getElementById('casos_prueba');
            resultados.innerHTML = '<h4>Resultados de Pruebas:</h4>';
            
            casos.forEach((caso, index) => {
                const resultado = limpiarValor(caso.input, caso.tipo);
                const esCorrecto = resultado === caso.esperado;
                
                const div = document.createElement('div');
                div.className = 'test-case';
                div.innerHTML = `
                    <strong>Prueba ${index + 1}:</strong> ${caso.descripcion}<br>
                    <strong>Entrada:</strong> "${caso.input}" | <strong>Tipo:</strong> ${caso.tipo}<br>
                    <strong>Esperado:</strong> ${caso.esperado} | <strong>Obtenido:</strong> ${resultado}<br>
                    <span class="${esCorrecto ? 'pass' : 'fail'}">${esCorrecto ? '✅ PASÓ' : '❌ FALLÓ'}</span>
                `;
                resultados.appendChild(div);
                
                log(`Prueba ${index + 1}: "${caso.input}" (${caso.tipo}) → ${resultado} ${esCorrecto ? '✅' : '❌'}`);
            });
        }

        function limpiarCampos() {
            document.getElementById('id_unidad').value = '';
            document.getElementById('id_factor').value = '';
            document.getElementById('resultado_unidad').innerHTML = '';
            document.getElementById('resultado_factor').innerHTML = '';
            document.getElementById('casos_prueba').innerHTML = '';
            document.getElementById('logs').innerHTML = '';
        }

        function log(mensaje) {
            console.log(mensaje);
            const logsDiv = document.getElementById('logs');
            if (logsDiv) {
                const logEntry = document.createElement('div');
                logEntry.className = 'log';
                logEntry.textContent = mensaje;
                logsDiv.appendChild(logEntry);
                logsDiv.scrollTop = logsDiv.scrollHeight;
            }
        }

        // Inicializar
        document.addEventListener('DOMContentLoaded', function() {
            log('🚀 Test de formatos Unidad y Factor iniciado');
        });
    </script>
</body>
</html>'''
    
    with open('test_formatos_unidad_factor.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test de formatos Unidad y Factor creado: test_formatos_unidad_factor.html")
    print("📝 Para probar: abra el archivo en un navegador web")

def mostrar_instrucciones():
    """Muestra las instrucciones para probar los formatos"""
    
    print("\n" + "=" * 60)
    print("🎯 INSTRUCCIONES PARA PROBAR FORMATOS:")
    print("=" * 60)
    
    print("\n1️⃣ TEST INDEPENDIENTE:")
    print("   • Abrir 'test_formatos_unidad_factor.html' en el navegador")
    print("   • Probar diferentes valores en los campos")
    print("   • Ejecutar 'Probar Casos de Prueba' para verificación automática")
    
    print("\n2️⃣ FORMATOS IMPLEMENTADOS:")
    print("   • <strong>Unidad:</strong> Solo enteros (máximo 10 dígitos)")
    print("     - Ejemplos válidos: 1000, 1234567890")
    print("     - Se remueven decimales automáticamente")
    print("     - Se truncan a 10 dígitos si excede")
    
    print("\n   • <strong>Factor:</strong> DECIMAL(10,2) - 10 enteros, 2 decimales")
    print("     - Ejemplos válidos: 1.50, 1234567890.99")
    print("     - Máximo 10 dígitos enteros")
    print("     - Máximo 2 dígitos decimales")
    print("     - Se trunca automáticamente si excede")
    
    print("\n3️⃣ VALIDACIÓN EN TIEMPO REAL:")
    print("   • Los campos se validan mientras se escribe")
    print("   • Se corrigen automáticamente valores inválidos")
    print("   • Se muestran mensajes de corrección")
    print("   • Se registran logs en consola del navegador")
    
    print("\n✅ RESULTADO ESPERADO:")
    print("   Los campos deben aceptar solo los formatos especificados")
    print("   y corregir automáticamente valores que no cumplan las reglas.")

if __name__ == "__main__":
    crear_test_formatos()
    mostrar_instrucciones()

#!/usr/bin/env python3
"""
Script para mostrar el cálculo detallado de Factor × Unidad
"""

def mostrar_calculo_detallado():
    """Muestra cómo funciona el cálculo de Factor × Unidad"""
    
    print("🧮 CÁLCULO DETALLADO - FACTOR × UNIDAD")
    print("=" * 60)
    
    print("\n📋 PASOS DEL CÁLCULO:")
    print("1. Validar que Factor > 0 Y Unidad > 0")
    print("2. Multiplicar: valorCalculado = Factor × Unidad")
    print("3. Aplicar tarifas ICS sobre valorCalculado")
    print("4. Sumar el impuesto al total de impuestos")
    
    print("\n🔍 CÓDIGO JAVASCRIPT IMPLEMENTADO:")
    print("""
    calcularImpuestoUnidadFactor(valorUnidad, valorFactor) {
        // 1. Validar que ambos valores sean mayores a cero
        if (!valorUnidad || valorUnidad <= 0 || !valorFactor || valorFactor <= 0) {
            console.log('⚠️ Unidad o Factor no válidos');
            return { impuestoTotal: 0, valorCalculado: 0 };
        }

        // 2. Multiplicación simple: Factor × Unidad
        const valorCalculado = valorFactor * valorUnidad;
        
        console.log('🧮 Cálculo Factor × Unidad:');
        console.log('   Factor:', valorFactor);
        console.log('   Unidad:', valorUnidad);
        console.log('   Resultado:', valorFactor, '×', valorUnidad, '=', valorCalculado);

        // 3. Aplicar tarifas ICS sobre el resultado
        const resultadoICS = this.calcularImpuestoICS(valorCalculado);
        
        console.log('✅ Impuesto calculado para Factor × Unidad: L.', resultadoICS.impuestoTotal.toFixed(2));

        return {
            impuestoTotal: resultadoICS.impuestoTotal,
            valorCalculado: valorCalculado
        };
    }
    """)
    
    print("\n📊 EJEMPLOS DE CÁLCULO:")
    
    ejemplos = [
        {"factor": 1, "unidad": 500, "descripcion": "Ejemplo básico"},
        {"factor": 1.5, "unidad": 1000, "descripcion": "Con decimales"},
        {"factor": 2.25, "unidad": 200, "descripcion": "Factor decimal"},
        {"factor": 0, "unidad": 500, "descripcion": "Factor = 0 (no calcula)"},
        {"factor": 1.5, "unidad": 0, "descripcion": "Unidad = 0 (no calcula)"},
        {"factor": 0, "unidad": 0, "descripcion": "Ambos = 0 (no calcula)"}
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        factor = ejemplo["factor"]
        unidad = ejemplo["unidad"]
        descripcion = ejemplo["descripcion"]
        
        if factor > 0 and unidad > 0:
            valor_calculado = factor * unidad
            print(f"\n{i}. {descripcion}:")
            print(f"   Factor: {factor}")
            print(f"   Unidad: {unidad}")
            print(f"   Cálculo: {factor} × {unidad} = {valor_calculado}")
            print(f"   ✅ Se calcula impuesto sobre {valor_calculado}")
        else:
            print(f"\n{i}. {descripcion}:")
            print(f"   Factor: {factor}")
            print(f"   Unidad: {unidad}")
            print(f"   ❌ No se calcula (uno o ambos valores = 0)")
    
    print("\n🎯 TARIFAS ICS APLICADAS:")
    print("Las tarifas ICS se aplican sobre el resultado de Factor × Unidad:")
    print("• $0 - $500,000: 0.3 por mil")
    print("• $500,000 - $10,000,000: 0.4 por mil")
    print("• $10,000,000 - $20,000,000: 0.3 por mil")
    print("• $20,000,000 - $30,000,000: 0.2 por mil")
    print("• $30,000,000+: 0.15 por mil")
    
    print("\n📝 LOGS EN CONSOLA DEL NAVEGADOR:")
    print("Cuando ingreses valores en el formulario, verás estos logs:")
    print("🧮 Cálculo Factor × Unidad:")
    print("   Factor: 1.5")
    print("   Unidad: 500")
    print("   Resultado: 1.5 × 500 = 750")
    print("✅ Impuesto calculado para Factor × Unidad: L. X.XX")
    
    print("\n🔧 CÓMO PROBAR EN EL FORMULARIO REAL:")
    print("1. Abrir el formulario de declaración de volumen")
    print("2. Abrir consola del navegador (F12)")
    print("3. Ingresar un valor en Factor (ej: 1.5)")
    print("4. Ingresar un valor en Unidad (ej: 500)")
    print("5. Observar los logs en la consola")
    print("6. Verificar que el campo 'Impuesto Calculado' se actualice")

def crear_ejemplo_visual():
    """Crea un ejemplo visual del cálculo"""
    
    ejemplo_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo Visual - Cálculo Factor × Unidad</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .step { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .calculation { background: #fff3e0; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ff9800; }
        .result { background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2196f3; }
        .log { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; font-family: monospace; font-size: 0.9em; border: 1px solid #dee2e6; }
        .highlight { background: #ffeb3b; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
        .example { background: #f0f8ff; padding: 15px; margin: 10px 0; border-radius: 8px; border: 2px solid #4169e1; }
        input { padding: 8px; margin: 5px; border: 1px solid #ccc; border-radius: 4px; width: 150px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #0056b3; }
        .formula { font-size: 1.2em; font-weight: bold; color: #d32f2f; text-align: center; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 Ejemplo Visual - Cálculo Factor × Unidad</h1>
        
        <div class="step">
            <h3>📋 Cómo Funciona el Cálculo</h3>
            <p>El sistema calcula el impuesto usando la fórmula: <span class="highlight">Factor × Unidad</span></p>
            <p>Luego aplica las tarifas ICS sobre el resultado obtenido.</p>
        </div>

        <div class="example">
            <h3>🎯 Ejemplo Práctico</h3>
            <p><strong>Escenario:</strong> Un negocio tiene 500 unidades de un producto con un factor de 1.5</p>
            <div class="formula">Factor (1.5) × Unidad (500) = 750</div>
            <p>El sistema calcula el impuesto sobre el valor 750 usando las tarifas ICS.</p>
        </div>

        <div class="step">
            <h3>🔧 Probar el Cálculo</h3>
            <label>Factor: <input type="text" id="factor" value="1.5" placeholder="Ej: 1.5"></label>
            <label>Unidad: <input type="text" id="unidad" value="500" placeholder="Ej: 500"></label>
            <button onclick="calcular()">🧮 Calcular</button>
            <button onclick="limpiar()">🧹 Limpiar</button>
        </div>

        <div id="resultado" class="result" style="display: none;">
            <h3>📊 Resultado del Cálculo</h3>
            <div id="detalle"></div>
        </div>

        <div class="step">
            <h3>📝 Logs del Sistema</h3>
            <div id="logs">Los logs aparecerán aquí cuando hagas un cálculo...</div>
        </div>
    </div>

    <script>
        // Tarifas ICS (copiadas del sistema real)
        const tarifas = [
            {"rango1": 0.0, "rango2": 500000.0, "valor": 0.3, "descripcion": "Rango $0 - $500,000"},
            {"rango1": 500000.01, "rango2": 10000000.0, "valor": 0.4, "descripcion": "Rango $500,000 - $10,000,000"},
            {"rango1": 10000000.01, "rango2": 20000000.0, "valor": 0.3, "descripcion": "Rango $10,000,000 - $20,000,000"},
            {"rango1": 20000000.01, "rango2": 30000000.0, "valor": 0.2, "descripcion": "Rango $20,000,000 - $30,000,000"},
            {"rango1": 30000000.01, "rango2": 9999999999.0, "valor": 0.15, "descripcion": "Rango $30,000,000+"}
        ];

        function calcularImpuestoICS(valorVentas) {
            if (!valorVentas || valorVentas <= 0) {
                return { impuestoTotal: 0, detalleCalculo: [] };
            }

            let impuestoTotal = 0;
            let valorRestante = valorVentas;
            const detalleCalculo = [];

            for (const tarifa of tarifas) {
                if (valorRestante <= 0) break;

                const diferencialRango = tarifa.rango2 - tarifa.rango1;
                if (diferencialRango <= 0) continue;

                let valorAplicable;
                if (valorRestante <= diferencialRango) {
                    valorAplicable = valorRestante;
                    valorRestante = 0;
                } else {
                    valorAplicable = diferencialRango;
                    valorRestante -= diferencialRango;
                }

                const impuestoRango = Math.round((valorAplicable * tarifa.valor / 1000) * 100) / 100;
                impuestoTotal += impuestoRango;

                detalleCalculo.push({
                    rango1: tarifa.rango1,
                    rango2: tarifa.rango2,
                    valorAplicable: valorAplicable,
                    tarifaPorMil: tarifa.valor,
                    impuestoRango: impuestoRango,
                    descripcion: tarifa.descripcion
                });
            }

            return {
                impuestoTotal: Math.round(impuestoTotal * 100) / 100,
                detalleCalculo: detalleCalculo
            };
        }

        function calcularImpuestoUnidadFactor(valorUnidad, valorFactor) {
            // Validar que ambos valores sean mayores a cero
            if (!valorUnidad || valorUnidad <= 0 || !valorFactor || valorFactor <= 0) {
                log('⚠️ Unidad o Factor no válidos - Unidad: ' + valorUnidad + ', Factor: ' + valorFactor);
                return { 
                    impuestoTotal: 0, 
                    detalleCalculo: [], 
                    valorUnidad: valorUnidad || 0, 
                    valorFactor: valorFactor || 0,
                    valorCalculado: 0
                };
            }

            // Multiplicación simple: Factor × Unidad
            const valorCalculado = valorFactor * valorUnidad;
            
            log('🧮 Cálculo Factor × Unidad:');
            log('   Factor: ' + valorFactor);
            log('   Unidad: ' + valorUnidad);
            log('   Resultado: ' + valorFactor + ' × ' + valorUnidad + ' = ' + valorCalculado);

            // Aplicar las mismas tarifas ICS que los otros tipos de venta
            const resultadoICS = calcularImpuestoICS(valorCalculado);
            
            const detalleCalculo = [{
                descripcion: `Factor × Unidad (${valorFactor} × ${valorUnidad})`,
                valorUnidad: valorUnidad,
                valorFactor: valorFactor,
                valorCalculado: valorCalculado,
                impuestoAplicado: resultadoICS.impuestoTotal
            }];

            log('✅ Impuesto calculado para Factor × Unidad: L. ' + resultadoICS.impuestoTotal.toFixed(2));

            return {
                impuestoTotal: resultadoICS.impuestoTotal,
                detalleCalculo: detalleCalculo,
                valorUnidad: valorUnidad,
                valorFactor: valorFactor,
                valorCalculado: valorCalculado
            };
        }

        function calcular() {
            const factor = parseFloat(document.getElementById('factor').value) || 0;
            const unidad = parseInt(document.getElementById('unidad').value) || 0;
            
            // Limpiar logs anteriores
            document.getElementById('logs').innerHTML = '';
            
            log('🚀 Iniciando cálculo...');
            
            const resultado = calcularImpuestoUnidadFactor(unidad, factor);
            
            // Mostrar resultado
            const resultadoDiv = document.getElementById('resultado');
            const detalleDiv = document.getElementById('detalle');
            
            if (resultado.impuestoTotal > 0) {
                resultadoDiv.style.display = 'block';
                detalleDiv.innerHTML = `
                    <p><strong>Factor:</strong> ${resultado.valorFactor}</p>
                    <p><strong>Unidad:</strong> ${resultado.valorUnidad}</p>
                    <p><strong>Valor Calculado:</strong> ${resultado.valorFactor} × ${resultado.valorUnidad} = <span class="highlight">${resultado.valorCalculado}</span></p>
                    <p><strong>Impuesto Calculado:</strong> L. <span class="highlight">${resultado.impuestoTotal.toFixed(2)}</span></p>
                `;
            } else {
                resultadoDiv.style.display = 'block';
                detalleDiv.innerHTML = `
                    <p style="color: #dc3545;"><strong>⚠️ No se puede calcular:</strong> Ambos valores deben ser mayores a 0</p>
                    <p>Factor: ${resultado.valorFactor} | Unidad: ${resultado.valorUnidad}</p>
                `;
            }
        }

        function limpiar() {
            document.getElementById('factor').value = '';
            document.getElementById('unidad').value = '';
            document.getElementById('resultado').style.display = 'none';
            document.getElementById('logs').innerHTML = 'Los logs aparecerán aquí cuando hagas un cálculo...';
        }

        function log(mensaje) {
            console.log(mensaje);
            const logsDiv = document.getElementById('logs');
            const logEntry = document.createElement('div');
            logEntry.className = 'log';
            logEntry.textContent = mensaje;
            logsDiv.appendChild(logEntry);
            logsDiv.scrollTop = logsDiv.scrollHeight;
        }

        // Ejemplo inicial
        document.addEventListener('DOMContentLoaded', function() {
            log('🚀 Sistema de cálculo Factor × Unidad iniciado');
            log('💡 Ingresa valores en Factor y Unidad, luego presiona "Calcular"');
        });
    </script>
</body>
</html>'''
    
    with open('ejemplo_visual_calculo.html', 'w', encoding='utf-8') as f:
        f.write(ejemplo_html)
    
    print("✅ Ejemplo visual creado: ejemplo_visual_calculo.html")

if __name__ == "__main__":
    mostrar_calculo_detallado()
    print()
    crear_ejemplo_visual()
    print("\n🎯 PARA VER EL CÁLCULO EN ACCIÓN:")
    print("1. Abrir 'ejemplo_visual_calculo.html' en el navegador")
    print("2. Ingresar valores en Factor y Unidad")
    print("3. Presionar 'Calcular' para ver el resultado")
    print("4. Observar los logs detallados del cálculo")

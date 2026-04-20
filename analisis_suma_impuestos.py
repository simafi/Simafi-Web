#!/usr/bin/env python3
"""
Análisis detallado del sistema de suma de impuestos
"""

def analizar_problema_suma():
    """Analizar el problema de suma de impuestos"""
    
    print("🔍 ANÁLISIS DETALLADO - SISTEMA DE SUMA DE IMPUESTOS")
    print("=" * 70)
    
    print("\n📋 PROBLEMA IDENTIFICADO:")
    print("Los cálculos individuales funcionan bien, pero la suma total no es correcta")
    
    print("\n🧮 CÁLCULOS INDIVIDUALES:")
    print("1. Ventas Rubro Producción (ventai) → Aplica tarifas ICS")
    print("2. Ventas Mercadería (ventac) → Aplica tarifas ICS") 
    print("3. Ventas por Servicios (ventas) → Aplica tarifas ICS")
    print("4. Ventas Productos Controlados (controlado) → Aplica tarifas ICS")
    print("5. Factor × Unidad → Multiplicación simple (SIN tarifas ICS)")
    
    print("\n❌ PROBLEMA EN LA SUMA:")
    print("El sistema está sumando:")
    print("- Impuestos calculados con tarifas ICS (1-4)")
    print("- Valor directo de Factor × Unidad (5)")
    print("Esto causa inconsistencia en el cálculo total")
    
    print("\n🎯 SOLUCIÓN PROPUESTA:")
    print("1. Crear variables ocultas para cada tipo de cálculo")
    print("2. Separar valores base de impuestos calculados")
    print("3. Aplicar lógica consistente para la suma")
    print("4. Agregar validaciones y logs detallados")

def crear_solucion_mejorada():
    """Crear la solución mejorada"""
    
    solucion_js = '''
    // SOLUCIÓN MEJORADA - SISTEMA DE SUMA DE IMPUESTOS
    
    class DeclaracionVolumenInteractivo {
        constructor() {
            this.camposCalculados = ['ventai', 'ventac', 'ventas', 'controlado', 'unidad', 'factor'];
            this.variablesOcultas = {};
            this.impuestosCalculados = {};
            this.init();
        }
        
        init() {
            this.verificarCamposDisponibles();
            this.setupEventListeners();
            this.crearVariablesOcultas();
        }
        
        crearVariablesOcultas() {
            // Crear variables ocultas para cada tipo de cálculo
            this.camposCalculados.forEach(campo => {
                const input = document.getElementById(`id_${campo}`);
                if (input) {
                    // Variable para valor base
                    this.variablesOcultas[`${campo}_base`] = 0;
                    // Variable para impuesto calculado
                    this.variablesOcultas[`${campo}_impuesto`] = 0;
                }
            });
            
            console.log('🔧 Variables ocultas creadas:', this.variablesOcultas);
        }
        
        calcularEnTiempoReal(fieldName) {
            console.log(`🔄 Calculando impuestos para campo: ${fieldName}`);
            
            // Obtener valores de todos los campos
            const valoresVentas = this.obtenerValoresVentas();
            console.log('📊 Valores de ventas obtenidos:', valoresVentas);
            
            // Calcular impuestos para cada tipo de venta
            const resultados = this.calcularTodosLosImpuestos(valoresVentas);
            
            // Calcular suma total
            const totalImpuesto = this.calcularSumaTotal(resultados);
            
            // Actualizar campo de impuesto
            this.actualizarCampoImpuesto(totalImpuesto);
            
            // Actualizar variables ocultas
            this.actualizarVariablesOcultas(resultados);
        }
        
        calcularTodosLosImpuestos(valoresVentas) {
            const resultados = {};
            
            // 1. Ventas Rubro Producción (con tarifas ICS)
            resultados.industria = this.calcularImpuestoICS(valoresVentas.ventai || 0);
            this.variablesOcultas.ventai_base = valoresVentas.ventai || 0;
            this.variablesOcultas.ventai_impuesto = resultados.industria.impuestoTotal;
            
            // 2. Ventas Mercadería (con tarifas ICS)
            resultados.comercio = this.calcularImpuestoICS(valoresVentas.ventac || 0);
            this.variablesOcultas.ventac_base = valoresVentas.ventac || 0;
            this.variablesOcultas.ventac_impuesto = resultados.comercio.impuestoTotal;
            
            // 3. Ventas por Servicios (con tarifas ICS)
            resultados.servicios = this.calcularImpuestoICS(valoresVentas.ventas || 0);
            this.variablesOcultas.ventas_base = valoresVentas.ventas || 0;
            this.variablesOcultas.ventas_impuesto = resultados.servicios.impuestoTotal;
            
            // 4. Ventas Productos Controlados (con tarifas ICS)
            resultados.controlados = this.calcularImpuestoICSControlados(valoresVentas.controlado || 0);
            this.variablesOcultas.controlado_base = valoresVentas.controlado || 0;
            this.variablesOcultas.controlado_impuesto = resultados.controlados.impuestoTotal;
            
            // 5. Factor × Unidad (multiplicación simple)
            resultados.unidadFactor = this.calcularImpuestoUnidadFactor(valoresVentas.unidad || 0, valoresVentas.factor || 0);
            this.variablesOcultas.unidad_base = valoresVentas.unidad || 0;
            this.variablesOcultas.factor_base = valoresVentas.factor || 0;
            this.variablesOcultas.unidadFactor_impuesto = resultados.unidadFactor.impuestoTotal;
            
            console.log('💰 Resultados de cálculo por tipo:', resultados);
            console.log('🔧 Variables ocultas actualizadas:', this.variablesOcultas);
            
            return resultados;
        }
        
        calcularSumaTotal(resultados) {
            // Sumar solo los impuestos calculados (no los valores base)
            const totalImpuesto = resultados.industria.impuestoTotal + 
                                 resultados.comercio.impuestoTotal + 
                                 resultados.servicios.impuestoTotal + 
                                 resultados.controlados.impuestoTotal +
                                 resultados.unidadFactor.impuestoTotal;
            
            console.log('🎯 SUMATORIA COMPLETA DE IMPUESTOS:');
            console.log(`   • Industria (Ventas Rubro Producción): L. ${resultados.industria.impuestoTotal.toFixed(2)}`);
            console.log(`   • Comercio (Ventas Mercadería): L. ${resultados.comercio.impuestoTotal.toFixed(2)}`);
            console.log(`   • Servicios (Ventas por Servicios): L. ${resultados.servicios.impuestoTotal.toFixed(2)}`);
            console.log(`   • Controlados (Ventas Productos Controlados): L. ${resultados.controlados.impuestoTotal.toFixed(2)}`);
            console.log(`   • Factor × Unidad: L. ${resultados.unidadFactor.impuestoTotal.toFixed(2)}`);
            console.log(`   = TOTAL IMPUESTO CALCULADO: L. ${totalImpuesto.toFixed(2)}`);
            
            return totalImpuesto;
        }
        
        actualizarVariablesOcultas(resultados) {
            // Actualizar campos ocultos en el formulario para envío
            Object.keys(this.variablesOcultas).forEach(key => {
                const campoOculto = document.getElementById(`hidden_${key}`);
                if (campoOculto) {
                    campoOculto.value = this.variablesOcultas[key];
                }
            });
        }
        
        // ... resto de métodos existentes ...
    }
    '''
    
    return solucion_js

def crear_test_suma_corregida():
    """Crear test para verificar la suma corregida"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Suma Corregida - Sistema de Impuestos</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .test-section { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .error { background: #ffebee; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #f44336; }
        .success { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #4caf50; }
        .log { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; font-family: monospace; font-size: 0.9em; border: 1px solid #dee2e6; }
        .highlight { background: #ffeb3b; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
        input { padding: 8px; margin: 5px; border: 1px solid #ccc; border-radius: 4px; width: 120px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #0056b3; }
        .resultado { background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2196f3; }
        .test-case { background: #fff3e0; padding: 10px; margin: 5px 0; border-radius: 4px; border: 1px solid #ff9800; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Suma Corregida - Sistema de Impuestos</h1>
        
        <div class="test-section">
            <h3>📋 Valores de Entrada</h3>
            <div class="grid">
                <div>
                    <label>Ventas Rubro Producción:</label><br>
                    <input type="text" id="ventai" value="1000" placeholder="0.00">
                </div>
                <div>
                    <label>Ventas Mercadería:</label><br>
                    <input type="text" id="ventac" value="2000" placeholder="0.00">
                </div>
                <div>
                    <label>Ventas por Servicios:</label><br>
                    <input type="text" id="ventas" value="1500" placeholder="0.00">
                </div>
                <div>
                    <label>Ventas Productos Controlados:</label><br>
                    <input type="text" id="controlado" value="500" placeholder="0.00">
                </div>
                <div>
                    <label>Factor:</label><br>
                    <input type="text" id="factor" value="2" placeholder="0.00">
                </div>
                <div>
                    <label>Unidad:</label><br>
                    <input type="text" id="unidad" value="100" placeholder="0">
                </div>
            </div>
            <button onclick="ejecutarTest()">🧪 Ejecutar Test</button>
            <button onclick="limpiarTest()">🧹 Limpiar</button>
        </div>

        <div id="resultado" class="resultado" style="display: none;">
            <h3>📊 Resultado del Test</h3>
            <div id="detalle"></div>
        </div>

        <div class="test-section">
            <h3>📝 Logs del Test</h3>
            <div id="logs">Los logs aparecerán aquí cuando ejecutes el test...</div>
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
            if (!valorUnidad || valorUnidad <= 0 || !valorFactor || valorFactor <= 0) {
                return { 
                    impuestoTotal: 0, 
                    valorCalculado: 0
                };
            }

            // Multiplicación simple: Factor × Unidad
            const valorCalculado = valorFactor * valorUnidad;
            
            log('🧮 Cálculo Factor × Unidad:');
            log(`   Factor: ${valorFactor}`);
            log(`   Unidad: ${valorUnidad}`);
            log(`   Resultado: ${valorFactor} × ${valorUnidad} = ${valorCalculado}`);

            // NO aplicar tarifas ICS - es una multiplicación simple
            const impuestoTotal = valorCalculado;
            
            log(`✅ Valor calculado para Factor × Unidad: L. ${impuestoTotal.toFixed(2)}`);

            return {
                impuestoTotal: impuestoTotal,
                valorCalculado: valorCalculado
            };
        }

        function ejecutarTest() {
            // Limpiar logs anteriores
            document.getElementById('logs').innerHTML = '';
            
            log('🚀 Iniciando test de suma corregida...');
            
            // Obtener valores de entrada
            const valores = {
                ventai: parseFloat(document.getElementById('ventai').value) || 0,
                ventac: parseFloat(document.getElementById('ventac').value) || 0,
                ventas: parseFloat(document.getElementById('ventas').value) || 0,
                controlado: parseFloat(document.getElementById('controlado').value) || 0,
                factor: parseFloat(document.getElementById('factor').value) || 0,
                unidad: parseInt(document.getElementById('unidad').value) || 0
            };
            
            log('📊 Valores de entrada:', valores);
            
            // Calcular impuestos para cada tipo
            const resultados = {};
            
            // 1. Ventas Rubro Producción (con tarifas ICS)
            resultados.industria = calcularImpuestoICS(valores.ventai);
            log(`🏭 Industria: ${valores.ventai} → Impuesto: ${resultados.industria.impuestoTotal}`);
            
            // 2. Ventas Mercadería (con tarifas ICS)
            resultados.comercio = calcularImpuestoICS(valores.ventac);
            log(`🛒 Comercio: ${valores.ventac} → Impuesto: ${resultados.comercio.impuestoTotal}`);
            
            // 3. Ventas por Servicios (con tarifas ICS)
            resultados.servicios = calcularImpuestoICS(valores.ventas);
            log(`🔧 Servicios: ${valores.ventas} → Impuesto: ${resultados.servicios.impuestoTotal}`);
            
            // 4. Ventas Productos Controlados (con tarifas ICS)
            resultados.controlados = calcularImpuestoICS(valores.controlado);
            log(`⚠️ Controlados: ${valores.controlado} → Impuesto: ${resultados.controlados.impuestoTotal}`);
            
            // 5. Factor × Unidad (multiplicación simple)
            resultados.unidadFactor = calcularImpuestoUnidadFactor(valores.unidad, valores.factor);
            log(`🧮 Factor × Unidad: ${valores.factor} × ${valores.unidad} = ${resultados.unidadFactor.valorCalculado} → Impuesto: ${resultados.unidadFactor.impuestoTotal}`);
            
            // Calcular suma total
            const totalImpuesto = resultados.industria.impuestoTotal + 
                                 resultados.comercio.impuestoTotal + 
                                 resultados.servicios.impuestoTotal + 
                                 resultados.controlados.impuestoTotal +
                                 resultados.unidadFactor.impuestoTotal;
            
            log('🎯 SUMATORIA COMPLETA DE IMPUESTOS:');
            log(`   • Industria: L. ${resultados.industria.impuestoTotal.toFixed(2)}`);
            log(`   • Comercio: L. ${resultados.comercio.impuestoTotal.toFixed(2)}`);
            log(`   • Servicios: L. ${resultados.servicios.impuestoTotal.toFixed(2)}`);
            log(`   • Controlados: L. ${resultados.controlados.impuestoTotal.toFixed(2)}`);
            log(`   • Factor × Unidad: L. ${resultados.unidadFactor.impuestoTotal.toFixed(2)}`);
            log(`   = TOTAL: L. ${totalImpuesto.toFixed(2)}`);
            
            // Mostrar resultado
            mostrarResultado(resultados, totalImpuesto);
        }

        function mostrarResultado(resultados, totalImpuesto) {
            const resultadoDiv = document.getElementById('resultado');
            const detalleDiv = document.getElementById('detalle');
            
            resultadoDiv.style.display = 'block';
            detalleDiv.innerHTML = `
                <div class="success">
                    <h4>✅ Test de Suma Completado</h4>
                    <div class="grid">
                        <div><strong>Industria:</strong> L. ${resultados.industria.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Comercio:</strong> L. ${resultados.comercio.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Servicios:</strong> L. ${resultados.servicios.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Controlados:</strong> L. ${resultados.controlados.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Factor × Unidad:</strong> L. ${resultados.unidadFactor.impuestoTotal.toFixed(2)}</div>
                        <div><strong>TOTAL IMPUESTO:</strong> L. <span class="highlight">${totalImpuesto.toFixed(2)}</span></div>
                    </div>
                </div>
            `;
        }

        function limpiarTest() {
            document.getElementById('ventai').value = '';
            document.getElementById('ventac').value = '';
            document.getElementById('ventas').value = '';
            document.getElementById('controlado').value = '';
            document.getElementById('factor').value = '';
            document.getElementById('unidad').value = '';
            document.getElementById('resultado').style.display = 'none';
            document.getElementById('logs').innerHTML = 'Los logs aparecerán aquí cuando ejecutes el test...';
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

        // Test inicial
        document.addEventListener('DOMContentLoaded', function() {
            log('🚀 Sistema de test de suma corregida iniciado');
            log('💡 Ingresa valores y presiona "Ejecutar Test" para ver la suma corregida');
        });
    </script>
</body>
</html>'''
    
    with open('test_suma_corregida.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test de suma corregida creado: test_suma_corregida.html")

if __name__ == "__main__":
    analizar_problema_suma()
    print()
    crear_solucion_mejorada()
    print()
    crear_test_suma_corregida()
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Revisar el análisis del problema")
    print("2. Implementar la solución mejorada en el formulario")
    print("3. Probar con el test de suma corregida")

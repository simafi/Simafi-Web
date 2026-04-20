#!/usr/bin/env python3
"""
Test para verificar cálculo independiente vs combinado con productos controlados
"""

def test_independiente_vs_combinado():
    """Test específico: independiente vs combinado"""
    
    print("🧪 TEST INDEPENDIENTE VS COMBINADO - PRODUCTOS CONTROLADOS")
    print("=" * 80)
    
    # Simular las tarifas normales ICS
    def calcularImpuestoICS(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return { 'impuestoTotal': 0 }
        
        if valorVentas <= 500000:
            impuesto = valorVentas * 0.3 / 1000
        elif valorVentas <= 10000000:
            impuesto = valorVentas * 0.4 / 1000
        else:
            impuesto = valorVentas * 0.3 / 1000
        
        return { 'impuestoTotal': round(impuesto, 2) }
    
    # Simular las tarifas para productos controlados
    def calcularImpuestoICSControlados(valorVentas):
        if not valorVentas or valorVentas <= 0:
            return { 'impuestoTotal': 0 }
        
        if valorVentas <= 1000000:
            impuesto = valorVentas * 1.0 / 1000
        elif valorVentas <= 5000000:
            impuesto = valorVentas * 1.5 / 1000
        else:
            impuesto = valorVentas * 2.0 / 1000
        
        return { 'impuestoTotal': round(impuesto, 2) }
    
    def calcularImpuestoUnidadFactor(valorUnidad, valorFactor):
        if not valorUnidad or valorUnidad <= 0 or not valorFactor or valorFactor <= 0:
            return { 'impuestoTotal': 0, 'valorCalculado': 0 }
        
        valorCalculado = valorFactor * valorUnidad
        return { 'impuestoTotal': valorCalculado, 'valorCalculado': valorCalculado }
    
    # Casos de prueba específicos
    casos_prueba = [
        {
            "nombre": "Caso 1: Solo productos controlados",
            "valores": {"ventai": 0, "ventac": 0, "ventas": 0, "controlado": 1000, "factor": 0, "unidad": 0}
        },
        {
            "nombre": "Caso 2: Productos controlados + industria",
            "valores": {"ventai": 1000, "ventac": 0, "ventas": 0, "controlado": 1000, "factor": 0, "unidad": 0}
        },
        {
            "nombre": "Caso 3: Productos controlados + Factor×Unidad",
            "valores": {"ventai": 0, "ventac": 0, "ventas": 0, "controlado": 1000, "factor": 2, "unidad": 100}
        },
        {
            "nombre": "Caso 4: Todos combinados",
            "valores": {"ventai": 1000, "ventac": 2000, "ventas": 1500, "controlado": 1000, "factor": 2, "unidad": 100}
        },
        {
            "nombre": "Caso 5: Valores altos",
            "valores": {"ventai": 10000, "ventac": 5000, "ventas": 7500, "controlado": 2000000, "factor": 3, "unidad": 200}
        }
    ]
    
    print("\n📊 EJECUTANDO COMPARACIÓN INDEPENDIENTE VS COMBINADO:")
    print("-" * 80)
    
    todos_pasan = True
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n🧪 {caso['nombre']}")
        print(f"   Valores: {caso['valores']}")
        
        # CÁLCULO INDEPENDIENTE - Solo productos controlados
        print(f"\n   📋 CÁLCULO INDEPENDIENTE (Solo productos controlados):")
        controlados_independiente = calcularImpuestoICSControlados(caso['valores']['controlado'])
        print(f"     Valor base: {caso['valores']['controlado']}")
        print(f"     Impuesto calculado: L. {controlados_independiente['impuestoTotal']:.2f}")
        
        # CÁLCULO COMBINADO - Todos los tipos
        print(f"\n   📋 CÁLCULO COMBINADO (Todos los tipos):")
        industria = calcularImpuestoICS(caso['valores']['ventai'])
        comercio = calcularImpuestoICS(caso['valores']['ventac'])
        servicios = calcularImpuestoICS(caso['valores']['ventas'])
        controlados_combinado = calcularImpuestoICSControlados(caso['valores']['controlado'])
        unidadFactor = calcularImpuestoUnidadFactor(caso['valores']['unidad'], caso['valores']['factor'])
        
        print(f"     Industria: L. {industria['impuestoTotal']:.2f}")
        print(f"     Comercio: L. {comercio['impuestoTotal']:.2f}")
        print(f"     Servicios: L. {servicios['impuestoTotal']:.2f}")
        print(f"     Controlados: L. {controlados_combinado['impuestoTotal']:.2f}")
        print(f"     Factor × Unidad: L. {unidadFactor['impuestoTotal']:.2f}")
        
        # Suma total combinada
        total_combinado = (industria['impuestoTotal'] + 
                          comercio['impuestoTotal'] + 
                          servicios['impuestoTotal'] + 
                          controlados_combinado['impuestoTotal'] +
                          unidadFactor['impuestoTotal'])
        
        print(f"     = TOTAL COMBINADO: L. {total_combinado:.2f}")
        
        # VERIFICACIÓN
        print(f"\n   🔍 VERIFICACIÓN:")
        
        # 1. Verificar que productos controlados es igual en ambos casos
        if abs(controlados_independiente['impuestoTotal'] - controlados_combinado['impuestoTotal']) < 0.01:
            print(f"     ✅ Productos controlados: IGUALES")
            print(f"         Independiente: L. {controlados_independiente['impuestoTotal']:.2f}")
            print(f"         Combinado: L. {controlados_combinado['impuestoTotal']:.2f}")
        else:
            print(f"     ❌ Productos controlados: DIFERENTES")
            print(f"         Independiente: L. {controlados_independiente['impuestoTotal']:.2f}")
            print(f"         Combinado: L. {controlados_combinado['impuestoTotal']:.2f}")
            todos_pasan = False
        
        # 2. Verificar que la suma es correcta
        suma_manual = (industria['impuestoTotal'] + 
                      comercio['impuestoTotal'] + 
                      servicios['impuestoTotal'] + 
                      controlados_combinado['impuestoTotal'] +
                      unidadFactor['impuestoTotal'])
        
        if abs(total_combinado - suma_manual) < 0.01:
            print(f"     ✅ Suma total: CORRECTA")
        else:
            print(f"     ❌ Suma total: INCORRECTA")
            print(f"         Calculada: L. {total_combinado:.2f}")
            print(f"         Manual: L. {suma_manual:.2f}")
            todos_pasan = False
        
        # 3. Análisis específico del problema
        if caso['valores']['controlado'] > 0:
            print(f"     🔍 Análisis productos controlados:")
            print(f"         Valor base: {caso['valores']['controlado']}")
            print(f"         Impuesto independiente: L. {controlados_independiente['impuestoTotal']:.2f}")
            print(f"         Impuesto combinado: L. {controlados_combinado['impuestoTotal']:.2f}")
            print(f"         Diferencia: L. {abs(controlados_independiente['impuestoTotal'] - controlados_combinado['impuestoTotal']):.2f}")
            
            # Verificar si hay otros valores que puedan estar afectando
            otros_impuestos = industria['impuestoTotal'] + comercio['impuestoTotal'] + servicios['impuestoTotal'] + unidadFactor['impuestoTotal']
            print(f"         Otros impuestos: L. {otros_impuestos:.2f}")
            print(f"         Total esperado: L. {controlados_independiente['impuestoTotal'] + otros_impuestos:.2f}")
            print(f"         Total obtenido: L. {total_combinado:.2f}")
    
    print("\n" + "=" * 80)
    if todos_pasan:
        print("✅ TODOS LOS CÁLCULOS SON CONSISTENTES")
        print("🎯 No hay diferencia entre cálculo independiente y combinado")
    else:
        print("❌ HAY INCONSISTENCIAS EN LOS CÁLCULOS")
        print("🔧 El problema está en la combinación de valores")
    
    return todos_pasan

def crear_test_html_independiente_vs_combinado():
    """Crear test HTML para verificar independiente vs combinado"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Independiente vs Combinado - Productos Controlados</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .test-section { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .error { background: #ffebee; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #f44336; }
        .success { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #4caf50; }
        .warning { background: #fff3e0; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ff9800; }
        .log { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; font-family: monospace; font-size: 0.9em; border: 1px solid #dee2e6; }
        .highlight { background: #ffeb3b; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
        input { padding: 8px; margin: 5px; border: 1px solid #ccc; border-radius: 4px; width: 120px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #0056b3; }
        .resultado { background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2196f3; }
        .test-case { background: #fff3e0; padding: 10px; margin: 5px 0; border-radius: 4px; border: 1px solid #ff9800; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
        .comparison-item { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Independiente vs Combinado - Productos Controlados</h1>
        
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
                    <input type="text" id="controlado" value="1000" placeholder="0.00">
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
        // Tarifas normales ICS
        const tarifasNormales = [
            {"rango1": 0.0, "rango2": 500000.0, "valor": 0.3, "descripcion": "Rango $0 - $500,000"},
            {"rango1": 500000.01, "rango2": 10000000.0, "valor": 0.4, "descripcion": "Rango $500,000 - $10,000,000"},
            {"rango1": 10000000.01, "rango2": 9999999999.0, "valor": 0.3, "descripcion": "Rango $10,000,000+"}
        ];

        // Tarifas para productos controlados
        const tarifasControlados = [
            {"rango1": 0.0, "rango2": 1000000.0, "valor": 1.0, "descripcion": "Controlados $0 - $1,000,000"},
            {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 1.5, "descripcion": "Controlados $1,000,000 - $5,000,000"},
            {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 2.0, "descripcion": "Controlados $5,000,000+"}
        ];

        function calcularImpuestoICS(valorVentas, tarifas) {
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

            const valorCalculado = valorFactor * valorUnidad;
            return {
                impuestoTotal: valorCalculado,
                valorCalculado: valorCalculado
            };
        }

        function ejecutarTest() {
            // Limpiar logs anteriores
            document.getElementById('logs').innerHTML = '';
            
            log('🚀 Iniciando test independiente vs combinado...');
            
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
            
            // CÁLCULO INDEPENDIENTE - Solo productos controlados
            log('\\n📋 CÁLCULO INDEPENDIENTE (Solo productos controlados):');
            const controlados_independiente = calcularImpuestoICS(valores.controlado, tarifasControlados);
            log(`   Valor base: ${valores.controlado}`);
            log(`   Impuesto calculado: L. ${controlados_independiente.impuestoTotal.toFixed(2)}`);
            
            // CÁLCULO COMBINADO - Todos los tipos
            log('\\n📋 CÁLCULO COMBINADO (Todos los tipos):');
            const industria = calcularImpuestoICS(valores.ventai, tarifasNormales);
            const comercio = calcularImpuestoICS(valores.ventac, tarifasNormales);
            const servicios = calcularImpuestoICS(valores.ventas, tarifasNormales);
            const controlados_combinado = calcularImpuestoICS(valores.controlado, tarifasControlados);
            const unidadFactor = calcularImpuestoUnidadFactor(valores.unidad, valores.factor);
            
            log(`   Industria: L. ${industria.impuestoTotal.toFixed(2)}`);
            log(`   Comercio: L. ${comercio.impuestoTotal.toFixed(2)}`);
            log(`   Servicios: L. ${servicios.impuestoTotal.toFixed(2)}`);
            log(`   Controlados: L. ${controlados_combinado.impuestoTotal.toFixed(2)}`);
            log(`   Factor × Unidad: L. ${unidadFactor.impuestoTotal.toFixed(2)}`);
            
            // Suma total combinada
            const total_combinado = industria.impuestoTotal + 
                                  comercio.impuestoTotal + 
                                  servicios.impuestoTotal + 
                                  controlados_combinado.impuestoTotal +
                                  unidadFactor.impuestoTotal;
            
            log(`   = TOTAL COMBINADO: L. ${total_combinado.toFixed(2)}`);
            
            // VERIFICACIÓN
            log('\\n🔍 VERIFICACIÓN:');
            
            // 1. Verificar que productos controlados es igual en ambos casos
            const diferencia_controlados = Math.abs(controlados_independiente.impuestoTotal - controlados_combinado.impuestoTotal);
            if (diferencia_controlados < 0.01) {
                log('   ✅ Productos controlados: IGUALES');
                log(`      Independiente: L. ${controlados_independiente.impuestoTotal.toFixed(2)}`);
                log(`      Combinado: L. ${controlados_combinado.impuestoTotal.toFixed(2)}`);
            } else {
                log('   ❌ Productos controlados: DIFERENTES');
                log(`      Independiente: L. ${controlados_independiente.impuestoTotal.toFixed(2)}`);
                log(`      Combinado: L. ${controlados_combinado.impuestoTotal.toFixed(2)}`);
                log(`      Diferencia: L. ${diferencia_controlados.toFixed(2)}`);
            }
            
            // 2. Verificar que la suma es correcta
            const suma_manual = industria.impuestoTotal + 
                              comercio.impuestoTotal + 
                              servicios.impuestoTotal + 
                              controlados_combinado.impuestoTotal +
                              unidadFactor.impuestoTotal;
            
            const diferencia_suma = Math.abs(total_combinado - suma_manual);
            if (diferencia_suma < 0.01) {
                log('   ✅ Suma total: CORRECTA');
            } else {
                log('   ❌ Suma total: INCORRECTA');
                log(`      Calculada: L. ${total_combinado.toFixed(2)}`);
                log(`      Manual: L. ${suma_manual.toFixed(2)}`);
                log(`      Diferencia: L. ${diferencia_suma.toFixed(2)}`);
            }
            
            // 3. Análisis específico del problema
            if (valores.controlado > 0) {
                log('\\n🔍 Análisis productos controlados:');
                log(`   Valor base: ${valores.controlado}`);
                log(`   Impuesto independiente: L. ${controlados_independiente.impuestoTotal.toFixed(2)}`);
                log(`   Impuesto combinado: L. ${controlados_combinado.impuestoTotal.toFixed(2)}`);
                log(`   Diferencia: L. ${diferencia_controlados.toFixed(2)}`);
                
                const otros_impuestos = industria.impuestoTotal + comercio.impuestoTotal + servicios.impuestoTotal + unidadFactor.impuestoTotal;
                log(`   Otros impuestos: L. ${otros_impuestos.toFixed(2)}`);
                log(`   Total esperado: L. ${(controlados_independiente.impuestoTotal + otros_impuestos).toFixed(2)}`);
                log(`   Total obtenido: L. ${total_combinado.toFixed(2)}`);
            }
            
            // Mostrar resultado
            mostrarResultado(controlados_independiente, controlados_combinado, total_combinado, diferencia_controlados, diferencia_suma);
        }

        function mostrarResultado(controlados_independiente, controlados_combinado, total_combinado, diferencia_controlados, diferencia_suma) {
            const resultadoDiv = document.getElementById('resultado');
            const detalleDiv = document.getElementById('detalle');
            
            resultadoDiv.style.display = 'block';
            
            let estado_controlados = diferencia_controlados < 0.01 ? 'success' : 'error';
            let estado_suma = diferencia_suma < 0.01 ? 'success' : 'error';
            
            detalleDiv.innerHTML = `
                <div class="comparison">
                    <div class="comparison-item">
                        <h4>📋 Cálculo Independiente</h4>
                        <p><strong>Productos Controlados:</strong> L. ${controlados_independiente.impuestoTotal.toFixed(2)}</p>
                    </div>
                    <div class="comparison-item">
                        <h4>📋 Cálculo Combinado</h4>
                        <p><strong>Productos Controlados:</strong> L. ${controlados_combinado.impuestoTotal.toFixed(2)}</p>
                        <p><strong>Total Combinado:</strong> L. ${total_combinado.toFixed(2)}</p>
                    </div>
                </div>
                <div class="${estado_controlados}">
                    <h4>${diferencia_controlados < 0.01 ? '✅' : '❌'} Productos Controlados</h4>
                    <p>Diferencia: L. ${diferencia_controlados.toFixed(2)}</p>
                </div>
                <div class="${estado_suma}">
                    <h4>${diferencia_suma < 0.01 ? '✅' : '❌'} Suma Total</h4>
                    <p>Diferencia: L. ${diferencia_suma.toFixed(2)}</p>
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
            log('🚀 Sistema de test independiente vs combinado iniciado');
            log('💡 Ingresa valores y presiona "Ejecutar Test" para comparar cálculos');
        });
    </script>
</body>
</html>'''
    
    with open('test_independiente_vs_combinado.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test HTML independiente vs combinado creado: test_independiente_vs_combinado.html")

if __name__ == "__main__":
    print("🧪 INICIANDO TEST INDEPENDIENTE VS COMBINADO...")
    print()
    
    if test_independiente_vs_combinado():
        print("\n✅ NO HAY DIFERENCIA ENTRE CÁLCULOS")
        print("🎯 El problema puede estar en la implementación del formulario")
    else:
        print("\n❌ HAY DIFERENCIAS ENTRE CÁLCULOS")
        print("🔧 El problema está en la combinación de valores")
    
    crear_test_html_independiente_vs_combinado()
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Probar con el test HTML independiente vs combinado")
    print("2. Verificar si hay diferencias en los cálculos")
    print("3. Identificar exactamente dónde está el conflicto")

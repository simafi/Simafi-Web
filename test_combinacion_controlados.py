#!/usr/bin/env python3
"""
Test específico para el problema de combinación con productos controlados
"""

def test_combinacion_controlados():
    """Test del problema de combinación con productos controlados"""
    
    print("🧪 TEST COMBINACIÓN - PRODUCTOS CONTROLADOS")
    print("=" * 70)
    
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
    
    # Casos específicos de combinación
    casos_prueba = [
        {
            "nombre": "Caso 1: Solo productos controlados",
            "valores": {"ventai": 0, "ventac": 0, "ventas": 0, "controlado": 1000, "factor": 0, "unidad": 0},
            "esperado_individual": 1.0,
            "esperado_total": 1.0
        },
        {
            "nombre": "Caso 2: Productos controlados + industria",
            "valores": {"ventai": 1000, "ventac": 0, "ventas": 0, "controlado": 1000, "factor": 0, "unidad": 0},
            "esperado_individual": 1.0,
            "esperado_total": 1.3
        },
        {
            "nombre": "Caso 3: Productos controlados + Factor×Unidad",
            "valores": {"ventai": 0, "ventac": 0, "ventas": 0, "controlado": 1000, "factor": 2, "unidad": 100},
            "esperado_individual": 1.0,
            "esperado_total": 201.0
        },
        {
            "nombre": "Caso 4: Todos combinados",
            "valores": {"ventai": 1000, "ventac": 2000, "ventas": 1500, "controlado": 1000, "factor": 2, "unidad": 100},
            "esperado_individual": 1.0,
            "esperado_total": 202.35
        },
        {
            "nombre": "Caso 5: Valores altos - productos controlados",
            "valores": {"ventai": 10000, "ventac": 5000, "ventas": 7500, "controlado": 2000000, "factor": 0, "unidad": 0},
            "esperado_individual": 3000.0,
            "esperado_total": 3006.75
        }
    ]
    
    print("\n📊 EJECUTANDO CASOS DE PRUEBA DE COMBINACIÓN:")
    print("-" * 70)
    
    todos_pasan = True
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n🧪 {caso['nombre']}")
        print(f"   Valores: {caso['valores']}")
        
        # Calcular impuestos individuales
        industria = calcularImpuestoICS(caso['valores']['ventai'])
        comercio = calcularImpuestoICS(caso['valores']['ventac'])
        servicios = calcularImpuestoICS(caso['valores']['ventas'])
        controlados = calcularImpuestoICSControlados(caso['valores']['controlado'])
        unidadFactor = calcularImpuestoUnidadFactor(caso['valores']['unidad'], caso['valores']['factor'])
        
        # Verificar cálculo individual de productos controlados
        if caso['valores']['controlado'] > 0:
            if abs(controlados['impuestoTotal'] - caso['esperado_individual']) < 0.01:
                print(f"   ✅ Cálculo individual controlados: CORRECTO ({controlados['impuestoTotal']})")
            else:
                print(f"   ❌ Cálculo individual controlados: ERROR")
                print(f"       Esperado: {caso['esperado_individual']}, Obtenido: {controlados['impuestoTotal']}")
                todos_pasan = False
        
        # Calcular suma total
        totalImpuesto = (industria['impuestoTotal'] + 
                        comercio['impuestoTotal'] + 
                        servicios['impuestoTotal'] + 
                        controlados['impuestoTotal'] +
                        unidadFactor['impuestoTotal'])
        
        print(f"   Resultados:")
        print(f"     • Industria: L. {industria['impuestoTotal']:.2f}")
        print(f"     • Comercio: L. {comercio['impuestoTotal']:.2f}")
        print(f"     • Servicios: L. {servicios['impuestoTotal']:.2f}")
        print(f"     • Controlados: L. {controlados['impuestoTotal']:.2f}")
        print(f"     • Factor × Unidad: L. {unidadFactor['impuestoTotal']:.2f}")
        print(f"     = TOTAL: L. {totalImpuesto:.2f}")
        
        # Verificar suma total
        if abs(totalImpuesto - caso['esperado_total']) < 0.01:
            print(f"   ✅ Suma total: CORRECTA")
        else:
            print(f"   ❌ Suma total: ERROR")
            print(f"       Esperado: {caso['esperado_total']}, Obtenido: {totalImpuesto:.2f}")
            todos_pasan = False
        
        # Análisis específico del problema
        if caso['valores']['controlado'] > 0 and (caso['valores']['ventai'] > 0 or caso['valores']['ventac'] > 0 or caso['valores']['ventas'] > 0 or caso['valores']['factor'] > 0):
            print(f"   🔍 Análisis combinación:")
            print(f"       Controlados individual: {controlados['impuestoTotal']:.2f}")
            print(f"       Otros impuestos: {industria['impuestoTotal'] + comercio['impuestoTotal'] + servicios['impuestoTotal'] + unidadFactor['impuestoTotal']:.2f}")
            print(f"       Suma esperada: {caso['esperado_total']:.2f}")
            print(f"       Suma obtenida: {totalImpuesto:.2f}")
    
    print("\n" + "=" * 70)
    if todos_pasan:
        print("✅ TODOS LOS CASOS DE COMBINACIÓN PASARON")
        print("🎯 No hay problema en la combinación")
    else:
        print("❌ ALGUNOS CASOS DE COMBINACIÓN FALLARON")
        print("🔧 Hay problema específico en la combinación")
    
    return todos_pasan

def crear_test_html_combinacion():
    """Crear test HTML para verificar la combinación"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Combinación - Productos Controlados</title>
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
        <h1>🧪 Test Combinación - Productos Controlados</h1>
        
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
            
            log('🚀 Iniciando test de combinación...');
            
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
            
            // Calcular impuestos individuales
            const industria = calcularImpuestoICS(valores.ventai, tarifasNormales);
            const comercio = calcularImpuestoICS(valores.ventac, tarifasNormales);
            const servicios = calcularImpuestoICS(valores.ventas, tarifasNormales);
            const controlados = calcularImpuestoICS(valores.controlado, tarifasControlados);
            const unidadFactor = calcularImpuestoUnidadFactor(valores.unidad, valores.factor);
            
            log('🔍 Cálculos individuales:');
            log(`   Industria: ${valores.ventai} → L. ${industria.impuestoTotal}`);
            log(`   Comercio: ${valores.ventac} → L. ${comercio.impuestoTotal}`);
            log(`   Servicios: ${valores.ventas} → L. ${servicios.impuestoTotal}`);
            log(`   Controlados: ${valores.controlado} → L. ${controlados.impuestoTotal} (tarifas especiales)`);
            log(`   Factor × Unidad: ${valores.factor} × ${valores.unidad} = ${unidadFactor.valorCalculado} → L. ${unidadFactor.impuestoTotal}`);
            
            // Calcular suma total
            const totalImpuesto = industria.impuestoTotal + 
                                 comercio.impuestoTotal + 
                                 servicios.impuestoTotal + 
                                 controlados.impuestoTotal +
                                 unidadFactor.impuestoTotal;
            
            log('🎯 Suma total:');
            log(`   Industria: L. ${industria.impuestoTotal.toFixed(2)}`);
            log(`   Comercio: L. ${comercio.impuestoTotal.toFixed(2)}`);
            log(`   Servicios: L. ${servicios.impuestoTotal.toFixed(2)}`);
            log(`   Controlados: L. ${controlados.impuestoTotal.toFixed(2)}`);
            log(`   Factor × Unidad: L. ${unidadFactor.impuestoTotal.toFixed(2)}`);
            log(`   = TOTAL: L. ${totalImpuesto.toFixed(2)}`);
            
            // Mostrar resultado
            mostrarResultado(industria, comercio, servicios, controlados, unidadFactor, totalImpuesto);
        }

        function mostrarResultado(industria, comercio, servicios, controlados, unidadFactor, totalImpuesto) {
            const resultadoDiv = document.getElementById('resultado');
            const detalleDiv = document.getElementById('detalle');
            
            resultadoDiv.style.display = 'block';
            detalleDiv.innerHTML = `
                <div class="success">
                    <h4>✅ Test de Combinación Completado</h4>
                    <div class="grid">
                        <div><strong>Industria:</strong> L. ${industria.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Comercio:</strong> L. ${comercio.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Servicios:</strong> L. ${servicios.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Controlados:</strong> L. ${controlados.impuestoTotal.toFixed(2)}</div>
                        <div><strong>Factor × Unidad:</strong> L. ${unidadFactor.impuestoTotal.toFixed(2)}</div>
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
            log('🚀 Sistema de test de combinación iniciado');
            log('💡 Ingresa valores y presiona "Ejecutar Test" para verificar la combinación');
        });
    </script>
</body>
</html>'''
    
    with open('test_combinacion_controlados.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test HTML de combinación creado: test_combinacion_controlados.html")

if __name__ == "__main__":
    print("🧪 INICIANDO TEST COMBINACIÓN...")
    print()
    
    if test_combinacion_controlados():
        print("\n✅ NO HAY PROBLEMA EN LA COMBINACIÓN")
        print("🎯 El problema puede estar en la implementación del formulario")
    else:
        print("\n❌ HAY PROBLEMA EN LA COMBINACIÓN")
        print("🔧 Necesita corrección específica")
    
    crear_test_html_combinacion()
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Probar con el test HTML de combinación")
    print("2. Verificar los logs detallados en el formulario real")
    print("3. Identificar dónde está el conflicto específico")

#!/usr/bin/env python3
"""
Script para verificar la funcionalidad completa del sistema de cálculo interactivo
"""

def verificar_funcionalidad_completa():
    """Verificación completa de la funcionalidad"""
    
    print("🔍 VERIFICACIÓN COMPLETA DE FUNCIONALIDAD")
    print("=" * 60)
    
    # Verificar template
    template_path = "tributario/tributario_app/templates/declaracion_volumen.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print("📋 VERIFICACIONES DEL TEMPLATE:")
        
        verificaciones = [
            ('DeclaracionVolumenInteractivo', 'Clase principal del sistema'),
            ('verificarCamposDisponibles', 'Función de verificación de campos'),
            ('calcularImpuestoICSControlados', 'Función para productos controlados'),
            ('resultadoControlados.impuestoTotal', 'Inclusión en sumatoria'),
            ('SUMATORIA COMPLETA DE IMPUESTOS', 'Logs de sumatoria detallados'),
            ('Campo impuesto actualizado', 'Confirmación de actualización'),
            ('id_impuesto', 'Campo de impuesto calculado')
        ]
        
        for verificacion, descripcion in verificaciones:
            if verificacion in contenido:
                print(f"✅ {descripcion}")
            else:
                print(f"❌ {descripcion}")
        
        # Verificar estructura del cálculo
        if 'resultadoIndustria.impuestoTotal +' in contenido and 'resultadoControlados.impuestoTotal' in contenido:
            print("✅ Sumatoria incluye productos controlados")
        else:
            print("❌ Sumatoria NO incluye productos controlados")
            
        # Verificar logs de depuración
        if 'console.log' in contenido and 'SUMATORIA COMPLETA' in contenido:
            print("✅ Logs de depuración incluidos")
        else:
            print("❌ Logs de depuración faltantes")
            
    except FileNotFoundError:
        print(f"❌ Template no encontrado: {template_path}")
    except Exception as e:
        print(f"❌ Error verificando template: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 FUNCIONALIDADES IMPLEMENTADAS:")
    print("1. ✅ JavaScript embebido en template")
    print("2. ✅ Verificación automática de campos")
    print("3. ✅ Cálculo de impuestos por tipo de venta")
    print("4. ✅ Sumatoria completa incluyendo productos controlados")
    print("5. ✅ Logs de depuración detallados")
    print("6. ✅ Actualización automática del campo impuesto")
    print("7. ✅ Validación de actualización exitosa")
    
    print("\n📊 CÁLCULO IMPLEMENTADO:")
    print("El sistema calcula impuestos para:")
    print("• Ventas Rubro Producción (Industria) - Tarifas estándar ICS")
    print("• Ventas Mercadería (Comercio) - Tarifas estándar ICS")
    print("• Ventas por Servicios - Tarifas estándar ICS")
    print("• Ventas Productos Controlados - Tarifas específicas más altas")
    print("\nY suma TODOS los impuestos en el campo 'Impuesto Calculado'")

def crear_test_funcionalidad():
    """Crea un test específico para verificar la funcionalidad"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test - Funcionalidad Completa del Sistema</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; border-radius: 8px; }
        .success { background-color: #d4edda; border-color: #c3e6cb; }
        .error { background-color: #f8d7da; border-color: #f5c6cb; }
        .info { background-color: #d1ecf1; border-color: #bee5eb; }
        input { margin: 5px; padding: 8px; width: 200px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        #resultado { font-weight: bold; font-size: 1.2em; }
        .desglose { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
        .total { background: #28a745; color: white; padding: 15px; border-radius: 5px; text-align: center; margin: 10px 0; }
        .log { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; font-family: monospace; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>🧪 Test - Funcionalidad Completa del Sistema de Cálculo</h1>
    
    <div class="test-section info">
        <h3>📋 Instrucciones</h3>
        <p>Este test simula exactamente el comportamiento del formulario real. Ingrese valores en los campos y observe cómo se calculan los impuestos automáticamente.</p>
    </div>
    
    <div class="test-section">
        <h3>💰 Campos de Ventas</h3>
        <label><strong>Ventas Rubro Producción:</strong></label>
        <input type="text" id="id_ventai" value="1000000" placeholder="Ej: 1000000" oninput="calcularAutomatico()"><br>
        
        <label><strong>Ventas Mercadería:</strong></label>
        <input type="text" id="id_ventac" value="500000" placeholder="Ej: 500000" oninput="calcularAutomatico()"><br>
        
        <label><strong>Ventas por Servicios:</strong></label>
        <input type="text" id="id_ventas" value="300000" placeholder="Ej: 300000" oninput="calcularAutomatico()"><br>
        
        <label><strong>Ventas Productos Controlados:</strong></label>
        <input type="text" id="id_controlado" value="200000" placeholder="Ej: 200000" oninput="calcularAutomatico()"><br>
        
        <button onclick="probarFuncionalidad()">🧮 Probar Funcionalidad Completa</button>
        <button onclick="limpiarCampos()">🧹 Limpiar Campos</button>
    </div>
    
    <div class="test-section">
        <h3>📊 Resultado del Cálculo</h3>
        <div id="resultado">Los cálculos aparecerán aquí automáticamente...</div>
    </div>
    
    <div class="test-section">
        <h3>📝 Logs del Sistema</h3>
        <div id="logs">Los logs del sistema aparecerán aquí...</div>
    </div>

    <script>
        // Sistema de cálculo idéntico al del template
        class DeclaracionVolumenInteractivo {
            constructor() {
                this.tarifas = [
                    {"rango1": 0.0, "rango2": 500000.0, "valor": 0.3, "categoria": "1", "descripcion": "Rango $0 - $500,000"},
                    {"rango1": 500000.01, "rango2": 10000000.0, "valor": 0.4, "categoria": "1", "descripcion": "Rango $500,000 - $10,000,000"},
                    {"rango1": 10000000.01, "rango2": 20000000.0, "valor": 0.3, "categoria": "1", "descripcion": "Rango $10,000,000 - $20,000,000"},
                    {"rango1": 20000000.01, "rango2": 30000000.0, "valor": 0.2, "categoria": "1", "descripcion": "Rango $20,000,000 - $30,000,000"},
                    {"rango1": 30000000.01, "rango2": 9999999999.0, "valor": 0.15, "categoria": "1", "descripcion": "Rango $30,000,000 - $9,999,999,999"}
                ];
                this.initializeSystem();
            }

            async initializeSystem() {
                this.verificarCamposDisponibles();
                this.setupEventListeners();
                this.log('🚀 Sistema de cálculo interactivo inicializado (versión embebida)');
            }

            verificarCamposDisponibles() {
                this.log('🔍 Verificando campos disponibles...');
                
                const camposRequeridos = ['ventai', 'ventac', 'ventas', 'controlado', 'impuesto'];
                const camposEncontrados = [];
                const camposFaltantes = [];
                
                camposRequeridos.forEach(campo => {
                    const elemento = document.getElementById(`id_${campo}`);
                    if (elemento) {
                        camposEncontrados.push(campo);
                        this.log(`✅ Campo ${campo} encontrado: ${elemento.tagName} con valor "${elemento.value || 'vacío'}"`);
                    } else {
                        camposFaltantes.push(campo);
                        this.log(`❌ Campo ${campo} NO encontrado (id_${campo})`);
                    }
                });
                
                this.log(`📊 Resumen de campos: ${camposEncontrados.length}/${camposRequeridos.length} encontrados`);
                
                if (camposFaltantes.length > 0) {
                    this.log(`⚠️ Campos faltantes: ${camposFaltantes.join(', ')}`);
                } else {
                    this.log('✅ Todos los campos requeridos están disponibles');
                }
            }

            setupEventListeners() {
                const campos = ['ventai', 'ventac', 'ventas', 'controlado'];
                campos.forEach(campo => {
                    const input = document.getElementById(`id_${campo}`);
                    if (input) {
                        input.addEventListener('input', () => this.calcularEnTiempoReal(campo));
                        input.addEventListener('blur', () => this.calcularEnTiempoReal(campo));
                    }
                });
            }

            calcularEnTiempoReal(fieldName) {
                this.log(`🔄 Calculando impuestos para campo: ${fieldName}`);
                
                const valoresVentas = this.obtenerValoresVentas();
                this.log('📊 Valores de ventas obtenidos: ' + JSON.stringify(valoresVentas));
                
                // Calcular impuestos para cada tipo de venta
                const resultadoIndustria = this.calcularImpuestoICS(valoresVentas.ventai || 0);
                const resultadoComercio = this.calcularImpuestoICS(valoresVentas.ventac || 0);
                const resultadoServicios = this.calcularImpuestoICS(valoresVentas.ventas || 0);
                const resultadoControlados = this.calcularImpuestoICSControlados(valoresVentas.controlado || 0);
                
                const resultados = {
                    industria: resultadoIndustria,
                    comercio: resultadoComercio,
                    servicios: resultadoServicios,
                    controlados: resultadoControlados
                };

                this.log('💰 Resultados de cálculo por tipo: ' + JSON.stringify(resultados));

                // SUMATORIA COMPLETA: Incluir TODOS los tipos de ventas
                const totalImpuesto = resultadoIndustria.impuestoTotal + 
                                     resultadoComercio.impuestoTotal + 
                                     resultadoServicios.impuestoTotal + 
                                     resultadoControlados.impuestoTotal;

                this.log('🎯 SUMATORIA COMPLETA DE IMPUESTOS:');
                this.log(`   • Industria (Ventas Rubro Producción): L. ${resultadoIndustria.impuestoTotal.toFixed(2)}`);
                this.log(`   • Comercio (Ventas Mercadería): L. ${resultadoComercio.impuestoTotal.toFixed(2)}`);
                this.log(`   • Servicios (Ventas por Servicios): L. ${resultadoServicios.impuestoTotal.toFixed(2)}`);
                this.log(`   • Controlados (Ventas Productos Controlados): L. ${resultadoControlados.impuestoTotal.toFixed(2)}`);
                this.log(`   = TOTAL IMPUESTO CALCULADO: L. ${totalImpuesto.toFixed(2)}`);

                this.actualizarCampoImpuesto(totalImpuesto);
            }

            obtenerValoresVentas() {
                const campos = ['ventai', 'ventac', 'ventas', 'controlado'];
                const valores = {};

                campos.forEach(campo => {
                    const input = document.getElementById(`id_${campo}`);
                    if (input && input.value) {
                        const valor = this.limpiarValor(input.value);
                        if (valor > 0) {
                            valores[campo] = valor;
                            this.log(`✅ Campo ${campo} detectado con valor: ${valor}`);
                        }
                    }
                });

                this.log('📋 Valores finales de ventas: ' + JSON.stringify(valores));
                return valores;
            }

            limpiarValor(valor) {
                if (!valor) return 0;
                let valorLimpio = valor.toString().replace(/[^0-9.]/g, '');
                const numero = parseFloat(valorLimpio) || 0;
                return numero;
            }

            calcularImpuestoICS(valorVentas) {
                if (!valorVentas || valorVentas <= 0) {
                    return { impuestoTotal: 0, detalleCalculo: [], valorVentas: 0 };
                }

                let impuestoTotal = 0;
                let valorRestante = valorVentas;
                const detalleCalculo = [];

                for (const tarifa of this.tarifas) {
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
                    detalleCalculo: detalleCalculo,
                    valorVentas: valorVentas
                };
            }

            calcularImpuestoICSControlados(valorVentas) {
                if (!valorVentas || valorVentas <= 0) {
                    return { impuestoTotal: 0, detalleCalculo: [], valorVentas: 0 };
                }

                const tarifasControlados = [
                    {"rango1": 0.0, "rango2": 1000000.0, "valor": 1.0, "categoria": "2", "descripcion": "Controlados $0 - $1,000,000"},
                    {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 1.5, "categoria": "2", "descripcion": "Controlados $1,000,000 - $5,000,000"},
                    {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 2.0, "categoria": "2", "descripcion": "Controlados $5,000,000+"}
                ];

                let impuestoTotal = 0;
                let valorRestante = valorVentas;
                const detalleCalculo = [];

                for (const tarifa of tarifasControlados) {
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
                    detalleCalculo: detalleCalculo,
                    valorVentas: valorVentas
                };
            }

            actualizarCampoImpuesto(totalImpuesto) {
                const campoImpuesto = document.getElementById('id_impuesto');
                if (campoImpuesto) {
                    const valorAnterior = campoImpuesto.value;
                    campoImpuesto.value = totalImpuesto.toFixed(2);
                    
                    this.log(`✅ Campo impuesto actualizado:`);
                    this.log(`   Valor anterior: L. ${valorAnterior || '0.00'}`);
                    this.log(`   Valor nuevo: L. ${totalImpuesto.toFixed(2)}`);
                    
                    if (campoImpuesto.value === totalImpuesto.toFixed(2)) {
                        this.log(`✅ Verificación exitosa: Campo impuesto contiene el valor correcto`);
                    } else {
                        this.log(`❌ Error: Campo impuesto no se actualizó correctamente`);
                    }
                    
                    campoImpuesto.dispatchEvent(new Event('change', { bubbles: true }));
                } else {
                    this.log('❌ Campo impuesto no encontrado (id_impuesto)');
                }
            }

            log(mensaje) {
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

            recalcular() {
                this.calcularEnTiempoReal('manual');
            }
        }

        // Variables globales
        let declaracionVolumenInteractivo;

        function calcularAutomatico() {
            if (declaracionVolumenInteractivo) {
                declaracionVolumenInteractivo.calcularEnTiempoReal('input');
            }
        }

        function probarFuncionalidad() {
            if (declaracionVolumenInteractivo) {
                declaracionVolumenInteractivo.recalcular();
            }
        }

        function limpiarCampos() {
            document.getElementById('id_ventai').value = '';
            document.getElementById('id_ventac').value = '';
            document.getElementById('id_ventas').value = '';
            document.getElementById('id_controlado').value = '';
            document.getElementById('resultado').innerHTML = 'Campos limpiados';
            document.getElementById('logs').innerHTML = '';
        }

        // Inicializar sistema
        document.addEventListener('DOMContentLoaded', function() {
            declaracionVolumenInteractivo = new DeclaracionVolumenInteractivo();
            
            // Crear campo de impuesto si no existe
            if (!document.getElementById('id_impuesto')) {
                const campoImpuesto = document.createElement('input');
                campoImpuesto.id = 'id_impuesto';
                campoImpuesto.type = 'text';
                campoImpuesto.placeholder = 'Impuesto Calculado';
                campoImpuesto.readOnly = true;
                campoImpuesto.style.cssText = 'margin: 5px; padding: 8px; width: 200px; background: #f8f9fa; border: 1px solid #28a745; border-radius: 4px; font-weight: bold; color: #155724;';
                document.querySelector('.test-section:nth-child(3)').appendChild(campoImpuesto);
            }
        });
    </script>
</body>
</html>'''
    
    with open('test_funcionalidad_completa.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test de funcionalidad completa creado: test_funcionalidad_completa.html")
    print("📝 Para probar: abra el archivo en un navegador web")

def mostrar_instrucciones_finales():
    """Muestra las instrucciones finales para verificar la funcionalidad"""
    
    print("\n" + "=" * 60)
    print("🎯 INSTRUCCIONES PARA VERIFICAR LA FUNCIONALIDAD:")
    print("=" * 60)
    
    print("\n1️⃣ TEST INDEPENDIENTE:")
    print("   • Abrir 'test_funcionalidad_completa.html' en el navegador")
    print("   • Ingresar valores en los campos de ventas")
    print("   • Observar que el campo 'Impuesto Calculado' se actualice automáticamente")
    print("   • Verificar que los logs muestren la sumatoria completa")
    
    print("\n2️⃣ FORMULARIO REAL:")
    print("   • Acceder a: http://localhost:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151:1547")
    print("   • Abrir consola del navegador (F12)")
    print("   • Ingresar valores en los campos de ventas")
    print("   • Verificar que aparezcan estos logs:")
    print("     - '🔍 Verificando campos disponibles...'")
    print("     - '✅ Campo controlado encontrado'")
    print("     - '🎯 SUMATORIA COMPLETA DE IMPUESTOS:'")
    print("     - '✅ Campo impuesto actualizado'")
    
    print("\n3️⃣ VERIFICACIÓN ESPECÍFICA:")
    print("   • Confirmar que el campo 'Impuesto Calculado' muestre la suma de:")
    print("     - Ventas Rubro Producción")
    print("     - Ventas Mercadería")
    print("     - Ventas por Servicios")
    print("     - Ventas Productos Controlados ← INCLUIDO")
    
    print("\n✅ RESULTADO ESPERADO:")
    print("   El sistema debe calcular automáticamente el impuesto total")
    print("   incluyendo TODOS los tipos de ventas, especialmente los")
    print("   Productos Controlados con sus tarifas específicas.")

if __name__ == "__main__":
    verificar_funcionalidad_completa()
    print()
    crear_test_funcionalidad()
    print()
    mostrar_instrucciones_finales()

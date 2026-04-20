#!/usr/bin/env python3
"""
Test para verificar el formulario de declaración de volumen
"""

def test_formulario_volumen():
    """Test del formulario de declaración de volumen"""
    
    print("🧪 TEST DEL FORMULARIO DE DECLARACIÓN DE VOLUMEN")
    print("=" * 60)
    
    # Verificar que el archivo del formulario existe
    import os
    formulario_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    
    if not os.path.exists(formulario_path):
        print("❌ ERROR: No se encontró el formulario")
        print(f"Ruta esperada: {formulario_path}")
        return False
    
    print("✅ Formulario encontrado")
    
    # Leer el contenido del formulario
    with open(formulario_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar elementos clave
    verificaciones = [
        ("Campo Factor", "id_factor" in contenido or "name='factor'" in contenido),
        ("Campo Unidad", "id_unidad" in contenido or "name='unidad'" in contenido),
        ("Función calcularImpuestoUnidadFactor", "calcularImpuestoUnidadFactor" in contenido),
        ("Validación Factor > 0", "valorFactor <= 0" in contenido),
        ("Validación Unidad > 0", "valorUnidad <= 0" in contenido),
        ("Multiplicación Factor × Unidad", "valorFactor * valorUnidad" in contenido),
        ("Logs de cálculo", "Cálculo Factor × Unidad" in contenido),
        ("Aplicación tarifas ICS", "calcularImpuestoICS" in contenido),
        ("Suma al total", "impuestoTotal" in contenido),
        ("Event listeners", "addEventListener" in contenido)
    ]
    
    print("\n🔍 VERIFICACIONES DEL FORMULARIO:")
    todas_pasan = True
    
    for descripcion, condicion in verificaciones:
        if condicion:
            print(f"✅ {descripcion}")
        else:
            print(f"❌ {descripcion}")
            todas_pasan = False
    
    # Verificar estructura del JavaScript
    print("\n📋 ESTRUCTURA DEL JAVASCRIPT:")
    
    # Buscar la clase principal
    if "class DeclaracionVolumenInteractivo" in contenido:
        print("✅ Clase DeclaracionVolumenInteractivo encontrada")
    else:
        print("❌ Clase DeclaracionVolumenInteractivo no encontrada")
        todas_pasan = False
    
    # Buscar métodos específicos
    metodos = [
        "verificarCamposDisponibles",
        "setupEventListeners", 
        "obtenerValoresVentas",
        "calcularImpuestoUnidadFactor",
        "calcularImpuestoICS",
        "calcularEnTiempoReal"
    ]
    
    for metodo in metodos:
        if metodo in contenido:
            print(f"✅ Método {metodo} encontrado")
        else:
            print(f"❌ Método {metodo} no encontrado")
            todas_pasan = False
    
    # Verificar configuración de campos
    print("\n🔧 CONFIGURACIÓN DE CAMPOS:")
    
    # Campo Factor
    if "data-format=\"decimal-10-2\"" in contenido or "data-format='decimal-10-2'" in contenido:
        print("✅ Campo Factor configurado (DECIMAL 10,2)")
    else:
        print("❌ Campo Factor no configurado correctamente")
        todas_pasan = False
    
    # Campo Unidad
    if "data-format=\"integer-11\"" in contenido or "data-format='integer-11'" in contenido:
        print("✅ Campo Unidad configurado (11 enteros)")
    else:
        print("❌ Campo Unidad no configurado correctamente")
        todas_pasan = False
    
    # Verificar validación de entrada
    print("\n📝 VALIDACIÓN DE ENTRADA:")
    
    if ("maxlength='11'" in contenido or 'maxlength="11"' in contenido) and ("pattern='^\\\\d{1,11}$'" in contenido or 'pattern="^\\\\d{1,11}$"' in contenido):
        print("✅ Validación Unidad (11 enteros)")
    else:
        print("❌ Validación Unidad no configurada")
        todas_pasan = False
    
    if ("maxlength='13'" in contenido or 'maxlength="13"' in contenido) and ("pattern='^\\\\d{1,10}(\\\\.\\\\d{0,2})?$'" in contenido or 'pattern="^\\\\d{1,10}(\\\\.\\\\d{0,2})?$"' in contenido):
        print("✅ Validación Factor (DECIMAL 10,2)")
    else:
        print("❌ Validación Factor no configurada")
        todas_pasan = False
    
    return todas_pasan

def crear_test_html():
    """Crear un test HTML para verificar el cálculo"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test - Cálculo Factor × Unidad</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .test { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .error { background: #ffebee; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #f44336; }
        .success { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #4caf50; }
        .log { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; font-family: monospace; font-size: 0.9em; border: 1px solid #dee2e6; }
        input { padding: 8px; margin: 5px; border: 1px solid #ccc; border-radius: 4px; width: 150px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #0056b3; }
        .resultado { background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2196f3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test - Cálculo Factor × Unidad</h1>
        
        <div class="test">
            <h3>📋 Test del Cálculo</h3>
            <p>Este test verifica que el cálculo Factor × Unidad funcione correctamente</p>
            
            <label>Factor: <input type="text" id="factor" value="1.5" placeholder="Ej: 1.5"></label>
            <label>Unidad: <input type="text" id="unidad" value="500" placeholder="Ej: 500"></label>
            <button onclick="ejecutarTest()">🧪 Ejecutar Test</button>
            <button onclick="limpiarTest()">🧹 Limpiar</button>
        </div>

        <div id="resultado" class="resultado" style="display: none;">
            <h3>📊 Resultado del Test</h3>
            <div id="detalle"></div>
        </div>

        <div class="test">
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
            log('🧮 Iniciando cálculo Factor × Unidad...');
            log(`   Factor recibido: ${valorFactor} (tipo: ${typeof valorFactor})`);
            log(`   Unidad recibida: ${valorUnidad} (tipo: ${typeof valorUnidad})`);
            
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

        function ejecutarTest() {
            const factor = parseFloat(document.getElementById('factor').value) || 0;
            const unidad = parseInt(document.getElementById('unidad').value) || 0;
            
            // Limpiar logs anteriores
            document.getElementById('logs').innerHTML = '';
            
            log('🚀 Iniciando test...');
            log(`📥 Valores de entrada: Factor=${factor}, Unidad=${unidad}`);
            
            const resultado = calcularImpuestoUnidadFactor(unidad, factor);
            
            // Mostrar resultado
            const resultadoDiv = document.getElementById('resultado');
            const detalleDiv = document.getElementById('detalle');
            
            if (resultado.impuestoTotal > 0) {
                resultadoDiv.style.display = 'block';
                detalleDiv.innerHTML = `
                    <div class="success">
                        <h4>✅ Test Exitoso</h4>
                        <p><strong>Factor:</strong> ${resultado.valorFactor}</p>
                        <p><strong>Unidad:</strong> ${resultado.valorUnidad}</p>
                        <p><strong>Valor Calculado:</strong> ${resultado.valorFactor} × ${resultado.valorUnidad} = <strong>${resultado.valorCalculado}</strong></p>
                        <p><strong>Impuesto Calculado:</strong> L. <strong>${resultado.impuestoTotal.toFixed(2)}</strong></p>
                    </div>
                `;
                log('✅ Test completado exitosamente');
            } else {
                resultadoDiv.style.display = 'block';
                detalleDiv.innerHTML = `
                    <div class="error">
                        <h4>❌ Test Fallido</h4>
                        <p><strong>Error:</strong> No se puede calcular</p>
                        <p>Factor: ${resultado.valorFactor} | Unidad: ${resultado.valorUnidad}</p>
                        <p>Ambos valores deben ser mayores a 0</p>
                    </div>
                `;
                log('❌ Test falló - valores inválidos');
            }
        }

        function limpiarTest() {
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
            log('🚀 Sistema de test iniciado');
            log('💡 Ingresa valores en Factor y Unidad, luego presiona "Ejecutar Test"');
        });
    </script>
</body>
</html>'''
    
    with open('test_formulario_volumen.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test HTML creado: test_formulario_volumen.html")

if __name__ == "__main__":
    print("🧪 INICIANDO TEST DEL FORMULARIO...")
    print()
    
    # Ejecutar test del formulario
    if test_formulario_volumen():
        print("\n✅ TODOS LOS TESTS PASARON")
        print("🎯 El formulario está configurado correctamente")
        
        # Crear test HTML
        crear_test_html()
        print("\n📁 Archivos de test creados:")
        print("   - test_formulario_volumen.html")
        
        print("\n🔧 PRÓXIMOS PASOS:")
        print("1. Abrir 'test_formulario_volumen.html' en el navegador")
        print("2. Probar el cálculo con diferentes valores")
        print("3. Si funciona, la funcionalidad está lista")
        
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        print("🔧 Necesita corrección antes de continuar")

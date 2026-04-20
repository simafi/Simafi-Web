#!/usr/bin/env python3
"""
Script para probar la sumatoria de impuestos incluyendo productos controlados
"""

def crear_test_suma_impuestos():
    """Crea un test HTML específico para verificar la sumatoria de impuestos"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test - Sumatoria de Impuestos con Productos Controlados</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
        .success { background-color: #d4edda; border-color: #c3e6cb; }
        .error { background-color: #f8d7da; border-color: #f5c6cb; }
        input { margin: 5px; padding: 8px; width: 200px; }
        button { padding: 10px 20px; margin: 5px; }
        #resultado { font-weight: bold; font-size: 1.2em; }
        .desglose { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🧮 Test - Sumatoria de Impuestos con Productos Controlados</h1>
    
    <div class="test-section">
        <h3>Campos de Ventas</h3>
        <label>Ventas Rubro Producción:</label>
        <input type="text" id="id_ventai" value="1000000" placeholder="Ej: 1000000"><br>
        
        <label>Ventas Mercadería:</label>
        <input type="text" id="id_ventac" value="500000" placeholder="Ej: 500000"><br>
        
        <label>Ventas por Servicios:</label>
        <input type="text" id="id_ventas" value="300000" placeholder="Ej: 300000"><br>
        
        <label>Ventas Productos Controlados:</label>
        <input type="text" id="id_controlado" value="200000" placeholder="Ej: 200000"><br>
        
        <button onclick="probarSumatoria()">🧮 Probar Sumatoria Completa</button>
        <button onclick="limpiarCampos()">🧹 Limpiar</button>
    </div>
    
    <div class="test-section">
        <h3>Resultado del Cálculo</h3>
        <div id="resultado">Haga clic en "Probar Sumatoria Completa"</div>
    </div>

    <script>
        // Sistema de cálculo embebido (igual al del template)
        class DeclaracionVolumenInteractivo {
            constructor() {
                this.tarifas = [
                    {"rango1": 0.0, "rango2": 500000.0, "valor": 0.3, "categoria": "1", "descripcion": "Rango $0 - $500,000"},
                    {"rango1": 500000.01, "rango2": 10000000.0, "valor": 0.4, "categoria": "1", "descripcion": "Rango $500,000 - $10,000,000"},
                    {"rango1": 10000000.01, "rango2": 20000000.0, "valor": 0.3, "categoria": "1", "descripcion": "Rango $10,000,000 - $20,000,000"},
                    {"rango1": 20000000.01, "rango2": 30000000.0, "valor": 0.2, "categoria": "1", "descripcion": "Rango $20,000,000 - $30,000,000"},
                    {"rango1": 30000000.01, "rango2": 9999999999.0, "valor": 0.15, "categoria": "1", "descripcion": "Rango $30,000,000 - $9,999,999,999"}
                ];
            }

            calcularImpuestoICS(valorVentas) {
                if (!valorVentas || valorVentas <= 0) return { impuestoTotal: 0 };
                
                let impuestoTotal = 0;
                let valorRestante = valorVentas;
                
                for (const tarifa of this.tarifas) {
                    if (valorRestante <= 0) break;
                    const diferencialRango = tarifa.rango2 - tarifa.rango1;
                    if (diferencialRango <= 0) continue;
                    
                    let valorAplicable = Math.min(valorRestante, diferencialRango);
                    impuestoTotal += (valorAplicable * tarifa.valor / 1000);
                    valorRestante -= valorAplicable;
                }
                
                return { impuestoTotal: Math.round(impuestoTotal * 100) / 100 };
            }

            calcularImpuestoICSControlados(valorVentas) {
                if (!valorVentas || valorVentas <= 0) return { impuestoTotal: 0 };
                
                const tarifasControlados = [
                    {"rango1": 0.0, "rango2": 1000000.0, "valor": 1.0},
                    {"rango1": 1000000.01, "rango2": 5000000.0, "valor": 1.5},
                    {"rango1": 5000000.01, "rango2": 9999999999.0, "valor": 2.0}
                ];
                
                let impuestoTotal = 0;
                let valorRestante = valorVentas;
                
                for (const tarifa of tarifasControlados) {
                    if (valorRestante <= 0) break;
                    const diferencialRango = tarifa.rango2 - tarifa.rango1;
                    if (diferencialRango <= 0) continue;
                    
                    let valorAplicable = Math.min(valorRestante, diferencialRango);
                    impuestoTotal += (valorAplicable * tarifa.valor / 1000);
                    valorRestante -= valorAplicable;
                }
                
                return { impuestoTotal: Math.round(impuestoTotal * 100) / 100 };
            }
        }

        function probarSumatoria() {
            const sistema = new DeclaracionVolumenInteractivo();
            
            // Obtener valores
            const ventai = parseFloat(document.getElementById('id_ventai').value) || 0;
            const ventac = parseFloat(document.getElementById('id_ventac').value) || 0;
            const ventas = parseFloat(document.getElementById('id_ventas').value) || 0;
            const controlado = parseFloat(document.getElementById('id_controlado').value) || 0;
            
            console.log('🧮 PROBANDO SUMATORIA DE IMPUESTOS:');
            console.log(`Ventas Rubro Producción: L. ${ventai.toLocaleString()}`);
            console.log(`Ventas Mercadería: L. ${ventac.toLocaleString()}`);
            console.log(`Ventas por Servicios: L. ${ventas.toLocaleString()}`);
            console.log(`Ventas Productos Controlados: L. ${controlado.toLocaleString()}`);
            
            // Calcular impuestos individuales
            const resultadoIndustria = sistema.calcularImpuestoICS(ventai);
            const resultadoComercio = sistema.calcularImpuestoICS(ventac);
            const resultadoServicios = sistema.calcularImpuestoICS(ventas);
            const resultadoControlados = sistema.calcularImpuestoICSControlados(controlado);
            
            console.log('💰 IMPUESTOS CALCULADOS:');
            console.log(`Industria: L. ${resultadoIndustria.impuestoTotal.toFixed(2)}`);
            console.log(`Comercio: L. ${resultadoComercio.impuestoTotal.toFixed(2)}`);
            console.log(`Servicios: L. ${resultadoServicios.impuestoTotal.toFixed(2)}`);
            console.log(`Controlados: L. ${resultadoControlados.impuestoTotal.toFixed(2)}`);
            
            // SUMATORIA COMPLETA
            const totalImpuesto = resultadoIndustria.impuestoTotal + 
                                 resultadoComercio.impuestoTotal + 
                                 resultadoServicios.impuestoTotal + 
                                 resultadoControlados.impuestoTotal;
            
            console.log('🎯 SUMATORIA COMPLETA:');
            console.log(`TOTAL IMPUESTO CALCULADO: L. ${totalImpuesto.toFixed(2)}`);
            
            // Mostrar resultado en la página
            const resultado = document.getElementById('resultado');
            resultado.innerHTML = `
                <div class="desglose">
                    <h4>📊 Desglose de Impuestos:</h4>
                    <p><strong>Industria (Ventas Rubro Producción):</strong> L. ${resultadoIndustria.impuestoTotal.toFixed(2)}</p>
                    <p><strong>Comercio (Ventas Mercadería):</strong> L. ${resultadoComercio.impuestoTotal.toFixed(2)}</p>
                    <p><strong>Servicios (Ventas por Servicios):</strong> L. ${resultadoServicios.impuestoTotal.toFixed(2)}</p>
                    <p><strong>Controlados (Ventas Productos Controlados):</strong> L. ${resultadoControlados.impuestoTotal.toFixed(2)}</p>
                </div>
                <div style="background: #28a745; color: white; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>🎯 TOTAL IMPUESTO CALCULADO: L. ${totalImpuesto.toFixed(2)}</h3>
                    <p>Este valor debe aparecer en el campo "Impuesto Calculado" del formulario</p>
                </div>
            `;
        }
        
        function limpiarCampos() {
            document.getElementById('id_ventai').value = '';
            document.getElementById('id_ventac').value = '';
            document.getElementById('id_ventas').value = '';
            document.getElementById('id_controlado').value = '';
            document.getElementById('resultado').innerHTML = 'Campos limpiados';
        }
        
        // Ejecutar test automáticamente al cargar
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                console.log('✅ Test de sumatoria cargado');
                probarSumatoria();
            }, 1000);
        });
    </script>
</body>
</html>'''
    
    with open('test_suma_impuestos.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test de sumatoria creado: test_suma_impuestos.html")
    print("📝 Para probar: abra el archivo en un navegador web")

def mostrar_instrucciones():
    """Muestra instrucciones para verificar la sumatoria"""
    
    print("🔍 VERIFICACIÓN DE SUMATORIA DE IMPUESTOS")
    print("=" * 50)
    print()
    print("📋 PASOS PARA VERIFICAR:")
    print("1. Abrir test_suma_impuestos.html en el navegador")
    print("2. Verificar en la consola (F12) que aparezcan los logs:")
    print("   - '🧮 PROBANDO SUMATORIA DE IMPUESTOS:'")
    print("   - '💰 IMPUESTOS CALCULADOS:'")
    print("   - '🎯 SUMATORIA COMPLETA:'")
    print("3. Confirmar que el total incluya productos controlados")
    print()
    print("🌐 LUEGO PROBAR EN EL FORMULARIO REAL:")
    print("1. Acceder a: http://localhost:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151:1547")
    print("2. Abrir consola del navegador (F12)")
    print("3. Ingresar valores en los campos de ventas")
    print("4. Verificar que aparezcan estos logs:")
    print("   - '🔍 Verificando campos disponibles...'")
    print("   - '✅ Campo controlado encontrado'")
    print("   - '🎯 SUMATORIA COMPLETA DE IMPUESTOS:'")
    print("   - '✅ Campo impuesto actualizado'")
    print()
    print("✅ RESULTADO ESPERADO:")
    print("El campo 'Impuesto Calculado' debe mostrar la suma de:")
    print("• Ventas Rubro Producción + Ventas Mercadería + Ventas por Servicios + Ventas Productos Controlados")

if __name__ == "__main__":
    crear_test_suma_impuestos()
    print()
    mostrar_instrucciones()

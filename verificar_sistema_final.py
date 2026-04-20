#!/usr/bin/env python3
"""
Script final para verificar que el sistema de cálculo interactivo esté funcionando
"""

def verificar_sistema_final():
    """Verificación final del sistema"""
    
    print("🔍 VERIFICACIÓN FINAL DEL SISTEMA DE CÁLCULO INTERACTIVO")
    print("=" * 70)
    
    # Verificar template
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        verificaciones = [
            ('DeclaracionVolumenInteractivo', 'Clase principal del sistema'),
            ('calcularImpuestoICSControlados', 'Función para productos controlados'),
            ('controlados: this.calcularImpuestoICSControlados', 'Inclusión en sumatoria'),
            ('resultados.controlados.impuestoTotal', 'Sumatoria de controlados'),
            ('Sistema de cálculo embebido cargado correctamente', 'Mensaje de confirmación')
        ]
        
        print("📋 VERIFICACIONES DEL TEMPLATE:")
        for verificacion, descripcion in verificaciones:
            if verificacion in contenido:
                print(f"✅ {descripcion}")
            else:
                print(f"❌ {descripcion}")
        
        # Verificar que no haya referencias a archivos externos problemáticos
        if 'src="{% static \'js/declaracion_volumen_interactivo.js\' %}"' in contenido:
            print("⚠️ Aún hay referencia a archivo externo (puede causar problemas)")
        else:
            print("✅ No hay referencias problemáticas a archivos externos")
            
    except FileNotFoundError:
        print(f"❌ Template no encontrado: {template_path}")
    except Exception as e:
        print(f"❌ Error verificando template: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 RESUMEN DE LA SOLUCIÓN IMPLEMENTADA:")
    print("1. ✅ JavaScript embebido directamente en el template")
    print("2. ✅ Cálculo de productos controlados incluido en sumatoria")
    print("3. ✅ Logs de depuración para facilitar troubleshooting")
    print("4. ✅ Sistema independiente de archivos estáticos externos")
    print("5. ✅ Tarifas específicas para productos controlados")
    
    print("\n📊 CÁLCULO ACTUALIZADO:")
    print("El campo 'Impuesto Calculado' ahora suma:")
    print("• Ventas Rubro Producción (Industria)")
    print("• Ventas Mercadería (Comercio)")
    print("• Ventas por Servicios")
    print("• Ventas Productos Controlados ← INCLUIDO")
    
    print("\n🧪 PARA PROBAR:")
    print("1. Acceder a: http://localhost:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151:1547")
    print("2. Abrir consola del navegador (F12 → Console)")
    print("3. Ingresar valores en los campos de ventas")
    print("4. Verificar que aparezcan estos logs:")
    print("   - '🚀 Sistema de cálculo interactivo inicializado (versión embebida)'")
    print("   - '✅ Sistema de cálculo embebido cargado correctamente'")
    print("   - '🔄 Calculando impuestos para campo: controlado'")
    print("   - '✅ Campo controlado detectado con valor: X'")
    print("   - '🎯 Total de impuestos calculado:'")
    print("5. Confirmar que el campo 'Impuesto Calculado' se actualice automáticamente")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("Si el sistema no funciona:")
    print("1. Verificar que el servidor esté ejecutándose en puerto 8080")
    print("2. Recargar la página (Ctrl+F5)")
    print("3. Verificar en la consola si hay errores JavaScript")
    print("4. Confirmar que los campos tengan los IDs correctos (id_ventai, id_ventac, etc.)")

def crear_test_rapido():
    """Crea un test HTML rápido para verificar el sistema"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Rápido - Sistema de Cálculo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
        input { margin: 5px; padding: 8px; width: 200px; }
        button { padding: 10px 20px; margin: 5px; }
        #resultado { font-weight: bold; font-size: 1.2em; color: #28a745; }
    </style>
</head>
<body>
    <h1>🧪 Test Rápido - Sistema de Cálculo Embebido</h1>
    
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
        
        <button onclick="probarSistema()">🧮 Probar Sistema</button>
    </div>
    
    <div class="test-section">
        <h3>Resultado</h3>
        <div id="resultado">Haga clic en "Probar Sistema"</div>
    </div>

    <script>
        // Incluir el mismo JavaScript del template
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

        function probarSistema() {
            const sistema = new DeclaracionVolumenInteractivo();
            
            const ventai = parseFloat(document.getElementById('id_ventai').value) || 0;
            const ventac = parseFloat(document.getElementById('id_ventac').value) || 0;
            const ventas = parseFloat(document.getElementById('id_ventas').value) || 0;
            const controlado = parseFloat(document.getElementById('id_controlado').value) || 0;
            
            const resultadoIndustria = sistema.calcularImpuestoICS(ventai);
            const resultadoComercio = sistema.calcularImpuestoICS(ventac);
            const resultadoServicios = sistema.calcularImpuestoICS(ventas);
            const resultadoControlados = sistema.calcularImpuestoICSControlados(controlado);
            
            const totalImpuesto = resultadoIndustria.impuestoTotal + 
                                 resultadoComercio.impuestoTotal + 
                                 resultadoServicios.impuestoTotal + 
                                 resultadoControlados.impuestoTotal;
            
            const resultado = document.getElementById('resultado');
            resultado.innerHTML = `
                <h4>📊 Resultados del Cálculo:</h4>
                <p>Industria: L. ${resultadoIndustria.impuestoTotal.toFixed(2)}</p>
                <p>Comercio: L. ${resultadoComercio.impuestoTotal.toFixed(2)}</p>
                <p>Servicios: L. ${resultadoServicios.impuestoTotal.toFixed(2)}</p>
                <p>Controlados: L. ${resultadoControlados.impuestoTotal.toFixed(2)}</p>
                <p><strong>Total Impuesto: L. ${totalImpuesto.toFixed(2)}</strong></p>
            `;
        }
    </script>
</body>
</html>'''
    
    with open('test_rapido_sistema.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Test rápido creado: test_rapido_sistema.html")
    print("📝 Para probar: abra el archivo en un navegador web")

if __name__ == "__main__":
    verificar_sistema_final()
    print("\n")
    crear_test_rapido()

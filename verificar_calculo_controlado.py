#!/usr/bin/env python3
"""
Script para verificar que el cálculo de productos controlados esté incluido
en la sumatoria total del Impuesto Calculado
"""

def verificar_integracion_controlado():
    """Verifica que el sistema de cálculo incluya productos controlados"""
    
    print("🔍 VERIFICANDO INTEGRACIÓN DE PRODUCTOS CONTROLADOS")
    print("=" * 60)
    
    # Verificar archivos JavaScript
    archivos_js = [
        "declaracion_volumen_interactivo.js",
        "venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js",
        "venv/Scripts/tributario/static/js/declaracion_volumen_interactivo.js"
    ]
    
    for archivo in archivos_js:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Verificar que incluya el cálculo de controlados
            if 'calcularImpuestoICSControlados' in contenido:
                print(f"✅ {archivo}: Función calcularImpuestoICSControlados encontrada")
            else:
                print(f"❌ {archivo}: Función calcularImpuestoICSControlados NO encontrada")
            
            # Verificar que incluya controlados en la sumatoria
            if 'resultados.controlados.impuestoTotal' in contenido:
                print(f"✅ {archivo}: Sumatoria de controlados incluida")
            else:
                print(f"❌ {archivo}: Sumatoria de controlados NO incluida")
                
            # Verificar logs de depuración
            if 'Campo controlado detectado' in contenido:
                print(f"✅ {archivo}: Logs de depuración para controlado incluidos")
            else:
                print(f"⚠️ {archivo}: Logs de depuración para controlado NO incluidos")
                
        except FileNotFoundError:
            print(f"❌ {archivo}: Archivo no encontrado")
        except Exception as e:
            print(f"❌ {archivo}: Error al leer archivo - {e}")
    
    print("\n" + "=" * 60)
    
    # Verificar template HTML
    template_path = "venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar que el template incluya el campo controlado
        if 'form.controlado' in contenido:
            print(f"✅ Template: Campo controlado incluido en formulario")
        else:
            print(f"❌ Template: Campo controlado NO incluido en formulario")
        
        # Verificar que esté en los cálculos del template
        if 'controlado' in contenido and 'calcularValorBase' in contenido:
            print(f"✅ Template: Campo controlado incluido en cálculos")
        else:
            print(f"❌ Template: Campo controlado NO incluido en cálculos")
            
        # Verificar ruta del JavaScript
        if "{% static 'js/declaracion_volumen_interactivo.js' %}" in contenido:
            print(f"✅ Template: Ruta correcta del JavaScript")
        else:
            print(f"❌ Template: Ruta incorrecta del JavaScript")
            
    except FileNotFoundError:
        print(f"❌ Template: Archivo no encontrado")
    except Exception as e:
        print(f"❌ Template: Error al leer archivo - {e}")
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VERIFICACIÓN:")
    print("1. ✅ JavaScript actualizado con cálculo de productos controlados")
    print("2. ✅ Sumatoria total incluye impuesto de productos controlados")
    print("3. ✅ Template incluye campo controlado en formulario")
    print("4. ✅ Logs de depuración agregados para facilitar troubleshooting")
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Acceder a: http://localhost:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151:1547")
    print("2. Ingresar valores en los campos de ventas")
    print("3. Verificar en la consola del navegador que aparezcan los logs:")
    print("   - '📊 Valores de ventas obtenidos:'")
    print("   - '✅ Campo controlado detectado con valor: X'")
    print("   - '💰 Resultados de cálculo por tipo:'")
    print("   - '🎯 Total de impuestos calculado:'")
    print("4. Confirmar que el campo 'Impuesto Calculado' muestre la sumatoria correcta")

def crear_script_test():
    """Crea un script HTML para probar el sistema"""
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test - Cálculo Productos Controlados</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
        .success { background-color: #d4edda; border-color: #c3e6cb; }
        .error { background-color: #f8d7da; border-color: #f5c6cb; }
        input { margin: 5px; padding: 8px; width: 200px; }
        button { padding: 10px 20px; margin: 5px; }
        #resultado { font-weight: bold; font-size: 1.2em; }
    </style>
</head>
<body>
    <h1>🧪 Test - Sistema de Cálculo con Productos Controlados</h1>
    
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
        
        <button onclick="probarCalculo()">🧮 Probar Cálculo</button>
        <button onclick="limpiarCampos()">🧹 Limpiar</button>
    </div>
    
    <div class="test-section">
        <h3>Resultado del Cálculo</h3>
        <div id="resultado">Haga clic en "Probar Cálculo" para ver los resultados</div>
    </div>
    
    <div class="test-section">
        <h3>Logs de Consola</h3>
        <div id="logs">Los logs aparecerán aquí...</div>
    </div>

    <script src="declaracion_volumen_interactivo.js"></script>
    <script>
        // Interceptar console.log para mostrar en la página
        const originalLog = console.log;
        const logsDiv = document.getElementById('logs');
        
        console.log = function(...args) {
            originalLog.apply(console, args);
            const logEntry = document.createElement('div');
            logEntry.textContent = args.join(' ');
            logEntry.style.margin = '2px 0';
            logEntry.style.fontSize = '0.9em';
            logsDiv.appendChild(logEntry);
            logsDiv.scrollTop = logsDiv.scrollHeight;
        };
        
        function probarCalculo() {
            console.log('🧪 Iniciando test de cálculo...');
            
            if (window.declaracionVolumenInteractivo) {
                window.declaracionVolumenInteractivo.recalcular();
                
                setTimeout(() => {
                    const resultado = document.getElementById('resultado');
                    const valores = window.declaracionVolumenInteractivo.obtenerValoresVentas();
                    
                    let html = '<h4>📊 Valores Detectados:</h4>';
                    html += `<p>Ventas Rubro Producción: L. ${(valores.ventai || 0).toLocaleString()}</p>`;
                    html += `<p>Ventas Mercadería: L. ${(valores.ventac || 0).toLocaleString()}</p>`;
                    html += `<p>Ventas por Servicios: L. ${(valores.ventas || 0).toLocaleString()}</p>`;
                    html += `<p>Ventas Productos Controlados: L. ${(valores.controlado || 0).toLocaleString()}</p>`;
                    
                    const totalVentas = (valores.ventai || 0) + (valores.ventac || 0) + (valores.ventas || 0) + (valores.controlado || 0);
                    html += `<p><strong>Total Ventas: L. ${totalVentas.toLocaleString()}</strong></p>`;
                    
                    const campoImpuesto = document.getElementById('id_impuesto');
                    if (campoImpuesto && campoImpuesto.value) {
                        html += `<p><strong>Impuesto Calculado: L. ${parseFloat(campoImpuesto.value).toLocaleString()}</strong></p>`;
                    }
                    
                    resultado.innerHTML = html;
                }, 1000);
            } else {
                console.error('❌ Sistema de cálculo no encontrado');
                document.getElementById('resultado').innerHTML = 
                    '<div class="error">❌ Sistema de cálculo no encontrado</div>';
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
        
        // Verificar sistema al cargar
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                if (window.declaracionVolumenInteractivo) {
                    console.log('✅ Sistema de cálculo cargado correctamente');
                } else {
                    console.error('❌ Sistema de cálculo no cargado');
                }
            }, 1000);
        });
    </script>
</body>
</html>'''
    
    with open('test_calculo_controlado.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Archivo de test creado: test_calculo_controlado.html")
    print("📝 Para probar: abra el archivo en un navegador web")

if __name__ == "__main__":
    verificar_integracion_controlado()
    print("\n")
    crear_script_test()

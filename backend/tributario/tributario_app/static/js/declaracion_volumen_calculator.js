/**
 * Calculadora de Impuestos ICS para Declaración de Volumen
 * Implementa cálculo automático basado en rangos progresivos
 */

class CalculadoraICS {
    constructor() {
        this.tarifas = [];
        this.initializeEventListeners();
        this.loadTarifas();
    }

    /**
     * Carga las tarifas desde el servidor o usa valores por defecto
     */
    async loadTarifas() {
        try {
            // Intentar cargar tarifas desde el servidor
            const response = await fetch('/tributario/api/tarifas-ics/?categoria=1');
            if (response.ok) {
                this.tarifas = await response.json();
            } else {
                throw new Error('No se pudieron cargar las tarifas');
            }
        } catch (error) {
            console.warn('Usando tarifas por defecto:', error);
            // Tarifas por defecto basadas en estructura común
            this.tarifas = [
                {rango1: 0, rango2: 1000000, valor: 2.5, descripcion: 'Primer rango'},
                {rango1: 1000000, rango2: 5000000, valor: 4.0, descripcion: 'Segundo rango'},
                {rango1: 5000000, rango2: 10000000, valor: 6.0, descripcion: 'Tercer rango'},
                {rango1: 10000000, rango2: 999999999, valor: 8.0, descripcion: 'Cuarto rango'}
            ];
        }
        
        // Ordenar tarifas por rango1
        this.tarifas.sort((a, b) => a.rango1 - b.rango1);
        console.log('Tarifas cargadas:', this.tarifas);
    }

    /**
     * Inicializa los event listeners para los campos del formulario
     */
    initializeEventListeners() {
        // Esperar a que el DOM esté listo
        document.addEventListener('DOMContentLoaded', () => {
            const campos = ['ventai', 'ventac', 'ventas'];
            
            campos.forEach(campo => {
                const input = document.getElementById(`id_${campo}`);
                if (input) {
                    // Eventos para cálculo en tiempo real
                    input.addEventListener('input', () => this.calcularTodos());
                    input.addEventListener('blur', () => this.calcularTodos());
                    input.addEventListener('change', () => this.calcularTodos());
                    
                    // Formatear números mientras se escribe
                    input.addEventListener('input', (e) => this.formatearNumero(e));
                }
            });

            // Botón de cálculo manual (si existe)
            const btnCalcular = document.getElementById('btn-calcular');
            if (btnCalcular) {
                btnCalcular.addEventListener('click', () => this.calcularTodos());
            }
        });
    }

    /**
     * Formatea números mientras se escriben
     */
    formatearNumero(event) {
        const input = event.target;
        let valor = input.value.replace(/[^\d]/g, '');
        
        if (valor) {
            // Formatear con comas como separadores de miles
            const numeroFormateado = parseInt(valor).toLocaleString('es-CO');
            input.value = numeroFormateado;
        }
    }

    /**
     * Calcula el impuesto ICS para un valor específico
     */
    calcularImpuestoICS(valorVentas) {
        if (!valorVentas || valorVentas <= 0) {
            return {
                impuestoTotal: 0,
                detalleCalculo: [],
                valorVentas: 0
            };
        }

        let impuestoTotal = 0;
        let valorRestante = valorVentas;
        const detalleCalculo = [];

        for (const tarifa of this.tarifas) {
            if (valorRestante <= 0) break;

            const diferencialRango = tarifa.rango2 - tarifa.rango1;
            
            if (diferencialRango <= 0) continue;

            // Determinar valor aplicable en este rango
            let valorAplicable;
            if (valorRestante <= diferencialRango) {
                valorAplicable = valorRestante;
                valorRestante = 0;
            } else {
                valorAplicable = diferencialRango;
                valorRestante -= diferencialRango;
            }

            // Calcular impuesto: (valor * tarifa) / 1000
            const impuestoRango = Math.round((valorAplicable * tarifa.valor / 1000) * 100) / 100;
            impuestoTotal += impuestoRango;

            detalleCalculo.push({
                rango1: tarifa.rango1,
                rango2: tarifa.rango2,
                diferencialRango: diferencialRango,
                valorAplicable: valorAplicable,
                tarifaPorMil: tarifa.valor,
                impuestoRango: impuestoRango,
                descripcion: tarifa.descripcion || `Rango ${tarifa.rango1.toLocaleString()} - ${tarifa.rango2.toLocaleString()}`
            });
        }

        return {
            impuestoTotal: Math.round(impuestoTotal * 100) / 100,
            detalleCalculo: detalleCalculo,
            valorVentas: valorVentas,
            valorRestante: valorRestante
        };
    }

    /**
     * Obtiene el valor numérico de un campo de entrada
     */
    obtenerValorCampo(campoId) {
        const input = document.getElementById(campoId);
        if (!input) return 0;
        
        // Remover formato y convertir a número
        const valor = input.value.replace(/[^\d]/g, '');
        return parseInt(valor) || 0;
    }

    /**
     * Calcula todos los impuestos del formulario
     */
    calcularTodos() {
        if (this.tarifas.length === 0) {
            console.warn('Tarifas no cargadas aún');
            return;
        }

        // Obtener valores de los campos
        const ventai = this.obtenerValorCampo('id_ventai');
        const ventac = this.obtenerValorCampo('id_ventac');
        const ventas = this.obtenerValorCampo('id_ventas');

        // Calcular impuestos
        const resultadoIndustria = this.calcularImpuestoICS(ventai);
        const resultadoComercio = this.calcularImpuestoICS(ventac);
        const resultadoServicios = this.calcularImpuestoICS(ventas);

        // Calcular totales
        const totalVentas = ventai + ventac + ventas;
        const totalImpuesto = resultadoIndustria.impuestoTotal + 
                             resultadoComercio.impuestoTotal + 
                             resultadoServicios.impuestoTotal;

        // Actualizar la interfaz
        this.actualizarInterfaz({
            industria: resultadoIndustria,
            comercio: resultadoComercio,
            servicios: resultadoServicios,
            totales: {
                totalVentas: totalVentas,
                totalImpuesto: totalImpuesto,
                ventai: ventai,
                ventac: ventac,
                ventas: ventas
            }
        });

        // Disparar evento personalizado para otros componentes
        document.dispatchEvent(new CustomEvent('calculoICSCompleto', {
            detail: {
                industria: resultadoIndustria,
                comercio: resultadoComercio,
                servicios: resultadoServicios,
                totales: {
                    totalVentas: totalVentas,
                    totalImpuesto: totalImpuesto
                }
            }
        }));
    }

    /**
     * Actualiza la interfaz con los resultados del cálculo
     */
    actualizarInterfaz(resultados) {
        // Actualizar campos de impuesto calculado
        this.actualizarCampoImpuesto('impuesto_industria', resultados.industria.impuestoTotal);
        this.actualizarCampoImpuesto('impuesto_comercio', resultados.comercio.impuestoTotal);
        this.actualizarCampoImpuesto('impuesto_servicios', resultados.servicios.impuestoTotal);
        this.actualizarCampoImpuesto('impuesto_total', resultados.totales.totalImpuesto);

        // IMPORTANTE: Actualizar el campo principal "impuesto calculado"
        this.actualizarImpuestoCalculado(resultados.totales.totalImpuesto);

        // Actualizar tabla de detalles si existe
        this.actualizarTablaDetalles(resultados);

        // Actualizar resumen visual
        this.actualizarResumenVisual(resultados);
    }

    /**
     * Actualiza un campo de impuesto específico
     */
    actualizarCampoImpuesto(campoId, valor) {
        const campo = document.getElementById(campoId);
        if (campo) {
            if (campo.tagName === 'INPUT') {
                campo.value = valor.toLocaleString('es-CO', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
            } else {
                campo.textContent = `$${valor.toLocaleString('es-CO', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                })}`;
            }
        }
    }

    /**
     * Actualiza el campo "impuesto calculado" con el resultado total
     */
    actualizarImpuestoCalculado(valorImpuesto) {
        // Buscar el campo por diferentes posibles IDs/nombres
        const posiblesIds = [
            'id_impuesto_calculado',
            'impuesto_calculado', 
            'id_impuesto',
            'impuesto',
            'total_impuesto',
            'id_total_impuesto'
        ];

        let campoEncontrado = false;
        
        for (const id of posiblesIds) {
            const campo = document.getElementById(id);
            if (campo) {
                if (campo.tagName === 'INPUT') {
                    campo.value = valorImpuesto.toFixed(2);
                } else {
                    campo.textContent = valorImpuesto.toFixed(2);
                }
                campoEncontrado = true;
                console.log(`Campo impuesto calculado actualizado: ${id} = ${valorImpuesto.toFixed(2)}`);
                break;
            }
        }

        // Si no encuentra el campo específico, buscar por name attribute
        if (!campoEncontrado) {
            const camposPorName = document.querySelectorAll('input[name*="impuesto"], input[name*="total"]');
            for (const campo of camposPorName) {
                if (campo.name.toLowerCase().includes('calculado') || 
                    campo.name.toLowerCase().includes('impuesto') ||
                    campo.name.toLowerCase().includes('total')) {
                    campo.value = valorImpuesto.toFixed(2);
                    campoEncontrado = true;
                    console.log(`Campo impuesto calculado actualizado por name: ${campo.name} = ${valorImpuesto.toFixed(2)}`);
                    break;
                }
            }
        }

        if (!campoEncontrado) {
            console.warn('No se encontró el campo "impuesto calculado". IDs buscados:', posiblesIds);
        }
    }

    /**
     * Actualiza la tabla de detalles del cálculo
     */
    actualizarTablaDetalles(resultados) {
        const tablaDetalles = document.getElementById('tabla-detalles-calculo');
        if (!tablaDetalles) return;

        let html = `
            <div class="table-responsive">
                <table class="table table-striped table-sm">
                    <thead class="table-dark">
                        <tr>
                            <th>Tipo</th>
                            <th>Valor Ventas</th>
                            <th>Impuesto Calculado</th>
                            <th>Detalles</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        // Fila Industria
        if (resultados.totales.ventai > 0) {
            html += `
                <tr>
                    <td><strong>Industria</strong></td>
                    <td>$${resultados.totales.ventai.toLocaleString('es-CO')}</td>
                    <td>$${resultados.industria.impuestoTotal.toLocaleString('es-CO', {minimumFractionDigits: 2})}</td>
                    <td>${this.generarDetalleRangos(resultados.industria.detalleCalculo)}</td>
                </tr>
            `;
        }

        // Fila Comercio
        if (resultados.totales.ventac > 0) {
            html += `
                <tr>
                    <td><strong>Comercio</strong></td>
                    <td>$${resultados.totales.ventac.toLocaleString('es-CO')}</td>
                    <td>$${resultados.comercio.impuestoTotal.toLocaleString('es-CO', {minimumFractionDigits: 2})}</td>
                    <td>${this.generarDetalleRangos(resultados.comercio.detalleCalculo)}</td>
                </tr>
            `;
        }

        // Fila Servicios
        if (resultados.totales.ventas > 0) {
            html += `
                <tr>
                    <td><strong>Servicios</strong></td>
                    <td>$${resultados.totales.ventas.toLocaleString('es-CO')}</td>
                    <td>$${resultados.servicios.impuestoTotal.toLocaleString('es-CO', {minimumFractionDigits: 2})}</td>
                    <td>${this.generarDetalleRangos(resultados.servicios.detalleCalculo)}</td>
                </tr>
            `;
        }

        // Fila Total
        html += `
                <tr class="table-info">
                    <td><strong>TOTAL</strong></td>
                    <td><strong>$${resultados.totales.totalVentas.toLocaleString('es-CO')}</strong></td>
                    <td><strong>$${resultados.totales.totalImpuesto.toLocaleString('es-CO', {minimumFractionDigits: 2})}</strong></td>
                    <td><em>Suma de todos los impuestos</em></td>
                </tr>
            </tbody>
        </table>
        </div>
        `;

        tablaDetalles.innerHTML = html;
    }

    /**
     * Genera el detalle de rangos aplicados
     */
    generarDetalleRangos(detalleCalculo) {
        if (!detalleCalculo || detalleCalculo.length === 0) {
            return '<em>Sin cálculo</em>';
        }

        return detalleCalculo.map(detalle => 
            `${detalle.descripcion}: $${detalle.valorAplicable.toLocaleString('es-CO')} × ${detalle.tarifaPorMil}‰ = $${detalle.impuestoRango.toLocaleString('es-CO', {minimumFractionDigits: 2})}`
        ).join('<br>');
    }

    /**
     * Actualiza el resumen visual con gráficos o indicadores
     */
    actualizarResumenVisual(resultados) {
        const resumenVisual = document.getElementById('resumen-visual');
        if (!resumenVisual) return;

        const porcentajeIndustria = resultados.totales.totalVentas > 0 ? 
            (resultados.totales.ventai / resultados.totales.totalVentas * 100) : 0;
        const porcentajeComercio = resultados.totales.totalVentas > 0 ? 
            (resultados.totales.ventac / resultados.totales.totalVentas * 100) : 0;
        const porcentajeServicios = resultados.totales.totalVentas > 0 ? 
            (resultados.totales.ventas / resultados.totales.totalVentas * 100) : 0;

        resumenVisual.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <div class="card bg-primary text-white">
                        <div class="card-body text-center">
                            <h5>Industria</h5>
                            <h3>$${resultados.industria.impuestoTotal.toLocaleString('es-CO', {minimumFractionDigits: 2})}</h3>
                            <small>${porcentajeIndustria.toFixed(1)}% del total</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-success text-white">
                        <div class="card-body text-center">
                            <h5>Comercio</h5>
                            <h3>$${resultados.comercio.impuestoTotal.toLocaleString('es-CO', {minimumFractionDigits: 2})}</h3>
                            <small>${porcentajeComercio.toFixed(1)}% del total</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-info text-white">
                        <div class="card-body text-center">
                            <h5>Servicios</h5>
                            <h3>$${resultados.servicios.impuestoTotal.toLocaleString('es-CO', {minimumFractionDigits: 2})}</h3>
                            <small>${porcentajeServicios.toFixed(1)}% del total</small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <div class="card bg-dark text-white">
                        <div class="card-body text-center">
                            <h4>Impuesto Total a Pagar</h4>
                            <h2>$${resultados.totales.totalImpuesto.toLocaleString('es-CO', {minimumFractionDigits: 2})}</h2>
                            <small>Sobre ventas totales de $${resultados.totales.totalVentas.toLocaleString('es-CO')}</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Método público para recalcular desde otros componentes
     */
    recalcular() {
        this.calcularTodos();
    }

    /**
     * Método para obtener los resultados actuales
     */
    obtenerResultados() {
        const ventai = this.obtenerValorCampo('id_ventai');
        const ventac = this.obtenerValorCampo('id_ventac');
        const ventas = this.obtenerValorCampo('id_ventas');

        return {
            industria: this.calcularImpuestoICS(ventai),
            comercio: this.calcularImpuestoICS(ventac),
            servicios: this.calcularImpuestoICS(ventas)
        };
    }
}

// Inicializar la calculadora cuando se carga la página
let calculadoraICS;
document.addEventListener('DOMContentLoaded', () => {
    calculadoraICS = new CalculadoraICS();
});

// Exponer funciones globales para compatibilidad
window.calcularImpuestosICS = () => {
    if (calculadoraICS) {
        calculadoraICS.recalcular();
    }
};

window.obtenerResultadosICS = () => {
    if (calculadoraICS) {
        return calculadoraICS.obtenerResultados();
    }
    return null;
};

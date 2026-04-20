/**
 * Sistema de cálculo interactivo EMBEBIDO para formulario declaracion_volumen
 * Versión simplificada que se incluye directamente en el template
 */

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
        this.setupEventListeners();
        console.log('🚀 Sistema de cálculo interactivo inicializado (versión embebida)');
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
        console.log(`🔄 Calculando impuestos para campo: ${fieldName}`);
        
        const valoresVentas = this.obtenerValoresVentas();
        console.log('📊 Valores de ventas obtenidos:', valoresVentas);
        
        const resultados = {
            industria: this.calcularImpuestoICS(valoresVentas.ventai || 0),
            comercio: this.calcularImpuestoICS(valoresVentas.ventac || 0),
            servicios: this.calcularImpuestoICS(valoresVentas.ventas || 0),
            controlados: this.calcularImpuestoICSControlados(valoresVentas.controlado || 0)
        };

        console.log('💰 Resultados de cálculo por tipo:', resultados);

        const totalImpuesto = resultados.industria.impuestoTotal + 
                             resultados.comercio.impuestoTotal + 
                             resultados.servicios.impuestoTotal + 
                             resultados.controlados.impuestoTotal;

        console.log('🎯 Total de impuestos calculado:', {
            industria: resultados.industria.impuestoTotal,
            comercio: resultados.comercio.impuestoTotal,
            servicios: resultados.servicios.impuestoTotal,
            controlados: resultados.controlados.impuestoTotal,
            total: totalImpuesto
        });

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
                    console.log(`✅ Campo ${campo} detectado con valor: ${valor}`);
                }
            }
        });

        console.log('📋 Valores finales de ventas:', valores);
        return valores;
    }

    limpiarValor(valor) {
        if (!valor) return 0;
        
        // Limpiar caracteres no numéricos excepto punto decimal
        let valorLimpio = valor.toString().replace(/[^0-9.]/g, '');
        
        // Convertir a número
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

        // Para productos controlados, usar tarifas más altas
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
            campoImpuesto.value = totalImpuesto.toFixed(2);
            console.log(`✅ Campo impuesto actualizado: L. ${totalImpuesto.toFixed(2)}`);
        }
    }

    recalcular() {
        this.calcularEnTiempoReal('manual');
    }
}

// Inicializar cuando el DOM esté listo
let declaracionVolumenInteractivo;
document.addEventListener('DOMContentLoaded', () => {
    declaracionVolumenInteractivo = new DeclaracionVolumenInteractivo();
    console.log('✅ Sistema de cálculo embebido cargado correctamente');
});

// Funciones globales para compatibilidad
window.calcularImpuestosDeclaracion = () => {
    if (declaracionVolumenInteractivo) {
        declaracionVolumenInteractivo.recalcular();
    }
};

window.obtenerCalculosDeclaracion = () => {
    if (declaracionVolumenInteractivo) {
        return declaracionVolumenInteractivo.obtenerValoresVentas();
    }
    return null;
};

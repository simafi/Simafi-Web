/**
 * Sistema de cálculo interactivo para formulario declaracion_volumen
 * Calcula automáticamente impuestos al ingresar valores en "Ventas Rubro Producción"
 */

class DeclaracionVolumenInteractivo {
    constructor() {
        this.tarifas = [
                {
                                "rango1": 0.0,
                                "rango2": 500000.0,
                                "valor": 0.3,
                                "categoria": "1",
                                "descripcion": "Rango $0 - $500,000"
                },
                {
                                "rango1": 500000.01,
                                "rango2": 10000000.0,
                                "valor": 0.4,
                                "categoria": "1",
                                "descripcion": "Rango $500,000 - $10,000,000"
                },
                {
                                "rango1": 10000000.01,
                                "rango2": 20000000.0,
                                "valor": 0.3,
                                "categoria": "1",
                                "descripcion": "Rango $10,000,000 - $20,000,000"
                },
                {
                                "rango1": 20000000.01,
                                "rango2": 30000000.0,
                                "valor": 0.2,
                                "categoria": "1",
                                "descripcion": "Rango $20,000,000 - $30,000,000"
                },
                {
                                "rango1": 30000000.01,
                                "rango2": 9999999999.0,
                                "valor": 0.15,
                                "categoria": "1",
                                "descripcion": "Rango $30,000,000 - $9,999,999,999"
                }
];
        this.initializeSystem();
    }

    /**
     * Inicializa el sistema de cálculo interactivo
     */
    async initializeSystem() {
        await this.loadTarifas();
        this.setupEventListeners();
        this.setupFormValidation();
        console.log('🚀 Sistema de cálculo interactivo inicializado');
    }

    /**
     * Carga las tarifas ICS desde el servidor o usa valores por defecto
     */
    async loadTarifas() {
        try {
            const response = await fetch('/tributario/api/tarifas-ics/?categoria=1');
            if (response.ok) {
                const data = await response.json();
                this.tarifas = data.tarifas || [];
            } else {
                throw new Error('No se pudieron cargar las tarifas del servidor');
            }
        } catch (error) {
            console.warn('Usando tarifas por defecto:', error);
            // Tarifas por defecto basadas en estructura común colombiana
            this.tarifas = [
                {
                                "rango1": 0.0,
                                "rango2": 500000.0,
                                "valor": 0.3,
                                "categoria": "1",
                                "descripcion": "Rango $0 - $500,000"
                },
                {
                                "rango1": 500000.01,
                                "rango2": 10000000.0,
                                "valor": 0.4,
                                "categoria": "1",
                                "descripcion": "Rango $500,000 - $10,000,000"
                },
                {
                                "rango1": 10000000.01,
                                "rango2": 20000000.0,
                                "valor": 0.3,
                                "categoria": "1",
                                "descripcion": "Rango $10,000,000 - $20,000,000"
                },
                {
                                "rango1": 20000000.01,
                                "rango2": 30000000.0,
                                "valor": 0.2,
                                "categoria": "1",
                                "descripcion": "Rango $20,000,000 - $30,000,000"
                },
                {
                                "rango1": 30000000.01,
                                "rango2": 9999999999.0,
                                "valor": 0.15,
                                "categoria": "1",
                                "descripcion": "Rango $30,000,000 - $9,999,999,999"
                }
];
        }
        
        this.tarifas.sort((a, b) => a.rango1 - b.rango1);
        console.log('📊 Tarifas cargadas:', this.tarifas.length, 'rangos');
    }

    /**
     * Configura los event listeners para los campos del formulario
     */
    setupEventListeners() {
        // Campos principales de ventas
        const camposVentas = [
            'ventai',      // Ventas Industria
            'ventac',      // Ventas Comercio  
            'ventas',      // Ventas Servicios
            'ventap',      // Ventas Rubro Producción
            'ventas_produccion', // Alternativo
            'rubro_produccion'   // Alternativo
        ];

        camposVentas.forEach(campo => {
            this.setupFieldListener(campo);
        });

        // Buscar campos por patrones comunes
        this.setupPatternListeners();

        // Botón de cálculo manual si existe
        const btnCalcular = document.getElementById('btn-calcular') || 
                           document.querySelector('[onclick*="calcular"]') ||
                           document.querySelector('.btn-calcular');
        
        if (btnCalcular) {
            btnCalcular.addEventListener('click', () => this.calcularTodos());
        }
    }

    /**
     * Configura listener para un campo específico
     */
    setupFieldListener(fieldName) {
        const posiblesIds = [
            `id_${fieldName}`,
            fieldName,
            `${fieldName}_input`,
            `campo_${fieldName}`
        ];

        for (const id of posiblesIds) {
            const field = document.getElementById(id);
            if (field) {
                this.addCalculationListeners(field, fieldName);
                console.log(`✅ Listener agregado a campo: ${id}`);
                return true;
            }
        }
        return false;
    }

    /**
     * Busca campos por patrones y agrega listeners
     */
    setupPatternListeners() {
        // Buscar inputs que contengan "venta" en el name o id
        const ventasInputs = document.querySelectorAll('input[name*="venta"], input[id*="venta"]');
        ventasInputs.forEach(input => {
            if (!input.hasAttribute('data-calculator-attached')) {
                this.addCalculationListeners(input, input.name || input.id);
                input.setAttribute('data-calculator-attached', 'true');
            }
        });

        // Buscar inputs que contengan "produccion" o "rubro"
        const produccionInputs = document.querySelectorAll('input[name*="produccion"], input[id*="produccion"], input[name*="rubro"], input[id*="rubro"]');
        produccionInputs.forEach(input => {
            if (!input.hasAttribute('data-calculator-attached')) {
                this.addCalculationListeners(input, input.name || input.id);
                input.setAttribute('data-calculator-attached', 'true');
                console.log(`✅ Campo de producción detectado: ${input.name || input.id}`);
            }
        });
    }

    /**
     * Agrega listeners de cálculo a un campo
     */
    addCalculationListeners(field, fieldName) {
        // Formateo de números mientras se escribe
        field.addEventListener('input', (e) => {
            this.formatearNumero(e);
            this.calcularEnTiempoReal(fieldName);
        });

        // Cálculo al perder el foco
        field.addEventListener('blur', () => {
            this.calcularEnTiempoReal(fieldName);
        });

        // Cálculo al cambiar el valor
        field.addEventListener('change', () => {
            this.calcularEnTiempoReal(fieldName);
        });

        // Indicador visual de que el campo tiene cálculo automático
        field.style.borderLeft = '3px solid #28a745';
        field.title = 'Cálculo automático de impuestos activado';
    }

    /**
     * Formatea números mientras se escriben
     */
    /**
     * Formatea números para DECIMAL(16,2) - 14 enteros + 2 decimales
     * Con separadores de miles en tiempo real
     */
    formatearNumero(event) {
        const input = event.target;
        let valor = input.value;
        
        // Guardar posición del cursor
        const cursorPos = input.selectionStart;
        
        // DETECCIÓN MEJORADA DE FORMATO EUROPEO/AMERICANO
        let valorLimpio = valor;
        
        // Caso específico: "5.000.000" (formato europeo puro - solo puntos como separadores de miles)
        if (/^\d{1,3}(\.\d{3})+$/.test(valor)) {
            // Es formato europeo puro: X.XXX.XXX (solo miles, sin decimales)
            valorLimpio = valor.replace(/\./g, '');
            console.log(`🔄 Formato europeo detectado: ${valor} → ${valorLimpio}`);
        }
        // Caso: "5.000.000,50" (formato europeo con decimales)
        else if (/^\d{1,3}(\.\d{3})+,\d{1,2}$/.test(valor)) {
            // Formato europeo completo: X.XXX.XXX,XX
            valorLimpio = valor.replace(/\./g, '').replace(',', '.');
            console.log(`🔄 Formato europeo con decimales: ${valor} → ${valorLimpio}`);
        }
        // Caso: "5,000,000.50" (formato americano)
        else if (/^\d{1,3}(,\d{3})+\.\d{1,2}$/.test(valor)) {
            // Formato americano: X,XXX,XXX.XX
            valorLimpio = valor.replace(/,/g, '');
            console.log(`🔄 Formato americano: ${valor} → ${valorLimpio}`);
        }
        // Caso: "5,000,000" (formato americano sin decimales)
        else if (/^\d{1,3}(,\d{3})+$/.test(valor)) {
            // Formato americano sin decimales: X,XXX,XXX
            valorLimpio = valor.replace(/,/g, '');
            console.log(`🔄 Formato americano sin decimales: ${valor} → ${valorLimpio}`);
        }
        // Casos mixtos o ambiguos
        else {
            const tienePuntoYComa = valor.includes('.') && valor.includes(',');
            const ultimoPunto = valor.lastIndexOf('.');
            const ultimaComa = valor.lastIndexOf(',');
            
            if (tienePuntoYComa) {
                // Determinar cuál es el separador decimal por posición
                if (ultimoPunto > ultimaComa) {
                    // Formato americano: 1,234.56
                    valorLimpio = valor.replace(/,/g, '');
                } else {
                    // Formato europeo: 1.234,56
                    valorLimpio = valor.replace(/\./g, '').replace(',', '.');
                }
            } else if (valor.includes(',') && !valor.includes('.')) {
                // Solo comas - verificar contexto
                const partesComa = valor.split(',');
                if (partesComa.length === 2 && partesComa[1].length <= 2) {
                    // Es separador decimal: 1234,56
                    valorLimpio = valor.replace(',', '.');
                } else {
                    // Son separadores de miles: 1,234,567
                    valorLimpio = valor.replace(/,/g, '');
                }
            } else if (valor.includes('.') && !valor.includes(',')) {
                // Solo puntos - verificar contexto
                const partesPunto = valor.split('.');
                if (partesPunto.length === 2 && partesPunto[1].length <= 2) {
                    // Es separador decimal americano: 1234.56
                    valorLimpio = valor;
                } else {
                    // Son separadores de miles europeos: 1.234.567
                    valorLimpio = valor.replace(/\./g, '');
                }
            } else {
                // Solo números, mantener como está
                valorLimpio = valor;
            }
        }
        
        // Limpiar caracteres no numéricos excepto punto decimal
        valorLimpio = valorLimpio.replace(/[^0-9.]/g, '');
        
        // Usar el valor limpio procesado
        valor = valorLimpio;
        
        // Permitir solo un punto decimal
        const partes = valor.split('.');
        if (partes.length > 2) {
            valor = partes[0] + '.' + partes.slice(1).join('');
        }
        
        // Recalcular partes después de limpiar
        const partesLimpias = valor.split('.');
        
        // Limitar a 14 enteros
        if (partesLimpias[0] && partesLimpias[0].length > 14) {
            partesLimpias[0] = partesLimpias[0].substring(0, 14);
            valor = partesLimpias.join('.');
        }
        
        // Limitar a 2 decimales
        if (partesLimpias[1] && partesLimpias[1].length > 2) {
            partesLimpias[1] = partesLimpias[1].substring(0, 2);
            valor = partesLimpias[0] + '.' + partesLimpias[1];
        }
        
        // Validar rango máximo DECIMAL(16,2)
        const numeroValor = parseFloat(valor);
        if (numeroValor > 99999999999999.99) {
            valor = '99999999999999.99';
        }
        
        // Aplicar formato con separadores de miles SIEMPRE
        if (valor) {
            const partesFormato = valor.split('.');
            
            // Formatear parte entera con separadores de miles
            if (partesFormato[0] && partesFormato[0].length > 0) {
                const parteEntera = partesFormato[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                
                if (partesFormato[1] !== undefined) {
                    // Tiene decimales
                    valor = parteEntera + '.' + partesFormato[1];
                } else {
                    // Solo enteros
                    valor = parteEntera;
                }
            }
        }
        
        // Actualizar valor del input
        const valorAnterior = input.value;
        input.value = valor;
        
        // Ajustar posición del cursor si el valor cambió (solo para inputs tipo text)
        if (valorAnterior !== valor && input.type === 'text') {
            const diferencia = valor.length - valorAnterior.length;
            const nuevaPos = Math.max(0, cursorPos + diferencia);
            setTimeout(() => {
                try {
                    input.setSelectionRange(nuevaPos, nuevaPos);
                } catch (e) {
                    // Ignorar error si el input no soporta setSelectionRange
                    console.warn('setSelectionRange no soportado en este input:', e);
                }
            }, 0);
        }
    }

    /**
     * Calcula impuestos en tiempo real
     */
    calcularEnTiempoReal(fieldName) {
        if (this.tarifas.length === 0) {
            console.warn('Tarifas no cargadas aún');
            return;
        }

        // Obtener todos los valores de ventas
        const valoresVentas = this.obtenerValoresVentas();
        
        // Calcular impuestos para cada tipo
        const resultados = {
            industria: this.calcularImpuestoICS(valoresVentas.ventai || 0),
            comercio: this.calcularImpuestoICS(valoresVentas.ventac || 0),
            servicios: this.calcularImpuestoICS(valoresVentas.ventas || 0),
            produccion: this.calcularImpuestoICS(valoresVentas.ventap || 0)
        };

        // Calcular totales
        const totalVentas = (valoresVentas.ventai || 0) + 
                           (valoresVentas.ventac || 0) + 
                           (valoresVentas.ventas || 0) + 
                           (valoresVentas.ventap || 0);

        const totalImpuesto = resultados.industria.impuestoTotal + 
                             resultados.comercio.impuestoTotal + 
                             resultados.servicios.impuestoTotal + 
                             resultados.produccion.impuestoTotal;

        // Actualizar interfaz
        this.actualizarCamposCalculados(totalImpuesto, resultados);
        
        // Mostrar feedback visual
        this.mostrarFeedbackCalculo(fieldName, totalImpuesto);

        // Disparar evento personalizado
        document.dispatchEvent(new CustomEvent('calculoICSRealizado', {
            detail: {
                campo: fieldName,
                totalVentas: totalVentas,
                totalImpuesto: totalImpuesto,
                resultados: resultados
            }
        }));
    }

    /**
     * Obtiene valores de todos los campos de ventas y controlado
     */
    obtenerValoresVentas() {
        // NOTA: ventap no existe en tabla BD - usar ventas como alternativa
        const campos = ['ventai', 'ventac', 'ventas', 'ventap', 'ventas_produccion', 'rubro_produccion', 'controlado', 'controlado'];
        const valores = {};

        campos.forEach(campo => {
            const valor = this.obtenerValorCampoValidado(campo);
            if (valor > 0) {
                // Mapear campos alternativos
                if (campo === 'ventas_produccion' || campo === 'rubro_produccion') {
                    valores.ventap = (valores.ventap || 0) + valor;
                } else if (campo === 'controlado') {
                    // Mapear 'controlado' a 'controlado' (nombre en BD)
                    valores.controlado = valor;
                } else {
                    valores[campo] = valor;
                }
            }
        });

        return valores;
    }

    /**
     * Obtiene el valor numérico de un campo
     */
    obtenerValorCampo(campo) {
        // Mapear 'controlado' a 'controlado' si es necesario
        const campoReal = campo === 'controlado' ? 'controlado' : campo;
        const posiblesIds = [`id_${campoReal}`, `id_${campo}`, campoReal, campo, `${campoReal}_input`, `${campo}_input`];
        
        for (const id of posiblesIds) {
            const input = document.getElementById(id);
            if (input && input.value) {
                let valor = input.value;
                
                // Detectar formato europeo vs americano
                const tienePuntoYComa = valor.includes('.') && valor.includes(',');
                const ultimoPunto = valor.lastIndexOf('.');
                const ultimaComa = valor.lastIndexOf(',');
                
                if (tienePuntoYComa) {
                    // Determinar cuál es el separador decimal
                    if (ultimoPunto > ultimaComa) {
                        // Formato americano: 1,234.56
                        valor = valor.replace(/,/g, '');
                    } else {
                        // Formato europeo: 1.234,56
                        valor = valor.replace(/\./g, '').replace(/,/g, '.');
                    }
                } else if (valor.includes(',') && !valor.includes('.')) {
                    // Solo comas - verificar si es decimal o miles
                    const partesComa = valor.split(',');
                    if (partesComa.length === 2 && partesComa[1].length <= 2) {
                        // Es separador decimal europeo
                        valor = valor.replace(/,/g, '.');
                    } else {
                        // Son separadores de miles
                        valor = valor.replace(/,/g, '');
                    }
                } else if (valor.includes('.') && !valor.includes(',')) {
                    // Solo puntos - verificar si es decimal o miles
                    const partesPunto = valor.split('.');
                    if (partesPunto.length === 2 && partesPunto[1].length <= 2) {
                        // Es separador decimal americano - mantener
                    } else {
                        // Son separadores de miles europeos
                        valor = valor.replace(/\./g, '');
                    }
                }
                
                // Limpiar caracteres no numéricos excepto punto decimal
                valor = valor.replace(/[^0-9.]/g, '');
                return parseFloat(valor) || 0;
            }
        }
        return 0;
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

    /**
     * Actualiza los campos calculados en el formulario
     */
    actualizarCamposCalculados(totalImpuesto, resultados) {
        // Campos posibles para el impuesto total - PRIORIDAD: campo 'impuesto' de tabla 'declara'
        const camposImpuesto = [
            'id_impuesto',           // Campo principal tabla declara
            'impuesto',              // Campo directo tabla declara  
            'id_impuesto_calculado', // Alternativo
            'impuesto_calculado'     // Alternativo
        ];

        let campoActualizado = false;
        
        // PRIORIDAD: Buscar campo 'impuesto' de tabla 'declara' primero
        const campoImpuestoTabla = document.getElementById('id_impuesto') || 
                                   document.querySelector('input[name="impuesto"]') ||
                                   document.getElementById('impuesto');
        
        if (campoImpuestoTabla) {
            campoImpuestoTabla.value = totalImpuesto.toFixed(2);
            campoImpuestoTabla.style.backgroundColor = '#e8f5e8';
            campoImpuestoTabla.style.fontWeight = 'bold';
            campoImpuestoTabla.style.color = '#155724';
            campoActualizado = true;
            console.log(`💰 Impuesto guardado en campo tabla 'declara': $${totalImpuesto.toFixed(2)}`);
        } else {
            // Fallback: buscar otros campos posibles
            for (const id of camposImpuesto) {
                const campo = document.getElementById(id);
                if (campo) {
                    campo.value = totalImpuesto.toFixed(2);
                    campo.style.backgroundColor = '#e8f5e8';
                    campoActualizado = true;
                    console.log(`💰 Impuesto actualizado en ${id}: $${totalImpuesto.toFixed(2)}`);
                    break;
                }
            }
        }

        if (!campoActualizado) {
            console.warn('⚠️ No se encontró campo para mostrar el impuesto calculado');
        }

        // Actualizar campos individuales si existen
        this.actualizarCampoIndividual('impuesto_industria', resultados.industria.impuestoTotal);
        this.actualizarCampoIndividual('impuesto_comercio', resultados.comercio.impuestoTotal);
        this.actualizarCampoIndividual('impuesto_servicios', resultados.servicios.impuestoTotal);
        this.actualizarCampoIndividual('impuesto_produccion', resultados.produccion.impuestoTotal);
    }

    /**
     * Actualiza un campo individual
     */
    actualizarCampoIndividual(campoId, valor) {
        const campo = document.getElementById(campoId);
        if (campo) {
            campo.value = valor.toFixed(2);
            campo.style.backgroundColor = '#f0f8ff';
        }
    }

    /**
     * Muestra feedback visual del cálculo
     */
    mostrarFeedbackCalculo(fieldName, totalImpuesto) {
        // Crear o actualizar indicador de cálculo
        let indicator = document.getElementById('calculo-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'calculo-indicator';
            indicator.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #28a745;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
                z-index: 1000;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            `;
            document.body.appendChild(indicator);
        }

        indicator.innerHTML = `
            <strong>✅ Cálculo Realizado</strong><br>
            Campo: ${fieldName}<br>
            Impuesto: $${totalImpuesto.toLocaleString('es-CO', {minimumFractionDigits: 2})}
        `;

        // Auto-ocultar después de 3 segundos
        setTimeout(() => {
            if (indicator) {
                indicator.style.opacity = '0';
                setTimeout(() => {
                    if (indicator && indicator.parentNode) {
                        indicator.parentNode.removeChild(indicator);
                    }
                }, 300);
            }
        }, 3000);
    }

    /**
     * Configura validación del formulario
     */
    setupFormValidation() {
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', (e) => {
                if (!this.validarFormulario()) {
                    e.preventDefault();
                    alert('Por favor complete todos los campos requeridos y verifique los cálculos.');
                }
            });
        }
    }

    /**
     * Valida el formulario antes del envío
     */
    validarFormulario() {
        const valoresVentas = this.obtenerValoresVentas();
        const totalVentas = Object.values(valoresVentas).reduce((sum, val) => sum + (val || 0), 0);
        
        if (totalVentas <= 0) {
            console.warn('⚠️ No hay valores de ventas ingresados');
            return false;
        }

        return true;
    }

    /**
     * Método público para recalcular
     */
    recalcular() {
        this.calcularEnTiempoReal('manual');
    }
    /**
     * Valida formato DECIMAL(16,2) para campos de ventas
     */
    validarDecimal16_2(numero) {
        // Máximo: 99,999,999,999,999.99 (14 enteros + 2 decimales)
        if (numero > 99999999999999.99) {
            return false;
        }
        
        return true;
    }
    
    /**
     * Obtiene valor validado para DECIMAL(16,2)
     */
    obtenerValorCampoValidado(campo) {
        // Mapear 'controlado' a 'controlado' si es necesario
        const campoReal = campo === 'controlado' ? 'controlado' : campo;
        const posiblesIds = [`id_${campoReal}`, `id_${campo}`, campoReal, campo, `${campoReal}_input`, `${campo}_input`];
        
        for (const id of posiblesIds) {
            const input = document.getElementById(id);
            if (input && input.value) {
                let valor = input.value;
                
                // Detectar formato europeo vs americano (igual que en obtenerValorCampo)
                const tienePuntoYComa = valor.includes('.') && valor.includes(',');
                const ultimoPunto = valor.lastIndexOf('.');
                const ultimaComa = valor.lastIndexOf(',');
                
                if (tienePuntoYComa) {
                    // Determinar cuál es el separador decimal
                    if (ultimoPunto > ultimaComa) {
                        // Formato americano: 1,234.56
                        valor = valor.replace(/,/g, '');
                    } else {
                        // Formato europeo: 1.234,56
                        valor = valor.replace(/\./g, '').replace(/,/g, '.');
                    }
                } else if (valor.includes(',') && !valor.includes('.')) {
                    // Solo comas - verificar si es decimal o miles
                    const partesComa = valor.split(',');
                    if (partesComa.length === 2 && partesComa[1].length <= 2) {
                        // Es separador decimal europeo
                        valor = valor.replace(/,/g, '.');
                    } else {
                        // Son separadores de miles
                        valor = valor.replace(/,/g, '');
                    }
                } else if (valor.includes('.') && !valor.includes(',')) {
                    // Solo puntos - verificar si es decimal o miles
                    const partesPunto = valor.split('.');
                    if (partesPunto.length === 2 && partesPunto[1].length <= 2) {
                        // Es separador decimal americano - mantener
                    } else {
                        // Son separadores de miles europeos
                        valor = valor.replace(/\./g, '');
                    }
                }
                
                // Limpiar caracteres no numéricos excepto punto decimal
                valor = valor.replace(/[^0-9.]/g, '');
                const numero = parseFloat(valor) || 0;
                
                // Validar formato DECIMAL(16,2)
                if (!this.validarDecimal16_2(numero)) {
                    console.warn(` Valor excede DECIMAL(16,2): ${numero}`);
                    return 0;
                }
                
                return numero;
            }
        }
        return 0;
    }
}

// Inicializar cuando el DOM esté listo
let declaracionVolumenInteractivo;
document.addEventListener('DOMContentLoaded', () => {
    declaracionVolumenInteractivo = new DeclaracionVolumenInteractivo();
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

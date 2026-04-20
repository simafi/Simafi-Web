
/* Última actualización: 2025-09-22 10:52:11 - Timestamp: 1758559931 */
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
        // Inicializar sistema de variables ocultas
        this.variablesOcultas = {};
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
            // Cargar tarifas para categoría 1 (Ventas Mercadería)
            const response1 = await fetch('/tributario/api-tarifas-ics/?categoria=1');
            // Cargar tarifas para categoría 2 (Ventas Productos Controlados)
            const response2 = await fetch('/tributario/api-tarifas-ics/?categoria=2');
            
            if (response1.ok && response2.ok) {
                const data1 = await response1.json();
                const data2 = await response2.json();
                this.tarifas = data1.tarifas || [];
                this.tarifasControlados = data2.tarifas || [];
            } else {
                throw new Error('No se pudieron cargar las tarifas del servidor');
            }
        } catch (error) {
            console.warn('Usando tarifas por defecto:', error);
            // Tarifas por defecto para categoría 1 (Ventas Mercadería)
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
            
            // Tarifas por defecto para categoría 2 (Ventas Productos Controlados)
            // NOTA: Estas se reemplazan con las tarifas reales de la tabla tarifasimptoics
            this.tarifasControlados = [];
        }
        
        this.tarifas.sort((a, b) => a.rango1 - b.rango1);
        this.tarifasControlados.sort((a, b) => a.rango1 - b.rango1);
        console.log('📊 Tarifas cargadas:', this.tarifas.length, 'rangos (categoría 1)');
        console.log('📊 Tarifas controlados cargadas:', this.tarifasControlados.length, 'rangos (categoría 2)');
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
            'valorexcento', // Valores Exentos
            'controlado',  // Ventas Productos Controlados
            'ventas_produccion', // Alternativo
            'rubro_produccion',   // Alternativo
            'unidad',      // Campo Unidad
            'factor',      // Campo Factor
            'ajuste'       // Campo Ajuste Interanual
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
        
        // Listeners básicos configurados
        
        // AGREGAR LISTENERS PARA CAMBIOS EN COMBOBOX MES Y TIPO
        this.setupComboboxListeners();
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

        // Buscar inputs que contengan "controlado"
        const controladoInputs = document.querySelectorAll('input[name*="controlado"], input[id*="controlado"]');
        controladoInputs.forEach(input => {
            if (!input.hasAttribute('data-calculator-attached')) {
                this.addCalculationListeners(input, input.name || input.id);
                input.setAttribute('data-calculator-attached', 'true');
                console.log(`✅ Campo de productos controlados detectado: ${input.name || input.id}`);
            }
        });

        // Buscar inputs que contengan "valorexcento" o "exento"
        const exentoInputs = document.querySelectorAll('input[name*="valorexcento"], input[id*="valorexcento"], input[name*="exento"], input[id*="exento"]');
        exentoInputs.forEach(input => {
            if (!input.hasAttribute('data-calculator-attached')) {
                this.addCalculationListeners(input, input.name || input.id);
                input.setAttribute('data-calculator-attached', 'true');
                console.log(`✅ Campo de valores exentos detectado: ${input.name || input.id}`);
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
     * Calcula impuestos en tiempo real usando sistema de variables ocultas
     */
    calcularEnTiempoReal(fieldName) {
        if (this.tarifas.length === 0) {
            console.warn('Tarifas no cargadas aún');
            return;
        }

        console.log(`🔄 Calculando impuesto INDEPENDIENTE para campo: ${fieldName}`);
        
        // Inicializar variables ocultas si no existen
        if (!this.variablesOcultas) {
            this.variablesOcultas = {};
        }

        // Obtener valores de todos los campos
        const valoresVentas = this.obtenerValoresVentas();
        console.log('📊 Valores de ventas obtenidos:', valoresVentas);
        
        // PASO 1: Calcular cada impuesto INDEPENDIENTEMENTE y guardar en variables ocultas
        this.calcularYGuardarImpuestosIndependientes(valoresVentas);
        
        // PASO 2: Hacer una sola suma usando las variables ocultas
        const totalImpuesto = this.sumarImpuestosDesdeVariablesOcultas();
        
        // PASO 3: Actualizar campo de impuesto
        this.actualizarCampoImpuesto(totalImpuesto);
        
        // PASO 4: Mostrar feedback visual
        this.mostrarFeedbackCalculo(fieldName, totalImpuesto);

        // PASO 5: Actualizar campos ocultos del formulario HTML
        this.actualizarCamposOcultosFormulario();
        
        // PASO 6: Disparar evento personalizado
        document.dispatchEvent(new CustomEvent('calculoICSRealizado', {
            detail: {
                campo: fieldName,
                totalImpuesto: totalImpuesto,
                variablesOcultas: this.variablesOcultas
            }
        }));
    }

    /**
     * Calcula cada impuesto independientemente y los guarda en variables ocultas
     */
    calcularYGuardarImpuestosIndependientes(valoresVentas) {
        console.log('🧮 CALCULANDO IMPUESTOS INDEPENDIENTES:');
        
        // 1. Ventas Rubro Producción (ventai)
        const valorVentai = valoresVentas.ventai || 0;
        const impuestoVentai = valorVentai > 0 ? this.calcularImpuestoICS(valorVentai).impuestoTotal : 0;
        this.variablesOcultas.ventai_base = valorVentai;
        this.variablesOcultas.ventai_impuesto = impuestoVentai;
        console.log(`   📊 Ventas Rubro Producción: L. ${valorVentai.toLocaleString('es-HN', {minimumFractionDigits: 2})} → Impuesto: L. ${impuestoVentai.toFixed(2)}`);
        
        // 2. Ventas Mercadería (ventac)
        const valorVentac = valoresVentas.ventac || 0;
        const impuestoVentac = valorVentac > 0 ? this.calcularImpuestoICS(valorVentac).impuestoTotal : 0;
        this.variablesOcultas.ventac_base = valorVentac;
        this.variablesOcultas.ventac_impuesto = impuestoVentac;
        console.log(`   📊 Ventas Mercadería: L. ${valorVentac.toLocaleString('es-HN', {minimumFractionDigits: 2})} → Impuesto: L. ${impuestoVentac.toFixed(2)}`);
        
        // 3. Ventas por Servicios (ventas)
        const valorVentas = valoresVentas.ventas || 0;
        const impuestoVentas = valorVentas > 0 ? this.calcularImpuestoICS(valorVentas).impuestoTotal : 0;
        this.variablesOcultas.ventas_base = valorVentas;
        this.variablesOcultas.ventas_impuesto = impuestoVentas;
        console.log(`   📊 Ventas por Servicios: L. ${valorVentas.toLocaleString('es-HN', {minimumFractionDigits: 2})} → Impuesto: L. ${impuestoVentas.toFixed(2)}`);
        
        // 4. Ventas Productos Controlados (controlado)
        const valorControlado = valoresVentas.controlado || 0;
        const impuestoControlado = valorControlado > 0 ? this.calcularImpuestoICSControlados(valorControlado).impuestoTotal : 0;
        this.variablesOcultas.controlado_base = valorControlado;
        this.variablesOcultas.controlado_impuesto = impuestoControlado;
        console.log(`   📊 Productos Controlados: L. ${valorControlado.toLocaleString('es-HN', {minimumFractionDigits: 2})} → Impuesto: L. ${impuestoControlado.toFixed(2)}`);
        
        // 5. Unidad × Factor (usando función específica)
        const valorUnidad = valoresVentas.unidad || 0;
        const valorFactor = valoresVentas.factor || 0;
        const resultadoUnidadFactor = this.calcularImpuestoUnidadFactor(valorUnidad, valorFactor);
        const impuestoUnidadFactor = resultadoUnidadFactor.impuestoTotal;
        this.variablesOcultas.unidad_base = valorUnidad;
        this.variablesOcultas.factor_base = valorFactor;
        this.variablesOcultas.unidadFactor_impuesto = impuestoUnidadFactor;
        console.log(`   📊 Unidad × Factor: ${valorUnidad} × ${valorFactor} = L. ${impuestoUnidadFactor.toFixed(2)}`);
        
        // 6. Ajuste Interanual (valor directo, no se calcula impuesto)
        const valorAjuste = valoresVentas.ajuste || 0;
        this.variablesOcultas.ajuste_base = valorAjuste;
        this.variablesOcultas.ajuste_impuesto = valorAjuste; // El ajuste se suma directamente
        console.log(`   📊 Ajuste Interanual: L. ${valorAjuste.toLocaleString('es-HN', {minimumFractionDigits: 2})}`);
        
        console.log('✅ Variables ocultas actualizadas:', this.variablesOcultas);
    }

    /**
     * Suma todos los impuestos desde las variables ocultas
     */
    sumarImpuestosDesdeVariablesOcultas() {
        console.log('🎯 SUMANDO IMPUESTOS DESDE VARIABLES OCULTAS:');
        
        const impuestoVentai = this.variablesOcultas.ventai_impuesto || 0;
        const impuestoVentac = this.variablesOcultas.ventac_impuesto || 0;
        const impuestoVentas = this.variablesOcultas.ventas_impuesto || 0;
        const impuestoControlado = this.variablesOcultas.controlado_impuesto || 0;
        const impuestoUnidadFactor = this.variablesOcultas.unidadFactor_impuesto || 0;
        const impuestoAjuste = this.variablesOcultas.ajuste_impuesto || 0;
        
        // Verificar tipos y convertir a números
        const ventai = parseFloat(impuestoVentai) || 0;
        const ventac = parseFloat(impuestoVentac) || 0;
        const ventas = parseFloat(impuestoVentas) || 0;
        const controlado = parseFloat(impuestoControlado) || 0;
        const unidadFactor = parseFloat(impuestoUnidadFactor) || 0;
        const ajuste = parseFloat(impuestoAjuste) || 0;
        
        console.log('🔢 IMPUESTOS INDIVIDUALES (convertidos a números):');
        console.log(`   • Ventas Rubro Producción: L. ${ventai.toFixed(2)}`);
        console.log(`   • Ventas Mercadería: L. ${ventac.toFixed(2)}`);
        console.log(`   • Ventas por Servicios: L. ${ventas.toFixed(2)}`);
        console.log(`   • Productos Controlados: L. ${controlado.toFixed(2)}`);
        console.log(`   • Unidad × Factor: L. ${unidadFactor.toFixed(2)}`);
        console.log(`   • Ajuste Interanual: L. ${ajuste.toFixed(2)}`);
        
        // Suma total
        const totalImpuesto = ventai + ventac + ventas + controlado + unidadFactor + ajuste;
        
        console.log('🎯 SUMA PASO A PASO:');
        console.log(`   Paso 1: ${ventai.toFixed(2)}`);
        console.log(`   Paso 2: ${ventai.toFixed(2)} + ${ventac.toFixed(2)} = ${(ventai + ventac).toFixed(2)}`);
        console.log(`   Paso 3: ${(ventai + ventac).toFixed(2)} + ${ventas.toFixed(2)} = ${(ventai + ventac + ventas).toFixed(2)}`);
        console.log(`   Paso 4: ${(ventai + ventac + ventas).toFixed(2)} + ${controlado.toFixed(2)} = ${(ventai + ventac + ventas + controlado).toFixed(2)}`);
        console.log(`   Paso 5: ${(ventai + ventac + ventas + controlado).toFixed(2)} + ${unidadFactor.toFixed(2)} = ${(ventai + ventac + ventas + controlado + unidadFactor).toFixed(2)}`);
        console.log(`   Paso 6: ${(ventai + ventac + ventas + controlado + unidadFactor).toFixed(2)} + ${ajuste.toFixed(2)} = ${totalImpuesto.toFixed(2)}`);
        
        console.log(`💰 TOTAL IMPUESTO FINAL: L. ${totalImpuesto.toFixed(2)}`);
        
        // CALCULAR Y ACTUALIZAR MULTA AUTOMÁTICAMENTE
        this.calcularYActualizarMultaAutomaticamente(totalImpuesto);
        
        return totalImpuesto;
    }

    /**
     * Calcula y actualiza la multa automáticamente basado en el impuesto calculado
     */
    calcularYActualizarMultaAutomaticamente(impuestoCalculado) {
        console.log('🧮 CALCULANDO MULTA AUTOMÁTICAMENTE');
        console.log(`   Impuesto base: L. ${impuestoCalculado.toFixed(2)}`);
        
        // Solo calcular multa si el impuesto es mayor a cero
        if (impuestoCalculado <= 0) {
            console.log('   ⚠️ Impuesto es 0 o negativo, multa = 0.00');
            this.actualizarCampoMulta(0);
            return;
        }
        
        // Calcular multa según las reglas
        const multa = this.calcularMultaSegunReglas(impuestoCalculado);
        
        // Actualizar el campo de multa
        this.actualizarCampoMulta(multa);
    }

    /**
     * Calcula la multa según las reglas de negocio (VALIDACIÓN NUMÉRICA)
     */
    calcularMultaSegunReglas(impuestoCalculado) {
        const campoMes = document.getElementById('id_mes');
        const campoTipo = document.getElementById('id_tipo');
        
        if (!campoMes || !campoTipo) {
            console.warn('⚠️ No se encontraron campos mes o tipo');
            return 0;
        }
        
        // LECTURA NUMÉRICA EXACTA
        const mes = parseInt(campoMes.value) || 0;
        const tipo = parseInt(campoTipo.value) || 0;
        
        console.log(`🔍 VALIDACIÓN NUMÉRICA DE MULTA:`);
        console.log(`   Mes (numérico): ${mes} ${mes === 1 ? '(ENERO)' : mes > 1 && mes <= 12 ? '(≠ ENERO)' : '(INVÁLIDO)'}`);
        console.log(`   Tipo (numérico): ${tipo} ${tipo === 1 ? '(NORMAL)' : tipo === 2 ? '(APERTURA)' : '(INVÁLIDO)'}`);
        console.log(`   Impuesto: L. ${impuestoCalculado.toFixed(2)}`);
        
        let multa = 0;
        let reglaAplicada = '';
        
        // VALIDACIÓN NUMÉRICA EXACTA
        console.log(`🧮 APLICANDO VALIDACIONES NUMÉRICAS:`);
        
        // REGLA 1: mes === 1 (Enero) → multa = 0.00
        if (mes === 1) {
            multa = 0;
            reglaAplicada = `Mes = 1 (Enero): Multa = 0.00`;
            console.log(`   ✅ ${reglaAplicada}`);
        }
        // REGLA 2: mes !== 1 AND tipo === 1 (Normal) → multa = impuesto
        else if (mes !== 1 && tipo === 1) {
            multa = impuestoCalculado;
            reglaAplicada = `Mes ≠ 1 (${mes}) + Tipo = 1 (Normal): Multa = Impuesto`;
            console.log(`   ⚠️ ${reglaAplicada} = L. ${multa.toFixed(2)}`);
        }
        // REGLA 3: mes !== 1 AND tipo !== 1 → multa = 0.00
        else if (mes !== 1 && tipo !== 1) {
            multa = 0;
            reglaAplicada = `Mes ≠ 1 (${mes}) + Tipo ≠ 1 (${tipo}): Multa = 0.00`;
            console.log(`   ✅ ${reglaAplicada}`);
        }
        // REGLA DEFAULT: Valores inválidos
        else {
            multa = 0;
            reglaAplicada = `Valores inválidos (Mes: ${mes}, Tipo: ${tipo}): Multa = 0.00`;
            console.log(`   ⚠️ ${reglaAplicada}`);
        }
        
        console.log(`💰 MULTA FINAL: L. ${multa.toFixed(2)} | REGLA: ${reglaAplicada}`);
        return multa;
    }

    /**
     * Actualiza el campo de multa en la interfaz
     */
    actualizarCampoMulta(valorMulta) {
        const campoMulta = document.getElementById('id_multadecla');
        
        if (campoMulta) {
            const valorAnterior = parseFloat(campoMulta.value) || 0;
            campoMulta.value = valorMulta.toFixed(2);
            
            // Aplicar estilos según el valor
            if (valorMulta > 0) {
                campoMulta.style.backgroundColor = '#fff3cd';
                campoMulta.style.borderColor = '#ffa000';
                campoMulta.style.color = '#856404';
            } else {
                campoMulta.style.backgroundColor = '#e8f5e8';
                campoMulta.style.borderColor = '#28a745';
                campoMulta.style.color = '#155724';
            }
            
            // Log del cambio
            if (valorAnterior !== valorMulta) {
                console.log(`💰 Campo multa actualizado: L. ${valorAnterior.toFixed(2)} → L. ${valorMulta.toFixed(2)}`);
            }
        } else {
            console.error('❌ Campo multa no encontrado');
        }
    }

    /**
     * Recalcula la multa cuando cambian los combobox (VALIDACIÓN NUMÉRICA)
     */
    recalcularMultaPorCambioCombobox() {
        console.log('🔄 RECALCULANDO MULTA POR CAMBIO EN COMBOBOX');
        
        // PASO 1: Leer valores actuales de combobox
        const campoMes = document.getElementById('id_mes');
        const campoTipo = document.getElementById('id_tipo');
        const campoImpuesto = document.getElementById('id_impuesto');
        
        console.log('📊 LEYENDO VALORES DE COMBOBOX:');
        
        if (campoMes) {
            console.log(`   Campo MES encontrado: ${campoMes.tagName}, valor="${campoMes.value}"`);
        } else {
            console.error('   ❌ Campo MES no encontrado');
        }
        
        if (campoTipo) {
            console.log(`   Campo TIPO encontrado: ${campoTipo.tagName}, valor="${campoTipo.value}"`);
            if (campoTipo.tagName === 'SELECT') {
                console.log(`   Opción seleccionada: "${campoTipo.options[campoTipo.selectedIndex]?.text || 'Ninguna'}"`);
            }
        } else {
            console.error('   ❌ Campo TIPO no encontrado');
        }
        
        // PASO 2: Convertir a números
        const mes = parseInt(campoMes?.value) || 0;
        const tipo = parseInt(campoTipo?.value) || 0;
        const impuesto = parseFloat(campoImpuesto?.value) || 0;
        
        console.log('🔢 VALORES CONVERTIDOS A NÚMEROS:');
        console.log(`   Mes: ${mes} ${mes === 1 ? '(ENERO)' : '(≠ ENERO)'}`);
        console.log(`   Tipo: ${tipo} ${tipo === 1 ? '(NORMAL)' : tipo === 2 ? '(APERTURA)' : '(OTRO)'}`);
        console.log(`   Impuesto: L. ${impuesto.toFixed(2)}`);
        
        // PASO 3: Aplicar validación de multa
        if (impuesto > 0) {
            console.log('✅ Impuesto > 0, aplicando reglas de multa');
            const nuevaMulta = this.calcularMultaSegunReglas(impuesto);
            this.actualizarCampoMulta(nuevaMulta);
        } else {
            console.log('⚠️ Impuesto ≤ 0, multa = 0.00');
            this.actualizarCampoMulta(0);
        }
    }

    /**
     * Configura listeners para cambios en combobox mes y tipo
     */
    setupComboboxListeners() {
        const campoMes = document.getElementById('id_mes');
        const campoTipo = document.getElementById('id_tipo');
        
        if (campoMes) {
            campoMes.addEventListener('change', () => {
                console.log('🔄 Mes cambió - Recalculando multa');
                this.recalcularMultaPorCambioCombobox();
            });
            console.log('✅ Listener agregado al combobox MES');
        } else {
            console.warn('⚠️ Combobox MES no encontrado');
        }
        
        if (campoTipo) {
            campoTipo.addEventListener('change', () => {
                console.log('🔄 Tipo cambió - Recalculando multa');
                this.recalcularMultaPorCambioCombobox();
            });
            console.log('✅ Listener agregado al combobox TIPO');
        } else {
            console.warn('⚠️ Combobox TIPO no encontrado');
        }
    }

    /**
     * Obtiene el nombre del mes
     */
    getNombreMes(mes) {
        const meses = ['Sin seleccionar', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
        return meses[mes] || 'Desconocido';
    }

    /**
     * Obtiene el nombre del tipo
     */
    getNombreTipo(tipo) {
        const tipos = ['Sin seleccionar', 'Normal', 'Apertura'];
        return tipos[tipo] || 'Desconocido';
    }

    /**
     * Actualiza el campo de impuesto en la interfaz
     */
    actualizarCampoImpuesto(totalImpuesto) {
        const camposImpuesto = [
            'id_impuesto',           // Campo principal
            'impuesto',              // Campo directo
            'id_impuesto_calculado', // Alternativo
            'impuesto_calculado'     // Alternativo
        ];

        let campoActualizado = false;
        
        for (const id of camposImpuesto) {
            const campo = document.getElementById(id);
            if (campo) {
                campo.value = totalImpuesto.toFixed(2);
                campo.style.backgroundColor = '#e8f5e8';
                campo.style.fontWeight = 'bold';
                campo.style.color = '#155724';
                campoActualizado = true;
                console.log(`💰 Campo impuesto actualizado (${id}): L. ${totalImpuesto.toFixed(2)}`);
                break;
            }
        }

        if (!campoActualizado) {
            console.warn('⚠️ No se encontró campo para mostrar el impuesto calculado');
        }
    }

    /**
     * Obtiene valores de todos los campos de ventas y controlado
     */
    obtenerValoresVentas() {
        // Solo campos de ventas reales (no incluir unidad, factor, ajuste)
        const campos = ['ventai', 'ventac', 'ventas', 'valorexcento', 'controlado', 'unidad', 'factor', 'ajuste'];
        const valores = {};

        campos.forEach(campo => {
            const valor = this.obtenerValorCampoValidado(campo);
            console.log(`🔍 Campo ${campo}: valor obtenido = ${valor}`);
            
            if (valor > 0) {
                valores[campo] = valor;
                console.log(`✅ Campo ${campo} incluido con valor: ${valor}`);
            }
        });

        console.log('📋 Valores finales de ventas:', valores);
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
                
                // PARSING MEJORADO DE FORMATOS NUMÉRICOS (MISMA LÓGICA)
                // Caso 1: "50,000.00" (formato americano con miles y decimales)
                if (/^\d{1,3}(,\d{3})+\.\d{1,2}$/.test(valor)) {
                    valor = valor.replace(/,/g, '');
                }
                // Caso 2: "50,000" (formato americano con miles, sin decimales)
                else if (/^\d{1,3}(,\d{3})+$/.test(valor)) {
                    valor = valor.replace(/,/g, '');
                }
                // Caso 3: "50.000,00" (formato europeo con miles y decimales)
                else if (/^\d{1,3}(\.\d{3})+,\d{1,2}$/.test(valor)) {
                    valor = valor.replace(/\./g, '').replace(',', '.');
                }
                // Caso 4: "50.000" (formato europeo con miles, sin decimales)
                else if (/^\d{1,3}(\.\d{3})+$/.test(valor)) {
                    valor = valor.replace(/\./g, '');
                }
                // Caso 5: "50.00" (formato americano simple con decimales)
                else if (/^\d+\.\d{1,2}$/.test(valor)) {
                    // Mantener como está - formato americano válido
                }
                // Caso 6: "50,00" (formato europeo simple con decimales)
                else if (/^\d+,\d{1,2}$/.test(valor)) {
                    valor = valor.replace(',', '.');
                }
                // Caso 7: Solo números
                else if (/^\d+$/.test(valor)) {
                    // Mantener como está
                }
                // Caso 8: Formatos mixtos o complejos
                else {
                    const tienePuntoYComa = valor.includes('.') && valor.includes(',');
                    const ultimoPunto = valor.lastIndexOf('.');
                    const ultimaComa = valor.lastIndexOf(',');
                    
                    if (tienePuntoYComa) {
                        if (ultimoPunto > ultimaComa) {
                            // Formato americano: 1,234.56
                            valor = valor.replace(/,/g, '');
                        } else {
                            // Formato europeo: 1.234,56
                            valor = valor.replace(/\./g, '').replace(',', '.');
                        }
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
     * Calcula el impuesto ICS para productos controlados (categoría 2)
     */
    calcularImpuestoICSControlados(valorVentas) {
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

        // Usar tarifas específicas para productos controlados (categoría 2)
        const tarifasAplicar = this.tarifasControlados || this.tarifas;

        for (const tarifa of tarifasAplicar) {
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
                descripcion: tarifa.descripcion,
                categoria: tarifa.categoria || "2"
            });
        }

        return {
            impuestoTotal: Math.round(impuestoTotal * 100) / 100,
            detalleCalculo: detalleCalculo,
            valorVentas: valorVentas
        };
    }

    calcularImpuestoUnidadFactor(valorUnidad, valorFactor) {
        // Validar que ambos valores sean mayores a cero
        if (!valorUnidad || valorUnidad <= 0 || !valorFactor || valorFactor <= 0) {
            console.log('⚠️ Unidad o Factor no válidos - Unidad:', valorUnidad, 'Factor:', valorFactor);
            return { 
                impuestoTotal: 0, 
                detalleCalculo: [], 
                valorUnidad: valorUnidad || 0, 
                valorFactor: valorFactor || 0,
                valorCalculado: 0
            };
        }

        // Multiplicación simple: Factor × Unidad con redondeo a 2 dígitos
        const valorCalculado = valorFactor * valorUnidad;
        
        // Redondear a 2 dígitos decimales
        const valorCalculadoRedondeado = Math.round(valorCalculado * 100) / 100;
        
        console.log(`🧮 Cálculo Factor × Unidad:`);
        console.log(`   Factor: ${valorFactor}`);
        console.log(`   Unidad: ${valorUnidad}`);
        console.log(`   Resultado: ${valorFactor} × ${valorUnidad} = ${valorCalculado}`);
        console.log(`   Resultado redondeado: ${valorCalculadoRedondeado.toFixed(2)}`);

        // NO aplicar tarifas ICS - es una multiplicación simple
        // El resultado se suma directamente al total de impuestos
        const impuestoTotal = valorCalculadoRedondeado;
        
        const detalleCalculo = [{
            descripcion: `Factor × Unidad (${valorFactor} × ${valorUnidad})`,
            valorUnidad: valorUnidad,
            valorFactor: valorFactor,
            valorCalculado: valorCalculadoRedondeado,
            impuestoAplicado: impuestoTotal
        }];

        console.log(`✅ Valor calculado para Factor × Unidad: L. ${impuestoTotal.toFixed(2)}`);

        return {
            impuestoTotal: impuestoTotal,
            detalleCalculo: detalleCalculo,
            valorUnidad: valorUnidad,
            valorFactor: valorFactor,
            valorCalculado: valorCalculadoRedondeado
        };
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
            Impuesto: L. ${totalImpuesto.toFixed(2)}
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
     * Configura validación del formulario - ELIMINADA COMPLETAMENTE
     */
    setupFormValidation() {
        // NO HACER NADA - Permitir que el formulario se envíe sin restricciones
        console.log('📝 Formulario configurado - SIN VALIDACIONES');
        console.log('✅ El formulario se enviará sin restricciones');
    }

    /**
     * Validación eliminada - No aplicar ninguna validación
     */
    validarFormularioMejorado() {
        // NO APLICAR NINGUNA VALIDACIÓN
        // Permitir el envío del formulario sin restricciones
        console.log('🔍 VALIDACIÓN ELIMINADA - Formulario se envía sin restricciones');
        
        return {
            esValido: true,
            mensajes: []
        };
    }

    /**
     * Validación eliminada - No aplicar ninguna validación
     */
    validarFormulario() {
        // NO APLICAR NINGUNA VALIDACIÓN
        // Permitir el envío del formulario sin restricciones
        console.log('🔍 VALIDACIÓN ELIMINADA - Formulario se envía sin restricciones');
        return true;
    }

    /**
     * Actualiza los campos ocultos del formulario HTML con las variables ocultas
     */
    actualizarCamposOcultosFormulario() {
        console.log('🔧 ACTUALIZANDO CAMPOS OCULTOS DEL FORMULARIO HTML');
        
        // Actualizar todos los campos ocultos basados en las variables ocultas
        Object.keys(this.variablesOcultas).forEach(key => {
            const campoOculto = document.getElementById(`hidden_${key}`);
            if (campoOculto) {
                const valorAnterior = campoOculto.value;
                campoOculto.value = this.variablesOcultas[key];
                console.log(`🔧 Campo oculto actualizado: hidden_${key} = ${this.variablesOcultas[key]} (anterior: ${valorAnterior})`);
            } else {
                console.warn(`⚠️ Campo oculto no encontrado: hidden_${key}`);
            }
        });
        
        console.log('✅ Campos ocultos del formulario HTML actualizados');
    }

    /**
     * Método público para recalcular
     */
    recalcular() {
        this.calcularEnTiempoReal('manual');
        
        // También recalcular Valor Base con tasas si la función está disponible
        if (window.recalcularValorBaseConTasas) {
            window.recalcularValorBaseConTasas();
        }
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
        
        console.log(`🔍 Buscando campo ${campo} con IDs posibles:`, posiblesIds);
        
        for (const id of posiblesIds) {
            const input = document.getElementById(id);
            console.log(`🔍 Probando ID ${id}:`, input ? `encontrado con valor "${input.value}"` : 'no encontrado');
            
            if (input && input.value) {
                let valor = input.value;
                
                // PARSING MEJORADO DE FORMATOS NUMÉRICOS
                console.log(`🔍 Parsing valor original: "${valor}"`);
                
                // Caso 1: "50,000.00" (formato americano con miles y decimales)
                if (/^\d{1,3}(,\d{3})+\.\d{1,2}$/.test(valor)) {
                    valor = valor.replace(/,/g, '');
                    console.log(`✅ Formato americano detectado: "${input.value}" → "${valor}"`);
                }
                // Caso 2: "50,000" (formato americano con miles, sin decimales)
                else if (/^\d{1,3}(,\d{3})+$/.test(valor)) {
                    valor = valor.replace(/,/g, '');
                    console.log(`✅ Formato americano sin decimales: "${input.value}" → "${valor}"`);
                }
                // Caso 3: "50.000,00" (formato europeo con miles y decimales)
                else if (/^\d{1,3}(\.\d{3})+,\d{1,2}$/.test(valor)) {
                    valor = valor.replace(/\./g, '').replace(',', '.');
                    console.log(`✅ Formato europeo detectado: "${input.value}" → "${valor}"`);
                }
                // Caso 4: "50.000" (formato europeo con miles, sin decimales)
                else if (/^\d{1,3}(\.\d{3})+$/.test(valor)) {
                    valor = valor.replace(/\./g, '');
                    console.log(`✅ Formato europeo sin decimales: "${input.value}" → "${valor}"`);
                }
                // Caso 5: "50.00" (formato americano simple con decimales)
                else if (/^\d+\.\d{1,2}$/.test(valor)) {
                    // Mantener como está - formato americano válido
                    console.log(`✅ Formato americano simple: "${input.value}" → "${valor}"`);
                }
                // Caso 6: "50,00" (formato europeo simple con decimales)
                else if (/^\d+,\d{1,2}$/.test(valor)) {
                    valor = valor.replace(',', '.');
                    console.log(`✅ Formato europeo simple: "${input.value}" → "${valor}"`);
                }
                // Caso 7: Solo números
                else if (/^\d+$/.test(valor)) {
                    console.log(`✅ Solo números: "${input.value}" → "${valor}"`);
                }
                // Caso 8: Formatos mixtos o complejos
                else {
                    const tienePuntoYComa = valor.includes('.') && valor.includes(',');
                    const ultimoPunto = valor.lastIndexOf('.');
                    const ultimaComa = valor.lastIndexOf(',');
                    
                    if (tienePuntoYComa) {
                        if (ultimoPunto > ultimaComa) {
                            // Formato americano: 1,234.56
                            valor = valor.replace(/,/g, '');
                            console.log(`✅ Formato mixto americano: "${input.value}" → "${valor}"`);
                        } else {
                            // Formato europeo: 1.234,56
                            valor = valor.replace(/\./g, '').replace(',', '.');
                            console.log(`✅ Formato mixto europeo: "${input.value}" → "${valor}"`);
                        }
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

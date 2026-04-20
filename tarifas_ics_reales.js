/**
 * Tarifas ICS reales obtenidas de tabla tarifasimptoics
 * Generado automáticamente desde base de datos
 */

const TARIFAS_ICS_REALES = [
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

// Función para obtener tarifas reales
function obtenerTarifasReales() {
    return TARIFAS_ICS_REALES;
}

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TARIFAS_ICS_REALES, obtenerTarifasReales };
}

// Script de Maestro de Negocios - Versión 3.0 FINAL
// Timestamp: 2025-10-07 13:30:00

console.log('✅ Script externo cargado: maestro_negocios_v3.js');
console.log('✅ Versión: 3.0-FINAL');
console.log('✅ URL Declaración correcta: /tributario/declaraciones/');

// Función para manejar declaración de volumen
window.manejarDeclaracionVolumenV3 = function() {
    const empresa = document.getElementById('id_empresa').value.trim();
    const rtm = document.getElementById('id_rtm').value.trim();
    const expe = document.getElementById('id_expe').value.trim();
    
    if (!empresa || !rtm || !expe) {
        alert('Los campos Empresa, RTM y Expediente son obligatorios para la declaración de volumen.');
        return;
    }
    
    // URL CORRECTA - Versión 3.0
    const url = `/tributario/declaraciones/?empresa=${encodeURIComponent(empresa)}&rtm=${encodeURIComponent(rtm)}&expe=${encodeURIComponent(expe)}`;
    
    console.log('🌐 Redirigiendo a declaración de volumen (V3):', url);
    window.location.href = url;
};

// Función para manejar configuración de tasas
window.manejarConfiguracionTasasV3 = function() {
    const empresa = document.getElementById('id_empresa').value.trim();
    const rtm = document.getElementById('id_rtm').value.trim();
    const expe = document.getElementById('id_expe').value.trim();
    
    if (!empresa || !rtm || !expe) {
        alert('Los campos Empresa, RTM y Expediente son obligatorios para la configuración de tasas.');
        return;
    }
    
    // URL CORRECTA - Versión 3.0
    const url = `/tributario/configurar-tasas-negocio/?empresa=${encodeURIComponent(empresa)}&rtm=${encodeURIComponent(rtm)}&expe=${encodeURIComponent(expe)}`;
    
    console.log('🌐 Redirigiendo a configuración de tasas (V3):', url);
    window.location.href = url;
};

console.log('✅ Funciones V3 registradas correctamente');



























































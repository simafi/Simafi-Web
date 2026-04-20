// Configuración del cursor de IA en español
// Este archivo contiene la configuración de idioma para el cursor de IA en JavaScript

const CURSOR_AI_CONFIG = {
    language: 'es',
    locale: 'es_ES',
    timezone: 'America/Tegucigalpa',
    dateFormat: 'DD/MM/YYYY',
    timeFormat: 'HH:mm:ss',
    datetimeFormat: 'DD/MM/YYYY HH:mm:ss',
    currency: 'HNL',
    decimalSeparator: ',',
    thousandsSeparator: '.',
    messages: {
        welcome: '¡Bienvenido al Sistema de Gestión de Negocios!',
        searchPlaceholder: 'Buscar negocio...',
        saveSuccess: 'Negocio guardado exitosamente',
        saveError: 'Error al guardar el negocio',
        deleteSuccess: 'Negocio eliminado exitosamente',
        deleteError: 'Error al eliminar el negocio',
        notFound: 'No se encontró el negocio',
        requiredFields: 'Los campos marcados con * son obligatorios',
        confirmDelete: '¿Está seguro que desea eliminar este negocio?',
        confirmUpdate: '¿Desea actualizar el negocio existente?',
        formCleared: 'Formulario limpiado. Puede realizar una nueva búsqueda.',
        loading: 'Cargando...',
        error: 'Error',
        success: 'Éxito',
        warning: 'Advertencia',
        info: 'Información',
        thinking: 'Pensando...',
        processing: 'Procesando su solicitud...',
        ready: 'Listo para ayudarle',
        notUnderstood: 'No entendí su solicitud, ¿puede reformularla?',
        helpAvailable: 'Estoy aquí para ayudarle. ¿En qué puedo asistirle?'
    },
    validation: {
        required: 'Este campo es obligatorio',
        invalidFormat: 'Formato inválido',
        minLength: 'Debe tener al menos {min} caracteres',
        maxLength: 'Debe tener máximo {max} caracteres',
        invalidEmail: 'Correo electrónico inválido',
        invalidDate: 'Fecha inválida',
        invalidNumber: 'Número inválido'
    },
    ui: {
        loadingText: 'Procesando...',
        noResults: 'No se encontraron resultados',
        backToMenu: 'Volver al menú principal',
        newRecord: 'Nuevo registro',
        editRecord: 'Editar registro',
        deleteRecord: 'Eliminar registro',
        saveRecord: 'Guardar registro',
        cancel: 'Cancelar',
        confirm: 'Confirmar',
        close: 'Cerrar',
        search: 'Buscar',
        filter: 'Filtrar',
        export: 'Exportar',
        import: 'Importar',
        refresh: 'Actualizar',
        print: 'Imprimir',
        help: 'Ayuda',
        settings: 'Configuración',
        logout: 'Cerrar sesión'
    }
};

// Función para obtener mensajes del cursor de IA
function getCursorMessage(key) {
    return CURSOR_AI_CONFIG.messages[key] || '';
}

// Función para obtener mensajes de validación
function getValidationMessage(key) {
    return CURSOR_AI_CONFIG.validation[key] || '';
}

// Función para obtener mensajes de UI
function getUIMessage(key) {
    return CURSOR_AI_CONFIG.ui[key] || '';
}

// Función para formatear fechas en español
function formatDateSpanish(date) {
    if (!date) return '';
    
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    
    return `${day}/${month}/${year}`;
}

// Función para formatear números en español
function formatNumberSpanish(number) {
    if (number === null || number === undefined) return '';
    
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// Función para mostrar mensajes del cursor de IA
function showCursorMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `mensaje mensaje-${type}`;
    messageDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.appendChild(messageDiv);
        
        // Remover el mensaje después de 5 segundos
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }
}

// Función para inicializar el cursor de IA en español
function initCursorAI() {
    console.log('Inicializando cursor de IA en español...');
    
    // Configurar el idioma del cursor
    document.documentElement.lang = 'es';
    
    // Agregar atributos de idioma a elementos específicos
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.setAttribute('lang', 'es');
    });
    
    // Mostrar mensaje de bienvenida
    showCursorMessage(getCursorMessage('welcome'), 'success');
    
    console.log('Cursor de IA configurado en español');
}

// Exportar configuración para uso global
if (typeof window !== 'undefined') {
    window.CURSOR_AI_CONFIG = CURSOR_AI_CONFIG;
    window.getCursorMessage = getCursorMessage;
    window.getValidationMessage = getValidationMessage;
    window.getUIMessage = getUIMessage;
    window.formatDateSpanish = formatDateSpanish;
    window.formatNumberSpanish = formatNumberSpanish;
    window.showCursorMessage = showCursorMessage;
    window.initCursorAI = initCursorAI;
} 
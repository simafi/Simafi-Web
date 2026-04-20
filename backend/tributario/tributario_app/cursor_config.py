# Configuración del cursor de IA en español
# Este archivo contiene la configuración de idioma para el cursor de IA

CURSOR_AI_CONFIG = {
    'language': 'es',
    'locale': 'es_ES',
    'timezone': 'America/Tegucigalpa',
    'date_format': '%d/%m/%Y',
    'time_format': '%H:%M:%S',
    'datetime_format': '%d/%m/%Y %H:%M:%S',
    'currency': 'HNL',
    'decimal_separator': ',',
    'thousands_separator': '.',
    'messages': {
        'welcome': '¡Bienvenido al Sistema de Gestión de Negocios!',
        'search_placeholder': 'Buscar negocio...',
        'save_success': 'Negocio guardado exitosamente',
        'save_error': 'Error al guardar el negocio',
        'delete_success': 'Negocio eliminado exitosamente',
        'delete_error': 'Error al eliminar el negocio',
        'not_found': 'No se encontró el negocio',
        'required_fields': 'Los campos marcados con * son obligatorios',
        'confirm_delete': '¿Está seguro que desea eliminar este negocio?',
        'confirm_update': '¿Desea actualizar el negocio existente?',
        'form_cleared': 'Formulario limpiado. Puede realizar una nueva búsqueda.',
        'loading': 'Cargando...',
        'error': 'Error',
        'success': 'Éxito',
        'warning': 'Advertencia',
        'info': 'Información'
    },
    'validation': {
        'required': 'Este campo es obligatorio',
        'invalid_format': 'Formato inválido',
        'min_length': 'Debe tener al menos {min} caracteres',
        'max_length': 'Debe tener máximo {max} caracteres',
        'invalid_email': 'Correo electrónico inválido',
        'invalid_date': 'Fecha inválida',
        'invalid_number': 'Número inválido'
    },
    'ui': {
        'loading_text': 'Procesando...',
        'no_results': 'No se encontraron resultados',
        'back_to_menu': 'Volver al menú principal',
        'new_record': 'Nuevo registro',
        'edit_record': 'Editar registro',
        'delete_record': 'Eliminar registro',
        'save_record': 'Guardar registro',
        'cancel': 'Cancelar',
        'confirm': 'Confirmar',
        'close': 'Cerrar',
        'search': 'Buscar',
        'filter': 'Filtrar',
        'export': 'Exportar',
        'import': 'Importar',
        'refresh': 'Actualizar',
        'print': 'Imprimir',
        'help': 'Ayuda',
        'settings': 'Configuración',
        'logout': 'Cerrar sesión'
    }
}

# Configuración específica para el cursor de IA
AI_CURSOR_CONFIG = {
    'language': 'es',
    'response_language': 'es',
    'interface_language': 'es',
    'date_format': 'DD/MM/YYYY',
    'time_format': 'HH:mm:ss',
    'number_format': {
        'decimal': ',',
        'thousands': '.',
        'currency': 'HNL'
    },
    'messages': {
        'thinking': 'Pensando...',
        'processing': 'Procesando su solicitud...',
        'ready': 'Listo para ayudarle',
        'error': 'Ha ocurrido un error',
        'success': 'Operación completada exitosamente',
        'not_understood': 'No entendí su solicitud, ¿puede reformularla?',
        'help_available': 'Estoy aquí para ayudarle. ¿En qué puedo asistirle?'
    }
}

def get_cursor_config():
    """Retorna la configuración del cursor de IA"""
    return CURSOR_AI_CONFIG

def get_ai_cursor_config():
    """Retorna la configuración específica del cursor de IA"""
    return AI_CURSOR_CONFIG

def get_message(key, config_type='cursor'):
    """Obtiene un mensaje específico según el tipo de configuración"""
    if config_type == 'cursor':
        return CURSOR_AI_CONFIG['messages'].get(key, '')
    elif config_type == 'ai':
        return AI_CURSOR_CONFIG['messages'].get(key, '')
    return '' 

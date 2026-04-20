"""
Configuración complementaria para tributario_app
Archivo de configuración adicional que no interfiere con los archivos principales
"""

# Configuraciones adicionales para el contexto de municipio
MUNICIPIO_DEFAULT = '0301'
MUNICIPIO_DESCRIPCION_DEFAULT = 'Municipio de Prueba'

# Configuraciones para formularios
FORM_MAX_LENGTH = {
    'codigo': 4,
    'descripcion': 200,
    'cuenta': 20,
    'cuentarez': 20,
    'tipo': 1,
    'empresa': 4
}

# Configuraciones para validaciones
VALIDACIONES = {
    'rubro_codigo_min_length': 2,
    'rubro_codigo_max_length': 4,
    'descripcion_min_length': 5,
    'descripcion_max_length': 200,
    'tipo_valores_validos': ['I', 'T']
}

# Configuraciones para AJAX
AJAX_CONFIG = {
    'timeout': 5000,  # 5 segundos
    'debounce_delay': 300,  # 300ms
    'retry_attempts': 3
}

# Configuraciones para mensajes
MENSAJES = {
    'exito_guardar': 'Registro guardado exitosamente',
    'exito_actualizar': 'Registro actualizado exitosamente',
    'exito_eliminar': 'Registro eliminado exitosamente',
    'error_validacion': 'Por favor, corrija los errores en el formulario',
    'error_guardar': 'Error al guardar el registro',
    'error_eliminar': 'Error al eliminar el registro',
    'confirmar_eliminar': '¿Está seguro de que desea eliminar este registro?'
}

# Configuraciones para estilos
ESTILOS = {
    'badge_impuestos': 'badge-primary',
    'badge_tasas': 'badge-info',
    'form_section_class': 'form-section',
    'section_title_class': 'section-title'
}




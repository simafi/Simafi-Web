from .cursor_config import get_cursor_config, get_ai_cursor_config

def cursor_ai_config(request):
    """
    Context processor para agregar la configuración del cursor de IA
    a todos los templates de Django
    """
    return {
        'cursor_config': get_cursor_config(),
        'ai_cursor_config': get_ai_cursor_config(),
        'ai_language': 'es',
        'ai_messages': get_cursor_config()['messages'],
        'ai_ui': get_cursor_config()['ui'],
        'ai_validation': get_cursor_config()['validation'],
    }

def municipio_context(request):
    """
    Context processor para hacer disponible el código de municipio en todas las plantillas
    """
    try:
        empresa = request.session.get('empresa', '')
        municipio_descripcion = request.session.get('municipio_descripcion', '')
    except AttributeError:
        # Si no hay sesión disponible (como en peticiones AJAX de prueba)
        empresa = '0301'
        municipio_descripcion = 'Municipio por defecto'
    
    return {
        'empresa': empresa,
        'municipio_descripcion': municipio_descripcion,
        'municipio_info': {
            'codigo': empresa,
            'descripcion': municipio_descripcion
        }
    } 

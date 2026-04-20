"""
Utilidades complementarias para tributario_app
Funciones de ayuda que no interfieren con el código principal
"""

def validar_codigo_rubro(codigo):
    """
    Valida que el código de rubro cumpla con los requisitos
    """
    if not codigo:
        return False, "El código es obligatorio"
    
    codigo = codigo.strip().upper()
    
    if len(codigo) < 2:
        return False, "El código debe tener al menos 2 caracteres"
    
    if len(codigo) > 4:
        return False, "El código no puede tener más de 4 caracteres"
    
    return True, codigo

def validar_descripcion(descripcion):
    """
    Valida que la descripción cumpla con los requisitos
    """
    if not descripcion:
        return False, "La descripción es obligatoria"
    
    descripcion = descripcion.strip()
    
    if len(descripcion) < 5:
        return False, "La descripción debe tener al menos 5 caracteres"
    
    if len(descripcion) > 200:
        return False, "La descripción no puede tener más de 200 caracteres"
    
    return True, descripcion

def validar_tipo(tipo):
    """
    Valida que el tipo sea válido
    """
    if not tipo:
        return False, "El tipo es obligatorio"
    
    tipo = tipo.strip().upper()
    
    if tipo not in ['I', 'T']:
        return False, "El tipo debe ser 'I' (Impuestos) o 'T' (Tasas)"
    
    return True, tipo

def formatear_mensaje_exito(accion, registro):
    """
    Formatea un mensaje de éxito
    """
    mensajes = {
        'guardar': f"✅ {registro} guardado exitosamente",
        'actualizar': f"✅ {registro} actualizado exitosamente",
        'eliminar': f"✅ {registro} eliminado exitosamente"
    }
    return mensajes.get(accion, f"✅ Operación completada exitosamente")

def formatear_mensaje_error(accion, error):
    """
    Formatea un mensaje de error
    """
    mensajes = {
        'guardar': f"❌ Error al guardar: {error}",
        'actualizar': f"❌ Error al actualizar: {error}",
        'eliminar': f"❌ Error al eliminar: {error}",
        'validacion': f"❌ Error de validación: {error}"
    }
    return mensajes.get(accion, f"❌ Error: {error}")

def obtener_badge_tipo(tipo):
    """
    Obtiene la clase CSS para el badge según el tipo
    """
    if tipo == 'I':
        return 'badge-primary'
    elif tipo == 'T':
        return 'badge-info'
    else:
        return 'badge-secondary'

def obtener_descripcion_tipo(tipo):
    """
    Obtiene la descripción del tipo
    """
    if tipo == 'I':
        return 'Impuestos'
    elif tipo == 'T':
        return 'Tasas'
    else:
        return 'Desconocido'




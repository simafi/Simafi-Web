from django import template
import re

register = template.Library()

@register.filter
def format_number(value):
    """
    Formatea un número agregando comas para separar miles y millones
    Siempre muestra .00 para números enteros
    """
    if value is None:
        return "0.00"
    
    try:
        # Convertir a float y formatear
        num = float(value)
        
        # Convertir a string con formato de miles y siempre 2 decimales
        formatted = "{:,.2f}".format(num)
        
        return formatted
    except (ValueError, TypeError):
        return str(value)

@register.filter
def split(value, arg):
    """
    Divide una cadena por el argumento dado
    """
    if value:
        return value.split(arg)
    return []

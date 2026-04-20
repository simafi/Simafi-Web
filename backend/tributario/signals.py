"""
Signals para el módulo tributario
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from .models import *  # Comentado para evitar conflictos de importación

# Aquí se pueden agregar los signals necesarios para el módulo tributario
# Por ejemplo, signals para cálculo automático de impuestos, notificaciones, etc.

@receiver(post_save, sender=None)
def tributario_post_save_handler(sender, instance, created, **kwargs):
    """
    Handler para eventos post_save en el módulo tributario
    """
    pass

@receiver(post_delete, sender=None)
def tributario_post_delete_handler(sender, instance, **kwargs):
    """
    Handler para eventos post_delete en el módulo tributario
    """
    pass










































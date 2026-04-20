"""
Signals para el módulo tesoreria
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

# Aquí se pueden agregar los signals necesarios para el módulo tesoreria
# Por ejemplo, signals para control de caja, notificaciones, etc.

@receiver(post_save, sender=None)
def tesoreria_post_save_handler(sender, instance, created, **kwargs):
    """
    Handler para eventos post_save en el módulo tesoreria
    """
    pass

@receiver(post_delete, sender=None)
def tesoreria_post_delete_handler(sender, instance, **kwargs):
    """
    Handler para eventos post_delete en el módulo tesoreria
    """
    pass









































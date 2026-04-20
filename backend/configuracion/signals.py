"""
Signals para el módulo configuracion
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

# Aquí se pueden agregar los signals necesarios para el módulo configuracion
# Por ejemplo, signals para auditoría de configuración, notificaciones, etc.

@receiver(post_save, sender=None)
def configuracion_post_save_handler(sender, instance, created, **kwargs):
    """
    Handler para eventos post_save en el módulo configuracion
    """
    pass

@receiver(post_delete, sender=None)
def configuracion_post_delete_handler(sender, instance, **kwargs):
    """
    Handler para eventos post_delete en el módulo configuracion
    """
    pass









































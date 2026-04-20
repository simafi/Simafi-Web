"""
Signals para el módulo api
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

# Aquí se pueden agregar los signals necesarios para el módulo api
# Por ejemplo, signals para auditoría de API, notificaciones, etc.

@receiver(post_save, sender=None)
def api_post_save_handler(sender, instance, created, **kwargs):
    """
    Handler para eventos post_save en el módulo api
    """
    pass

@receiver(post_delete, sender=None)
def api_post_delete_handler(sender, instance, **kwargs):
    """
    Handler para eventos post_delete en el módulo api
    """
    pass









































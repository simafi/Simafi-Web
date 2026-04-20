from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core - Funcionalidades Base'
    
    def ready(self):
        """Inicialización del módulo core"""
        # import core.signals  # Comentado temporalmente para evitar problemas
        pass

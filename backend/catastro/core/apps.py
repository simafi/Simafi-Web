from django.apps import AppConfig


class CatastroCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catastro.core'
    label = 'catastro_core'
    verbose_name = 'Core - Funcionalidades Base'
    
    def ready(self):
        """Inicialización del módulo core"""
        import catastro.core.signals

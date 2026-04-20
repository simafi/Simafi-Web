from django.apps import AppConfig


class TributarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tributario'
    verbose_name = 'Tributario - Gestión de Impuestos y Tasas'
    
    def ready(self):
        """Inicialización del módulo tributario"""
        import tributario.signals

from django.apps import AppConfig


class ContabilidadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contabilidad'
    verbose_name = 'Contabilidad - Módulo Contable NIC/IAS'

    def ready(self):
        """Inicialización del módulo contabilidad"""
        try:
            import contabilidad.signals
        except ImportError:
            pass

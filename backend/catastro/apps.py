from django.apps import AppConfig

class CatastroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catastro'
    verbose_name = 'Catastro Municipal'
    
    def ready(self):
        # Importar señales para que se registren
        try:
            import catastro.signals
        except ImportError:
            pass










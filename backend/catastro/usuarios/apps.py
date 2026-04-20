from django.apps import AppConfig


class CatastroUsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catastro.usuarios'
    label = 'catastro_usuarios'
    verbose_name = 'Usuarios - Gestión de Usuarios'
    
    def ready(self):
        """Inicialización del módulo usuarios"""
        import catastro.usuarios.signals

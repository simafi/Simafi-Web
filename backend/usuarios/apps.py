from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    verbose_name = 'Usuarios - Gestión de Usuarios'
    
    def ready(self):
        """Inicialización del módulo usuarios"""
        import usuarios.signals

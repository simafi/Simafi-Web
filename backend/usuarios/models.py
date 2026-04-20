from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from core.models import BaseModel, Municipio


class Usuario(BaseModel):
    """
    Modelo de usuario del sistema
    """
    empresa = models.CharField(max_length=4, verbose_name="Código de Empresa", default='', db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=15, verbose_name="Nombre de Usuario", db_collation='latin1_swedish_ci')
    password = models.CharField(max_length=255, verbose_name="Contraseña", db_collation='latin1_swedish_ci')
    es_superusuario = models.BooleanField(
        default=False,
        verbose_name="Superusuario",
        help_text="Si está activo, puede acceder a todos los módulos sin contraseña por módulo.",
    )
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre", db_collation='latin1_swedish_ci')
    email = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    is_active = models.BooleanField(default=True, verbose_name="Usuario Activo")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Último Acceso")
    failed_login_attempts = models.IntegerField(default=0, verbose_name="Intentos Fallidos")
    locked_until = models.DateTimeField(null=True, blank=True, verbose_name="Bloqueado Hasta")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Municipio")
    
    def save(self, *args, **kwargs):
        # Hash la contraseña antes de guardarla si es nueva o ha sido modificada
        if not self.pk or not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        if self.nombre:
            return self.nombre
        return self.usuario

    def get_short_name(self):
        """Retorna el nombre corto del usuario"""
        return self.nombre or self.usuario

    def is_locked(self):
        """Verifica si el usuario está bloqueado"""
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False

    def lock_account(self, duration_minutes=30):
        """Bloquea la cuenta del usuario por un tiempo determinado"""
        self.locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save()

    def unlock_account(self):
        """Desbloquea la cuenta del usuario"""
        self.locked_until = None
        self.failed_login_attempts = 0
        self.save()

    def record_failed_login(self):
        """Registra un intento fallido de login"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lock_account()
        self.save()

    def record_successful_login(self):
        """Registra un login exitoso"""
        self.last_login = timezone.now()
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = 'mod_usuarios_usuario'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['nombre', 'usuario']
        unique_together = ('empresa', 'usuario')
        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['usuario']),
            models.Index(fields=['is_active']),
        ]


class UsuarioAccesoModulo(BaseModel):
    """
    Credenciales específicas por módulo (usuario + contraseña distinta por módulo).
    El superusuario no requiere filas aquí.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='accesos_modulo',
        verbose_name='Usuario',
    )
    codigo_modulo = models.CharField(max_length=32, verbose_name='Código de módulo', db_collation='latin1_swedish_ci')
    password = models.CharField(max_length=255, verbose_name='Contraseña del módulo', db_collation='latin1_swedish_ci')

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario.usuario} → {self.codigo_modulo}'

    class Meta:
        db_table = 'mod_usuarios_acceso_modulo'
        verbose_name = 'Acceso a módulo'
        verbose_name_plural = 'Accesos por módulo'
        unique_together = ('usuario', 'codigo_modulo')
        indexes = [
            models.Index(fields=['codigo_modulo']),
        ]


class PerfilUsuario(BaseModel):
    """
    Perfil extendido del usuario
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo")
    departamento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departamento")
    foto = models.FileField(upload_to='usuarios/fotos/', blank=True, null=True, verbose_name="Foto de Perfil")
    
    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name()}"
    
    class Meta:
        db_table = 'mod_usuarios_perfil'
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"


class Permiso(BaseModel):
    """
    Permisos del sistema
    """
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    modulo = models.CharField(max_length=50, verbose_name="Módulo")
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        db_table = 'mod_usuarios_permiso'
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        ordering = ['modulo', 'nombre']


class Rol(BaseModel):
    """
    Roles de usuario
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    permisos = models.ManyToManyField(Permiso, blank=True, verbose_name="Permisos")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'mod_usuarios_rol'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class UsuarioRol(BaseModel):
    """
    Asignación de roles a usuarios
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='roles_asignados')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios_asignados')
    fecha_asignacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Asignación")
    asignado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='roles_asignados_por')
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.rol.nombre}"
    
    class Meta:
        db_table = 'mod_usuarios_usuario_rol'
        verbose_name = "Asignación de Rol"
        verbose_name_plural = "Asignaciones de Roles"
        unique_together = ('usuario', 'rol')

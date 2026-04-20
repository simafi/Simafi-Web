from decimal import Decimal

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Modelo base que incluye campos comunes para todos los modelos del sistema
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        abstract = True


class Municipio(models.Model):
    """
    Modelo de municipio - Usa la tabla existente
    Estructura basada en: CREATE TABLE `municipio`
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4, unique=True, default='', verbose_name="Código", db_collation='latin1_swedish_ci')
    DESCRIPCION = models.CharField(max_length=29, verbose_name="Descripción", db_collation='latin1_swedish_ci')
    fesqui = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), verbose_name="Factor esquina", null=True, blank=True)
    por_concer = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Porcentaje de concertación"
    )
    vl_exento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor exento"
    )
    tasau = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Tasa Urbana",
        null=True,
        blank=True
    )
    tasar = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Tasa Rural",
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.codigo} - {getattr(self, 'DESCRIPCION', '')}"
    
    @property
    def descripcion(self):
        """Propiedad para compatibilidad con código existente que usa descripcion en minúsculas"""
        return getattr(self, 'DESCRIPCION', '')
    
    class Meta:
        db_table = 'municipio'
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['codigo']


class SystemConfig(BaseModel):
    """
    Configuración del sistema
    """
    key = models.CharField(max_length=100, unique=True, verbose_name="Clave")
    value = models.TextField(verbose_name="Valor")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Municipio")
    
    def __str__(self):
        return f"{self.key}: {self.value}"
    
    class Meta:
        db_table = 'system_config'
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"


class AuditLog(BaseModel):
    """
    Registro de auditoría para acciones importantes del sistema
    """
    ACTION_CHOICES = [
        ('CREATE', 'Crear'),
        ('UPDATE', 'Actualizar'),
        ('DELETE', 'Eliminar'),
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cerrar sesión'),
        ('EXPORT', 'Exportar'),
        ('IMPORT', 'Importar'),
    ]
    
    user = models.CharField(max_length=100, verbose_name="Usuario")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Acción")
    model_name = models.CharField(max_length=100, verbose_name="Modelo")
    object_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID del objeto")
    details = models.TextField(blank=True, null=True, verbose_name="Detalles")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Dirección IP")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Municipio")
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"
    
    class Meta:
        db_table = 'audit_log'
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-created_at']


class Oficina(BaseModel):
    """
    Modelo de oficina municipal
    """
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    codigo = models.CharField(max_length=10, verbose_name="Código")
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
    class Meta:
        db_table = 'mod_core_oficina'
        verbose_name = "Oficina"
        verbose_name_plural = "Oficinas"
        unique_together = ('municipio', 'codigo')
        ordering = ['codigo']

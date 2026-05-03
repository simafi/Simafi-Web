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
    Modelo de municipio — columnas alineadas con la tabla MySQL `municipio` (DESCRIBE).
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4, unique=True, default='', verbose_name="Código", db_column='codigo')
    descripcion = models.CharField(max_length=29, verbose_name="Descripción", db_column='DESCRIPCION')
    fesqui = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), verbose_name="Factor esquina", db_column='fesqui',
    )
    por_concer = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=Decimal('0.00'),
        verbose_name="Porcentaje de concertación", db_column='por_concer',
    )
    vl_exento = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, default=Decimal('0.00'), 
        verbose_name="Valor exento", db_column='vl_exento'
    )
    tasau = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), verbose_name="Tasa urbana", db_column='tasau',
    )
    tasar = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), verbose_name="Tasa rural", db_column='tasar',
    )
    # Responsables / cargos (CHAR en MySQL)
    alcalde = models.CharField(max_length=50, blank=True, null=True, verbose_name="Alcalde", db_column='alcalde')
    auditor = models.CharField(max_length=50, blank=True, null=True, verbose_name="Auditor", db_column='auditor')
    presupuestos = models.CharField(max_length=50, blank=True, null=True, verbose_name="Presupuestos", db_column='presupuestos')
    contador = models.CharField(max_length=50, blank=True, null=True, verbose_name="Contador", db_column='contador')
    tesorero = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tesorero", db_column='tesorero')
    secretario = models.CharField(max_length=50, blank=True, null=True, verbose_name="Secretario", db_column='secretario')
    proyecto = models.CharField(max_length=50, blank=True, null=True, verbose_name="Proyecto", db_column='proyecto')
    activo = models.CharField(max_length=7, blank=True, null=True, verbose_name="Activo", db_column='activo')
    financiero = models.CharField(max_length=50, blank=True, null=True, verbose_name="Financiero", db_column='financiero')
    tesorera = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tesorera", db_column='tesorera')
    tributacion = models.CharField(
        max_length=100, blank=True, default='', verbose_name="Tributación", db_column='tributacion',
    )
    gerentefin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gerente financiero", db_column='gerentefin')
    gerentegeneral = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gerente general", db_column='gerentegeneral')
    porce_condo1 = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), verbose_name="% condonación 1", db_column='porce_condo1',
    )
    porce_condo2 = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), verbose_name="% condonación 2", db_column='porce_condo2',
    )
    fecondona1 = models.DateField(null=True, blank=True, verbose_name="Fecha condonación 1", db_column='fecondona1')
    fecondona2 = models.DateField(null=True, blank=True, verbose_name="Fecha condonación 2", db_column='fecondona2')
    interes = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), verbose_name="Interés", db_column='interes',
    )
    desc_tercera = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), verbose_name="Descuento tercera", db_column='desc_tercera',
    )

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    def clean(self):
        """Regla: los dos primeros dígitos de `codigo` deben existir en `departamento.depto` (misma lógica que el formulario)."""
        from django.core.exceptions import ValidationError

        from .municipio_depto import codigo_municipio_tiene_departamento_valido

        codigo = (self.codigo or '').strip()
        if not codigo:
            return
        if len(codigo) < 2:
            raise ValidationError({
                'codigo': 'El código debe tener al menos 2 caracteres (prefijo de departamento).',
            })
        if not codigo_municipio_tiene_departamento_valido(codigo):
            raise ValidationError({
                'codigo': 'Los dos primeros dígitos deben coincidir con un código de la tabla departamento.',
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'municipio'
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['codigo']
        managed = False


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


class Departamento(models.Model):
    """
    Tabla `departamento` (estructura real en bdsimafipy: id, depto, descripcion).
    """

    id = models.AutoField(primary_key=True)
    depto = models.CharField(
        max_length=3,
        unique=True,
        verbose_name="Código departamento",
        db_collation='latin1_swedish_ci',
        db_column='depto',
    )
    descripcion = models.CharField(
        max_length=29,
        verbose_name="Descripción",
        db_collation='latin1_swedish_ci',
        db_column='descripcion',
    )

    def __str__(self):
        return f"{self.depto} - {self.descripcion}"

    class Meta:
        db_table = 'departamento'
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['depto']
        managed = False


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

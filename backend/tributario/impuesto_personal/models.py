from django.db import models
from tributario.models import Identificacion, Negocio
from django.utils import timezone
from decimal import Decimal

class Contribuyente(models.Model):
    """
    Extensión de Identificacion para propósitos de Impuesto Personal
    """
    persona = models.OneToOneField(Identificacion, on_delete=models.CASCADE, related_name='contribuyente_personal')
    rtn = models.CharField(max_length=20, blank=True, null=True, verbose_name="RTN")
    direccion_notificacion = models.TextField(blank=True, null=True, verbose_name="Dirección de Notificación")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    
    def __str__(self):
        return f"{self.persona.nombres} {self.persona.apellidos} ({self.persona.identidad})"

    class Meta:
        verbose_name = "Contribuyente Personal"
        verbose_name_plural = "Contribuyentes Personales"

class TarifasPersonal(models.Model):
    """
    Tabla de rangos impositivos para el Impuesto Personal (Honduras)
    """
    ano = models.IntegerField(verbose_name="Año Fiscal")
    desde = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Rango Desde")
    hasta = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Rango Hasta")
    tasa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tasa (Millar)")
    valor_fijo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Fijo")

    def __str__(self):
        return f"Tarifa {self.ano}: {self.desde} - {self.hasta}"

    class Meta:
        verbose_name = "Tarifa Impuesto Personal"
        verbose_name_plural = "Tarifas Impuesto Personal"
        ordering = ['ano', 'desde']

class DeclaracionPersonal(models.Model):
    """
    Declaración de Impuesto Personal
    """
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('presentada', 'Presentada'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    ]
    
    contribuyente = models.ForeignKey(Contribuyente, on_delete=models.CASCADE, related_name='declaraciones')
    ano_fiscal = models.IntegerField(verbose_name="Año Fiscal")
    fecha_presentacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Presentación")
    renta_bruta = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Renta Bruta Anual")
    deducciones = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name="Deducciones")
    renta_neta = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Renta Neta Gravable")
    impuesto_calculado = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Impuesto Calculado")
    multa = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Multa por Presentación Tardía")
    recargo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Recargos/Intereses")
    total_pagar = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Total a Pagar")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador', verbose_name="Estado")
    usuario = models.CharField(max_length=50, blank=True, null=True, verbose_name="Usuario que registró")
    
    def __str__(self):
        return f"Declaración {self.ano_fiscal} - {self.contribuyente.persona.identidad}"

    class Meta:
        verbose_name = "Declaración Personal"
        verbose_name_plural = "Declaraciones Personales"
        unique_together = ('contribuyente', 'ano_fiscal')

class PlanillaEmpresa(models.Model):
    """
    Carga de planillas de empresas para vinculación y verificación
    """
    empresa = models.ForeignKey(Negocio, on_delete=models.CASCADE, verbose_name="Empresa/Negocio")
    ano = models.IntegerField(verbose_name="Año")
    mes = models.IntegerField(verbose_name="Mes")
    archivo = models.FileField(upload_to='planillas/', verbose_name="Archivo de Planilla")
    fecha_carga = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Planilla de Empresa"
        verbose_name_plural = "Planillas de Empresas"

class DetallePlanilla(models.Model):
    """
    Detalle individual por empleado en la planilla
    """
    planilla = models.ForeignKey(PlanillaEmpresa, on_delete=models.CASCADE, related_name='detalles')
    identidad = models.CharField(max_length=20, verbose_name="Identidad del Empleado")
    nombre_empleado = models.CharField(max_length=150, verbose_name="Nombre")
    sueldo_bruto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Sueldo Bruto")
    impuesto_retenido = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Impuesto Retenido")
    
    class Meta:
        verbose_name = "Detalle de Planilla"
        verbose_name_plural = "Detalles de Planillas"

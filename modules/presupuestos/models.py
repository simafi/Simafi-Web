from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class PresupuestoIngresos(models.Model):
    """
    Modelo para gestionar el presupuesto de ingresos municipales
    """
    ano = models.IntegerField('Año')
    fuente_ingreso = models.CharField('Fuente de Ingreso', max_length=200)
    descripcion = models.TextField('Descripción', blank=True)
    monto_presupuestado = models.DecimalField('Monto Presupuestado', max_digits=15, decimal_places=2, default=Decimal('0.00'))
    monto_ejecutado = models.DecimalField('Monto Ejecutado', max_digits=15, decimal_places=2, default=Decimal('0.00'))
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    fecha_modificacion = models.DateTimeField('Fecha de Modificación', auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='presupuestos_ingresos_creados')
    usuario_modificacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='presupuestos_ingresos_modificados')

    class Meta:
        verbose_name = 'Presupuesto de Ingresos'
        verbose_name_plural = 'Presupuestos de Ingresos'
        ordering = ['-ano', 'fuente_ingreso']

    def __str__(self):
        return f"{self.ano} - {self.fuente_ingreso} - {self.monto_presupuestado}"


class PresupuestoGastos(models.Model):
    """
    Modelo para gestionar el presupuesto de gastos municipales
    """
    ano = models.IntegerField('Año')
    categoria_gasto = models.CharField('Categoría de Gasto', max_length=200)
    subcategoria = models.CharField('Subcategoría', max_length=200, blank=True)
    descripcion = models.TextField('Descripción', blank=True)
    monto_presupuestado = models.DecimalField('Monto Presupuestado', max_digits=15, decimal_places=2, default=Decimal('0.00'))
    monto_ejecutado = models.DecimalField('Monto Ejecutado', max_digits=15, decimal_places=2, default=Decimal('0.00'))
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    fecha_modificacion = models.DateTimeField('Fecha de Modificación', auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='presupuestos_gastos_creados')
    usuario_modificacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='presupuestos_gastos_modificados')

    class Meta:
        verbose_name = 'Presupuesto de Gastos'
        verbose_name_plural = 'Presupuestos de Gastos'
        ordering = ['-ano', 'categoria_gasto']

    def __str__(self):
        return f"{self.ano} - {self.categoria_gasto} - {self.monto_presupuestado}"


class EjecucionPresupuestaria(models.Model):
    """
    Modelo para registrar la ejecución presupuestaria
    """
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]

    tipo = models.CharField('Tipo', max_length=10, choices=TIPO_CHOICES)
    presupuesto_ingreso = models.ForeignKey(PresupuestoIngresos, on_delete=models.CASCADE, null=True, blank=True)
    presupuesto_gasto = models.ForeignKey(PresupuestoGastos, on_delete=models.CASCADE, null=True, blank=True)
    fecha_ejecucion = models.DateField('Fecha de Ejecución')
    monto = models.DecimalField('Monto', max_digits=15, decimal_places=2)
    descripcion = models.TextField('Descripción')
    documento_referencia = models.CharField('Documento de Referencia', max_length=100, blank=True)
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Ejecución Presupuestaria'
        verbose_name_plural = 'Ejecuciones Presupuestarias'
        ordering = ['-fecha_ejecucion']

    def __str__(self):
        return f"{self.tipo} - {self.fecha_ejecucion} - {self.monto}"


class ModificacionPresupuestaria(models.Model):
    """
    Modelo para gestionar modificaciones presupuestarias
    """
    TIPO_CHOICES = [
        ('traslado', 'Traslado'),
        ('suplemento', 'Suplemento'),
        ('reduccion', 'Reducción'),
    ]

    tipo_modificacion = models.CharField('Tipo de Modificación', max_length=20, choices=TIPO_CHOICES)
    presupuesto_origen = models.ForeignKey(PresupuestoGastos, on_delete=models.CASCADE, related_name='modificaciones_origen')
    presupuesto_destino = models.ForeignKey(PresupuestoGastos, on_delete=models.CASCADE, related_name='modificaciones_destino', null=True, blank=True)
    monto = models.DecimalField('Monto', max_digits=15, decimal_places=2)
    fecha_modificacion = models.DateField('Fecha de Modificación')
    justificacion = models.TextField('Justificación')
    documento_aprobacion = models.CharField('Documento de Aprobación', max_length=100, blank=True)
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Modificación Presupuestaria'
        verbose_name_plural = 'Modificaciones Presupuestarias'
        ordering = ['-fecha_modificacion']

    def __str__(self):
        return f"{self.tipo_modificacion} - {self.fecha_modificacion} - {self.monto}"
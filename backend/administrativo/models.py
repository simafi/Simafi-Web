# -*- coding: utf-8 -*-
import os

from decimal import Decimal

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import get_valid_filename


def proveedor_documentacion_upload_to(instance, filename):
    """
    Almacenamiento por municipio (empresa): cada código queda en su carpeta para no mezclar archivos.
    """
    safe = get_valid_filename(os.path.basename(filename)) or "documento"
    emp = (instance.empresa or "na").strip()[:10]
    pk_part = instance.pk if instance.pk else "nuevo"
    return f"adm_proveedores/{emp}/{pk_part}/{safe}"


class Proveedor(models.Model):
    """Proveedor o contratista para gestión administrativa (por empresa/municipio)."""

    empresa = models.CharField(max_length=10, verbose_name='Empresa/Municipio', db_index=True)
    razon_social = models.CharField(max_length=200, verbose_name='Razón social / nombre')
    nit = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='RTN / DNI / NIT',
    )
    telefono = models.CharField(max_length=40, blank=True, default='', verbose_name='Teléfono')
    email = models.EmailField(blank=True, default='', verbose_name='Correo')
    direccion = models.CharField(max_length=255, blank=True, default='', verbose_name='Dirección')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    notas = models.TextField(blank=True, default='', verbose_name='Notas')
    documentacion_descripcion = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Referencia del documento',
        help_text='Breve descripción del archivo (ej. RTN, constancia, convenio).',
    )
    documentacion = models.FileField(
        upload_to=proveedor_documentacion_upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'])],
        verbose_name='Documentación digital',
        help_text='PDF u ofimática. El archivo se guarda en carpeta exclusiva del municipio en sesión.',
    )

    class Meta:
        db_table = 'adm_proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['razon_social']
        indexes = [
            models.Index(fields=['empresa', 'razon_social']),
        ]

    def __str__(self):
        return f'{self.razon_social} ({self.empresa})'

    @property
    def documentacion_cargada(self):
        return bool(self.documentacion and self.documentacion.name)


class ContratoAdministrativo(models.Model):
    ESTADO_BORRADOR = 'borrador'
    ESTADO_VIGENTE = 'vigente'
    ESTADO_VENCIDO = 'vencido'
    ESTADO_ANULADO = 'anulado'
    ESTADO_CHOICES = [
        (ESTADO_BORRADOR, 'Borrador'),
        (ESTADO_VIGENTE, 'Vigente'),
        (ESTADO_VENCIDO, 'Vencido'),
        (ESTADO_ANULADO, 'Anulado'),
    ]

    empresa = models.CharField(max_length=10, verbose_name='Empresa/Municipio', db_index=True)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='contratos',
        verbose_name='Proveedor',
    )
    numero = models.CharField(max_length=80, verbose_name='Número de contrato / orden')
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name='Fecha inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha fin')
    monto_estimado = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Monto estimado',
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_BORRADOR,
        verbose_name='Estado',
    )
    observaciones = models.TextField(blank=True, default='', verbose_name='Observaciones')

    class Meta:
        db_table = 'adm_contrato'
        verbose_name = 'Contrato administrativo'
        verbose_name_plural = 'Contratos administrativos'
        ordering = ['-fecha_inicio', 'numero']
        indexes = [
            models.Index(fields=['empresa', 'estado']),
        ]

    def __str__(self):
        return f'{self.numero} — {self.proveedor.razon_social}'


class ExpedienteGestion(models.Model):
    TIPO_COMPRAS = 'compras'
    TIPO_CONTRATACION = 'contratacion'
    TIPO_GENERAL = 'general'
    TIPO_OTRO = 'otro'
    TIPO_CHOICES = [
        (TIPO_COMPRAS, 'Compras'),
        (TIPO_CONTRATACION, 'Contratación'),
        (TIPO_GENERAL, 'General'),
        (TIPO_OTRO, 'Otro'),
    ]

    ESTADO_ABIERTO = 'abierto'
    ESTADO_TRAMITE = 'en_tramite'
    ESTADO_CERRADO = 'cerrado'
    ESTADO_ARCHIVADO = 'archivado'
    ESTADO_CHOICES = [
        (ESTADO_ABIERTO, 'Abierto'),
        (ESTADO_TRAMITE, 'En trámite'),
        (ESTADO_CERRADO, 'Cerrado'),
        (ESTADO_ARCHIVADO, 'Archivado'),
    ]

    empresa = models.CharField(max_length=10, verbose_name='Empresa/Municipio', db_index=True)
    codigo_interno = models.CharField(max_length=40, verbose_name='Código interno')
    titulo = models.CharField(max_length=200, verbose_name='Título')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_GENERAL, verbose_name='Tipo')
    fecha_apertura = models.DateField(verbose_name='Fecha de apertura')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_ABIERTO,
        verbose_name='Estado',
    )
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')

    class Meta:
        db_table = 'adm_expediente'
        verbose_name = 'Expediente de gestión'
        verbose_name_plural = 'Expedientes de gestión'
        ordering = ['-fecha_apertura', 'codigo_interno']
        unique_together = [('empresa', 'codigo_interno')]
        indexes = [
            models.Index(fields=['empresa', 'estado']),
        ]

    def __str__(self):
        return f'{self.codigo_interno} — {self.titulo}'

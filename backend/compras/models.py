# -*- coding: utf-8 -*-
"""
Modelos del proceso de compras: requisiciones, cotizaciones, órdenes de compra y movimientos de bodega.

Integración:
- contabilidad.Inventario (NIC 2) para catálogo de existencias.
- presupuestos.CuentaPresupuestaria / Compromiso para codificación y reserva.
- administrativo.Proveedor para proveedores.
"""
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from administrativo.models import Proveedor
from contabilidad.models import EjercicioFiscal, Inventario
from presupuestos.models import Compromiso, CuentaPresupuestaria


class ComprasBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio", db_index=True)

    class Meta:
        abstract = True


class Requisicion(ComprasBaseModel):
    """Solicitud interna de materiales/bienes (paso inicial del proceso)."""

    ESTADO_CHOICES = [
        ("BORRADOR", "Borrador"),
        ("ENVIADA", "Enviada a aprobación"),
        ("APROBADA", "Aprobada"),
        ("RECHAZADA", "Rechazada"),
        ("CANCELADA", "Cancelada"),
    ]

    numero = models.CharField(max_length=30, verbose_name="Número")
    correlativo = models.PositiveIntegerField(
        default=0,
        verbose_name="N° correlativo",
        help_text="Secuencial por empresa y ejercicio fiscal (asignación automática).",
    )
    fecha = models.DateField(verbose_name="Fecha")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="BORRADOR")
    solicitante = models.CharField(max_length=120, blank=True, default="", verbose_name="Solicitante")
    observaciones = models.TextField(blank=True, default="", verbose_name="Observaciones")
    ejercicio = models.ForeignKey(
        EjercicioFiscal,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="requisiciones_compras",
        verbose_name="Ejercicio fiscal",
    )

    class Meta:
        db_table = "compras_requisicion"
        verbose_name = "Requisición"
        verbose_name_plural = "Requisiciones"
        ordering = ["-fecha", "-id"]
        unique_together = ("empresa", "numero")

    def __str__(self):
        return f"REQ {self.numero} ({self.get_estado_display()})"


class RequisicionDetalle(models.Model):
    requisicion = models.ForeignKey(
        Requisicion,
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="Requisición",
    )
    nro_linea = models.PositiveSmallIntegerField(default=1, verbose_name="Línea")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    cantidad = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
        verbose_name="Cantidad",
    )
    unidad = models.CharField(max_length=20, default="UND", verbose_name="Unidad de medida")
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="requisiciones_detalle",
        verbose_name="Material / ítem de bodega (inventario)",
        help_text="Obligatorio en cada línea: catálogo NIC 2; la existencia en bodega es Inventario.cantidad.",
    )
    cuenta_presupuestaria = models.ForeignKey(
        CuentaPresupuestaria,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="requisiciones_detalle",
        verbose_name="Código presupuestario",
    )

    class Meta:
        db_table = "compras_requisicion_detalle"
        verbose_name = "Detalle de requisición"
        verbose_name_plural = "Detalles de requisición"
        ordering = ["requisicion", "nro_linea"]

    def __str__(self):
        return f"{self.requisicion.numero} - L{self.nro_linea}"


class SolicitudCotizacion(ComprasBaseModel):
    """Convocatoria / solicitud de cotizaciones (marco tipo ONCAE parametrizable en vistas)."""

    ESTADO_CHOICES = [
        ("BORRADOR", "Borrador"),
        ("PUBLICADA", "Publicada / enviada a proveedores"),
        ("CERRADA", "Cerrada sin adjudicar"),
        ("ADJUDICADA", "Adjudicada"),
    ]

    numero = models.CharField(max_length=30, verbose_name="Número")
    fecha = models.DateField(verbose_name="Fecha")
    fecha_limite_respuesta = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha límite de ofertas",
    )
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="BORRADOR")
    requisicion = models.ForeignKey(
        Requisicion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_cotizacion",
        verbose_name="Requisición origen",
    )
    observaciones = models.TextField(blank=True, default="", verbose_name="Observaciones / alcance")
    texto_marco_oncae = models.TextField(
        blank=True,
        default="",
        verbose_name="Marco legal / referencia ONCAE",
        help_text="Texto para impresión de convocatoria (bases, normativa aplicable).",
    )

    class Meta:
        db_table = "compras_solicitud_cotizacion"
        verbose_name = "Solicitud de cotización"
        verbose_name_plural = "Solicitudes de cotización"
        unique_together = ("empresa", "numero")
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"SC {self.numero}"


class SolicitudCotizacionDetalle(models.Model):
    """Líneas de ítems a cotizar (vinculables a inventario / bodega)."""

    solicitud = models.ForeignKey(
        SolicitudCotizacion,
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="Solicitud",
    )
    nro_linea = models.PositiveSmallIntegerField(default=1, verbose_name="Línea")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    cantidad = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
        verbose_name="Cantidad",
    )
    unidad = models.CharField(max_length=20, default="UND", verbose_name="Unidad")
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="solicitudes_cotizacion_detalle",
        verbose_name="Material / inventario",
    )

    class Meta:
        db_table = "compras_solicitud_cotizacion_detalle"
        verbose_name = "Detalle solicitud de cotización"
        verbose_name_plural = "Detalles solicitud de cotización"
        ordering = ["solicitud", "nro_linea"]

    def __str__(self):
        return f"{self.solicitud.numero} L{self.nro_linea}"


class InvitacionCotizacion(models.Model):
    """Invitación a un proveedor a cotizar (base para envío de formato)."""

    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente de respuesta"),
        ("RECIBIDA", "Oferta recibida"),
        ("DECLINADA", "Declinada"),
    ]

    solicitud = models.ForeignKey(
        SolicitudCotizacion,
        on_delete=models.CASCADE,
        related_name="invitaciones",
        verbose_name="Solicitud",
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="invitaciones_cotizacion",
        verbose_name="Proveedor",
    )
    fecha_invitacion = models.DateField(null=True, blank=True, verbose_name="Fecha de invitación")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="PENDIENTE")

    class Meta:
        db_table = "compras_invitacion_cotizacion"
        verbose_name = "Invitación a cotizar"
        verbose_name_plural = "Invitaciones a cotizar"
        unique_together = ("solicitud", "proveedor")

    def __str__(self):
        return f"{self.solicitud.numero} → {self.proveedor}"


class OfertaProveedor(models.Model):
    """Respuesta económica del proveedor a una invitación."""

    invitacion = models.OneToOneField(
        InvitacionCotizacion,
        on_delete=models.CASCADE,
        related_name="oferta",
        verbose_name="Invitación",
    )
    fecha_recepcion = models.DateField(verbose_name="Fecha de recepción")
    monto_total = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Monto total ofertado")
    notas = models.TextField(blank=True, default="", verbose_name="Notas / condiciones")
    es_seleccionada = models.BooleanField(default=False, verbose_name="Oferta seleccionada")

    class Meta:
        db_table = "compras_oferta_proveedor"
        verbose_name = "Oferta de proveedor"
        verbose_name_plural = "Ofertas de proveedores"

    def __str__(self):
        return f"Oferta {self.invitacion} — {self.monto_total}"


class OrdenCompra(ComprasBaseModel):
    """Orden de compra formal; insumo para compromiso presupuestario y orden de pago."""

    ESTADO_CHOICES = [
        ("BORRADOR", "Borrador"),
        ("APROBADA", "Aprobada"),
        ("PARCIAL", "Recibido parcial"),
        ("CERRADA", "Cerrada"),
        ("ANULADA", "Anulada"),
    ]

    numero = models.CharField(max_length=30, verbose_name="Número OC")
    fecha = models.DateField(verbose_name="Fecha")
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="ordenes_compra",
        verbose_name="Proveedor",
    )
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="BORRADOR")
    requisicion = models.ForeignKey(
        Requisicion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordenes_compra",
        verbose_name="Requisición",
    )
    solicitud_cotizacion = models.ForeignKey(
        SolicitudCotizacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordenes_compra",
        verbose_name="Solicitud de cotización",
    )
    ejercicio = models.ForeignKey(
        EjercicioFiscal,
        on_delete=models.PROTECT,
        related_name="ordenes_compra",
        verbose_name="Ejercicio fiscal",
    )
    compromiso = models.ForeignKey(
        Compromiso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordenes_compra",
        verbose_name="Compromiso presupuestario",
        help_text="Reserva de fondo asociada (cuando exista).",
    )
    monto_total = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Monto total")
    observaciones = models.TextField(blank=True, default="", verbose_name="Observaciones")

    class Meta:
        db_table = "compras_orden_compra"
        verbose_name = "Orden de compra"
        verbose_name_plural = "Órdenes de compra"
        unique_together = ("empresa", "numero")
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"OC {self.numero}"


class OrdenCompraDetalle(models.Model):
    orden = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="Orden de compra",
    )
    nro_linea = models.PositiveSmallIntegerField(default=1, verbose_name="Línea")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ordenes_compra_detalle",
        verbose_name="Ítem inventario",
    )
    cuenta_presupuestaria = models.ForeignKey(
        CuentaPresupuestaria,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ordenes_compra_detalle",
        verbose_name="Partida presupuestaria",
    )

    class Meta:
        db_table = "compras_orden_compra_detalle"
        verbose_name = "Detalle orden de compra"
        verbose_name_plural = "Detalle órdenes de compra"
        ordering = ["orden", "nro_linea"]


class MovimientoBodega(ComprasBaseModel):
    """Entrada/salida de bodega vinculada al inventario contable (existencias)."""

    TIPO_CHOICES = [
        ("ENTRADA", "Entrada"),
        ("SALIDA", "Salida"),
    ]

    fecha = models.DateField(
        verbose_name="Fecha de registro en bodega",
        help_text="Fecha en que se registra el movimiento en kardex (puede ser distinta a la fecha de la compra).",
    )
    fecha_compra = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de la compra",
        help_text="Fecha del documento de compra o factura del proveedor.",
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo")
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.PROTECT,
        related_name="movimientos_bodega",
        verbose_name="Ítem inventario",
    )
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, verbose_name="Cantidad")
    costo_unitario = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        default=0,
        verbose_name="Costo unitario",
    )
    orden_detalle = models.ForeignKey(
        OrdenCompraDetalle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movimientos_bodega",
        verbose_name="Línea OC origen (entrada)",
    )
    referencia = models.CharField(max_length=120, blank=True, default="", verbose_name="Referencia / documento")
    notas = models.TextField(blank=True, default="", verbose_name="Notas")

    class Meta:
        db_table = "compras_movimiento_bodega"
        verbose_name = "Movimiento de bodega"
        verbose_name_plural = "Movimientos de bodega"
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.inventario.codigo} {self.cantidad}"

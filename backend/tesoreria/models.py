from django.db import models
from core.models import BaseModel
from core.pg_sequence import assign_pk_if_postgres_serial_missing as _pg_assign_next_pk_if_no_serial
from contabilidad.models import CuentaContable


class CuentaTesoreria(BaseModel):
    """
    Configuración de una fuente de recaudación/pago en Tesorería (Caja/Banco/Chequera),
    enlazada a una cuenta contable del catálogo de Contabilidad.

    Esta configuración se usará luego por Presupuestos al generar el asiento contable
    cuando se emite/cierra (por ejemplo, al registrar el cheque).
    """

    TIPO_CHOICES = [
        ('CAJA_GENERAL', 'Caja General'),
        ('BANCO', 'Banco'),
        ('CHEQUERA', 'Cuenta de Cheques / Chequera'),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    codigo = models.CharField(max_length=30, verbose_name="Código")
    nombre = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nombre")

    cuenta_contable = models.ForeignKey(
        CuentaContable,
        on_delete=models.PROTECT,
        related_name='tesoreria_cuentas',
        verbose_name='Cuenta contable (catálogo contable)',
    )

    class Meta:
        db_table = 'teso_cuenta_tesoreria'
        verbose_name = "Cuenta de Tesorería"
        verbose_name_plural = "Cuentas de Tesorería"
        unique_together = ('empresa', 'tipo', 'codigo')
        ordering = ['tipo', 'codigo']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.codigo} ({self.empresa})"


from presupuestos.models import OrdenPago

class PagoTesoreria(BaseModel):
    TIPO_PAGO_CHOICES = [
        ("CHEQUE", "Cheque"),
        ("TRANSFERENCIA", "Transferencia Bancaria"),
        ("EFECTIVO", "Efectivo/Caja"),
    ]
    ESTADO_CHOICES = [
        ("EMITIDO", "Emitido/Pendiente"),
        ("PAGADO", "Pagado/Efectuado"),
        ("ANULADO", "Anulado"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    tipo_pago = models.CharField(max_length=20, choices=TIPO_PAGO_CHOICES, default="CHEQUE")
    numero_referencia = models.CharField(max_length=50, verbose_name="No. Cheque / Referencia")
    fecha = models.DateField(verbose_name="Fecha de Pago")
    cuenta_tesoreria = models.ForeignKey(
        CuentaTesoreria,
        on_delete=models.PROTECT,
        related_name="pagos",
        verbose_name="Cuenta Origen",
    )
    beneficiario = models.CharField(max_length=200, verbose_name="Beneficiario / Páguese a")
    concepto = models.TextField(blank=True, null=True, verbose_name="Concepto del Pago")
    monto_total = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Monto Total")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="EMITIDO")
    punto_acta = models.CharField(max_length=100, blank=True, null=True, verbose_name="Punto de Acta / Respaldo")
    
    # Nuevos campos para control de cheques
    is_delivered = models.BooleanField(default=False, verbose_name="Entregado")
    fecha_entrega = models.DateField(null=True, blank=True, verbose_name="Fecha de Entrega")

    class Meta:
        db_table = "teso_pago"
        verbose_name = "Pago de Tesorería"
        verbose_name_plural = "Pagos de Tesorería"
        unique_together = ("empresa", "numero_referencia", "tipo_pago")
        ordering = ["-fecha", "-numero_referencia"]

    def __str__(self):
        return f"{self.tipo_pago} {self.numero_referencia} - {self.beneficiario}"


class PagoDetalleOrden(BaseModel):
    pago = models.ForeignKey(PagoTesoreria, on_delete=models.CASCADE, related_name="detalles_ordenes")
    orden_pago = models.ForeignKey(OrdenPago, on_delete=models.PROTECT, related_name="pagos_tesoreria")
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto Aplicado")

    class Meta:
        db_table = "teso_pago_detalle_orden"


class DepositoTesoreria(BaseModel):
    empresa = models.CharField(max_length=10)
    fecha = models.DateField()
    numero_referencia = models.CharField(max_length=50)
    cuenta_tesoreria = models.ForeignKey(CuentaTesoreria, on_delete=models.PROTECT, related_name="depositos")
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    concepto = models.TextField(blank=True, null=True)
    is_reconciled = models.BooleanField(default=False)

    class Meta:
        db_table = "teso_deposito"
        unique_together = ("empresa", "numero_referencia")


class NotaTesoreria(BaseModel):
    TIPO_CHOICES = [("CREDITO", "Nota de Crédito"), ("DEBITO", "Nota de Débito")]
    empresa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateField()
    numero_referencia = models.CharField(max_length=50)
    cuenta_tesoreria = models.ForeignKey(CuentaTesoreria, on_delete=models.PROTECT, related_name="notas")
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    concepto = models.TextField(blank=True, null=True)
    orden_pago = models.ForeignKey(OrdenPago, on_delete=models.SET_NULL, null=True, blank=True, related_name="notas_debito")
    is_reconciled = models.BooleanField(default=False)

    class Meta:
        db_table = "teso_nota"
        unique_together = ("empresa", "tipo", "numero_referencia")


class ConciliacionBancaria(BaseModel):
    ESTADO_CHOICES = [("BORRADOR", "Borrador/En Proceso"), ("FINALIZADA", "Finalizada")]
    empresa = models.CharField(max_length=10)
    cuenta_tesoreria = models.ForeignKey(CuentaTesoreria, on_delete=models.PROTECT)
    anio = models.IntegerField()
    mes = models.IntegerField()
    saldo_banco = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    saldo_libro = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="BORRADOR")
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "teso_conciliacion"
        unique_together = ("empresa", "cuenta_tesoreria", "anio", "mes")


class DetalleConciliacion(BaseModel):
    conciliacion = models.ForeignKey(ConciliacionBancaria, on_delete=models.CASCADE, related_name="detalles")
    # Referencia genérica o enlaces específicos? Usaremos enlaces específicos opcionales
    pago = models.ForeignKey(PagoTesoreria, on_delete=models.SET_NULL, null=True, blank=True)
    deposito = models.ForeignKey(DepositoTesoreria, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.ForeignKey(NotaTesoreria, on_delete=models.SET_NULL, null=True, blank=True)
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    fecha_banco = models.DateField()

    class Meta:
        db_table = "teso_conciliacion_detalle"


class CobroCaja(BaseModel):
    FUENTE_CHOICES = [
        ("CAJA", "Caja"),
        ("WEBSERVICE", "Webservice"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    fecha = models.DateField(verbose_name="Fecha de Cobro")
    cajero = models.CharField(max_length=50, blank=True, null=True, verbose_name="Cajero")
    total_cobrado = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Total Cobrado")
    fuente = models.CharField(max_length=15, choices=FUENTE_CHOICES, default="CAJA", verbose_name="Fuente")
    recibos_json = models.TextField(blank=True, null=True, verbose_name="Recibos incluidos (JSON)")
    referencia = models.CharField(max_length=80, blank=True, null=True, verbose_name="Referencia")
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")

    class Meta:
        db_table = "teso_cobro_caja"
        verbose_name = "Cobro en Caja"
        verbose_name_plural = "Cobros en Caja"
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.empresa} | {self.fecha} | {self.total_cobrado}"

    def save(self, *args, **kwargs):
        _pg_assign_next_pk_if_no_serial("teso_cobro_caja", self)
        super().save(*args, **kwargs)


class CobroCajaMetodo(BaseModel):
    FORMA_CHOICES = [
        ("EFECTIVO", "Efectivo"),
        ("POS", "POS"),
        ("CHEQUE", "Cheque"),
        ("COMPENSACION", "Compensación"),
    ]

    cobro = models.ForeignKey(CobroCaja, on_delete=models.CASCADE, related_name="metodos")
    forma_pago = models.CharField(max_length=20, choices=FORMA_CHOICES, default="EFECTIVO", verbose_name="Forma de Pago")
    monto = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Monto")
    referencia = models.CharField(max_length=80, blank=True, null=True, verbose_name="Referencia/Documento")

    class Meta:
        db_table = "teso_cobro_caja_metodo"
        verbose_name = "Detalle de Forma de Pago"
        verbose_name_plural = "Detalles de Formas de Pago"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        _pg_assign_next_pk_if_no_serial("teso_cobro_caja_metodo", self)
        super().save(*args, **kwargs)


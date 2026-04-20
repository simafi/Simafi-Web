from django.db import models
from core.models import BaseModel
from contabilidad.models import CuentaContable, EjercicioFiscal, CentroCosto


class Fondo(BaseModel):
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    codigo = models.CharField(max_length=20, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        db_table = "presu_fondo"
        verbose_name = "Fondo"
        verbose_name_plural = "Fondos"
        unique_together = ("empresa", "codigo")
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class CuentaPresupuestaria(BaseModel):
    TIPO_PRES_CHOICES = [
        ("INGRESO", "Ingreso"),
        ("EGRESO", "Egreso"),
    ]
    TIPO_CTA_CHOICES = [
        ("TITULO", "Título/Agrupadora"),
        ("DETALLE", "Detalle/Movimiento"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    codigo = models.CharField(max_length=40, verbose_name="Código presupuestario")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    tipo_presupuesto = models.CharField(max_length=10, choices=TIPO_PRES_CHOICES, default="EGRESO", verbose_name="Tipo Presupuesto")
    tipo_cuenta = models.CharField(max_length=10, choices=TIPO_CTA_CHOICES, default="DETALLE", verbose_name="Tipo Cuenta")
    
    cuenta_padre = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcuentas",
        verbose_name="Cuenta padre",
    )
    nivel = models.IntegerField(default=1, verbose_name="Nivel jerárquico")
    
    rubro_tributario = models.CharField(max_length=20, blank=True, null=True, verbose_name="Rubro tributario")

    # Enlace manual al catálogo contable
    cuenta_contable = models.ForeignKey(
        CuentaContable,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="cuentas_presupuestarias",
        verbose_name="Cuenta contable",
    )

    class Meta:
        db_table = "presu_cuenta_presup"
        verbose_name = "Cuenta Presupuestaria"
        verbose_name_plural = "Cuentas Presupuestarias"
        unique_together = ("empresa", "codigo")
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class PresupuestoAnual(BaseModel):
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    ejercicio = models.ForeignKey(
        EjercicioFiscal,
        on_delete=models.PROTECT,
        related_name="presupuestos_anuales",
        verbose_name="Ejercicio fiscal",
    )
    cuenta = models.ForeignKey(
        CuentaPresupuestaria,
        on_delete=models.CASCADE,
        related_name="presupuestos_anuales",
        verbose_name="Cuenta presupuestaria",
    )
    fondo = models.ForeignKey(
        Fondo,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="presupuestos_anuales",
        verbose_name="Fondo de financiamiento",
    )
    monto_inicial = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Monto inicial/Aprobado")
    monto_reformas = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Reformas/Modificaciones")
    
    @property
    def monto_vigente(self):
        return self.monto_inicial + self.monto_reformas

    class Meta:
        db_table = "presu_anual"
        verbose_name = "Presupuesto Anual"
        verbose_name_plural = "Presupuestos Anuales"
        unique_together = ("empresa", "ejercicio", "cuenta", "fondo")
        ordering = ["cuenta__codigo"]

    def __str__(self):
        return f"{self.cuenta.codigo} ({self.ejercicio.anio}): {self.monto_vigente}"


class ReformaPresupuestaria(BaseModel):
    TIPO_CHOICES = [
        ("AMPLIACION", "Ampliación (+)"),
        ("REDUCCION", "Reducción (-)"),
        ("TRASPASO", "Traspaso (+/-)"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    fecha = models.DateField(verbose_name="Fecha")
    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.PROTECT, related_name="reformas")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    referencia = models.CharField(max_length=100, verbose_name="No. Documento/Referencia")
    punto_acta = models.CharField(max_length=100, blank=True, null=True, verbose_name="Punto de Acta / Resolución")
    concepto = models.TextField(verbose_name="Concepto")
    
    # El fondo se maneja en egresos como dimensión del presupuesto
    fondo = models.ForeignKey(
        Fondo,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reformas",
        verbose_name="Fondo afectado",
    )

    # Para traspasos
    cuenta_origen = models.ForeignKey(
        CuentaPresupuestaria, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True, 
        related_name="reformas_origen",
        verbose_name="Cuenta Origen (solo para traspasos)"
    )
    # Para todos los tipos
    cuenta_destino = models.ForeignKey(
        CuentaPresupuestaria, 
        on_delete=models.PROTECT, 
        related_name="reformas_destino",
        verbose_name="Cuenta Destino/Afectada"
    )
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto")

    class Meta:
        db_table = "presu_reforma"
        verbose_name = "Reforma Presupuestaria"
        verbose_name_plural = "Reformas Presupuestarias"
        ordering = ["-fecha", "-id"]

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        if is_new:
            # Actualizar presupuesto anual de cuenta destino
            pa_dest, _ = PresupuestoAnual.objects.get_or_create(
                empresa=self.empresa, 
                ejercicio=self.ejercicio, 
                cuenta=self.cuenta_destino,
                fondo=self.fondo
            )
            
            if self.tipo == "AMPLIACION":
                pa_dest.monto_reformas += self.monto
            elif self.tipo == "REDUCCION":
                pa_dest.monto_reformas -= self.monto
            elif self.tipo == "TRASPASO":
                pa_dest.monto_reformas += self.monto
                if self.cuenta_origen:
                    # El traspaso suele ser dentro del mismo fondo o entre fondos?
                    # Por ahora asumimos mismo fondo si no se especifica otra cosa.
                    pa_orig, _ = PresupuestoAnual.objects.get_or_create(
                        empresa=self.empresa, 
                        ejercicio=self.ejercicio, 
                        cuenta=self.cuenta_origen,
                        fondo=self.fondo
                    )
                    pa_orig.monto_reformas -= self.monto
                    pa_orig.save()
            
            pa_dest.save()

    def __str__(self):
        return f"{self.tipo} - {self.referencia}"


class ProyectoInversion(BaseModel):
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    codigo = models.CharField(max_length=20, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del proyecto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    ejercicio = models.ForeignKey(
        EjercicioFiscal,
        on_delete=models.PROTECT,
        related_name="proyectos_inversion",
        verbose_name="Ejercicio fiscal",
    )

    # El proyecto nace en Presupuestos, pero puede enlazarse opcionalmente a centro de gasto en Contabilidad.
    centro_costo = models.ForeignKey(
        CentroCosto,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="proyectos_presupuesto",
        verbose_name="Centro de gasto (opcional)",
    )

    class Meta:
        db_table = "presu_proyecto_inversion"
        verbose_name = "Proyecto de Inversión"
        verbose_name_plural = "Proyectos de Inversión"
        unique_together = ("empresa", "ejercicio", "codigo")
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class OrdenPago(BaseModel):
    ESTADO_CHOICES = [
        ("BORRADOR", "Borrador/Preparación"),
        ("APROBADA", "Aprobada/Lista para Pago"),
        ("PAGADA", "Pagada (Tesorería)"),
        ("ANULADA", "Anulada"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    numero = models.CharField(max_length=30, verbose_name="Número")
    fecha = models.DateField(verbose_name="Fecha")
    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.PROTECT, related_name="ordenes_pago")
    favorecido = models.CharField(max_length=200, verbose_name="Favorecido")
    concepto = models.TextField(verbose_name="Concepto")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="BORRADOR")
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "presu_orden_pago"
        verbose_name = "Orden de Pago"
        verbose_name_plural = "Órdenes de Pago"
        unique_together = ("empresa", "numero")
        ordering = ["-fecha", "-numero"]

    def __str__(self):
        return f"OP {self.numero}"


class OrdenPagoDetalle(BaseModel):
    orden_pago = models.ForeignKey(OrdenPago, on_delete=models.CASCADE, related_name="detalles")
    linea = models.IntegerField(default=1)
    cuenta_presupuestaria = models.ForeignKey(CuentaPresupuestaria, on_delete=models.PROTECT)
    fondo = models.ForeignKey(Fondo, on_delete=models.PROTECT)
    proyecto = models.ForeignKey(ProyectoInversion, on_delete=models.PROTECT, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    monto = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "presu_orden_pago_det"
        verbose_name = "Detalle de Orden de Pago"
        verbose_name_plural = "Detalles de Orden de Pago"
        ordering = ["orden_pago", "linea"]
        unique_together = ("orden_pago", "linea")


class EjecucionPresupuestaria(BaseModel):
    ORIGEN_CHOICES = [
        ("MANUAL", "Manual"),
        ("ORDEN_PAGO", "Orden de Pago"),
        ("CHEQUE", "Cheque"),
        ("CIERRE_CAJA", "Cierre de Caja"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    fecha = models.DateField(verbose_name="Fecha")
    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.PROTECT, related_name="ejecuciones_presup")
    periodo = models.IntegerField(default=1, verbose_name="Período")
    cuenta_presupuestaria = models.ForeignKey(CuentaPresupuestaria, on_delete=models.PROTECT)
    fondo = models.ForeignKey(Fondo, on_delete=models.PROTECT, blank=True, null=True)
    proyecto = models.ForeignKey(ProyectoInversion, on_delete=models.PROTECT, blank=True, null=True)
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default="MANUAL")
    referencia = models.CharField(max_length=60, blank=True, null=True)
    monto = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "presu_ejecucion"
        verbose_name = "Ejecución Presupuestaria"
        verbose_name_plural = "Ejecuciones Presupuestarias"
        ordering = ["-fecha", "-id"]

class Compromiso(BaseModel):
    """Reserva de fondo previa a la orden de pago."""
    ESTADO_CHOICES = [
        ("BORRADOR", "Borrador/Preparación"),
        ("COMPROMETIDO", "Comprometido/Reserva"),
        ("ANULADO", "Anulado"),
    ]

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    numero = models.CharField(max_length=30, verbose_name="Número de Reserva")
    fecha = models.DateField(verbose_name="Fecha")
    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.PROTECT, related_name="compromisos")
    favorecido = models.CharField(max_length=200, verbose_name="Favorecido/Proveedor")
    concepto = models.TextField(verbose_name="Concepto de la Reserva")
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="BORRADOR")
    fondo = models.ForeignKey(Fondo, on_delete=models.PROTECT, related_name="compromisos", null=True, blank=True)

    class Meta:
        db_table = "presu_compromiso"
        verbose_name = "Compromiso/Reserva de Fondo"
        verbose_name_plural = "Compromisos/Reservas de Fondo"
        unique_together = ("empresa", "ejercicio", "numero")

    def __str__(self):
        return f"Reserva {self.numero} - {self.favorecido}"


class OperacionManual(BaseModel):
    """Registro de afectación manual de cuentas (Ingresos o Egresos)."""
    TIPO_OPERACION_CHOICES = [
        ("INGRESO", "Ingreso"),
        ("EGRESO", "Egreso"),
    ]
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    tipo = models.CharField(max_length=10, choices=TIPO_OPERACION_CHOICES, default="EGRESO")
    fecha = models.DateField(verbose_name="Fecha")
    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.PROTECT, related_name="operaciones_manuales")
    beneficiario = models.CharField(max_length=200, verbose_name="Beneficiario")
    concepto = models.TextField(verbose_name="Concepto")
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    fondo = models.ForeignKey(Fondo, on_delete=models.PROTECT, related_name="operaciones_manuales")
    cuenta = models.ForeignKey(CuentaPresupuestaria, on_delete=models.PROTECT)

    class Meta:
        db_table = "presu_operacion_manual"
        verbose_name = "Operación Manual"
        verbose_name_plural = "Operaciones Manuales"

    def __str__(self):
        return f"{self.tipo} - {self.id} - {self.monto}"


class RendicionForma07Ajuste(BaseModel):
    """
    Ajustes y datos de firma para Forma 07 (Cuenta de Tesorería).
    Se guardan por empresa + ejercicio para permitir completar extrapresupuestarios y firmas.
    """

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.PROTECT, related_name="rendicion_f07_ajustes")

    entradas_extra_efectivo = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    entradas_extra_bancos = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    pagos_extra_efectivo = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    pagos_extra_bancos = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    alcalde_nombre = models.CharField(max_length=200, blank=True, null=True)
    tesorero_nombre = models.CharField(max_length=200, blank=True, null=True)
    contador_nombre = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "presu_rendicion_f07_ajuste"
        unique_together = ("empresa", "ejercicio")
        verbose_name = "Rendición Forma 07 - Ajustes"
        verbose_name_plural = "Rendición Forma 07 - Ajustes"


class RendicionForma04Ajuste(BaseModel):
    """
    Ajustes y firmas para Forma 04 (Liquidación del Presupuesto / resultado presupuestario).
    """

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    ejercicio = models.ForeignKey(
        EjercicioFiscal, on_delete=models.PROTECT, related_name="rendicion_f04_ajustes"
    )
    ajuste_por_ingreso = models.DecimalField(
        max_digits=18, decimal_places=2, default=0, verbose_name="Ajuste por ingreso"
    )
    ajuste_por_egreso = models.DecimalField(
        max_digits=18, decimal_places=2, default=0, verbose_name="Ajuste por egreso"
    )
    alcalde_nombre = models.CharField(max_length=200, blank=True, null=True)
    tesorero_nombre = models.CharField(max_length=200, blank=True, null=True)
    contador_nombre = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "presu_rendicion_f04_ajuste"
        unique_together = ("empresa", "ejercicio")
        verbose_name = "Rendición Forma 04 - Ajustes"
        verbose_name_plural = "Rendición Forma 04 - Ajustes"


class RendicionForma05Ajuste(BaseModel):
    """
    Ajustes globales y firmas para Forma 05 (Arqueo de Caja General).
    Complementa totales declarados además de los que vienen de Tesorería.
    """

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    ejercicio = models.ForeignKey(
        EjercicioFiscal, on_delete=models.PROTECT, related_name="rendicion_f05_ajustes"
    )
    extra_entradas_efectivo = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Ajuste entradas efectivo (cobros caja)",
    )
    extra_salidas_efectivo = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Ajuste salidas efectivo (sumatoria)",
    )
    extra_cheques = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        verbose_name="Ajuste sumatoria cheques",
    )
    alcalde_nombre = models.CharField(max_length=200, blank=True, null=True)
    tesorero_nombre = models.CharField(max_length=200, blank=True, null=True)
    contador_nombre = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "presu_rendicion_f05_ajuste"
        unique_together = ("empresa", "ejercicio")
        verbose_name = "Rendición Forma 05 - Ajustes"
        verbose_name_plural = "Rendición Forma 05 - Ajustes"


class RendicionForma05SalidaManual(BaseModel):
    """
    Líneas adicionales de salida de efectivo para Forma 05 (documentos no cargados en Tesorería o aclaraciones).
    Se suman a las salidas automáticas cuando la fecha está dentro del periodo del informe.
    """

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    ejercicio = models.ForeignKey(
        EjercicioFiscal, on_delete=models.PROTECT, related_name="rendicion_f05_salidas_manuales"
    )
    fecha = models.DateField(verbose_name="Fecha del documento")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    documento = models.CharField(max_length=80, blank=True, default="", verbose_name="No. documento / referencia")
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Valor")
    orden = models.PositiveSmallIntegerField(default=0, verbose_name="Orden")

    class Meta:
        db_table = "presu_rendicion_f05_salida_manual"
        ordering = ["orden", "fecha", "id"]
        verbose_name = "Rendición Forma 05 - Salida manual"
        verbose_name_plural = "Rendición Forma 05 - Salidas manuales"


class RendicionForma06Captura(BaseModel):
    """
    Forma 06 TSC — Arqueo de Caja Chica o Fondo Rotatorio.
    Declaración y datos de quienes firman el arqueo por duplicado.
    """

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    ejercicio = models.ForeignKey(
        EjercicioFiscal, on_delete=models.PROTECT, related_name="rendicion_f06_capturas"
    )
    municipal_arqueo_nombre = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Municipal que realiza el arqueo (nombre completo)",
    )
    empleado_municipal_nombre = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Empleado(a) Municipal que realiza el arqueo",
    )
    responsable_nombre = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Responsable",
    )
    numero_arqueo = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="No. de arqueo / acta"
    )
    fecha_arqueo = models.DateField(blank=True, null=True, verbose_name="Fecha del arqueo")

    class Meta:
        db_table = "presu_rendicion_f06_captura"
        unique_together = ("empresa", "ejercicio")
        verbose_name = "Rendición Forma 06 - Captura"
        verbose_name_plural = "Rendición Forma 06 - Capturas"

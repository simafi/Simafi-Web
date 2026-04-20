"""
Modelos del Módulo de Contabilidad - SIMAFI Web
Basado en Normas Internacionales de Contabilidad (NIC/IAS)

Nomenclatura de cuentas según Marco Conceptual NIC 1:
  1xxxx - Activo: Recursos controlados por la entidad
  2xxxx - Pasivo: Obligaciones actuales
  3xxxx - Patrimonio: Parte residual (activos - pasivos)
  4xxxx - Ingresos: Incrementos en beneficios económicos
  5xxxx - Gastos: Decrementos en beneficios económicos
"""

from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


# ============================================================================
# MODELO BASE
# ============================================================================

class ContabilidadBaseModel(models.Model):
    """Modelo base con campos de auditoría comunes"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Creado por")
    updated_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Actualizado por")

    class Meta:
        abstract = True


# ============================================================================
# NIC 1 - PRESENTACIÓN DE ESTADOS FINANCIEROS
# ============================================================================

class EjercicioFiscal(ContabilidadBaseModel):
    """
    NIC 1 - Ejercicio fiscal / año contable.
    Define el periodo anual de información financiera.
    """
    ESTADO_CHOICES = [
        ('ABIERTO', 'Abierto'),
        ('CERRADO', 'Cerrado'),
        ('EN_CIERRE', 'En proceso de cierre'),
    ]

    anio = models.IntegerField(unique=True, verbose_name="Año fiscal")
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de fin")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ABIERTO', verbose_name="Estado")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"Ejercicio {self.anio} - {self.descripcion}"

    class Meta:
        db_table = 'cont_ejercicio_fiscal'
        verbose_name = "Ejercicio Fiscal"
        verbose_name_plural = "Ejercicios Fiscales"
        ordering = ['-anio']


class PeriodoContable(ContabilidadBaseModel):
    """
    NIC 1 - Período contable (mensual) dentro del ejercicio fiscal.
    """
    ESTADO_CHOICES = [
        ('ABIERTO', 'Abierto'),
        ('CERRADO', 'Cerrado'),
    ]

    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.CASCADE,
                                  related_name='periodos', verbose_name="Ejercicio fiscal")
    numero = models.IntegerField(verbose_name="Número de período (1-13)")
    nombre = models.CharField(max_length=50, verbose_name="Nombre del período")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de fin")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ABIERTO', verbose_name="Estado")

    def __str__(self):
        return f"{self.nombre} - {self.ejercicio.anio}"

    class Meta:
        db_table = 'cont_periodo_contable'
        verbose_name = "Período Contable"
        verbose_name_plural = "Períodos Contables"
        ordering = ['ejercicio', 'numero']
        unique_together = ('ejercicio', 'numero')


# ============================================================================
# MARCO CONCEPTUAL - PLAN DE CUENTAS
# ============================================================================

class GrupoCuenta(ContabilidadBaseModel):
    """
    Marco Conceptual - Grupos principales de cuentas contables.
    Refleja los elementos de los estados financieros:
    Activo, Pasivo, Patrimonio, Ingresos, Gastos.
    """
    NATURALEZA_CHOICES = [
        ('DEUDORA', 'Deudora'),
        ('ACREEDORA', 'Acreedora'),
    ]

    codigo = models.CharField(max_length=1, unique=True, verbose_name="Código del grupo")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del grupo")
    naturaleza = models.CharField(max_length=10, choices=NATURALEZA_CHOICES, verbose_name="Naturaleza")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    orden = models.IntegerField(default=0, verbose_name="Orden de presentación")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        db_table = 'cont_grupo_cuenta'
        verbose_name = "Grupo de Cuenta"
        verbose_name_plural = "Grupos de Cuentas"
        ordering = ['codigo']


class CuentaContable(ContabilidadBaseModel):
    """
    NIC 1 / Marco Conceptual - Plan de cuentas contable jerárquico.
    Estructura:
      Nivel 1: X (grupo) - Ej: 1=Activo
      Nivel 2: XX (subgrupo) - Ej: 11=Activo Corriente
      Nivel 3: XXX (rubro) - Ej: 111=Efectivo y Equivalentes
      Nivel 4: XXXX (cuenta) - Ej: 1111=Caja
      Nivel 5: XXXXX (subcuenta) - Ej: 11111=Caja General
    """
    TIPO_CHOICES = [
        ('TITULO', 'Título/Agrupadora'),
        ('DETALLE', 'Detalle/Movimiento'),
    ]
    NATURALEZA_CHOICES = [
        ('DEUDORA', 'Deudora'),
        ('ACREEDORA', 'Acreedora'),
    ]

    codigo = models.CharField(max_length=20, verbose_name="Código de cuenta")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de cuenta")
    grupo = models.ForeignKey(GrupoCuenta, on_delete=models.PROTECT,
                              related_name='cuentas', verbose_name="Grupo")
    cuenta_padre = models.ForeignKey('self', on_delete=models.CASCADE,
                                     null=True, blank=True,
                                     related_name='subcuentas', verbose_name="Cuenta padre")
    nivel = models.IntegerField(default=1, verbose_name="Nivel jerárquico")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='DETALLE', verbose_name="Tipo")
    naturaleza = models.CharField(max_length=10, choices=NATURALEZA_CHOICES, verbose_name="Naturaleza")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    acepta_movimiento = models.BooleanField(default=True, verbose_name="Acepta movimiento")
    requiere_centro_costo = models.BooleanField(default=False, verbose_name="Requiere centro de costo")
    requiere_tercero = models.BooleanField(default=False, verbose_name="Requiere tercero")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def saldo_normal(self):
        """Retorna si el saldo normal es débito o crédito"""
        return self.naturaleza

    class Meta:
        db_table = 'cont_cuenta_contable'
        verbose_name = "Cuenta Contable"
        verbose_name_plural = "Cuentas Contables"
        ordering = ['codigo']
        unique_together = ('codigo', 'empresa')


class CentroCosto(ContabilidadBaseModel):
    """
    NIC 1 - Centro de costo para distribución de gastos e ingresos.
    """
    codigo = models.CharField(max_length=20, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    centro_padre = models.ForeignKey('self', on_delete=models.CASCADE,
                                     null=True, blank=True,
                                     related_name='subcentros', verbose_name="Centro padre")
    responsable = models.CharField(max_length=200, blank=True, null=True, verbose_name="Responsable")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        db_table = 'cont_centro_costo'
        verbose_name = "Centro de Costo"
        verbose_name_plural = "Centros de Costo"
        ordering = ['codigo']
        unique_together = ('codigo', 'empresa')


# ============================================================================
# NIC 21 - EFECTOS DE LAS VARIACIONES EN TASAS DE CAMBIO
# ============================================================================

class Moneda(ContabilidadBaseModel):
    """
    NIC 21 - Monedas para transacciones en moneda extranjera.
    """
    codigo = models.CharField(max_length=3, unique=True, verbose_name="Código ISO")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la moneda")
    simbolo = models.CharField(max_length=5, verbose_name="Símbolo")
    es_local = models.BooleanField(default=False, verbose_name="Es moneda local")
    decimales = models.IntegerField(default=2, verbose_name="Decimales")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        db_table = 'cont_moneda'
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"
        ordering = ['codigo']


class TipoCambio(ContabilidadBaseModel):
    """
    NIC 21 - Tipos de cambio históricos para conversión de moneda extranjera.
    """
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE,
                               related_name='tipos_cambio', verbose_name="Moneda")
    fecha = models.DateField(verbose_name="Fecha")
    tasa_compra = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Tasa de compra")
    tasa_venta = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Tasa de venta")
    tasa_promedio = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Tasa promedio")

    def __str__(self):
        return f"{self.moneda.codigo} - {self.fecha} - {self.tasa_promedio}"

    class Meta:
        db_table = 'cont_tipo_cambio'
        verbose_name = "Tipo de Cambio"
        verbose_name_plural = "Tipos de Cambio"
        ordering = ['-fecha']
        unique_together = ('moneda', 'fecha')


# ============================================================================
# NIC 1 / NIC 8 - ASIENTOS CONTABLES (LIBRO DIARIO)
# ============================================================================

class TipoAsiento(ContabilidadBaseModel):
    """
    NIC 8 - Tipos de asiento contable.
    """
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    prefijo = models.CharField(max_length=5, verbose_name="Prefijo para numeración")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    es_automatico = models.BooleanField(default=False, verbose_name="Es automático")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        db_table = 'cont_tipo_asiento'
        verbose_name = "Tipo de Asiento"
        verbose_name_plural = "Tipos de Asiento"
        ordering = ['codigo']


class AsientoContable(ContabilidadBaseModel):
    """
    NIC 1 - Asiento contable / comprobante del libro diario.
    Registra las transacciones contables con partida doble.
    """
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('APROBADO', 'Aprobado'),
        ('CONTABILIZADO', 'Contabilizado'),
        ('ANULADO', 'Anulado'),
    ]

    numero = models.CharField(max_length=20, verbose_name="Número de asiento")
    tipo = models.ForeignKey(TipoAsiento, on_delete=models.PROTECT,
                             related_name='asientos', verbose_name="Tipo de asiento")
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.PROTECT,
                                related_name='asientos', verbose_name="Período contable")
    fecha = models.DateField(verbose_name="Fecha del asiento")
    concepto = models.TextField(verbose_name="Concepto/Descripción")
    referencia = models.CharField(max_length=100, blank=True, null=True, verbose_name="Referencia")
    documento = models.CharField(max_length=50, blank=True, null=True, verbose_name="No. Documento")
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT,
                               null=True, blank=True,
                               related_name='asientos', verbose_name="Moneda")
    tasa_cambio = models.DecimalField(max_digits=18, decimal_places=6, default=Decimal('1.000000'),
                                      verbose_name="Tasa de cambio")
    total_debe = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                     verbose_name="Total debe")
    total_haber = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                      verbose_name="Total haber")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR', verbose_name="Estado")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")
    aprobado_por = models.CharField(max_length=100, blank=True, null=True, verbose_name="Aprobado por")
    fecha_aprobacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de aprobación")

    def __str__(self):
        return f"{self.numero} - {self.fecha} - {self.concepto[:50]}"

    @property
    def esta_cuadrado(self):
        """Verifica que el asiento esté cuadrado (debe = haber)"""
        return self.total_debe == self.total_haber

    def recalcular_totales(self):
        """Recalcula totales desde las líneas de detalle"""
        from django.db.models import Sum
        totales = self.detalles.aggregate(
            total_d=Sum('debe'),
            total_h=Sum('haber')
        )
        self.total_debe = totales['total_d'] or Decimal('0.00')
        self.total_haber = totales['total_h'] or Decimal('0.00')
        self.save(update_fields=['total_debe', 'total_haber'])

    class Meta:
        db_table = 'cont_asiento_contable'
        verbose_name = "Asiento Contable"
        verbose_name_plural = "Asientos Contables"
        ordering = ['-fecha', '-numero']
        unique_together = ('numero', 'empresa')


class DetalleAsiento(ContabilidadBaseModel):
    """
    NIC 1 - Línea de detalle del asiento contable (partida doble).
    Cada línea tiene cargo (debe) o abono (haber).
    """
    asiento = models.ForeignKey(AsientoContable, on_delete=models.CASCADE,
                                related_name='detalles', verbose_name="Asiento")
    linea = models.IntegerField(verbose_name="Número de línea")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               related_name='movimientos', verbose_name="Cuenta contable")
    concepto = models.CharField(max_length=500, blank=True, null=True, verbose_name="Concepto de línea")
    debe = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'), verbose_name="Debe")
    haber = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'), verbose_name="Haber")
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.PROTECT,
                                     null=True, blank=True,
                                     related_name='movimientos', verbose_name="Centro de costo")
    tercero = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tercero")
    referencia = models.CharField(max_length=100, blank=True, null=True, verbose_name="Referencia")

    def __str__(self):
        return f"L{self.linea}: {self.cuenta.codigo} D:{self.debe} H:{self.haber}"

    class Meta:
        db_table = 'cont_detalle_asiento'
        verbose_name = "Detalle de Asiento"
        verbose_name_plural = "Detalles de Asientos"
        ordering = ['asiento', 'linea']
        unique_together = ('asiento', 'linea')


# ============================================================================
# LIBRO MAYOR
# ============================================================================

class LibroMayor(ContabilidadBaseModel):
    """
    NIC 1 - Saldos acumulados por cuenta y período.
    Permite consultas rápidas de saldos sin recorrer todos los asientos.
    """
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.CASCADE,
                               related_name='saldos', verbose_name="Cuenta contable")
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE,
                                related_name='saldos', verbose_name="Período contable")
    saldo_anterior = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                         verbose_name="Saldo anterior")
    debitos = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                  verbose_name="Total débitos del período")
    creditos = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                   verbose_name="Total créditos del período")
    saldo_final = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                      verbose_name="Saldo final")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.cuenta.codigo} - {self.periodo} - Saldo: {self.saldo_final}"

    def calcular_saldo_final(self):
        """Calcula el saldo final según la naturaleza de la cuenta"""
        if self.cuenta.naturaleza == 'DEUDORA':
            self.saldo_final = self.saldo_anterior + self.debitos - self.creditos
        else:
            self.saldo_final = self.saldo_anterior - self.debitos + self.creditos

    class Meta:
        db_table = 'cont_libro_mayor'
        verbose_name = "Libro Mayor"
        verbose_name_plural = "Registros del Libro Mayor"
        ordering = ['cuenta__codigo', 'periodo__ejercicio__anio', 'periodo__numero']
        unique_together = ('cuenta', 'periodo', 'empresa')


# ============================================================================
# NIC 16 - PROPIEDADES, PLANTA Y EQUIPO
# ============================================================================

class ActivoFijo(ContabilidadBaseModel):
    """
    NIC 16 - Reconocimiento y depreciación de activos fijos.
    Propiedades, planta y equipo con vida útil mayor a un período.
    """
    METODO_DEPRECIACION_CHOICES = [
        ('LINEA_RECTA', 'Línea recta'),
        ('SALDOS_DECRECIENTES', 'Saldos decrecientes'),
        ('UNIDADES_PRODUCCION', 'Unidades de producción'),
        ('SUMA_DIGITOS', 'Suma de dígitos de los años'),
    ]
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('DEPRECIADO', 'Totalmente depreciado'),
        ('BAJA', 'Dado de baja'),
        ('VENDIDO', 'Vendido'),
    ]

    codigo = models.CharField(max_length=20, verbose_name="Código del activo")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    cuenta_activo = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                      related_name='activos_fijos', verbose_name="Cuenta de activo")
    cuenta_depreciacion = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                            related_name='depreciaciones_acumuladas',
                                            verbose_name="Cuenta de depreciación acumulada")
    cuenta_gasto_depreciacion = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                                   related_name='gastos_depreciacion',
                                                   verbose_name="Cuenta gasto depreciación")
    fecha_adquisicion = models.DateField(verbose_name="Fecha de adquisición")
    costo_adquisicion = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Costo de adquisición")
    valor_residual = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                         verbose_name="Valor residual")
    vida_util_meses = models.IntegerField(verbose_name="Vida útil (meses)")
    metodo_depreciacion = models.CharField(max_length=30, choices=METODO_DEPRECIACION_CHOICES,
                                           default='LINEA_RECTA', verbose_name="Método de depreciación")
    depreciacion_acumulada = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                                 verbose_name="Depreciación acumulada")
    valor_en_libros = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                          verbose_name="Valor en libros")
    ubicacion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ubicación")
    responsable = models.CharField(max_length=200, blank=True, null=True, verbose_name="Responsable")
    numero_serie = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número de serie")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    @property
    def base_depreciable(self):
        """NIC 16: Base depreciable = costo - valor residual"""
        return self.costo_adquisicion - self.valor_residual

    @property
    def depreciacion_mensual(self):
        """Depreciación mensual por línea recta"""
        if self.vida_util_meses > 0:
            return self.base_depreciable / self.vida_util_meses
        return Decimal('0.00')

    class Meta:
        db_table = 'cont_activo_fijo'
        verbose_name = "Activo Fijo"
        verbose_name_plural = "Activos Fijos"
        ordering = ['codigo']
        unique_together = ('codigo', 'empresa')


class Depreciacion(ContabilidadBaseModel):
    """
    NIC 16 - Registro de cálculos de depreciación mensual.
    """
    activo = models.ForeignKey(ActivoFijo, on_delete=models.CASCADE,
                               related_name='depreciaciones', verbose_name="Activo fijo")
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.PROTECT,
                                related_name='depreciaciones', verbose_name="Período")
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto depreciación")
    depreciacion_acumulada = models.DecimalField(max_digits=18, decimal_places=2,
                                                  verbose_name="Depreciación acumulada")
    valor_en_libros = models.DecimalField(max_digits=18, decimal_places=2,
                                          verbose_name="Valor en libros")
    asiento = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='depreciaciones', verbose_name="Asiento generado")

    def __str__(self):
        return f"{self.activo.codigo} - {self.periodo} - {self.monto}"

    class Meta:
        db_table = 'cont_depreciacion'
        verbose_name = "Depreciación"
        verbose_name_plural = "Depreciaciones"
        ordering = ['activo', 'periodo']
        unique_together = ('activo', 'periodo')


# ============================================================================
# NIC 2 - INVENTARIOS
# ============================================================================


class TipoInventario(ContabilidadBaseModel):
    """
    Catálogo configurable por empresa (municipio, empresa de agua, etc.).
    Los nombres y el orden se definen aquí; no dependen de un listado fijo en código.
    """

    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio", db_index=True)
    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre del tipo",
        help_text="Ej. Químicos para tratamiento, Repuestos de bombeo, Suministros de oficina.",
    )
    orden = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Prioridad en listas y reportes (menor = primero).",
    )
    notas = models.TextField(
        blank=True,
        default="",
        verbose_name="Notas internas",
        help_text="Opcional: ámbito de uso (municipal, saneamiento, etc.).",
    )
    codigo_legacy = models.CharField(
        max_length=30,
        blank=True,
        default="",
        verbose_name="Código de referencia (heredado)",
        help_text="Clave del listado estándar anterior (p. ej. MATERIA_PRIMA); vacío si el tipo es totalmente nuevo.",
    )

    class Meta:
        db_table = "cont_tipo_inventario"
        verbose_name = "Tipo de inventario (catálogo)"
        verbose_name_plural = "Tipos de inventario (catálogo)"
        ordering = ["empresa", "orden", "nombre"]
        unique_together = ("empresa", "nombre")

    def __str__(self):
        return f"{self.nombre} ({self.empresa})"


class Inventario(ContabilidadBaseModel):
    """
    NIC 2 - Valoración y contabilización de inventarios.
    Debe medirse al menor entre costo y valor neto realizable (VNR).
    """
    METODO_VALORACION_CHOICES = [
        ('PEPS', 'Primeras Entradas, Primeras Salidas (FIFO)'),
        ('PROMEDIO', 'Costo Promedio Ponderado'),
        ('ESPECIFICA', 'Identificación Específica'),
    ]

    codigo = models.CharField(max_length=20, verbose_name="Código interno")
    tipo_inventario = models.ForeignKey(
        TipoInventario,
        on_delete=models.PROTECT,
        related_name="inventarios",
        null=True,
        blank=True,
        verbose_name="Tipo de inventario",
        help_text="Definido en el catálogo por empresa (configuración de tipos).",
    )
    nomenclatura = models.CharField(
        max_length=120,
        blank=True,
        default='',
        verbose_name="Nomenclatura / clasificación del material",
        help_text="Código de catálogo (p. ej. UNSPSC, CPV u homologación interna) para estandarizar el material.",
    )
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    cuenta_inventario = models.ForeignKey(
        CuentaContable,
        on_delete=models.PROTECT,
        related_name="inventarios",
        verbose_name="Cuenta de inventario",
        help_text=(
            "Vinculación con el plan de cuentas (catálogo contable de su empresa): cuenta de activo donde se "
            "reconoce el valor del stock de este ítem (existencias a costo o al menor entre costo y valor "
            "neto realizable, según NIC 2). Debe ser una cuenta de detalle que acepte movimientos, en la rama "
            "de inventarios o materiales. Solo puede elegir cuentas ya dadas de alta en Contabilidad → Plan de cuentas."
        ),
    )
    cuenta_costo_venta = models.ForeignKey(
        CuentaContable,
        on_delete=models.PROTECT,
        related_name="costos_venta",
        verbose_name="Cuenta de costo de venta / consumo",
        help_text=(
            "Segunda vinculación al mismo plan de cuentas: cuenta de gasto o de costo que se usa cuando el bien "
            "sale de inventario (venta, consumo interno, donación, merma o baja), para registrar el costo asociado "
            "(por ejemplo costo de ventas, consumo de materiales o gasto por servicios, según el caso). La cuenta "
            "concreta la define su ente y su manual contable; también debe existir en el catálogo contable."
        ),
    )
    unidad_medida = models.CharField(max_length=20, verbose_name="Unidad de medida")
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=Decimal('0.0000'),
                                   verbose_name="Cantidad en existencia")
    costo_unitario = models.DecimalField(max_digits=18, decimal_places=4, default=Decimal('0.0000'),
                                         verbose_name="Costo unitario")
    costo_total = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                      verbose_name="Costo total")
    valor_neto_realizable = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                                verbose_name="Valor neto realizable (VNR)")
    metodo_valoracion = models.CharField(max_length=20, choices=METODO_VALORACION_CHOICES,
                                         default='PROMEDIO', verbose_name="Método de valoración")
    stock_minimo = models.DecimalField(max_digits=18, decimal_places=4, default=Decimal('0.0000'),
                                       verbose_name="Stock mínimo")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    @property
    def valor_contable(self):
        """NIC 2: Menor entre costo y VNR"""
        return min(self.costo_total, self.valor_neto_realizable) if self.valor_neto_realizable > 0 else self.costo_total

    class Meta:
        db_table = 'cont_inventario'
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        ordering = ['tipo_inventario__orden', 'tipo_inventario__nombre', 'codigo']
        unique_together = ('codigo', 'empresa')


# ============================================================================
# NIC 37 - PROVISIONES, PASIVOS CONTINGENTES Y ACTIVOS CONTINGENTES
# ============================================================================

class Provision(ContabilidadBaseModel):
    """
    NIC 37 - Provisiones por obligaciones de incertidumbre en monto o vencimiento.
    Se reconocen cuando: existe obligación presente, es probable la salida de recursos,
    y se puede estimar fiablemente.
    """
    TIPO_CHOICES = [
        ('PROVISION', 'Provisión'),
        ('PASIVO_CONTINGENTE', 'Pasivo Contingente'),
        ('ACTIVO_CONTINGENTE', 'Activo Contingente'),
    ]
    PROBABILIDAD_CHOICES = [
        ('PROBABLE', 'Probable (>50%)'),
        ('POSIBLE', 'Posible (20-50%)'),
        ('REMOTA', 'Remota (<20%)'),
    ]

    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='PROVISION', verbose_name="Tipo")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               related_name='provisiones', verbose_name="Cuenta contable")
    monto_estimado = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto estimado")
    probabilidad = models.CharField(max_length=20, choices=PROBABILIDAD_CHOICES,
                                    default='PROBABLE', verbose_name="Probabilidad")
    fecha_origen = models.DateField(verbose_name="Fecha de origen")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha estimada de vencimiento")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas y justificación")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.tipo} - {self.descripcion[:50]}"

    class Meta:
        db_table = 'cont_provision'
        verbose_name = "Provisión"
        verbose_name_plural = "Provisiones"
        ordering = ['-fecha_origen']


# ============================================================================
# NIC 38 - ACTIVOS INTANGIBLES
# ============================================================================

class ActivoIntangible(ContabilidadBaseModel):
    """
    NIC 38 - Activos intangibles sin sustancia física.
    Ej: Licencias de software, patentes, marcas, derechos de autor.
    """
    TIPO_CHOICES = [
        ('VIDA_DEFINIDA', 'Vida útil definida'),
        ('VIDA_INDEFINIDA', 'Vida útil indefinida'),
    ]

    codigo = models.CharField(max_length=20, verbose_name="Código")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               related_name='intangibles', verbose_name="Cuenta contable")
    cuenta_amortizacion = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                            related_name='amortizaciones_intangibles',
                                            verbose_name="Cuenta amortización")
    tipo_vida = models.CharField(max_length=20, choices=TIPO_CHOICES,
                                 default='VIDA_DEFINIDA', verbose_name="Tipo de vida útil")
    costo_adquisicion = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Costo de adquisición")
    amortizacion_acumulada = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                                  verbose_name="Amortización acumulada")
    vida_util_meses = models.IntegerField(null=True, blank=True, verbose_name="Vida útil (meses)")
    fecha_adquisicion = models.DateField(verbose_name="Fecha de adquisición")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'cont_activo_intangible'
        verbose_name = "Activo Intangible"
        verbose_name_plural = "Activos Intangibles"
        ordering = ['codigo']
        unique_together = ('codigo', 'empresa')


# ============================================================================
# NIC 32, 39, NIIF 9 - INSTRUMENTOS FINANCIEROS
# ============================================================================

class InstrumentoFinanciero(ContabilidadBaseModel):
    """
    NIC 32/39, NIIF 9 - Clasificación, reconocimiento y medición de instrumentos financieros.
    """
    CLASIFICACION_CHOICES = [
        ('COSTO_AMORTIZADO', 'Costo amortizado'),
        ('VALOR_RAZONABLE_ORI', 'Valor razonable con cambios en ORI'),
        ('VALOR_RAZONABLE_RESULTADO', 'Valor razonable con cambios en resultados'),
    ]
    TIPO_CHOICES = [
        ('ACTIVO', 'Activo financiero'),
        ('PASIVO', 'Pasivo financiero'),
        ('PATRIMONIO', 'Instrumento de patrimonio'),
    ]

    codigo = models.CharField(max_length=20, verbose_name="Código")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    clasificacion = models.CharField(max_length=30, choices=CLASIFICACION_CHOICES,
                                     verbose_name="Clasificación NIIF 9")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               related_name='instrumentos_financieros', verbose_name="Cuenta contable")
    valor_nominal = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Valor nominal")
    valor_razonable = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                          verbose_name="Valor razonable")
    tasa_interes = models.DecimalField(max_digits=8, decimal_places=4, default=Decimal('0.0000'),
                                       verbose_name="Tasa de interés")
    fecha_emision = models.DateField(verbose_name="Fecha de emisión")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de vencimiento")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'cont_instrumento_financiero'
        verbose_name = "Instrumento Financiero"
        verbose_name_plural = "Instrumentos Financieros"
        ordering = ['codigo']


# ============================================================================
# NIC 12 - IMPUESTO A LAS GANANCIAS
# ============================================================================

class ImpuestoDiferido(ContabilidadBaseModel):
    """
    NIC 12 - Impuestos corrientes y diferidos.
    Diferencias temporarias entre base contable y fiscal.
    """
    TIPO_CHOICES = [
        ('ACTIVO', 'Impuesto diferido activo'),
        ('PASIVO', 'Impuesto diferido pasivo'),
    ]

    descripcion = models.CharField(max_length=500, verbose_name="Descripción de la diferencia")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               related_name='impuestos_diferidos', verbose_name="Cuenta contable")
    base_contable = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Base contable")
    base_fiscal = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Base fiscal")
    diferencia_temporaria = models.DecimalField(max_digits=18, decimal_places=2,
                                                verbose_name="Diferencia temporaria")
    tasa_impuesto = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tasa de impuesto (%)")
    impuesto_diferido = models.DecimalField(max_digits=18, decimal_places=2,
                                            verbose_name="Monto impuesto diferido")
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.PROTECT,
                                related_name='impuestos_diferidos', verbose_name="Período")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.tipo} - {self.descripcion[:50]}"

    def calcular_diferido(self):
        """Calcula el impuesto diferido"""
        self.diferencia_temporaria = self.base_contable - self.base_fiscal
        self.impuesto_diferido = abs(self.diferencia_temporaria) * (self.tasa_impuesto / 100)

    class Meta:
        db_table = 'cont_impuesto_diferido'
        verbose_name = "Impuesto Diferido"
        verbose_name_plural = "Impuestos Diferidos"
        ordering = ['-periodo']


# ============================================================================
# NIC 19 - BENEFICIOS A LOS EMPLEADOS
# ============================================================================

class BeneficioEmpleado(ContabilidadBaseModel):
    """
    NIC 19 - Beneficios a empleados a corto y largo plazo.
    Ej: Vacaciones, indemnizaciones, jubilaciones, bonificaciones.
    """
    TIPO_CHOICES = [
        ('CORTO_PLAZO', 'Beneficio a corto plazo'),
        ('POST_EMPLEO', 'Beneficio post-empleo'),
        ('LARGO_PLAZO', 'Beneficio a largo plazo'),
        ('TERMINACION', 'Beneficio por terminación'),
    ]

    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de beneficio")
    cuenta_gasto = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                     related_name='gastos_beneficios', verbose_name="Cuenta de gasto")
    cuenta_provision = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                         related_name='provisiones_beneficios',
                                         verbose_name="Cuenta de provisión")
    monto_mensual = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto mensual estimado")
    provision_acumulada = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                              verbose_name="Provisión acumulada")
    numero_empleados = models.IntegerField(default=0, verbose_name="Número de empleados")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.tipo} - {self.descripcion}"

    class Meta:
        db_table = 'cont_beneficio_empleado'
        verbose_name = "Beneficio a Empleado"
        verbose_name_plural = "Beneficios a Empleados"
        ordering = ['tipo']


# ============================================================================
# NIC 40 - PROPIEDADES DE INVERSIÓN
# ============================================================================

class PropiedadInversion(ContabilidadBaseModel):
    """
    NIC 40 - Inmuebles mantenidos para obtener rentas o plusvalías.
    Se distinguen de las propiedades ocupadas por el dueño (NIC 16).
    """
    MODELO_MEDICION_CHOICES = [
        ('COSTO', 'Modelo del costo'),
        ('VALOR_RAZONABLE', 'Modelo del valor razonable'),
    ]

    codigo = models.CharField(max_length=20, verbose_name="Código")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción del inmueble")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               related_name='propiedades_inversion', verbose_name="Cuenta contable")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    costo_adquisicion = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Costo de adquisición")
    valor_razonable = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                          verbose_name="Valor razonable")
    modelo_medicion = models.CharField(max_length=20, choices=MODELO_MEDICION_CHOICES,
                                       default='COSTO', verbose_name="Modelo de medición")
    ingreso_renta_mensual = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                                verbose_name="Ingreso por renta mensual")
    fecha_adquisicion = models.DateField(verbose_name="Fecha de adquisición")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'cont_propiedad_inversion'
        verbose_name = "Propiedad de Inversión"
        verbose_name_plural = "Propiedades de Inversión"
        ordering = ['codigo']
        unique_together = ('codigo', 'empresa')


# ============================================================================
# NIC 41 - AGRICULTURA
# ============================================================================

class ActivoBiologico(ContabilidadBaseModel):
    """
    NIC 41 - Activos biológicos y productos agrícolas.
    Medición a valor razonable menos costos de venta.
    """
    TIPO_CHOICES = [
        ('CONSUMIBLE', 'Activo biológico consumible'),
        ('PRODUCTOR', 'Activo biológico productor'),
    ]

    codigo = models.CharField(max_length=20, verbose_name="Código")
    descripcion = models.CharField(max_length=500, verbose_name="Descripción")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               related_name='activos_biologicos', verbose_name="Cuenta contable")
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=Decimal('0.0000'),
                                   verbose_name="Cantidad")
    unidad_medida = models.CharField(max_length=20, verbose_name="Unidad de medida")
    valor_razonable = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Valor razonable")
    costos_venta = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                       verbose_name="Costos estimados de venta")
    fecha_medicion = models.DateField(verbose_name="Fecha de última medición")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    @property
    def valor_neto(self):
        """NIC 41: Valor razonable menos costos de venta"""
        return self.valor_razonable - self.costos_venta

    class Meta:
        db_table = 'cont_activo_biologico'
        verbose_name = "Activo Biológico"
        verbose_name_plural = "Activos Biológicos"
        ordering = ['codigo']
        unique_together = ('codigo', 'empresa')


# ============================================================================
# NIC 23 - COSTOS POR PRÉSTAMOS
# ============================================================================

class CostoPrestamo(ContabilidadBaseModel):
    """
    NIC 23 - Capitalización de intereses en activos calificados.
    Los costos por préstamos directamente atribuibles a la adquisición o
    construcción de un activo calificado deben capitalizarse.
    """
    descripcion = models.CharField(max_length=500, verbose_name="Descripción del préstamo")
    cuenta_prestamo = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                        related_name='prestamos', verbose_name="Cuenta de préstamo")
    cuenta_interes = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                       related_name='intereses_prestamo', verbose_name="Cuenta de interés")
    monto_principal = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto principal")
    tasa_interes_anual = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Tasa de interés anual (%)")
    fecha_desembolso = models.DateField(verbose_name="Fecha de desembolso")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    interes_acumulado = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                            verbose_name="Interés acumulado")
    capitalizable = models.BooleanField(default=False, verbose_name="¿Es capitalizable? (activo calificado)")
    activo_calificado = models.ForeignKey(ActivoFijo, on_delete=models.SET_NULL,
                                          null=True, blank=True,
                                          related_name='prestamos', verbose_name="Activo calificado")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.descripcion[:50]} - {self.monto_principal}"

    class Meta:
        db_table = 'cont_costo_prestamo'
        verbose_name = "Costo por Préstamo"
        verbose_name_plural = "Costos por Préstamos"
        ordering = ['-fecha_desembolso']


# ============================================================================
# NIC 8 - POLÍTICAS CONTABLES
# ============================================================================

class PoliticaContable(ContabilidadBaseModel):
    """
    NIC 8 - Registro de políticas contables adoptadas.
    Cambios en políticas y estimaciones contables.
    """
    TIPO_CAMBIO_CHOICES = [
        ('POLITICA', 'Cambio de política contable'),
        ('ESTIMACION', 'Cambio en estimación contable'),
        ('ERROR', 'Corrección de error'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título de la política")
    descripcion = models.TextField(verbose_name="Descripción detallada")
    tipo_cambio = models.CharField(max_length=20, choices=TIPO_CAMBIO_CHOICES,
                                   blank=True, null=True, verbose_name="Tipo de cambio")
    fecha_vigencia = models.DateField(verbose_name="Fecha de vigencia")
    nic_relacionada = models.CharField(max_length=50, blank=True, null=True,
                                       verbose_name="NIC/NIIF relacionada")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.titulo}"

    class Meta:
        db_table = 'cont_politica_contable'
        verbose_name = "Política Contable"
        verbose_name_plural = "Políticas Contables"
        ordering = ['-fecha_vigencia']


# ============================================================================
# NIC 10 - HECHOS OCURRIDOS DESPUÉS DEL PERIODO
# ============================================================================

class HechoPosterior(ContabilidadBaseModel):
    """
    NIC 10 - Hechos ocurridos después del período sobre el que se informa.
    Pueden requerir ajuste o solo revelación.
    """
    TIPO_CHOICES = [
        ('AJUSTE', 'Hecho que implica ajuste'),
        ('NO_AJUSTE', 'Hecho que no implica ajuste (solo revelación)'),
    ]

    ejercicio = models.ForeignKey(EjercicioFiscal, on_delete=models.CASCADE,
                                  related_name='hechos_posteriores', verbose_name="Ejercicio fiscal")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de hecho")
    descripcion = models.TextField(verbose_name="Descripción del hecho")
    fecha_hecho = models.DateField(verbose_name="Fecha del hecho")
    impacto_financiero = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                             verbose_name="Impacto financiero estimado")
    asiento_ajuste = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='hechos_posteriores', verbose_name="Asiento de ajuste")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.tipo} - {self.descripcion[:50]}"

    class Meta:
        db_table = 'cont_hecho_posterior'
        verbose_name = "Hecho Posterior"
        verbose_name_plural = "Hechos Posteriores"
        ordering = ['-fecha_hecho']


# ============================================================================
# NIC 36 - DETERIORO DEL VALOR DE LOS ACTIVOS
# ============================================================================

class DeterioroActivo(ContabilidadBaseModel):
    """
    NIC 36 - Deterioro del valor de los activos.
    Asegura que los activos no estén contabilizados por encima de su importe recuperable.
    """
    TIPO_ACTIVO_CHOICES = [
        ('FIJO', 'Activo fijo (NIC 16)'),
        ('INTANGIBLE', 'Activo intangible (NIC 38)'),
        ('INVERSION', 'Propiedad de inversión (NIC 40)'),
        ('BIOLOGICO', 'Activo biológico (NIC 41)'),
    ]

    tipo_activo = models.CharField(max_length=20, choices=TIPO_ACTIVO_CHOICES, verbose_name="Tipo de activo")
    activo_fijo = models.ForeignKey(ActivoFijo, on_delete=models.CASCADE,
                                    null=True, blank=True,
                                    related_name='deterioros', verbose_name="Activo fijo")
    activo_intangible = models.ForeignKey(ActivoIntangible, on_delete=models.CASCADE,
                                          null=True, blank=True,
                                          related_name='deterioros', verbose_name="Activo intangible")
    cuenta_perdida = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                       related_name='deterioros', verbose_name="Cuenta de pérdida")
    valor_en_libros = models.DecimalField(max_digits=18, decimal_places=2,
                                          verbose_name="Valor en libros antes del deterioro")
    importe_recuperable = models.DecimalField(max_digits=18, decimal_places=2,
                                              verbose_name="Importe recuperable")
    perdida_deterioro = models.DecimalField(max_digits=18, decimal_places=2,
                                            verbose_name="Pérdida por deterioro")
    fecha_evaluacion = models.DateField(verbose_name="Fecha de evaluación")
    asiento = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='deterioros', verbose_name="Asiento generado")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"Deterioro - {self.tipo_activo} - {self.perdida_deterioro}"

    def calcular_deterioro(self):
        """NIC 36: Pérdida = Valor en libros - Importe recuperable"""
        if self.valor_en_libros > self.importe_recuperable:
            self.perdida_deterioro = self.valor_en_libros - self.importe_recuperable
        else:
            self.perdida_deterioro = Decimal('0.00')

    class Meta:
        db_table = 'cont_deterioro_activo'
        verbose_name = "Deterioro de Activo"
        verbose_name_plural = "Deterioros de Activos"
        ordering = ['-fecha_evaluacion']


# ============================================================================
# NIC 7 - ESTADO DE FLUJOS DE EFECTIVO
# ============================================================================

class FlujoEfectivo(ContabilidadBaseModel):
    """
    NIC 7 - Clasificación de flujos de efectivo.
    Categorización de movimientos de caja para el estado de flujos.
    """
    CATEGORIA_CHOICES = [
        ('OPERACION', 'Actividades de Operación'),
        ('INVERSION', 'Actividades de Inversión'),
        ('FINANCIAMIENTO', 'Actividades de Financiamiento'),
    ]

    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE,
                                related_name='flujos_efectivo', verbose_name="Período")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoría")
    concepto = models.CharField(max_length=500, verbose_name="Concepto")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                               null=True, blank=True,
                               related_name='flujos_efectivo', verbose_name="Cuenta contable")
    entrada = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                  verbose_name="Entrada de efectivo")
    salida = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                                 verbose_name="Salida de efectivo")
    neto = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'),
                               verbose_name="Flujo neto")
    empresa = models.CharField(max_length=10, verbose_name="Empresa/Municipio")

    def __str__(self):
        return f"{self.categoria} - {self.concepto[:50]}"

    def calcular_neto(self):
        """Calcula el flujo neto"""
        self.neto = self.entrada - self.salida

    class Meta:
        db_table = 'cont_flujo_efectivo'
        verbose_name = "Flujo de Efectivo"
        verbose_name_plural = "Flujos de Efectivo"
        ordering = ['periodo', 'categoria']

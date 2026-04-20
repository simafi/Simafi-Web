"""
Módulo de Facturación de Servicios Públicos - SIMAFI Web
Modelos para: Catastro de Usuarios, Rubros/Tarifas, Medidores,
Lecturas, Facturación por Ciclo, Órdenes de Trabajo
"""
from django.db import models
from django.utils import timezone
import os


# ─────────────────────────────────────────────────────────
# 1. CATÁLOGO DE RUBROS (T0001=Agua, T0002=Alcantarillado…)
# ─────────────────────────────────────────────────────────
class SPRubro(models.Model):
    TIPO_CHOICES = [
        ('F', 'Tasa Fija'),
        ('M', 'Medición (Consumo)'),
        ('A', 'Anual'),
    ]
    empresa        = models.CharField(max_length=4, verbose_name="Municipio/Empresa")
    codigo         = models.CharField(max_length=10, verbose_name="Código (ej. T0001)")
    descripcion    = models.CharField(max_length=200, verbose_name="Descripción")
    tipo_cobro     = models.CharField(max_length=1, choices=TIPO_CHOICES, default='F', verbose_name="Tipo de Cobro")
    cuenta         = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cuenta Contable Corriente")
    cuentarez      = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cuenta Contable Rezago")
    activo         = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateField(auto_now_add=True)
    usuario        = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'sp_rubro'
        unique_together = (('empresa', 'codigo'),)
        ordering = ['empresa', 'codigo']
        verbose_name = "Rubro Servicio Público"
        verbose_name_plural = "Rubros Servicios Públicos"

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


# ─────────────────────────────────────────────────────────
# 2. TARIFAS (fija o por tramos de consumo)
# ─────────────────────────────────────────────────────────
class SPTarifa(models.Model):
    empresa        = models.CharField(max_length=4, verbose_name="Municipio/Empresa")
    rubro          = models.CharField(max_length=10, verbose_name="Código Rubro")
    ano            = models.IntegerField(verbose_name="Año vigente")
    descripcion    = models.CharField(max_length=200, blank=True, null=True)
    cargo_fijo     = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Cargo Fijo")
    precio_m3      = models.DecimalField(max_digits=10, decimal_places=4, default=0, verbose_name="Precio por m³")
    minimo_m3      = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Consumo mínimo m³")
    usa_tramos     = models.BooleanField(default=False, verbose_name="Usa tarifas escalonadas")
    activo         = models.BooleanField(default=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    usuario        = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'sp_tarifa'
        unique_together = (('empresa', 'rubro', 'ano'),)
        ordering = ['empresa', 'rubro', '-ano']
        verbose_name = "Tarifa SP"
        verbose_name_plural = "Tarifas SP"

    def __str__(self):
        return f"{self.rubro} ({self.ano}) - Cargo fijo: {self.cargo_fijo}"


class SPTramoTarifa(models.Model):
    """Tramos escalonados: ej. 0-10 m³ a Q10, 11-20 m³ a Q15, etc."""
    tarifa         = models.ForeignKey(SPTarifa, on_delete=models.CASCADE, related_name='tramos')
    desde_m3       = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Desde m³")
    hasta_m3       = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Hasta m³ (vacío=ilimitado)")
    precio_m3      = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Precio por m³ en este tramo")
    orden          = models.IntegerField(default=1)

    class Meta:
        db_table = 'sp_tramo_tarifa'
        ordering = ['tarifa', 'orden']
        verbose_name = "Tramo Tarifa"
        verbose_name_plural = "Tramos Tarifa"

    def __str__(self):
        hasta = self.hasta_m3 or "∞"
        return f"{self.desde_m3} - {hasta} m³ @ {self.precio_m3}"


# ─────────────────────────────────────────────────────────
# 3. CATASTRO DE USUARIOS (Padrón de abonados)
# ─────────────────────────────────────────────────────────
class SPCatastroUsuario(models.Model):
    CATEGORIA_CHOICES = [
        ('D', 'Doméstico'),
        ('C', 'Comercial'),
        ('I', 'Industrial'),
        ('G', 'Gubernamental'),
        ('S', 'Social/ONG'),
    ]
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('S', 'Suspendido'),
        ('C', 'Cancelado'),
        ('M', 'Moroso'),
    ]
    empresa            = models.CharField(max_length=4, verbose_name="Municipio")
    codigo_abonado     = models.CharField(max_length=20, verbose_name="Código de Abonado")
    identidad          = models.CharField(max_length=20, blank=True, null=True, verbose_name="DNI/RTN")
    nombre             = models.CharField(max_length=200, verbose_name="Nombre completo")
    direccion          = models.TextField(verbose_name="Dirección del servicio")
    barrio             = models.CharField(max_length=100, blank=True, null=True, verbose_name="Barrio/Colonia")
    municipio_nombre   = models.CharField(max_length=100, blank=True, null=True, verbose_name="Municipio geográfico")
    categoria          = models.CharField(max_length=1, choices=CATEGORIA_CHOICES, default='D', verbose_name="Categoría")
    estado             = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A', verbose_name="Estado")
    ciclo              = models.CharField(max_length=5, blank=True, null=True, verbose_name="Ciclo de facturación")
    ruta               = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ruta de lectura")
    secuencia          = models.IntegerField(default=0, verbose_name="Secuencia en ruta")
    telefono           = models.CharField(max_length=20, blank=True, null=True)
    celular            = models.CharField(max_length=20, blank=True, null=True)
    correo             = models.CharField(max_length=100, blank=True, null=True)
    referencia         = models.TextField(blank=True, null=True, verbose_name="Referencia de ubicación")
    latitud            = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud           = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    fecha_conexion     = models.DateField(null=True, blank=True, verbose_name="Fecha de conexión")
    fecha_suspension   = models.DateField(null=True, blank=True)
    fecha_cancelacion  = models.DateField(null=True, blank=True)
    comentario         = models.TextField(blank=True, null=True)
    usuario            = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion     = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sp_catastro_usuario'
        unique_together = (('empresa', 'codigo_abonado'),)
        ordering = ['empresa', 'ciclo', 'ruta', 'secuencia']
        verbose_name = "Abonado de Servicios Públicos"
        verbose_name_plural = "Catastro de Abonados"

    def __str__(self):
        return f"{self.codigo_abonado} - {self.nombre}"


# ─────────────────────────────────────────────────────────
# 4. MEDIDORES
# ─────────────────────────────────────────────────────────
class SPMedidor(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo/Instalado'),
        ('D', 'Desmontado'),
        ('R', 'En reparación'),
        ('B', 'De baja'),
    ]
    empresa        = models.CharField(max_length=4)
    abonado        = models.ForeignKey(SPCatastroUsuario, on_delete=models.CASCADE, related_name='medidores')
    numero_serie   = models.CharField(max_length=50, verbose_name="N° de Serie")
    marca          = models.CharField(max_length=100, blank=True, null=True)
    diametro       = models.CharField(max_length=20, blank=True, null=True, verbose_name="Diámetro (pulgadas)")
    lectura_inicial= models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Lectura inicial (m³)")
    fecha_instalacion = models.DateField(null=True, blank=True)
    fecha_retiro   = models.DateField(null=True, blank=True)
    estado         = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    observacion    = models.TextField(blank=True, null=True)
    usuario        = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sp_medidor'
        ordering = ['-fecha_instalacion']
        verbose_name = "Medidor"
        verbose_name_plural = "Medidores"

    def __str__(self):
        return f"Medidor {self.numero_serie} - {self.abonado.codigo_abonado}"


# ─────────────────────────────────────────────────────────
# 5. CICLOS / RUTAS DE LECTURA
# ─────────────────────────────────────────────────────────
class SPCicloRuta(models.Model):
    empresa        = models.CharField(max_length=4)
    ciclo          = models.CharField(max_length=5, verbose_name="Código de ciclo (ej. C001)")
    descripcion    = models.CharField(max_length=100)
    ruta           = models.CharField(max_length=10, blank=True, null=True)
    lecturador     = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lector responsable")
    dia_lectura    = models.IntegerField(null=True, blank=True, verbose_name="Día de lectura del mes")
    activo         = models.BooleanField(default=True)

    class Meta:
        db_table = 'sp_ciclo_ruta'
        unique_together = (('empresa', 'ciclo', 'ruta'),)
        ordering = ['empresa', 'ciclo', 'ruta']
        verbose_name = "Ciclo/Ruta"
        verbose_name_plural = "Ciclos y Rutas"

    def __str__(self):
        return f"Ciclo {self.ciclo} - Ruta {self.ruta or 'N/A'} ({self.empresa})"


# ─────────────────────────────────────────────────────────
# 5B. CALENDARIO DE PROCESOS (lecturas, facturación, cortes…)
# ─────────────────────────────────────────────────────────
class SPProcesoCalendario(models.Model):
    TIPO_CHOICES = [
        ("L", "Lecturas"),
        ("F", "Facturación"),
        ("C", "Cortes/Reconexiones"),
        ("R", "Reporte"),
        ("O", "Otro"),
    ]

    empresa = models.CharField(max_length=4, verbose_name="Municipio/Empresa")
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default="O")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    inicio = models.DateTimeField(verbose_name="Inicio")
    fin = models.DateTimeField(blank=True, null=True, verbose_name="Fin")
    todo_el_dia = models.BooleanField(default=False, verbose_name="Todo el día")
    color = models.CharField(max_length=20, blank=True, null=True, verbose_name="Color (CSS/HEX)")
    usuario = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sp_proceso_calendario"
        ordering = ["-inicio"]
        verbose_name = "Proceso (Calendario)"
        verbose_name_plural = "Calendario de Procesos"

    def __str__(self):
        return f"{self.empresa} - {self.titulo} ({self.inicio:%Y-%m-%d})"


# ─────────────────────────────────────────────────────────
# 6. LECTURAS DE MEDIDORES
# ─────────────────────────────────────────────────────────
def foto_medidor_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'sp_lecturas/{instance.empresa}/{instance.abonado_id}/{instance.periodo_ano}-{instance.periodo_mes:02d}{ext}'


class SPLectura(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('V', 'Validada'),
        ('F', 'Facturada'),
        ('A', 'Anulada'),
    ]
    empresa        = models.CharField(max_length=4)
    abonado        = models.ForeignKey(SPCatastroUsuario, on_delete=models.CASCADE, related_name='lecturas')
    medidor        = models.ForeignKey(SPMedidor, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturas')
    periodo_ano    = models.IntegerField(verbose_name="Año")
    periodo_mes    = models.IntegerField(verbose_name="Mes")
    lectura_anterior = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Lectura anterior m³")
    lectura_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Lectura actual m³")
    consumo_m3     = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Consumo m³")
    consumo_promedio = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Promedio histórico m³")
    es_estimado    = models.BooleanField(default=False, verbose_name="Lectura estimada/promedio")
    fecha_lectura  = models.DateField(verbose_name="Fecha de lectura")
    # FileField (no ImageField): evita exigir Pillow en el arranque; sigue admitiendo imágenes y .url en plantillas.
    foto_medidor   = models.FileField(upload_to=foto_medidor_path, null=True, blank=True, verbose_name="Foto del medidor")
    lecturador     = models.CharField(max_length=100, blank=True, null=True)
    observacion    = models.TextField(blank=True, null=True)
    estado         = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    usuario        = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sp_lectura'
        unique_together = (('empresa', 'abonado', 'periodo_ano', 'periodo_mes'),)
        ordering = ['-periodo_ano', '-periodo_mes', 'abonado']
        verbose_name = "Lectura de Medidor"
        verbose_name_plural = "Lecturas de Medidores"

    def __str__(self):
        return f"Lectura {self.abonado.codigo_abonado} {self.periodo_ano}-{self.periodo_mes:02d}: {self.consumo_m3} m³"

    def save(self, *args, **kwargs):
        # Auto-calcular consumo
        self.consumo_m3 = max(0, self.lectura_actual - self.lectura_anterior)
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────────────────
# 7. FACTURAS
# ─────────────────────────────────────────────────────────
class SPFactura(models.Model):
    ESTADO_CHOICES = [
        ('E', 'Emitida'),
        ('P', 'Pagada'),
        ('V', 'Vencida'),
        ('A', 'Anulada'),
        ('PP', 'Pago parcial'),
    ]
    empresa        = models.CharField(max_length=4)
    numero_factura = models.IntegerField(verbose_name="N° de factura")
    abonado        = models.ForeignKey(SPCatastroUsuario, on_delete=models.CASCADE, related_name='facturas')
    periodo_ano    = models.IntegerField(verbose_name="Año")
    periodo_mes    = models.IntegerField(verbose_name="Mes")
    ciclo          = models.CharField(max_length=5, blank=True, null=True)
    fecha_emision  = models.DateField(default=timezone.now)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    lectura        = models.ForeignKey(SPLectura, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas')
    subtotal       = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descuentos     = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    mora           = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total          = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    estado         = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='E')
    observacion    = models.TextField(blank=True, null=True)
    usuario        = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_pago     = models.DateField(null=True, blank=True)
    recibo_pago    = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'sp_factura'
        unique_together = (('empresa', 'numero_factura'),)
        ordering = ['-periodo_ano', '-periodo_mes', 'abonado']
        verbose_name = "Factura SP"
        verbose_name_plural = "Facturas SP"

    def __str__(self):
        return f"Factura #{self.numero_factura} - {self.abonado.codigo_abonado} {self.periodo_ano}-{self.periodo_mes:02d}"


class SPDetalleFactura(models.Model):
    factura        = models.ForeignKey(SPFactura, on_delete=models.CASCADE, related_name='detalles')
    rubro          = models.CharField(max_length=10)
    descripcion    = models.CharField(max_length=200)
    consumo_m3     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cargo_fijo     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cargo_consumo  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal       = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'sp_detalle_factura'
        verbose_name = "Detalle Factura SP"
        verbose_name_plural = "Detalles Factura SP"


# ─────────────────────────────────────────────────────────
# 7B. CATÁLOGOS PARA ÓRDENES DE TRABAJO
# ─────────────────────────────────────────────────────────
class SPResponsable(models.Model):
    """Cuadrilla / fontanero responsable por código."""

    empresa = models.CharField(max_length=4, verbose_name="Municipio/Empresa")
    codigo = models.CharField(max_length=20, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    telefono = models.CharField(max_length=30, blank=True, null=True)
    activo = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sp_responsable"
        unique_together = (("empresa", "codigo"),)
        ordering = ["empresa", "codigo"]
        verbose_name = "Responsable (Fontanero)"
        verbose_name_plural = "Responsables (Fontaneros)"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class SPConceptoOT(models.Model):
    """Conceptos / tipos de reclamo para clasificar OTs y resumir pendientes/atendidas."""

    empresa = models.CharField(max_length=4, verbose_name="Municipio/Empresa")
    codigo = models.CharField(max_length=20, verbose_name="Código")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    activo = models.BooleanField(default=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sp_concepto_ot"
        unique_together = (("empresa", "codigo"),)
        ordering = ["empresa", "codigo"]
        verbose_name = "Concepto de Orden (Reclamo)"
        verbose_name_plural = "Conceptos de Orden (Reclamos)"

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


# ─────────────────────────────────────────────────────────
# 8. ÓRDENES DE TRABAJO
# ─────────────────────────────────────────────────────────
class SPOrdenTrabajo(models.Model):
    TIPO_CHOICES = [
        ('NI', 'Nueva instalación'),
        ('RM', 'Reposición de medidor'),
        ('RP', 'Reparación/fuga'),
        ('CO', 'Corte de servicio'),
        ('RC', 'Reconexión de servicio'),
        ('IN', 'Inspección'),
        ('MN', 'Mantenimiento preventivo'),
        ('OT', 'Otro'),
    ]
    PRIORIDAD_CHOICES = [
        ('A', 'Alta'),
        ('M', 'Media'),
        ('B', 'Baja'),
    ]
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('A', 'Asignada'),
        ('E', 'En ejecución'),
        ('C', 'Completada'),
        ('X', 'Cancelada'),
    ]
    empresa        = models.CharField(max_length=4)
    numero_ot      = models.IntegerField(verbose_name="N° de Orden")
    abonado        = models.ForeignKey(SPCatastroUsuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_trabajo')
    concepto       = models.ForeignKey(SPConceptoOT, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes', verbose_name="Concepto/Reclamo")
    tipo           = models.CharField(max_length=2, choices=TIPO_CHOICES, default='IN')
    descripcion    = models.TextField(verbose_name="Descripción del trabajo")
    prioridad      = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')
    estado         = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    tecnico_asignado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Técnico asignado")
    responsable_asignado = models.ForeignKey(
        SPResponsable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordenes_asignadas",
        verbose_name="Responsable (asignado)",
    )
    responsable_cierre = models.ForeignKey(SPResponsable, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_cerradas', verbose_name="Responsable (cierre)")
    fecha_emision  = models.DateField(default=timezone.now)
    fecha_programada = models.DateField(null=True, blank=True)
    fecha_inicio   = models.DateField(null=True, blank=True)
    fecha_cierre   = models.DateField(null=True, blank=True)
    observacion    = models.TextField(blank=True, null=True)
    resultado      = models.TextField(blank=True, null=True, verbose_name="Resultado/Cierre")
    costo_total    = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usuario        = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sp_orden_trabajo'
        unique_together = (('empresa', 'numero_ot'),)
        ordering = ['-fecha_emision', '-numero_ot']
        verbose_name = "Orden de Trabajo"
        verbose_name_plural = "Órdenes de Trabajo"

    def __str__(self):
        return f"OT #{self.numero_ot} - {self.get_tipo_display()} ({self.estado})"


class SPInsumoOrdenTrabajo(models.Model):
    orden          = models.ForeignKey(SPOrdenTrabajo, on_delete=models.CASCADE, related_name='insumos')
    descripcion    = models.CharField(max_length=200, verbose_name="Material/Insumo")
    unidad         = models.CharField(max_length=30, blank=True, null=True)
    cantidad       = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal       = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'sp_insumo_orden_trabajo'
        verbose_name = "Insumo OT"
        verbose_name_plural = "Insumos OT"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.costo_unitario
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────────────────
# 9. CONTROL DE CORTES Y RECONEXIONES
# ─────────────────────────────────────────────────────────
class SPCorteSuspension(models.Model):
    TIPO_CHOICES = [
        ('C', 'Corte por mora'),
        ('R', 'Reconexión'),
        ('CS', 'Corte a solicitud'),
        ('RS', 'Reconexión por solicitud'),
    ]
    empresa        = models.CharField(max_length=4)
    abonado        = models.ForeignKey(SPCatastroUsuario, on_delete=models.CASCADE, related_name='cortes')
    tipo           = models.CharField(max_length=2, choices=TIPO_CHOICES)
    fecha          = models.DateField(default=timezone.now)
    orden_trabajo  = models.ForeignKey(SPOrdenTrabajo, on_delete=models.SET_NULL, null=True, blank=True)
    monto_adeudado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observacion    = models.TextField(blank=True, null=True)
    usuario        = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sp_corte_suspension'
        ordering = ['-fecha']
        verbose_name = "Corte/Reconexión"
        verbose_name_plural = "Cortes y Reconexiones"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.abonado.codigo_abonado} ({self.fecha})"


# ─────────────────────────────────────────────────────────
# 10. CONSECUTIVO DE FACTURAS
# ─────────────────────────────────────────────────────────
class SPConsecutivo(models.Model):
    empresa        = models.CharField(max_length=4, unique=True)
    ultimo_numero  = models.IntegerField(default=0)
    ultimo_numero_ot = models.IntegerField(default=0)

    class Meta:
        db_table = 'sp_consecutivo'

    @classmethod
    def siguiente_factura(cls, empresa):
        obj, _ = cls.objects.get_or_create(empresa=empresa)
        obj.ultimo_numero += 1
        obj.save()
        return obj.ultimo_numero

    @classmethod
    def siguiente_ot(cls, empresa):
        obj, _ = cls.objects.get_or_create(empresa=empresa)
        obj.ultimo_numero_ot += 1
        obj.save()
        return obj.ultimo_numero_ot

from django.db import models
from core.models import BaseModel, Municipio
from decimal import Decimal


class Identificacion(models.Model):
    """
    Modelo de identificación de contribuyentes - Estructura alineada con la tabla real de la base de datos
    """
    identidad = models.CharField(max_length=18, unique=True, verbose_name="Identidad", db_collation='latin1_swedish_ci')
    nombres = models.CharField(max_length=30, null=True, blank=True, verbose_name="Nombres", db_collation='latin1_swedish_ci')
    apellidos = models.CharField(max_length=30, null=True, blank=True, verbose_name="Apellidos", db_collation='latin1_swedish_ci')
    fechanac = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    
    def __str__(self):
        return f"{self.identidad} - {self.nombres} {self.apellidos}"
    
    class Meta:
        db_table = 'identificacion'
        verbose_name = "Identificación"
        verbose_name_plural = "Identificaciones"
        app_label = 'tributario_app'


class Actividad(models.Model):
    """
    Modelo de actividades - Estructura alineada con la tabla real de la base de datos
    
    CREATE TABLE `actividad` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `empresa` CHAR(4) COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
      `codigo` CHAR(20) COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
      `cuentarez` CHAR(20) COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
      `cuentarec` CHAR(20) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
      `cuentaint` CHAR(20) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
      `descripcion` CHAR(200) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
      PRIMARY KEY USING BTREE (`id`),
      UNIQUE KEY `actividad_idx1` USING BTREE (`empresa`, `codigo`),
      UNIQUE KEY `actividad_empresa_codigo_4b4f70db_uniq` USING BTREE (`empresa`, `codigo`)
    ) ENGINE=MyISAM
    """
    empresa = models.CharField(max_length=4, default='', verbose_name="Empresa", db_collation='utf8mb4_0900_ai_ci')
    codigo = models.CharField(max_length=20, default='', verbose_name="Código", db_collation='utf8mb4_0900_ai_ci')
    cuentarez = models.CharField(max_length=20, default='', verbose_name="Cuenta Rezago", db_collation='utf8mb4_0900_ai_ci')
    cuentarec = models.CharField(max_length=20, blank=True, default='', verbose_name="Cuenta Recargos", db_collation='utf8mb4_0900_ai_ci')
    cuentaint = models.CharField(max_length=20, blank=True, default='', verbose_name="Cuenta Intereses", db_collation='utf8mb4_0900_ai_ci')
    descripcion = models.CharField(max_length=200, blank=True, default='', verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci')
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
    class Meta:
        db_table = 'actividad'
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        unique_together = ('empresa', 'codigo')
        app_label = 'tributario_app'


class Oficina(models.Model):
    """
    Modelo de oficinas - Estructura alineada con la tabla real de la base de datos
    """
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='utf8mb4_0900_ai_ci')
    codigo = models.CharField(max_length=20, verbose_name="Código", db_collation='utf8mb4_0900_ai_ci')
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci')
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
    class Meta:
        db_table = 'oficina'
        verbose_name = "Oficina"
        verbose_name_plural = "Oficinas"
        unique_together = ('empresa', 'codigo')
        app_label = 'tributario_app'


class Negocio(models.Model):
    """
    Modelo de negocios - Estructura alineada exactamente con la tabla real de la base de datos
    
    CREATE TABLE `negocios` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `empresa` VARCHAR(4) NOT NULL,
      `rtm` VARCHAR(16) NOT NULL,
      `expe` VARCHAR(12) NOT NULL,
      `nombrenego` VARCHAR(100) DEFAULT ' ',
      `comerciante` VARCHAR(100) DEFAULT ' ',
      `identidad` VARCHAR(20) NOT NULL,
      `rtnpersonal` VARCHAR(20) DEFAULT ' ',
      `rtnnego` VARCHAR(19) DEFAULT ' ',
      `catastral` VARCHAR(17) NOT NULL,
      `identidadrep` VARCHAR(20) DEFAULT ' ',
      `representante` VARCHAR(100) DEFAULT ' ',
      `direccion` VARCHAR(100) DEFAULT ' ',
      `actividad` VARCHAR(20) DEFAULT ' ',
      `estatus` VARCHAR(1) NOT NULL,
      `descriestatus` VARCHAR(50) DEFAULT ' ',
      `fecha_ini` DATE DEFAULT NULL,
      `fecha_can` DATE DEFAULT NULL,
      `telefono` VARCHAR(20) DEFAULT ' ',
      `celular` VARCHAR(20) DEFAULT ' ',
      `socios` VARCHAR(250) NOT NULL,
      `correo` VARCHAR(35) DEFAULT ' ',
      `pagweb` VARCHAR(40) DEFAULT ' ',
      `comentario` LONGTEXT DEFAULT NULL,
      `descriactividad` VARCHAR(100) DEFAULT ' ',
      `usuario` VARCHAR(10) DEFAULT ' ',
      `fechasys` DATETIME DEFAULT NULL,
      `cx` DECIMAL(12,2) DEFAULT 0.00,
      `cy` DECIMAL(12,2) DEFAULT 0.00
    )
    """
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    rtm = models.CharField(max_length=16, verbose_name="RTM", db_collation='latin1_swedish_ci')
    expe = models.CharField(max_length=12, verbose_name="Expediente", db_collation='latin1_swedish_ci')
    nombrenego = models.CharField(max_length=100, default=' ', verbose_name="Nombre Negocio", db_collation='latin1_swedish_ci')
    comerciante = models.CharField(max_length=100, default=' ', verbose_name="Comerciante", db_collation='latin1_swedish_ci')
    identidad = models.CharField(max_length=20, verbose_name="Identidad", db_collation='latin1_swedish_ci')
    rtnpersonal = models.CharField(max_length=20, default=' ', verbose_name="RTN Personal", db_collation='latin1_swedish_ci')
    rtnnego = models.CharField(max_length=19, default=' ', verbose_name="RTN Negocio", db_collation='latin1_swedish_ci')
    catastral = models.CharField(max_length=17, verbose_name="Catastral", db_collation='latin1_swedish_ci')
    identidadrep = models.CharField(max_length=20, default=' ', verbose_name="Identidad Representante", db_collation='latin1_swedish_ci')
    representante = models.CharField(max_length=100, default=' ', verbose_name="Representante", db_collation='latin1_swedish_ci')
    direccion = models.CharField(max_length=100, default=' ', verbose_name="Dirección", db_collation='latin1_swedish_ci')
    actividad = models.CharField(max_length=20, default=' ', verbose_name="Actividad", db_collation='latin1_swedish_ci')
    estatus = models.CharField(max_length=1, verbose_name="Estatus", db_collation='latin1_swedish_ci')
    descriestatus = models.CharField(max_length=50, default=' ', verbose_name="Descripción Estatus", db_collation='latin1_swedish_ci')
    fecha_ini = models.DateField(null=True, blank=True, verbose_name="Fecha Inicio")
    fecha_can = models.DateField(null=True, blank=True, verbose_name="Fecha Cancelación")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    telefono = models.CharField(max_length=20, default=' ', verbose_name="Teléfono", db_collation='latin1_swedish_ci')
    celular = models.CharField(max_length=20, default=' ', verbose_name="Celular", db_collation='latin1_swedish_ci')
    socios = models.CharField(max_length=250, verbose_name="Socios", db_collation='latin1_swedish_ci')
    correo = models.CharField(max_length=35, default=' ', verbose_name="Correo", db_collation='latin1_swedish_ci')
    pagweb = models.CharField(max_length=40, default=' ', verbose_name="Página Web", db_collation='latin1_swedish_ci')
    comentario = models.TextField(null=True, blank=True, verbose_name="Comentario", db_collation='latin1_swedish_ci')
    descriactividad = models.CharField(max_length=100, default=' ', verbose_name="Descripción Actividad", db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=10, default=' ', verbose_name="Usuario", db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Sistema")
    cx = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Coordenada X (UTM)")
    cy = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Coordenada Y (UTM)")
    
    def __str__(self):
        return f"{self.rtm} - {self.nombrenego}"
    
    @property
    def info_edad(self):
        """
        Retorna información del grupo etario del contribuyente.
        Utiliza el DNI (identidad) o la fecha_nacimiento manual.
        """
        from .tributario_app.utils_cedula import info_cedula
        return info_cedula(self.identidad, self.fecha_nacimiento)

    def es_tercera_edad(self):
        return self.info_edad['aplica_tercera_edad']

    def es_cuarta_edad(self):
        return self.info_edad['aplica_cuarta_edad']
    
    class Meta:
        db_table = 'negocios'
        verbose_name = "Negocio"
        verbose_name_plural = "Negocios"
        unique_together = ('empresa', 'rtm', 'expe')
        app_label = 'tributario_app'
        indexes = [
            models.Index(fields=['nombrenego']),
            models.Index(fields=['comerciante']),
            models.Index(fields=['identidad']),
            models.Index(fields=['rtm']),
            models.Index(fields=['expe']),
            models.Index(fields=['actividad']),
        ]


class PagoVariosTemp(models.Model):
    """
    Modelo temporal de pagos varios - Estructura exacta según CREATE TABLE
    """
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=6, null=True, blank=True, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    recibo = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Recibo")
    rubro = models.CharField(max_length=6, default='', blank=True, verbose_name="Rubro", db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=16, verbose_name="Código", db_collation='latin1_swedish_ci')
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha")
    identidad = models.CharField(max_length=31, null=True, blank=True, verbose_name="Identidad", db_collation='latin1_swedish_ci')
    nombre = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nombre", db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción", db_collation='latin1_swedish_ci')
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor")
    comentario = models.CharField(max_length=500, null=True, blank=True, verbose_name="Comentario", db_collation='latin1_swedish_ci')
    oficina = models.CharField(max_length=20, null=True, blank=True, verbose_name="Oficina", db_collation='latin1_swedish_ci')
    facturadora = models.CharField(max_length=45, null=True, blank=True, verbose_name="Facturadora", db_collation='latin1_swedish_ci')
    aplicado = models.CharField(max_length=1, default='0', verbose_name="Aplicado", db_collation='latin1_swedish_ci')
    traslado = models.CharField(max_length=1, default='0', verbose_name="Traslado", db_collation='latin1_swedish_ci')
    solvencia = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="Solvencia")
    fecha_solv = models.DateField(null=True, blank=True, verbose_name="Fecha Solvencia")
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Cantidad")
    vl_unit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Unitario")
    deposito = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name="Depósito")
    cajero = models.CharField(max_length=20, null=True, blank=True, verbose_name="Cajero", db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=30, null=True, blank=True, verbose_name="Usuario", db_collation='latin1_swedish_ci')
    referencia = models.CharField(max_length=20, null=True, blank=True, verbose_name="Referencia", db_collation='latin1_swedish_ci')
    banco = models.CharField(max_length=3, null=True, blank=True, verbose_name="Banco", db_collation='latin1_swedish_ci')
    Tipofa = models.CharField(max_length=1, default=' ', verbose_name="Tipo de Factura", db_collation='latin1_swedish_ci')
    Rtm = models.CharField(max_length=20, default=' ', verbose_name="RTM", db_collation='latin1_swedish_ci')
    expe = models.CharField(max_length=12, default='0', verbose_name='Expediente', db_collation='latin1_swedish_ci')
    pagodia = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Pago del Día")
    rcaja = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Recibo de Caja")
    Rfechapag = models.DateField(null=True, blank=True, verbose_name="Fecha de Pago Real")
    permiso = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Permiso")
    Fechavence = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    direccion = models.CharField(max_length=100, default=' ', verbose_name="Dirección", db_collation='latin1_swedish_ci')
    prima = models.CharField(max_length=1, default='', verbose_name="Prima", db_collation='latin1_swedish_ci')
    categoria = models.CharField(max_length=2, default='', verbose_name="Categoría", db_collation='latin1_swedish_ci')
    sexo = models.CharField(max_length=1, default='', verbose_name="Sexo", db_collation='latin1_swedish_ci')
    rtn = models.CharField(max_length=20, null=True, blank=True, verbose_name="RTN", db_collation='latin1_swedish_ci')
    
    def __str__(self):
        return f"ID: {self.id} - Recibo {self.recibo} - {self.nombre} - ${self.valor}"
    
    def calcular_total(self):
        """Calcula el total basado en cantidad * valor unitario"""
        return self.cantidad * self.vl_unit
    
    def es_valido(self):
        """Verifica si el registro tiene los campos mínimos requeridos"""
        return (
            self.recibo and 
            self.codigo and 
            self.valor > 0
        )
    
    def get_display_name(self):
        """Retorna un nombre legible para el registro"""
        if self.nombre:
            return f"{self.nombre} - Recibo {self.recibo}"
        return f"Recibo {self.recibo}"
    
    def save(self, *args, **kwargs):
        """Sobrescribe el método save para validaciones adicionales"""
        # Si no hay valor calculado, calcularlo
        if not self.valor or self.valor == 0:
            self.valor = self.calcular_total()
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'pagovariostemp'
        verbose_name = "Pago Varios Temporal"
        verbose_name_plural = "Pagos Varios Temporales"
        ordering = ['-fecha', '-recibo']
        indexes = [
            models.Index(fields=['recibo']),
            models.Index(fields=['solvencia']),
            models.Index(fields=['codigo']),
            models.Index(fields=['fecha']),
        ]
        app_label = 'tributario_app'


class NoRecibos(models.Model):
    """
    Modelo de números de recibos - Estructura exacta según CREATE TABLE
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=6, null=True, blank=True, default=None, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    numero = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Número")
    solvencia = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Solvencia")
    
    def __str__(self):
        return f"ID: {self.id} - Empresa: {self.empresa or 'GLOBAL'} - Número: {self.numero}"
    
    @classmethod
    def obtener_siguiente_numero(cls):
        """
        Mantiene compatibilidad para llamadas heredadas utilizando el control global.
        """
        return cls.obtener_siguiente_numero_por_empresa(None)
    
    @classmethod
    def obtener_siguiente_numero_por_empresa(cls, empresa):
        """
        Obtiene el siguiente número de recibo controlado por empresa.
        Incrementa el número y lo guarda en la tabla para mantener la secuencia.
        """
        try:
            from django.db import transaction
            
            empresa_normalizada = (empresa or '').strip() or None
            
            with transaction.atomic():
                registro = (
                    cls.objects.select_for_update()
                    .filter(empresa=empresa_normalizada)
                    .first()
                )
                
                if not registro:
                    registro = cls.objects.create(
                        empresa=empresa_normalizada,
                        numero=0,
                        solvencia=0
                    )
                
                registro.numero = (registro.numero or 0) + 1
                registro.save(update_fields=['numero'])
                
                return int(registro.numero)
                
        except Exception as e:
            # En caso de error, usar timestamp como fallback
            import time
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error al obtener siguiente número de recibo: {str(e)}")
            return int(time.time())
    
    class Meta:
        db_table = 'norecibos'
        verbose_name = "Número de Recibo"
        verbose_name_plural = "Números de Recibos"
        app_label = 'tributario_app'


class Rubro(models.Model):
    """
    Modelo para la tabla rubros.
    Estructura alineada exactamente con la tabla real de la base de datos.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='utf8mb4_0900_ai_ci', default='')
    codigo = models.CharField(max_length=6, verbose_name="Código", db_collation='utf8mb4_0900_ai_ci', default='')
    descripcion = models.CharField(max_length=200, blank=True, verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci', default='')
    cuenta = models.CharField(max_length=20, blank=True, verbose_name="Cuenta", db_collation='utf8mb4_0900_ai_ci', default='')
    cuentarez = models.CharField(max_length=20, blank=True, verbose_name="Cuenta Rezago", db_collation='utf8mb4_0900_ai_ci', default='')
    tipo = models.CharField(max_length=1, blank=True, verbose_name="Tipo", db_collation='utf8mb4_0900_ai_ci', default='')

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    # ── Propiedades de tipo inferidas por prefijo de código ──────────────────
    # No requieren ALTER TABLE; se determinan dinámicamente por convención:
    #   RT* = Recargo sobre Tasa
    #   RB* = Recargo Bienes Inmuebles Urbano
    #   RR* = Recargo Bienes Inmuebles Rural
    #   RC* = Recargo Comercio/ICS
    #   T*  = Tasa (agua, aseo, etc.)
    #   B*  = Bienes Inmuebles
    #   resto = Impuesto general

    @property
    def es_recargo(self):
        """True si el código comienza con R (recargo moratorio)"""
        return self.codigo.upper().startswith('R')

    @property
    def es_recargo_tasa(self):
        return self.codigo.upper().startswith('RT')

    @property
    def es_recargo_bi_urbano(self):
        return self.codigo.upper().startswith('RB')

    @property
    def es_recargo_bi_rural(self):
        return self.codigo.upper().startswith('RR')

    @property
    def es_recargo_comercio(self):
        return self.codigo.upper().startswith('RC')

    @property
    def es_tasa(self):
        """True si el código comienza con T (tasa de servicio)"""
        return self.codigo.upper().startswith('T') and not self.es_recargo

    @property
    def es_bien_inmueble(self):
        """True si el código comienza con B (bienes inmuebles)"""
        return self.codigo.upper().startswith('B')

    @property
    def tipo_descripcion(self):
        """Descripción legible del tipo de rubro"""
        c = self.codigo.upper()
        if c.startswith('RT'):  return 'Recargo Tasa'
        if c.startswith('RB'):  return 'Recargo BI Urbano'
        if c.startswith('RR'):  return 'Recargo BI Rural'
        if c.startswith('RC'):  return 'Recargo Comercio'
        if c.startswith('R'):   return 'Recargo'
        if c.startswith('T'):   return 'Tasa'
        if c.startswith('B'):   return 'Bienes Inmuebles'
        return 'Impuesto'

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para normalizar el código a mayúsculas"""
        if self.codigo:
            self.codigo = self.codigo.upper().strip()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'rubros'
        verbose_name = "Rubro"
        verbose_name_plural = "Rubros"
        unique_together = ('empresa', 'codigo')
        app_label = 'tributario_app'


class RubroMoratorioConfig(models.Model):
    """
    Configuración adicional para rubros que representan recargos e intereses moratorios.

    - Permite vincular rubro moratorio -> rubro padre (el rubro base que genera mora).
    - Permite parametrizar tasa de recargo e interés (mensuales) por rubro.
    - No altera la tabla legacy `rubros` (evita romper integridad / compatibilidad).
    """

    MODULO_CHOICES = [
        ('BI', 'Bienes Inmuebles'),
        ('ICS', 'Negocios (ICS)'),
        ('AMBOS', 'Ambos'),
    ]

    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name="Empresa")

    # Rubro que se cobrará como mora (recargo/interés)
    rubro_codigo = models.CharField(max_length=6, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name="Rubro Moratorio")

    # Rubro base que genera la mora
    rubro_padre_codigo = models.CharField(max_length=6, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name="Rubro Padre")

    # Tasas mensuales en porcentaje (ej: 2.50 = 2.5%)
    tasa_recargo_mensual = models.DecimalField(max_digits=7, decimal_places=4, default=Decimal('0.0000'), verbose_name="Tasa Recargo Mensual (%)")
    tasa_interes_mensual = models.DecimalField(max_digits=7, decimal_places=4, default=Decimal('0.0000'), verbose_name="Tasa Interés Mensual (%)")

    aplica_modulo = models.CharField(max_length=5, choices=MODULO_CHOICES, default='AMBOS', verbose_name="Aplica a")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    usuario_crea = models.CharField(max_length=50, default='', blank=True, db_collation='latin1_swedish_ci', verbose_name="Usuario crea")
    fecha_crea = models.DateTimeField(auto_now_add=True)
    usuario_modifica = models.CharField(max_length=50, default='', blank=True, db_collation='latin1_swedish_ci', verbose_name="Usuario modifica")
    fecha_modifica = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rubro_moratorio_config'
        app_label = 'tributario_app'
        verbose_name = "Config Rubro Moratorio"
        verbose_name_plural = "Config Rubros Moratorios"
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'rubro_codigo'], name='uniq_rubro_moratorio_por_empresa'),
        ]
        indexes = [
            models.Index(fields=['empresa', 'rubro_padre_codigo'], name='idx_rubromora_emp_padre'),
            models.Index(fields=['empresa', 'rubro_codigo'], name='idx_rubromora_emp_rubro'),
        ]

    def __str__(self):
        return f"[{self.empresa}] {self.rubro_codigo} -> {self.rubro_padre_codigo}"


class PlanArbitrio(models.Model):
    """
    Modelo para la tabla planarbitio.
    Estructura alineada exactamente con la tabla real de la base de datos.
    
    CREATE TABLE `planarbitio` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `empresa` CHAR(4) COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
      `rubro` CHAR(6) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
      `cod_tarifa` CHAR(4) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
      `tipocat` CHAR(1) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
      `ano` DECIMAL(4,0) NOT NULL,
      `codigo` CHAR(20) COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
      `descripcion` CHAR(200) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
      `minimo` DECIMAL(12,2) DEFAULT 0.00,
      `maximo` DECIMAL(12,2) DEFAULT 0.00,
      `valor` DECIMAL(12,2) DEFAULT 0.00,
      PRIMARY KEY USING BTREE (`id`),
      UNIQUE KEY `planarbitio_idx1` USING BTREE (`empresa`, `rubro`, `cod_tarifa`, `tipocat`, `ano`, `codigo`),
      KEY `planarbitio_idx2` USING BTREE (`empresa`),
      KEY `planarbitio_idx3` USING BTREE (`rubro`),
      KEY `planarbitio_idx4` USING BTREE (`cod_tarifa`),
      KEY `planarbitio_idx5` USING BTREE (`ano`),
      KEY `planarbitio_idx6` USING BTREE (`codigo`),
      KEY `planarbitio_idx7` USING BTREE (`tipocat`)
    ) ENGINE=MyISAM
    AUTO_INCREMENT=249 ROW_FORMAT=FIXED CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci';
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    empresa = models.CharField(max_length=4, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Empresa')
    rubro = models.CharField(max_length=6, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Rubro')
    cod_tarifa = models.CharField(max_length=4, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', verbose_name='Código de Tarifa')
    tipocat = models.CharField(max_length=1, default='', blank=True, null=False, db_collation='utf8mb4_0900_ai_ci', verbose_name='Tipo de Categoría')
    ano = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Año')
    codigo = models.CharField(max_length=20, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Código')
    descripcion = models.CharField(max_length=200, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Descripción')
    minimo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor Mínimo')
    maximo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor Máximo')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return f"Plan {self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'planarbitio'
        verbose_name = 'Plan de Arbitrio'
        verbose_name_plural = 'Planes de Arbitrio'
        ordering = ['-ano', 'codigo']
        unique_together = ('empresa', 'rubro', 'cod_tarifa', 'tipocat', 'ano', 'codigo')
        indexes = [
            models.Index(fields=['empresa'], name='planarbitio_idx2'),
            models.Index(fields=['rubro'], name='planarbitio_idx3'),
            models.Index(fields=['cod_tarifa'], name='planarbitio_idx4'),
            models.Index(fields=['ano'], name='planarbitio_idx5'),
            models.Index(fields=['codigo'], name='planarbitio_idx6'),
            models.Index(fields=['tipocat'], name='planarbitio_idx7'),
        ]
        app_label = 'tributario_app'


class Tarifas(models.Model):
    """
    Modelo para la tabla tarifas.
    Estructura alineada exactamente con la tabla real de la base de datos.
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    empresa = models.CharField(max_length=4, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Empresa')
    rubro = models.CharField(max_length=6, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Rubro')
    cod_tarifa = models.CharField(max_length=20, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', verbose_name='Código de Tarifa')
    ano = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Año')
    descripcion = models.CharField(max_length=200, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Descripción')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, verbose_name='Valor')
    frecuencia = models.CharField(max_length=1, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', verbose_name='Frecuencia')
    tipo = models.CharField(max_length=1, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', verbose_name='Tipo')
    tipomodulo = models.CharField(max_length=1, blank=True, null=True, db_collation='utf8mb4_0900_ai_ci', default='', verbose_name='Tipo Módulo')

    def __str__(self):
        return f"{self.cod_tarifa} - {self.descripcion}"

    class Meta:
        db_table = 'tarifas'
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'
        ordering = ['-ano', 'cod_tarifa']
        unique_together = ('empresa', 'ano', 'cod_tarifa')
        app_label = 'tributario_app'




class TarifasImptoics(models.Model):
    """
    Modelo para la tabla tarifasimptoics - Tarifas de impuestos sobre comercio y servicios
    Incluye tarifas escalonadas por categoría (1=general, 2=productos controlados)
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    categoria = models.CharField(max_length=1, blank=True, null=True, default='', verbose_name="Categoría", db_collation='utf8mb4_0900_ai_ci')
    descripcion = models.CharField(max_length=200, blank=True, null=True, default='', verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci')
    codigo = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True, default=0, verbose_name="Código")
    rango1 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Rango 1")
    rango2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Rango 2")
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor")
    
    class Meta:
        db_table = 'tarifasimptoics'
        verbose_name = "Tarifa Imptoics"
        verbose_name_plural = "Tarifas Imptoics"
        app_label = 'tributario_app'
        ordering = ['categoria', 'rango1']
    
    def __str__(self):
        return f"Tarifa Cat.{self.categoria} - {self.descripcion}"


class DeclaracionVolumen(models.Model):
    """
    Modelo para la tabla declara - Declaraciones de volumen de ventas
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    nodecla = models.CharField(max_length=20, default='', verbose_name="Número de Declaración", db_collation='latin1_swedish_ci')
    empresa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    idneg = models.IntegerField(default=0, verbose_name="ID Negocio")
    rtm = models.CharField(max_length=20, default='', verbose_name="RTM", db_collation='latin1_swedish_ci')
    expe = models.CharField(max_length=10, default='', verbose_name="Expediente", db_collation='latin1_swedish_ci')
    ano = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Año")
    tipo = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name="Tipo")
    mes = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name="Mes")
    ventai = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, verbose_name="Ventas Rubro Producción")
    ventac = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, verbose_name="Ventas Mercadería")
    ventas = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, verbose_name="Ventas por Servicios")
    valorexcento = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, verbose_name="Valor Exento")
    controlado = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, verbose_name="Productos Controlados")
    # Campo REAL en MySQL `declara.valor_base` (obligatorio en algunos esquemas).
    # Se guarda explícitamente para evitar error 1364 (sin default).
    valor_base = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, verbose_name="Valor Base", db_column='valor_base')
    unidad = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="Unidad")
    factor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Factor")
    multadecla = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Multa Declaración")
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Impuesto")
    ajuste = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Ajuste")
    fechssys = models.DateTimeField(blank=True, null=True, verbose_name="Fecha Sistema")
    usuario = models.CharField(max_length=50, default='', verbose_name="Usuario", db_collation='latin1_swedish_ci')
    
    class Meta:
        db_table = 'declara'
        verbose_name = "Declaración de Volumen"
        verbose_name_plural = "Declaraciones de Volumen"
        app_label = 'tributario_app'
        unique_together = (('empresa', 'rtm', 'expe', 'ano'),)
        indexes = [
            models.Index(fields=['rtm'], name='declara_idx1'),
            models.Index(fields=['expe'], name='declara_idx2'),
            models.Index(fields=['ano'], name='declara_idx3'),
            models.Index(fields=['idneg'], name='declara_idx5'),
        ]
    
    @property
    def valor_base_calculado(self):
        """Propiedad calculada (no persistida) para el valor base"""
        return (
            (self.ventai or 0) +
            (self.ventac or 0) +
            (self.ventas or 0) +
            (self.valorexcento or 0) +
            (self.controlado or 0)
        )
    
    def __str__(self):
        return f"Declaración {self.nodecla} - {self.rtm}/{self.expe} - Año {self.ano}"


class AnoEmpreNu(models.Model):
    """
    Modelo para la tabla anoemprenu - Control de números de declaraciones, permisos y planes por empresa y año
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=6, blank=True, null=True, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    ano = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True, verbose_name="Año")
    nudecla = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="Número de Declaración")
    nopermiso = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name="Número de Permiso de Operación")
    noplanes = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Número de Planes")
    
    def __str__(self):
        return f"Empresa {self.empresa} - Año {self.ano}"
    
    class Meta:
        db_table = 'anoemprenu'
        verbose_name = "Año Empresa Numeración"
        verbose_name_plural = "Años Empresa Numeración"
        app_label = 'tributario_app'
        ordering = ['-ano', 'empresa']


class TasasDecla(models.Model):
    """
    Modelo para la tabla tasasdecla - Tasas vinculadas a declaraciones
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    idneg = models.IntegerField(default=0, verbose_name="ID Negocio")
    rtm = models.CharField(max_length=20, default='', verbose_name="RTM", db_collation='latin1_swedish_ci')
    expe = models.CharField(max_length=10, default='', verbose_name="Expediente", db_collation='latin1_swedish_ci')
    nodecla = models.CharField(max_length=20, default='', verbose_name="Número de Declaración", db_collation='latin1_swedish_ci')
    ano = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Año")
    rubro = models.CharField(max_length=6, default='', verbose_name="Rubro", db_collation='latin1_swedish_ci')
    cod_tarifa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Código de Tarifa", db_collation='latin1_swedish_ci')
    frecuencia = models.CharField(max_length=1, default='', verbose_name="Frecuencia", db_collation='latin1_swedish_ci')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor")
    cuenta = models.CharField(max_length=20, default='', verbose_name="Cuenta", db_collation='latin1_swedish_ci')
    cuentarez = models.CharField(max_length=20, default='', verbose_name="Cuenta Rezago", db_collation='latin1_swedish_ci')
    tipota = models.CharField(max_length=1, default='', verbose_name="Tipo Tasa", db_collation='latin1_swedish_ci', db_column='tipota')
    
    def __str__(self):
        return f"Tasa {self.rtm}/{self.expe} - Rubro {self.rubro}"
    
    class Meta:
        db_table = 'tasasdecla'
        verbose_name = "Tasa de Declaración"
        verbose_name_plural = "Tasas de Declaraciones"
        app_label = 'tributario_app'
        unique_together = (('empresa', 'rtm', 'expe', 'ano', 'rubro', 'nodecla'),)
        indexes = [
            models.Index(fields=['rtm'], name='tasasdecla_idx1'),
            models.Index(fields=['expe'], name='tasasdecla_idx2'),
            models.Index(fields=['cod_tarifa'], name='tasasdecla_idx3'),
            models.Index(fields=['idneg'], name='tasasdecla_idx5'),
        ]




class TarifasICS(models.Model):
    """
    Modelo para la tabla tarifasics.
    Estructura alineada exactamente con la tabla real de la base de datos.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    idneg = models.IntegerField(verbose_name="ID Negocio", default=0)
    rtm = models.CharField(max_length=20, verbose_name="RTM", db_collation='latin1_swedish_ci', default='')
    expe = models.CharField(max_length=10, blank=True, null=True, verbose_name="Expediente", db_collation='latin1_swedish_ci', default='')
    rubro = models.CharField(max_length=6, blank=True, null=True, verbose_name="Rubro", db_collation='latin1_swedish_ci', default='')
    cod_tarifa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Código de Tarifa", db_collation='latin1_swedish_ci', default='')
    valor = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Valor", 
        default=0.00
    )
    cuenta = models.CharField(max_length=20, blank=True, default='', verbose_name="Cuenta", db_collation='latin1_swedish_ci')
    cuentarez = models.CharField(max_length=20, blank=True, default='', verbose_name="Cuenta Rezago", db_collation='latin1_swedish_ci')

    class Meta:
        db_table = 'tarifasics'
        verbose_name = "Tarifa ICS"
        verbose_name_plural = "Tarifas ICS"
        app_label = 'tributario_app'
        indexes = [
            models.Index(fields=['rtm'], name='tarifasics_idx1'),
            models.Index(fields=['expe'], name='tarifasics_idx2'),
            models.Index(fields=['cod_tarifa'], name='tarifasics_idx3'),
            models.Index(fields=['idneg'], name='tarifasics_idx5'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'rtm', 'expe', 'rubro'],
                name='tarifasics_idx4'
            )
        ]

    def __str__(self):
        return f"Tarifa ICS {self.cod_tarifa} - {self.rtm}/{self.expe}"


class Anos(models.Model):
    """
    Modelo para la tabla anos.
    Almacena los años disponibles en el sistema.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    ano = models.DecimalField(max_digits=4, decimal_places=0, unique=True, verbose_name="Año")
    
    class Meta:
        db_table = 'anos'
        verbose_name = "Año"
        verbose_name_plural = "Años"
        ordering = ['-ano']
        app_label = 'tributario_app'
        managed = False

    def __str__(self):
        return str(int(self.ano))


class TransaccionesIcs(models.Model):
    """
    Historial transaccional ICS para cálculo de estado de cuenta y mora acumulativa
    Estructura alineada exactamente con la tabla transaccionesics de la base de datos.
    
    CREATE TABLE `transaccionesics` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `idneg` INTEGER NOT NULL DEFAULT 0,
      `nodeclara` CHAR(20) COLLATE latin1_swedish_ci DEFAULT '',
      `empresa` CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL,
      `rtm` CHAR(16) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
      `expe` CHAR(12) COLLATE latin1_swedish_ci DEFAULT '',
      `ano` DECIMAL(4,0) DEFAULT 0,
      `mes` CHAR(2) COLLATE latin1_swedish_ci DEFAULT '',
      `operacion` CHAR(1) COLLATE latin1_swedish_ci DEFAULT '',
      `rubro` CHAR(6) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
      `fecha` DATE DEFAULT NULL,
      `monto` DECIMAL(12,2) DEFAULT 0.00,
      `tasa` DECIMAL(7,2) DEFAULT 0.00,
      `usuario` CHAR(50) COLLATE latin1_swedish_ci DEFAULT '',
      `fechasys` DATETIME(6) DEFAULT NULL,
      PRIMARY KEY USING BTREE (`id`),
      UNIQUE KEY `transaccionesics_idx7` USING BTREE (`empresa`, `rtm`, `expe`, `ano`, `mes`, `rubro`),
      KEY `transaccionesics_idx1` USING BTREE (`rtm`),
      KEY `transaccionesics_idx2` USING BTREE (`expe`),
      KEY `transaccionesics_idx3` USING BTREE (`rubro`),
      KEY `transaccionesics_idx4` USING BTREE (`fecha`),
      KEY `transaccionesics_idx5` USING BTREE (`idneg`),
      KEY `transaccionesics_idx6` USING BTREE (`empresa`)
    ) ENGINE=MyISAM
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    idneg = models.IntegerField(default=0, verbose_name="ID Negocio")
    nodeclara = models.CharField(max_length=20, blank=True, default='', db_collation='latin1_swedish_ci', verbose_name="No. Declaración")
    empresa = models.CharField(max_length=4, blank=True, null=True, default=None, db_collation='latin1_swedish_ci', verbose_name="Empresa")
    rtm = models.CharField(max_length=16, blank=False, default='', db_collation='latin1_swedish_ci', verbose_name="RTM")
    expe = models.CharField(max_length=12, blank=True, default='', db_collation='latin1_swedish_ci', verbose_name="Expediente")
    ano = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name="Año")
    mes = models.CharField(max_length=2, blank=True, default='', db_collation='latin1_swedish_ci', verbose_name="Mes")
    operacion = models.CharField(max_length=1, blank=True, default='', db_collation='latin1_swedish_ci', verbose_name="Operación")
    rubro = models.CharField(max_length=6, blank=False, default='', db_collation='latin1_swedish_ci', verbose_name="Rubro")
    fecha = models.DateField(blank=True, null=True, verbose_name="Fecha")
    vencimiento = models.DateField(blank=True, null=True, verbose_name="Vencimiento")
    monto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Monto")
    tasa = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name="Tasa")
    usuario = models.CharField(max_length=50, blank=True, default='', db_collation='latin1_swedish_ci', verbose_name="Usuario")
    fechasys = models.DateTimeField(blank=True, null=True, verbose_name="Fecha Sistema")

    class Meta:
        db_table = 'transaccionesics'
        verbose_name = "Transacción ICS"
        verbose_name_plural = "Transacciones ICS"
        app_label = 'tributario_app'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'rtm', 'expe', 'ano', 'mes', 'rubro'],
                name='transaccionesics_idx7'
            ),
        ]
        indexes = [
            models.Index(fields=['rtm'], name='transaccionesics_idx1'),
            models.Index(fields=['expe'], name='transaccionesics_idx2'),
            models.Index(fields=['rubro'], name='transaccionesics_idx3'),
            models.Index(fields=['fecha'], name='transaccionesics_idx4'),
            models.Index(fields=['idneg'], name='transaccionesics_idx5'),
            models.Index(fields=['empresa'], name='transaccionesics_idx6'),
        ]

    def __str__(self):
        return f"{self.rtm}/{self.expe} {int(self.ano) if self.ano is not None else ''}-{self.mes}"
    
    def obtener_rango_meses(self):
        """
        Obtiene el rango de meses que cubre esta transacción de pago.
        Retorna un diccionario con información del rango si está disponible en nodeclara.
        
        Formato esperado en nodeclara: "ANO-MES|ANO-MES" (ej: "2024-01|2024-03")
        
        Returns:
            dict: {
                'ano_desde': int, 'mes_desde': int,
                'ano_hasta': int, 'mes_hasta': int,
                'rango_str': str
            } o None si no hay rango disponible
        """
        if not self.nodeclara or self.operacion != 'F':
            return None
        
        try:
            # Formato: "2024-01|2024-03"
            if '|' in self.nodeclara:
                partes = self.nodeclara.split('|')
                if len(partes) == 2:
                    desde_parts = partes[0].split('-')
                    hasta_parts = partes[1].split('-')
                    
                    if len(desde_parts) == 2 and len(hasta_parts) == 2:
                        ano_desde = int(desde_parts[0])
                        mes_desde = int(desde_parts[1])
                        ano_hasta = int(hasta_parts[0])
                        mes_hasta = int(hasta_parts[1])
                        
                        return {
                            'ano_desde': ano_desde,
                            'mes_desde': mes_desde,
                            'ano_hasta': ano_hasta,
                            'mes_hasta': mes_hasta,
                            'rango_str': self.nodeclara
                        }
        except (ValueError, IndexError):
            pass
        
        return None


class TipoCategoria(models.Model):
    """
    Modelo para la tabla tipocategoria.
    Estructura alineada exactamente con la tabla real de la base de datos.
    
    CREATE TABLE `tipocategoria` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `codigo` CHAR(1) COLLATE latin1_swedish_ci NOT NULL,
      `descripcion` CHAR(50) COLLATE latin1_swedish_ci NOT NULL,
      PRIMARY KEY USING BTREE (`id`),
      UNIQUE KEY `codigo_new` USING BTREE (`codigo`)
    ) ENGINE=MyISAM
    AUTO_INCREMENT=10 ROW_FORMAT=FIXED CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci';
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    codigo = models.CharField(max_length=1, unique=True, verbose_name="Código", db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, verbose_name="Descripción", db_collation='latin1_swedish_ci')
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
    class Meta:
        db_table = 'tipocategoria'
        verbose_name = "Tipo de Categoría"
        verbose_name_plural = "Tipos de Categoría"
        app_label = 'tributario_app'
        constraints = [
            models.UniqueConstraint(
                fields=['codigo'],
                name='codigo_new'
            ),
        ]
        ordering = ['codigo']

class TransaccionesBienesInmuebles(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocata1 = models.CharField(max_length=20, default='', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    rubro = models.CharField(max_length=6, verbose_name='Rubro', db_collation='latin1_swedish_ci')
    ano = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Año')
    mes = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Mes')
    operacion = models.CharField(max_length=1, default='F', verbose_name='Operación', db_collation='latin1_swedish_ci')
    monto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto')
    fecha = models.DateField(null=True, blank=True, verbose_name='Fecha')
    vencimiento = models.DateField(null=True, blank=True, verbose_name='Vencimiento')
    usuario = models.CharField(max_length=50, null=True, blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Sistema')
    estado = models.CharField(max_length=1, default='A', verbose_name='Estado', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'tributario'
        db_table = 'transaccionesbienesinmuebles'
        verbose_name = 'Transacción Bienes Inmuebles'
        verbose_name_plural = 'Transacciones Bienes Inmuebles'
        ordering = ['-ano', '-mes', 'fecha']
        indexes = [
            models.Index(fields=['empresa', 'cocata1'], name='idx_transbienes_emp_cocata'),
            models.Index(fields=['empresa', 'cocata1', 'ano', 'mes', 'rubro'], name='idx_transbienes_unique'),
        ]

    def __str__(self):
        return f"{self.cocata1} - {self.rubro} - {self.ano}/{self.mes} - {self.operacion}: {self.monto}"


# ══════════════════════════════════════════════════════════════════════════════
# PARAMETROS TRIBUTARIOS — Tabla global de configuración de amnistías,
# descuentos y recargos. Aplicable a todos los municipios (empresa='GLOB')
# o puede tener registro específico por empresa para sobrescribir el global.
# ══════════════════════════════════════════════════════════════════════════════
class ParametrosTributarios(models.Model):
    """
    Parámetros globales/por-municipio del módulo tributario.
    Maneja: Amnistía tributaria, descuentos 3ra/4ta edad,
    descuento pago anual anticipado y tasas de recargo moratorio.

    tipo_parametro:
        AM = Amnistía tributaria
        TE = Descuento Tercera Edad
        CE = Descuento Cuarta Edad
        PA = Descuento Pago Anual Anticipado
        RM = Tasa de Recargo Moratorio

    Campo operacion en transacciones generadas:
        N = Condonación de recargo (amnistía)
        D = Descuento sobre saldo (amnistía/descuento)
        E = Descuento 3ra Edad
        Q = Descuento 4ta Edad
        C = Descuento pago anual
        A = Cargo recargo moratorio
    """

    TIPO_CHOICES = [
        ('AM', 'Amnistía Tributaria'),
        ('TE', 'Descuento Tercera Edad'),
        ('CE', 'Descuento Cuarta Edad'),
        ('PA', 'Descuento Pago Anual Anticipado'),
        ('RM', 'Tasa de Recargo Moratorio'),
    ]

    id = models.AutoField(primary_key=True)
    empresa = models.CharField(
        max_length=4, default='GLOB',
        verbose_name="Empresa (GLOB=Global)",
        db_collation='latin1_swedish_ci',
        help_text="Use 'GLOB' para aplicar a todos los municipios. "
                  "Un código de empresa específico sobrescribe el global."
    )
    tipo_parametro = models.CharField(
        max_length=2, choices=TIPO_CHOICES,
        verbose_name="Tipo de Parámetro"
    )
    ano_vigencia = models.IntegerField(
        verbose_name="Año de Vigencia",
        help_text="Año fiscal al que aplica este parámetro"
    )
    descripcion = models.CharField(
        max_length=200, default='',
        verbose_name="Descripción",
        db_collation='latin1_swedish_ci'
    )
    numero_decreto = models.CharField(
        max_length=50, blank=True, default='',
        verbose_name="Número de Decreto",
        db_collation='latin1_swedish_ci',
        help_text="Ej: Decreto No. 123-2024 — base legal del beneficio"
    )

    # ── Fechas de vigencia del decreto ────────────────────────────────────────
    fecha_inicio = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Inicio de Vigencia",
        help_text="Inicio del periodo durante el cual el beneficio está activo"
    )
    fecha_fin = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Fin de Vigencia",
        help_text="Fin del periodo de vigencia del beneficio. Nulo = sin límite de vigencia"
    )
    fecha_corte = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Corte de Saldos",
        help_text="Los cargos vencidos HASTA esta fecha aplican el beneficio (corte de deuda)"
    )

    # ── Qué condona / descuenta ───────────────────────────────────────────────
    aplica_recargos = models.BooleanField(
        default=False,
        verbose_name="Aplica a Recargos (rubros R*)",
        help_text="Si True, condona/descuenta rubros cuyo código inicia con R"
    )
    aplica_intereses = models.BooleanField(
        default=False,
        verbose_name="Aplica a Intereses Moratorios"
    )
    aplica_saldo_impuesto = models.BooleanField(
        default=False,
        verbose_name="Aplica descuento sobre saldo de impuesto/tasa"
    )

    # ── Porcentajes (0-100) ───────────────────────────────────────────────────
    porcentaje_condonacion = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('100.00'),
        verbose_name="% Condonación de Recargos/Intereses",
        help_text="100 = condonación total; menores = parcial"
    )
    porcentaje_descuento_saldo = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'),
        verbose_name="% Descuento sobre Saldo de Impuesto"
    )

    # ── Pago anual anticipado ─────────────────────────────────────────────────
    meses_anticipacion = models.IntegerField(
        default=4,
        verbose_name="Meses de Anticipación Requeridos",
        help_text="Mínimo de meses de anticipación para descuento de pago anual"
    )
    porcentaje_descuento_anual = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'),
        verbose_name="% Descuento Pago Anual"
    )

    # ── Recargo moratorio ─────────────────────────────────────────────────────
    tasa_recargo_mensual = models.DecimalField(
        max_digits=7, decimal_places=4, default=Decimal('0.0000'),
        verbose_name="Tasa Mensual de Recargo Moratorio (%)",
        help_text="Ej: 2.5 = 2.5% mensual sobre saldo vencido"
    )
    recargo_maximo_porcentaje = models.DecimalField(
        max_digits=7, decimal_places=2, default=Decimal('0.00'),
        verbose_name="Recargo Máximo (%)",
        help_text="0 = sin límite"
    )

    # ── Auditoría ─────────────────────────────────────────────────────────────
    activo = models.BooleanField(default=True, verbose_name="Activo")
    usuario_crea = models.CharField(
        max_length=50, default='', blank=True,
        verbose_name="Usuario que crea",
        db_collation='latin1_swedish_ci'
    )
    fecha_crea = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    usuario_modifica = models.CharField(
        max_length=50, blank=True, default='',
        verbose_name="Último usuario que modifica",
        db_collation='latin1_swedish_ci'
    )
    fecha_modifica = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")

    class Meta:
        db_table = 'parametros_tributarios'
        verbose_name = "Parámetro Tributario"
        verbose_name_plural = "Parámetros Tributarios"
        app_label = 'tributario_app'
        ordering = ['-ano_vigencia', 'tipo_parametro', 'empresa']
        indexes = [
            models.Index(
                fields=['empresa', 'tipo_parametro', 'ano_vigencia'],
                name='idx_paramtrib_emp_tipo_ano'
            ),
            models.Index(fields=['activo'], name='idx_paramtrib_activo'),
        ]

    def __str__(self):
        return (f"[{self.empresa}] {self.get_tipo_parametro_display()} "
                f"— Año {self.ano_vigencia}")

    @classmethod
    def obtener_parametro(cls, tipo, empresa, ano, fecha_consulta=None):
        """
        Busca parámetro activo para tipo/empresa/año, verificando que esté
        dentro de su período de vigencia (fecha_inicio <= hoy <= fecha_fin).
        Busca primero el registro específico de empresa; si no, el global (GLOB).
        """
        from datetime import date
        hoy = fecha_consulta or date.today()

        def _filtrar(qs):
            """Filtra por vigencia de fechas: inicio <= hoy <= fin (o fin nulo)"""
            candidatos = qs.filter(
                tipo_parametro=tipo, ano_vigencia=ano, activo=True
            ).order_by('-ano_vigencia')
            for p in candidatos:
                inicio_ok = (p.fecha_inicio is None) or (p.fecha_inicio <= hoy)
                fin_ok    = (p.fecha_fin is None) or (p.fecha_fin >= hoy)
                if inicio_ok and fin_ok:
                    return p
            return None

        # 1. Buscar específico de empresa
        p = _filtrar(cls.objects.filter(empresa=empresa))
        if p:
            return p
        # 2. Buscar global
        return _filtrar(cls.objects.filter(empresa='GLOB'))

    @classmethod
    def amnistia_activa(cls, empresa, ano=None, fecha_consulta=None):
        """
        Devuelve el parámetro de amnistía activo para la empresa/año,
        verificando que hoy esté dentro del periodo de vigencia del decreto.
        """
        from datetime import date
        hoy = fecha_consulta or date.today()
        if ano is None:
            ano = hoy.year
        return cls.obtener_parametro('AM', empresa, ano, fecha_consulta=hoy)

    @classmethod
    def calcular_cuotas_descuento_anual(cls, empresa, fecha_pago):
        """
        Calcula cuántas cuotas del año vigente (año siguiente al pago)
        califican para el descuento de pago anual anticipado.

        Regla: se requieren 'meses_anticipacion' meses de anticipación.
        Ejemplo con 4 meses:
          - Pago en sep (9) → mes inicio = 9+4 = 13 → ninguna califica
            CORRECCIÓN: sep del AÑO ANTERIOR → cuotas año vigente:
            mes_inicio_califica = 1 (todas las 12 cuotas de enero a dic)
          - Pago en oct anterior → mes_inicio_califica = 2 → 11 cuotas (feb-dic)
          - Pago en nov anterior → mes_inicio_califica = 3 → 10 cuotas
          - Pago en dic anterior → mes_inicio_califica = 4 → 9 cuotas

        Retorna: (cuotas_con_descuento, mes_inicio, porcentaje)
        """
        from datetime import date
        param = cls.obtener_parametro('PA', empresa, fecha_pago.year + 1)
        if not param or param.porcentaje_descuento_anual == 0:
            return 0, 0, Decimal('0.00')

        meses_ant = param.meses_anticipacion  # 4 por defecto
        mes_pago = fecha_pago.month

        # El primer mes del año siguiente que SÍ califica es mes_pago + meses_ant
        # (porque entre el mes de pago y ese mes hay >= meses_ant de diferencia)
        # Mes de pago 9 (sep) + 4 = 13 => desborda, pero en el año vigente = mes 1
        # En realidad: se paga en mes M del año anterior, las cuotas del año siguiente
        # desde mes (M + meses_ant - 12) en adelante califican, pero nunca antes de enero.
        mes_inicio = max(1, mes_pago + meses_ant - 12)
        cuotas = 13 - mes_inicio  # cuotas desde mes_inicio hasta diciembre
        if cuotas <= 0:
            return 0, 0, Decimal('0.00')
        return cuotas, mes_inicio, param.porcentaje_descuento_anual

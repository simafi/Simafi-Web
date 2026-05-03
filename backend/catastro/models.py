from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()

class FactoresRiego(models.Model):
    """
    Catálogo de factores de riego (códigos, descripción y valor)
    Tabla: factoresriego
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - codigo: CHAR(3) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
    - descripcion: CHAR(45) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
    - valor: DECIMAL(12,2) NOT NULL DEFAULT 0.00
    - PRIMARY KEY (id)
    - UNIQUE KEY factoresriego_idx1 (empresa, codigo)
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=3, default='0', verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=45, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor')

    class Meta:
        app_label = 'catastro'
        db_table = 'factoresriego'
        verbose_name = 'Factor de Riego'
        verbose_name_plural = 'Factores de Riego'
        ordering = ['empresa', 'codigo']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'codigo'], name='factoresriego_idx1')
        ]
        indexes = [
            models.Index(fields=['empresa'], name='factoresriego_idx2')
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class AreasRurales(models.Model):
    """
    Modelo para la tabla areasrurales que contiene las áreas rurales asociadas a una clave catastral
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocata1 = models.CharField(max_length=20, verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    fac = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor')
    codfac = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor', db_collation='latin1_swedish_ci')
    facarea = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor')
    monto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto')
    usuario = models.CharField(max_length=50, default='', blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro')

    class Meta:
        app_label = 'catastro'
        db_table = 'areasrurales'
        verbose_name = 'Área Rural'
        verbose_name_plural = 'Áreas Rurales'
        # Se eliminó UniqueConstraint para permitir múltiples registros por cocata1
        indexes = [
            models.Index(fields=['cocata1']),
            models.Index(fields=['empresa', 'cocata1']),
        ]

    def __str__(self):
        return f"Área Rural - {self.cocata1} - {self.codfac or 'Sin código'}"

class BDCata1(models.Model):
    """
    Modelo para la tabla bdcata1 que contiene los datos generales del catastro municipal
    """
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('S', 'Suspendido'),
    ]
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocata1 = models.CharField(max_length=20, verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    ficha = models.DecimalField(max_digits=1, decimal_places=0, default=1, verbose_name='Número de Ficha')
    claveant = models.CharField(max_length=15, null=True, blank=True, verbose_name='Clave Anterior', db_collation='latin1_swedish_ci')
    mapa = models.CharField(max_length=7, null=True, blank=True, verbose_name='Mapa', db_collation='latin1_swedish_ci')
    bloque = models.CharField(max_length=3, null=True, blank=True, verbose_name='Bloque', db_collation='latin1_swedish_ci')
    predio = models.CharField(max_length=4, null=True, blank=True, default=' ', verbose_name='Predio', db_collation='latin1_swedish_ci')
    depto = models.CharField(max_length=3, null=True, blank=True, verbose_name='Departamento', db_collation='latin1_swedish_ci')
    municipio = models.CharField(max_length=2, null=True, blank=True, verbose_name='Municipio', db_collation='latin1_swedish_ci')
    barrio = models.CharField(max_length=8, null=True, blank=True, verbose_name='Barrio', db_collation='latin1_swedish_ci')
    caserio = models.CharField(max_length=3, null=True, blank=True, verbose_name='Caserío', db_collation='latin1_swedish_ci')
    sitio = models.CharField(max_length=3, null=True, blank=True, verbose_name='Sitio', db_collation='latin1_swedish_ci')
    nombres = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombres', db_collation='latin1_swedish_ci')
    apellidos = models.CharField(max_length=100, null=True, blank=True, verbose_name='Apellidos', db_collation='latin1_swedish_ci')
    identidad = models.CharField(max_length=20, null=True, blank=True, verbose_name='Número de Identidad', db_collation='latin1_swedish_ci')
    rtn = models.CharField(max_length=20, null=True, blank=True, verbose_name='RTN', db_collation='latin1_swedish_ci')
    ubicacion = models.CharField(max_length=80, null=True, blank=True, verbose_name='Ubicación', db_collation='latin1_swedish_ci')
    nacionalidad = models.CharField(max_length=3, null=True, blank=True, verbose_name='Nacionalidad', db_collation='latin1_swedish_ci')
    uso = models.CharField(max_length=3, default='0', verbose_name='Uso del Predio', db_collation='latin1_swedish_ci')
    subuso = models.CharField(max_length=3, null=True, blank=True, verbose_name='Sub-Uso', db_collation='latin1_swedish_ci')
    constru = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Construcción')
    nofichas = models.DecimalField(max_digits=5, decimal_places=0, default=0, verbose_name='Número de Fichas')
    bvl2tie = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor de la Tierra')
    conedi = models.DecimalField(max_digits=5, decimal_places=0, default=0, verbose_name='Conservación de Edificación')
    mejoras = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Mejoras')
    cedif = models.DecimalField(max_digits=5, decimal_places=0, default=0, verbose_name='Clase de Edificación')
    detalle = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Detalle')
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Impuesto')
    grabable = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto Grabable')
    cultivo = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000, verbose_name='Cultivo')
    declarado = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor Declarado')
    condetalle = models.DecimalField(max_digits=5, decimal_places=0, default=0, verbose_name='Condición de Detalle')
    exencion = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Exención')
    usuario = models.CharField(max_length=50, null=True, blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Registro')
    st = models.CharField(max_length=3, null=True, blank=True, verbose_name='Sector', db_collation='latin1_swedish_ci')
    codhab = models.CharField(max_length=3, null=True, blank=True, verbose_name='Código de Habilitación', db_collation='latin1_swedish_ci')
    codprop = models.CharField(max_length=3, null=True, blank=True, verbose_name='Código de Propiedad', db_collation='latin1_swedish_ci')
    tasaimpositiva = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name='Tasa Impositiva')
    declaimpto = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Declaración de Impuesto')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True, verbose_name='Género', db_collation='latin1_swedish_ci')
    telefono = models.CharField(max_length=40, default='0', verbose_name='Teléfono', db_collation='latin1_swedish_ci')
    tipopropiedad = models.DecimalField(max_digits=12, decimal_places=2, default=1.00, verbose_name='Tipo de Propiedad')
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A', verbose_name='Estado del Registro', db_collation='latin1_swedish_ci')
    clavesure = models.CharField(max_length=18, null=True, blank=True, verbose_name='Clave Segura', db_collation='latin1_swedish_ci')
    cx = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Coordenada X (UTM)')
    cy = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Coordenada Y (UTM)')
    zonificacion = models.CharField(max_length=5, null=True, blank=True, verbose_name='Zonificación', db_collation='latin1_swedish_ci')
    bexenc = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name='Porcentaje Exención')
    vivienda = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Número de Viviendas')
    apartamentos = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Num. Apartamentos')
    cuartos = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Num. Cuartos Adic')
    lote = models.CharField(max_length=10, null=True, blank=True, default='', verbose_name='Lote', db_collation='latin1_swedish_ci')
    bloquecol = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='Bloque-Col', db_collation='latin1_swedish_ci')
    terceraedad = models.CharField(max_length=1, null=True, blank=True, default='', verbose_name='Descuento Tercera Edad', db_collation='latin1_swedish_ci')
    foto = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name='Foto', db_collation='latin1_swedish_ci')
    croquis = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name='Croquis', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'bdcata1'
        verbose_name = 'Registro Catastral'
        verbose_name_plural = 'Registros Catastrales'
        ordering = ['cocata1']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'cocata1'], name='bdcata1_idx1')
        ]
        indexes = [
            models.Index(fields=['barrio'], name='bdcata1_idx2'),
            models.Index(fields=['uso'], name='bdcata1_idx3'),
            models.Index(fields=['subuso'], name='bdcata1_idx4'),
        ]

    def __str__(self):
        return f"{self.cocata1} - {self.apellidos or ''} {self.nombres or ''}"


class BDTerreno(models.Model):
    """
    Modelo para la tabla bdterreno que contiene los datos de avalúo del terreno
    """

    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, db_column='empresa', verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocata1 = models.CharField(max_length=20, db_column='cocata1', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')

    # Sección 1 - Valores Básicos
    bvlbas1 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor Básico 1')
    baream21 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área 2.1')
    tipica1 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Tipología 1')
    bfacmodi = models.DecimalField(max_digits=7, decimal_places=3, default=0.000, verbose_name='Factor de Modificación 1')
    bfrente = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Frente')
    besqui = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Cantidad de Esquinas')
    esquina = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Factor de Esquina')

    # Sección 2 - Valores Adicionales
    bvlbas2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor Básico 2')
    baream22 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área 2.2')
    tipica2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Tipología 2')
    bfacmod2 = models.DecimalField(max_digits=7, decimal_places=3, default=0.000, verbose_name='Factor de Modificación 2')
    bfrente2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Frente 2')

    # Topografía
    btopogra = models.CharField(max_length=3, default='0', verbose_name='Tipo de Topografía', db_collation='latin1_swedish_ci')
    bfactopo = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name='Factor de Topografía')

    # Factores de Ajuste
    fac1 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 1')
    codfac1 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 1', db_collation='latin1_swedish_ci')
    facarea1 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 1')
    monto1 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 1')

    # Repetir para los demás factores (fac2 a fac10)
    fac2 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 2')
    codfac2 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 2', db_collation='latin1_swedish_ci')
    facarea2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 2')
    monto2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 2')
    fac3 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 3')
    codfac3 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 3', db_collation='latin1_swedish_ci')
    facarea3 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 3')
    monto3 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 3')
    fac4 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 4')
    codfac4 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 4', db_collation='latin1_swedish_ci')
    facarea4 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 4')
    monto4 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 4')
    fac5 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 5')
    codfac5 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 5', db_collation='latin1_swedish_ci')
    facarea5 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 5')
    monto5 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 5')
    fac6 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 6')
    codfac6 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 6', db_collation='latin1_swedish_ci')
    facarea6 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 6')
    monto6 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 6')
    fac7 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Factor 7')
    codfac7 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 7', db_collation='latin1_swedish_ci')
    facarea7 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 7')
    monto7 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 7')
    fac8 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 8')
    codfac8 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 8', db_collation='latin1_swedish_ci')
    facarea8 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 8')
    monto8 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 8')
    fac9 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 9')
    codfac9 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 9', db_collation='latin1_swedish_ci')
    facarea9 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 9')
    monto9 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 9')
    fac10 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor 10')
    codfac10 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Factor 10', db_collation='latin1_swedish_ci')
    facarea10 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área Factor 10')
    monto10 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto 10')

    # Factores adicionales (continuación)
    fcarea = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Área')
    fcubic = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Cúbico')
    fcservi = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Servicios')
    fcacceso = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Acceso')
    fcagua = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Agua')
    fcarea2 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Área 2')
    fcservi2 = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Servicios 2')
    fctopo = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Topografía')
    fcconfi = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor Configuración')

    # Auditoría
    usuario = models.CharField(max_length=50, default='', blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro')

    class Meta:
        app_label = 'catastro'
        db_table = 'bdterreno'
        verbose_name = 'Avalúo de Terreno'
        verbose_name_plural = 'Avalúos de Terrenos'
        unique_together = [['cocata1']]

    def __str__(self):
        return f"Avalúo - {self.cocata1}"

    def calcular_valor_terreno(self) -> Decimal:
        """
        Calcula el valor total del terreno en base a los valores básicos,
        áreas y factores de modificación registrados.
        """
        subtotal1 = (self.bvlbas1 or Decimal('0')) * (self.baream21 or Decimal('0')) * (self.bfacmodi or Decimal('0'))
        subtotal2 = (self.bvlbas2 or Decimal('0')) * (self.baream22 or Decimal('0')) * (self.bfacmod2 or Decimal('0'))
        total = subtotal1 + subtotal2
        try:
            return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except InvalidOperation:
            return Decimal('0.00')


class Colindantes(models.Model):
    """
    Modelo para la tabla colindantes que contiene información de los colindantes del predio
    Tabla: colindantes
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - cocata1: CHAR(20) COLLATE latin1_swedish_ci NOT NULL
    - tipo: CHAR(1) COLLATE latin1_swedish_ci NOT NULL
    - colindante: CHAR(200) COLLATE latin1_swedish_ci DEFAULT NULL
    - codcolinda: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - usuario: CHAR(50) COLLATE latin1_swedish_ci DEFAULT ''
    - fechasys: DATETIME DEFAULT NULL
    - PRIMARY KEY (id)
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocata1 = models.CharField(max_length=20, verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    tipo = models.CharField(max_length=1, verbose_name='Tipo', db_collation='latin1_swedish_ci')
    colindante = models.CharField(max_length=200, null=True, blank=True, default=None, verbose_name='Colindante', db_collation='latin1_swedish_ci')
    codcolinda = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Código Colindante', db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha Sistema')

    class Meta:
        app_label = 'catastro'
        db_table = 'colindantes'
        verbose_name = 'Colindante'
        verbose_name_plural = 'Colindantes'
        ordering = ['empresa', 'cocata1', 'tipo']
        indexes = [
            models.Index(fields=['empresa', 'cocata1']),
        ]

    def __str__(self):
        return f"Colindante - {self.cocata1} - {self.tipo}"


class Copropietarios(models.Model):
    """
    Modelo para la tabla copropietarios que contiene información de los copropietarios del predio
    Tabla: copropietarios
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - cocata1: CHAR(20) COLLATE latin1_swedish_ci NOT NULL DEFAULT ''
    - identidad: CHAR(18) COLLATE latin1_swedish_ci DEFAULT ''
    - nombre: CHAR(100) COLLATE latin1_swedish_ci DEFAULT ''
    - porcentaje: DECIMAL(7,2) DEFAULT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY copropietarios_idx1 (empresa, cocata1, identidad)
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocata1 = models.CharField(max_length=20, default='', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    identidad = models.CharField(max_length=18, null=True, blank=True, default='', verbose_name='Identidad (DNI)', db_collation='latin1_swedish_ci')
    nombre = models.CharField(max_length=100, null=True, blank=True, default='', verbose_name='Nombre', db_collation='latin1_swedish_ci')
    porcentaje = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=None, verbose_name='Porcentaje (%)')

    class Meta:
        app_label = 'catastro'
        db_table = 'copropietarios'
        verbose_name = 'Copropietario'
        verbose_name_plural = 'Copropietarios'
        ordering = ['empresa', 'cocata1', 'id']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'cocata1', 'identidad'], name='copropietarios_idx1')
        ]
        indexes = [
            models.Index(fields=['empresa', 'cocata1']),
        ]

    def __str__(self):
        nombre_completo = self.nombre or ''
        if nombre_completo:
            return f"{nombre_completo} - {self.cocata1}"
        return f"Copropietario - {self.cocata1}"


class Colindancias(models.Model):
    """
    Modelo para la tabla colindancias que contiene el catálogo de tipos de colindancias
    Tabla: colindancias
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: CHAR(1) COLLATE latin1_swedish_ci DEFAULT '0'
    - descripcion: CHAR(100) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=1, unique=True, default='0', verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'catastro'
        db_table = 'colindancias'
        verbose_name = 'Tipo de Colindancia'
        verbose_name_plural = 'Tipos de Colindancias'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class DetalleAdicionales(models.Model):
    """
    Modelo para la tabla detalleadicionales que contiene información adicional del predio
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, default='', blank=True, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    clave = models.CharField(max_length=14, default='', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=6, null=True, blank=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    area = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Área')
    porce = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Porcentaje')
    unit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor Unitario')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Total')
    descripcion = models.CharField(max_length=30, null=True, blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')
    edifino = models.DecimalField(max_digits=3, decimal_places=0, default=0, null=True, blank=True, verbose_name='Edif. No.')
    piso = models.DecimalField(max_digits=2, decimal_places=0, default=0, null=True, blank=True, verbose_name='Piso')
    codedi = models.CharField(max_length=4, null=True, blank=True, verbose_name='Código Edific.', db_collation='latin1_swedish_ci')
    fraccion = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Fracción')
    valuedi = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Valor Unit Edif. M2', db_column='valoredi')
    usuario = models.CharField(max_length=50, default='', blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro')

    class Meta:
        app_label = 'catastro'
        db_table = 'detalleadicionales'
        verbose_name = 'Detalle Adicional'
        verbose_name_plural = 'Detalles Adicionales'
        ordering = ['clave', 'id']
        indexes = [
            models.Index(fields=['clave'], name='detalleadicionales_idx1'),
        ]

    def __str__(self):
        return f"{self.clave} - {self.descripcion or 'Sin descripción'}"


class BitacoraCatastro(models.Model):
    """
    Modelo para la tabla bitacoracatastro que registra los cambios en el catastro
    """
    id = models.BigAutoField(primary_key=True)
    clave = models.CharField(max_length=20, verbose_name='Clave Catastral')
    fecha = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Cambio')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuario')
    propietarioantes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Propietario Anterior')
    propietarioactual = models.CharField(max_length=200, null=True, blank=True, verbose_name='Propietario Actual')
    concepto = models.TextField(verbose_name='Concepto del Cambio')
    valorantes = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name='Valor Anterior')
    valoractual = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name='Valor Actual')

    class Meta:
        app_label = 'catastro'
        db_table = 'bitacoracatastro'
        verbose_name = 'Bitácora de Cambios'
        verbose_name_plural = 'Bitácora de Cambios'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.fecha} - {self.clave} - {self.concepto[:50]}..."


class Identificacion(models.Model):
    """
    Modelo para la tabla identificacion que contiene los datos de identificación de personas
    """
    id = models.AutoField(primary_key=True)
    identidad = models.CharField(max_length=18, unique=True, verbose_name='Número de Identidad', db_collation='latin1_swedish_ci')
    nombres = models.CharField(max_length=30, null=True, blank=True, verbose_name='Nombres', db_collation='latin1_swedish_ci')
    apellidos = models.CharField(max_length=30, null=True, blank=True, verbose_name='Apellidos', db_collation='latin1_swedish_ci')
    fechanac = models.DateField(null=True, blank=True, verbose_name='Fecha de Nacimiento')

    class Meta:
        app_label = 'catastro'
        db_table = 'identificacion'
        verbose_name = 'Identificación'
        verbose_name_plural = 'Identificaciones'
        ordering = ['identidad']
        indexes = [
            models.Index(fields=['identidad']),
        ]

    def __str__(self):
        return f"{self.identidad} - {self.nombres or ''} {self.apellidos or ''}".strip()


class TipoSexo(models.Model):
    """
    Modelo para la tabla tiposexo que contiene los tipos de sexo disponibles
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=1, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=30, null=True, blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'tiposexo'
        verbose_name = 'Tipo de Sexo'
        verbose_name_plural = 'Tipos de Sexo'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion or ''}".strip()


class Usos(models.Model):
    """
    Modelo para la tabla usos que contiene los tipos de uso disponibles
    """
    id = models.AutoField(primary_key=True)
    uso = models.CharField(max_length=3, unique=True, verbose_name='Uso', db_column='USO', db_collation='latin1_swedish_ci')
    desuso = models.CharField(max_length=34, verbose_name='Descripción de Uso', db_column='DESUSO', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'usos'
        verbose_name = 'Uso'
        verbose_name_plural = 'Usos'
        ordering = ['uso']
        indexes = [
            models.Index(fields=['uso']),
        ]

    def __str__(self):
        return f"{self.uso} - {self.desuso or ''}".strip()


class Subuso(models.Model):
    """
    Modelo para la tabla subuso que contiene los subusos relacionados con cada uso
    """
    id = models.AutoField(primary_key=True)
    uso = models.CharField(max_length=3, verbose_name='Uso', db_collation='latin1_swedish_ci')
    codsubuso = models.CharField(max_length=5, default=' ', verbose_name='Código Subuso', db_collation='latin1_swedish_ci')
    des_subuso = models.CharField(max_length=34, verbose_name='Descripción Subuso', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'subuso'
        verbose_name = 'Subuso'
        verbose_name_plural = 'Subusos'
        ordering = ['uso', 'codsubuso']
        indexes = [
            models.Index(fields=['uso']),
            models.Index(fields=['uso', 'codsubuso']),
        ]

    def __str__(self):
        return f"{self.codsubuso} - {self.des_subuso or ''}".strip()


class Habitacional(models.Model):
    """
    Modelo para la tabla habitacional que contiene los códigos habitacionales disponibles
    """
    id = models.AutoField(primary_key=True)
    cohabit = models.CharField(max_length=2, default='0', verbose_name='Código Habitacional', db_collation='latin1_swedish_ci')
    bdeshabit = models.CharField(max_length=45, default='', verbose_name='Descripción Habitacional', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'habitacional'
        verbose_name = 'Habitacional'
        verbose_name_plural = 'Habitacionales'
        ordering = ['cohabit']
        indexes = [
            models.Index(fields=['cohabit']),
        ]

    def __str__(self):
        return f"{self.cohabit} - {self.bdeshabit or ''}".strip()


class Propietarios(models.Model):
    """
    Modelo para la tabla propietarios que contiene los códigos de propietarios disponibles
    """
    id = models.AutoField(primary_key=True)
    copropi = models.CharField(max_length=2, unique=True, default='', verbose_name='Código Propietario', db_collation='latin1_swedish_ci')
    bdespro = models.CharField(max_length=50, default='0', verbose_name='Descripción Propietario', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'propietarios'
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'
        ordering = ['copropi']
        indexes = [
            models.Index(fields=['copropi']),
        ]

    def __str__(self):
        return f"{self.copropi} - {self.bdespro or ''}".strip()


class Zonasusos(models.Model):
    """
    Modelo para la tabla zonasusos que contiene las zonas de uso disponibles
    """
    id = models.AutoField(primary_key=True)
    tipozona = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='Tipo de Zona', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'zonasusos'
        verbose_name = 'Zona de Uso'
        verbose_name_plural = 'Zonas de Uso'
        ordering = ['tipozona']
        indexes = [
            models.Index(fields=['tipozona']),
        ]

    def __str__(self):
        return f"{self.tipozona or ''} - {self.descripcion or ''}".strip()


class Nacionalidad(models.Model):
    """
    Modelo para la tabla nacionalidad que contiene las nacionalidades disponibles
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=45, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'nacionalidad'
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion or ''}".strip()


class Caserio(models.Model):
    """
    Modelo para la tabla caserio que contiene los caseríos relacionados con depto, municipio y barrio
    """
    id = models.AutoField(primary_key=True)
    depto = models.CharField(max_length=3, verbose_name='Departamento', db_collation='latin1_spanish_ci')
    codmuni = models.CharField(max_length=3, verbose_name='Código Municipio', db_collation='latin1_swedish_ci')
    codbarrio = models.CharField(max_length=3, default='', verbose_name='Código Barrio', db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=3, default='', verbose_name='Código Caserío', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, null=True, blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'caserio'
        verbose_name = 'Caserío'
        verbose_name_plural = 'Caseríos'
        ordering = ['depto', 'codmuni', 'codbarrio', 'codigo']
        unique_together = [['depto', 'codmuni', 'codbarrio', 'codigo']]
        indexes = [
            models.Index(fields=['depto', 'codmuni', 'codbarrio']),
            models.Index(fields=['depto', 'codmuni', 'codbarrio', 'codigo']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion or ''}".strip()

class Edificacion(models.Model):
    """
    Modelo para la tabla edificacion que contiene las edificaciones asociadas a una clave catastral
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, default='', blank=True, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    clave = models.CharField(max_length=14, default='0', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    edifino = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='No. Edif.')
    piso = models.DecimalField(max_digits=2, decimal_places=0, null=True, blank=True, default=None, verbose_name='Piso')
    area = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Área')
    uso = models.CharField(max_length=1, null=True, blank=True, default=None, verbose_name='Uso', db_collation='latin1_swedish_ci')
    clase = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Clase', db_collation='latin1_swedish_ci')
    calidad = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Cal.', db_collation='latin1_swedish_ci')
    costo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Costo')
    bueno = models.DecimalField(max_digits=3, decimal_places=0, default=0, null=True, blank=True, verbose_name='Bueno')
    totedi = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Total Edificación')
    descripcion = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=50, default='', blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro')

    class Meta:
        app_label = 'catastro'
        db_table = 'edificacion'
        verbose_name = 'Edificación'
        verbose_name_plural = 'Edificaciones'
        ordering = ['clave', 'edifino']
        indexes = [
            models.Index(fields=['clave'], name='edificacion_idx1'),
            models.Index(fields=['clave', 'edifino', 'piso'], name='edificacion_idx2')
        ]

    def __str__(self):
        return f"Edificación {self.edifino} - Clave: {self.clave}"

class Costos(models.Model):
    """
    Modelo para la tabla costos que contiene los costos básicos unitarios por empresa, uso, clase y calidad
    Tabla: costos
    Estructura SQL según CREATE TABLE:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT ''
    - USO: CHAR(2) NOT NULL DEFAULT ''
    - CLASE: CHAR(1) NOT NULL DEFAULT ''
    - CALIDAD: CHAR(3) NOT NULL DEFAULT ''
    - COSTO: DECIMAL(13,2) NOT NULL DEFAULT 0.00
    - rango1: DECIMAL(11,0) DEFAULT 0
    - rango2: DECIMAL(11,0) DEFAULT 0
    - PRIMARY KEY (id)
    - UNIQUE KEY (empresa, uso, clase, calidad)
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    empresa = models.CharField(max_length=4, default='', verbose_name='Empresa', db_collation='latin1_swedish_ci')
    uso = models.CharField(max_length=2, default='', verbose_name='Uso', db_collation='latin1_swedish_ci')
    clase = models.CharField(max_length=1, default='', verbose_name='Clase', db_collation='latin1_swedish_ci')
    calidad = models.CharField(max_length=3, default='', verbose_name='Calidad', db_collation='latin1_swedish_ci')
    costo = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, verbose_name='Costo')
    rango1 = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name='Rango 1')
    rango2 = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name='Rango 2')

    class Meta:
        app_label = 'catastro'
        db_table = 'costos'
        verbose_name = 'Costo Básico Unitario'
        verbose_name_plural = 'Costos Básicos Unitarios'
        # Clave única compuesta: empresa, uso, clase, calidad
        unique_together = [['empresa', 'uso', 'clase', 'calidad']]
        indexes = [
            models.Index(fields=['empresa', 'uso', 'clase', 'calidad'], name='costos_idx1'),
        ]

    def __str__(self):
        return f"Costo - Empresa: {self.empresa}, Uso: {self.uso}, Clase: {self.clase}, Calidad: {self.calidad}"

class TipoDetalle(models.Model):
    """
    Catálogo de tipos de detalles (códigos, descripción y costo)
    Tabla: tipodetalle
    Estructura SQL:
    - id: INTEGER AUTO_INCREMENT PRIMARY KEY
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - codigo: CHAR(4) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
    - descripcion: CHAR(30) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
    - costo: DECIMAL(12,3) UNSIGNED NOT NULL DEFAULT 0.000
    - UNIQUE KEY (empresa, codigo)
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=4, default='0', verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=30, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    costo = models.DecimalField(max_digits=12, decimal_places=3, default=0.000, verbose_name='Costo')

    class Meta:
        app_label = 'catastro'
        db_table = 'tipodetalle'
        verbose_name = 'Tipo de Detalle'
        verbose_name_plural = 'Tipos de Detalle'
        ordering = ['codigo']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'codigo'], name='tipodetalle_idx1')
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class UsoEdifica(models.Model):
    """
    Catálogo de usos de edificación
    Tabla: usoedifica
    Estructura SQL:
    - id: INTEGER AUTO_INCREMENT PRIMARY KEY
    - codigo: CHAR(3) COLLATE latin1_swedish_ci NOT NULL
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'usoedifica'
        verbose_name = 'Uso de Edificación'
        verbose_name_plural = 'Usos de Edificación'
        ordering = ['codigo']
        constraints = [
            models.UniqueConstraint(fields=['codigo'], name='codigo')
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Barrios(models.Model):
    """
    Modelo para la tabla barrios que contiene los barrios y aldeas del municipio
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, default='', blank=True, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    depto = models.CharField(max_length=2, default='', verbose_name='Departamento', db_collation='latin1_swedish_ci')
    codmuni = models.CharField(max_length=2, default='', verbose_name='Código Municipio', db_collation='latin1_swedish_ci')
    codbarrio = models.CharField(max_length=8, default='', verbose_name='Código Barrio', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=29, null=True, blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')
    tipica = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Tipología')

    class Meta:
        app_label = 'catastro'
        db_table = 'barrios'
        verbose_name = 'Barrio / Aldea'
        verbose_name_plural = 'Barrios / Aldeas'
        ordering = ['empresa', 'depto', 'codmuni', 'codbarrio']
        unique_together = [['empresa', 'depto', 'codmuni', 'codbarrio']]
        indexes = [
            models.Index(fields=['empresa'], name='barrios_idx1'),
        ]

    def __str__(self):
        return f"{self.codbarrio} - {self.descripcion or ''}"

class Topografia(models.Model):
    """
    Modelo para la tabla topografia que contiene los tipos de topografía del predio
    Tabla: topografia
    Estructura SQL según CREATE TABLE:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - cotopo: CHAR(2) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
    - descritopo: VARCHAR(40) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
    - factopo: DECIMAL(5,2) NOT NULL DEFAULT 0.00
    - PRIMARY KEY (id)
    - UNIQUE KEY topografia_idx1 (empresa, cotopo)
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cotopo = models.CharField(max_length=2, default='0', verbose_name='Código Topografía', db_collation='latin1_swedish_ci')
    descritopo = models.CharField(max_length=40, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    factopo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Factor Topografía')

    class Meta:
        app_label = 'catastro'
        db_table = 'topografia'
        verbose_name = 'Topografía del Predio'
        verbose_name_plural = 'Topografías del Predio'
        ordering = ['empresa', 'cotopo']
        unique_together = [['empresa', 'cotopo']]
        indexes = [
            models.Index(fields=['empresa'], name='topografia_idx2')
        ]

    def __str__(self):
        return f"{self.cotopo} - {self.descritopo or ''}"

class ConfiTipologia(models.Model):
    """
    Configuración de tipología
    Tabla: confi_tipologia
    Estructura SQL:
    - id: INTEGER AUTO_INCREMENT PRIMARY KEY
    - uso: CHAR(2) COLLATE latin1_swedish_ci DEFAULT '0'
    - clase: CHAR(1) COLLATE latin1_swedish_ci DEFAULT '0'
    - tipo: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - categoria: CHAR(1) COLLATE latin1_swedish_ci DEFAULT NULL
    - descripcion: CHAR(100) COLLATE latin1_swedish_ci DEFAULT ''
    - peso: DECIMAL(7,0) DEFAULT 0
    """
    id = models.AutoField(primary_key=True)
    uso = models.CharField(max_length=2, default='0', verbose_name='Uso', db_collation='latin1_swedish_ci')
    clase = models.CharField(max_length=1, default='0', verbose_name='Clase', db_collation='latin1_swedish_ci')
    tipo = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Tipo', db_collation='latin1_swedish_ci')
    categoria = models.CharField(max_length=1, null=True, blank=True, default=None, verbose_name='Categoría', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')
    peso = models.DecimalField(max_digits=7, decimal_places=0, default=0, verbose_name='Peso')

    class Meta:
        app_label = 'catastro'
        db_table = 'confi_tipologia'
        verbose_name = 'Configuración de Tipología'
        verbose_name_plural = 'Configuraciones de Tipología'
        ordering = ['uso', 'clase', 'tipo']
        constraints = [
            models.UniqueConstraint(
                fields=['uso', 'clase', 'tipo', 'categoria'],
                name='confi_tipologia_idx1'
            )
        ]

    def __str__(self):
        return f"{self.uso}-{self.clase}-{self.tipo or ''} - {self.descripcion or 'Sin descripción'}"

class Especificaciones(models.Model):
    """
    Especificaciones de edificación para cálculo de calidad
    Tabla: especificaciones
    """
    id = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=14, default='0', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    piso = models.CharField(max_length=1, null=True, blank=True, default=None, verbose_name='Piso', db_collation='latin1_swedish_ci')
    edifino = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name='No. Edif.')
    uso = models.CharField(max_length=1, null=True, blank=True, default=None, verbose_name='Uso', db_collation='latin1_swedish_ci')
    clase = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Clase', db_collation='latin1_swedish_ci')
    
    # Funcionalidad
    codfun = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Función', db_collation='latin1_swedish_ci')
    descrifun = models.CharField(max_length=100, null=True, blank=True, default=None, verbose_name='Descripción Función', db_collation='latin1_swedish_ci')
    pesofun = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Función')
    
    # Piso
    codpiso = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Piso', db_collation='latin1_swedish_ci')
    descripiso = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Piso', db_collation='latin1_swedish_ci')
    pesopiso = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Piso')
    
    # Pared Externa
    codparext = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Pared Ext.', db_collation='latin1_swedish_ci')
    descriparext = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Pared Ext.', db_collation='latin1_swedish_ci')
    pesoparext = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Pared Ext.')
    
    # Techo
    codtecho = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Techo', db_collation='latin1_swedish_ci')
    descritecho = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Techo', db_collation='latin1_swedish_ci')
    pesotecho = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Techo')
    
    # Pared Interna
    codparint = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Pared Int.', db_collation='latin1_swedish_ci')
    descriparint = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Pared Int.', db_collation='latin1_swedish_ci')
    pesoparint = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Pared Int.')
    
    # Cielo
    codcielo = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Cielo', db_collation='latin1_swedish_ci')
    descricielo = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Cielo', db_collation='latin1_swedish_ci')
    pesocielo = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Cielo')
    
    # Carpintería
    codcarpenti = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Carpintería', db_collation='latin1_swedish_ci')
    descricarpenti = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Carpintería', db_collation='latin1_swedish_ci')
    pesocarpini = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Carpintería')
    
    # Eléctrica
    codelectri = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Eléctrica', db_collation='latin1_swedish_ci')
    descrielectri = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Eléctrica', db_collation='latin1_swedish_ci')
    pesoelectri = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Eléctrica')
    
    # Plomería
    codplome = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Plomería', db_collation='latin1_swedish_ci')
    descriplome = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Plomería', db_collation='latin1_swedish_ci')
    pesoplome = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Plomería')
    
    # Otros
    codotros = models.CharField(max_length=2, default='', blank=True, verbose_name='Código Otros', db_collation='latin1_swedish_ci')
    descriotros = models.CharField(max_length=100, default='', blank=True, verbose_name='Descripción Otros', db_collation='latin1_swedish_ci')
    pesotros = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Peso Otros')
    
    usuario = models.CharField(max_length=50, default='', blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro')
    pesos = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name='Pesos Totales')
    calidad = models.CharField(max_length=3, default='', blank=True, verbose_name='Calidad', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'especificaciones'
        verbose_name = 'Especificación'
        verbose_name_plural = 'Especificaciones'
        ordering = ['clave', 'edifino', 'piso']
        indexes = [
            models.Index(fields=['clave'], name='clave'),
            models.Index(fields=['uso'], name='uso'),
            models.Index(fields=['clase'], name='clase'),
            models.Index(fields=['piso'], name='piso'),
            models.Index(fields=['edifino'], name='edifino'),
        ]

    def __str__(self):
        return f"{self.clave} - Edif. {self.edifino} - Piso {self.piso or 'N/A'} - Calidad: {self.calidad or 'N/A'}"

class DetEspecificacion(models.Model):
    """
    Detalle de especificaciones de edificación
    Tabla: detespecificacion
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, default='', blank=True, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    clave = models.CharField(max_length=14, default='0', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    edifino = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='No. Edificación')
    piso = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Piso')
    
    # Piso
    pisoestruc = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Piso Estructura')
    pisoacabado = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Piso Acabado')
    pisocalidad = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Piso Calidad')
    
    # Pared Externa
    paredextestruc = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Ext. Estructura')
    paredextacabado = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Ext. Acabado')
    paredextcalidad = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Ext. Calidad')
    paredextpintura = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Ext. Pintura')
    
    # Techo
    techotipo = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Techo Tipo')
    techoarteson = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Techo Artesón')
    techoacabado = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Techo Acabado')
    techocalidad = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Techo Calidad')
    
    # Pared Interna
    paredintestruc = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Int. Estructura')
    paredintacabado = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Int. Acabado')
    paredintacalidad = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Int. Calidad')
    paredintpintura = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Pared Int. Pintura')
    
    # Cielo
    cieloestruc = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Cielo Estructura')
    cieloacabado = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Cielo Acabado')
    cielocalidad = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Cielo Calidad')
    
    # Eléctrica
    electrialumbrado = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Eléctrica Alumbrado')
    electrisalida = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Eléctrica Salida')
    electricalidad = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Eléctrica Calidad')
    
    # Plomería
    inodorocal = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Inodoro Calidad')
    lavamanocal = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Lavamanos Calidad')
    duchacal = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Ducha Calidad')
    lavatrastocal = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Lavatrapos Calidad')
    lavanderocal = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Lavandero Calidad')
    
    # Puertas
    puerta1 = models.CharField(max_length=50, default='', blank=True, verbose_name='Puerta 1', db_collation='latin1_swedish_ci')
    puerta2 = models.CharField(max_length=50, default='', blank=True, verbose_name='Puerta 2', db_collation='latin1_swedish_ci')
    puerta3 = models.CharField(max_length=50, default='', blank=True, verbose_name='Puerta 3', db_collation='latin1_swedish_ci')
    puerta4 = models.CharField(max_length=50, default='', blank=True, verbose_name='Puerta 4', db_collation='latin1_swedish_ci')
    
    # Ventanas
    ventana1 = models.CharField(max_length=50, default='', blank=True, verbose_name='Ventana 1', db_collation='latin1_swedish_ci')
    ventana2 = models.CharField(max_length=50, default='', blank=True, verbose_name='Ventana 2', db_collation='latin1_swedish_ci')
    ventana3 = models.CharField(max_length=50, default='', blank=True, verbose_name='Ventana 3', db_collation='latin1_swedish_ci')
    ventana4 = models.CharField(max_length=50, default='', blank=True, verbose_name='Ventana 4', db_collation='latin1_swedish_ci')
    
    # Closets
    closet1 = models.CharField(max_length=50, default='', blank=True, verbose_name='Closet 1', db_collation='latin1_swedish_ci')
    closet2 = models.CharField(max_length=50, default='', blank=True, verbose_name='Closet 2', db_collation='latin1_swedish_ci')
    closet3 = models.CharField(max_length=50, default='', blank=True, verbose_name='Closet 3', db_collation='latin1_swedish_ci')
    closet4 = models.CharField(max_length=50, default='', blank=True, verbose_name='Closet 4', db_collation='latin1_swedish_ci')
    
    # Gabinetes
    gabinete1 = models.CharField(max_length=50, default='', blank=True, verbose_name='Gabinete 1', db_collation='latin1_swedish_ci')
    gabinete2 = models.CharField(max_length=50, default='', blank=True, verbose_name='Gabinete 2', db_collation='latin1_swedish_ci')
    gabinete3 = models.CharField(max_length=50, default='', blank=True, verbose_name='Gabinete 3', db_collation='latin1_swedish_ci')
    gabinete4 = models.CharField(max_length=50, default='', blank=True, verbose_name='Gabinete 4', db_collation='latin1_swedish_ci')
    
    # Auditoría
    usuario = models.CharField(max_length=50, default='', blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro')

    class Meta:
        app_label = 'catastro'
        db_table = 'detespecificacion'
        verbose_name = 'Detalle de Especificación'
        verbose_name_plural = 'Detalles de Especificaciones'
        indexes = [
            models.Index(fields=['empresa', 'clave', 'edifino', 'piso'], name='detespecificacion_idx1')
        ]

    def __str__(self):
        return f"{self.clave} - Edif. {self.edifino} - Piso {self.piso}"


# Señales para manejar los triggers de la base de datos
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Count

def actualizar_campos_bdcata1_desde_detalles(empresa, clave):
    """
    Función auxiliar para actualizar los campos detalle y condetalle en bdcata1
    basado en la sumatoria y conteo de detalles adicionales
    """
    try:
        # Buscar el registro en bdcata1
        bien_inmueble = BDCata1.objects.filter(empresa=empresa, cocata1=clave).first()
        
        if bien_inmueble:
            # Calcular la suma del campo total de todos los detalles adicionales
            suma_total = DetalleAdicionales.objects.filter(
                empresa=empresa,
                clave=clave
            ).aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
            
            # Contar cuántos detalles adicionales existen
            cantidad_detalles = DetalleAdicionales.objects.filter(
                empresa=empresa,
                clave=clave
            ).count()
            
            # Actualizar los campos en bdcata1
            bien_inmueble.detalle = suma_total
            bien_inmueble.condetalle = Decimal(str(cantidad_detalles))
            bien_inmueble.save(update_fields=['detalle', 'condetalle'])
            
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Actualizados campos en bdcata1: detalle={suma_total}, condetalle={cantidad_detalles} para cocata1={clave}")
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error al actualizar campos en bdcata1: {str(e)}")

@receiver(post_save, sender=DetalleAdicionales)
def registrar_cambio_detalle_adicional(sender, instance, created, **kwargs):
    """
    Registra en la bitácora los cambios en los detalles adicionales
    y actualiza los campos detalle y condetalle en bdcata1
    """
    try:
        if created:
            concepto = f"Creación de detalle adicional: {instance.descripcion or 'Sin descripción'}"
        else:
            concepto = f"Actualización de detalle adicional: {instance.descripcion or 'Sin descripción'}"
        
        # Intentar obtener el objeto User si está disponible
        usuario_obj = None
        try:
            # Intentar obtener el User desde el atributo _usuario_obj si fue establecido
            usuario_obj = getattr(instance, '_usuario_obj', None)
            
            # Si no está disponible, intentar buscar por nombre de usuario
            if not usuario_obj and instance.usuario:
                try:
                    # Buscar usuario por username (el campo usuario ahora es CharField con el nombre)
                    usuario_obj = User.objects.filter(username=instance.usuario).first()
                except Exception:
                    pass
        except Exception:
            pass
        
        # Intentar crear el registro en la bitácora, pero no fallar si la tabla no existe
        try:
            BitacoraCatastro.objects.create(
                clave=instance.clave,
                usuario=usuario_obj,  # Puede ser None si no se encuentra el User
                concepto=concepto,
                valoractual=instance.total
            )
        except Exception as e:
            # Si la tabla no existe o hay algún error, solo registrar en el log pero no fallar
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"No se pudo registrar en bitácora: {str(e)}")
        
        # Actualizar campos detalle y condetalle en bdcata1
        if instance.empresa and instance.clave:
            actualizar_campos_bdcata1_desde_detalles(instance.empresa, instance.clave)
            
    except Exception as e:
        # Manejar cualquier error en el signal sin interrumpir el guardado
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error en signal de detalle adicional: {str(e)}")

@receiver(post_delete, sender=DetalleAdicionales)
def registrar_eliminacion_detalle_adicional(sender, instance, **kwargs):
    """
    Registra en la bitácora la eliminación de detalles adicionales
    """
    try:
        # Intentar obtener el objeto User si está disponible
        usuario_obj = None
        try:
            # Intentar obtener el User desde el atributo _usuario_obj si fue establecido
            usuario_obj = getattr(instance, '_usuario_obj', None)
            
            # Si no está disponible, intentar buscar por nombre de usuario
            if not usuario_obj and instance.usuario:
                try:
                    # Buscar usuario por username (el campo usuario ahora es CharField con el nombre)
                    usuario_obj = User.objects.filter(username=instance.usuario).first()
                except Exception:
                    pass
        except Exception:
            pass
        
        # Intentar crear el registro en la bitácora, pero no fallar si la tabla no existe
        try:
            BitacoraCatastro.objects.create(
                clave=instance.clave,
                usuario=usuario_obj,  # Puede ser None si no se encuentra el User
                concepto=f"Eliminación de detalle adicional: {instance.descripcion or 'Sin descripción'}",
                valorantes=instance.total
            )
        except Exception as e:
            # Si la tabla no existe o hay algún error, solo registrar en el log pero no fallar
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"No se pudo registrar en bitácora: {str(e)}")
        
        # Actualizar campos detalle y condetalle en bdcata1 al eliminar un detalle
        if instance.empresa and instance.clave:
            actualizar_campos_bdcata1_desde_detalles(instance.empresa, instance.clave)
            
    except Exception as e:
        # Manejar cualquier error en el signal sin interrumpir la eliminación
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error en signal de eliminación de detalle adicional: {str(e)}")

@receiver(post_save, sender=BDTerreno)
def registrar_cambio_terreno(sender, instance, **kwargs):
    """
    Registra en la bitácora los cambios en los terrenos
    """
    # Aquí puedes implementar la lógica para detectar cambios específicos
    # y registrarlos en la bitácora de manera similar a los triggers SQL
    pass

class TipoMaterial(models.Model):
    """
    Modelo para la tabla tipomaterial que contiene los tipos de materiales
    Tabla: tipomaterial
    Estructura SQL según CREATE TABLE:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - No: CHAR(2) COLLATE latin1_swedish_ci NOT NULL DEFAULT ''
    - descripcion: CHAR(45) COLLATE latin1_swedish_ci NOT NULL DEFAULT ''
    - PRIMARY KEY (id)
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    No = models.CharField(max_length=2, default='', verbose_name='Número', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=45, default='', verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'tipomaterial'
        verbose_name = 'Tipo de Material'
        verbose_name_plural = 'Tipos de Material'
        ordering = ['No']

    def __str__(self):
        return f"{self.No} - {self.descripcion or ''}"

class ValorArbol(models.Model):
    """
    Modelo para la tabla valorarbol que contiene las clases y variedades de cultivo
    Tabla: valorarbol
    Estructura SQL según CREATE TABLE:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - codigo: CHAR(6) COLLATE latin1_swedish_ci NOT NULL DEFAULT ''
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL DEFAULT ''
    - valor: DECIMAL(12,2) NOT NULL DEFAULT 0.00
    - PRIMARY KEY (id)
    - UNIQUE KEY valorarbol_idx1 (empresa, codigo)
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=6, default='', verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, default='', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor')

    class Meta:
        app_label = 'catastro'
        db_table = 'valorarbol'
        verbose_name = 'Valor Árbol'
        verbose_name_plural = 'Valores Árbol'
        ordering = ['codigo']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'codigo'], name='valorarbol_idx1')
        ]
        indexes = [
            models.Index(fields=['empresa', 'codigo'], name='valorarbol_idx1')
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion or ''}"

class FactorCultivo(models.Model):
    """
    Modelo para la tabla factorcultivo que contiene los factores de cultivo por rango
    Tabla: factorcultivo
    Estructura SQL según CREATE TABLE:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - codigo: CHAR(6) COLLATE latin1_swedish_ci NOT NULL DEFAULT ''
    - rango1: DECIMAL(4,0) NOT NULL DEFAULT 0
    - rango2: DECIMAL(4,0) NOT NULL DEFAULT 0
    - factor: DECIMAL(6,3) NOT NULL DEFAULT 0.000
    - PRIMARY KEY (id)
    - KEY factorcultivo_idx1 (empresa, codigo, rango1)
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=6, default='', verbose_name='Código', db_collation='latin1_swedish_ci')
    rango1 = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name='Rango 1')
    rango2 = models.DecimalField(max_digits=4, decimal_places=0, default=0, verbose_name='Rango 2')
    factor = models.DecimalField(max_digits=6, decimal_places=3, default=0.000, verbose_name='Factor')

    class Meta:
        app_label = 'catastro'
        db_table = 'factorcultivo'
        verbose_name = 'Factor de Cultivo'
        verbose_name_plural = 'Factores de Cultivo'
        ordering = ['codigo', 'rango1']
        indexes = [
            models.Index(fields=['empresa', 'codigo', 'rango1'], name='factorcultivo_idx1')
        ]

class CultivoPermanente(models.Model):
    """
    Modelo para la tabla cultivopermanente que contiene el avalúo de cultivos permanentes
    Tabla: cultivopermanente
    Estructura SQL según CREATE TABLE:
    CREATE TABLE `cultivopermanente` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `empresa` CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL,
      `clave` CHAR(20) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0',
      `clase` CHAR(6) COLLATE latin1_swedish_ci DEFAULT NULL,
      `arbol` DECIMAL(7,0) DEFAULT 0,
      `estado` CHAR(1) COLLATE latin1_swedish_ci DEFAULT '0',
      `edad` DECIMAL(3,0) DEFAULT 0,
      `factor` DECIMAL(7,2) DEFAULT 0.00,
      `valor` DECIMAL(12,2) DEFAULT 0.00,
      `usuario` CHAR(50) COLLATE latin1_swedish_ci DEFAULT '',
      `fechasys` DATETIME DEFAULT NULL,
      PRIMARY KEY USING BTREE (`id`),
      KEY `cultivopermanente_idx1` USING BTREE (`empresa`),
      KEY `cultivopermanente_idx2` USING BTREE (`clave`)
    ) ENGINE=MyISAM AUTO_INCREMENT=1 ROW_FORMAT=FIXED CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci';
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    clave = models.CharField(max_length=20, default='0', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    clase = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name='Clase', db_collation='latin1_swedish_ci')
    arbol = models.DecimalField(max_digits=7, decimal_places=0, default=0, verbose_name='Árbol')
    estado = models.CharField(max_length=1, default='0', verbose_name='Estado', db_collation='latin1_swedish_ci')
    edad = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Edad')
    factor = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name='Factor')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor')
    usuario = models.CharField(max_length=50, default='', blank=True, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha de Registro')

    class Meta:
        app_label = 'catastro'
        db_table = 'cultivopermanente'
        verbose_name = 'Cultivo Permanente'
        verbose_name_plural = 'Cultivos Permanentes'
        ordering = ['clave', 'clase']
        indexes = [
            models.Index(fields=['empresa'], name='cultivopermanente_idx1'),
            models.Index(fields=['clave'], name='cultivopermanente_idx2')
        ]

    def __str__(self):
        return f"{self.clave} - {self.clase or 'N/A'}"

class Legales(models.Model):
    """
    Modelo para la tabla legales que contiene la información legal del predio
    Tabla: legales
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - colegal: CHAR(20) COLLATE latin1_swedish_ci NOT NULL
    - inscripcion: DATE DEFAULT NULL
    - coregistro: CHAR(3) COLLATE latin1_swedish_ci DEFAULT NULL
    - tomo: CHAR(6) COLLATE latin1_swedish_ci DEFAULT NULL
    - folio: CHAR(6) COLLATE latin1_swedish_ci DEFAULT NULL
    - asiento: CHAR(15) COLLATE latin1_swedish_ci DEFAULT NULL
    - area: DECIMAL(10,2) DEFAULT 0.00
    - naturaleza: DECIMAL(1,0) DEFAULT 0
    - dominio: DECIMAL(1,0) DEFAULT 0
    - numero: CHAR(10) COLLATE latin1_swedish_ci DEFAULT '0'
    - linea: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - foto: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - predio2: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - tipo: DECIMAL(1,0) DEFAULT 0
    - tmed: DECIMAL(1,0) DEFAULT 0
    - unidad: DECIMAL(1,0) DEFAULT 0
    - certificacion: CHAR(10) COLLATE latin1_swedish_ci DEFAULT '0'
    - acta: CHAR(10) COLLATE latin1_swedish_ci DEFAULT '0'
    - tipopro: DECIMAL(1,0) DEFAULT 0
    - usuario: CHAR(50) COLLATE latin1_swedish_ci DEFAULT NULL
    - fechasys: DATETIME DEFAULT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY legales_idx1 (empresa, colegal)
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    colegal = models.CharField(max_length=20, verbose_name='Código Legal', db_collation='latin1_swedish_ci')
    inscripcion = models.DateField(null=True, blank=True, default=None, verbose_name='Inscripción')
    coregistro = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Código Registro', db_collation='latin1_swedish_ci')
    tomo = models.CharField(max_length=6, null=True, blank=True, default=None, verbose_name='Tomo', db_collation='latin1_swedish_ci')
    folio = models.CharField(max_length=6, null=True, blank=True, default=None, verbose_name='Folio', db_collation='latin1_swedish_ci')
    asiento = models.CharField(max_length=15, null=True, blank=True, default=None, verbose_name='Asiento', db_collation='latin1_swedish_ci')
    area = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Área')
    naturaleza = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Naturaleza')
    dominio = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Dominio')
    numero = models.CharField(max_length=10, default='0', verbose_name='Número', db_collation='latin1_swedish_ci')
    linea = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Línea', db_collation='latin1_swedish_ci')
    foto = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Foto', db_collation='latin1_swedish_ci')
    predio2 = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Predio 2', db_collation='latin1_swedish_ci')
    tipo = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Tipo')
    tmed = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Tmed')
    unidad = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Unidad')
    certificacion = models.CharField(max_length=10, default='0', verbose_name='Certificación', db_collation='latin1_swedish_ci')
    acta = models.CharField(max_length=10, default='0', verbose_name='Acta', db_collation='latin1_swedish_ci')
    tipopro = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name='Tipo Propiedad')
    usuario = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha Sistema')

    class Meta:
        app_label = 'catastro'
        db_table = 'legales'
        verbose_name = 'Información Legal'
        verbose_name_plural = 'Informaciones Legales'
        ordering = ['empresa', 'colegal']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'colegal'], name='legales_idx1')
        ]
        indexes = [
            # Índices simples existentes en la base de datos
            models.Index(fields=['naturaleza'], name='legales_idx2'),
            models.Index(fields=['dominio'], name='legales_idx3'),
            models.Index(fields=['tipo'], name='legales_idx4'),
            # Índices compuestos para optimizar agrupaciones con empresa
            models.Index(fields=['empresa', 'naturaleza'], name='legales_idx_naturaleza'),
            models.Index(fields=['empresa', 'dominio'], name='legales_idx_dominio'),
            models.Index(fields=['empresa', 'tipo'], name='legales_idx_tipo'),
        ]

    def __str__(self):
        return f"{self.colegal or 'N/A'}"

class Caracteristicas(models.Model):
    """
    Modelo para la tabla caracteristicas que contiene las características del predio
    Tabla: caracteristicas
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - cocata1: CHAR(20) COLLATE latin1_swedish_ci NOT NULL
    - iglesia: DECIMAL(2,0) DEFAULT 0
    - mercado: DECIMAL(2,0) DEFAULT 0
    - escuela: DECIMAL(2,0) DEFAULT 0
    - embarque: DECIMAL(2,0) DEFAULT 0
    - proparea: DECIMAL(9,2) DEFAULT 0.00
    - propexplota: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - proptopo: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - caudal: CHAR(3) COLLATE latin1_swedish_ci DEFAULT '0'
    - pozo: CHAR(3) COLLATE latin1_swedish_ci DEFAULT NULL
    - comunicacion: CHAR(3) COLLATE latin1_swedish_ci DEFAULT NULL
    - dis1 a dis5: DECIMAL(10,2) DEFAULT 0.00
    - friego1 a friego5: DECIMAL(7,3) DEFAULT 0.000
    - sisirri1 a sisirri5: CHAR(3) COLLATE latin1_swedish_ci DEFAULT NULL
    - areairri1 a areairri5: DECIMAL(12,2) DEFAULT 0.00
    - usot1 a usot4: CHAR(3) o VARCHAR(3) COLLATE latin1_swedish_ci DEFAULT NULL
    - porcet1 a porcet4: DECIMAL(3,0) DEFAULT 0
    - usuario: CHAR(50) COLLATE latin1_swedish_ci DEFAULT ''
    - fechasys: DATETIME DEFAULT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY caracteristicas_idx1 (empresa, cocata1)
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocata1 = models.CharField(max_length=20, verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    iglesia = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Iglesia')
    mercado = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Mercado')
    escuela = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Escuela')
    embarque = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Embarque')
    proparea = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Prop Area')
    propexplota = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Prop Explota', db_collation='latin1_swedish_ci')
    proptopo = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Prop Topo', db_collation='latin1_swedish_ci')
    caudal = models.CharField(max_length=3, default='0', verbose_name='Caudal', db_collation='latin1_swedish_ci')
    pozo = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Pozo', db_collation='latin1_swedish_ci')
    comunicacion = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Comunicación', db_collation='latin1_swedish_ci')
    dis1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Dis 1')
    friego1 = models.DecimalField(max_digits=7, decimal_places=3, default=0.000, verbose_name='F Riego 1')
    sisirri1 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Sis Irri 1', db_collation='latin1_swedish_ci')
    areairri1 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Area Irri 1')
    dis2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Dis 2')
    friego2 = models.DecimalField(max_digits=7, decimal_places=3, default=0.000, verbose_name='F Riego 2')
    sisirri2 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Sis Irri 2', db_collation='latin1_swedish_ci')
    areairri2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Area Irri 2')
    dis3 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Dis 3')
    friego3 = models.DecimalField(max_digits=7, decimal_places=3, default=0.000, verbose_name='F Riego 3')
    sisirri3 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Sis Irri 3', db_collation='latin1_swedish_ci')
    areairri3 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Area Irri 3')
    dis4 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Dis 4')
    friego4 = models.DecimalField(max_digits=7, decimal_places=3, default=0.000, verbose_name='F Riego 4')
    sisirri4 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Sis Irri 4', db_collation='latin1_swedish_ci')
    areairri4 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Area Irri 4')
    dis5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Dis 5')
    friego5 = models.DecimalField(max_digits=7, decimal_places=3, default=0.000, verbose_name='F Riego 5')
    sisirri5 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Sis Irri 5', db_collation='latin1_swedish_ci')
    areairri5 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Area Irri 5')
    usot1 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Uso T1', db_collation='latin1_swedish_ci')
    porcet1 = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Porcet 1')
    usot2 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Uso T2', db_collation='latin1_swedish_ci')
    porcet2 = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Porcet 2')
    usot3 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Uso T3', db_collation='latin1_swedish_ci')
    porcet3 = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Porcet 3')
    usot4 = models.CharField(max_length=3, null=True, blank=True, default=None, verbose_name='Uso T4', db_collation='latin1_swedish_ci')
    porcet4 = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Porcet 4')
    usuario = models.CharField(max_length=50, default='', verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha Sistema')

    class Meta:
        app_label = 'catastro'
        db_table = 'caracteristicas'
        verbose_name = 'Características del Predio'
        verbose_name_plural = 'Características de Predios'
        ordering = ['empresa', 'cocata1']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'cocata1'], name='caracteristicas_idx1')
        ]

    def __str__(self):
        return f"Características - {self.cocata1}"

class TipoDocumento(models.Model):
    """
    Modelo para la tabla tipodocumento que contiene los tipos de documentos legales
    Tabla: tipodocumento
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(200) COLLATE latin1_swedish_ci DEFAULT '0'
    - PRIMARY KEY (id)
    - UNIQUE KEY tipodocumento_idx1 (empresa, codigo)
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Código')
    descripcion = models.CharField(max_length=200, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'catastro'
        db_table = 'tipodocumento'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['empresa', 'codigo']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'codigo'], name='tipodocumento_idx1')
        ]
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Naturaleza(models.Model):
    """
    Modelo para la tabla naturaleza que contiene las naturalezas legales
    Tabla: naturaleza
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(200) COLLATE latin1_swedish_ci DEFAULT '0'
    - PRIMARY KEY (id)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Código')
    descripcion = models.CharField(max_length=200, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'catastro'
        db_table = 'naturaleza'
        verbose_name = 'Naturaleza'
        verbose_name_plural = 'Naturalezas'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Dominio(models.Model):
    """
    Modelo para la tabla dominio que contiene los dominios legales
    Tabla: dominio
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(200) COLLATE latin1_swedish_ci DEFAULT '0'
    - PRIMARY KEY (id)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Código')
    descripcion = models.CharField(max_length=200, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'catastro'
        db_table = 'dominio'
        verbose_name = 'Dominio'
        verbose_name_plural = 'Dominios'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoMedida(models.Model):
    """
    Modelo para la tabla tipomedida que contiene los tipos de medida
    Tabla: tipomedida
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(200) COLLATE latin1_swedish_ci DEFAULT '0'
    - PRIMARY KEY (id)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Código')
    descripcion = models.CharField(max_length=200, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'catastro'
        db_table = 'tipomedida'
        verbose_name = 'Tipo de Medida'
        verbose_name_plural = 'Tipos de Medida'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class UnidadArea(models.Model):
    """
    Modelo para la tabla unidadarea que contiene las unidades de área
    Tabla: unidadarea
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(200) COLLATE latin1_swedish_ci DEFAULT '0'
    - PRIMARY KEY (id)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='Código')
    descripcion = models.CharField(max_length=200, default='0', verbose_name='Descripción', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'catastro'
        db_table = 'unidadarea'
        verbose_name = 'Unidad de Área'
        verbose_name_plural = 'Unidades de Área'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class RegistroPropiedad(models.Model):
    """
    Modelo para la tabla registropropiedad que contiene los registros de propiedad
    Tabla: registropropiedad
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: CHAR(3) COLLATE latin1_swedish_ci NOT NULL DEFAULT '' (PRIMARY KEY)
    - departamento: VARCHAR(29) COLLATE latin1_swedish_ci NOT NULL
    - municipio: VARCHAR(29) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (codigo)
    - UNIQUE KEY REGPRO_K_REGISTRO (id)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, default='', unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    departamento = models.CharField(max_length=29, verbose_name='Departamento', db_collation='latin1_swedish_ci')
    municipio = models.CharField(max_length=29, verbose_name='Municipio', db_collation='latin1_swedish_ci')
    
    class Meta:
        app_label = 'catastro'
        db_table = 'registropropiedad'
        verbose_name = 'Registro de Propiedad'
        verbose_name_plural = 'Registros de Propiedad'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.departamento}, {self.municipio}"

class Explotacion(models.Model):
    """
    Modelo para la tabla explotacion que contiene códigos y descripciones de explotación
    Tabla: explotacion
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: CHAR(3) COLLATE latin1_swedish_ci NOT NULL
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'explotacion'
        verbose_name = 'Explotación'
        verbose_name_plural = 'Explotaciones'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Vias(models.Model):
    """
    Modelo para la tabla vias que contiene códigos y descripciones de vías de comunicación
    Tabla: vias
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: CHAR(3) COLLATE latin1_swedish_ci NOT NULL
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'vias'
        verbose_name = 'Vía'
        verbose_name_plural = 'Vías'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Irrigacion(models.Model):
    """
    Modelo para la tabla irrigacion que contiene códigos y descripciones de sistemas de irrigación
    Tabla: irrigacion
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: CHAR(3) COLLATE latin1_swedish_ci NOT NULL
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'irrigacion'
        verbose_name = 'Sistema de Irrigación'
        verbose_name_plural = 'Sistemas de Irrigación'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class UsoTierra(models.Model):
    """
    Modelo para la tabla usotierra que contiene códigos y descripciones de usos de la tierra
    Tabla: usotierra
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: CHAR(3) COLLATE latin1_swedish_ci NOT NULL
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'usotierra'
        verbose_name = 'Uso de la Tierra'
        verbose_name_plural = 'Usos de la Tierra'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Complemento(models.Model):
    """
    Modelo para la tabla complemento que contiene datos complementarios del predio
    Tabla: complemento
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - empresa: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
    - cocomple: CHAR(20) COLLATE latin1_swedish_ci NOT NULL
    - fechaadqui: DATE DEFAULT NULL
    - monto: DECIMAL(12,2) DEFAULT 0.00
    - clatra: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - maquinaria: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - delineador: CHAR(30) COLLATE latin1_swedish_ci DEFAULT NULL
    - observacion: VARCHAR(5000) COLLATE latin1_swedish_ci DEFAULT NULL
    - fedeli: DATE DEFAULT NULL
    - bs1 a bs8: CHAR(4) COLLATE latin1_swedish_ci DEFAULT '0'
    - ocupante: CHAR(50) COLLATE latin1_swedish_ci DEFAULT NULL
    - renta: DECIMAL(12,2) DEFAULT 0.00
    - observ2: CHAR(70) COLLATE latin1_swedish_ci DEFAULT NULL
    - causa: CHAR(2) COLLATE latin1_swedish_ci DEFAULT NULL
    - Bnocalcu: CHAR(100) COLLATE latin1_swedish_ci DEFAULT ''
    - Bfecal: DATE DEFAULT NULL
    - usuario: CHAR(50) COLLATE latin1_swedish_ci DEFAULT ''
    - fechasys: DATETIME DEFAULT NULL
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    cocomple = models.CharField(max_length=20, verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    fechaadqui = models.DateField(null=True, blank=True, default=None, verbose_name='Fecha Adquisición')
    monto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Monto de la Transacción')
    clatra = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Clase de Transaccion', db_collation='latin1_swedish_ci')
    maquinaria = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Maquinaria', db_collation='latin1_swedish_ci')
    delineador = models.CharField(max_length=30, null=True, blank=True, default=None, verbose_name='Delineador', db_collation='latin1_swedish_ci')
    observacion = models.TextField(max_length=5000, null=True, blank=True, default=None, verbose_name='Observación', db_collation='latin1_swedish_ci')
    fedeli = models.DateField(null=True, blank=True, default=None, verbose_name='Fecha Delimitación')
    bs1 = models.CharField(max_length=4, default='0', verbose_name='BS1', db_collation='latin1_swedish_ci')
    bs2 = models.CharField(max_length=4, default='0', verbose_name='BS2', db_collation='latin1_swedish_ci')
    bs3 = models.CharField(max_length=4, default='0', verbose_name='BS3', db_collation='latin1_swedish_ci')
    bs4 = models.CharField(max_length=4, default='0', verbose_name='BS4', db_collation='latin1_swedish_ci')
    bs5 = models.CharField(max_length=4, default='0', verbose_name='BS5', db_collation='latin1_swedish_ci')
    bs6 = models.CharField(max_length=4, default='0', verbose_name='BS6', db_collation='latin1_swedish_ci')
    bs7 = models.CharField(max_length=4, default='0', verbose_name='BS7', db_collation='latin1_swedish_ci')
    bs8 = models.CharField(max_length=4, default='0', verbose_name='BS8', db_collation='latin1_swedish_ci')
    bs9 = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='BS9', db_collation='latin1_swedish_ci')
    ocupante = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name='Ocupante', db_collation='latin1_swedish_ci')
    renta = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Renta')
    observ2 = models.CharField(max_length=70, null=True, blank=True, default=None, verbose_name='Observación 2', db_collation='latin1_swedish_ci')
    causa = models.CharField(max_length=2, null=True, blank=True, default=None, verbose_name='Causa', db_collation='latin1_swedish_ci')
    Bnocalcu = models.CharField(max_length=100, default='', verbose_name='Calculista', db_collation='latin1_swedish_ci')
    Bfecal = models.DateField(null=True, blank=True, default=None, verbose_name='Fecha Calculo')
    usuario = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha Sistema')

    class Meta:
        app_label = 'catastro'
        db_table = 'complemento'
        verbose_name = 'Datos Complementarios'
        verbose_name_plural = 'Datos Complementarios'
        ordering = ['empresa', 'cocomple']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'cocomple'], name='complemento_idx1')
        ]
    
    def __str__(self):
        return f"{self.cocomple or 'N/A'}"

class Agua(models.Model):
    """
    Modelo para la tabla agua que contiene códigos y descripciones de servicios de agua
    Tabla: agua
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'agua'
        verbose_name = 'Agua'
        verbose_name_plural = 'Servicios de Agua'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Telefono(models.Model):
    """
    Modelo para la tabla telefono que contiene códigos y descripciones de servicios de teléfono
    Tabla: telefono
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'telefono'
        verbose_name = 'Teléfono'
        verbose_name_plural = 'Teléfonos'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Drenaje(models.Model):
    """
    Modelo para la tabla drenaje que contiene códigos y descripciones de servicios de drenaje
    Tabla: drenaje
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'drenaje'
        verbose_name = 'Drenaje'
        verbose_name_plural = 'Drenajes'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Calle(models.Model):
    """
    Modelo para la tabla calle que contiene códigos y descripciones de servicios de calle
    Tabla: calle
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'calle'
        verbose_name = 'Calle'
        verbose_name_plural = 'Calles'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Electricidad(models.Model):
    """
    Modelo para la tabla electricidad que contiene códigos y descripciones de servicios de electricidad
    Tabla: electricidad
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'electricidad'
        verbose_name = 'Electricidad'
        verbose_name_plural = 'Electricidades'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Acera(models.Model):
    """
    Modelo para la tabla acera que contiene códigos y descripciones de servicios de acera
    Tabla: acera
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'acera'
        verbose_name = 'Acera'
        verbose_name_plural = 'Aceras'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Alumbrado(models.Model):
    """
    Modelo para la tabla alumbrado que contiene códigos y descripciones de servicios de alumbrado público
    Tabla: alumbrado
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'alumbrado'
        verbose_name = 'Alumbrado'
        verbose_name_plural = 'Alumbrados'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Tren(models.Model):
    """
    Modelo para la tabla tren que contiene códigos y descripciones de servicios de tren de aseo
    Tabla: tren
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'tren'
        verbose_name = 'Tren de Aseo'
        verbose_name_plural = 'Trenes de Aseo'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Adicionales(models.Model):
    """
    Modelo para la tabla adicionales que contiene códigos y descripciones de servicios adicionales
    Tabla: adicionales
    Estructura SQL:
    - id: INTEGER NOT NULL AUTO_INCREMENT (PRIMARY KEY)
    - codigo: DECIMAL(2,0) DEFAULT 0
    - descripcion: CHAR(50) COLLATE latin1_swedish_ci NOT NULL
    - PRIMARY KEY (id)
    - UNIQUE KEY codigo (codigo)
    """
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=2, decimal_places=0, default=0, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'adicionales'
        verbose_name = 'Servicio Adicional'
        verbose_name_plural = 'Servicios Adicionales'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class ComentariosCatastro(models.Model):
    """
    Modelo para la tabla comentarios_catastro que contiene comentarios asociados a una clave catastral
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    clave = models.CharField(max_length=20, default='', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    comentario = models.CharField(max_length=2000, null=True, blank=True, default=None, verbose_name='Comentario', db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=50, default='', verbose_name='Usuario', db_collation='latin1_swedish_ci')
    fecha = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Fecha')

    class Meta:
        app_label = 'catastro'
        db_table = 'comentarios_catastro'
        verbose_name = 'Comentario Catastro'
        verbose_name_plural = 'Comentarios Catastro'
        ordering = ['-fecha', '-id']
        indexes = [
            models.Index(fields=['clave'], name='clave'),
            models.Index(fields=['empresa'], name='comentarios_catastro_idx1'),
        ]

    def __str__(self):
        comentario_preview = (self.comentario[:50] + '...') if self.comentario and len(self.comentario) > 50 else (self.comentario or 'Sin comentario')
        return f"{self.clave} - {comentario_preview}"

class TasasMunicipales(models.Model):
    """
    Modelo para la tabla tasassmunicipales que contiene las tasas municipales para bienes inmuebles
    """
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Empresa', db_collation='latin1_swedish_ci')
    clave = models.CharField(max_length=20, default='', verbose_name='Clave Catastral', db_collation='latin1_swedish_ci')
    rubro = models.CharField(max_length=6, null=True, blank=True, default='', verbose_name='Rubro', db_collation='latin1_swedish_ci')
    cod_tarifa = models.CharField(max_length=4, null=True, blank=True, default=None, verbose_name='Código de Tarifa', db_collation='latin1_swedish_ci')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Valor')
    cuenta = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='Cuenta', db_collation='latin1_swedish_ci')
    cuentarez = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='Cuenta Rezago', db_collation='latin1_swedish_ci')

    class Meta:
        app_label = 'catastro'
        db_table = 'tasassmunicipales'
        verbose_name = 'Tasa Municipal'
        verbose_name_plural = 'Tasas Municipales'
        ordering = ['clave', 'rubro', 'cod_tarifa']
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'clave', 'rubro'], name='tarifasics_idx4')
        ]
        indexes = [
            models.Index(fields=['clave'], name='tarifasics_idx1'),
            models.Index(fields=['cod_tarifa'], name='tarifasics_idx3'),
            models.Index(fields=['empresa', 'clave'], name='tarifasics_idx_empresa_clave'),
        ]

    def __str__(self):
        return f"{self.clave} - {self.rubro} - {self.cod_tarifa} - {self.valor}"


# Mapas digitales (proyecto / capa / GeoJSON) — ver models_mapas.py
from .models_mapas import MapaCapa, MapaElemento, MapaProyecto  # noqa: E402, F401

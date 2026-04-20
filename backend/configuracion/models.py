from decimal import Decimal

from django.db import models

# Re-export para formularios y vistas existentes
from core.models import Departamento  # noqa: F401


class Nacionalidad(models.Model):
    """Vista ORM de la tabla nacionalidad (catálogo global, no exclusivo de Catastro)."""

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=45, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        db_table = 'nacionalidad'
        managed = False
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descripcion or ''}".strip()


class Sitio(models.Model):
    """Catálogo: sitio del predio (tabla propia en BD)."""

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    descripcion = models.CharField(max_length=150, verbose_name='Descripción')

    class Meta:
        db_table = 'sitio'
        verbose_name = 'Sitio del predio'
        verbose_name_plural = 'Sitios del predio'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.descripcion or ""}'.strip()


# --- Catálogos de predio: columnas alineadas a tablas MySQL reales (DESCRIBE) ---


class Habitacional(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=2, unique=True, verbose_name='Código', db_column='cohabit')
    descripcion = models.CharField(max_length=45, verbose_name='Descripción', db_column='bdeshabit')

    class Meta:
        db_table = 'habitacional'
        managed = False
        verbose_name = 'Código habitacional'
        verbose_name_plural = 'Códigos habitacionales'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.descripcion or ""}'.strip()


class _CodigoDecimal2Desc50(models.Model):
    """Esquema común: codigo decimal(2,0), descripcion char(50)."""

    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(
        max_digits=2, decimal_places=0, null=True, blank=True, unique=True,
        verbose_name='Código', db_column='codigo',
    )
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_column='descripcion')

    class Meta:
        abstract = True

    def __str__(self):
        c = self.codigo if self.codigo is not None else ''
        return f'{c} - {self.descripcion or ""}'.strip()


class Agua(_CodigoDecimal2Desc50):
    class Meta:
        db_table = 'agua'
        managed = False
        verbose_name = 'Agua'
        verbose_name_plural = 'Agua'
        ordering = ['codigo']


class Alumbrado(_CodigoDecimal2Desc50):
    class Meta:
        db_table = 'alumbrado'
        managed = False
        verbose_name = 'Alumbrado'
        verbose_name_plural = 'Alumbrado'
        ordering = ['codigo']


class Calle(_CodigoDecimal2Desc50):
    class Meta:
        db_table = 'calle'
        managed = False
        verbose_name = 'Calle'
        verbose_name_plural = 'Calles'
        ordering = ['codigo']


class Colindancias(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=1, null=True, blank=True, unique=True, verbose_name='Código', db_column='codigo')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', db_column='descripcion')

    class Meta:
        db_table = 'colindancias'
        managed = False
        verbose_name = 'Colindancias'
        verbose_name_plural = 'Colindancias'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo or ""} - {self.descripcion or ""}'.strip()


class _CodigoDecimal2Desc200(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.DecimalField(
        max_digits=2, decimal_places=0, null=True, blank=True,
        verbose_name='Código', db_column='codigo',
    )
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Descripción', db_column='descripcion')

    class Meta:
        abstract = True

    def __str__(self):
        c = self.codigo if self.codigo is not None else ''
        return f'{c} - {self.descripcion or ""}'.strip()


class Dominio(_CodigoDecimal2Desc200):
    class Meta:
        db_table = 'dominio'
        managed = False
        verbose_name = 'Tipo de dominio'
        verbose_name_plural = 'Tipos de dominio'
        ordering = ['codigo']


class Drenaje(_CodigoDecimal2Desc50):
    class Meta:
        db_table = 'drenaje'
        managed = False
        verbose_name = 'Tipo de alcantarillado'
        verbose_name_plural = 'Tipos de alcantarillado'
        ordering = ['codigo']


class Electricidad(_CodigoDecimal2Desc50):
    class Meta:
        db_table = 'electricidad'
        managed = False
        verbose_name = 'Electricidad'
        verbose_name_plural = 'Electricidad'
        ordering = ['codigo']


class _CodigoChar3Desc50(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, verbose_name='Código', db_column='codigo')
    descripcion = models.CharField(max_length=50, verbose_name='Descripción', db_column='descripcion')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.codigo} - {self.descripcion or ""}'.strip()


class Explotacion(_CodigoChar3Desc50):
    class Meta:
        db_table = 'explotacion'
        managed = False
        verbose_name = 'Explotación del predio'
        verbose_name_plural = 'Explotación del predio'
        ordering = ['codigo']


class Irrigacion(_CodigoChar3Desc50):
    class Meta:
        db_table = 'irrigacion'
        managed = False
        verbose_name = 'Sistema de irrigación'
        verbose_name_plural = 'Sistemas de irrigación'
        ordering = ['codigo']


class Naturaleza(_CodigoDecimal2Desc200):
    class Meta:
        db_table = 'naturaleza'
        managed = False
        verbose_name = 'Naturaleza jurídica'
        verbose_name_plural = 'Naturalezas jurídicas'
        ordering = ['codigo']


class CfgSubuso(models.Model):
    """
    Catálogo subuso (tabla `subuso`). Nombre de clase distinto de `catastro.Subuso` para evitar
    colisiones de importación y estados obsoletos con columnas codigo/descripcion genéricas.
    """

    id = models.AutoField(primary_key=True)
    uso = models.CharField(max_length=3, verbose_name='Uso', db_column='uso')
    codsubuso = models.CharField(max_length=5, blank=True, null=True, verbose_name='Cód. subuso', db_column='codsubuso')
    descripcion = models.CharField(max_length=34, verbose_name='Descripción', db_column='des_subuso')

    class Meta:
        db_table = 'subuso'
        managed = False
        verbose_name = 'Uso del predio'
        verbose_name_plural = 'Usos del predio'
        ordering = ['uso', 'codsubuso']

    def __str__(self):
        return f'{self.uso} {self.codsubuso or ""} - {self.descripcion or ""}'.strip()


class Telefono(_CodigoDecimal2Desc50):
    class Meta:
        db_table = 'telefono'
        managed = False
        verbose_name = 'Teléfono'
        verbose_name_plural = 'Teléfono'
        ordering = ['codigo']


class Tipomedida(_CodigoDecimal2Desc200):
    class Meta:
        db_table = 'tipomedida'
        managed = False
        verbose_name = 'Tipo de medida'
        verbose_name_plural = 'Tipos de medida'
        ordering = ['codigo']


class CfgTopografia(models.Model):
    """Catálogo topografía (tabla `topografia`). Clase dedicada; columnas reales MySQL."""

    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, blank=True, null=True, verbose_name='Empresa', db_column='empresa')
    cotopo = models.CharField(max_length=2, verbose_name='Cód. topografía', db_column='cotopo')
    descritopo = models.CharField(max_length=40, verbose_name='Descripción', db_column='descritopo')
    factopo = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), verbose_name='Factor', db_column='factopo')

    class Meta:
        db_table = 'topografia'
        managed = False
        verbose_name = 'Topografía del predio'
        verbose_name_plural = 'Topografías del predio'
        ordering = ['empresa', 'cotopo']

    def __str__(self):
        return f'{self.empresa or ""} {self.cotopo} - {self.descritopo or ""}'.strip()


class Usotierra(_CodigoChar3Desc50):
    class Meta:
        db_table = 'usotierra'
        managed = False
        verbose_name = 'Uso de tierra'
        verbose_name_plural = 'Usos de tierra'
        ordering = ['codigo']


class Vias(_CodigoChar3Desc50):
    class Meta:
        db_table = 'vias'
        managed = False
        verbose_name = 'Vías de comunicación'
        verbose_name_plural = 'Vías de comunicación'
        ordering = ['codigo']


class Zonasusos(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20, blank=True, null=True, unique=True,
        verbose_name='Tipo de zona', db_column='tipozona',
    )
    descripcion = models.CharField(max_length=100, blank=True, null=True, verbose_name='Descripción', db_column='descripcion')

    class Meta:
        db_table = 'zonasusos'
        managed = False
        verbose_name = 'Zonificación'
        verbose_name_plural = 'Zonificaciones'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo or ""} - {self.descripcion or ""}'.strip()


class Caserio(models.Model):
    """Vista ORM de la tabla caserio (catálogo global por depto/municipio/barrio)."""

    id = models.AutoField(primary_key=True)
    depto = models.CharField(max_length=3, verbose_name='Departamento', db_collation='latin1_spanish_ci')
    codmuni = models.CharField(max_length=3, verbose_name='Código Municipio', db_collation='latin1_swedish_ci')
    codbarrio = models.CharField(max_length=3, default='', verbose_name='Código Barrio', db_collation='latin1_swedish_ci')
    codigo = models.CharField(max_length=3, default='', verbose_name='Código Caserío', db_collation='latin1_swedish_ci')
    descripcion = models.CharField(max_length=50, null=True, blank=True, verbose_name='Descripción', db_collation='latin1_swedish_ci')

    class Meta:
        db_table = 'caserio'
        managed = False
        verbose_name = 'Caserío'
        verbose_name_plural = 'Caseríos'
        ordering = ['depto', 'codmuni', 'codbarrio', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descripcion or ''}".strip()

from django.db import models
from modules.core.models import BaseModel, Municipio

class PropiedadInmueble(BaseModel):
    """
    Modelo para propiedades inmuebles
    """
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    codigo_catastral = models.CharField(max_length=50, unique=True, verbose_name="Código Catastral")
    direccion = models.TextField(verbose_name="Dirección")
    propietario = models.CharField(max_length=200, verbose_name="Propietario")
    area_terreno = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área del Terreno (m²)")
    area_construccion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Área de Construcción (m²)")
    valor_catastral = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Catastral")

    def __str__(self):
        return f"{self.codigo_catastral} - {self.direccion}"

    class Meta:
        db_table = 'catastro_propiedad_inmueble'
        verbose_name = "Propiedad Inmueble"
        verbose_name_plural = "Propiedades Inmuebles"
        ordering = ['codigo_catastral']

class Terreno(BaseModel):
    """
    Modelo para terrenos
    """
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    codigo_terreno = models.CharField(max_length=50, unique=True, verbose_name="Código del Terreno")
    direccion = models.TextField(verbose_name="Dirección")
    propietario = models.CharField(max_length=200, verbose_name="Propietario")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área (m²)")
    valor_catastral = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Catastral")

    def __str__(self):
        return f"{self.codigo_terreno} - {self.direccion}"

    class Meta:
        db_table = 'catastro_terreno'
        verbose_name = "Terreno"
        verbose_name_plural = "Terrenos"
        ordering = ['codigo_terreno']

class Construccion(BaseModel):
    """
    Modelo para construcciones
    """
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    codigo_construccion = models.CharField(max_length=50, unique=True, verbose_name="Código de Construcción")
    direccion = models.TextField(verbose_name="Dirección")
    propietario = models.CharField(max_length=200, verbose_name="Propietario")
    area_construccion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área de Construcción (m²)")
    tipo_construccion = models.CharField(max_length=100, verbose_name="Tipo de Construcción")
    valor_catastral = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Catastral")

    def __str__(self):
        return f"{self.codigo_construccion} - {self.direccion}"

    class Meta:
        db_table = 'catastro_construccion'
        verbose_name = "Construcción"
        verbose_name_plural = "Construcciones"
        ordering = ['codigo_construccion']

class Vehiculo(BaseModel):
    """
    Modelo para vehículos
    """
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    placa = models.CharField(max_length=20, unique=True, verbose_name="Placa")
    propietario = models.CharField(max_length=200, verbose_name="Propietario")
    marca = models.CharField(max_length=100, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    año = models.IntegerField(verbose_name="Año")
    valor_catastral = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Catastral")

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

    class Meta:
        db_table = 'catastro_vehiculo'
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['placa']

class EstablecimientoComercial(BaseModel):
    """
    Modelo para establecimientos comerciales
    """
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    codigo_establecimiento = models.CharField(max_length=50, unique=True, verbose_name="Código del Establecimiento")
    nombre_comercial = models.CharField(max_length=200, verbose_name="Nombre Comercial")
    propietario = models.CharField(max_length=200, verbose_name="Propietario")
    direccion = models.TextField(verbose_name="Dirección")
    actividad_comercial = models.CharField(max_length=200, verbose_name="Actividad Comercial")
    area_local = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área del Local (m²)")
    valor_catastral = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Catastral")

    def __str__(self):
        return f"{self.codigo_establecimiento} - {self.nombre_comercial}"

    class Meta:
        db_table = 'catastro_establecimiento_comercial'
        verbose_name = "Establecimiento Comercial"
        verbose_name_plural = "Establecimientos Comerciales"
        ordering = ['codigo_establecimiento']

class TasasMunicipales(models.Model):
    """
    Modelo para la tabla tasassmunicipales - Tasas municipales registradas
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    clave = models.CharField(max_length=20, default='', verbose_name="Clave", db_collation='latin1_swedish_ci')
    rubro = models.CharField(max_length=6, default='', verbose_name="Rubro", db_collation='latin1_swedish_ci')
    cod_tarifa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Código de Tarifa", db_collation='latin1_swedish_ci')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor")
    cuenta = models.CharField(max_length=20, default='', verbose_name="Cuenta", db_collation='latin1_swedish_ci')
    cuentarez = models.CharField(max_length=20, default='', verbose_name="Cuenta Rezago", db_collation='latin1_swedish_ci')
    
    def __str__(self):
        return f"Tasa {self.clave} - Rubro {self.rubro}"
    
    class Meta:
        db_table = 'tasassmunicipales'
        verbose_name = "Tasa Municipal"
        verbose_name_plural = "Tasas Municipales"
        unique_together = (('empresa', 'clave', 'rubro'),)
        ordering = ['clave', 'rubro']





























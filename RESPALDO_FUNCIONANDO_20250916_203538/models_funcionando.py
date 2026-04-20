from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.validators import MinValueValidator

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4, unique=True, default='', verbose_name="Código")
    descripcion = models.CharField(max_length=29, verbose_name="Descripción")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'municipio'
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['codigo']



class usuario(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, verbose_name="Código de Empresa", default='', db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=15, verbose_name="Nombre de Usuario", db_collation='latin1_swedish_ci')
    password = models.CharField(max_length=255, verbose_name="Contraseña", db_collation='latin1_swedish_ci')
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre", db_collation='latin1_swedish_ci')

    def save(self, *args, **kwargs):
        # Hash la contraseña antes de guardarla si es nueva o ha sido modificada
        if not self.pk or not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
            self.password_changed_at = timezone.now()
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        if self.nombre:
            return self.nombre
        return self.usuario

    def get_short_name(self):
        """Retorna el nombre corto del usuario"""
        return self.nombre or self.usuario

    def is_locked(self):
        """Verifica si el usuario está bloqueado"""
        return False  # Simplificado para la estructura básica

    def lock_account(self, duration_minutes=30):
        """Bloquea la cuenta del usuario por un tiempo determinado"""
        pass  # Simplificado para la estructura básica

    def unlock_account(self):
        """Desbloquea la cuenta del usuario"""
        pass  # Simplificado para la estructura básica

    def record_failed_login(self):
        """Registra un intento fallido de login"""
        pass  # Simplificado para la estructura básica

    def record_successful_login(self):
        """Registra un login exitoso"""
        pass  # Simplificado para la estructura básica

    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['nombre', 'usuario']
        unique_together = ('empresa', 'usuario', 'password')
        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['usuario']),
        ]

class Identificacion(models.Model):
    id = models.AutoField(primary_key=True)
    identidad = models.CharField(max_length=18, unique=True, db_collation='latin1_swedish_ci')
    nombres = models.CharField(max_length=30, null=True, blank=True, db_collation='latin1_swedish_ci')
    apellidos = models.CharField(max_length=30, null=True, blank=True, db_collation='latin1_swedish_ci')
    fechanac = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.identidad} - {self.nombres} {self.apellidos}"

    class Meta:
        db_table = 'identificacion'
        verbose_name = "Identificación"
        verbose_name_plural = "Identificaciones"

class Actividad(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4)
    codigo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'actividad'
        ordering = ['codigo']
        unique_together = ('empresa', 'codigo')

class Oficina(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4)
    codigo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'oficina'
        ordering = ['codigo']
        unique_together = ('empresa', 'codigo')

class Negocio(models.Model):
    """
    Modelo para la tabla negocios.
    Estructura alineada exactamente con la tabla real de la base de datos.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    rtm = models.CharField(max_length=16, verbose_name="RTM", db_collation='latin1_swedish_ci')
    expe = models.CharField(max_length=12, verbose_name="Expediente", db_collation='latin1_swedish_ci')
    nombrenego = models.CharField(max_length=100, default=' ', verbose_name="Nombre del Negocio", db_collation='latin1_swedish_ci')
    comerciante = models.CharField(max_length=100, default=' ', verbose_name="Comerciante", db_collation='latin1_swedish_ci')
    identidad = models.CharField(max_length=20, default=' ', verbose_name="Identidad", db_collation='latin1_swedish_ci')  # NOT NULL en la tabla
    rtnpersonal = models.CharField(max_length=20, default=' ', verbose_name="RTN Personal", db_collation='latin1_swedish_ci')
    rtnnego = models.CharField(max_length=19, default=' ', verbose_name="RTN Negocio", db_collation='latin1_swedish_ci')
    catastral = models.CharField(max_length=17, default=' ', verbose_name="Catastral", db_collation='latin1_swedish_ci')  # NOT NULL en la tabla
    identidadrep = models.CharField(max_length=20, default=' ', verbose_name="Identidad Representante", db_collation='latin1_swedish_ci')
    representante = models.CharField(max_length=100, default=' ', verbose_name="Representante", db_collation='latin1_swedish_ci')
    direccion = models.CharField(max_length=100, default=' ', verbose_name="Dirección", db_collation='latin1_swedish_ci')
    actividad = models.CharField(max_length=20, default=' ', verbose_name="Actividad", db_collation='latin1_swedish_ci')
    estatus = models.CharField(max_length=1, default=' ', verbose_name="Estatus", db_collation='latin1_swedish_ci')  # NOT NULL en la tabla
    descriestatus = models.CharField(max_length=50, default=' ', verbose_name="Descripción Estatus", db_collation='latin1_swedish_ci')
    fecha_ini = models.DateField(null=True, blank=True, verbose_name="Fecha Inicio")
    fecha_can = models.DateField(null=True, blank=True, verbose_name="Fecha Cancelación")
    telefono = models.CharField(max_length=20, default=' ', verbose_name="Teléfono", db_collation='latin1_swedish_ci')
    celular = models.CharField(max_length=20, default=' ', verbose_name="Celular", db_collation='latin1_swedish_ci')
    socios = models.CharField(max_length=250, default=' ', verbose_name="Socios", db_collation='latin1_swedish_ci')  # NOT NULL en la tabla
    correo = models.CharField(max_length=35, default=' ', verbose_name="Correo", db_collation='latin1_swedish_ci')
    pagweb = models.CharField(max_length=40, default=' ', verbose_name="Página Web", db_collation='latin1_swedish_ci')
    comentario = models.TextField(null=True, blank=True, verbose_name="Comentario", db_collation='latin1_swedish_ci')
    descriactividad = models.CharField(max_length=100, default=' ', verbose_name="Descripción Actividad", db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=10, default=' ', verbose_name="Usuario", db_collation='latin1_swedish_ci')
    fechasys = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Sistema")
    categoria = models.CharField(max_length=2, default=' ', verbose_name="Categoría", db_collation='latin1_swedish_ci')  # NOT NULL en la tabla
    cx = models.DecimalField(max_digits=11, decimal_places=8, default=0.00000000, verbose_name="Coordenada X")
    cy = models.DecimalField(max_digits=11, decimal_places=8, default=0.00000000, verbose_name="Coordenada Y")

    def __str__(self):
        return self.nombrenego or self.rtm or str(self.pk)

    class Meta:
        db_table = 'negocios'
        unique_together = ('empresa', 'rtm', 'expe')
        verbose_name = "Negocio"
        verbose_name_plural = "Negocios"
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
    Modelo para almacenar pagos varios temporales.
    Esta tabla contiene los registros de pagos antes de ser procesados definitivamente.
    """
    # Campo id como AUTO_INCREMENT - configuración explícita
    id = models.BigAutoField(primary_key=True)
    empresa = models.CharField(max_length=6, null=True, blank=True, verbose_name="Empresa")
    recibo = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Número de Recibo")
    codigo = models.CharField(max_length=16, verbose_name="Código de Actividad")
    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de Pago")
    identidad = models.CharField(max_length=31, null=True, blank=True, verbose_name="Identidad")
    nombre = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nombre")
    descripcion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción")
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Total")
    comentario = models.CharField(max_length=500, null=True, blank=True, verbose_name="Comentario")
    oficina = models.CharField(max_length=20, null=True, blank=True, verbose_name="Oficina")
    facturadora = models.CharField(max_length=45, null=True, blank=True, verbose_name="Facturadora")
    aplicado = models.CharField(max_length=1, default='0', verbose_name="Aplicado")
    traslado = models.CharField(max_length=1, default='0', verbose_name="Traslado")
    solvencia = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="Solvencia")
    fecha_solv = models.DateField(null=True, blank=True, verbose_name="Fecha de Solvencia")
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Cantidad")
    vl_unit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Unitario")
    deposito = models.DecimalField(max_digits=1, decimal_places=0, default=0, verbose_name="Depósito")
    cajero = models.CharField(max_length=20, null=True, blank=True, verbose_name="Cajero")
    usuario = models.CharField(max_length=30, null=True, blank=True, verbose_name="Usuario")
    referencia = models.CharField(max_length=20, null=True, blank=True, verbose_name="Referencia")
    banco = models.CharField(max_length=3, null=True, blank=True, verbose_name="Banco")
    Tipofa = models.CharField(max_length=1, default=' ', verbose_name="Tipo de Factura")
    Rtm = models.CharField(max_length=20, default=' ', verbose_name="RTM")
    expe = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name="Expediente")
    pagodia = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Pago del Día")
    rcaja = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Recibo de Caja")
    Direccion = models.CharField(max_length=80, default=' ', verbose_name="Dirección")
    Rfechapag = models.DateField(null=True, blank=True, verbose_name="Fecha de Pago Real")
    permiso = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Permiso")
    Fechavence = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    direccion = models.CharField(max_length=100, default=' ', verbose_name="Dirección")
    prima = models.CharField(max_length=1, default='', blank=True, verbose_name="Prima")
    categoria = models.CharField(max_length=2, default='', blank=True, verbose_name="Categoría")
    sexo = models.CharField(max_length=1, default='', blank=True, verbose_name="Sexo")
    rtn = models.CharField(max_length=20, null=True, blank=True, verbose_name="RTN")

    class Meta:
        db_table = 'pagovariostemp'
        verbose_name = "Pago Varios Temporal"
        verbose_name_plural = "Pagos Varios Temporales"
        ordering = ['-fecha', '-recibo']

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
            self.fecha and 
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

class NoRecibos(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    solvencia = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    class Meta:
        db_table = 'norecibos'
        verbose_name = "Número de Recibo"
        verbose_name_plural = "Números de Recibos"

    def __str__(self):
        return f"Recibo #{self.numero}"

class Rubro(models.Model):
    """
    Modelo para la tabla rubros.
    Estructura alineada exactamente con la tabla real de la base de datos.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='utf8mb4_0900_ai_ci', default='')
    codigo = models.CharField(max_length=4, verbose_name="Código", db_collation='utf8mb4_0900_ai_ci', default='')
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci', default='')
    cuenta = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cuenta", db_collation='utf8mb4_0900_ai_ci', default='')
    cuentarez = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cuenta Rezago", db_collation='utf8mb4_0900_ai_ci', default='')
    tipo = models.CharField(max_length=1, blank=True, null=True, verbose_name="Tipo", db_collation='utf8mb4_0900_ai_ci', default='')

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para manejar mejor la validación de duplicados"""
        # Si es una actualización (tiene ID), permitir el guardado
        if self.pk:
            super().save(*args, **kwargs)
        else:
            # Si es un nuevo registro, verificar duplicados
            try:
                existing = Rubro.objects.get(empresa=self.empresa, codigo=self.codigo)
                # Si existe, actualizar en lugar de crear
                existing.descripcion = self.descripcion
                existing.cuenta = self.cuenta
                existing.cuentarez = self.cuentarez
                existing.tipo = self.tipo
                existing.save()
                # Actualizar el ID para que el objeto actual refleje el registro actualizado
                self.pk = existing.pk
            except Rubro.DoesNotExist:
                # No existe, crear nuevo
                super().save(*args, **kwargs)

    class Meta:
        db_table = 'rubros'
        verbose_name = "Rubro"
        verbose_name_plural = "Rubros"
        ordering = ['codigo']
        unique_together = ('empresa', 'codigo')
        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['codigo']),
            models.Index(fields=['empresa', 'codigo']),
        ]

class PlanArbitrio(models.Model):
    """
    Modelo para la tabla planarbitio.
    Almacena las tasas y rangos para el cálculo de arbitrios.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='utf8mb4_0900_ai_ci', default='')
    rubro = models.CharField(max_length=4, verbose_name="Rubro", db_collation='utf8mb4_0900_ai_ci', default='')
    cod_tarifa = models.CharField(max_length=4, verbose_name="Código Tarifa", db_collation='utf8mb4_0900_ai_ci', null=True)
    ano = models.DecimalField(max_digits=4, decimal_places=0, verbose_name="Año")
    codigo = models.CharField(max_length=20, verbose_name="Código", db_collation='utf8mb4_0900_ai_ci', default='')
    descripcion = models.CharField(max_length=200, verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci', default='')
    minimo = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Mínimo", default=0.00, null=True, blank=True)
    maximo = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Máximo", default=0.00, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", default=0.00, null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion} ({self.ano})"

    class Meta:
        db_table = 'planarbitio'
        verbose_name = "Plan de Arbitrio"
        verbose_name_plural = "Planes de Arbitrio"
        unique_together = ['empresa', 'rubro', 'cod_tarifa', 'ano', 'codigo']
        indexes = [
            models.Index(fields=['empresa'], name='planarbitio_empresa_idx'),
            models.Index(fields=['rubro'], name='planarbitio_rubro_idx'),
            models.Index(fields=['cod_tarifa'], name='planarbitio_cod_tarifa_idx'),
            models.Index(fields=['ano'], name='planarbitio_ano_idx'),
            models.Index(fields=['empresa', 'rubro'], name='planarbitio_empresa_rubro_idx'),
        ]

    @classmethod
    def calcular_tasa_por_volumen(cls, empresa, rubro, ano, volumen_total):
        """
        Calcula la tasa aplicable según el volumen total declarado.
        
        Args:
            empresa (str): Código de la empresa
            rubro (str): Código del rubro
            ano (int): Año de vigencia
            volumen_total (Decimal): Volumen total declarado
            
        Returns:
            dict: Información de la tasa aplicable
        """
        try:
            # Buscar la tasa que corresponda al rango del volumen
            tasa = cls.objects.filter(
                empresa=empresa,
                rubro=rubro,
                ano=ano,
                minimo__lte=volumen_total,
                maximo__gte=volumen_total
            ).first()
            
            if tasa:
                return {
                    'exito': True,
                    'tasa': {
                        'codigo': tasa.codigo,
                        'descripcion': tasa.descripcion,
                        'minimo': float(tasa.minimo),
                        'maximo': float(tasa.maximo),
                        'valor': float(tasa.valor),
                        'volumen_aplicable': float(volumen_total)
                    }
                }
            else:
                # Si no encuentra tasa en rango, buscar la más cercana
                tasas_disponibles = cls.objects.filter(
                    empresa=empresa,
                    rubro=rubro,
                    ano=ano
                ).order_by('minimo')
                
                if tasas_disponibles.exists():
                    # Usar la tasa con el mínimo más alto que no exceda el volumen
                    tasa_menor = tasas_disponibles.filter(minimo__lte=volumen_total).order_by('-minimo').first()
                    if tasa_menor:
                        return {
                            'exito': True,
                            'tasa': {
                                'codigo': tasa_menor.codigo,
                                'descripcion': tasa_menor.descripcion,
                                'minimo': float(tasa_menor.minimo),
                                'maximo': float(tasa_menor.maximo),
                                'valor': float(tasa_menor.valor),
                                'volumen_aplicable': float(volumen_total),
                                'nota': 'Aplicada tasa del rango más cercano'
                            }
                        }
                
                return {
                    'exito': False,
                    'mensaje': f'No se encontró tasa aplicable para el volumen {volumen_total}'
                }
                
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f'Error al calcular tasa: {str(e)}'
            }

    @classmethod
    def obtener_tasas_por_negocio(cls, empresa, rubro, ano, volumen_total=None):
        """
        Obtiene todas las tasas (fijas y variables) aplicables al negocio.
        
        Args:
            empresa (str): Código de la empresa
            rubro (str): Código del rubro
            ano (int): Año de vigencia
            volumen_total (Decimal): Volumen total declarado (solo para tasas variables)
            
        Returns:
            dict: Información de las tasas aplicables
        """
        try:
            from tributario_app.models import Tarifas
            
            # Obtener tasas fijas desde la tabla tarifas
            tasas_fijas = Tarifas.objects.filter(
                empresa=empresa,
                rubro=rubro,
                ano=ano,
                tipo='F'  # Tasas fijas
            )
            
            # Obtener tasas variables desde planarbitio
            tasas_variables = cls.objects.filter(
                empresa=empresa,
                rubro=rubro,
                ano=ano
            ).order_by('minimo')
            
            resultado = {
                'exito': True,
                'tasas_fijas': [],
                'tasas_variables': [],
                'empresa': empresa,
                'rubro': rubro,
                'ano': ano
            }
            
            # Procesar tasas fijas
            for tasa in tasas_fijas:
                resultado['tasas_fijas'].append({
                    'codigo': tasa.codigo,
                    'descripcion': tasa.descripcion,
                    'valor': float(tasa.valor),
                    'tipo': 'Fija',
                    'aplicable': True
                })
            
            # Procesar tasas variables
            if volumen_total is not None:
                for tasa in tasas_variables:
                    es_aplicable = (tasa.minimo <= volumen_total <= tasa.maximo)
                    resultado['tasas_variables'].append({
                        'codigo': tasa.codigo,
                        'descripcion': tasa.descripcion,
                        'minimo': float(tasa.minimo),
                        'maximo': float(tasa.maximo),
                        'valor': float(tasa.valor),
                        'tipo': 'Variable',
                        'aplicable': es_aplicable,
                        'volumen_aplicable': float(volumen_total) if es_aplicable else None
                    })
            else:
                # Si no hay volumen, mostrar todas las tasas variables disponibles
                for tasa in tasas_variables:
                    resultado['tasas_variables'].append({
                        'codigo': tasa.codigo,
                        'descripcion': tasa.descripcion,
                        'minimo': float(tasa.minimo),
                        'maximo': float(tasa.maximo),
                        'valor': float(tasa.valor),
                        'tipo': 'Variable',
                        'aplicable': False,
                        'volumen_aplicable': None
                    })
            
            return resultado
                
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f'Error al obtener tasas: {str(e)}'
            }

class Tarifas(models.Model):
    """
    Modelo para la tabla tarifas.
    Estructura alineada exactamente con la tabla real de la base de datos.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='utf8mb4_0900_ai_ci', default='')
    rubro = models.CharField(max_length=4, blank=True, null=True, verbose_name="Rubro", db_collation='utf8mb4_0900_ai_ci', default='')
    cod_tarifa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Código de Tarifa", db_collation='utf8mb4_0900_ai_ci', default='')
    ano = models.DecimalField(max_digits=4, decimal_places=0, verbose_name="Año")
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci', default='')
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", default=0.00)
    frecuencia = models.CharField(max_length=1, blank=True, null=True, verbose_name="Frecuencia", db_collation='utf8mb4_0900_ai_ci', choices=[
        ('A', 'Anual'),
        ('M', 'Mensual'),
    ])
    tipo = models.CharField(max_length=1, blank=True, null=True, verbose_name="Tipo", db_collation='utf8mb4_0900_ai_ci', choices=[
        ('F', 'Fija'),
        ('V', 'Variable'),
    ])
    categoria = models.CharField(max_length=1, blank=True, null=True, verbose_name="Categoría", db_collation='utf8mb4_0900_ai_ci', choices=[
        ('D', 'Doméstico'),
        ('C', 'Comercial'),
    ])

    class Meta:
        db_table = 'tarifas'
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        unique_together = ['empresa', 'rubro', 'ano', 'cod_tarifa']
        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['rubro']),
            models.Index(fields=['ano']),
            models.Index(fields=['cod_tarifa']),
            models.Index(fields=['empresa', 'rubro', 'ano', 'cod_tarifa']),
        ]

    def __str__(self):
        return f"{self.empresa} - {self.cod_tarifa} - {self.ano}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribir el método save para manejar la lógica de actualización vs creación
        """
        # Verificar si ya existe una tarifa con los mismos criterios
        try:
            existing = Tarifas.objects.get(
                empresa=self.empresa,
                rubro=self.rubro,
                ano=self.ano,
                cod_tarifa=self.cod_tarifa
            )
            # Si existe y no es la misma instancia, actualizar
            if existing.pk != self.pk:
                existing.descripcion = self.descripcion
                existing.valor = self.valor
                existing.frecuencia = self.frecuencia
                existing.tipo = self.tipo
                existing.categoria = self.categoria
                existing.save()
                # Actualizar el ID para que el objeto actual refleje el registro actualizado
                self.pk = existing.pk
                return
        except Tarifas.DoesNotExist:
            pass
        
        # Si no existe, crear nuevo
        super().save(*args, **kwargs)

class Anos(models.Model):
    """
    Modelo para la tabla anos.
    Estructura alineada exactamente con la tabla real de la base de datos.
    CREATE TABLE `anos` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `ano` DECIMAL(4,0) NOT NULL DEFAULT 0,
      PRIMARY KEY USING BTREE (`id`)
    )
    """
    id = models.AutoField(primary_key=True)
    ano = models.DecimalField(max_digits=4, decimal_places=0, verbose_name="Año", default=0)

    class Meta:
        db_table = 'anos'
        verbose_name = "Año"
        verbose_name_plural = "Años"

    def __str__(self):
        return str(self.ano)


class TarifasICS(models.Model):
    """
    Modelo para la tabla tarifasics.
    Estructura alineada exactamente con la tabla real de la base de datos.
    
    CREATE TABLE `tarifasics` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `empresa` CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL,
      `idneg` INTEGER NOT NULL DEFAULT 0,
      `rtm` CHAR(20) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
      `expe` CHAR(10) COLLATE latin1_swedish_ci DEFAULT '',
      `rubro` CHAR(4) COLLATE latin1_swedish_ci DEFAULT '',
      `cod_tarifa` VARCHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL,
      `valor` DECIMAL(12,2) DEFAULT 0.00,
      PRIMARY KEY USING BTREE (`id`),
      UNIQUE KEY `tarifasics_idx4` USING BTREE (`empresa`, `rtm`, `expe`, `cod_tarifa`),
      KEY `tarifasics_idx1` USING BTREE (`rtm`),
      KEY `tarifasics_idx2` USING BTREE (`expe`),
      KEY `tarifasics_idx3` USING BTREE (`cod_tarifa`),
      KEY `tarifasics_idx5` USING BTREE (`idneg`)
    ) ENGINE=MyISAM
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Empresa", db_collation='latin1_swedish_ci')
    idneg = models.IntegerField(verbose_name="ID Negocio", default=0)
    rtm = models.CharField(max_length=20, verbose_name="RTM", db_collation='latin1_swedish_ci', default='')
    expe = models.CharField(max_length=10, blank=True, null=True, verbose_name="Expediente", db_collation='latin1_swedish_ci', default='')
    rubro = models.CharField(max_length=4, blank=True, null=True, verbose_name="Rubro", db_collation='latin1_swedish_ci', default='')
    cod_tarifa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Código de Tarifa", db_collation='latin1_swedish_ci', default='')
    valor = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Valor", 
        default=0.00
    )

    class Meta:
        db_table = 'tarifasics'
        verbose_name = "Tarifa ICS"
        verbose_name_plural = "Tarifas ICS"
        indexes = [
            models.Index(fields=['rtm'], name='tarifasics_idx1'),
            models.Index(fields=['expe'], name='tarifasics_idx2'),
            models.Index(fields=['cod_tarifa'], name='tarifasics_idx3'),
            models.Index(fields=['idneg'], name='tarifasics_idx5'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'rtm', 'expe', 'cod_tarifa'],
                name='tarifasics_idx4'
            )
        ]

    def __str__(self):
        return f"Empresa {self.empresa} - Negocio {self.idneg} - Tarifa {self.cod_tarifa} - Valor {self.valor}"

    @classmethod
    def obtener_tarifas_por_negocio(cls, idneg):
        """
        Obtiene todas las tarifas vinculadas a un negocio específico.
        
        Args:
            idneg (int): ID del negocio
            
        Returns:
            QuerySet: Tarifas vinculadas al negocio
        """
        return cls.objects.filter(idneg=idneg).order_by('cod_tarifa')
    
    @classmethod
    def obtener_tarifas_por_empresa(cls, empresa):
        """
        Obtiene todas las tarifas vinculadas a una empresa específica.
        
        Args:
            empresa (str): Código de la empresa
            
        Returns:
            QuerySet: Tarifas vinculadas a la empresa
        """
        return cls.objects.filter(empresa=empresa).order_by('rtm', 'expe', 'cod_tarifa')
    
    @classmethod
    def obtener_tarifas_por_negocio_completo(cls, empresa, rtm, expe):
        """
        Obtiene todas las tarifas vinculadas a un negocio específico usando empresa, RTM y expediente.
        
        Args:
            empresa (str): Código de la empresa
            rtm (str): RTM del negocio
            expe (str): Expediente del negocio
            
        Returns:
            QuerySet: Tarifas vinculadas al negocio
        """
        return cls.objects.filter(empresa=empresa, rtm=rtm, expe=expe).order_by('cod_tarifa')


class TarifasImptoics(models.Model):
    """
    Modelo para la tabla tarifasimptoics.
    Estructura exacta de la tabla en la base de datos bdsimafipy.
    
    CREATE TABLE `tarifasimptoics` (
      `id` INTEGER NOT NULL AUTO_INCREMENT,
      `categoria` CHAR(1) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
      `descripcion` CHAR(200) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
      `codigo` DECIMAL(1,0) DEFAULT NULL,
      `rango1` DECIMAL(12,2) DEFAULT 0.00,
      `rango2` DECIMAL(12,2) DEFAULT 0.00,
      `valor` DECIMAL(12,2) DEFAULT 0.00,
      PRIMARY KEY USING BTREE (`id`)
    ) ENGINE=MyISAM AUTO_INCREMENT=253 ROW_FORMAT=FIXED CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci';
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    categoria = models.CharField(max_length=1, verbose_name="Categoría", db_collation='utf8mb4_0900_ai_ci', default='')
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci')
    codigo = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True, verbose_name="Código")
    rango1 = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Rango 1", default=0.00)
    rango2 = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Rango 2", default=0.00)
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", default=0.00)

    def __str__(self):
        return f"Categoría {self.categoria} - Rango {self.rango1}-{self.rango2} - Valor {self.valor}"

    class Meta:
        db_table = 'tarifasimptoics'
        verbose_name = "Tarifa Imptoics"
        verbose_name_plural = "Tarifas Imptoics"
        ordering = ['categoria', 'rango1']
        managed = True  # Django maneja la tabla

    @classmethod
    def calcular_tarifa_escalonada(cls, categoria, valor_venta):
        """
        Calcula la tarifa escalonada para un valor de venta dado.
        
        Args:
            categoria (str): Categoría de la tarifa (ej: '1')
            valor_venta (Decimal): Valor de la venta a calcular
            
        Returns:
            dict: Información del cálculo escalonado
        """
        try:
            # Obtener todas las tarifas de la categoría ordenadas por rango
            tarifas = cls.objects.filter(categoria=categoria).order_by('rango1')
            
            if not tarifas.exists():
                return {
                    'exito': False,
                    'mensaje': f'No se encontraron tarifas para la categoría {categoria}'
                }
            
            total_calculo = 0
            detalle_calculo = []
            valor_restante = valor_venta
            
            for i, tarifa in enumerate(tarifas, 1):
                if valor_restante <= 0:
                    break
                
                rango1 = float(tarifa.rango1)
                rango2 = float(tarifa.rango2)
                valor_factor = float(tarifa.valor)
                
                # Algoritmo correcto según la explicación del usuario
                if i == 1:  # Primera línea
                    if valor_restante <= rango2:
                        # Caso 1: valor <= rango2
                        # Cálculo: round(valor / 1000, 2) * campo_valor
                        valor_a_calcular = valor_restante
                        impuesto_linea = round(valor_a_calcular / 1000, 2) * valor_factor
                        total_calculo += impuesto_linea
                        
                        detalle_calculo.append(
                            f"Línea {i}: L. {valor_a_calcular:,.2f} ÷ 1000 × {valor_factor:,.2f} = L. {impuesto_linea:,.2f}"
                        )
                        
                        valor_restante = 0  # Se agota el valor
                    else:
                        # Caso 2: valor > rango2
                        # Cálculo: ((rango2 - rango1) / 1000) * campo_valor
                        valor_a_calcular = rango2 - rango1
                        impuesto_linea = round(valor_a_calcular / 1000, 2) * valor_factor
                        total_calculo += impuesto_linea
                        
                        detalle_calculo.append(
                            f"Línea {i}: L. {valor_a_calcular:,.2f} ÷ 1000 × {valor_factor:,.2f} = L. {impuesto_linea:,.2f}"
                        )
                        
                        # Restar rango2 del valor declarado
                        valor_restante = valor_restante - rango2
                else:  # Líneas subsiguientes (2, 3, 4, ...)
                    # Calcular: (rango2 - rango1) + 0.01
                    rango_calculo = (rango2 - rango1) + 0.01
                    
                    if valor_restante <= rango_calculo:
                        # Caso: valor <= rango_calculo
                        # Cálculo: valor / 1000 * campo_valor
                        valor_a_calcular = valor_restante
                        impuesto_linea = round(valor_a_calcular / 1000, 2) * valor_factor
                        total_calculo += impuesto_linea
                        
                        detalle_calculo.append(
                            f"Línea {i}: L. {valor_a_calcular:,.2f} ÷ 1000 × {valor_factor:,.2f} = L. {impuesto_linea:,.2f}"
                        )
                        
                        valor_restante = 0  # Se agota el valor
                    else:
                        # Caso: valor > rango_calculo
                        # Cálculo: rango_calculo / 1000 * campo_valor
                        valor_a_calcular = rango_calculo
                        impuesto_linea = round(valor_a_calcular / 1000, 2) * valor_factor
                        total_calculo += impuesto_linea
                        
                        detalle_calculo.append(
                            f"Línea {i}: L. {valor_a_calcular:,.2f} ÷ 1000 × {valor_factor:,.2f} = L. {impuesto_linea:,.2f}"
                        )
                        
                        # Restar rango_calculo del valor restante
                        valor_restante = valor_restante - rango_calculo
            
            return {
                'exito': True,
                'total': total_calculo,
                'detalle': '; '.join(detalle_calculo),
                'valor_original': valor_venta,
                'categoria': categoria
            }
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f'Error al calcular tarifa escalonada: {str(e)}'
            }

class DeclaracionVolumen(models.Model):
    """
    Modelo para la tabla declara - Estructura exacta de la base de datos
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='latin1_swedish_ci', blank=True, null=True)
    idneg = models.IntegerField(verbose_name="ID Negocio", default=0)
    rtm = models.CharField(max_length=20, verbose_name="RTM", db_collation='latin1_swedish_ci', default='')
    expe = models.CharField(max_length=10, verbose_name="Expediente", db_collation='latin1_swedish_ci', default='')
    ano = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Año", default=0.00)
    tipo = models.DecimalField(max_digits=1, decimal_places=0, verbose_name="Tipo", default=0)
    mes = models.DecimalField(max_digits=4, decimal_places=0, verbose_name="Mes", default=0)
    ventai = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="Ventas Rubro Producción", default=0.00)
    ventac = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="Ventas Mercadería", default=0.00)
    ventas = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="Ventas por Servicios", default=0.00)
    valorexcento = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="Valores Exentos", default=0.00)
    controlado = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="Ventas Productos Controlados", default=0.00)
    unidad = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="Unidad", default=0)
    factor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Factor", default=0.00)
    fechssys = models.DateTimeField(blank=True, null=True, verbose_name="Fecha Sistema")
    usuario = models.CharField(max_length=50, verbose_name="Usuario", db_collation='latin1_swedish_ci', default='')
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Impuesto Calculado", default=0.00)

    def save(self, *args, **kwargs):
        # Calcular el impuesto total usando tarifas escalonadas
        self.impuesto = self.calcular_impuesto_total()
        
        # Guardar la declaración
        super().save(*args, **kwargs)
        
        # Crear o actualizar el rubro 0003 con el impuesto calculado
        if self.impuesto > 0:
            self.crear_actualizar_rubro_0003()
    
    def calcular_impuesto_total(self):
        """Calcula el impuesto total basado en las tarifas escalonadas"""
        from decimal import Decimal
        
        total_impuesto = Decimal('0.00')
        
        # Calcular impuesto para ventai
        if self.ventai > 0:
            calculo_ventai = TarifasImptoics.calcular_tarifa_escalonada('1', self.ventai)
            if calculo_ventai.get('exito'):
                total_impuesto += Decimal(str(calculo_ventai.get('total', 0)))
        
        # Calcular impuesto para ventac
        if self.ventac > 0:
            calculo_ventac = TarifasImptoics.calcular_tarifa_escalonada('1', self.ventac)
            if calculo_ventac.get('exito'):
                total_impuesto += Decimal(str(calculo_ventac.get('total', 0)))
        
        # Calcular impuesto para ventas
        if self.ventas > 0:
            calculo_ventas = TarifasImptoics.calcular_tarifa_escalonada('1', self.ventas)
            if calculo_ventas.get('exito'):
                total_impuesto += Decimal(str(calculo_ventas.get('total', 0)))
        
        return total_impuesto
    
    def crear_actualizar_rubro_0003(self):
        """Crea o actualiza el rubro 0003 con el impuesto calculado"""
        from .models import Rubro, Tarifas
        
        try:
            # Obtener el código de empresa desde la sesión o del negocio
            empresa = '0001'  # Por defecto, se puede obtener de la sesión
            
            # Buscar o crear el rubro 0003
            rubro, created = Rubro.objects.get_or_create(
                empresa=empresa,
                codigo='0003',
                defaults={
                    'descripcion': 'Impuesto sobre Ventas',
                    'cuenta': '0003',
                    'cuentarez': '0003',
                    'tipo': 'I'
                }
            )
            
            if created:
                print(f"✅ Rubro 0003 creado exitosamente")
            else:
                print(f"✅ Rubro 0003 ya existe")
            
            # Buscar o crear la tarifa para el rubro 0003
            ano_actual = int(self.ano) if self.ano else 2024
            
            tarifa, created = Tarifas.objects.get_or_create(
                empresa=empresa,
                rubro='0003',
                cod_tarifa='IMP',
                ano=ano_actual,
                defaults={
                    'descripcion': f'Impuesto Calculado - {self.rtm}-{self.expe}',
                    'valor': self.impuesto,
                    'frecuencia': 'M',
                    'tipo': 'F',
                    'categoria': 'C'
                }
            )
            
            if not created:
                # Actualizar el valor de la tarifa existente
                tarifa.valor = self.impuesto
                tarifa.descripcion = f'Impuesto Calculado - {self.rtm}-{self.expe}'
                tarifa.save()
                print(f"✅ Tarifa del rubro 0003 actualizada: L. {self.impuesto}")
            else:
                print(f"✅ Tarifa del rubro 0003 creada: L. {self.impuesto}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear/actualizar rubro 0003: {str(e)}")
            return False

    @property
    def base_calculo(self):
        """Propiedad calculada para la base de cálculo"""
        return (
            self.ventai + 
            self.ventac + 
            self.ventas + 
            self.valorexcento + 
            self.controlado
        )

    def __str__(self):
        return f"Declaración {self.rtm}-{self.expe} - {self.ano}/{self.mes:02d}"

    class Meta:
        db_table = 'declara'
        verbose_name = "Declaración de Volumen"
        verbose_name_plural = "Declaraciones de Volumen"
        indexes = [
            models.Index(fields=['rtm'], name='declara_idx1'),
            models.Index(fields=['expe'], name='declara_idx2'),
            models.Index(fields=['ano'], name='declara_idx3'),
            models.Index(fields=['idneg'], name='declara_idx5'),
        ]





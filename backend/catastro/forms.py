from django import forms
from django.forms import inlineformset_factory
from core.models import Municipio

# Importar modelos desde el módulo local (C:\simafiweb\venv\Scripts\catastro\models.py)
from .models import (
    BDCata1, BDTerreno, Colindantes, Colindancias, Copropietarios, DetalleAdicionales, 
    TipoSexo, Usos, Habitacional, Propietarios, Zonasusos, Nacionalidad, Edificacion, Costos, TipoDetalle, Barrios, Topografia, ConfiTipologia, Especificaciones, TipoMaterial, DetEspecificacion, ValorArbol, FactorCultivo, FactoresRiego, CultivoPermanente, Legales, Caracteristicas, TipoDocumento, Naturaleza, Dominio, TipoMedida, UnidadArea, RegistroPropiedad, Explotacion, Vias, Irrigacion, UsoTierra, Complemento, Agua, Telefono, Drenaje, Calle, Electricidad, Acera, Alumbrado, Tren, Adicionales, ComentariosCatastro, TasasMunicipales
)

class BDCata1Form(forms.ModelForm):
    """Formulario para el modelo BDCata1"""
    
    # Campo ficha con opciones personalizadas
    FICHA_CHOICES = [
        ('1', '1 - Ficha Urbana'),
        ('2', '2 - Ficha Rural'),
    ]
    
    ficha = forms.ChoiceField(
        choices=FICHA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='1',
        required=False,
        label='Ficha'
    )
    
    # Campo uso como ChoiceField para cargar desde la tabla Usos
    uso = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label='Código de Uso'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar usos desde la base de datos
        try:
            from .models import Usos
            usos = Usos.objects.all().order_by('uso')
            uso_choices = [('', '-- Seleccione un código de uso --')]
            for uso_obj in usos:
                uso_choices.append((uso_obj.uso, f"{uso_obj.uso} - {uso_obj.desuso}"))
            self.fields['uso'].choices = uso_choices
        except Exception as e:
            # Si hay error al cargar, usar opciones vacías
            self.fields['uso'].choices = [('', '-- Error al cargar usos --')]
    
    # Campo tipopropiedad con opciones personalizadas
    TIPO_PROPIEDAD_CHOICES = [
        ('1', '1 - Propiedad Normal'),
        ('2', '2 - Condominio (P.H)'),
    ]
    
    tipopropiedad = forms.ChoiceField(
        choices=TIPO_PROPIEDAD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='1',
        required=False,
        label='Tipo de Propiedad'
    )
    
    # Campo estatus tributario con opciones personalizadas
    ESTATUS_TRIBUTARIO_CHOICES = [
        ('1', '1 - Exento'),
        ('2', '2 - Parcialmente Exento'),
        ('3', '3 - Totalmente Tributario'),
        ('4', '4 - Totalmente Exento sin Valores'),
    ]
    
    st = forms.ChoiceField(
        choices=ESTATUS_TRIBUTARIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label='Estatus Tributario'
    )
    
    # Campo tercera edad con opciones personalizadas
    TERCERA_EDAD_CHOICES = [
        ('', '-- Seleccione --'),
        ('S', 'S - Sí'),
        ('N', 'N - No'),
    ]
    
    terceraedad = forms.ChoiceField(
        choices=TERCERA_EDAD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label='Descuento Tercera Edad'
    )
    
    class Meta:
        model = BDCata1
        fields = '__all__'
        # No excluir usuario y fechasys para que se muestren en el formulario
        widgets = {
            'cocata1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la clave catastral'}),
            'claveant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave anterior si existe'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres del propietario'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos del propietario'}),
            'identidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identidad'}),
            'rtn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RTN si aplica'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación exacta'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'depto': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'barrio': forms.Select(attrs={'class': 'form-select'}),
            'caserio': forms.Select(attrs={'class': 'form-select'}),
            'mapa': forms.TextInput(attrs={'class': 'form-control'}),
            'bloque': forms.TextInput(attrs={'class': 'form-control'}),
            'predio': forms.TextInput(attrs={'class': 'form-control'}),
            'lote': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de lote'}),
            'bloquecol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bloque-Col'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            'uso': forms.Select(attrs={'class': 'form-select'}),
            'subuso': forms.Select(attrs={'class': 'form-select'}),
            'constru': forms.NumberInput(attrs={'class': 'form-control'}),
            'nofichas': forms.NumberInput(attrs={'class': 'form-control'}),
            'bvl2tie': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'conedi': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'mejoras': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cedif': forms.NumberInput(attrs={'class': 'form-control'}),
            'detalle': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'impuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'grabable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cultivo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'declarado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'exencion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'condetalle': forms.NumberInput(attrs={'class': 'form-control'}),
            'st': forms.Select(attrs={'class': 'form-select'}),
            'codhab': forms.Select(attrs={'class': 'form-select'}),
            'codprop': forms.Select(attrs={'class': 'form-select'}),
            'bexenc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Porcentaje de Exención'}),
            'tasaimpositiva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'declaimpto': forms.NumberInput(attrs={'class': 'form-control'}),
            'clavesure': forms.TextInput(attrs={'class': 'form-control'}),
            'cx': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Coordenada X (UTM)'}),
            'cy': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Coordenada Y (UTM)'}),
            'zonificacion': forms.Select(attrs={'class': 'form-select'}),
            'vivienda': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1', 'placeholder': 'Cantidad de viviendas'}),
            'apartamentos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1', 'placeholder': 'Número de apartamentos'}),
            'cuartos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1', 'placeholder': 'Número de cuartos adicionales'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Usuario que registró'}),
            'fechasys': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Fecha de registro'}),
            'terceraedad': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ruta de la foto'}),
            'croquis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ruta del croquis'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar usos desde la base de datos para el campo uso
        try:
            from .models import Usos
            usos = Usos.objects.all().order_by('uso')
            uso_choices = [('', '-- Seleccione un código de uso --')]
            for uso_obj in usos:
                uso_choices.append((uso_obj.uso, f"{uso_obj.uso} - {uso_obj.desuso}"))
            # Actualizar las opciones del campo uso
            if 'uso' in self.fields:
                self.fields['uso'].choices = uso_choices
                self.fields['uso'].label = 'Código de Uso'
        except Exception as e:
            # Si hay error al cargar, mantener las opciones por defecto
            if 'uso' in self.fields:
                self.fields['uso'].choices = [('', '-- Error al cargar usos --')]
        
        # Hacer todos los campos opcionales (sin restricciones de validación)
        for field_name, field in self.fields.items():
            field.required = False
        
        # Cambiar el label del campo constru
        if 'constru' in self.fields:
            self.fields['constru'].label = 'Constru (futuras construcciones)'
        
        # Configurar campos de auditoría como readonly
        if 'usuario' in self.fields:
            self.fields['usuario'].required = False
            self.fields['usuario'].label = 'Usuario'
        if 'fechasys' in self.fields:
            self.fields['fechasys'].required = False
            self.fields['fechasys'].label = 'Fecha sistema'
            # El campo fechasys se muestra como texto readonly, el formato se maneja en la vista/API
        
        # Asegurar que campos personalizados (barrio, caserio, subuso) se procesen correctamente
        # Estos campos vienen de comboboxes personalizados en el template
        campos_personalizados = ['barrio', 'caserio', 'subuso']
        for campo in campos_personalizados:
            if campo in self.fields:
                # Asegurar que el campo acepte valores vacíos
                self.fields[campo].required = False
                # Si hay datos iniciales, establecerlos
                if self.initial and campo in self.initial:
                    self.fields[campo].initial = self.initial[campo]
        
        # Configurar campo bexenc (Porcentaje Exención)
        if 'bexenc' in self.fields:
            self.fields['bexenc'].label = 'Porcentaje Exención (%)'
            self.fields['bexenc'].required = False
        
        # Si hay una instancia existente, convertir el valor de ficha a string para el ChoiceField
        if self.instance and self.instance.pk and self.instance.ficha:
            self.fields['ficha'].initial = str(int(self.instance.ficha))
        # Si hay una instancia existente, convertir el valor de tipopropiedad a string para el ChoiceField
        if self.instance and self.instance.pk and self.instance.tipopropiedad:
            # Convertir Decimal a int y luego a string para comparar con las opciones
            tipoprop_value = int(float(self.instance.tipopropiedad))
            if tipoprop_value in [1, 2]:
                self.fields['tipopropiedad'].initial = str(tipoprop_value)
        
        # Cargar opciones de sexo desde la tabla tiposexo
        try:
            tipos_sexo = TipoSexo.objects.all().order_by('codigo')
            SEXO_CHOICES = [('', 'Seleccione un sexo')] + [
                (tipo.codigo, f"{tipo.codigo} - {tipo.descripcion or ''}".strip())
                for tipo in tipos_sexo
            ]
            self.fields['sexo'] = forms.ChoiceField(
                choices=SEXO_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Sexo'
            )
            # Si hay una instancia existente, establecer el valor inicial del sexo
            if self.instance and self.instance.pk and self.instance.sexo:
                self.fields['sexo'].initial = self.instance.sexo
        except Exception as e:
            # Fallback a opciones por defecto si hay error al cargar desde la BD
            self.fields['sexo'] = forms.ChoiceField(
                choices=[('', 'Seleccione un sexo'), ('M', 'M - Masculino'), ('F', 'F - Femenino')],
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Sexo'
            )
        
        # Cargar opciones de uso desde la tabla usos
        try:
            usos = Usos.objects.all().order_by('uso')
            USO_CHOICES = [('', 'Seleccione un uso')] + [
                (uso.uso, f"{uso.uso} - {uso.desuso or ''}".strip())
                for uso in usos
            ]
            self.fields['uso'] = forms.ChoiceField(
                choices=USO_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Uso del Predio'
            )
            # Si hay una instancia existente, establecer el valor inicial del uso
            if self.instance and self.instance.pk and self.instance.uso:
                self.fields['uso'].initial = self.instance.uso
        except Exception as e:
            # Fallback a opciones por defecto si hay error al cargar desde la BD
            self.fields['uso'] = forms.ChoiceField(
                choices=[('', 'Seleccione un uso'), ('0', '0 - Sin uso')],
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Uso del Predio'
            )
        
        # Establecer valor inicial del estatus tributario si hay una instancia existente
        if self.instance and self.instance.pk and self.instance.st:
            self.fields['st'].initial = self.instance.st
        
        # Cargar opciones de código habitacional desde la tabla habitacional
        try:
            habitacionales = Habitacional.objects.all().order_by('cohabit')
            COD_HABITACIONAL_CHOICES = [('', 'Seleccione un código habitacional')] + [
                (hab.cohabit, f"{hab.cohabit} - {hab.bdeshabit or ''}".strip())
                for hab in habitacionales
            ]
            self.fields['codhab'] = forms.ChoiceField(
                choices=COD_HABITACIONAL_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Código Habitacional'
            )
            # Si hay una instancia existente, establecer el valor inicial del código habitacional
            if self.instance and self.instance.pk and self.instance.codhab:
                self.fields['codhab'].initial = self.instance.codhab
        except Exception as e:
            # Fallback a opciones por defecto si hay error al cargar desde la BD
            self.fields['codhab'] = forms.ChoiceField(
                choices=[('', 'Seleccione un código habitacional')],
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Código Habitacional'
            )
        
        # Cargar opciones de código propietario desde la tabla propietarios
        try:
            propietarios = Propietarios.objects.all().order_by('copropi')
            COD_PROPIETARIO_CHOICES = [('', 'Seleccione un código propietario')] + [
                (prop.copropi, f"{prop.copropi} - {prop.bdespro or ''}".strip())
                for prop in propietarios
            ]
            self.fields['codprop'] = forms.ChoiceField(
                choices=COD_PROPIETARIO_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Código Propietario'
            )
            # Si hay una instancia existente, establecer el valor inicial del código propietario
            if self.instance and self.instance.pk and self.instance.codprop:
                self.fields['codprop'].initial = self.instance.codprop
        except Exception as e:
            # Fallback a opciones por defecto si hay error al cargar desde la BD
            self.fields['codprop'] = forms.ChoiceField(
                choices=[('', 'Seleccione un código propietario')],
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Código Propietario'
            )
        
        # Cargar opciones de zonificación desde la tabla zonasusos
        try:
            zonasusos = Zonasusos.objects.all().order_by('tipozona')
            ZONIFICACION_CHOICES = [('', 'Seleccione una zona')] + [
                (zona.tipozona or '', f"{zona.tipozona or ''} - {zona.descripcion or ''}".strip())
                for zona in zonasusos if zona.tipozona
            ]
            self.fields['zonificacion'] = forms.ChoiceField(
                choices=ZONIFICACION_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Zonificación'
            )
            # Si hay una instancia existente, establecer el valor inicial de la zonificación
            if self.instance and self.instance.pk and self.instance.zonificacion:
                self.fields['zonificacion'].initial = self.instance.zonificacion
        except Exception as e:
            # Fallback a opciones por defecto si hay error al cargar desde la BD
            self.fields['zonificacion'] = forms.ChoiceField(
                choices=[('', 'Seleccione una zona')],
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Zonificación'
            )
        
        # Cargar opciones de nacionalidad desde la tabla nacionalidad
        try:
            nacionalidades = Nacionalidad.objects.all().order_by('codigo')
            NACIONALIDAD_CHOICES = [('', 'Seleccione una nacionalidad')] + [
                (nac.codigo, f"{nac.codigo} - {nac.descripcion or ''}".strip())
                for nac in nacionalidades
            ]
            self.fields['nacionalidad'] = forms.ChoiceField(
                choices=NACIONALIDAD_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Nacionalidad'
            )
            # Si hay una instancia existente, establecer el valor inicial de la nacionalidad
            if self.instance and self.instance.pk and self.instance.nacionalidad:
                self.fields['nacionalidad'].initial = self.instance.nacionalidad
        except Exception as e:
            # Fallback a opciones por defecto si hay error al cargar desde la BD
            self.fields['nacionalidad'] = forms.ChoiceField(
                choices=[('', 'Seleccione una nacionalidad')],
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False,
                label='Nacionalidad'
            )
    
    def clean(self):
        """Asignar valores por defecto a todos los campos vacíos para evitar errores de validación"""
        from decimal import Decimal, InvalidOperation
        cleaned_data = super().clean()
        
        # Campos numéricos con sus valores por defecto
        campos_numericos_defaults = {
            'constru': Decimal('0'),
            'nofichas': Decimal('0'),
            'conedi': Decimal('0'),
            'cedif': Decimal('0'),
            'cultivo': Decimal('0.0000'),
            'bvl2tie': Decimal('0.00'),
            'mejoras': Decimal('0.00'),
            'detalle': Decimal('0.00'),
            'impuesto': Decimal('0.00'),
            'grabable': Decimal('0.00'),
            'declarado': Decimal('0.00'),
            'exencion': Decimal('0.00'),
            'condetalle': Decimal('0'),
            'bexenc': Decimal('0.00'),  # DECIMAL(7,2) en BD - Porcentaje Exención
            'tasaimpositiva': Decimal('0.00'),
            'declaimpto': Decimal('0'),
            'cx': Decimal('0.00'),
            'cy': Decimal('0.00'),
            'tipopropiedad': Decimal('1.00'),
            'ficha': Decimal('1'),
            'vivienda': Decimal('0'),  # DECIMAL(3,0) en BD - Número de Viviendas
            'apartamentos': Decimal('0'),  # DECIMAL(1,0) en BD - Num. Apartamentos
            'cuartos': Decimal('0'),  # DECIMAL(12,0) en BD - Num. Cuartos Adic
        }
        
        # Asignar valores por defecto a campos numéricos vacíos
        for campo, valor_default in campos_numericos_defaults.items():
            if campo not in cleaned_data or cleaned_data[campo] is None or cleaned_data[campo] == '':
                cleaned_data[campo] = valor_default
        
        # Campos de texto con valores por defecto
        campos_texto_defaults = {
            'uso': '0',
            'subuso': '',  # Permitir vacío para subuso
            'zonificacion': '',  # Permitir vacío para zonificacion
            'telefono': '0',
            'estado': 'A',
            'lote': '',  # CHAR(10) DEFAULT '' en BD
            'bloquecol': '',  # CHAR(20) DEFAULT '' en BD
        }
        
        for campo, valor_default in campos_texto_defaults.items():
            if campo not in cleaned_data or cleaned_data[campo] is None or cleaned_data[campo] == '':
                cleaned_data[campo] = valor_default
        
        # Asegurar que bexenc tenga un valor por defecto si está vacío (ya está en campos_numericos_defaults, pero lo verificamos explícitamente)
        if 'bexenc' not in cleaned_data or cleaned_data['bexenc'] is None or cleaned_data['bexenc'] == '':
            cleaned_data['bexenc'] = Decimal('0.00')

        # Valor declarado: <input type="number"> vacío no envía clave; 0 debe persistir (no dejar el valor anterior).
        if getattr(self, 'data', None) is not None and self.is_bound:
            if 'declarado' in self.data:
                raw = (self.data.get('declarado') or '').strip()
                try:
                    cleaned_data['declarado'] = Decimal(raw) if raw else Decimal('0.00')
                except (InvalidOperation, ValueError, TypeError):
                    cleaned_data['declarado'] = Decimal('0.00')
            else:
                cleaned_data['declarado'] = Decimal('0.00')

        return cleaned_data
    
    def clean_ficha(self):
        """Convertir el valor de ficha a Decimal para guardarlo en el modelo"""
        from decimal import Decimal
        ficha_value = self.cleaned_data.get('ficha')
        if ficha_value:
            try:
                return Decimal(str(ficha_value))
            except (ValueError, TypeError):
                return Decimal('1')
        return Decimal('1')  # Valor por defecto
    
    def clean_tipopropiedad(self):
        """Convertir el valor de tipopropiedad a Decimal para guardarlo en el modelo"""
        from decimal import Decimal
        tipoprop_value = self.cleaned_data.get('tipopropiedad')
        if tipoprop_value:
            try:
                return Decimal(str(tipoprop_value))
            except (ValueError, TypeError):
                return Decimal('1.00')
        return Decimal('1.00')  # Valor por defecto
    
    def clean_bexenc(self):
        """Validar bexenc (Porcentaje Exención) - DECIMAL(7,2)
        Permite valores entre 0 y 99999.99
        """
        from decimal import Decimal, ROUND_DOWN, InvalidOperation
        
        bexenc_value = self.cleaned_data.get('bexenc')
        if bexenc_value is None or bexenc_value == '':
            return Decimal('0.00')
        
        try:
            valor = Decimal(str(bexenc_value))
            # Asegurar máximo 2 decimales
            valor_redondeado = valor.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
            return valor_redondeado
        except (ValueError, TypeError, InvalidOperation):
            return Decimal('0.00')

class BDTerrenoForm(forms.ModelForm):
    """Formulario para el modelo BDTerreno"""
    class Meta:
        model = BDTerreno
        fields = '__all__'
        exclude = ['cocata1', 'usuario', 'fechasys']
        widgets = {
            'bvlbas1': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'baream21': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'tipica1': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'bfacmodi': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.001'}),
            'bfrente': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'bvlbas2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'baream22': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'tipica2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'bfacmod2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'bfrente2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
            'btopogra': forms.Select(attrs={'class': 'form-select'}),
            'bfactopo': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos opcionales (sin restricciones de validación)
        for field_name, field in self.fields.items():
            field.required = False

class EdificacionForm(forms.ModelForm):
    """Formulario para el modelo Edificacion"""
    
    class Meta:
        model = Edificacion
        fields = ['edifino', 'piso', 'area', 'uso', 'clase', 'calidad', 'costo', 'bueno', 'totedi', 'usuario', 'fechasys']
        widgets = {
            'edifino': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'required': True}),
            'piso': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '99'}),
            'area': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'uso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '1'}),
            'clase': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'calidad': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0', 'readonly': True}),
            'bueno': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999'}),
            'totedi': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0', 'readonly': True}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'maxlength': '50'}),
            'fechasys': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'type': 'text'}),
        }
        labels = {
            'edifino': 'No. Edif.',
            'piso': 'Piso',
            'area': 'Area',
            'uso': 'Uso',
            'clase': 'Clase',
            'calidad': 'Calidad',
            'costo': 'Costo/M2',
            'bueno': '% Bueno',
            'totedi': 'Total',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos opcionales excepto edifino y piso que son obligatorios
        for field_name, field in self.fields.items():
            if field_name not in ['edifino', 'piso']:
                field.required = False
            else:
                field.required = True
        
        # Configurar campos de solo lectura
        if 'usuario' in self.fields:
            self.fields['usuario'].widget.attrs['readonly'] = True
        if 'fechasys' in self.fields:
            self.fields['fechasys'].widget.attrs['readonly'] = True
        if 'costo' in self.fields:
            self.fields['costo'].widget.attrs['readonly'] = True
        

class CostosForm(forms.ModelForm):
    """Formulario para el modelo Costos - Costos Básicos Unitarios"""
    
    class Meta:
        model = Costos
        fields = ['uso', 'clase', 'calidad', 'costo', 'rango1', 'rango2']
        widgets = {
            'uso': forms.Select(attrs={'class': 'form-select'}),
            'clase': forms.Select(attrs={'class': 'form-select'}),
            'calidad': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3', 'pattern': '[0-9]{1,3}', 'title': 'Ingrese un valor numérico de 1 a 3 dígitos'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'rango1': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0'}),
            'rango2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0'}),
        }
        labels = {
            'uso': 'Uso *',
            'clase': 'Clase *',
            'calidad': 'Calidad *',
            'costo': 'Costo',
            'rango1': 'Rango 1',
            'rango2': 'Rango 2',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar opciones de uso desde la tabla usoedifica
        # El campo uso es CHAR(2), así que tomamos los primeros 2 caracteres del código
        try:
            from .models import UsoEdifica
            usos_edifica = UsoEdifica.objects.all().order_by('codigo')
            USO_CHOICES = [('', 'Seleccione un uso')]
            for uso in usos_edifica:
                codigo_uso = uso.codigo[:2]  # Tomar solo los primeros 2 caracteres
                descripcion_completa = f"{codigo_uso} - {uso.descripcion or ''}".strip()
                # Evitar duplicados en las opciones
                if not any(choice[0] == codigo_uso for choice in USO_CHOICES):
                    USO_CHOICES.append((codigo_uso, descripcion_completa))
            
            self.fields['uso'] = forms.ChoiceField(
                choices=USO_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=True,
                label='Uso *'
            )
        except Exception as e:
            # Fallback si hay error al cargar
            self.fields['uso'] = forms.ChoiceField(
                choices=[('', 'Seleccione un uso')],
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=True,
                label='Uso *'
            )
        
        # Opciones para clase con descripciones específicas
        CLASE_CHOICES = [
            ('', 'Seleccione una clase'),
            ('1', '1 - Madera'),
            ('2', '2 - Ladrillo o Bloque'),
            ('3', '3 - Loza o Terraza'),
            ('4', '4 - Bajareque o Adobe'),
            ('5', '5 - Acero Estructural'),
            ('6', '6 - Panelit'),
        ]
        self.fields['clase'] = forms.ChoiceField(
            choices=CLASE_CHOICES,
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=True,
            label='Clase *'
        )
        
        # Si hay una instancia existente, establecer los valores iniciales
        if self.instance and self.instance.pk:
            if self.instance.uso:
                self.fields['uso'].initial = self.instance.uso
            if self.instance.clase:
                self.fields['clase'].initial = self.instance.clase
        
        # Nota: El campo 'empresa' se asigna automáticamente en la vista, no está en el formulario
        # Hacer calidad requerida y costo opcional
        self.fields['calidad'].required = True
        self.fields['costo'].required = False

class CatastroLoginForm(forms.Form):
    """
    Formulario de login específico para el módulo de catastro
    """
    usuario = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'required': True
        }),
        label="Usuario"
    )
    
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'required': True
        }),
        label="Contraseña"
    )
    
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all().order_by('codigo'),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        label="Municipio",
        empty_label="Seleccione un municipio"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el queryset para mostrar código y descripción
        self.fields['municipio'].queryset = Municipio.objects.all().order_by('codigo')
        self.fields['municipio'].label_from_instance = lambda obj: f"{obj.codigo} - {obj.descripcion}"
    
    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        password = cleaned_data.get('password')
        municipio = cleaned_data.get('municipio')
        
        if not usuario:
            raise forms.ValidationError("El usuario es obligatorio")
        
        if not password:
            raise forms.ValidationError("La contraseña es obligatoria")
        
        if not municipio:
            raise forms.ValidationError("Debe seleccionar un municipio")
        
        return cleaned_data

class EdificacionEspecialForm(forms.ModelForm):
    """Formulario para crear una edificación especial con valor estimado"""
    
    class Meta:
        model = Edificacion
        fields = ['descripcion', 'edifino', 'piso', 'uso', 'clase', 'calidad', 'totedi', 'usuario', 'fechasys']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Ingrese la descripción de la edificación especial',
                'required': True
            }),
            'edifino': forms.NumberInput(attrs={
                'class': 'form-control text-end',
                'step': '1',
                'min': '0',
                'max': '999',
                'required': True
            }),
            'piso': forms.NumberInput(attrs={
                'class': 'form-control text-end',
                'step': '1',
                'min': '0',
                'max': '99',
                'required': True
            }),
            'uso': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '1',
                'readonly': True,
                'value': 'E'
            }),
            'clase': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '2',
                'readonly': True
            }),
            'calidad': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '2',
                'readonly': True
            }),
            'totedi': forms.NumberInput(attrs={
                'class': 'form-control text-end',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fechasys': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'descripcion': 'Descripción',
            'edifino': 'No. Edificación',
            'piso': 'Piso',
            'uso': 'Uso',
            'clase': 'Clase',
            'calidad': 'Calidad',
            'totedi': 'Total Edificación (Valor Estimado)',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        # Establecer valores por defecto
        self.fields['uso'].initial = 'E'
        self.fields['clase'].initial = ''
        self.fields['calidad'].initial = ''
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fechasys'].initial = fecha_sistema
        
        # Campos de solo lectura
        self.fields['uso'].required = False
        self.fields['clase'].required = False
        self.fields['calidad'].required = False
        self.fields['usuario'].required = False
        self.fields['fechasys'].required = False

class DetalleAdicionalesForm(forms.ModelForm):
    """Formulario para el modelo DetalleAdicionales"""
    
    # Campo código como CharField (texto) para búsqueda automática
    # Permite búsqueda por código o descripción (texto), pero al guardar solo se guarda el código (6 caracteres)
    codigo = forms.CharField(
        max_length=50,  # Aumentado para permitir búsquedas por texto/descripción
        required=False,
        label='Código',
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'placeholder': 'Ingrese código o descripción y busque'})
    )
    
    class Meta:
        model = DetalleAdicionales
        fields = ['empresa', 'clave', 'codigo', 'area', 'porce', 'unit', 'total', 'descripcion', 'edifino', 'piso', 'codedi', 'fraccion', 'valuedi', 'usuario', 'fechasys']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'clave': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '14', 'readonly': True}),
            'area': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'porce': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'unit': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'total': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0', 'readonly': True}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '30'}),
            'edifino': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999'}),
            'piso': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '99'}),
            'codedi': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4'}),
            'fraccion': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0', 'readonly': True}),
            'valuedi': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0', 'readonly': True}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'maxlength': '50'}),
            'fechasys': forms.DateTimeInput(
                attrs={'class': 'form-control', 'readonly': True, 'type': 'text'},
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'empresa': 'Empresa',
            'clave': 'Clave Catastral',
            'area': 'Área',
            'porce': 'Porcentaje (%)',
            'unit': 'Valor Unitario',
            'total': 'Total',
            'descripcion': 'Descripción',
            'codedi': 'Código Edific.',
            'fraccion': 'Fracción',
            'valuedi': 'Valor Unit Edif. M2',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
        }
    
    def __init__(self, *args, **kwargs):
        # Obtener empresa, clave, usuario y fecha del contexto si están disponibles
        empresa = kwargs.pop('empresa', None)
        clave = kwargs.pop('clave', None)
        usuario = kwargs.pop('usuario', None)
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        super().__init__(*args, **kwargs)
        
        # Establecer valores iniciales si se proporcionan
        if empresa:
            self.fields['empresa'].initial = empresa
        if clave:
            self.fields['clave'].initial = clave
        
        # Inicializar usuario y fecha sistema si se proporcionan (para nuevos registros)
        if usuario is not None:
            self.fields['usuario'].initial = usuario
        elif not self.instance.pk:  # Si es un nuevo registro y no se proporcionó usuario
            # Intentar obtener del request si está disponible en el contexto
            pass
        
        if fecha_sistema is not None:
            # Formatear la fecha para mostrarla en el campo
            from django.utils import timezone
            from datetime import datetime
            if isinstance(fecha_sistema, (timezone.datetime, datetime)):
                # Si es un objeto datetime, formatearlo
                if isinstance(fecha_sistema, timezone.datetime):
                    self.fields['fechasys'].initial = fecha_sistema.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    self.fields['fechasys'].initial = fecha_sistema.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # Si ya es un string, usarlo directamente
                self.fields['fechasys'].initial = fecha_sistema
        elif not self.instance.pk:  # Si es un nuevo registro y no se proporcionó fecha
            # Establecer fecha actual
            from django.utils import timezone
            self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Hacer todos los campos opcionales excepto los requeridos
        for field_name, field in self.fields.items():
            if field_name not in ['empresa', 'clave', 'usuario', 'fechasys']:
                field.required = False
        
        # Configurar campos fraccion y valuedi como readonly y opcionales
        if 'fraccion' in self.fields:
            self.fields['fraccion'].required = False
            self.fields['fraccion'].widget.attrs['readonly'] = True
        if 'valuedi' in self.fields:
            self.fields['valuedi'].required = False
            self.fields['valuedi'].widget.attrs['readonly'] = True
        
        # Configurar campos de solo lectura
        if 'usuario' in self.fields:
            self.fields['usuario'].widget.attrs['readonly'] = True
        if 'fechasys' in self.fields:
            self.fields['fechasys'].widget.attrs['readonly'] = True
        if 'total' in self.fields:
            self.fields['total'].widget.attrs['readonly'] = True
        
        # Si hay una instancia existente, establecer el valor inicial del código
        if self.instance and self.instance.pk and self.instance.codigo:
            self.fields['codigo'].initial = self.instance.codigo
    
    def clean(self):
        """Validar y calcular total automáticamente"""
        from decimal import Decimal
        cleaned_data = super().clean()
        
        # Asegurar que codedi sea un string válido (puede venir vacío o con valor)
        if 'codedi' in cleaned_data:
            codedi_value = cleaned_data.get('codedi')
            if codedi_value:
                # Convertir a string, limpiar espacios y limitar a 4 caracteres
                cleaned_data['codedi'] = str(codedi_value).strip()[:4]
            else:
                # Si está vacío, establecer como None para que se guarde como NULL
                cleaned_data['codedi'] = None
        
        # Calcular total si hay área, porcentaje y valor unitario
        area = cleaned_data.get('area', Decimal('0.00'))
        porce = cleaned_data.get('porce', Decimal('0.00'))
        unit = cleaned_data.get('unit', Decimal('0.00'))
        
        if area and porce and unit:
            # Calcular: Total = Valor Unitario * Área * Porcentaje (%)
            # Nota: El porcentaje se divide entre 100 para convertirlo a decimal
            try:
                total = unit * area * (porce / Decimal('100'))
                cleaned_data['total'] = total.quantize(Decimal('0.01'))
            except (ValueError, TypeError, InvalidOperation):
                cleaned_data['total'] = Decimal('0.00')
        else:
            cleaned_data['total'] = Decimal('0.00')
        
        # Asignar valores por defecto a campos vacíos
        campos_defaults = {
            'area': Decimal('0.00'),
            'porce': Decimal('0.00'),
            'unit': Decimal('0.00'),
            'total': Decimal('0.00'),
            'edifino': Decimal('0'),
            'piso': Decimal('0'),
            'fraccion': Decimal('0.00'),
            'valuedi': Decimal('0.00'),
            'empresa': cleaned_data.get('empresa', ''),
            'clave': cleaned_data.get('clave', ''),
        }
        
        for campo, valor_default in campos_defaults.items():
            if campo not in cleaned_data or cleaned_data[campo] is None or cleaned_data[campo] == '':
                cleaned_data[campo] = valor_default
        
        return cleaned_data

class BarriosForm(forms.ModelForm):
    """Formulario para el modelo Barrios"""
    
    class Meta:
        model = Barrios
        fields = ['empresa', 'codbarrio', 'descripcion', 'tipica']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'codbarrio': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '8'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '29'}),
            'tipica': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'empresa': 'Empresa',
            'codbarrio': 'Código Barrio',
            'descripcion': 'Descripción',
            'tipica': 'Tipología',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        # Establecer empresa si se proporciona
        if empresa:
            self.fields['empresa'].initial = empresa
        # Hacer campos requeridos
        self.fields['codbarrio'].required = True

class TopografiaForm(forms.ModelForm):
    """Formulario para el modelo Topografia"""
    
    class Meta:
        model = Topografia
        fields = ['empresa', 'cotopo', 'descritopo', 'factopo']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'cotopo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'descritopo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '40'}),
            'factopo': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'empresa': 'Empresa',
            'cotopo': 'Código Topografía *',
            'descritopo': 'Descripción *',
            'factopo': 'Factor Topografía *',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        # Establecer empresa si se proporciona
        if empresa:
            self.fields['empresa'].initial = empresa
        # Hacer campos requeridos
        self.fields['cotopo'].required = True
        self.fields['descritopo'].required = True
        self.fields['factopo'].required = True


class UsosPredioForm(forms.ModelForm):
    """Catálogo de usos del predio (tabla usos). Base para sub usos y demás referencias."""

    class Meta:
        model = Usos
        fields = ['uso', 'desuso']
        widgets = {
            'uso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3', 'autocomplete': 'off'}),
            'desuso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '34'}),
        }
        labels = {
            'uso': 'Código de uso',
            'desuso': 'Descripción del uso',
        }

    def __init__(self, *args, **kwargs):
        uso_readonly = kwargs.pop('uso_readonly', False)
        super().__init__(*args, **kwargs)
        self.fields['uso'].required = True
        self.fields['desuso'].required = True
        if uso_readonly and 'uso' in self.fields:
            self.fields['uso'].widget.attrs['readonly'] = True

    def clean_uso(self):
        raw = (self.cleaned_data.get('uso') or '').strip()
        if not raw:
            raise forms.ValidationError('El código de uso es obligatorio.')
        return raw[:3]

    def clean_desuso(self):
        return (self.cleaned_data.get('desuso') or '').strip()[:34]


class ValorArbolForm(forms.ModelForm):
    """Formulario para el modelo ValorArbol"""
    
    class Meta:
        model = ValorArbol
        fields = ['empresa', 'codigo', 'descripcion', 'valor']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '6', 'id': 'id_codigo_valor_arbol'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'empresa': 'Empresa',
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'valor': 'Valor',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        # Establecer empresa si se proporciona
        if empresa:
            self.fields['empresa'].initial = empresa
        # Hacer campos requeridos
        self.fields['codigo'].required = True
        self.fields['descripcion'].required = True
        self.fields['valor'].required = True
    
    def clean(self):
        """
        Validar que no exista un registro con la misma empresa y código
        Si existe y estamos creando (no editando), no lanzar error aquí,
        la vista se encargará de redirigir a la edición
        """
        cleaned_data = super().clean()
        
        # Solo validar si estamos creando un nuevo registro (no editando)
        if not self.instance.pk:
            empresa = cleaned_data.get('empresa', '').strip()
            codigo = cleaned_data.get('codigo', '').strip()
            
            if empresa and codigo:
                # Verificar si ya existe un registro con la misma empresa y código
                from .models import ValorArbol
                valor_arbol_existente = ValorArbol.objects.filter(
                    empresa=empresa,
                    codigo=codigo
                ).first()
                
                if valor_arbol_existente:
                    # No lanzar error aquí, la vista se encargará de redirigir
                    # Solo agregar información al cleaned_data para que la vista la use
                    cleaned_data['_valor_arbol_existente_id'] = valor_arbol_existente.id
        
        return cleaned_data

class FactorCultivoForm(forms.ModelForm):
    """Formulario para el modelo FactorCultivo"""
    
    # Campos adicionales de solo lectura para mostrar información del cultivo
    descripcion_cultivo = forms.CharField(
        required=False,
        label='Descripción del Cultivo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'id': 'id_descripcion_cultivo',
            'placeholder': 'Se completa automáticamente'
        })
    )
    
    valor_cultivo = forms.DecimalField(
        required=False,
        label='Valor del Cultivo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control text-end',
            'readonly': True,
            'id': 'id_valor_cultivo',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    
    class Meta:
        model = FactorCultivo
        fields = ['empresa', 'codigo', 'rango1', 'rango2', 'factor']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '6', 'id': 'id_codigo_cultivo', 'readonly': True}),
            'rango1': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '9999'}),
            'rango2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '9999'}),
            'factor': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.001', 'min': '0', 'max': '999.999'}),
        }
        labels = {
            'empresa': 'Empresa',
            'codigo': 'Código Cultivo',
            'rango1': 'Rango 1',
            'rango2': 'Rango 2',
            'factor': 'Factor',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        codigo_cultivo = kwargs.pop('codigo_cultivo', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa si se proporciona
        if empresa:
            self.fields['empresa'].initial = empresa
        
        # Si se proporciona código de cultivo, cargar información del cultivo
        if codigo_cultivo:
            self.fields['codigo'].initial = codigo_cultivo
            try:
                from .models import ValorArbol
                valor_arbol = ValorArbol.objects.filter(
                    empresa=empresa,
                    codigo=codigo_cultivo
                ).first()
                if valor_arbol:
                    self.fields['descripcion_cultivo'].initial = valor_arbol.descripcion or ''
                    self.fields['valor_cultivo'].initial = valor_arbol.valor or 0.00
            except Exception:
                pass
        
        # Hacer campos requeridos
        self.fields['codigo'].required = True
        self.fields['rango1'].required = True
        self.fields['rango2'].required = True
        self.fields['factor'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        rango1 = cleaned_data.get('rango1')
        rango2 = cleaned_data.get('rango2')
        
        # Validar que rango2 sea mayor o igual a rango1
        if rango1 is not None and rango2 is not None:
            if rango2 < rango1:
                raise forms.ValidationError({
                    'rango2': 'El Rango 2 debe ser mayor o igual al Rango 1'
                })
        
        return cleaned_data

class TierraRuralForm(forms.ModelForm):
    """Formulario para valores de tierra rural (FactoresRiego)"""
    
    class Meta:
        model = FactoresRiego
        fields = ['empresa', 'codigo', 'descripcion', 'valor']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3', 'id': 'id_codigo_tierra'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '45'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0', 'max': '9999999999.99'}),
        }
        labels = {
            'empresa': 'Empresa',
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'valor': 'Valor',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa si se proporciona
        if empresa:
            self.fields['empresa'].initial = empresa
        
        # Hacer campos requeridos
        self.fields['codigo'].required = True
        self.fields['descripcion'].required = True
        self.fields['valor'].required = True
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').strip()
        if len(codigo) > 3:
            raise forms.ValidationError('El código no puede tener más de 3 caracteres.')
        return codigo

class CultivoPermanenteForm(forms.ModelForm):
    """Formulario para el modelo CultivoPermanente"""
    
    # Campo adicional de solo lectura para mostrar información del cultivo
    descripcion_clase = forms.CharField(
        required=False,
        label='Descripción de la Clase',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'id': 'id_descripcion_clase',
            'placeholder': 'Se completa automáticamente'
        })
    )
    
    valor_cultivo = forms.DecimalField(
        required=False,
        label='Valor del Cultivo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control text-end',
            'readonly': True,
            'id': 'id_valor_cultivo',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    
    class Meta:
        model = CultivoPermanente
        fields = ['empresa', 'clave', 'clase', 'arbol', 'estado', 'edad', 'factor', 'valor']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'clave': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20', 'readonly': True}),
            'arbol': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '9999999'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999'}),
            'factor': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': 'any', 'min': '0'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0', 'max': '9999999999.99'}),
        }
        labels = {
            'empresa': 'Empresa',
            'clave': 'Clave Catastral',
            'clase': 'Clase de Cultivo y Variedad',
            'arbol': 'Numero Arboles',
            'estado': 'Estado Fitosanitario',
            'edad': 'Edad',
            'factor': 'Factor de Modificación',
            'valor': 'Valor Cultivo',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        clave = kwargs.pop('clave', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa y clave: SIEMPRE priorizar valores de la instancia si existe
        if self.instance and self.instance.pk:
            # Si hay una instancia (edición), FORZAR los valores de la instancia
            # CRÍTICO: Usar los valores directamente de la instancia, no de initial
            if self.instance.empresa:
                # Forzar el valor en el widget directamente
                self.fields['empresa'].widget.attrs['value'] = str(self.instance.empresa)
                self.fields['empresa'].initial = self.instance.empresa
                self.initial['empresa'] = self.instance.empresa
            if self.instance.clave:
                # Forzar el valor en el widget directamente
                self.fields['clave'].widget.attrs['value'] = str(self.instance.clave)
                self.fields['clave'].initial = self.instance.clave
                self.initial['clave'] = self.instance.clave
        else:
            # Si no hay instancia (nuevo), usar los parámetros proporcionados
            if empresa:
                self.fields['empresa'].initial = empresa
                self.fields['empresa'].widget.attrs['value'] = str(empresa)
                self.initial['empresa'] = empresa
            if clave:
                self.fields['clave'].initial = clave
                self.fields['clave'].widget.attrs['value'] = str(clave)
                self.initial['clave'] = clave
        
        # Cambiar el campo clase a ModelChoiceField con ValorArbol filtrado por empresa
        from .models import ValorArbol
        
        # Obtener empresa para filtrar: priorizar instancia, luego parámetro
        empresa_para_filtro = None
        if self.instance and self.instance.pk and self.instance.empresa:
            empresa_para_filtro = self.instance.empresa
        elif empresa:
            empresa_para_filtro = empresa
        
        # Si hay una instancia con clase, buscar el ValorArbol correspondiente SOLO por código
        valor_arbol_initial = None
        if self.instance and self.instance.pk and self.instance.clase:
            try:
                # Extraer solo el código si el campo clase contiene más información
                codigo_clase = str(self.instance.clase).strip()
                # Si contiene "-" o espacios, tomar solo la primera parte (código)
                if '-' in codigo_clase:
                    codigo_clase = codigo_clase.split('-')[0].strip()
                elif ' ' in codigo_clase:
                    codigo_clase = codigo_clase.split()[0].strip()
                
                empresa_busqueda = self.instance.empresa or empresa_para_filtro or empresa
                # Buscar SOLO por código, no por descripción
                valor_arbol_initial = ValorArbol.objects.filter(
                    empresa=empresa_busqueda,
                    codigo=codigo_clase
                ).first()
            except Exception:
                pass
        
        # Crear queryset filtrado por empresa
        # Si hay un valor_arbol_initial, asegurarse de que esté incluido en el queryset
        from django.db.models import Q
        if empresa_para_filtro:
            if valor_arbol_initial:
                # Incluir el objeto inicial aunque no coincida con el filtro de empresa
                queryset = ValorArbol.objects.filter(
                    Q(empresa=empresa_para_filtro) | Q(pk=valor_arbol_initial.pk)
                )
            else:
                queryset = ValorArbol.objects.filter(empresa=empresa_para_filtro)
        else:
            if valor_arbol_initial:
                queryset = ValorArbol.objects.filter(Q(pk=valor_arbol_initial.pk))
            else:
                queryset = ValorArbol.objects.all()
        
        queryset = queryset.order_by('codigo')
        
        # Reemplazar el campo clase con ModelChoiceField
        # Usar to_field_name='codigo' para que el valor guardado sea el código, no el ID
        self.fields['clase'] = forms.ModelChoiceField(
            queryset=queryset,
            required=True,
            label='Clase de Cultivo y Variedad',
            widget=forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_clase_cultivo'
            }),
            empty_label='Seleccione una clase de cultivo...',
            to_field_name='codigo'  # Esto hace que el valor guardado sea el código, no el ID
        )
        
        # Establecer el valor inicial si existe (usando el código)
        if valor_arbol_initial:
            # Establecer el initial usando el código, no el objeto completo
            self.fields['clase'].initial = valor_arbol_initial.codigo
        
        # Reemplazar el campo estado con ChoiceField
        self.fields['estado'] = forms.ChoiceField(
            choices=[
                ('', 'Seleccione un estado...'),
                ('1', '1 - Bueno'),
                ('2', '2 - Regular'),
                ('3', '3 - Malo'),
            ],
            required=True,
            label='Estado Fitosanitario',
            widget=forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_estado_cultivo'
            })
        )
        
        # Agregar campo temporal valorarbol (solo lectura)
        self.fields['valorarbol'] = forms.DecimalField(
            required=False,
            label='Valor por Árbol',
            widget=forms.NumberInput(attrs={
                'class': 'form-control text-end',
                'readonly': True,
                'step': '0.01',
                'id': 'id_valorarbol'
            }),
            initial=0.00
        )
        
        # Agregar campo temporal factor_estado (solo lectura)
        self.fields['factor_estado'] = forms.DecimalField(
            required=False,
            label='Factor Estado',
            widget=forms.NumberInput(attrs={
                'class': 'form-control text-end',
                'readonly': True,
                'step': '0.01',
                'id': 'id_factor_estado'
            }),
            initial=0.00
        )
        
        # Agregar campo temporal factor_edad (solo lectura)
        self.fields['factor_edad'] = forms.DecimalField(
            required=False,
            label='Factor Edad',
            widget=forms.NumberInput(attrs={
                'class': 'form-control text-end',
                'readonly': True,
                'step': 'any',
                'id': 'id_factor_edad'
            }),
            initial=0.00
        )
        
        # Si hay una instancia existente, establecer TODOS los valores iniciales de campos temporales
        if self.instance and self.instance.pk:
            try:
                # 1. Inicializar campos relacionados con ValorArbol (clase)
                if self.instance.clase:
                    # Extraer solo el código si contiene más información
                    codigo_clase = str(self.instance.clase).strip()
                    if '-' in codigo_clase:
                        codigo_clase = codigo_clase.split('-')[0].strip()
                    elif ' ' in codigo_clase:
                        codigo_clase = codigo_clase.split()[0].strip()
                    
                    empresa_busqueda = self.instance.empresa or empresa_para_filtro or empresa
                    valor_arbol = ValorArbol.objects.filter(
                        empresa=empresa_busqueda,
                        codigo=codigo_clase
                    ).first()
                    if valor_arbol:
                        # Establecer campos relacionados con ValorArbol
                        self.fields['descripcion_clase'].initial = valor_arbol.descripcion or ''
                        self.fields['valorarbol'].initial = valor_arbol.valor or 0.00
                        # valor_cultivo se calculará después con factor_estado y factor_edad
                
                # 2. Inicializar factor_estado según el estado existente
                if self.instance.estado:
                    estado = str(self.instance.estado).strip()
                    if estado == '1':
                        self.fields['factor_estado'].initial = 1.00
                    elif estado == '2':
                        self.fields['factor_estado'].initial = 0.70
                    elif estado == '3':
                        self.fields['factor_estado'].initial = 0.40
                    else:
                        self.fields['factor_estado'].initial = 0.00
                
                # 3. Inicializar factor_edad desde FactorCultivo
                if self.instance.clase and self.instance.edad:
                    # Extraer solo el código
                    codigo_clase = str(self.instance.clase).strip()
                    if '-' in codigo_clase:
                        codigo_clase = codigo_clase.split('-')[0].strip()
                    elif ' ' in codigo_clase:
                        codigo_clase = codigo_clase.split()[0].strip()
                    
                    empresa_busqueda = self.instance.empresa or empresa_para_filtro or empresa
                    edad_valor = float(self.instance.edad) if self.instance.edad else 0
                    
                    # Buscar FactorCultivo donde edad >= rango1 AND edad <= rango2
                    from .models import FactorCultivo
                    factor_cultivo = FactorCultivo.objects.filter(
                        empresa=empresa_busqueda,
                        codigo=codigo_clase,
                        rango1__lte=edad_valor,
                        rango2__gte=edad_valor
                    ).first()
                    
                    if factor_cultivo:
                        self.fields['factor_edad'].initial = factor_cultivo.factor or 0.00
                    else:
                        self.fields['factor_edad'].initial = 0.00
                
                # 4. Cargar valores directamente desde la BD (NO recalcular al editar)
                # Factor de Modificación (factor) - usar el valor guardado directamente
                if self.instance.factor:
                    self.fields['factor'].initial = float(self.instance.factor) if self.instance.factor else 0.00
                
                # Valor Cultivo (valor) - usar el valor guardado directamente
                if self.instance.valor:
                    self.fields['valor'].initial = float(self.instance.valor) if self.instance.valor else 0.00
                    # También establecer valor_cultivo para mostrar en el campo temporal
                    self.fields['valor_cultivo'].initial = float(self.instance.valor) if self.instance.valor else 0.00
                else:
                    self.fields['valor_cultivo'].initial = 0.00
                    
            except Exception as e:
                # En caso de error, establecer valores por defecto
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error al inicializar campos temporales: {str(e)}", exc_info=True)
                pass
        
        # Hacer campos requeridos
        self.fields['clave'].required = True
        self.fields['arbol'].required = True
        self.fields['edad'].required = True
        self.fields['factor'].required = True
        self.fields['valor'].required = True
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # IMPORTANTE: Preservar empresa y clave si ya existen en la instancia
        # Esto es crítico para evitar que se cambien durante la edición
        empresa_original = None
        clave_original = None
        if instance.pk:
            # Si es una edición, guardar los valores originales
            empresa_original = instance.empresa
            clave_original = instance.clave
        
        # Asegurar que clase sea SOLO el código (string) y no el objeto ValorArbol
        # Con to_field_name='codigo', el cleaned_data ya contiene el código directamente
        clase = self.cleaned_data.get('clase')
        if clase:
            # Con to_field_name='codigo', clase ya es el código (string), no el objeto
            if isinstance(clase, str):
                # Asegurarse de que sea solo el código (sin descripción)
                # Si contiene "-" o espacios, tomar solo la primera parte (código)
                codigo_limpio = clase.split('-')[0].split()[0].strip() if '-' in clase or ' ' in clase else clase.strip()
                instance.clase = codigo_limpio
            elif hasattr(clase, 'codigo'):
                # Si por alguna razón es un objeto, extraer solo el código
                instance.clase = str(clase.codigo).strip()
            else:
                # Cualquier otro caso, convertir a string y limpiar
                codigo_limpio = str(clase).split('-')[0].split()[0].strip() if '-' in str(clase) or ' ' in str(clase) else str(clase).strip()
                instance.clase = codigo_limpio
        
        # RESTAURAR empresa y clave si se están editando (protección adicional)
        if instance.pk and empresa_original:
            instance.empresa = empresa_original
        if instance.pk and clave_original:
            instance.clave = clave_original
        
        if commit:
            instance.save()
        return instance

class ComentariosCatastroForm(forms.ModelForm):
    """Formulario para comentarios de catastro"""
    
    class Meta:
        model = ComentariosCatastro
        fields = ['comentario', 'usuario', 'fecha']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Ingrese el comentario...',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'comentario': 'Comentario',
            'usuario': 'Usuario',
            'fecha': 'Fecha',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fecha'].initial = fecha_sistema
        
        self.fields['usuario'].required = False
        self.fields['fecha'].required = False

class TipoMaterialForm(forms.ModelForm):
    """Formulario para el modelo TipoMaterial"""
    
    class Meta:
        model = TipoMaterial
        fields = ['No', 'descripcion']
        widgets = {
            'No': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '45'}),
        }
        labels = {
            'No': 'Número *',
            'descripcion': 'Descripción *',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos requeridos
        self.fields['No'].required = True
        self.fields['descripcion'].required = True

class ConfiTipologiaForm(forms.ModelForm):
    """Formulario para el modelo ConfiTipologia"""
    
    class Meta:
        model = ConfiTipologia
        fields = ['uso', 'clase', 'tipo', 'categoria', 'descripcion', 'peso']
        widgets = {
            'uso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'clase': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '1'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '1'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0'}),
        }
        labels = {
            'uso': 'Uso',
            'clase': 'Clase',
            'tipo': 'Tipo',
            'categoria': 'Categoría',
            'descripcion': 'Descripción',
            'peso': 'Peso',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos requeridos
        self.fields['uso'].required = True
        self.fields['clase'].required = True

class EspecificacionesForm(forms.ModelForm):
    """Formulario para el modelo Especificaciones"""
    
    class Meta:
        model = Especificaciones
        fields = [
            'clave', 'piso', 'edifino', 'uso', 'clase',
            'codfun', 'descrifun', 'pesofun',
            'codpiso', 'descripiso', 'pesopiso',
            'codparext', 'descriparext', 'pesoparext',
            'codtecho', 'descritecho', 'pesotecho',
            'codparint', 'descriparint', 'pesoparint',
            'codcielo', 'descricielo', 'pesocielo',
            'codcarpenti', 'descricarpenti', 'pesocarpini',
            'codelectri', 'descrielectri', 'pesoelectri',
            'codplome', 'descriplome', 'pesoplome',
            'codotros', 'descriotros', 'pesotros',
            'usuario', 'fechasys', 'pesos', 'calidad'
        ]
        widgets = {
            'clave': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '14', 'readonly': True}),
            'piso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '1'}),
            'edifino': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '99999999999'}),
            'uso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '1'}),
            'clase': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            
            'codfun': forms.Select(attrs={'class': 'form-select', 'id': 'id_codfun'}),
            'descrifun': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesofun': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codpiso': forms.Select(attrs={'class': 'form-select', 'id': 'id_codpiso'}),
            'descripiso': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesopiso': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codparext': forms.Select(attrs={'class': 'form-select', 'id': 'id_codparext'}),
            'descriparext': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesoparext': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codtecho': forms.Select(attrs={'class': 'form-select', 'id': 'id_codtecho'}),
            'descritecho': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesotecho': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codparint': forms.Select(attrs={'class': 'form-select', 'id': 'id_codparint'}),
            'descriparint': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesoparint': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codcielo': forms.Select(attrs={'class': 'form-select', 'id': 'id_codcielo'}),
            'descricielo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesocielo': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codcarpenti': forms.Select(attrs={'class': 'form-select', 'id': 'id_codcarpenti'}),
            'descricarpenti': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesocarpini': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codelectri': forms.Select(attrs={'class': 'form-select', 'id': 'id_codelectri'}),
            'descrielectri': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesoelectri': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codplome': forms.Select(attrs={'class': 'form-select', 'id': 'id_codplome'}),
            'descriplome': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesoplome': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'codotros': forms.Select(attrs={'class': 'form-select', 'id': 'id_codotros'}),
            'descriotros': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100', 'readonly': True}),
            'pesotros': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'max': '999', 'readonly': True}),
            
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'readonly': True}),
            'fechasys': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True}),
            'pesos': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '1', 'min': '0', 'readonly': True}),
            'calidad': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3', 'readonly': True}),
        }
        labels = {
            'clave': 'Clave Catastral',
            'piso': 'Piso',
            'edifino': 'No. Edif. *',
            'uso': 'Uso',
            'clase': 'Clase',
            'codfun': 'Código FUNDICIONES',
            'descrifun': 'Descripción FUNDICIONES',
            'pesofun': 'Peso FUNDICIONES',
            'codpiso': 'Código Piso',
            'descripiso': 'Descripción Piso',
            'pesopiso': 'Peso Piso',
            'codparext': 'Código Pared Ext.',
            'descriparext': 'Descripción Pared Ext.',
            'pesoparext': 'Peso Pared Ext.',
            'codtecho': 'Código Techo',
            'descritecho': 'Descripción Techo',
            'pesotecho': 'Peso Techo',
            'codparint': 'Código Pared Int.',
            'descriparint': 'Descripción Pared Int.',
            'pesoparint': 'Peso Pared Int.',
            'codcielo': 'Código Cielo',
            'descricielo': 'Descripción Cielo',
            'pesocielo': 'Peso Cielo',
            'codcarpenti': 'Código Carpintería',
            'descricarpenti': 'Descripción Carpintería',
            'pesocarpini': 'Peso Carpintería',
            'codelectri': 'Código Eléctrica',
            'descrielectri': 'Descripción Eléctrica',
            'pesoelectri': 'Peso Eléctrica',
            'codplome': 'Código Plomería',
            'descriplome': 'Descripción Plomería',
            'pesoplome': 'Peso Plomería',
            'codotros': 'Código Otros',
            'descriotros': 'Descripción Otros',
            'pesotros': 'Peso Otros',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
            'pesos': 'Pesos Totales',
            'calidad': 'Calidad',
        }
    
    def __init__(self, *args, **kwargs):
        clave = kwargs.pop('clave', None)
        usuario = kwargs.pop('usuario', None)
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        super().__init__(*args, **kwargs)
        
        if clave:
            self.fields['clave'].initial = clave
        
        if usuario is not None:
            self.fields['usuario'].initial = usuario
        
        if fecha_sistema is not None:
            from django.utils import timezone
            from datetime import datetime
            if isinstance(fecha_sistema, (timezone.datetime, datetime)):
                self.fields['fechasys'].initial = fecha_sistema.strftime('%Y-%m-%d %H:%M:%S')
            else:
                self.fields['fechasys'].initial = fecha_sistema
        
        # Hacer campos requeridos
        self.fields['edifino'].required = True
        
        # Configurar comboboxes con opciones vacías inicialmente (se llenarán con JavaScript)
        self.fields['codfun'].choices = [('', 'Seleccione...')]
        self.fields['codpiso'].choices = [('', 'Seleccione...')]
        self.fields['codparext'].choices = [('', 'Seleccione...')]
        self.fields['codtecho'].choices = [('', 'Seleccione...')]
        self.fields['codparint'].choices = [('', 'Seleccione...')]
        self.fields['codcielo'].choices = [('', 'Seleccione...')]
        self.fields['codcarpenti'].choices = [('', 'Seleccione...')]
        self.fields['codelectri'].choices = [('', 'Seleccione...')]
        self.fields['codplome'].choices = [('', 'Seleccione...')]
        self.fields['codotros'].choices = [('', 'Seleccione...')]
        
        # Hacer campos readonly
        if 'usuario' in self.fields:
            self.fields['usuario'].widget.attrs['readonly'] = True
        if 'fechasys' in self.fields:
            self.fields['fechasys'].widget.attrs['readonly'] = True
        if 'pesos' in self.fields:
            self.fields['pesos'].widget.attrs['readonly'] = True
        if 'calidad' in self.fields:
            self.fields['calidad'].widget.attrs['readonly'] = True

class DetEspecificacionForm(forms.ModelForm):
    """Formulario para el modelo DetEspecificacion"""
    
    # Opciones para pisoestruc (Estructura)
    PISO_ESTRUCTURA_CHOICES = [
        ('1', '1 - Madera'),
        ('2', '2 - Cemento'),
        ('3', '3 - Tierra Apisonada'),
    ]
    
    # Opciones para pisoacabado (Acabado)
    PISO_ACABADO_CHOICES = [
        ('1', '1 - Concreto Color'),
        ('2', '2 - Mosaico'),
        ('3', '3 - Terrazo'),
        ('4', '4 - Ceramica'),
        ('5', '5 - Madera Machimbre'),
        ('6', '6 - Madera Decorativo'),
        ('7', '7 - Marmol'),
        ('8', '8 - Ninguno'),
    ]
    
    # Opciones para pisocalidad (Calidad)
    PISO_CALIDAD_CHOICES = [
        ('1', '1 - INFERIOR'),
        ('2', '2 - REGULAR'),
        ('3', '3 - SUPERIOR'),
    ]
    
    # Convertir campos a ChoiceField
    pisoestruc = forms.ChoiceField(
        choices=PISO_ESTRUCTURA_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Estructura'
    )
    
    pisoacabado = forms.ChoiceField(
        choices=PISO_ACABADO_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Acabado'
    )
    
    pisocalidad = forms.ChoiceField(
        choices=PISO_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Calidad'
    )
    
    # Opciones para Pared Externa - Estructura
    PARED_EXT_ESTRUCTURA_CHOICES = [
        ('1', '1 - Madera'),
        ('2', '2 - Bloque de Concreto'),
        ('3', '3 - Ladrillo Rafon'),
        ('4', '4 - Acero'),
        ('5', '5 - Adobe'),
        ('6', '6 - Bahareque'),
        ('7', '7 - Lamina de Zinc'),
    ]
    
    # Opciones para Pared Externa - Acabado
    PARED_EXT_ACABADO_CHOICES = [
        ('1', '1 - Tabla'),
        ('2', '2 - Madera Botagua'),
        ('3', '3 - Repello Rustico'),
        ('4', '4 - Repello Fino'),
    ]
    
    # Opciones para Pared Externa - Pintura
    PARED_EXT_PINTURA_CHOICES = [
        ('1', '1 - ACEITE'),
        ('2', '2 - AGUA'),
        ('3', '3 - VINILICA'),
    ]
    
    # Opciones para Pared Externa - Calidad
    PARED_EXT_CALIDAD_CHOICES = [
        ('1', '1 - INFERIOR'),
        ('2', '2 - REGULAR'),
        ('3', '3 - SUPERIOR'),
    ]
    
    # Convertir campos de Pared Externa a ChoiceField
    paredextestruc = forms.ChoiceField(
        choices=PARED_EXT_ESTRUCTURA_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Estructura'
    )
    
    paredextacabado = forms.ChoiceField(
        choices=PARED_EXT_ACABADO_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Acabado'
    )
    
    paredextpintura = forms.ChoiceField(
        choices=PARED_EXT_PINTURA_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Pintura'
    )
    
    paredextcalidad = forms.ChoiceField(
        choices=PARED_EXT_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Calidad'
    )
    
    # Opciones para Techo - Tipo
    TECHO_TIPO_CHOICES = [
        ('1', '1 - Media Aguas'),
        ('2', '2 - Dos Aguas'),
        ('3', '3 - Varias Aguas'),
    ]
    
    # Opciones para Techo - Artesón
    TECHO_ARTESON_CHOICES = [
        ('1', '1 - Madera de Pino'),
        ('2', '2 - Concreto'),
        ('3', '3 - Acero'),
    ]
    
    # Opciones para Techo - Acabado
    TECHO_ACABADO_CHOICES = [
        ('1', '1 - Lamina de Zinc'),
        ('2', '2 - Lamina de Adbesto'),
        ('3', '3 - Teja de Barro'),
        ('4', '4 - Teja de Cemento'),
        ('5', '5 - Aluzinc'),
    ]
    
    # Opciones para Techo - Calidad
    TECHO_CALIDAD_CHOICES = [
        ('1', '1 - INFERIOR'),
        ('2', '2 - REGULAR'),
        ('3', '3 - SUPERIOR'),
    ]
    
    # Convertir campos de Techo a ChoiceField
    techotipo = forms.ChoiceField(
        choices=TECHO_TIPO_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Tipo'
    )
    
    techoarteson = forms.ChoiceField(
        choices=TECHO_ARTESON_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Artesón'
    )
    
    techoacabado = forms.ChoiceField(
        choices=TECHO_ACABADO_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Acabado'
    )
    
    techocalidad = forms.ChoiceField(
        choices=TECHO_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Calidad'
    )
    
    # Opciones para Pared Interna - Estructura
    PARED_INT_ESTRUCTURA_CHOICES = [
        ('1', '1 - Madera'),
        ('2', '2 - Concreto'),
        ('3', '3 - Ladrillo Rafon'),
        ('4', '4 - Acero'),
        ('5', '5 - Adobe'),
        ('6', '6 - Bahareque'),
    ]
    
    # Opciones para Pared Interna - Acabado
    PARED_INT_ACABADO_CHOICES = [
        ('1', '1 - Tabla'),
        ('2', '2 - Madera'),
        ('3', '3 - Repello'),
        ('4', '4 - Repello Fino'),
    ]
    
    # Opciones para Pared Interna - Pintura
    PARED_INT_PINTURA_CHOICES = [
        ('1', '1 - ACEITE'),
        ('2', '2 - AGUA'),
        ('3', '3 - VINILICA'),
    ]
    
    # Opciones para Pared Interna - Calidad
    PARED_INT_CALIDAD_CHOICES = [
        ('1', '1 - INFERIOR'),
        ('2', '2 - REGULAR'),
        ('3', '3 - SUPERIOR'),
    ]
    
    # Convertir campos de Pared Interna a ChoiceField
    paredintestruc = forms.ChoiceField(
        choices=PARED_INT_ESTRUCTURA_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Estructura'
    )
    
    paredintacabado = forms.ChoiceField(
        choices=PARED_INT_ACABADO_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Acabado'
    )
    
    paredintpintura = forms.ChoiceField(
        choices=PARED_INT_PINTURA_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Pintura'
    )
    
    paredintacalidad = forms.ChoiceField(
        choices=PARED_INT_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Calidad'
    )
    
    # Opciones para Cielo Raso - Estructura
    CIELO_ESTRUCTURA_CHOICES = [
        ('1', '1 - Madera'),
        ('2', '2 - Cemento Reforzado'),
        ('3', '3 - Pintura'),
    ]
    
    # Opciones para Cielo Raso - Acabado
    CIELO_ACABADO_CHOICES = [
        ('1', '1 - Plywood de Pino'),
        ('2', '2 - Machimbre'),
        ('3', '3 - Aislite'),
        ('4', '4 - Cellotex'),
        ('5', '5 - Adbesto'),
    ]
    
    # Opciones para Cielo Raso - Calidad
    CIELO_CALIDAD_CHOICES = [
        ('1', '1 - INFERIOR'),
        ('2', '2 - REGULAR'),
        ('3', '3 - SUPERIOR'),
    ]
    
    # Convertir campos de Cielo Raso a ChoiceField
    cieloestruc = forms.ChoiceField(
        choices=CIELO_ESTRUCTURA_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Estructura'
    )
    
    cieloacabado = forms.ChoiceField(
        choices=CIELO_ACABADO_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Acabado'
    )
    
    cielocalidad = forms.ChoiceField(
        choices=CIELO_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Calidad'
    )
    
    # Opciones para Electricidad - Alambrado
    ELECTRICIDAD_ALAMBRADO_CHOICES = [
        ('1', '1 - Alambrado Visible'),
        ('2', '2 - Conducto Protector'),
        ('3', '3 - Plastico'),
    ]
    
    # Opciones para Electricidad - Salidas
    ELECTRICIDAD_SALIDAS_CHOICES = [
        ('1', '1 - Pocas'),
        ('2', '2 - Suficientes'),
        ('3', '3 - Abundantes'),
    ]
    
    # Opciones para Electricidad - Calidad
    ELECTRICIDAD_CALIDAD_CHOICES = [
        ('1', '1 - Inferior'),
        ('2', '2 - Regular'),
        ('3', '3 - Superior'),
    ]
    
    # Convertir campos de Electricidad a ChoiceField
    electrialumbrado = forms.ChoiceField(
        choices=ELECTRICIDAD_ALAMBRADO_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Alambrado'
    )
    
    electrisalida = forms.ChoiceField(
        choices=ELECTRICIDAD_SALIDAS_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Salidas'
    )
    
    electricalidad = forms.ChoiceField(
        choices=ELECTRICIDAD_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Calidad'
    )
    
    # Opciones para Plomería - Instalaciones Sanitarias
    PLOMERIA_CALIDAD_CHOICES = [
        ('1', '1 - INFERIOR'),
        ('2', '2 - REGULAR'),
        ('3', '3 - SUPERIOR'),
    ]
    
    # Convertir campos de Plomería a ChoiceField
    inodorocal = forms.ChoiceField(
        choices=PLOMERIA_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Inodoros'
    )
    
    lavamanocal = forms.ChoiceField(
        choices=PLOMERIA_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Lavamanos'
    )
    
    duchacal = forms.ChoiceField(
        choices=PLOMERIA_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Duchas'
    )
    
    lavatrastocal = forms.ChoiceField(
        choices=PLOMERIA_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Lavatrastos'
    )
    
    lavanderocal = forms.ChoiceField(
        choices=PLOMERIA_CALIDAD_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Lavanderos'
    )
    
    class Meta:
        model = DetEspecificacion
        fields = '__all__'
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'clave': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '14'}),
            'edifino': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'piso': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'pisocalidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredextestruc': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredextacabado': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredextcalidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredextpintura': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'techotipo': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'techoarteson': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'techoacabado': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'techocalidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredintestruc': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredintacabado': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredintacalidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'paredintpintura': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'cieloestruc': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'cieloacabado': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'cielocalidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'electrialumbrado': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'electrisalida': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'electricalidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'inodorocal': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'lavamanocal': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'duchacal': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'lavatrastocal': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'lavanderocal': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '9'}),
            'puerta1': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'puerta2': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'puerta3': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'puerta4': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'ventana1': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'ventana2': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'ventana3': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'ventana4': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'closet1': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'closet2': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'closet3': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'closet4': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'gabinete1': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'gabinete2': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'gabinete3': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'gabinete4': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'readonly': True}),
            'fechasys': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'type': 'datetime-local'}),
        }
        labels = {
            'empresa': 'Empresa',
            'clave': 'Clave Catastral *',
            'edifino': 'No. Edificación *',
            'piso': 'Piso',
            'pisocalidad': 'Piso Calidad',
            'paredextestruc': 'Pared Ext. Estructura',
            'paredextacabado': 'Pared Ext. Acabado',
            'paredextcalidad': 'Pared Ext. Calidad',
            'paredextpintura': 'Pared Ext. Pintura',
            'techotipo': 'Techo Tipo',
            'techoarteson': 'Techo Artesón',
            'techoacabado': 'Techo Acabado',
            'techocalidad': 'Techo Calidad',
            'paredintestruc': 'Pared Int. Estructura',
            'paredintacabado': 'Pared Int. Acabado',
            'paredintacalidad': 'Pared Int. Calidad',
            'paredintpintura': 'Pared Int. Pintura',
            'cieloestruc': 'Cielo Estructura',
            'cieloacabado': 'Cielo Acabado',
            'cielocalidad': 'Cielo Calidad',
            'electrialumbrado': 'Eléctrica Alumbrado',
            'electrisalida': 'Eléctrica Salida',
            'electricalidad': 'Eléctrica Calidad',
            'inodorocal': 'Inodoro Calidad',
            'lavamanocal': 'Lavamanos Calidad',
            'duchacal': 'Ducha Calidad',
            'lavatrastocal': 'Lavatrapos Calidad',
            'lavanderocal': 'Lavandero Calidad',
            'puerta1': 'Puerta 1',
            'puerta2': 'Puerta 2',
            'puerta3': 'Puerta 3',
            'puerta4': 'Puerta 4',
            'ventana1': 'Ventana 1',
            'ventana2': 'Ventana 2',
            'ventana3': 'Ventana 3',
            'ventana4': 'Ventana 4',
            'closet1': 'Closet 1',
            'closet2': 'Closet 2',
            'closet3': 'Closet 3',
            'closet4': 'Closet 4',
            'gabinete1': 'Gabinete 1',
            'gabinete2': 'Gabinete 2',
            'gabinete3': 'Gabinete 3',
            'gabinete4': 'Gabinete 4',
            'usuario': 'Usuario',
            'fechasys': 'Fecha de Registro',
            'empresa': 'Municipio',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clave'].required = True
        self.fields['edifino'].required = True
        
        # Hacer el campo empresa readonly y cambiar label a Municipio
        self.fields['empresa'].widget.attrs['readonly'] = True
        self.fields['empresa'].label = 'Municipio'
        
        # Convertir valores numéricos a string para los ChoiceField
        if self.instance and self.instance.pk:
            if self.instance.pisoestruc is not None:
                try:
                    self.fields['pisoestruc'].initial = str(int(self.instance.pisoestruc))
                except (ValueError, TypeError):
                    pass
            if self.instance.pisoacabado is not None:
                try:
                    self.fields['pisoacabado'].initial = str(int(self.instance.pisoacabado))
                except (ValueError, TypeError):
                    pass
            if self.instance.pisocalidad is not None:
                try:
                    self.fields['pisocalidad'].initial = str(int(self.instance.pisocalidad))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredextestruc is not None:
                try:
                    self.fields['paredextestruc'].initial = str(int(self.instance.paredextestruc))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredextacabado is not None:
                try:
                    self.fields['paredextacabado'].initial = str(int(self.instance.paredextacabado))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredextpintura is not None:
                try:
                    self.fields['paredextpintura'].initial = str(int(self.instance.paredextpintura))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredextcalidad is not None:
                try:
                    self.fields['paredextcalidad'].initial = str(int(self.instance.paredextcalidad))
                except (ValueError, TypeError):
                    pass
            if self.instance.techotipo is not None:
                try:
                    self.fields['techotipo'].initial = str(int(self.instance.techotipo))
                except (ValueError, TypeError):
                    pass
            if self.instance.techoarteson is not None:
                try:
                    self.fields['techoarteson'].initial = str(int(self.instance.techoarteson))
                except (ValueError, TypeError):
                    pass
            if self.instance.techoacabado is not None:
                try:
                    self.fields['techoacabado'].initial = str(int(self.instance.techoacabado))
                except (ValueError, TypeError):
                    pass
            if self.instance.techocalidad is not None:
                try:
                    self.fields['techocalidad'].initial = str(int(self.instance.techocalidad))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredintestruc is not None:
                try:
                    self.fields['paredintestruc'].initial = str(int(self.instance.paredintestruc))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredintacabado is not None:
                try:
                    self.fields['paredintacabado'].initial = str(int(self.instance.paredintacabado))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredintpintura is not None:
                try:
                    self.fields['paredintpintura'].initial = str(int(self.instance.paredintpintura))
                except (ValueError, TypeError):
                    pass
            if self.instance.paredintacalidad is not None:
                try:
                    self.fields['paredintacalidad'].initial = str(int(self.instance.paredintacalidad))
                except (ValueError, TypeError):
                    pass
            if self.instance.cieloestruc is not None:
                try:
                    self.fields['cieloestruc'].initial = str(int(self.instance.cieloestruc))
                except (ValueError, TypeError):
                    pass
            if self.instance.cieloacabado is not None:
                try:
                    self.fields['cieloacabado'].initial = str(int(self.instance.cieloacabado))
                except (ValueError, TypeError):
                    pass
            if self.instance.cielocalidad is not None:
                try:
                    self.fields['cielocalidad'].initial = str(int(self.instance.cielocalidad))
                except (ValueError, TypeError):
                    pass
            if self.instance.electrialumbrado is not None:
                try:
                    self.fields['electrialumbrado'].initial = str(int(self.instance.electrialumbrado))
                except (ValueError, TypeError):
                    pass
            if self.instance.electrisalida is not None:
                try:
                    self.fields['electrisalida'].initial = str(int(self.instance.electrisalida))
                except (ValueError, TypeError):
                    pass
            if self.instance.electricalidad is not None:
                try:
                    self.fields['electricalidad'].initial = str(int(self.instance.electricalidad))
                except (ValueError, TypeError):
                    pass
            if self.instance.inodorocal is not None:
                try:
                    self.fields['inodorocal'].initial = str(int(self.instance.inodorocal))
                except (ValueError, TypeError):
                    pass
            if self.instance.lavamanocal is not None:
                try:
                    self.fields['lavamanocal'].initial = str(int(self.instance.lavamanocal))
                except (ValueError, TypeError):
                    pass
            if self.instance.duchacal is not None:
                try:
                    self.fields['duchacal'].initial = str(int(self.instance.duchacal))
                except (ValueError, TypeError):
                    pass
            if self.instance.lavatrastocal is not None:
                try:
                    self.fields['lavatrastocal'].initial = str(int(self.instance.lavatrastocal))
                except (ValueError, TypeError):
                    pass
            if self.instance.lavanderocal is not None:
                try:
                    self.fields['lavanderocal'].initial = str(int(self.instance.lavanderocal))
                except (ValueError, TypeError):
                    pass
        
        # Inicializar fechasys con la fecha actual si es un nuevo registro o mostrar la fecha guardada
        if 'fechasys' in self.fields:
            from django.utils import timezone
            if self.instance and self.instance.pk and self.instance.fechasys:
                # Si hay un registro existente con fecha, formatearla para datetime-local
                fecha = self.instance.fechasys
                if hasattr(fecha, 'strftime'):
                    self.fields['fechasys'].initial = fecha.strftime('%Y-%m-%dT%H:%M')
                else:
                    self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
            else:
                # Si es un nuevo registro, usar la fecha actual
                self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Convertir los valores de ChoiceField de string a Decimal
        if self.cleaned_data.get('pisoestruc'):
            try:
                from decimal import Decimal
                instance.pisoestruc = Decimal(self.cleaned_data['pisoestruc'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('pisoacabado'):
            try:
                from decimal import Decimal
                instance.pisoacabado = Decimal(self.cleaned_data['pisoacabado'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('pisocalidad'):
            try:
                from decimal import Decimal
                instance.pisocalidad = Decimal(self.cleaned_data['pisocalidad'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredextestruc'):
            try:
                from decimal import Decimal
                instance.paredextestruc = Decimal(self.cleaned_data['paredextestruc'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredextacabado'):
            try:
                from decimal import Decimal
                instance.paredextacabado = Decimal(self.cleaned_data['paredextacabado'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredextpintura'):
            try:
                from decimal import Decimal
                instance.paredextpintura = Decimal(self.cleaned_data['paredextpintura'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredextcalidad'):
            try:
                from decimal import Decimal
                instance.paredextcalidad = Decimal(self.cleaned_data['paredextcalidad'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('techotipo'):
            try:
                from decimal import Decimal
                instance.techotipo = Decimal(self.cleaned_data['techotipo'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('techoarteson'):
            try:
                from decimal import Decimal
                instance.techoarteson = Decimal(self.cleaned_data['techoarteson'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('techoacabado'):
            try:
                from decimal import Decimal
                instance.techoacabado = Decimal(self.cleaned_data['techoacabado'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('techocalidad'):
            try:
                from decimal import Decimal
                instance.techocalidad = Decimal(self.cleaned_data['techocalidad'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredintestruc'):
            try:
                from decimal import Decimal
                instance.paredintestruc = Decimal(self.cleaned_data['paredintestruc'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredintacabado'):
            try:
                from decimal import Decimal
                instance.paredintacabado = Decimal(self.cleaned_data['paredintacabado'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredintpintura'):
            try:
                from decimal import Decimal
                instance.paredintpintura = Decimal(self.cleaned_data['paredintpintura'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('paredintacalidad'):
            try:
                from decimal import Decimal
                instance.paredintacalidad = Decimal(self.cleaned_data['paredintacalidad'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('cieloestruc'):
            try:
                from decimal import Decimal
                instance.cieloestruc = Decimal(self.cleaned_data['cieloestruc'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('cieloacabado'):
            try:
                from decimal import Decimal
                instance.cieloacabado = Decimal(self.cleaned_data['cieloacabado'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('cielocalidad'):
            try:
                from decimal import Decimal
                instance.cielocalidad = Decimal(self.cleaned_data['cielocalidad'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('electrialumbrado'):
            try:
                from decimal import Decimal
                instance.electrialumbrado = Decimal(self.cleaned_data['electrialumbrado'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('electrisalida'):
            try:
                from decimal import Decimal
                instance.electrisalida = Decimal(self.cleaned_data['electrisalida'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('electricalidad'):
            try:
                from decimal import Decimal
                instance.electricalidad = Decimal(self.cleaned_data['electricalidad'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('inodorocal'):
            try:
                from decimal import Decimal
                instance.inodorocal = Decimal(self.cleaned_data['inodorocal'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('lavamanocal'):
            try:
                from decimal import Decimal
                instance.lavamanocal = Decimal(self.cleaned_data['lavamanocal'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('duchacal'):
            try:
                from decimal import Decimal
                instance.duchacal = Decimal(self.cleaned_data['duchacal'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('lavatrastocal'):
            try:
                from decimal import Decimal
                instance.lavatrastocal = Decimal(self.cleaned_data['lavatrastocal'])
            except (ValueError, TypeError):
                pass
        if self.cleaned_data.get('lavanderocal'):
            try:
                from decimal import Decimal
                instance.lavanderocal = Decimal(self.cleaned_data['lavanderocal'])
            except (ValueError, TypeError):
                pass
        if commit:
            instance.save()
        return instance

class ComentariosCatastroForm(forms.ModelForm):
    """Formulario para comentarios de catastro"""
    
    class Meta:
        model = ComentariosCatastro
        fields = ['comentario', 'usuario', 'fecha']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Ingrese el comentario...',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'comentario': 'Comentario',
            'usuario': 'Usuario',
            'fecha': 'Fecha',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fecha'].initial = fecha_sistema
        
        self.fields['usuario'].required = False
        self.fields['fecha'].required = False

class BusquedaBienInmuebleForm(forms.Form):
    """
    Formulario para búsqueda de bienes inmuebles
    """
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Clave Catastral, Identidad, Nombres, Apellidos, Clave Segura o Ubicación',
            'autofocus': True
        })
    )

class LegalesForm(forms.ModelForm):
    """Formulario para información legal del predio (Legales)"""
    
    class Meta:
        model = Legales
        fields = ['empresa', 'colegal', 'inscripcion', 'coregistro', 'tomo', 'folio', 'asiento', 'area', 
                  'naturaleza', 'dominio', 'numero', 'linea', 'foto', 'predio2', 'tipo', 'tmed', 
                  'unidad', 'certificacion', 'acta', 'tipopro', 'usuario', 'fechasys']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'colegal': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20', 'required': True}),
            'inscripcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'tomo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '6'}),
            'folio': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '6'}),
            'asiento': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'area': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'linea': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'foto': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4'}),
            'predio2': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4'}),
            'certificacion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'acta': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'readonly': True}),
            'fechasys': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'type': 'text'}),
        }
        labels = {
            'empresa': 'Municipio',
            'colegal': 'Clave Catastral',
            'inscripcion': 'Fecha Inscripción',
            'coregistro': 'Registro / Propiedad',
            'tomo': 'Tomo',
            'folio': 'Folio',
            'asiento': 'Asiento',
            'area': 'Área',
            'naturaleza': 'Naturaleza Juridica',
            'dominio': 'Clase de Dominio',
            'numero': 'Matrícula',
            'linea': 'Línea',
            'foto': 'Foto',
            'predio2': 'Predio',
            'tipo': 'Tipo de Documento',
            'tmed': 'Tipo de Medida',
            'unidad': 'Unidad de Area',
            'certificacion': 'No. Certificacion',
            'acta': 'Acta / Año',
            'tipopro': 'Tipo Propiedad',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        cocata1 = kwargs.pop('cocata1', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa y colegal si se proporcionan
        empresa_para_filtro = None
        if self.instance and self.instance.pk and self.instance.empresa:
            empresa_para_filtro = self.instance.empresa
        elif empresa:
            empresa_para_filtro = empresa
        
        if empresa_para_filtro:
            self.fields['empresa'].initial = empresa_para_filtro
        if cocata1:
            self.fields['colegal'].initial = cocata1
        
        # Establecer fecha de inscripción si existe en la instancia
        if self.instance and self.instance.pk and self.instance.inscripcion:
            # Convertir DateField a formato YYYY-MM-DD para el input type="date"
            # Asegurar que sea un objeto date, no string
            if isinstance(self.instance.inscripcion, str):
                # Si es string, intentar parsearlo
                try:
                    from datetime import datetime
                    fecha_obj = datetime.strptime(self.instance.inscripcion, '%d/%m/%Y').date()
                    self.fields['inscripcion'].initial = fecha_obj.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    try:
                        from datetime import datetime
                        fecha_obj = datetime.strptime(self.instance.inscripcion, '%Y-%m-%d').date()
                        self.fields['inscripcion'].initial = fecha_obj.strftime('%Y-%m-%d')
                    except (ValueError, TypeError):
                        pass
            else:
                # Si es un objeto date, formatearlo directamente
                self.fields['inscripcion'].initial = self.instance.inscripcion.strftime('%Y-%m-%d')
        
        # Hacer campos requeridos
        self.fields['colegal'].required = True
        
        # Cambiar el campo tipopro a ChoiceField con opciones fijas
        if 'tipopro' in self.fields:
            self.fields['tipopro'] = forms.ChoiceField(
                choices=[
                    ('', 'Seleccione un tipo de propiedad...'),
                    ('1', '1 - Nuda Propiedad'),
                    ('2', '2 - Usufructo'),
                ],
                required=False,
                label='Tipo Propiedad',
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'id_tipopro'
                })
            )
            
            # Si hay una instancia con tipopro, establecer el valor inicial
            if self.instance and self.instance.pk and self.instance.tipopro is not None:
                try:
                    # Convertir el valor a string para el initial
                    valor_inicial = str(self.instance.tipopro).strip()
                    # Asegurar que sea '1' o '2'
                    if valor_inicial in ['1', '2']:
                        self.fields['tipopro'].initial = valor_inicial
                except Exception:
                    pass
        
        # Cambiar el campo tipo a ModelChoiceField con TipoDocumento filtrado por empresa
        if 'tipo' in self.fields:
            from .models import TipoDocumento
            from django.db.models import Q
            
            # Obtener empresa para filtrar: priorizar instancia, luego parámetro
            empresa_filtro = None
            if self.instance and self.instance.pk and self.instance.empresa:
                empresa_filtro = self.instance.empresa
            elif empresa:
                empresa_filtro = empresa
            
            # Filtrar TipoDocumento por empresa y ordenar numéricamente por código
            queryset = TipoDocumento.objects.all()
            if empresa_filtro:
                queryset = queryset.filter(empresa=empresa_filtro)
            
            # Ordenar numéricamente por código (DecimalField se ordena numéricamente por defecto)
            queryset = queryset.order_by('codigo')
            
            # Cambiar el campo tipo a ModelChoiceField
            self.fields['tipo'] = forms.ModelChoiceField(
                queryset=queryset,
                required=False,
                label='Tipo de Documento',
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'id_tipo'
                }),
                empty_label='Seleccione un tipo de documento',
                to_field_name='codigo'
            )
            
            # Si hay una instancia con tipo, establecer el valor inicial
            if self.instance and self.instance.pk and self.instance.tipo:
                try:
                    # Con to_field_name='codigo', el initial debe ser el código directamente
                    # Asegurar que solo se use el código (Decimal), no la descripción
                    codigo_inicial = self.instance.tipo
                    # Si es Decimal, convertirlo a string para el initial
                    if hasattr(codigo_inicial, '__str__'):
                        codigo_inicial = str(codigo_inicial).strip()
                    self.fields['tipo'].initial = codigo_inicial
                except Exception:
                    pass
        
        # Cambiar el campo naturaleza a ModelChoiceField con Naturaleza
        if 'naturaleza' in self.fields:
            from .models import Naturaleza
            
            # Obtener todas las naturalezas y ordenar numéricamente por código
            queryset = Naturaleza.objects.all().order_by('codigo')
            
            # Cambiar el campo naturaleza a ModelChoiceField
            self.fields['naturaleza'] = forms.ModelChoiceField(
                queryset=queryset,
                required=False,
                label='Naturaleza Juridica',
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'id_naturaleza'
                }),
                empty_label='Seleccione una naturaleza',
                to_field_name='codigo'
            )
            
            # Si hay una instancia con naturaleza, establecer el valor inicial
            if self.instance and self.instance.pk and self.instance.naturaleza:
                try:
                    # Con to_field_name='codigo', el initial debe ser el código directamente
                    # Asegurar que solo se use el código (Decimal), no la descripción
                    codigo_inicial = self.instance.naturaleza
                    # Si es Decimal, convertirlo a string para el initial
                    if hasattr(codigo_inicial, '__str__'):
                        codigo_inicial = str(codigo_inicial).strip()
                    self.fields['naturaleza'].initial = codigo_inicial
                except Exception:
                    pass
        
        # Cambiar el campo dominio a ModelChoiceField con Dominio
        if 'dominio' in self.fields:
            from .models import Dominio
            
            # Obtener todos los dominios y ordenar numéricamente por código
            queryset = Dominio.objects.all().order_by('codigo')
            
            # Cambiar el campo dominio a ModelChoiceField
            self.fields['dominio'] = forms.ModelChoiceField(
                queryset=queryset,
                required=False,
                label='Clase de Dominio',
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'id_dominio'
                }),
                empty_label='Seleccione un dominio',
                to_field_name='codigo'
            )
            
            # Si hay una instancia con dominio, establecer el valor inicial
            if self.instance and self.instance.pk and self.instance.dominio:
                try:
                    # Con to_field_name='codigo', el initial debe ser el código directamente
                    # Asegurar que solo se use el código (Decimal), no la descripción
                    codigo_inicial = self.instance.dominio
                    # Si es Decimal, convertirlo a string para el initial
                    if hasattr(codigo_inicial, '__str__'):
                        codigo_inicial = str(codigo_inicial).strip()
                    self.fields['dominio'].initial = codigo_inicial
                except Exception:
                    pass
        
        # Cambiar el campo tmed a ModelChoiceField con TipoMedida
        if 'tmed' in self.fields:
            from .models import TipoMedida
            
            # Obtener todos los tipos de medida y ordenar numéricamente por código
            queryset = TipoMedida.objects.all().order_by('codigo')
            
            # Cambiar el campo tmed a ModelChoiceField
            self.fields['tmed'] = forms.ModelChoiceField(
                queryset=queryset,
                required=False,
                label='Tipo de Medida',
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'id_tmed'
                }),
                empty_label='Seleccione un tipo de medida',
                to_field_name='codigo'
            )
            
            # Si hay una instancia con tmed, establecer el valor inicial
            if self.instance and self.instance.pk and self.instance.tmed:
                try:
                    # Con to_field_name='codigo', el initial debe ser el código directamente
                    # Asegurar que solo se use el código (Decimal), no la descripción
                    codigo_inicial = self.instance.tmed
                    # Si es Decimal, convertirlo a string para el initial
                    if hasattr(codigo_inicial, '__str__'):
                        codigo_inicial = str(codigo_inicial).strip()
                    self.fields['tmed'].initial = codigo_inicial
                except Exception:
                    pass
        
        # Cambiar el campo unidad a ModelChoiceField con UnidadArea
        if 'unidad' in self.fields:
            from .models import UnidadArea
            
            # Obtener todas las unidades de área y ordenar numéricamente por código
            queryset = UnidadArea.objects.all().order_by('codigo')
            
            # Cambiar el campo unidad a ModelChoiceField
            self.fields['unidad'] = forms.ModelChoiceField(
                queryset=queryset,
                required=False,
                label='Unidad de Area',
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'id_unidad'
                }),
                empty_label='Seleccione una unidad de área',
                to_field_name='codigo'
            )
            
            # Si hay una instancia con unidad, establecer el valor inicial
            if self.instance and self.instance.pk and self.instance.unidad:
                try:
                    # Con to_field_name='codigo', el initial debe ser el código directamente
                    # Asegurar que solo se use el código (Decimal), no la descripción
                    codigo_inicial = self.instance.unidad
                    # Si es Decimal, convertirlo a string para el initial
                    if hasattr(codigo_inicial, '__str__'):
                        codigo_inicial = str(codigo_inicial).strip()
                    self.fields['unidad'].initial = codigo_inicial
                except Exception:
                    pass
        
        # Cambiar el campo coregistro a ModelChoiceField con RegistroPropiedad
        if 'coregistro' in self.fields:
            from .models import RegistroPropiedad
            
            # Obtener todos los registros de propiedad y ordenar por código
            queryset = RegistroPropiedad.objects.all().order_by('codigo')
            
            # Cambiar el campo coregistro a ModelChoiceField
            self.fields['coregistro'] = forms.ModelChoiceField(
                queryset=queryset,
                required=False,
                label='Registro / Propiedad',
                widget=forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'id_coregistro'
                }),
                empty_label='Seleccione un registro de propiedad',
                to_field_name='codigo'
            )
            
            # Si hay una instancia con coregistro, establecer el valor inicial
            if self.instance and self.instance.pk and self.instance.coregistro:
                try:
                    # Con to_field_name='codigo', el initial debe ser el código directamente
                    # Asegurar que solo se use el código, no la descripción completa
                    codigo_inicial = str(self.instance.coregistro).strip()
                    # Si tiene más de 3 caracteres, extraer solo el código (primeros caracteres)
                    if len(codigo_inicial) > 3:
                        codigo_inicial = codigo_inicial.split('-')[0].split()[0].strip()[:3]
                    self.fields['coregistro'].initial = codigo_inicial
                except Exception:
                    pass
        
        # Configurar campos de solo lectura
        if 'usuario' in self.fields:
            self.fields['usuario'].widget.attrs['readonly'] = True
        if 'fechasys' in self.fields:
            self.fields['fechasys'].widget.attrs['readonly'] = True
    
    def clean_coregistro(self):
        """
        Método clean personalizado para asegurar que coregistro solo contenga el código,
        no la descripción completa. Se ejecuta ANTES del método save().
        """
        coregistro = self.cleaned_data.get('coregistro')
        
        if coregistro is None:
            return None
        
        # Si es un objeto modelo, extraer solo el código
        if hasattr(coregistro, 'codigo'):
            codigo = str(coregistro.codigo).strip()
        elif isinstance(coregistro, str):
            codigo = coregistro.strip()
            # Si tiene más de 3 caracteres o contiene "-", extraer solo el código
            if len(codigo) > 3 or '-' in codigo:
                # Separar por "-" y tomar la primera parte
                codigo = codigo.split('-')[0].strip()
                # Si aún tiene espacios, tomar solo la primera palabra
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        else:
            codigo = str(coregistro).strip()
            # Limpiar si tiene descripción
            if len(codigo) > 3 or '-' in codigo:
                codigo = codigo.split('-')[0].strip()
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        
        # Limitar a máximo 3 caracteres
        if codigo and len(codigo) > 3:
            codigo = codigo[:3]
        
        return codigo if codigo else None
    
    def clean_naturaleza(self):
        """
        Método clean personalizado para asegurar que naturaleza solo contenga el código,
        no la descripción completa. Se ejecuta ANTES del método save().
        El código se convierte a Decimal ya que el campo es DecimalField.
        """
        from decimal import Decimal
        
        naturaleza = self.cleaned_data.get('naturaleza')
        
        if naturaleza is None:
            return None
        
        # Si es un objeto modelo, extraer solo el código
        if hasattr(naturaleza, 'codigo'):
            codigo = str(naturaleza.codigo).strip()
        elif isinstance(naturaleza, str):
            codigo = naturaleza.strip()
            # Si tiene más de 2 caracteres o contiene "-", extraer solo el código
            if len(codigo) > 2 or '-' in codigo:
                # Separar por "-" y tomar la primera parte
                codigo = codigo.split('-')[0].strip()
                # Si aún tiene espacios, tomar solo la primera palabra
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        else:
            codigo = str(naturaleza).strip()
            # Limpiar si tiene descripción
            if len(codigo) > 2 or '-' in codigo:
                codigo = codigo.split('-')[0].strip()
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        
        # Convertir a Decimal si hay código
        if codigo:
            try:
                return Decimal(codigo)
            except (ValueError, TypeError):
                return None
        
        return None
    
    def clean_dominio(self):
        """
        Método clean personalizado para asegurar que dominio solo contenga el código,
        no la descripción completa. Se ejecuta ANTES del método save().
        El código se convierte a Decimal ya que el campo es DecimalField.
        """
        from decimal import Decimal
        
        dominio = self.cleaned_data.get('dominio')
        
        if dominio is None:
            return None
        
        # Si es un objeto modelo, extraer solo el código
        if hasattr(dominio, 'codigo'):
            codigo = str(dominio.codigo).strip()
        elif isinstance(dominio, str):
            codigo = dominio.strip()
            # Si tiene más de 2 caracteres o contiene "-", extraer solo el código
            if len(codigo) > 2 or '-' in codigo:
                # Separar por "-" y tomar la primera parte
                codigo = codigo.split('-')[0].strip()
                # Si aún tiene espacios, tomar solo la primera palabra
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        else:
            codigo = str(dominio).strip()
            # Limpiar si tiene descripción
            if len(codigo) > 2 or '-' in codigo:
                codigo = codigo.split('-')[0].strip()
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        
        # Convertir a Decimal si hay código
        if codigo:
            try:
                return Decimal(codigo)
            except (ValueError, TypeError):
                return None
        
        return None
    
    def clean_tipo(self):
        """
        Método clean personalizado para asegurar que tipo solo contenga el código,
        no la descripción completa. Se ejecuta ANTES del método save().
        El código se convierte a Decimal ya que el campo es DecimalField.
        """
        from decimal import Decimal
        
        tipo = self.cleaned_data.get('tipo')
        
        if tipo is None:
            return None
        
        # Si es un objeto modelo, extraer solo el código
        if hasattr(tipo, 'codigo'):
            codigo = str(tipo.codigo).strip()
        elif isinstance(tipo, str):
            codigo = tipo.strip()
            # Si tiene más de 2 caracteres o contiene "-", extraer solo el código
            if len(codigo) > 2 or '-' in codigo:
                # Separar por "-" y tomar la primera parte
                codigo = codigo.split('-')[0].strip()
                # Si aún tiene espacios, tomar solo la primera palabra
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        else:
            codigo = str(tipo).strip()
            # Limpiar si tiene descripción
            if len(codigo) > 2 or '-' in codigo:
                codigo = codigo.split('-')[0].strip()
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        
        # Convertir a Decimal si hay código
        if codigo:
            try:
                return Decimal(codigo)
            except (ValueError, TypeError):
                return None
        
        return None
    
    def clean_tmed(self):
        """
        Método clean personalizado para asegurar que tmed solo contenga el código,
        no la descripción completa. Se ejecuta ANTES del método save().
        El código se convierte a Decimal ya que el campo es DecimalField.
        """
        from decimal import Decimal
        
        tmed = self.cleaned_data.get('tmed')
        
        if tmed is None:
            return None
        
        # Si es un objeto modelo, extraer solo el código
        if hasattr(tmed, 'codigo'):
            codigo = str(tmed.codigo).strip()
        elif isinstance(tmed, str):
            codigo = tmed.strip()
            # Si tiene más de 2 caracteres o contiene "-", extraer solo el código
            if len(codigo) > 2 or '-' in codigo:
                # Separar por "-" y tomar la primera parte
                codigo = codigo.split('-')[0].strip()
                # Si aún tiene espacios, tomar solo la primera palabra
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        else:
            codigo = str(tmed).strip()
            # Limpiar si tiene descripción
            if len(codigo) > 2 or '-' in codigo:
                codigo = codigo.split('-')[0].strip()
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        
        # Convertir a Decimal si hay código
        if codigo:
            try:
                return Decimal(codigo)
            except (ValueError, TypeError):
                return None
        
        return None
    
    def clean_unidad(self):
        """
        Método clean personalizado para asegurar que unidad solo contenga el código,
        no la descripción completa. Se ejecuta ANTES del método save().
        El código se convierte a Decimal ya que el campo es DecimalField.
        """
        from decimal import Decimal
        
        unidad = self.cleaned_data.get('unidad')
        
        if unidad is None:
            return None
        
        # Si es un objeto modelo, extraer solo el código
        if hasattr(unidad, 'codigo'):
            codigo = str(unidad.codigo).strip()
        elif isinstance(unidad, str):
            codigo = unidad.strip()
            # Si tiene más de 2 caracteres o contiene "-", extraer solo el código
            if len(codigo) > 2 or '-' in codigo:
                # Separar por "-" y tomar la primera parte
                codigo = codigo.split('-')[0].strip()
                # Si aún tiene espacios, tomar solo la primera palabra
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        else:
            codigo = str(unidad).strip()
            # Limpiar si tiene descripción
            if len(codigo) > 2 or '-' in codigo:
                codigo = codigo.split('-')[0].strip()
                if ' ' in codigo:
                    codigo = codigo.split()[0].strip()
        
        # Convertir a Decimal si hay código
        if codigo:
            try:
                return Decimal(codigo)
            except (ValueError, TypeError):
                return None
        
        return None
    
    def save(self, commit=True):
        """
        Método save personalizado para asegurar que TODOS los campos ModelChoiceField
        con to_field_name='codigo' guarden SOLO el código, no el objeto completo ni la descripción.
        
        Comboboxes que deben guardar solo el código:
        - coregistro (Registro / Propiedad): CHAR(3) - guarda solo código
        - tipo (Tipo de Documento): Decimal - guarda solo código
        - naturaleza (Naturaleza Juridica): Decimal - guarda solo código
        - dominio (Clase de Dominio): Decimal - guarda solo código
        - tmed (Tipo de Medida): Decimal - guarda solo código
        - unidad (Unidad de Area): Decimal - guarda solo código
        """
        instance = super().save(commit=False)
        from decimal import Decimal
        
        def extraer_codigo(valor, es_decimal=False, max_length=None):
            """
            Función auxiliar para extraer solo el código de un valor.
            Maneja casos donde el valor puede ser:
            - Un string con código y descripción (ej: "01 - Descripción" o "AB - ATLANTIDA, TELA")
            - Un objeto modelo con atributo 'codigo' (ej: RegistroPropiedad, TipoDocumento, etc.)
            - Ya un código limpio (ej: "AB", "01")
            """
            if valor is None:
                return None
            
            codigo_final = None
            
            # PRIORIDAD 1: Si es un objeto modelo, extraer directamente el código
            if hasattr(valor, 'codigo'):
                try:
                    codigo_final = str(valor.codigo).strip()
                except (AttributeError, TypeError):
                    pass
            
            # PRIORIDAD 2: Si es string, puede ser código puro o código con descripción
            if codigo_final is None and isinstance(valor, str):
                valor_str = valor.strip()
                # Si contiene "-" o tiene más de 3 caracteres, probablemente tiene descripción
                # Ejemplo: "AB - ATLANTIDA, TELA" -> extraer solo "AB"
                if '-' in valor_str:
                    # Separar por "-" y tomar la primera parte
                    codigo_limpio = valor_str.split('-')[0].strip()
                    # Si aún tiene espacios, tomar solo la primera palabra
                    codigo_limpio = codigo_limpio.split()[0] if ' ' in codigo_limpio else codigo_limpio
                    codigo_final = codigo_limpio
                elif len(valor_str) > 3:
                    # Si es muy largo, probablemente tiene descripción, tomar solo primera palabra
                    codigo_final = valor_str.split()[0].strip()
                else:
                    # Es un código corto, usarlo directamente
                    codigo_final = valor_str
            
            # PRIORIDAD 3: Cualquier otro caso, convertir a string y limpiar
            if codigo_final is None:
                codigo_str = str(valor).strip()
                # Intentar extraer código de representación string del objeto
                if '-' in codigo_str:
                    codigo_limpio = codigo_str.split('-')[0].strip()
                    codigo_limpio = codigo_limpio.split()[0] if ' ' in codigo_limpio else codigo_limpio
                    codigo_final = codigo_limpio
                elif len(codigo_str) > 3:
                    codigo_final = codigo_str.split()[0].strip()
                else:
                    codigo_final = codigo_str
            
            # Aplicar límite de longitud si se especifica (IMPORTANTE: antes de convertir a Decimal)
            if max_length and codigo_final:
                codigo_final = codigo_final[:max_length]
            
            # Convertir a Decimal si es necesario
            if es_decimal and codigo_final:
                try:
                    return Decimal(codigo_final)
                except (ValueError, TypeError):
                    return codigo_final
            
            return codigo_final
        
        # 1. coregistro (Registro / Propiedad) - CHAR(3)
        # Ejemplo: Si el combobox muestra "AB - ATLANTIDA, TELA", solo guarda "AB"
        # Los códigos pueden ser alfanuméricos (ej: "AB", "01", "XYZ")
        # NOTA: El método clean_coregistro() ya limpió el valor, pero por seguridad
        # lo verificamos nuevamente aquí
        coregistro = self.cleaned_data.get('coregistro')
        
        # El valor ya debería estar limpio por clean_coregistro(), pero por seguridad:
        if coregistro:
            # Si es un objeto modelo, extraer el código
            if hasattr(coregistro, 'codigo'):
                codigo_coregistro = str(coregistro.codigo).strip()[:3]
            else:
                codigo_coregistro = extraer_codigo(coregistro, es_decimal=False, max_length=3)
                if codigo_coregistro:
                    codigo_coregistro = str(codigo_coregistro).strip()[:3]
            instance.coregistro = codigo_coregistro if codigo_coregistro else None
        else:
            instance.coregistro = None
        
        # 2. tipo (Tipo de Documento) - Decimal
        # NOTA: El método clean_tipo() ya limpió el valor y lo convirtió a Decimal
        tipo = self.cleaned_data.get('tipo')
        if tipo:
            # Si es un objeto modelo, extraer el código
            if hasattr(tipo, 'codigo'):
                try:
                    from decimal import Decimal
                    instance.tipo = Decimal(str(tipo.codigo).strip())
                except (ValueError, TypeError):
                    instance.tipo = extraer_codigo(tipo, es_decimal=True)
            else:
                # Ya debería estar limpio por clean_tipo(), pero por seguridad:
                instance.tipo = extraer_codigo(tipo, es_decimal=True)
        else:
            instance.tipo = None
        
        # 3. naturaleza (Naturaleza Juridica) - Decimal
        # NOTA: El método clean_naturaleza() ya limpió el valor y lo convirtió a Decimal
        naturaleza = self.cleaned_data.get('naturaleza')
        if naturaleza:
            # Si es un objeto modelo, extraer el código
            if hasattr(naturaleza, 'codigo'):
                try:
                    from decimal import Decimal
                    instance.naturaleza = Decimal(str(naturaleza.codigo).strip())
                except (ValueError, TypeError):
                    instance.naturaleza = extraer_codigo(naturaleza, es_decimal=True)
            else:
                # Ya debería estar limpio por clean_naturaleza(), pero por seguridad:
                instance.naturaleza = extraer_codigo(naturaleza, es_decimal=True)
        else:
            instance.naturaleza = None
        
        # 4. dominio (Clase de Dominio) - Decimal
        # NOTA: El método clean_dominio() ya limpió el valor y lo convirtió a Decimal
        dominio = self.cleaned_data.get('dominio')
        if dominio:
            # Si es un objeto modelo, extraer el código
            if hasattr(dominio, 'codigo'):
                try:
                    from decimal import Decimal
                    instance.dominio = Decimal(str(dominio.codigo).strip())
                except (ValueError, TypeError):
                    instance.dominio = extraer_codigo(dominio, es_decimal=True)
            else:
                # Ya debería estar limpio por clean_dominio(), pero por seguridad:
                instance.dominio = extraer_codigo(dominio, es_decimal=True)
        else:
            instance.dominio = None
        
        # 5. tmed (Tipo de Medida) - Decimal
        # NOTA: El método clean_tmed() ya limpió el valor y lo convirtió a Decimal
        tmed = self.cleaned_data.get('tmed')
        if tmed:
            # Si es un objeto modelo, extraer el código
            if hasattr(tmed, 'codigo'):
                try:
                    from decimal import Decimal
                    instance.tmed = Decimal(str(tmed.codigo).strip())
                except (ValueError, TypeError):
                    instance.tmed = extraer_codigo(tmed, es_decimal=True)
            else:
                # Ya debería estar limpio por clean_tmed(), pero por seguridad:
                instance.tmed = extraer_codigo(tmed, es_decimal=True)
        else:
            instance.tmed = None
        
        # 6. unidad (Unidad de Area) - Decimal
        # NOTA: El método clean_unidad() ya limpió el valor y lo convirtió a Decimal
        unidad = self.cleaned_data.get('unidad')
        if unidad:
            # Si es un objeto modelo, extraer el código
            if hasattr(unidad, 'codigo'):
                try:
                    from decimal import Decimal
                    instance.unidad = Decimal(str(unidad.codigo).strip())
                except (ValueError, TypeError):
                    instance.unidad = extraer_codigo(unidad, es_decimal=True)
            else:
                # Ya debería estar limpio por clean_unidad(), pero por seguridad:
                instance.unidad = extraer_codigo(unidad, es_decimal=True)
        else:
            instance.unidad = None
        
        # 7. tipopro (Tipo Propiedad) - Decimal
        # El campo tipopro es un ChoiceField que devuelve '1' o '2' como string
        tipopro = self.cleaned_data.get('tipopro')
        if tipopro:
            try:
                from decimal import Decimal
                # Convertir el string a Decimal
                instance.tipopro = Decimal(str(tipopro).strip())
            except (ValueError, TypeError):
                # Si hay error, usar valor por defecto 0
                instance.tipopro = Decimal('0')
        else:
            instance.tipopro = Decimal('0')
        
        if commit:
            instance.save()
        return instance

class ComentariosCatastroForm(forms.ModelForm):
    """Formulario para comentarios de catastro"""
    
    class Meta:
        model = ComentariosCatastro
        fields = ['comentario', 'usuario', 'fecha']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Ingrese el comentario...',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'comentario': 'Comentario',
            'usuario': 'Usuario',
            'fecha': 'Fecha',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fecha'].initial = fecha_sistema
        
        self.fields['usuario'].required = False
        self.fields['fecha'].required = False




































class CaracteristicasForm(forms.ModelForm):
    """Formulario para características del predio (Caracteristicas)"""
    
    class Meta:
        model = Caracteristicas
        fields = ['empresa', 'cocata1', 'iglesia', 'mercado', 'escuela', 'embarque', 'proparea', 
                  'propexplota', 'proptopo', 'caudal', 'pozo', 'comunicacion',
                  'dis1', 'friego1', 'sisirri1', 'areairri1',
                  'dis2', 'friego2', 'sisirri2', 'areairri2',
                  'dis3', 'friego3', 'sisirri3', 'areairri3',
                  'dis4', 'friego4', 'sisirri4', 'areairri4',
                  'dis5', 'friego5', 'sisirri5', 'areairri5',
                  'usot1', 'porcet1', 'usot2', 'porcet2', 'usot3', 'porcet3', 'usot4', 'porcet4',
                  'usuario', 'fechasys']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'cocata1': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20', 'readonly': True}),
            'iglesia': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '99'}),
            'mercado': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '99'}),
            'escuela': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '99'}),
            'embarque': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '99'}),
            'proparea': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'caudal': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'pozo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'dis1': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'friego1': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.001', 'min': '0'}),
            'areairri1': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'dis2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'friego2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.001', 'min': '0'}),
            'areairri2': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'dis3': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'friego3': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.001', 'min': '0'}),
            'areairri3': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'dis4': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'friego4': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.001', 'min': '0'}),
            'areairri4': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'dis5': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'friego5': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.001', 'min': '0'}),
            'areairri5': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'porcet1': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'porcet2': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'porcet3': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'porcet4': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'readonly': True}),
            'fechasys': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'type': 'text'}),
        }
        labels = {
            'empresa': 'Municipio',
            'cocata1': 'Clave Catastral',
            'iglesia': 'Iglesia',
            'mercado': 'Mercado mas Cercano (Kms)',
            'escuela': 'Escuela',
            'embarque': 'Sitio de Embarque (Kms)',
            'proparea': 'Area (Has)',
            'propexplota': 'Explotación',
            'proptopo': 'Topografia',
            'caudal': 'Caudal',
            'pozo': 'Pozo',
            'comunicacion': 'Vias de Comunicación',
            'dis1': 'Dist. Km',
            'friego1': 'Riego',
            'sisirri1': 'Sistema de Irrigación',
            'areairri1': 'Area (Has)',
            'dis2': 'Dist. Km',
            'friego2': 'Riego',
            'sisirri2': 'Sistema de Irrigación',
            'areairri2': 'Area (Has)',
            'dis3': 'Dist. Km',
            'friego3': 'Riego',
            'sisirri3': 'Sistema de Irrigación',
            'areairri3': 'Area (Has)',
            'dis4': 'Dist. Km',
            'friego4': 'Riego',
            'sisirri4': 'Sistema de Irrigación',
            'areairri4': 'Area (Has)',
            'dis5': 'Dist. Km',
            'friego5': 'Riego',
            'sisirri5': 'Sistema de Irrigación',
            'areairri5': 'Area (Has)',
            'usot1': 'Uso',
            'porcet1': 'Porcentaje',
            'usot2': 'Uso',
            'porcet2': 'Porcentaje',
            'usot3': 'Uso',
            'porcet3': 'Porcentaje',
            'usot4': 'Uso',
            'porcet4': 'Porcentaje',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        cocata1 = kwargs.pop('cocata1', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa y cocata1 si se proporcionan
        if empresa:
            self.fields['empresa'].initial = empresa
        if cocata1:
            self.fields['cocata1'].initial = cocata1
        
        # Hacer campos requeridos
        self.fields['cocata1'].required = True
        
        # Obtener empresa para filtros
        empresa_para_filtro = None
        if self.instance and self.instance.pk and self.instance.empresa:
            empresa_para_filtro = self.instance.empresa
        elif empresa:
            empresa_para_filtro = empresa
        
        # Convertir propexplota en ModelChoiceField vinculado a Explotacion
        self.fields['propexplota'] = forms.ModelChoiceField(
            queryset=Explotacion.objects.all().order_by('codigo'),
            required=False,
            label='Explotación',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_propexplota'}),
            empty_label='Seleccione una explotación...',
            to_field_name='codigo'
        )
        
        # Establecer valor inicial si existe una instancia
        if self.instance and self.instance.pk and self.instance.propexplota:
            try:
                explotacion_initial = Explotacion.objects.get(codigo=self.instance.propexplota)
                self.fields['propexplota'].initial = explotacion_initial
            except Explotacion.DoesNotExist:
                pass
        
        # Convertir proptopo en ModelChoiceField vinculado a Topografia, filtrado por empresa
        queryset_topografia = Topografia.objects.all()
        if empresa_para_filtro:
            queryset_topografia = queryset_topografia.filter(empresa=empresa_para_filtro)
        queryset_topografia = queryset_topografia.order_by('cotopo')
        
        self.fields['proptopo'] = forms.ModelChoiceField(
            queryset=queryset_topografia,
            required=False,
            label='Topografia',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_proptopo'}),
            empty_label='Seleccione una topografía...',
            to_field_name='cotopo'
        )
        
        # Establecer valor inicial si existe una instancia
        if self.instance and self.instance.pk and self.instance.proptopo:
            try:
                topografia_initial = Topografia.objects.filter(empresa=empresa_para_filtro).get(cotopo=self.instance.proptopo)
                self.fields['proptopo'].initial = topografia_initial
            except (Topografia.DoesNotExist, Topografia.MultipleObjectsReturned):
                pass
        
        # Convertir comunicacion en ModelChoiceField vinculado a Vias
        self.fields['comunicacion'] = forms.ModelChoiceField(
            queryset=Vias.objects.all().order_by('codigo'),
            required=False,
            label='Vias de Comunicación',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_comunicacion'}),
            empty_label='Seleccione una vía de comunicación...',
            to_field_name='codigo'
        )
        
        # Establecer valor inicial si existe una instancia
        if self.instance and self.instance.pk and self.instance.comunicacion:
            try:
                vias_initial = Vias.objects.get(codigo=self.instance.comunicacion)
                self.fields['comunicacion'].initial = vias_initial
            except Vias.DoesNotExist:
                pass
        
        # Convertir sisirri1 a sisirri5 en ModelChoiceField vinculados a Irrigacion
        for i in range(1, 6):
            field_name = f'sisirri{i}'
            self.fields[field_name] = forms.ModelChoiceField(
                queryset=Irrigacion.objects.all().order_by('codigo'),
                required=False,
                label=f'Sistema de Irrigación {i}',
                widget=forms.Select(attrs={'class': 'form-control', 'id': f'id_{field_name}'}),
                empty_label='Seleccione un sistema...',
                to_field_name='codigo'
            )
            
            # Establecer valor inicial si existe una instancia
            if self.instance and self.instance.pk:
                instance_value = getattr(self.instance, field_name, None)
                if instance_value:
                    try:
                        irrigacion_initial = Irrigacion.objects.get(codigo=instance_value)
                        self.fields[field_name].initial = irrigacion_initial
                    except Irrigacion.DoesNotExist:
                        pass
        
        # Convertir usot1 a usot4 en ModelChoiceField vinculados a UsoTierra
        for i in range(1, 5):
            field_name = f'usot{i}'
            self.fields[field_name] = forms.ModelChoiceField(
                queryset=UsoTierra.objects.all().order_by('codigo'),
                required=False,
                label='Uso',
                widget=forms.Select(attrs={'class': 'form-control', 'id': f'id_{field_name}'}),
                empty_label='Seleccione un uso...',
                to_field_name='codigo'
            )
            
            # Establecer valor inicial si existe una instancia
            if self.instance and self.instance.pk:
                instance_value = getattr(self.instance, field_name, None)
                if instance_value:
                    try:
                        usotierra_initial = UsoTierra.objects.get(codigo=instance_value)
                        self.fields[field_name].initial = usotierra_initial
                    except UsoTierra.DoesNotExist:
                        pass
        
        # Establecer fecha sistema
        if not self.instance or not self.instance.pk:
            from django.utils import timezone
            self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        elif self.instance and self.instance.pk and self.instance.fechasys:
            self.fields['fechasys'].initial = self.instance.fechasys.strftime('%Y-%m-%d %H:%M:%S')
        else:
            from django.utils import timezone
            self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def clean_propexplota(self):
        """Limpia el campo propexplota para asegurar que solo se guarde el código"""
        propexplota = self.cleaned_data.get('propexplota')
        if propexplota:
            # Si es un objeto Explotacion, obtener el código
            if isinstance(propexplota, Explotacion):
                return propexplota.codigo
            # Si ya es un string, devolverlo tal cual
            elif isinstance(propexplota, str):
                return propexplota[:2]  # Limitar a 2 caracteres según el modelo
        return propexplota
    
    def clean_proptopo(self):
        """Limpia el campo proptopo para asegurar que solo se guarde el código"""
        proptopo = self.cleaned_data.get('proptopo')
        if proptopo:
            # Si es un objeto Topografia, obtener el código
            if isinstance(proptopo, Topografia):
                return proptopo.cotopo
            # Si ya es un string, devolverlo tal cual
            elif isinstance(proptopo, str):
                return proptopo[:2]  # Limitar a 2 caracteres según el modelo
        return proptopo
    
    def clean_comunicacion(self):
        """Limpia el campo comunicacion para asegurar que solo se guarde el código"""
        comunicacion = self.cleaned_data.get('comunicacion')
        if comunicacion:
            # Si es un objeto Vias, obtener el código
            if isinstance(comunicacion, Vias):
                return comunicacion.codigo
            # Si ya es un string, devolverlo tal cual
            elif isinstance(comunicacion, str):
                return comunicacion[:3]  # Limitar a 3 caracteres según el modelo
        return comunicacion
    
    def clean_sisirri1(self):
        """Limpia el campo sisirri1 para asegurar que solo se guarde el código"""
        sisirri1 = self.cleaned_data.get('sisirri1')
        if sisirri1:
            if isinstance(sisirri1, Irrigacion):
                return sisirri1.codigo
            elif isinstance(sisirri1, str):
                return sisirri1[:3]
        return sisirri1
    
    def clean_sisirri2(self):
        """Limpia el campo sisirri2 para asegurar que solo se guarde el código"""
        sisirri2 = self.cleaned_data.get('sisirri2')
        if sisirri2:
            if isinstance(sisirri2, Irrigacion):
                return sisirri2.codigo
            elif isinstance(sisirri2, str):
                return sisirri2[:3]
        return sisirri2
    
    def clean_sisirri3(self):
        """Limpia el campo sisirri3 para asegurar que solo se guarde el código"""
        sisirri3 = self.cleaned_data.get('sisirri3')
        if sisirri3:
            if isinstance(sisirri3, Irrigacion):
                return sisirri3.codigo
            elif isinstance(sisirri3, str):
                return sisirri3[:3]
        return sisirri3
    
    def clean_sisirri4(self):
        """Limpia el campo sisirri4 para asegurar que solo se guarde el código"""
        sisirri4 = self.cleaned_data.get('sisirri4')
        if sisirri4:
            if isinstance(sisirri4, Irrigacion):
                return sisirri4.codigo
            elif isinstance(sisirri4, str):
                return sisirri4[:3]
        return sisirri4
    
    def clean_sisirri5(self):
        """Limpia el campo sisirri5 para asegurar que solo se guarde el código"""
        sisirri5 = self.cleaned_data.get('sisirri5')
        if sisirri5:
            if isinstance(sisirri5, Irrigacion):
                return sisirri5.codigo
            elif isinstance(sisirri5, str):
                return sisirri5[:3]
        return sisirri5
    
    def clean_usot1(self):
        """Limpia el campo usot1 para asegurar que solo se guarde el código"""
        usot1 = self.cleaned_data.get('usot1')
        if usot1:
            if isinstance(usot1, UsoTierra):
                return usot1.codigo
            elif isinstance(usot1, str):
                return usot1[:3]
        return usot1
    
    def clean_usot2(self):
        """Limpia el campo usot2 para asegurar que solo se guarde el código"""
        usot2 = self.cleaned_data.get('usot2')
        if usot2:
            if isinstance(usot2, UsoTierra):
                return usot2.codigo
            elif isinstance(usot2, str):
                return usot2[:3]
        return usot2
    
    def clean_usot3(self):
        """Limpia el campo usot3 para asegurar que solo se guarde el código"""
        usot3 = self.cleaned_data.get('usot3')
        if usot3:
            if isinstance(usot3, UsoTierra):
                return usot3.codigo
            elif isinstance(usot3, str):
                return usot3[:3]
        return usot3
    
    def clean_usot4(self):
        """Limpia el campo usot4 para asegurar que solo se guarde el código"""
        usot4 = self.cleaned_data.get('usot4')
        if usot4:
            if isinstance(usot4, UsoTierra):
                return usot4.codigo
            elif isinstance(usot4, str):
                return usot4[:3]
        return usot4
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        from django.utils import timezone
        
        # Asegurar que propexplota solo guarde el código
        if 'propexplota' in self.cleaned_data:
            propexplota_value = self.cleaned_data['propexplota']
            if isinstance(propexplota_value, Explotacion):
                instance.propexplota = propexplota_value.codigo
            elif propexplota_value:
                instance.propexplota = str(propexplota_value)[:2]
            else:
                instance.propexplota = None
        
        # Asegurar que proptopo solo guarde el código
        if 'proptopo' in self.cleaned_data:
            proptopo_value = self.cleaned_data['proptopo']
            if isinstance(proptopo_value, Topografia):
                instance.proptopo = proptopo_value.cotopo
            elif proptopo_value:
                instance.proptopo = str(proptopo_value)[:2]
            else:
                instance.proptopo = None
        
        # Asegurar que comunicacion solo guarde el código
        if 'comunicacion' in self.cleaned_data:
            comunicacion_value = self.cleaned_data['comunicacion']
            if isinstance(comunicacion_value, Vias):
                instance.comunicacion = comunicacion_value.codigo
            elif comunicacion_value:
                instance.comunicacion = str(comunicacion_value)[:3]
            else:
                instance.comunicacion = None
        
        # Asegurar que sisirri1 a sisirri5 solo guarden el código
        for i in range(1, 6):
            field_name = f'sisirri{i}'
            if field_name in self.cleaned_data:
                field_value = self.cleaned_data[field_name]
                if isinstance(field_value, Irrigacion):
                    setattr(instance, field_name, field_value.codigo)
                elif field_value:
                    setattr(instance, field_name, str(field_value)[:3])
                else:
                    setattr(instance, field_name, None)
        
        # Asegurar que usot1 a usot4 solo guarden el código
        for i in range(1, 5):
            field_name = f'usot{i}'
            if field_name in self.cleaned_data:
                field_value = self.cleaned_data[field_name]
                if isinstance(field_value, UsoTierra):
                    setattr(instance, field_name, field_value.codigo)
                elif field_value:
                    setattr(instance, field_name, str(field_value)[:3])
                else:
                    setattr(instance, field_name, None)
        
        # Establecer usuario y fechasys
        if not instance.usuario:
            # El usuario se establecerá en la vista
            pass
        if not instance.fechasys:
            instance.fechasys = timezone.now()
        
        if commit:
            instance.save()
        return instance

class ComentariosCatastroForm(forms.ModelForm):
    """Formulario para comentarios de catastro"""
    
    class Meta:
        model = ComentariosCatastro
        fields = ['comentario', 'usuario', 'fecha']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Ingrese el comentario...',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'comentario': 'Comentario',
            'usuario': 'Usuario',
            'fecha': 'Fecha',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fecha'].initial = fecha_sistema
        
        self.fields['usuario'].required = False
        self.fields['fecha'].required = False

class ComplementoForm(forms.ModelForm):
    """Formulario para datos complementarios del predio (Complemento)"""
    
    class Meta:
        model = Complemento
        fields = ['empresa', 'cocomple', 'fechaadqui', 'monto', 'clatra', 'maquinaria', 
                  'delineador', 'observacion', 'fedeli', 'bs1', 'bs2', 'bs3', 'bs4', 
                  'bs5', 'bs6', 'bs7', 'bs8', 'bs9', 'ocupante', 'renta', 'observ2', 
                  'causa', 'Bnocalcu', 'Bfecal', 'usuario', 'fechasys']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'cocomple': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20', 'readonly': True}),
            'fechaadqui': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'monto': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'clatra': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'maquinaria': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'delineador': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '30'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'maxlength': '5000'}),
            'fedeli': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'ocupante': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'renta': forms.NumberInput(attrs={'class': 'form-control text-end', 'step': '0.01', 'min': '0'}),
            'observ2': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '70'}),
            'causa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'Bnocalcu': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'Bfecal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'readonly': True}),
            'fechasys': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'type': 'text'}),
        }
        labels = {
            'empresa': 'Municipio',
            'cocomple': 'Clave Catastral',
            'fechaadqui': 'Fecha Adquisición',
            'monto': 'Monto de la Transacción',
            'clatra': 'Clase de Transaccion',
            'maquinaria': 'Maquinaria',
            'delineador': 'Delineador',
            'observacion': 'Observación',
            'fedeli': 'Fecha Delimitación',
            'bs1': 'Agua',
            'bs2': 'Telefono',
            'bs3': 'Drenaje',
            'bs4': 'Calle',
            'bs5': 'Electricidad',
            'bs6': 'Acera',
            'bs7': 'Alumbrado Publico',
            'bs8': 'Tren de Aseo',
            'bs9': 'Servicios Adicionales',
            'ocupante': 'Ocupante',
            'renta': 'Renta',
            'observ2': 'Observación 2',
            'causa': 'Causa',
            'Bnocalcu': 'Calculista',
            'Bfecal': 'Fecha Calculo',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        cocata1 = kwargs.pop('cocata1', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa y cocata1 si se proporcionan
        if empresa:
            self.fields['empresa'].initial = empresa
        if cocata1:
            self.fields['cocomple'].initial = cocata1
        
        # Hacer campos requeridos
        self.fields['cocomple'].required = True
        
        # Convertir bs1 (Agua) en ModelChoiceField vinculado a Agua
        self.fields['bs1'] = forms.ModelChoiceField(
            queryset=Agua.objects.all().order_by('codigo'),
            required=False,
            label='Agua',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs1'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        # Establecer valor inicial si existe una instancia
        if self.instance and self.instance.pk and self.instance.bs1:
            try:
                from decimal import Decimal
                codigo_bs1 = Decimal(str(self.instance.bs1))
                agua_initial = Agua.objects.get(codigo=codigo_bs1)
                self.fields['bs1'].initial = agua_initial
            except (Agua.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs2 (Telefono) en ModelChoiceField vinculado a Telefono
        self.fields['bs2'] = forms.ModelChoiceField(
            queryset=Telefono.objects.all().order_by('codigo'),
            required=False,
            label='Telefono',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs2'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs2:
            try:
                from decimal import Decimal
                codigo_bs2 = Decimal(str(self.instance.bs2))
                telefono_initial = Telefono.objects.get(codigo=codigo_bs2)
                self.fields['bs2'].initial = telefono_initial
            except (Telefono.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs3 (Drenaje) en ModelChoiceField vinculado a Drenaje
        self.fields['bs3'] = forms.ModelChoiceField(
            queryset=Drenaje.objects.all().order_by('codigo'),
            required=False,
            label='Drenaje',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs3'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs3:
            try:
                from decimal import Decimal
                codigo_bs3 = Decimal(str(self.instance.bs3))
                drenaje_initial = Drenaje.objects.get(codigo=codigo_bs3)
                self.fields['bs3'].initial = drenaje_initial
            except (Drenaje.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs4 (Calle) en ModelChoiceField vinculado a Calle
        self.fields['bs4'] = forms.ModelChoiceField(
            queryset=Calle.objects.all().order_by('codigo'),
            required=False,
            label='Calle',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs4'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs4:
            try:
                from decimal import Decimal
                codigo_bs4 = Decimal(str(self.instance.bs4))
                calle_initial = Calle.objects.get(codigo=codigo_bs4)
                self.fields['bs4'].initial = calle_initial
            except (Calle.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs5 (Electricidad) en ModelChoiceField vinculado a Electricidad
        self.fields['bs5'] = forms.ModelChoiceField(
            queryset=Electricidad.objects.all().order_by('codigo'),
            required=False,
            label='Electricidad',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs5'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs5:
            try:
                from decimal import Decimal
                codigo_bs5 = Decimal(str(self.instance.bs5))
                electricidad_initial = Electricidad.objects.get(codigo=codigo_bs5)
                self.fields['bs5'].initial = electricidad_initial
            except (Electricidad.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs6 (Acera) en ModelChoiceField vinculado a Acera
        self.fields['bs6'] = forms.ModelChoiceField(
            queryset=Acera.objects.all().order_by('codigo'),
            required=False,
            label='Acera',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs6'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs6:
            try:
                from decimal import Decimal
                codigo_bs6 = Decimal(str(self.instance.bs6))
                acera_initial = Acera.objects.get(codigo=codigo_bs6)
                self.fields['bs6'].initial = acera_initial
            except (Acera.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs7 (Alumbrado) en ModelChoiceField vinculado a Alumbrado
        self.fields['bs7'] = forms.ModelChoiceField(
            queryset=Alumbrado.objects.all().order_by('codigo'),
            required=False,
            label='Alumbrado Publico',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs7'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs7:
            try:
                from decimal import Decimal
                codigo_bs7 = Decimal(str(self.instance.bs7))
                alumbrado_initial = Alumbrado.objects.get(codigo=codigo_bs7)
                self.fields['bs7'].initial = alumbrado_initial
            except (Alumbrado.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs8 (Tren) en ModelChoiceField vinculado a Tren
        self.fields['bs8'] = forms.ModelChoiceField(
            queryset=Tren.objects.all().order_by('codigo'),
            required=False,
            label='Tren de Aseo',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs8'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs8:
            try:
                from decimal import Decimal
                codigo_bs8 = Decimal(str(self.instance.bs8))
                tren_initial = Tren.objects.get(codigo=codigo_bs8)
                self.fields['bs8'].initial = tren_initial
            except (Tren.DoesNotExist, ValueError, Exception):
                pass
        
        # Convertir bs9 (Adicionales) en ModelChoiceField vinculado a Adicionales
        self.fields['bs9'] = forms.ModelChoiceField(
            queryset=Adicionales.objects.all().order_by('codigo'),
            required=False,
            label='Servicios Adicionales',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bs9'}),
            empty_label='Seleccione un servicio...',
            to_field_name='codigo'
        )
        
        if self.instance and self.instance.pk and self.instance.bs9:
            try:
                from decimal import Decimal
                codigo_bs9 = Decimal(str(self.instance.bs9))
                adicionales_initial = Adicionales.objects.get(codigo=codigo_bs9)
                self.fields['bs9'].initial = adicionales_initial
            except (Adicionales.DoesNotExist, ValueError, Exception):
                pass
        
        # Formatear fechas para inputs HTML5 de tipo date (YYYY-MM-DD)
        # Esto asegura que las fechas se muestren correctamente al recargar el formulario
        if self.instance and self.instance.pk:
            from datetime import date, datetime
            
            # Fecha Adquisición (fechaadqui)
            if hasattr(self.instance, 'fechaadqui') and self.instance.fechaadqui:
                try:
                    fecha_value = self.instance.fechaadqui
                    if isinstance(fecha_value, date):
                        self.fields['fechaadqui'].initial = fecha_value.strftime('%Y-%m-%d')
                    elif isinstance(fecha_value, str) and fecha_value.strip():
                        # Intentar parsear diferentes formatos de fecha
                        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y']:
                            try:
                                if ' ' in fmt:
                                    fecha_parsed = datetime.strptime(fecha_value, fmt).date()
                                else:
                                    fecha_parsed = datetime.strptime(fecha_value, fmt).date()
                                self.fields['fechaadqui'].initial = fecha_parsed.strftime('%Y-%m-%d')
                                break
                            except ValueError:
                                continue
                except (ValueError, AttributeError, TypeError, Exception) as e:
                    # Si no se puede parsear, dejar que Django maneje el valor
                    pass
            
            # Fecha Delimitación (fedeli)
            if hasattr(self.instance, 'fedeli') and self.instance.fedeli:
                try:
                    fecha_value = self.instance.fedeli
                    if isinstance(fecha_value, date):
                        self.fields['fedeli'].initial = fecha_value.strftime('%Y-%m-%d')
                    elif isinstance(fecha_value, str) and fecha_value.strip():
                        # Intentar parsear diferentes formatos de fecha
                        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y']:
                            try:
                                if ' ' in fmt:
                                    fecha_parsed = datetime.strptime(fecha_value, fmt).date()
                                else:
                                    fecha_parsed = datetime.strptime(fecha_value, fmt).date()
                                self.fields['fedeli'].initial = fecha_parsed.strftime('%Y-%m-%d')
                                break
                            except ValueError:
                                continue
                except (ValueError, AttributeError, TypeError, Exception) as e:
                    # Si no se puede parsear, dejar que Django maneje el valor
                    pass
            
            # Fecha Calculo (Bfecal)
            if hasattr(self.instance, 'Bfecal') and self.instance.Bfecal:
                try:
                    fecha_value = self.instance.Bfecal
                    if isinstance(fecha_value, date):
                        self.fields['Bfecal'].initial = fecha_value.strftime('%Y-%m-%d')
                    elif isinstance(fecha_value, str) and fecha_value.strip():
                        # Intentar parsear diferentes formatos de fecha
                        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y']:
                            try:
                                if ' ' in fmt:
                                    fecha_parsed = datetime.strptime(fecha_value, fmt).date()
                                else:
                                    fecha_parsed = datetime.strptime(fecha_value, fmt).date()
                                self.fields['Bfecal'].initial = fecha_parsed.strftime('%Y-%m-%d')
                                break
                            except ValueError:
                                continue
                except (ValueError, AttributeError, TypeError, Exception) as e:
                    # Si no se puede parsear, dejar que Django maneje el valor
                    pass
        
        # Establecer fecha sistema
        if not self.instance or not self.instance.pk:
            from django.utils import timezone
            self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        elif self.instance and self.instance.pk and self.instance.fechasys:
            self.fields['fechasys'].initial = self.instance.fechasys.strftime('%Y-%m-%d %H:%M:%S')
        else:
            from django.utils import timezone
            self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def clean_bs1(self):
        """Limpia el campo bs1 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs1 = self.cleaned_data.get('bs1')
        if bs1:
            # Con to_field_name='codigo', Django devuelve el Decimal directamente
            if isinstance(bs1, (Decimal, int, float)):
                return str(int(Decimal(str(bs1))))[:4]
            elif isinstance(bs1, Agua):
                return str(int(bs1.codigo))[:4]
            elif isinstance(bs1, str):
                return bs1[:4]
        return '0'
    
    def clean_bs2(self):
        """Limpia el campo bs2 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs2 = self.cleaned_data.get('bs2')
        if bs2:
            if isinstance(bs2, (Decimal, int, float)):
                return str(int(Decimal(str(bs2))))[:4]
            elif isinstance(bs2, Telefono):
                return str(int(bs2.codigo))[:4]
            elif isinstance(bs2, str):
                return bs2[:4]
        return '0'
    
    def clean_bs3(self):
        """Limpia el campo bs3 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs3 = self.cleaned_data.get('bs3')
        if bs3:
            if isinstance(bs3, (Decimal, int, float)):
                return str(int(Decimal(str(bs3))))[:4]
            elif isinstance(bs3, Drenaje):
                return str(int(bs3.codigo))[:4]
            elif isinstance(bs3, str):
                return bs3[:4]
        return '0'
    
    def clean_bs4(self):
        """Limpia el campo bs4 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs4 = self.cleaned_data.get('bs4')
        if bs4:
            if isinstance(bs4, (Decimal, int, float)):
                return str(int(Decimal(str(bs4))))[:4]
            elif isinstance(bs4, Calle):
                return str(int(bs4.codigo))[:4]
            elif isinstance(bs4, str):
                return bs4[:4]
        return '0'
    
    def clean_bs5(self):
        """Limpia el campo bs5 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs5 = self.cleaned_data.get('bs5')
        if bs5:
            if isinstance(bs5, (Decimal, int, float)):
                return str(int(Decimal(str(bs5))))[:4]
            elif isinstance(bs5, Electricidad):
                return str(int(bs5.codigo))[:4]
            elif isinstance(bs5, str):
                return bs5[:4]
        return '0'
    
    def clean_bs6(self):
        """Limpia el campo bs6 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs6 = self.cleaned_data.get('bs6')
        if bs6:
            if isinstance(bs6, (Decimal, int, float)):
                return str(int(Decimal(str(bs6))))[:4]
            elif isinstance(bs6, Acera):
                return str(int(bs6.codigo))[:4]
            elif isinstance(bs6, str):
                return bs6[:4]
        return '0'
    
    def clean_bs7(self):
        """Limpia el campo bs7 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs7 = self.cleaned_data.get('bs7')
        if bs7:
            if isinstance(bs7, (Decimal, int, float)):
                return str(int(Decimal(str(bs7))))[:4]
            elif isinstance(bs7, Alumbrado):
                return str(int(bs7.codigo))[:4]
            elif isinstance(bs7, str):
                return bs7[:4]
        return '0'
    
    def clean_bs8(self):
        """Limpia el campo bs8 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs8 = self.cleaned_data.get('bs8')
        if bs8:
            if isinstance(bs8, (Decimal, int, float)):
                return str(int(Decimal(str(bs8))))[:4]
            elif isinstance(bs8, Tren):
                return str(int(bs8.codigo))[:4]
            elif isinstance(bs8, str):
                return bs8[:4]
        return '0'
    
    def clean_bs9(self):
        """Limpia el campo bs9 para asegurar que solo se guarde el código"""
        from decimal import Decimal
        bs9 = self.cleaned_data.get('bs9')
        if bs9:
            if isinstance(bs9, (Decimal, int, float)):
                return str(int(Decimal(str(bs9))))[:4]
            elif isinstance(bs9, Adicionales):
                return str(int(bs9.codigo))[:4]
            elif isinstance(bs9, str):
                return bs9[:4]
        return None  # bs9 puede ser NULL según el modelo
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        from django.utils import timezone
        from decimal import Decimal
        
        # Asegurar que todos los campos bs solo guarden el código
        bs_fields = {
            'bs1': Agua,
            'bs2': Telefono,
            'bs3': Drenaje,
            'bs4': Calle,
            'bs5': Electricidad,
            'bs6': Acera,
            'bs7': Alumbrado,
            'bs8': Tren,
            'bs9': Adicionales,
        }
        
        for field_name, model_class in bs_fields.items():
            if field_name in self.cleaned_data:
                field_value = self.cleaned_data[field_name]
                if field_value:
                    if isinstance(field_value, (Decimal, int, float)):
                        instance_value = str(int(Decimal(str(field_value))))[:4]
                    elif isinstance(field_value, model_class):
                        instance_value = str(int(field_value.codigo))[:4]
                    else:
                        instance_value = str(field_value)[:4]
                    setattr(instance, field_name, instance_value)
                else:
                    # bs9 puede ser NULL, los demás campos tienen valor por defecto '0'
                    if field_name == 'bs9':
                        setattr(instance, field_name, None)
                    else:
                        setattr(instance, field_name, '0')
        
        # Establecer usuario y fechasys
        if not instance.usuario:
            # El usuario se establecerá en la vista
            pass
        if not instance.fechasys:
            instance.fechasys = timezone.now()
        
        if commit:
            instance.save()
        return instance

class ComentariosCatastroForm(forms.ModelForm):
    """Formulario para comentarios de catastro"""
    
    class Meta:
        model = ComentariosCatastro
        fields = ['comentario', 'usuario', 'fecha']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Ingrese el comentario...',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'comentario': 'Comentario',
            'usuario': 'Usuario',
            'fecha': 'Fecha',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fecha'].initial = fecha_sistema
        
        self.fields['usuario'].required = False
        self.fields['fecha'].required = False

class ColindantesForm(forms.ModelForm):
    """Formulario para colindantes del predio"""
    
    TIPO_CHOICES = [
        ('N', 'N - Norte'),
        ('S', 'S - Sur'),
        ('E', 'E - Este'),
        ('O', 'O - Oeste'),
    ]
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Colindancia',
        required=True
    )
    
    class Meta:
        model = Colindantes
        fields = ['empresa', 'cocata1', 'tipo', 'colindante', 'codcolinda', 'usuario', 'fechasys']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'cocata1': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20', 'readonly': True}),
            'colindante': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '200'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'readonly': True}),
            'fechasys': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'type': 'text'}),
        }
        labels = {
            'empresa': 'Municipio',
            'cocata1': 'Clave Catastral',
            'colindante': 'Colindante',
            'codcolinda': 'Código Colindante',
            'usuario': 'Usuario',
            'fechasys': 'Fecha Sistema',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        cocata1 = kwargs.pop('cocata1', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa y cocata1 si se proporcionan
        if empresa:
            self.fields['empresa'].initial = empresa
        if cocata1:
            self.fields['cocata1'].initial = cocata1
        
        # Hacer campos requeridos
        self.fields['cocata1'].required = True
        
        # Convertir codcolinda en ModelChoiceField vinculado a Colindancias
        self.fields['codcolinda'] = forms.ModelChoiceField(
            queryset=Colindancias.objects.all().order_by('codigo'),
            required=False,
            label='Código Colindante',
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_codcolinda'}),
            empty_label='Seleccione un código...',
            to_field_name='codigo'
        )
        
        # Establecer valor inicial si existe una instancia
        if self.instance and self.instance.pk and self.instance.codcolinda:
            try:
                colindancia_initial = Colindancias.objects.get(codigo=self.instance.codcolinda)
                self.fields['codcolinda'].initial = colindancia_initial
            except (Colindancias.DoesNotExist, ValueError, Exception):
                pass
        
        # Establecer fecha sistema
        if not self.instance or not self.instance.pk:
            from django.utils import timezone
            self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        elif self.instance and self.instance.pk and self.instance.fechasys:
            self.fields['fechasys'].initial = self.instance.fechasys.strftime('%Y-%m-%d %H:%M:%S')
        else:
            from django.utils import timezone
            self.fields['fechasys'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def clean_codcolinda(self):
        """Limpia el campo codcolinda para asegurar que solo se guarde el código"""
        codcolinda = self.cleaned_data.get('codcolinda')
        if codcolinda:
            # Con to_field_name='codigo', Django puede devolver el objeto o el código directamente
            if isinstance(codcolinda, Colindancias):
                return codcolinda.codigo[:2]  # codcolinda es CHAR(2) en Colindantes
            elif isinstance(codcolinda, str):
                return codcolinda[:2]
        return None  # codcolinda puede ser NULL según el modelo
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        from django.utils import timezone
        
        # Guardar solo el código de codcolinda usando el valor limpiado
        if 'codcolinda' in self.cleaned_data:
            instance.codcolinda = self.cleaned_data['codcolinda']
        
        # Establecer usuario y fechasys
        if not instance.usuario:
            # El usuario se establecerá en la vista
            pass
        if not instance.fechasys:
            instance.fechasys = timezone.now()
        
        if commit:
            instance.save()
        return instance

class ComentariosCatastroForm(forms.ModelForm):
    """Formulario para comentarios de catastro"""
    
    class Meta:
        model = ComentariosCatastro
        fields = ['comentario', 'usuario', 'fecha']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Ingrese el comentario...',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'comentario': 'Comentario',
            'usuario': 'Usuario',
            'fecha': 'Fecha',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fecha'].initial = fecha_sistema
        
        self.fields['usuario'].required = False
        self.fields['fecha'].required = False


class CopropietariosForm(forms.ModelForm):
    """Formulario para copropietarios del predio"""
    
    class Meta:
        model = Copropietarios
        fields = ['empresa', 'cocata1', 'identidad', 'nombre', 'porcentaje']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4', 'readonly': True}),
            'cocata1': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20', 'readonly': True}),
            'identidad': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '18'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '99999.99'}),
        }
        labels = {
            'empresa': 'Municipio',
            'cocata1': 'Clave Catastral',
            'identidad': 'Identidad (DNI)',
            'nombre': 'Nombre',
            'porcentaje': 'Porcentaje (%)',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        cocata1 = kwargs.pop('cocata1', None)
        super().__init__(*args, **kwargs)
        
        # Establecer empresa y cocata1 si se proporcionan
        if empresa:
            self.fields['empresa'].initial = empresa
        if cocata1:
            self.fields['cocata1'].initial = cocata1
        
        # Hacer campos requeridos
        self.fields['cocata1'].required = True
        self.fields['nombre'].required = True
    
    def clean_porcentaje(self):
        """Valida que el porcentaje esté en un rango válido"""
        porcentaje = self.cleaned_data.get('porcentaje')
        if porcentaje is not None:
            if porcentaje < 0 or porcentaje > 99999.99:
                raise forms.ValidationError('El porcentaje debe estar entre 0 y 99999.99.')
        return porcentaje
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Establecer empresa y cocata1 si no están establecidos
        if not instance.empresa and self.cleaned_data.get('empresa'):
            instance.empresa = self.cleaned_data['empresa']
        if not instance.cocata1 and self.cleaned_data.get('cocata1'):
            instance.cocata1 = self.cleaned_data['cocata1'] or ''
        
        if commit:
            instance.save()
        return instance

class ComentariosCatastroForm(forms.ModelForm):
    """Formulario para comentarios de catastro"""
    
    class Meta:
        model = ComentariosCatastro
        fields = ['comentario', 'usuario', 'fecha']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Ingrese el comentario...',
                'required': True
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'maxlength': '50'
            }),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'type': 'text'
                },
                format='%Y-%m-%d %H:%M:%S'
            ),
        }
        labels = {
            'comentario': 'Comentario',
            'usuario': 'Usuario',
            'fecha': 'Fecha',
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', '')
        clave = kwargs.pop('clave', '')
        usuario = kwargs.pop('usuario', '')
        fecha_sistema = kwargs.pop('fecha_sistema', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['usuario'].initial = usuario[:50]
        if fecha_sistema:
            self.fields['fecha'].initial = fecha_sistema
        
        self.fields['usuario'].required = False
        self.fields['fecha'].required = False


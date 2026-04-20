from django import forms
from .models import PagoVariosTemp, Actividad, Oficina, usuario, Municipio, Rubro, PlanArbitrio, Anos, Tarifas, TarifasICS, DeclaracionVolumen

class DynamicChoiceField(forms.ChoiceField):
    """
    Campo ChoiceField personalizado que no valida contra las opciones iniciales
    ya que estas se cargan dinámicamente via AJAX
    """
    def validate(self, value):
        """Sobrescribir validación para no validar contra opciones estáticas"""
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'], code='required')
        # No validar contra self.choices ya que se cargan dinámicamente

class LoginForm(forms.Form):
    usuario = forms.CharField(
        max_length=150,
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password'
        })
    )
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all().order_by('codigo'),
        label='Municipio',
        empty_label="Seleccione un municipio",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'municipio-select'
        })
    )

class UsuarioRegistrationForm(forms.ModelForm):
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código de municipio'
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su contraseña'
        })
    )
    
    class Meta:
        model = usuario
        fields = [
            'empresa', 'usuario', 'password', 'nombre'
        ]
        widgets = {
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if commit:
            user.save()
        return user

class UsuarioUpdateForm(forms.ModelForm):
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código de municipio'
        })
    )
    
    class Meta:
        model = usuario
        fields = [
            'empresa', 'usuario', 'nombre'
        ]
        widgets = {
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            })
        }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña actual'
        })
    )
    new_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su nueva contraseña'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Las nuevas contraseñas no coinciden.")
        
        return cleaned_data

class PagoVariosForm(forms.ModelForm):
    class Meta:
        model = PagoVariosTemp
        fields = ['identidad', 'nombre', 'fecha']
        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'id_nombre'}),
            'identidad': forms.TextInput(),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class ConceptoForm(forms.Form):
    empresa = forms.CharField(max_length=4, label="Municipio")
    codigo = forms.CharField(max_length=20, label="Código")
    descripcion = forms.CharField(max_length=200, required=False, label="Descripción")
    cantidad = forms.DecimalField(max_digits=12, decimal_places=2, label="Cantidad")
    vl_unit = forms.DecimalField(max_digits=12, decimal_places=2, label="Valor Unitario")
    valor = forms.DecimalField(max_digits=12, decimal_places=2, required=True, label="Total")

class ActividadForm(forms.ModelForm):
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        })
    )
    
    class Meta:
        model = Actividad
        fields = ['empresa', 'codigo', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={'maxlength': 20}),
            'descripcion': forms.Textarea(attrs={'maxlength': 200, 'rows': 2, 'style': 'resize:vertical; width:100%; min-width:300px;'}),
        }

class OficinaForm(forms.ModelForm):
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        })
    )
    
    class Meta:
        model = Oficina
        fields = ['empresa', 'codigo', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={'maxlength': 20}),
            'descripcion': forms.Textarea(attrs={'maxlength': 200, 'rows': 2, 'style': 'resize:vertical; width:100%; min-width:300px;'}),
        }

class RubroForm(forms.ModelForm):
    # Explicitly define required fields
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        })
    )
    descripcion = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': 200,
            'placeholder': 'Ingrese descripción del rubro',
            'required': 'required',
            'class': 'form-control'
        })
    )
    cuenta = forms.CharField(
        max_length=20,
        required=True
    )
    cuentarez = forms.CharField(
        max_length=20,
        required=True
    )
    tipo = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.Select(attrs={
            'required': 'required',
            'class': 'form-control'
        }, choices=[
            ('', 'Seleccione tipo'),
            ('I', 'Impuestos'),
            ('T', 'Tasas'),
        ])
    )
    
    class Meta:
        model = Rubro
        fields = ['empresa', 'codigo', 'descripcion', 'cuenta', 'cuentarez', 'tipo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'maxlength': 4,
                'style': 'text-transform: uppercase;'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # Validación mínima - solo verificar que los campos requeridos estén presentes
        # La lógica de duplicados se maneja completamente en el modelo
        return cleaned_data
    
    def validate_unique(self):
        """
        Deshabilitar la validación única a nivel de formulario
        ya que se maneja en el modelo
        """
        pass

class PlanArbitrioForm(forms.ModelForm):
    """
    Formulario para el Plan de Arbitrio
    """
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        })
    )
    rubro = forms.CharField(
        max_length=4,
        label="Rubro",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d; text-transform: uppercase;',
            'placeholder': ''
        })
    )

    cod_tarifa = forms.CharField(
        max_length=4,
        label="Código de Tarifa",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d; text-transform: uppercase;',
            'placeholder': ''
        })
    )
    ano = forms.DecimalField(
        max_digits=4,
        decimal_places=0,
        label="Año",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;',
            'placeholder': '2024',
            'inputmode': 'numeric',
            'pattern': '^\\d{4}$',
            'maxlength': '4'
        })
    )
    codigo = forms.CharField(
        max_length=20,
        label="Código",
        widget=forms.TextInput(attrs={
            'maxlength': 20,
            'class': 'form-control',
            'style': 'text-transform: uppercase;',
            'placeholder': 'Ingrese código para búsqueda automática'
        })
    )
    descripcion = forms.CharField(
        max_length=200,
        label="Descripción",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 200,
            'placeholder': ''
        })
    )
    minimo = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor Mínimo",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'decimal',
            'pattern': '^\\d{1,10}(\\.\\d{1,2})?$',
            'data-format': 'decimal-10-2',
            'maxlength': '13'
        })
    )
    maximo = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor Máximo",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'decimal',
            'pattern': '^\\d{1,10}(\\.\\d{1,2})?$',
            'data-format': 'decimal-10-2',
            'maxlength': '13'
        })
    )
    valor = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor de la Tarifa",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'decimal',
            'pattern': '^\\d{1,10}(\\.\\d{1,2})?$',
            'data-format': 'decimal-10-2',
            'maxlength': '13'
        })
    )

    
    class Meta:
        model = PlanArbitrio
        fields = [
            'empresa', 'rubro', 'cod_tarifa', 'ano', 'codigo', 'descripcion', 
            'minimo', 'maximo', 'valor'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def clean_minimo(self):
        minimo = self.cleaned_data.get('minimo')
        if minimo is not None and minimo < 0:
            raise forms.ValidationError("El valor mínimo debe ser mayor o igual a cero.")
        return minimo

    def clean_maximo(self):
        maximo = self.cleaned_data.get('maximo')
        if maximo is not None and maximo <= 0:
            raise forms.ValidationError("El valor máximo debe ser mayor a cero.")
        return maximo

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor < 0:
            raise forms.ValidationError("El valor no puede ser negativo.")
        return valor

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')
        codigo = cleaned_data.get('codigo')
        ano = cleaned_data.get('ano')
        rubro = cleaned_data.get('rubro')
        cod_tarifa = cleaned_data.get('cod_tarifa')
        minimo = cleaned_data.get('minimo')
        maximo = cleaned_data.get('maximo')
        
        # Validar año
        if ano and (ano < 2020 or ano > 2030):
            raise forms.ValidationError("El año debe estar entre 2020 y 2030")
        
        # Validar que el mínimo no sea mayor que el máximo
        if minimo is not None and maximo is not None and minimo > maximo:
            raise forms.ValidationError("El valor mínimo no puede ser mayor que el valor máximo.")
        
        # Validar que no exista un plan para los mismos criterios únicos
        # SOLO para nuevos registros, no para actualizaciones
        # Verificar si es una actualización mediante el campo is_update
        is_update = self.data.get('is_update', '') == 'true'
        
        if empresa and rubro and cod_tarifa and ano and codigo and not self.instance.pk and not is_update:
            # La validación de duplicados se maneja en la vista, no en el formulario
            # Esto permite que la vista decida si actualizar o crear un nuevo registro
            pass
        
        return cleaned_data

class TarifasForm(forms.ModelForm):
    """
    Formulario para las Tarifas
    """
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        }),
        initial=''
    )
    rubro = forms.CharField(
        max_length=4,
        label="Rubro",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d; text-transform: uppercase;',
            'placeholder': ''
        })
    )
    cod_tarifa = forms.CharField(
        max_length=4,
        label="Código de Tarifa",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'style': 'text-transform: uppercase;',
            'placeholder': ''
        })
    )
    descripcion = forms.CharField(
        max_length=200,
        label="Descripción",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 200,
            'placeholder': ''
        })
    )
    valor = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor",
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'max': '999999999.99',
            'placeholder': '0.00'
        })
    )
    frecuencia = forms.CharField(
        max_length=1,
        label="Frecuencia",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }, choices=[
            ('', 'Seleccione frecuencia'),
            ('A', 'Anual'),
            ('M', 'Mensual'),
        ])
    )
    tipo = forms.CharField(
        max_length=1,
        label="Tipo",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }, choices=[
            ('', 'Seleccione tipo'),
            ('F', 'Fija'),
            ('V', 'Variable'),
        ])
    )
    categoria = forms.CharField(
        max_length=1,
        label="Categoría",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }, choices=[
            ('', 'Seleccione categoría'),
            ('D', 'Doméstico'),
            ('C', 'Comercial'),
        ])
    )
    
    ano = forms.DecimalField(
        max_digits=4,
        decimal_places=0,
        label="Año",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'ano-select'
        }, choices=[])
    )
    
    class Meta:
        model = Tarifas
        fields = [
            'empresa', 'rubro', 'ano', 'cod_tarifa', 'descripcion', 
            'valor', 'frecuencia', 'tipo', 'categoria'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar las opciones del combobox de años desde la tabla Anos
        try:
            anos_choices = [('', 'Seleccione un año')] + [
                (str(ano.ano), str(ano.ano)) 
                for ano in Anos.objects.all().order_by('-ano')
            ]
            self.fields['ano'].widget.choices = anos_choices
        except Exception as e:
            # Si hay error, usar años por defecto
            anos_choices = [('', 'Seleccione un año')] + [
                (str(year), str(year)) for year in range(2030, 2019, -1)
            ]
            self.fields['ano'].widget.choices = anos_choices
    
    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')
        ano = cleaned_data.get('ano')
        valor = cleaned_data.get('valor')
        tipo = cleaned_data.get('tipo')
        rubro = cleaned_data.get('rubro')
        cod_tarifa = cleaned_data.get('cod_tarifa')
        
        # Validar valor según el tipo
        if tipo == 'F' and (not valor or valor <= 0):
            raise forms.ValidationError("El valor es obligatorio cuando el tipo es Fija")
        
        # ✅ NUEVA VALIDACIÓN: Código de tarifa máximo 4 caracteres
        if cod_tarifa and len(cod_tarifa) > 4:
            raise forms.ValidationError("El código de tarifa no puede exceder 4 caracteres")
        
        # Validar que el código de tarifa no esté vacío si se proporciona
        if cod_tarifa and len(cod_tarifa.strip()) == 0:
            raise forms.ValidationError("El código de tarifa no puede estar vacío")
        
        # Validar campos obligatorios al grabar
        if not empresa:
            raise forms.ValidationError("El código de municipio es obligatorio")
        
        if not rubro:
            raise forms.ValidationError("El código de rubro es obligatorio")
        
        if not ano:
            raise forms.ValidationError("El año es obligatorio")
        
        if not cod_tarifa:
            raise forms.ValidationError("El código de tarifa es obligatorio")
        
        # Validar frecuencia obligatoria
        frecuencia = cleaned_data.get('frecuencia')
        if not frecuencia:
            raise forms.ValidationError("La frecuencia es obligatoria")
        
        # Validar tipo obligatorio
        tipo = cleaned_data.get('tipo')
        if not tipo:
            raise forms.ValidationError("El tipo es obligatorio")
        
        # Validar categoría obligatoria
        categoria = cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError("La categoría es obligatoria")
        
        # NO validar duplicados aquí - se maneja en la vista
        # Esto evita que Django valide automáticamente la restricción unique_together
        
        return cleaned_data
    
    def validate_unique(self):
        """
        Deshabilitar la validación única a nivel de formulario
        ya que se maneja en el modelo y la vista
        """
        pass
    
    def save(self, commit=True):
        """
        Sobrescribir el método save para evitar la validación automática de unique_together
        """
        instance = super().save(commit=False)
        
        # Si no es commit, retornar la instancia sin guardar
        if not commit:
            return instance
        
        # Si es commit, intentar guardar pero manejar errores de duplicado
        try:
            instance.save()
            return instance
        except Exception as e:
            # Si hay error de duplicado, no lanzar excepción aquí
            # La vista se encargará de manejar la actualización
            raise e


class TarifasICSForm(forms.ModelForm):
    """
    Formulario para las Tarifas ICS (Configuración de Tasas por Negocio)
    """
    # Campo para seleccionar rubro
    rubro = forms.ChoiceField(
        label="Rubro",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_rubro',
            'style': 'background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 2px solid #dee2e6; border-radius: 8px; padding: 12px; font-size: 1rem; transition: all 0.3s ease;'
        })
    )
    
    # Campo para seleccionar tarifa del rubro
    tarifa_rubro = DynamicChoiceField(
        label="Tarifa del Rubro",
        required=True,
        choices=[],  # Opciones vacías inicialmente
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tarifa_rubro',
            'style': 'background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 2px solid #dee2e6; border-radius: 8px; padding: 12px; font-size: 1rem; transition: all 0.3s ease;'
        })
    )
    
    # Campo para el valor personalizado (opcional)
    valor_personalizado = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor Personalizado",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_valor_personalizado',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0',
            'style': 'background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 2px solid #dee2e6; border-radius: 8px; padding: 12px; font-size: 1rem; transition: all 0.3s ease;'
        })
    )

    class Meta:
        model = TarifasICS
        fields = ['idneg', 'rtm', 'expe', 'cod_tarifa', 'valor']
        widgets = {
            'idneg': forms.HiddenInput(),
            'rtm': forms.HiddenInput(),
            'expe': forms.HiddenInput(),
            'cod_tarifa': forms.HiddenInput(),
            'valor': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer que el campo valor no sea requerido ya que se calcula automáticamente
        self.fields['valor'].required = False
        
        # Cargar las opciones del combobox de rubros
        try:
            from .models import Rubro
            rubros_choices = [('', 'Seleccione un rubro')] + [
                (rubro.codigo, f"{rubro.codigo} - {rubro.descripcion}")
                for rubro in Rubro.objects.all().order_by('codigo')
            ]
            self.fields['rubro'].choices = rubros_choices
        except Exception as e:
            # Si hay error, usar opciones por defecto
            self.fields['rubro'].choices = [('', 'Seleccione un rubro')]
        
        # Inicializar opciones de tarifas vacías
        self.fields['tarifa_rubro'].choices = [('', 'Seleccione primero un rubro')]
    
    def clean(self):
        cleaned_data = super().clean()
        rubro = cleaned_data.get('rubro')
        tarifa_rubro = cleaned_data.get('tarifa_rubro')
        valor_personalizado = cleaned_data.get('valor_personalizado')
        
        # Validar que se haya seleccionado un rubro
        if not rubro:
            raise forms.ValidationError("Debe seleccionar un rubro")
        
        # Validar que se haya seleccionado una tarifa del rubro
        if not tarifa_rubro:
            raise forms.ValidationError("Debe seleccionar una tarifa del rubro")
        
        # Validar que el valor personalizado sea positivo si se proporciona
        if valor_personalizado and valor_personalizado <= 0:
            raise forms.ValidationError("El valor personalizado debe ser mayor a 0")
        
        return cleaned_data
    
    def clean_tarifa_rubro(self):
        """Validación personalizada para el campo tarifa_rubro"""
        tarifa_rubro = self.cleaned_data.get('tarifa_rubro')
        if tarifa_rubro:
            # No validar contra las opciones del formulario ya que se cargan dinámicamente
            # Solo validar que no esté vacío y que sea un valor válido
            if tarifa_rubro.strip():
                return tarifa_rubro
        return tarifa_rubro

class DeclaracionVolumenForm(forms.ModelForm):
    """Formulario para declaración de volumen de ventas"""
    
    class Meta:
        model = DeclaracionVolumen
        fields = [
            'idneg', 'rtm', 'expe', 'ano', 'tipo', 'mes',
            'ventai', 'ventac', 'ventas', 'valorexcento', 'controlado',
            'unidad', 'factor', 'impuesto'
        ]
        widgets = {
            'idneg': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'placeholder': 'ID del negocio'
            }),
            'rtm': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'placeholder': 'RTM'
            }),
            'expe': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'placeholder': 'Expediente'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2020',
                'max': '2030',
                'step': '1',
                'placeholder': 'Año'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Seleccione tipo'),
                (1, 'Normal'),
                (2, 'Apertura')
            ]),
            'mes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '12',
                'step': '1',
                'placeholder': 'Mes'
            }),
            'ventai': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': '^\\d{1,14}(\\.\\d{0,2})?$',
                'data-format': 'decimal-16-2',
                'maxlength': '17'
            }),
            'ventac': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': '^\\d{1,14}(\\.\\d{0,2})?$',
                'data-format': 'decimal-16-2',
                'maxlength': '17'
            }),
            'ventas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': '^\\d{1,14}(\\.\\d{0,2})?$',
                'data-format': 'decimal-16-2',
                'maxlength': '17'
            }),
            'valorexcento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': '^\\d{1,14}(\\.\\d{0,2})?$',
                'data-format': 'decimal-16-2',
                'maxlength': '17'
            }),
            'controlado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'inputmode': 'decimal',
                'pattern': '^\\d{1,14}(\\.\\d{0,2})?$',
                'data-format': 'decimal-16-2',
                'maxlength': '17'
            }),
            'unidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'min': '0',
                'placeholder': '0',
                'id': 'id_unidad',
                'maxlength': '11',
                'pattern': '^\\d{1,11}$',
                'inputmode': 'numeric',
                'data-format': 'integer-11'
            }),
            'factor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'id': 'id_factor',
                'maxlength': '13',
                'pattern': '^\\d{1,10}(\\.\\d{0,2})?$',
                'inputmode': 'decimal',
                'data-format': 'decimal-10-2'
            }),
            'impuesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'readonly': True,
                'id': 'id_impuesto',
                'style': 'background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border: 2px solid #ff9800; color: #e65100; font-weight: 700; text-align: center;'
            })
        }
        labels = {
            'idneg': 'ID Negocio',
            'rtm': 'RTM',
            'expe': 'Expediente',
            'ano': 'Año',
            'tipo': 'Tipo de Declaración',
            'mes': 'Mes',
            'ventai': 'Ventas Rubro Producción',
            'ventac': 'Ventas Mercadería',
            'ventas': 'Ventas por Servicios',
            'valorexcento': 'Valores Exentos',
            'controlado': 'Ventas Productos Controlados',
            'unidad': 'Unidad',
            'factor': 'Factor',
            'impuesto': 'Impuesto Calculado'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Establecer valores por defecto
        if not self.instance.pk:
            from datetime import datetime
            current_year = datetime.now().year
            current_month = datetime.now().month
            
            self.fields['ano'].initial = current_year
            self.fields['mes'].initial = current_month
            self.fields['tipo'].initial = 1  # Normal por defecto
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que al menos uno de los campos de ventas tenga valor
        ventai = cleaned_data.get('ventai', 0) or 0
        ventac = cleaned_data.get('ventac', 0) or 0
        ventas = cleaned_data.get('ventas', 0) or 0
        valorexcento = cleaned_data.get('valorexcento', 0) or 0
        controlado = cleaned_data.get('controlado', 0) or 0
        
        total_ventas = ventai + ventac + ventas + valorexcento + controlado
        
        if total_ventas <= 0:
            raise forms.ValidationError(
                "Al menos uno de los campos de ventas debe tener un valor mayor a 0."
            )
        
        return cleaned_data

class PlanArbitrioForm(forms.ModelForm):
    """Formulario para Plan de Arbitrio"""
    
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        }),
        initial=''
    )
    
    rubro = forms.CharField(
        max_length=4,
        label="Rubro",
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'placeholder': 'Código del rubro'
        })
    )
    
    cod_tarifa = forms.CharField(
        max_length=4,
        label="Código de Tarifa",
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'placeholder': 'Código de tarifa'
        })
    )
    
    ano = forms.DecimalField(
        max_digits=4,
        decimal_places=0,
        label="Año",
        required=True,
        widget=forms.NumberInput(attrs={
            'min': '2020',
            'max': '2030',
            'step': '1',
            'placeholder': 'Año'
        })
    )
    
    codigo = forms.CharField(
        max_length=20,
        label="Código",
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': 20,
            'placeholder': 'Código del plan'
        })
    )
    
    descripcion = forms.CharField(
        max_length=200,
        label="Descripción",
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': 200,
            'placeholder': 'Descripción del plan'
        })
    )
    
    minimo = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor Mínimo",
        required=True,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'placeholder': '0.00'
        })
    )
    
    maximo = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor Máximo",
        required=True,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'placeholder': '0.00'
        })
    )
    
    valor = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor",
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;',
            'placeholder': '0.00'
        })
    )
    
    class Meta:
        model = PlanArbitrio
        fields = [
            'empresa', 'rubro', 'cod_tarifa', 'ano', 'codigo', 
            'descripcion', 'minimo', 'maximo', 'valor'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si se proporciona initial_data, usarlo
        if 'initial' in kwargs:
            initial = kwargs['initial']
            if 'empresa' in initial:
                self.fields['empresa'].initial = initial['empresa']
    
    def clean(self):
        cleaned_data = super().clean()
        minimo = cleaned_data.get('minimo')
        maximo = cleaned_data.get('maximo')
        
        # Calcular valor automáticamente como promedio
        if minimo is not None and maximo is not None:
            if minimo > maximo:
                raise forms.ValidationError("El valor mínimo no puede ser mayor que el máximo")
            cleaned_data['valor'] = (minimo + maximo) / 2
        
        return cleaned_data


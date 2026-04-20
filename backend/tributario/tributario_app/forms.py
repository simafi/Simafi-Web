from django import forms
from typing import TYPE_CHECKING

# Models moved to modular system - import from core and tributario modules
from core.models import Municipio
from usuarios.models import Usuario as usuario
from tributario.models import Actividad, Rubro, Oficina, TarifasICS, DeclaracionVolumen, TipoCategoria

# Para type checking
if TYPE_CHECKING:
    from django.db.models import QuerySet, Manager

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
        queryset=getattr(Municipio, 'objects').all().order_by('codigo'),
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

# PagoVariosForm disabled - model moved to modular system
# class PagoVariosForm(forms.ModelForm):
#     class Meta:
#         model = PagoVariosTemp
#         fields = ['identidad', 'nombre', 'fecha']
#         widgets = {
#             'nombre': forms.TextInput(attrs={'id': 'id_nombre'}),
#             'identidad': forms.TextInput(),
#             'fecha': forms.DateInput(attrs={'type': 'date'})}

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
            'descripcion': forms.Textarea(attrs={'maxlength': 200, 'rows': 2, 'style': 'resize:vertical; width:100%; min-width:300px;'})}

class OficinaForm(forms.Form):
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        })
    )
    codigo = forms.CharField(
        max_length=20,
        label="Código",
        widget=forms.TextInput(attrs={'maxlength': 20})
    )
    descripcion = forms.CharField(
        max_length=200,
        label="Descripción",
        widget=forms.Textarea(attrs={'maxlength': 200, 'rows': 2, 'style': 'resize:vertical; width:100%; min-width:300px;'})
    )

class RubroForm(forms.ModelForm):
    # Explicitly define required fields
    empresa = forms.CharField(
        max_length=4,
        label="Municipio",
        required=True,
        widget=forms.TextInput(attrs={
            'maxlength': 4,
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; color: #6c757d;'
        })
    )
    descripcion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 200,
            'placeholder': 'Ingrese descripción del rubro',
            'class': 'form-control'
        })
    )
    cuenta = forms.CharField(
        max_length=20,
        required=False
    )
    cuentarez = forms.CharField(
        max_length=20,
        required=False
    )
    tipo = forms.ChoiceField(
        required=True,
        choices=[
            ('', 'Seleccione tipo'),
            ('I', 'Impuestos'),
            ('T', 'Tasas')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        error_messages={
            'required': 'El campo Tipo es obligatorio. Debe seleccionar si es Impuesto o Tasa.'
        }
    )
    
    class Meta:
        model = Rubro
        fields = ['empresa', 'codigo', 'descripcion', 'cuenta', 'cuentarez', 'tipo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'maxlength': 6,
                'style': 'text-transform: uppercase;'
            })}
    
    def clean_codigo(self):
        """Convertir código de rubro a mayúsculas"""
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            return codigo.upper().strip()
        return codigo
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validación de campos obligatorios
        empresa = cleaned_data.get('empresa')
        codigo = cleaned_data.get('codigo')
        
        if not empresa:
            raise forms.ValidationError("El campo Municipio es obligatorio.")
        
        if not codigo:
            raise forms.ValidationError("El campo Código de Rubro es obligatorio.")
        
        # Asegurar que el código esté en mayúsculas
        if codigo:
            cleaned_data['codigo'] = codigo.upper().strip()
        
        # El campo 'tipo' se valida automáticamente por ser ChoiceField required
        # No es necesario validarlo aquí para evitar mensajes duplicados
        
        # Normalizar campos opcionales a string vacío si son None
        if cleaned_data.get('descripcion') is None:
            cleaned_data['descripcion'] = ''
        if cleaned_data.get('cuenta') is None:
            cleaned_data['cuenta'] = ''
        if cleaned_data.get('cuentarez') is None:
            cleaned_data['cuentarez'] = ''
        
        return cleaned_data
    
    def validate_unique(self):
        """
        Deshabilitar la validación única a nivel de formulario
        ya que se maneja en el modelo
        """
        pass

class PlanArbitrioForm(forms.Form):
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
        max_length=6,
        label="Rubro",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 6,
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
    tipocat = forms.ChoiceField(
        label="Categoría",
        required=False,
        choices=[],  # Se llenará dinámicamente desde la base de datos
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipocat',
            'name': 'tipocat'  # Asegurar que tenga el nombre correcto
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener las categorías desde la tabla tipocategoria
        try:
            categorias = TipoCategoria.objects.all().order_by('codigo')
            choices = [('', '---------')]
            for categoria in categorias:
                # Usar el código como valor y mostrar código + descripción
                choices.append((categoria.codigo, f"{categoria.codigo}. {categoria.descripcion}"))
            self.fields['tipocat'].choices = choices
        except Exception as e:
            # Si hay error al cargar, usar valores por defecto
            print(f"Error al cargar categorías desde BD: {e}")
            self.fields['tipocat'].choices = [
                ('', '---------'),
                ('1', '1. Viviendas'),
                ('2', '2. Apartamentos'),
                ('3', '3. Cuarterías'),
            ]
    
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

    def clean_tipocat(self):
        """Limpia y valida el campo tipocat - debe ser solo '1', '2' o '3'"""
        tipocat = self.cleaned_data.get('tipocat', '').strip()
        if tipocat:
            # Extraer solo el número (1, 2 o 3) del valor del select
            import re
            match = re.match(r'^([123])', tipocat)
            if match:
                return match.group(1)  # Retornar solo '1', '2' o '3'
            else:
                # Si no es válido, retornar string vacío o None según sea required
                return ''
        return tipocat
    
    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')
        codigo = cleaned_data.get('codigo')
        ano = cleaned_data.get('ano')
        rubro = cleaned_data.get('rubro')
        cod_tarifa = cleaned_data.get('cod_tarifa')
        minimo = cleaned_data.get('minimo')
        maximo = cleaned_data.get('maximo')
        tipocat = cleaned_data.get('tipocat', '').strip()
        
        # Asegurar que tipocat sea solo '1', '2' o '3'
        if tipocat:
            import re
            match = re.match(r'^([123])', tipocat)
            if match:
                cleaned_data['tipocat'] = match.group(1)
            else:
                cleaned_data['tipocat'] = ''
        
        # Validar año
        if ano and (ano < 2020 or ano > 2030):
            raise forms.ValidationError("El año debe estar entre 2020 y 2030")
        
        # Validar que el mínimo no sea mayor que el máximo
        if minimo is not None and maximo is not None and minimo > maximo:
            raise forms.ValidationError("El valor mínimo no puede ser mayor que el valor máximo.")
        
        return cleaned_data

class TarifasForm(forms.Form):
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
        max_length=6,
        label="Rubro",
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength': 6,
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
            ('M', 'Mensual')])
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
            ('V', 'Variable')])
    )
    tipomodulo = forms.CharField(
        max_length=1,
        label="Tipo Módulo",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }, choices=[
            ('', 'Seleccione tipo módulo'),
            ('D', 'D - Doméstico'),
            ('C', 'C - Comercial')])
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar las opciones del combobox de años
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
        # Para tipo Fija: valor es obligatorio (puede ser 0 para exentas)
        # Para tipo Variable: valor es opcional (se calcula según plan arbitrio)
        if tipo == 'F':
            # Solo validar si el valor está completamente vacío (None o string vacío)
            if valor is None or (isinstance(valor, str) and valor.strip() == ''):
                raise forms.ValidationError("El valor es obligatorio cuando el tipo es Fija. Puede ingresar 0 para tarifas exentas.")
            # Convertir a float si es string
            if isinstance(valor, str):
                try:
                    valor = float(valor)
                    cleaned_data['valor'] = valor
                except ValueError:
                    raise forms.ValidationError("El valor debe ser un número válido")
        
        # Validar que el valor no sea negativo (si se proporciona)
        if valor is not None and valor != '' and float(valor) < 0:
            raise forms.ValidationError("El valor no puede ser negativo")
        
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
        
        # Validar tipo módulo obligatorio
        tipomodulo = cleaned_data.get('tipomodulo')
        if not tipomodulo:
            raise forms.ValidationError("El tipo módulo es obligatorio")
        
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



# NOTA: TarifasICSForm duplicado eliminado (líneas 623-783)
# La versión correcta ModelForm está en la línea 1046


class DeclaracionVolumenForm(forms.ModelForm):
    """Formulario para declaración de volumen de ventas"""
    
    class Meta:
        model = DeclaracionVolumen
        fields = [
            'idneg', 'rtm', 'expe', 'ano', 'tipo', 'mes',
            'ventai', 'ventac', 'ventas', 'valorexcento', 'controlado',
            'unidad', 'factor', 'multadecla', 'impuesto', 'ajuste'
        ]
        # Excluir valor_base de los campos del modelo ya que es calculado
        exclude = []
    
    # Campos adicionales del formulario
    empresa = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'Empresa'
        }),
        label='Empresa',
        required=False
    )
    idneg = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'ID del negocio'
        }),
        label='ID Negocio',
        required=False
    )
    rtm = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'RTM'
        }),
        label='RTM',
        required=False
    )
    expe = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'Expediente'
        }),
        label='Expediente',
        required=False
    )
    ano = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '2020',
            'max': '2030',
            'step': '1',
            'placeholder': 'Año'
        }),
        label='Año',
        required=True
    )
    tipo = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=[
            ('', 'Seleccione tipo'),
            (1, 'Normal'),
            (2, 'Apertura')
        ],
        label='Tipo de Declaración',
        required=True
    )
    mes = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '12',
            'step': '1',
            'placeholder': 'Mes'
        }),
        label='Mes',
        required=True
    )
    ventai = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'text',
            'data-format': 'decimal-16-2',
            'maxlength': '20'
        }),
        label='Ventas Rubro Producción',
        required=False
    )
    ventac = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'text',
            'data-format': 'decimal-16-2',
            'maxlength': '20'
        }),
        label='Ventas Mercadería',
        required=False
    )
    ventas = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'text',
            'data-format': 'decimal-16-2',
            'maxlength': '20'
        }),
        label='Ventas por Servicios',
        required=False
    )
    valorexcento = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'text',
            'data-format': 'decimal-16-2',
            'maxlength': '20'
        }),
        label='Valores Exentos',
        required=False
    )
    controlado = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'inputmode': 'text',
            'data-format': 'decimal-16-2',
            'maxlength': '20'
        }),
        label='Ventas Productos Controlados',
        required=False
    )
    unidad = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0',
            'id': 'id_unidad',
            'maxlength': '11',
            'pattern': '^\\d{1,11}$',
            'inputmode': 'numeric',
            'data-format': 'integer-11'
        }),
        label='Unidad',
        required=False
    )
    factor = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'id': 'id_factor',
            'maxlength': '16',
            'inputmode': 'text',
            'data-format': 'decimal-10-2'
        }),
        label='Factor',
        required=False
    )
    multadecla = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'readonly': True,
            'id': 'id_multadecla',
            'style': 'background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border: 2px solid #ffa000; color: #e65100; font-weight: 700; text-align: center;',
            'title': 'Campo calculado automáticamente según reglas de multa'
        }),
        label='Multa Declaración Tardía',
        required=False
    )
    impuesto = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'readonly': True,
            'id': 'id_impuesto',
            'style': 'background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border: 2px solid #ff9800; color: #e65100; font-weight: 700; text-align: center;'
        }),
        label='Impuesto Calculado',
        required=False
    )
    ajuste = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'id': 'id_ajuste',
            'inputmode': 'text',
            'data-format': 'decimal-12-2',
            'maxlength': '16',
            'style': 'background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border: 2px solid #9c27b0; color: #4a148c; font-weight: 600;'
        }),
        label='Ajuste Interanual',
        required=False
    )
    # Campo calculado para mostrar el valor base (usa la propiedad del modelo)
    valor_base = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'readonly': True,
            'id': 'id_valor_base',
            'style': 'background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); border: 2px solid #4caf50; color: #1b5e20; font-weight: 700; text-align: center; font-size: 16px;',
            'title': 'Valor Base calculado automáticamente (Ventas Totales)'
        }),
        label='Valor Base (Ventas Totales)',
        required=False
    )
    nodecla = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'Número de Declaración'
        }),
        label='Número de Declaración',
        required=False
    )
    usuario = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'Usuario'
        }),
        label='Usuario',
        required=False
    )
    fechssys = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'placeholder': 'Fecha de Registro'
        }),
        label='Fecha de Registro',
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        # Limpiar separadores de miles ANTES de que Django procese los datos
        if args and isinstance(args[0], dict):
            data = args[0].copy()  # Hacer una copia mutable
            campos_numericos = ['ventai', 'ventac', 'ventas', 'valorexcento', 'controlado', 'factor', 'ajuste']
            for campo in campos_numericos:
                if campo in data and data[campo]:
                    # Remover separadores de miles (comas)
                    data[campo] = str(data[campo]).replace(',', '').strip()
            args = (data,) + args[1:]
        
        super().__init__(*args, **kwargs)
        
        # Convertir campos Decimal a int para evitar problemas de validación
        if hasattr(self, 'instance') and self.instance:
            from decimal import Decimal
            # Convertir campos Decimal a int para el formulario
            if hasattr(self.instance, 'ano') and isinstance(self.instance.ano, Decimal):
                self.initial['ano'] = int(self.instance.ano)
            if hasattr(self.instance, 'mes') and isinstance(self.instance.mes, Decimal):
                self.initial['mes'] = int(self.instance.mes)
            if hasattr(self.instance, 'tipo') and isinstance(self.instance.tipo, Decimal):
                self.initial['tipo'] = int(self.instance.tipo)
        
        # Hacer campos calculados opcionales
        self.fields['impuesto'].required = False
        self.fields['multadecla'].required = False
        self.fields['ajuste'].required = False
        self.fields['valor_base'].required = False
        
        # Calcular valor base automáticamente usando la propiedad del modelo
        self._calcular_valor_base()
        
        # Asegurar que el campo valor_base tenga el valor correcto en initial
        if hasattr(self, 'instance') and self.instance and hasattr(self.instance, 'valor_base'):
            self.initial['valor_base'] = float(self.instance.valor_base)
            print(f"Valor base inicializado desde instancia: {self.initial['valor_base']}")
        
        # Hacer campos de ventas opcionales (solo al menos uno debe tener valor)
        self.fields['ventai'].required = False
        self.fields['ventac'].required = False
        self.fields['ventas'].required = False
        self.fields['valorexcento'].required = False
        self.fields['controlado'].required = False
        
        # Hacer campos de unidad y factor opcionales
        self.fields['unidad'].required = False
        self.fields['factor'].required = False
        
        # Hacer idneg opcional (se asignará automáticamente en la vista)
        self.fields['idneg'].required = False
        
        # Establecer valores por defecto si no se pasaron datos iniciales
        if not kwargs.get('initial'):
            from datetime import datetime
            current_year = datetime.now().year
            current_month = datetime.now().month
            
            self.fields['ano'].initial = current_year
            self.fields['mes'].initial = current_month
            self.fields['tipo'].initial = 1  # Normal por defecto
    
    def _calcular_valor_base(self):
        """Calcula el valor base usando la propiedad del modelo o datos del formulario"""
        try:
            from decimal import Decimal
            
            # Inicializar el diccionario initial si no existe
            if not hasattr(self, 'initial') or self.initial is None:
                self.initial = {}
            
            valor_base = 0
            
            # Si hay una instancia del modelo (al editar), usar su propiedad valor_base
            if hasattr(self, 'instance') and self.instance and hasattr(self.instance, 'valor_base'):
                valor_base = float(self.instance.valor_base)
                print(f"Usando propiedad del modelo: {valor_base}")
            else:
                # Si no hay instancia, calcular desde los datos del formulario
                ventai = 0
                ventac = 0
                ventas = 0
                valorexcento = 0
                controlado = 0
                
                # Si hay data (formulario enviado), obtener de ahí
                if hasattr(self, 'data') and self.data:
                    ventai = self.data.get('ventai', 0) or 0
                    ventac = self.data.get('ventac', 0) or 0
                    ventas = self.data.get('ventas', 0) or 0
                    valorexcento = self.data.get('valorexcento', 0) or 0
                    controlado = self.data.get('controlado', 0) or 0
                # Si no, obtener de initial
                elif self.initial:
                    ventai = self.initial.get('ventai', 0) or 0
                    ventac = self.initial.get('ventac', 0) or 0
                    ventas = self.initial.get('ventas', 0) or 0
                    valorexcento = self.initial.get('valorexcento', 0) or 0
                    controlado = self.initial.get('controlado', 0) or 0
                
                # Convertir a Decimal y calcular suma
                ventai = Decimal(str(ventai)) if ventai else Decimal('0')
                ventac = Decimal(str(ventac)) if ventac else Decimal('0')
                ventas = Decimal(str(ventas)) if ventas else Decimal('0')
                valorexcento = Decimal(str(valorexcento)) if valorexcento else Decimal('0')
                controlado = Decimal(str(controlado)) if controlado else Decimal('0')
                
                valor_base = float(ventai + ventac + ventas + valorexcento + controlado)
                print(f"Calculado desde datos: {valor_base}")
            
            # Actualizar el campo valor_base en initial
            self.initial['valor_base'] = valor_base
            
        except Exception as e:
            # Si hay error, establecer valor_base en 0
            if not hasattr(self, 'initial') or self.initial is None:
                self.initial = {}
            self.initial['valor_base'] = 0
            print(f"Error en _calcular_valor_base: {e}")
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que RTM y EXPE estén presentes
        rtm = cleaned_data.get('rtm', '').strip()
        expe = cleaned_data.get('expe', '').strip()
        
        if not rtm:
            raise forms.ValidationError(
                "El campo RTM es obligatorio."
            )
        
        if not expe:
            raise forms.ValidationError(
                "El campo Expediente es obligatorio."
            )
        
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
        
        # Calcular el valor_base para mostrar en el formulario (NO se guarda en BD)
        # Se calcula automáticamente usando la propiedad del modelo
        cleaned_data['valor_base'] = total_ventas
        
        # NO validar el impuesto aquí - se calculará automáticamente en el modelo
        # El impuesto se calcula automáticamente en el método save() del modelo
        
        return cleaned_data
    
    def save(self, commit=True):
        """Sobrescribir el método save para calcular y guardar valor_base"""
        instance = super().save(commit=False)
        
        # Calcular valor_base usando la propiedad del modelo
        if hasattr(instance, 'valor_base'):
            # El valor_base se calcula automáticamente en la propiedad del modelo
            # No necesitamos hacer nada aquí ya que es una propiedad calculada
            pass
        
        if commit:
            instance.save()
        
        return instance


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
            from tributario.models import Rubro
            rubros_choices = [('', 'Seleccione un rubro')] + [
                (rubro.codigo, f"{rubro.codigo} - {rubro.descripcion}")
                for rubro in getattr(Rubro, 'objects').all().order_by('codigo')
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


class TipoCategoriaForm(forms.ModelForm):
    """
    Formulario para TipoCategoria
    """
    class Meta:
        model = TipoCategoria
        fields = ['codigo', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 1,
                'style': 'text-transform: uppercase;',
                'placeholder': 'Ej: 1, 2, 3'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 50,
                'placeholder': 'Ej: Viviendas, Apartamentos'
            })
        }
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción'
        }
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').strip().upper()
        if len(codigo) != 1:
            raise forms.ValidationError("El código debe tener exactamente 1 carácter")
        return codigo
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if not descripcion:
            raise forms.ValidationError("La descripción es obligatoria")
        return descripcion
    
    def clean_tarifa_rubro(self):
        """Validación personalizada para el campo tarifa_rubro"""
        tarifa_rubro = self.cleaned_data.get('tarifa_rubro')
        if tarifa_rubro:
            # No validar contra las opciones del formulario ya que se cargan dinámicamente
            pass
        return tarifa_rubro

from tributario.models import ParametrosTributarios

class ParametrosTributariosForm(forms.ModelForm):
    class Meta:
        model = ParametrosTributarios
        fields = [
            'empresa', 'tipo_parametro', 'ano_vigencia', 'descripcion', 
            'numero_decreto', 'fecha_inicio', 'fecha_fin', 'fecha_corte',
            'aplica_recargos', 'aplica_intereses', 'aplica_saldo_impuesto',
            'porcentaje_condonacion', 'porcentaje_descuento_saldo',
            'meses_anticipacion', 'porcentaje_descuento_anual',
            'tasa_recargo_mensual', 'recargo_maximo_porcentaje', 'activo'
        ]
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 4}),
            'tipo_parametro': forms.Select(attrs={'class': 'form-control'}),
            'ano_vigencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 2020, 'max': 2030}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_decreto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_corte': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'porcentaje_condonacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'porcentaje_descuento_saldo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'meses_anticipacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'porcentaje_descuento_anual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_recargo_mensual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'recargo_maximo_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aplica_recargos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aplica_intereses': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aplica_saldo_impuesto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned = super().clean()
        tipo = (cleaned.get('tipo_parametro') or '').strip()

        # Descuento por edad: configuración fija por ley.
        # Solo se deben manejar 25% (TE) y 35% (CE). El resto de campos
        # no deben alterar este comportamiento.
        if tipo in ('TE', 'CE'):
            cleaned['aplica_saldo_impuesto'] = True
            cleaned['aplica_recargos'] = False
            cleaned['aplica_intereses'] = False
            cleaned['porcentaje_condonacion'] = Decimal('0.00')
            cleaned['porcentaje_descuento_anual'] = Decimal('0.00')
            cleaned['meses_anticipacion'] = 0
            cleaned['tasa_recargo_mensual'] = Decimal('0.0000')
            cleaned['recargo_maximo_porcentaje'] = Decimal('0.00')

            if tipo == 'TE':
                cleaned['porcentaje_descuento_saldo'] = Decimal('25.00')
            else:
                cleaned['porcentaje_descuento_saldo'] = Decimal('35.00')

        return cleaned





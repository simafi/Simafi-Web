from django import forms
from .models import TasasMunicipales

class DynamicChoiceField(forms.ChoiceField):
    """Campo de elección dinámico que permite actualizar las opciones"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TasasMunicipalesForm(forms.ModelForm):
    """
    Formulario para las Tasas Municipales (Configuración de Tasas por Bien Inmueble)
    Similar a TarifasICSForm pero para bienes inmuebles
    """
    # Campo para seleccionar rubro
    rubro = forms.ChoiceField(
        label="Rubro",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_rubro',
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
        })
    )
    
    # Campo para el valor personalizado (opcional)
    valor_personalizado = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Valor",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_valor_personalizado',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0',
        })
    )

    class Meta:
        model = TasasMunicipales
        fields = ['empresa', 'clave', 'rubro', 'cod_tarifa', 'valor', 'cuenta', 'cuentarez']
        widgets = {
            'empresa': forms.HiddenInput(),
            'clave': forms.HiddenInput(),
            'rubro': forms.HiddenInput(),
            'cod_tarifa': forms.HiddenInput(),
            'valor': forms.HiddenInput(),
            'cuenta': forms.HiddenInput(),
            'cuentarez': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer que el campo valor no sea requerido ya que se calcula automáticamente
        if 'valor' in self.fields:
            self.fields['valor'].required = False
        
        # Cargar las opciones del combobox de rubros
        try:
            from tributario.models import Rubro
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
            raise forms.ValidationError("El valor debe ser mayor a 0")
        
        return cleaned_data



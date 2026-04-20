
from django import forms
from .models import DeclaracionVolumen, Anos

class DeclaracionVolumenForm(forms.ModelForm):
    """Formulario para declaración de volumen con años dinámicos"""
    
    class Meta:
        model = DeclaracionVolumen
        fields = '__all__'
        widgets = {
            'ano': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_ano'
            }),
            'mes': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_mes'
            }),
            'ventai': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'id': 'id_ventai'
            }),
            'ventac': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '0',
                'id': 'id_ventac'
            }),
            'ventas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0', 
                'id': 'id_ventas'
            }),
            'ventap': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'id': 'id_ventap'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar años dinámicamente desde la tabla Anos
        try:
            anos_choices = [('', 'Seleccione un año')] + [
                (str(int(ano.ano)), str(int(ano.ano))) 
                for ano in Anos.objects.all().order_by('-ano')
            ]
            self.fields['ano'].widget.choices = anos_choices
        except Exception as e:
            print(f"Error cargando años: {e}")
            # Fallback con años estáticos
            current_year = 2024
            anos_choices = [('', 'Seleccione un año')] + [
                (str(year), str(year)) 
                for year in range(current_year, current_year - 10, -1)
            ]
            self.fields['ano'].widget.choices = anos_choices
        
        # Configurar meses
        meses_choices = [
            ('', 'Seleccione mes'),
            ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
            ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
            ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'),
            ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
        ]
        self.fields['mes'].widget.choices = meses_choices

# FORMULARIOS DJANGO CORREGIDOS - forms.py
# Cambiar 'cocontrolado' por 'controlado'

from django import forms
from .models import Declara

class DeclaraForm(forms.ModelForm):
    class Meta:
        model = Declara
        fields = [
            'rtm', 'expe', 'ano', 'tipo', 'mes',
            'ventai', 'ventac', 'ventas', 'valorexcento',
            'controlado',  # CORREGIDO: era 'cocontrolado'
            'unidad', 'factor', 'usuario', 'impuesto'
        ]
        
        widgets = {
            'ventai': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ventas Industria',
                'data-format': 'decimal-16-2'
            }),
            'ventac': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ventas Comercio',
                'data-format': 'decimal-16-2'
            }),
            'ventas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ventas Servicios', 
                'data-format': 'decimal-16-2'
            }),
            'controlado': forms.TextInput(attrs={  # CORREGIDO
                'class': 'form-control',
                'placeholder': 'Valor Controlado',
                'data-format': 'decimal-16-2'
            }),
            'impuesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Impuesto Calculado',
                'data-format': 'decimal-12-2',
                'readonly': True
            })
        }
        
        labels = {
            'ventai': 'Ventas Industria',
            'ventac': 'Ventas Comercio', 
            'ventas': 'Ventas Servicios',
            'controlado': 'Valor Controlado',  # CORREGIDO
            'impuesto': 'Impuesto ICS'
        }

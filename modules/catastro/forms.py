from django import forms
from .models import PropiedadInmueble, Terreno, Construccion, Vehiculo, EstablecimientoComercial
from modules.core.models import Municipio

class PropiedadInmuebleForm(forms.ModelForm):
    """
    Formulario para propiedades inmuebles
    """
    class Meta:
        model = PropiedadInmueble
        fields = [
            'municipio', 'codigo_catastral', 'direccion', 'propietario',
            'area_terreno', 'area_construccion', 'valor_catastral'
        ]
        widgets = {
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'codigo_catastral': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'propietario': forms.TextInput(attrs={'class': 'form-control'}),
            'area_terreno': forms.NumberInput(attrs={'class': 'form-control'}),
            'area_construccion': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_catastral': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TerrenoForm(forms.ModelForm):
    """
    Formulario para terrenos
    """
    class Meta:
        model = Terreno
        fields = ['municipio', 'codigo_terreno', 'direccion', 'propietario', 'area', 'valor_catastral']
        widgets = {
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'codigo_terreno': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'propietario': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_catastral': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ConstruccionForm(forms.ModelForm):
    """
    Formulario para construcciones
    """
    class Meta:
        model = Construccion
        fields = [
            'municipio', 'codigo_construccion', 'direccion', 'propietario',
            'area_construccion', 'tipo_construccion', 'valor_catastral'
        ]
        widgets = {
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'codigo_construccion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'propietario': forms.TextInput(attrs={'class': 'form-control'}),
            'area_construccion': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_construccion': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_catastral': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VehiculoForm(forms.ModelForm):
    """
    Formulario para vehículos
    """
    class Meta:
        model = Vehiculo
        fields = ['municipio', 'placa', 'propietario', 'marca', 'modelo', 'año', 'valor_catastral']
        widgets = {
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'año': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_catastral': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EstablecimientoComercialForm(forms.ModelForm):
    """
    Formulario para establecimientos comerciales
    """
    class Meta:
        model = EstablecimientoComercial
        fields = [
            'municipio', 'codigo_establecimiento', 'nombre_comercial', 'propietario',
            'direccion', 'actividad_comercial', 'area_local', 'valor_catastral'
        ]
        widgets = {
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'codigo_establecimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actividad_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'area_local': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_catastral': forms.NumberInput(attrs={'class': 'form-control'}),
        }





























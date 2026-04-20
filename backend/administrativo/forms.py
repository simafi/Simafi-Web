from django import forms
from core.models import Departamento

from .models import ContratoAdministrativo, ExpedienteGestion, Proveedor


class DepartamentoForm(forms.ModelForm):
    """
    Formulario para el Departamento (columnas reales: depto, descripcion).
    """

    depto = forms.CharField(
        max_length=3,
        label="Código",
        widget=forms.TextInput(attrs={
            'maxlength': 3,
            'style': 'text-transform: uppercase;',
            'placeholder': 'Ingrese código del departamento'
        })
    )
    descripcion = forms.CharField(
        max_length=29,
        label="Descripción",
        widget=forms.TextInput(attrs={
            'maxlength': 29,
            'placeholder': 'Descripción del departamento'
        })
    )

    class Meta:
        model = Departamento
        fields = ['depto', 'descripcion']

    def clean(self):
        cleaned_data = super().clean()
        depto = cleaned_data.get('depto')

        if depto:
            try:
                existing = Departamento.objects.get(depto=depto)
                if self.instance.pk and existing.pk == self.instance.pk:
                    pass
                else:
                    raise forms.ValidationError(
                        f"Ya existe un departamento con el código {depto}"
                    )
            except Departamento.DoesNotExist:
                pass

        return cleaned_data


class ProveedorForm(forms.ModelForm):
    def __init__(self, *args, empresa_sesion=None, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa_sesion:
            self.fields['empresa'].widget.attrs['readonly'] = True
            if not self.instance.pk:
                self.initial.setdefault('empresa', empresa_sesion)

    class Meta:
        model = Proveedor
        fields = [
            'empresa',
            'razon_social',
            'nit',
            'telefono',
            'email',
            'direccion',
            'activo',
            'notas',
            'documentacion_descripcion',
            'documentacion',
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'documentacion_descripcion': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej. Copia RTN, constancia fiscal…'}
            ),
            'documentacion': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': '.pdf,.png,.jpg,.jpeg,.doc,.docx'}
            ),
        }


class ContratoAdministrativoForm(forms.ModelForm):
    def __init__(self, *args, empresa=None, empresa_sesion=None, **kwargs):
        super().__init__(*args, **kwargs)
        emp = empresa or empresa_sesion
        if emp:
            self.fields['proveedor'].queryset = Proveedor.objects.filter(empresa=emp).order_by(
                'razon_social'
            )
            self.fields['empresa'].widget.attrs['readonly'] = True
            if not self.instance.pk:
                self.initial.setdefault('empresa', emp)
        elif self.instance and self.instance.pk:
            self.fields['proveedor'].queryset = Proveedor.objects.filter(
                empresa=self.instance.empresa
            ).order_by('razon_social')
        else:
            self.fields['proveedor'].queryset = Proveedor.objects.all().order_by('razon_social')

    class Meta:
        model = ContratoAdministrativo
        fields = [
            'empresa',
            'proveedor',
            'numero',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'monto_estimado',
            'estado',
            'observaciones',
        ]
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monto_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ExpedienteGestionForm(forms.ModelForm):
    def __init__(self, *args, empresa_sesion=None, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa_sesion:
            self.fields['empresa'].widget.attrs['readonly'] = True
            if not self.instance.pk:
                self.initial.setdefault('empresa', empresa_sesion)

    class Meta:
        model = ExpedienteGestion
        fields = [
            'empresa',
            'codigo_interno',
            'titulo',
            'tipo',
            'fecha_apertura',
            'estado',
            'descripcion',
        ]
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_interno': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_apertura': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

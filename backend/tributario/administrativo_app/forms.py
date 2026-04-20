from django import forms
from .models import Departamento


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

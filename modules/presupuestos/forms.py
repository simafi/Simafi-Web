from django import forms
from .models import PresupuestoIngresos, PresupuestoGastos, EjecucionPresupuestaria, ModificacionPresupuestaria


class PresupuestoIngresosForm(forms.ModelForm):
    class Meta:
        model = PresupuestoIngresos
        fields = ['ano', 'fuente_ingreso', 'descripcion', 'monto_presupuestado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'monto_presupuestado': forms.NumberInput(attrs={'step': '0.01'}),
        }


class PresupuestoGastosForm(forms.ModelForm):
    class Meta:
        model = PresupuestoGastos
        fields = ['ano', 'categoria_gasto', 'subcategoria', 'descripcion', 'monto_presupuestado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'monto_presupuestado': forms.NumberInput(attrs={'step': '0.01'}),
        }


class EjecucionPresupuestariaForm(forms.ModelForm):
    class Meta:
        model = EjecucionPresupuestaria
        fields = ['tipo', 'presupuesto_ingreso', 'presupuesto_gasto', 'fecha_ejecucion', 'monto', 'descripcion', 'documento_referencia']
        widgets = {
            'fecha_ejecucion': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'monto': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar presupuestos por tipo
        if self.instance and self.instance.tipo == 'ingreso':
            self.fields['presupuesto_gasto'].required = False
            self.fields['presupuesto_gasto'].widget = forms.HiddenInput()
        elif self.instance and self.instance.tipo == 'gasto':
            self.fields['presupuesto_ingreso'].required = False
            self.fields['presupuesto_ingreso'].widget = forms.HiddenInput()


class ModificacionPresupuestariaForm(forms.ModelForm):
    class Meta:
        model = ModificacionPresupuestaria
        fields = ['tipo_modificacion', 'presupuesto_origen', 'presupuesto_destino', 'monto', 'fecha_modificacion', 'justificacion', 'documento_aprobacion']
        widgets = {
            'fecha_modificacion': forms.DateInput(attrs={'type': 'date'}),
            'justificacion': forms.Textarea(attrs={'rows': 3}),
            'monto': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para traslados, destino es requerido
        if self.instance and self.instance.tipo_modificacion == 'traslado':
            self.fields['presupuesto_destino'].required = True
        else:
            self.fields['presupuesto_destino'].required = False
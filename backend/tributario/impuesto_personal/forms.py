from django import forms
from .models import DeclaracionPersonal, PlanillaEmpresa, Contribuyente
from .services import calcular_impuesto_personal, calcular_multa_y_recargos

class DeclaracionPersonalForm(forms.ModelForm):
    class Meta:
        model = DeclaracionPersonal
        fields = ['contribuyente', 'ano_fiscal', 'renta_bruta', 'deducciones']
        widgets = {
            'contribuyente': forms.HiddenInput(),
            'ano_fiscal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'renta_bruta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deducciones': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        renta_bruta = cleaned_data.get('renta_bruta')
        deducciones = cleaned_data.get('deducciones')
        ano_fiscal = cleaned_data.get('ano_fiscal')
        
        if renta_bruta is not None and ano_fiscal is not None:
            impuesto, renta_neta = calcular_impuesto_personal(renta_bruta, deducciones or 0, ano_fiscal)
            multa, recargo = calcular_multa_y_recargos(impuesto, forms.utils.timezone.now(), ano_fiscal)
            
            cleaned_data['renta_neta'] = renta_neta
            cleaned_data['impuesto_calculado'] = impuesto
            cleaned_data['multa'] = multa
            cleaned_data['recargo'] = recargo
            cleaned_data['total_pagar'] = impuesto + multa + recargo
            
        return cleaned_data

class PlanillaUploadForm(forms.ModelForm):
    class Meta:
        model = PlanillaEmpresa
        fields = ['empresa', 'ano', 'mes', 'archivo']
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'mes': forms.NumberInput(attrs={'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }

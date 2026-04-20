from django import forms
from .models import CuentaTesoreria, PagoTesoreria, DepositoTesoreria, NotaTesoreria, ConciliacionBancaria


class CuentaTesoreriaForm(forms.ModelForm):
    class Meta:
        model = CuentaTesoreria
        fields = ["tipo", "codigo", "nombre", "cuenta_contable", "empresa"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "codigo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Código (ej. BCH-01 o 001)"}
            ),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre (opcional)"}
            ),
            "cuenta_contable": forms.Select(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }


class PagoTesoreriaForm(forms.ModelForm):
    class Meta:
        model = PagoTesoreria
        fields = [
            "tipo_pago",
            "numero_referencia",
            "fecha",
            "cuenta_tesoreria",
            "beneficiario",
            "concepto",
            "punto_acta",
            "empresa",
        ]
        widgets = {
            "tipo_pago": forms.Select(attrs={"class": "form-control"}),
            "numero_referencia": forms.TextInput(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "cuenta_tesoreria": forms.Select(attrs={"class": "form-control"}),
            "beneficiario": forms.TextInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "punto_acta": forms.TextInput(attrs={"class": "form-control", "placeholder": "No. Acta (opcional)"}),
            "empresa": forms.HiddenInput(),
        }


class DepositoTesoreriaForm(forms.ModelForm):
    class Meta:
        model = DepositoTesoreria
        fields = ["fecha", "numero_referencia", "cuenta_tesoreria", "monto", "concepto", "empresa"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "numero_referencia": forms.TextInput(attrs={"class": "form-control"}),
            "cuenta_tesoreria": forms.Select(attrs={"class": "form-control"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "empresa": forms.HiddenInput(),
        }


class NotaTesoreriaForm(forms.ModelForm):
    class Meta:
        model = NotaTesoreria
        fields = ["tipo", "fecha", "numero_referencia", "cuenta_tesoreria", "monto", "concepto", "orden_pago", "empresa"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "numero_referencia": forms.TextInput(attrs={"class": "form-control"}),
            "cuenta_tesoreria": forms.Select(attrs={"class": "form-control"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "orden_pago": forms.Select(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }


class ConciliacionBancariaForm(forms.ModelForm):
    class Meta:
        model = ConciliacionBancaria
        fields = ["cuenta_tesoreria", "anio", "mes", "saldo_banco", "empresa"]
        widgets = {
            "cuenta_tesoreria": forms.Select(attrs={"class": "form-control"}),
            "anio": forms.NumberInput(attrs={"class": "form-control"}),
            "mes": forms.NumberInput(attrs={"class": "form-control"}),
            "saldo_banco": forms.NumberInput(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }


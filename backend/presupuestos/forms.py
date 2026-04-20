from django import forms
from contabilidad.models import CuentaContable, EjercicioFiscal, CentroCosto
from .models import (
    Fondo, CuentaPresupuestaria, ProyectoInversion, OrdenPago, 
    PresupuestoAnual, ReformaPresupuestaria, Compromiso, OperacionManual
)


class FondoForm(forms.ModelForm):
    class Meta:
        model = Fondo
        fields = ["codigo", "nombre", "descripcion", "empresa"]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "empresa": forms.HiddenInput(),
        }


class CuentaPresupuestariaForm(forms.ModelForm):
    class Meta:
        model = CuentaPresupuestaria
        fields = [
            "codigo",
            "nombre",
            "tipo_presupuesto",
            "tipo_cuenta",
            "cuenta_padre",
            "nivel",
            "rubro_tributario",
            "cuenta_contable",
            "empresa",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_presupuesto": forms.Select(attrs={"class": "form-control"}),
            "tipo_cuenta": forms.Select(attrs={"class": "form-control"}),
            "cuenta_padre": forms.Select(attrs={"class": "form-control"}),
            "nivel": forms.NumberInput(attrs={"class": "form-control"}),
            "rubro_tributario": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Código rubro (opcional)"}
            ),
            "cuenta_contable": forms.Select(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        tipo_presupuesto = kwargs.pop("tipo_presupuesto", None)
        super().__init__(*args, **kwargs)
        
        # Filtrar catálogo contable
        qs_contable = CuentaContable.objects.filter(is_active=True).order_by("codigo")
        # Filtrar posibles padres
        qs_padre = CuentaPresupuestaria.objects.filter(is_active=True, tipo_cuenta="TITULO").order_by("codigo")
        
        if empresa:
            qs_contable = qs_contable.filter(empresa=empresa)
            qs_padre = qs_padre.filter(empresa=empresa)
        
        if tipo_presupuesto:
            qs_padre = qs_padre.filter(tipo_presupuesto=tipo_presupuesto)
            
        self.fields["cuenta_contable"].queryset = qs_contable
        self.fields["cuenta_padre"].queryset = qs_padre
        self.fields["cuenta_contable"].required = False


class PresupuestoAnualForm(forms.ModelForm):
    cuenta_manual = forms.CharField(
        required=False,
        label="Cuenta Presupuestaria (Detalle) - Manual",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite el código de cuenta, por ejemplo: 11.01.01",
            }
        ),
    )

    class Meta:
        model = PresupuestoAnual
        fields = ["ejercicio", "cuenta", "fondo", "monto_inicial", "monto_reformas", "empresa"]
        widgets = {
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "cuenta": forms.Select(attrs={"class": "form-control"}),
            "fondo": forms.Select(attrs={"class": "form-control"}),
            "monto_inicial": forms.NumberInput(attrs={"class": "form-control"}),
            "monto_reformas": forms.NumberInput(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        tipo_presupuesto = kwargs.pop("tipo_presupuesto", None)
        super().__init__(*args, **kwargs)
        
        qs_ej = EjercicioFiscal.objects.all().order_by("-anio")
        qs_cta = CuentaPresupuestaria.objects.filter(is_active=True, tipo_cuenta="DETALLE").order_by("codigo")
        qs_fondo = Fondo.objects.filter(is_active=True).order_by("codigo")
        
        if empresa:
            qs_ej = qs_ej.filter(empresa=empresa)
            qs_cta = qs_cta.filter(empresa=empresa)
            qs_fondo = qs_fondo.filter(empresa=empresa)
            
        if tipo_presupuesto:
            qs_cta = qs_cta.filter(tipo_presupuesto=tipo_presupuesto)
            
        self.fields["ejercicio"].queryset = qs_ej
        self.fields["cuenta"].queryset = qs_cta
        self.fields["fondo"].queryset = qs_fondo
        self.fields["cuenta"].required = False

    def clean(self):
        cleaned_data = super().clean()
        cuenta = cleaned_data.get("cuenta")
        cuenta_manual = (cleaned_data.get("cuenta_manual") or "").strip()

        if cuenta_manual:
            cuenta_manual = cuenta_manual.split("-")[0].strip()
            cuenta_obj = self.fields["cuenta"].queryset.filter(codigo__iexact=cuenta_manual).first()
            if not cuenta_obj:
                self.add_error(
                    "cuenta_manual",
                    "La cuenta ingresada manualmente no existe o no es de tipo detalle para este presupuesto.",
                )
            else:
                cleaned_data["cuenta"] = cuenta_obj
                return cleaned_data

        if not cuenta:
            self.add_error("cuenta", "Seleccione una cuenta o ingrese el código manualmente.")

        return cleaned_data


class AmpliacionPresupuestariaForm(forms.ModelForm):
    class Meta:
        model = ReformaPresupuestaria
        fields = ["fecha", "ejercicio", "referencia", "punto_acta", "concepto", "fondo", "cuenta_destino", "monto", "empresa"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "referencia": forms.TextInput(attrs={"class": "form-control", "placeholder": "No. Documento"}),
            "punto_acta": forms.TextInput(attrs={"class": "form-control", "placeholder": "No. Acta de Aprobación"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "fondo": forms.Select(attrs={"class": "form-control"}),
            "cuenta_destino": forms.Select(attrs={"class": "form-control"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields["ejercicio"].queryset = EjercicioFiscal.objects.filter(empresa=empresa).order_by("-anio")
            self.fields["cuenta_destino"].queryset = CuentaPresupuestaria.objects.filter(empresa=empresa, is_active=True, tipo_cuenta="DETALLE").order_by("codigo")
            self.fields["fondo"].queryset = Fondo.objects.filter(empresa=empresa, is_active=True).order_by("codigo")


class ReduccionPresupuestariaForm(forms.ModelForm):
    class Meta:
        model = ReformaPresupuestaria
        fields = ["fecha", "ejercicio", "referencia", "punto_acta", "concepto", "fondo", "cuenta_destino", "monto", "empresa"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "referencia": forms.TextInput(attrs={"class": "form-control"}),
            "punto_acta": forms.TextInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "fondo": forms.Select(attrs={"class": "form-control"}),
            "cuenta_destino": forms.Select(attrs={"class": "form-control"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields["ejercicio"].queryset = EjercicioFiscal.objects.filter(empresa=empresa).order_by("-anio")
            self.fields["cuenta_destino"].queryset = CuentaPresupuestaria.objects.filter(empresa=empresa, is_active=True, tipo_cuenta="DETALLE").order_by("codigo")
            self.fields["fondo"].queryset = Fondo.objects.filter(empresa=empresa, is_active=True).order_by("codigo")


class TraspasoPresupuestariaForm(forms.ModelForm):
    class Meta:
        model = ReformaPresupuestaria
        fields = ["fecha", "ejercicio", "referencia", "punto_acta", "concepto", "fondo", "cuenta_origen", "cuenta_destino", "monto", "empresa"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "referencia": forms.TextInput(attrs={"class": "form-control"}),
            "punto_acta": forms.TextInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "fondo": forms.Select(attrs={"class": "form-control"}),
            "cuenta_origen": forms.Select(attrs={"class": "form-control"}),
            "cuenta_destino": forms.Select(attrs={"class": "form-control"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields["ejercicio"].queryset = EjercicioFiscal.objects.filter(empresa=empresa).order_by("-anio")
            qs_cta = CuentaPresupuestaria.objects.filter(empresa=empresa, is_active=True, tipo_cuenta="DETALLE").order_by("codigo")
            self.fields["cuenta_origen"].queryset = qs_cta
            self.fields["cuenta_destino"].queryset = qs_cta
            self.fields["fondo"].queryset = Fondo.objects.filter(empresa=empresa, is_active=True).order_by("codigo")


class ProyectoInversionForm(forms.ModelForm):
    class Meta:
        model = ProyectoInversion
        fields = ["codigo", "nombre", "descripcion", "ejercicio", "centro_costo", "empresa"]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "centro_costo": forms.Select(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)
        ej = EjercicioFiscal.objects.all().order_by("-anio")
        cc = CentroCosto.objects.filter(is_active=True).order_by("codigo")
        if empresa:
            ej = ej.filter(empresa=empresa)
            cc = cc.filter(empresa=empresa)
        self.fields["ejercicio"].queryset = ej
        self.fields["centro_costo"].queryset = cc
        self.fields["centro_costo"].required = False


class OrdenPagoForm(forms.ModelForm):
    class Meta:
        model = OrdenPago
        fields = ["numero", "fecha", "ejercicio", "favorecido", "concepto", "empresa"]
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "favorecido": forms.TextInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "empresa": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)
        qs = EjercicioFiscal.objects.all().order_by("-anio")
        if empresa:
            qs = qs.filter(empresa=empresa)
        self.fields["ejercicio"].queryset = qs


class CompromisoForm(forms.ModelForm):
    class Meta:
        model = Compromiso
        fields = ["numero", "fecha", "favorecido", "concepto", "total", "fondo", "ejercicio", "empresa"]
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "favorecido": forms.TextInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "total": forms.NumberInput(attrs={"class": "form-control"}),
            "fondo": forms.Select(attrs={"class": "form-control"}),
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }


class OperacionManualForm(forms.ModelForm):
    class Meta:
        model = OperacionManual
        fields = ["tipo", "fecha", "beneficiario", "concepto", "monto", "fondo", "cuenta", "ejercicio", "empresa"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "beneficiario": forms.TextInput(attrs={"class": "form-control"}),
            "concepto": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "fondo": forms.Select(attrs={"class": "form-control"}),
            "cuenta": forms.Select(attrs={"class": "form-control"}),
            "ejercicio": forms.Select(attrs={"class": "form-control"}),
            "empresa": forms.HiddenInput(),
        }


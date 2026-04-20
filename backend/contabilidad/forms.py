"""
Formularios Django para el módulo de Contabilidad
"""
from django import forms
from .models import (
    EjercicioFiscal, PeriodoContable, GrupoCuenta, CuentaContable,
    CentroCosto, Moneda, TipoCambio, TipoAsiento, AsientoContable,
    DetalleAsiento, ActivoFijo, Inventario, Provision, TipoInventario,
)


class EjercicioFiscalForm(forms.ModelForm):
    class Meta:
        model = EjercicioFiscal
        fields = ['anio', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado', 'empresa']
        widgets = {
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2026'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del ejercicio'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'empresa': forms.HiddenInput(),
        }


class PeriodoContableForm(forms.ModelForm):
    class Meta:
        model = PeriodoContable
        fields = ['ejercicio', 'numero', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'ejercicio': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 13}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class GrupoCuentaForm(forms.ModelForm):
    class Meta:
        model = GrupoCuenta
        fields = ['codigo', 'nombre', 'naturaleza', 'descripcion', 'orden']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 1, 'placeholder': '1-5'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'naturaleza': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Etiquetas del combo Grupo: igual que en la explicación del formulario (1 Activo, 2 Pasivo, etc.)
GRUPO_ETIQUETAS = {
    '1': '1 Activo — Bienes y derechos (efectivo, bancos, inventarios, cuentas por cobrar, activos fijos)',
    '2': '2 Pasivo — Obligaciones (cuentas por pagar, préstamos, impuestos por pagar)',
    '3': '3 Capital — Patrimonio (capital social, reservas, utilidades acumuladas)',
    '4': '4 Cuentas de orden — Control y contracuentas',
    '5': '5 Ingresos — Ventas, ingresos por servicios, otros ingresos',
    '6': '6 Egresos — Gastos operativos, costos, gastos financieros y otros',
    '7': '7 Egresos — Gastos operativos, costos, gastos financieros y otros',
}


class CuentaContableForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = [
            'codigo', 'nombre', 'grupo', 'cuenta_padre', 'nivel',
            'tipo', 'naturaleza', 'descripcion', 'acepta_movimiento',
            'requiere_centro_costo', 'requiere_tercero', 'empresa'
        ]
        help_texts = {
            'nivel': 'Profundidad de la cuenta en el árbol: 1 = grupo (ej. Activo), 2 = subgrupo, 3 = rubro, 4 = cuenta, 5 = subcuenta. Suele coincidir con la cantidad de segmentos del código (ej. 111-01-02 tiene nivel 3).',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 11101'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la cuenta'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'cuenta_padre': forms.Select(attrs={'class': 'form-control'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': '1 a 5'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'naturaleza': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'acepta_movimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requiere_centro_costo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requiere_tercero': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'empresa': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo'].queryset = GrupoCuenta.objects.filter(is_active=True).order_by('codigo')
        self.fields['grupo'].choices = self._get_grupo_choices()
        self.fields['grupo'].label = 'Grupo'

    def _get_grupo_choices(self):
        """Opciones de Grupo en lista plana: 1 Activo, 2 Pasivo, etc., para que se vean en el combo."""
        grupos = GrupoCuenta.objects.filter(is_active=True).order_by('codigo')
        choices = []
        for g in grupos:
            label = GRUPO_ETIQUETAS.get(g.codigo) or f"{g.codigo} - {g.nombre}"
            choices.append((str(g.pk), label))
        if not choices:
            choices = [('', '— Sin grupos configurados —')]
        return choices


class CentroCostoForm(forms.ModelForm):
    class Meta:
        model = CentroCosto
        fields = ['codigo', 'nombre', 'centro_padre', 'responsable', 'empresa']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'centro_padre': forms.Select(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.HiddenInput(),
        }


class AsientoContableForm(forms.ModelForm):
    class Meta:
        model = AsientoContable
        fields = [
            'numero', 'tipo', 'periodo', 'fecha', 'concepto',
            'referencia', 'documento', 'moneda', 'tasa_cambio', 'empresa'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de asiento'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'concepto': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Concepto del asiento'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'moneda': forms.Select(attrs={'class': 'form-control'}),
            'tasa_cambio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'empresa': forms.HiddenInput(),
        }


class DetalleAsientoForm(forms.ModelForm):
    class Meta:
        model = DetalleAsiento
        fields = ['linea', 'cuenta', 'concepto', 'debe', 'haber', 'centro_costo', 'tercero', 'referencia']
        widgets = {
            'linea': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': True}),
            'cuenta': forms.Select(attrs={'class': 'form-control form-control-sm cuenta-select'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'debe': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end campo-debe', 'step': '0.01', 'value': '0.00'}),
            'haber': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end campo-haber', 'step': '0.01', 'value': '0.00'}),
            'centro_costo': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'tercero': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


class ActivoFijoForm(forms.ModelForm):
    class Meta:
        model = ActivoFijo
        fields = [
            'codigo', 'descripcion', 'cuenta_activo', 'cuenta_depreciacion',
            'cuenta_gasto_depreciacion', 'fecha_adquisicion', 'costo_adquisicion',
            'valor_residual', 'vida_util_meses', 'metodo_depreciacion',
            'ubicacion', 'responsable', 'numero_serie', 'estado', 'empresa'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cuenta_activo': forms.Select(attrs={'class': 'form-control'}),
            'cuenta_depreciacion': forms.Select(attrs={'class': 'form-control'}),
            'cuenta_gasto_depreciacion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_adquisicion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'costo_adquisicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_residual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vida_util_meses': forms.NumberInput(attrs={'class': 'form-control'}),
            'metodo_depreciacion': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'empresa': forms.HiddenInput(),
        }


class TipoInventarioForm(forms.ModelForm):
    """Catálogo de tipos por empresa; codigo_legacy documenta el listado estándar heredado."""

    class Meta:
        model = TipoInventario
        fields = ["nombre", "orden", "notas", "codigo_legacy", "is_active", "empresa"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "orden": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "codigo_legacy": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Opcional — solo si homologa clave antigua",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "empresa": forms.HiddenInput(),
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            'codigo', 'tipo_inventario', 'nomenclatura', 'descripcion',
            'cuenta_inventario', 'cuenta_costo_venta',
            'unidad_medida', 'cantidad', 'costo_unitario', 'valor_neto_realizable',
            'metodo_valoracion', 'stock_minimo', 'empresa',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único por empresa'}),
            'tipo_inventario': forms.Select(attrs={'class': 'form-control js-select2-tipo-inventario'}),
            'nomenclatura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. UNSPSC, CPV o código de catálogo',
            }),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cuenta_inventario': forms.Select(attrs={'class': 'form-control js-cuenta-select2-inventario'}),
            'cuenta_costo_venta': forms.Select(attrs={'class': 'form-control js-cuenta-select2-inventario'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'costo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'valor_neto_realizable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo_valoracion': forms.Select(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'empresa': forms.HiddenInput(),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        emp = (empresa or "").strip()
        for name in ("cuenta_inventario", "cuenta_costo_venta"):
            if name in self.fields:
                self.fields[name].empty_label = "— Buscar cuenta (código o nombre) —"
        if emp and "tipo_inventario" in self.fields:
            qs = TipoInventario.objects.filter(empresa=emp, is_active=True)
            if self.instance.pk and getattr(self.instance, "tipo_inventario_id", None):
                qs = qs | TipoInventario.objects.filter(pk=self.instance.tipo_inventario_id)
            self.fields["tipo_inventario"].queryset = qs.distinct().order_by("orden", "nombre")
            self.fields["tipo_inventario"].required = False
            self.fields["tipo_inventario"].empty_label = "— Seleccione tipo (catálogo) —"

    def save(self, commit=True):
        from decimal import Decimal
        obj = super().save(commit=False)
        q = obj.cantidad or Decimal('0')
        cu = obj.costo_unitario or Decimal('0')
        obj.costo_total = (q * cu).quantize(Decimal('0.01'))
        if commit:
            obj.save()
            self.save_m2m()
        return obj


class ProvisionForm(forms.ModelForm):
    class Meta:
        model = Provision
        fields = [
            'descripcion', 'tipo', 'cuenta', 'monto_estimado',
            'probabilidad', 'fecha_origen', 'fecha_vencimiento', 'notas', 'empresa'
        ]
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cuenta': forms.Select(attrs={'class': 'form-control'}),
            'monto_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'probabilidad': forms.Select(attrs={'class': 'form-control'}),
            'fecha_origen': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'empresa': forms.HiddenInput(),
        }


# Formset para líneas de detalle del asiento
DetalleAsientoFormSet = forms.inlineformset_factory(
    AsientoContable,
    DetalleAsiento,
    form=DetalleAsientoForm,
    extra=5,
    can_delete=True,
    min_num=2,
    validate_min=True,
)

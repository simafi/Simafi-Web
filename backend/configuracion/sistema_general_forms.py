# -*- coding: utf-8 -*-
"""Formularios de configuración general del sistema (multi-municipio)."""
from collections import OrderedDict

from django import forms

from core.municipio_depto import (
    departamento_para_codigo_municipio,
    dos_digitos_codigo_departamento,
    municipio_codigo_coincide_departamento,
)
from core.models import Departamento, Municipio
from .models import Caserio, Nacionalidad, Sitio


class FormControlMixin:
    def _apply_widgets(self):
        for _name, field in self.fields.items():
            w = field.widget
            if isinstance(w, (forms.TextInput, forms.NumberInput, forms.EmailInput)):
                w.attrs.setdefault('class', 'form-control')
            elif isinstance(w, forms.DateInput):
                w.attrs.setdefault('class', 'form-control')
                if not getattr(w, 'input_type', None) or w.input_type == 'text':
                    w.input_type = 'date'
            elif isinstance(w, forms.Select):
                w.attrs.setdefault('class', 'form-select')
            elif isinstance(w, forms.Textarea):
                w.attrs.setdefault('class', 'form-control')
                w.attrs.setdefault('rows', 2)


_FORM_CATALOGO_PREDIO = {}


def catalogo_predio_form(model_class):
    """ModelForm dinámico: todos los campos del catálogo salvo PK (tablas reales MySQL)."""
    if model_class not in _FORM_CATALOGO_PREDIO:
        field_names = [f.name for f in model_class._meta.fields if not f.primary_key]

        class _CatalogoPredioForm(forms.ModelForm, FormControlMixin):
            class Meta:
                model = model_class
                fields = field_names

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._apply_widgets()

        _CatalogoPredioForm.__name__ = f'{model_class.__name__}Form'
        _FORM_CATALOGO_PREDIO[model_class] = _CatalogoPredioForm
    return _FORM_CATALOGO_PREDIO[model_class]


def catalogo_codigo_desc_form(model_class):
    """Compatibilidad: delega en catálogo predio completo."""
    return catalogo_predio_form(model_class)


class DepartamentoForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Departamento
        fields = ['depto', 'descripcion']
        labels = {
            'depto': 'Código (3 caracteres)',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widgets()


class MunicipioForm(forms.ModelForm, FormControlMixin):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.none(),
        label='Departamento',
        required=True,
        empty_label='Seleccione departamento…',
        help_text='Cada municipio pertenece a un departamento: los dos primeros dígitos del código deben coincidir con el código del departamento.',
    )

    class Meta:
        model = Municipio
        fields = [
            'codigo', 'descripcion',
            'fesqui', 'por_concer', 'vl_exento', 'tasau', 'tasar', 'interes', 'desc_tercera',
            'alcalde', 'auditor', 'presupuestos', 'contador', 'tesorero', 'secretario', 'tesorera',
            'financiero', 'tributacion', 'gerentefin', 'gerentegeneral',
            'proyecto', 'activo',
            'porce_condo1', 'porce_condo2', 'fecondona1', 'fecondona2',
        ]
        labels = {
            'codigo': 'Código (típ. 4 dígitos: 2 del departamento + 2 del municipio)',
            'descripcion': 'Nombre del municipio',
            'fesqui': 'Factor esquina',
            'por_concer': 'Porcentaje concertación',
            'vl_exento': 'Valor exento',
            'tasau': 'Tasa urbana',
            'tasar': 'Tasa rural',
            'interes': 'Interés',
            'desc_tercera': 'Descuento tercera edad / tercera',
            'alcalde': 'Alcalde',
            'auditor': 'Auditor',
            'presupuestos': 'Presupuestos',
            'contador': 'Contador',
            'tesorero': 'Tesorero',
            'secretario': 'Secretario',
            'tesorera': 'Tesorera',
            'financiero': 'Financiero',
            'tributacion': 'Tributación',
            'gerentefin': 'Gerente financiero',
            'gerentegeneral': 'Gerente general',
            'proyecto': 'Proyecto',
            'activo': 'Activo',
            'porce_condo1': '% condonación 1',
            'porce_condo2': '% condonación 2',
            'fecondona1': 'Fecha condonación 1',
            'fecondona2': 'Fecha condonación 2',
        }

    def __init__(self, *args, **kwargs):
        depto_bloqueado = kwargs.pop('depto_bloqueado', None)
        super().__init__(*args, **kwargs)
        self._depto_bloqueado = depto_bloqueado
        if depto_bloqueado is not None:
            self.fields['departamento'].queryset = Departamento.objects.filter(pk=depto_bloqueado.pk)
            self.fields['departamento'].initial = depto_bloqueado.pk
            self.fields['departamento'].widget = forms.HiddenInput()
        else:
            self.fields['departamento'].queryset = Departamento.objects.all().order_by('depto')
        inst = getattr(self, 'instance', None)
        if depto_bloqueado is None and inst and getattr(inst, 'pk', None) and getattr(inst, 'codigo', None):
            dep = departamento_para_codigo_municipio(inst.codigo)
            if dep:
                self.fields['departamento'].initial = dep.pk
        elif depto_bloqueado is not None and inst and getattr(inst, 'pk', None):
            self.fields['departamento'].initial = depto_bloqueado.pk
        for fname in ('fecondona1', 'fecondona2'):
            if fname in self.fields:
                self.fields[fname].widget = forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={'class': 'form-control', 'type': 'date'},
                )
                self.fields[fname].input_formats = ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']
        self._apply_widgets()
        # Mostrar primero departamento, luego código y el resto
        order = ['departamento', 'codigo', 'descripcion'] + [
            f for f in self.fields
            if f not in ('departamento', 'codigo', 'descripcion')
        ]
        self.fields = OrderedDict((k, self.fields[k]) for k in order if k in self.fields)

    def clean(self):
        cleaned = super().clean()
        codigo = (cleaned.get('codigo') or '').strip()
        dept = cleaned.get('departamento')
        if getattr(self, '_depto_bloqueado', None) and dept and dept.pk != self._depto_bloqueado.pk:
            self.add_error('departamento', 'El departamento no coincide con el contexto seleccionado.')
        if dept and codigo:
            if not municipio_codigo_coincide_departamento(codigo, dept):
                self.add_error(
                    'codigo',
                    'Los dos primeros dígitos del código deben coincidir con el código del departamento seleccionado '
                    f'({dept.depto}).',
                )
        elif dept and not codigo:
            self.add_error('codigo', 'Indique el código del municipio.')
        return cleaned


class SitioForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Sitio
        fields = ['codigo', 'descripcion']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widgets()


class CaserioForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Caserio
        fields = ['depto', 'codmuni', 'codbarrio', 'codigo', 'descripcion']
        labels = {
            'depto': 'Código departamento',
            'codmuni': 'Código municipio',
            'codbarrio': 'Código barrio',
            'codigo': 'Código caserío',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        depto_codmuni_bloqueado = kwargs.pop('depto_codmuni_bloqueado', None)
        super().__init__(*args, **kwargs)
        self._depto_codmuni_bloqueado = depto_codmuni_bloqueado
        if depto_codmuni_bloqueado is not None:
            d0, m0 = depto_codmuni_bloqueado
            self.fields['depto'].widget = forms.HiddenInput()
            self.fields['codmuni'].widget = forms.HiddenInput()
            self.fields['depto'].initial = d0
            self.fields['codmuni'].initial = m0
        self._apply_widgets()
        order = ['depto', 'codmuni', 'codbarrio', 'codigo', 'descripcion']
        self.fields = OrderedDict((k, self.fields[k]) for k in order if k in self.fields)

    def clean(self):
        cleaned = super().clean()
        t = getattr(self, '_depto_codmuni_bloqueado', None)
        if t is not None:
            d0, m0 = t
            if (cleaned.get('depto') or '').strip() != d0 or (cleaned.get('codmuni') or '').strip() != m0:
                self.add_error(
                    None,
                    'El departamento y municipio del caserío deben coincidir con el municipio seleccionado.',
                )
        return cleaned


class NacionalidadForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Nacionalidad
        fields = ['codigo', 'descripcion']
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widgets()

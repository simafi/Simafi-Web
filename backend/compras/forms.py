# -*- coding: utf-8 -*-
from datetime import date
from decimal import Decimal

from django import forms
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from administrativo.models import Proveedor
from contabilidad.models import Inventario
from presupuestos.models import Compromiso

from .models import (
    InvitacionCotizacion,
    MovimientoBodega,
    OfertaProveedor,
    OrdenCompra,
    OrdenCompraDetalle,
    Requisicion,
    RequisicionDetalle,
    SolicitudCotizacion,
    SolicitudCotizacionDetalle,
)


def label_inventario_catalogo(obj: Inventario) -> str:
    """Texto de opción en selects de ítem inventario (tipo, nomenclatura, existencias)."""
    ex = obj.cantidad
    sm = obj.stock_minimo
    tipo = "—"
    if getattr(obj, "tipo_inventario_id", None) and getattr(obj, "tipo_inventario", None):
        tipo = obj.tipo_inventario.nombre
    nom = (getattr(obj, "nomenclatura", None) or "").strip()
    nom_part = f" | Nom.: {nom}" if nom else ""
    return (
        f"{obj.codigo} — [{tipo}]{nom_part} — {obj.descripcion[:50]}"
        f"{'…' if len(obj.descripcion) > 50 else ''} | "
        f"Exist.: {ex} {obj.unidad_medida} | Mín.: {sm}"
    )


class RequisicionNuevaForm(forms.ModelForm):
    """Alta de cabecera (número correlativo y ejercicio fiscal se asignan al guardar)."""

    class Meta:
        model = Requisicion
        fields = ["fecha", "solicitante", "observaciones"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "solicitante": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)


class RequisicionForm(forms.ModelForm):
    """Edición de cabecera (incluye estado). El ejercicio fiscal no se edita (queda el asignado al crear)."""

    class Meta:
        model = Requisicion
        fields = ["numero", "fecha", "solicitante", "observaciones", "estado"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "solicitante": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "estado": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["numero"].disabled = True


class RequisicionDetalleForm(forms.ModelForm):
    """Línea opcional en formularios vacíos (se ignoran al guardar si no hay descripción)."""

    class Meta:
        model = RequisicionDetalle
        fields = ("nro_linea", "descripcion", "cantidad", "unidad", "inventario", "cuenta_presupuestaria")
        widgets = {
            "nro_linea": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "unidad": forms.TextInput(attrs={"class": "form-control"}),
            "inventario": forms.Select(attrs={"class": "form-control form-select requisicion-inv-select"}),
            "cuenta_presupuestaria": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        req = getattr(self.instance, "requisicion", None)
        self._empresa = (getattr(req, "empresa", None) or "").strip()
        for name in ("descripcion", "cantidad", "unidad", "inventario", "cuenta_presupuestaria"):
            if name in self.fields:
                self.fields[name].required = False
        inv = self.fields.get("inventario")
        if inv:
            inv.label = "Material (bodega / inventario)"
            inv.help_text = "Existencia actual = cantidad en catálogo de inventario (bodega)."
            inv.label_from_instance = label_inventario_catalogo

    def clean(self):
        data = super().clean()
        desc = (data.get("descripcion") or "").strip()
        cant = data.get("cantidad")
        inv = data.get("inventario")
        if not desc and (cant is None or cant == "") and not inv:
            return data
        if not inv:
            raise forms.ValidationError(
                "Seleccione el material en inventario/bodega; la requisición se basa en existencias del catálogo."
            )
        if self._empresa and inv.empresa != self._empresa:
            raise forms.ValidationError("El ítem de inventario no corresponde a su empresa.")
        if not desc:
            data["descripcion"] = inv.descripcion[:500]
            desc = (data.get("descripcion") or "").strip()
        if cant is None or cant <= 0:
            raise forms.ValidationError("Indique cantidad mayor a cero.")
        um = (inv.unidad_medida or "").strip()
        if um and not (data.get("unidad") or "").strip():
            data["unidad"] = um
        elif not (data.get("unidad") or "").strip():
            data["unidad"] = "UND"
        return data


class RequisicionDetalleInlineFormSet(BaseInlineFormSet):
    """No persiste líneas en blanco; si se vacía una línea existente, la elimina."""

    def save(self, commit=True):
        saved = []
        for form in self.forms:
            if not form.is_bound or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                if form.instance.pk:
                    form.instance.delete()
                continue
            desc = (form.cleaned_data.get("descripcion") or "").strip()
            if not desc:
                if form.instance.pk:
                    form.instance.delete()
                continue
            saved.append(form.save(commit=commit))
        return saved


RequisicionDetalleFormSet = inlineformset_factory(
    Requisicion,
    RequisicionDetalle,
    form=RequisicionDetalleForm,
    formset=RequisicionDetalleInlineFormSet,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class OrdenCompraNuevaForm(forms.ModelForm):
    """Alta de cabecera OC (número y monto se asignan al guardar / al editar líneas)."""

    class Meta:
        model = OrdenCompra
        fields = ("fecha", "proveedor", "requisicion", "solicitud_cotizacion", "observaciones")
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "proveedor": forms.Select(attrs={"class": "form-control"}),
            "requisicion": forms.Select(attrs={"class": "form-control"}),
            "solicitud_cotizacion": forms.Select(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields["proveedor"].queryset = Proveedor.objects.filter(
                empresa=empresa, activo=True
            ).order_by("razon_social")
            self.fields["requisicion"].queryset = Requisicion.objects.filter(empresa=empresa).order_by(
                "-fecha", "-id"
            )
            self.fields["solicitud_cotizacion"].queryset = SolicitudCotizacion.objects.filter(
                empresa=empresa
            ).order_by("-fecha", "-id")
        self.fields["requisicion"].required = False
        self.fields["solicitud_cotizacion"].required = False


class OrdenCompraForm(forms.ModelForm):
    """Edición de cabecera OC (monto total se recalcula desde las líneas)."""

    class Meta:
        model = OrdenCompra
        fields = (
            "numero",
            "fecha",
            "proveedor",
            "estado",
            "requisicion",
            "solicitud_cotizacion",
            "compromiso",
            "observaciones",
        )
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "proveedor": forms.Select(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
            "requisicion": forms.Select(attrs={"class": "form-control"}),
            "solicitud_cotizacion": forms.Select(attrs={"class": "form-control"}),
            "compromiso": forms.Select(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields["proveedor"].queryset = Proveedor.objects.filter(
                empresa=empresa, activo=True
            ).order_by("razon_social")
            self.fields["requisicion"].queryset = Requisicion.objects.filter(empresa=empresa).order_by(
                "-fecha", "-id"
            )
            self.fields["solicitud_cotizacion"].queryset = SolicitudCotizacion.objects.filter(
                empresa=empresa
            ).order_by("-fecha", "-id")
            self.fields["compromiso"].queryset = Compromiso.objects.filter(empresa=empresa).order_by(
                "-fecha", "-id"
            )
        self.fields["requisicion"].required = False
        self.fields["solicitud_cotizacion"].required = False
        self.fields["compromiso"].required = False
        self.fields["numero"].disabled = True


class OrdenCompraDetalleForm(forms.ModelForm):
    """Líneas OC; subtotal se calcula al guardar."""

    class Meta:
        model = OrdenCompraDetalle
        fields = (
            "nro_linea",
            "descripcion",
            "cantidad",
            "precio_unitario",
            "inventario",
            "cuenta_presupuestaria",
        )
        widgets = {
            "nro_linea": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "inventario": forms.Select(attrs={"class": "form-control"}),
            "cuenta_presupuestaria": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("descripcion", "cantidad", "precio_unitario", "inventario", "cuenta_presupuestaria"):
            if name in self.fields:
                self.fields[name].required = False

    def clean(self):
        data = super().clean()
        desc = (data.get("descripcion") or "").strip()
        cant = data.get("cantidad")
        if not desc and (cant is None or cant == ""):
            return data
        if not desc:
            raise forms.ValidationError("Indique descripción en la línea.")
        if cant is None or cant <= 0:
            raise forms.ValidationError("Indique cantidad mayor a cero.")
        pu = data.get("precio_unitario")
        if pu is None:
            data["precio_unitario"] = Decimal("0")
        return data


class OrdenCompraDetalleInlineFormSet(BaseInlineFormSet):
    def save(self, commit=True):
        saved = []
        for form in self.forms:
            if not form.is_bound or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                if form.instance.pk:
                    form.instance.delete()
                continue
            desc = (form.cleaned_data.get("descripcion") or "").strip()
            if not desc:
                if form.instance.pk:
                    form.instance.delete()
                continue
            obj = form.save(commit=False)
            pu = obj.precio_unitario or Decimal("0")
            obj.subtotal = (obj.cantidad * pu).quantize(Decimal("0.01"))
            if commit:
                obj.save()
            saved.append(obj)

        if commit and self.instance.pk:
            total = (
                OrdenCompraDetalle.objects.filter(orden_id=self.instance.pk).aggregate(
                    t=Sum("subtotal")
                )["t"]
                or Decimal("0")
            )
            OrdenCompra.objects.filter(pk=self.instance.pk).update(monto_total=total)
        return saved


OrdenCompraDetalleFormSet = inlineformset_factory(
    OrdenCompra,
    OrdenCompraDetalle,
    form=OrdenCompraDetalleForm,
    formset=OrdenCompraDetalleInlineFormSet,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class SolicitudCotizacionNuevaForm(forms.ModelForm):
    class Meta:
        model = SolicitudCotizacion
        fields = ("fecha", "fecha_limite_respuesta", "requisicion", "observaciones", "texto_marco_oncae")
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_limite_respuesta": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "requisicion": forms.Select(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "texto_marco_oncae": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields["requisicion"].queryset = Requisicion.objects.filter(empresa=empresa).order_by(
                "-fecha", "-id"
            )
        self.fields["requisicion"].required = False
        self.fields["fecha_limite_respuesta"].required = False


class SolicitudCotizacionForm(forms.ModelForm):
    class Meta:
        model = SolicitudCotizacion
        fields = (
            "numero",
            "fecha",
            "fecha_limite_respuesta",
            "estado",
            "requisicion",
            "observaciones",
            "texto_marco_oncae",
        )
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_limite_respuesta": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
            "requisicion": forms.Select(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "texto_marco_oncae": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields["requisicion"].queryset = Requisicion.objects.filter(empresa=empresa).order_by(
                "-fecha", "-id"
            )
        self.fields["requisicion"].required = False
        self.fields["fecha_limite_respuesta"].required = False
        self.fields["numero"].disabled = True


class SolicitudCotizacionDetalleForm(forms.ModelForm):
    class Meta:
        model = SolicitudCotizacionDetalle
        fields = ("nro_linea", "descripcion", "cantidad", "unidad", "inventario")
        widgets = {
            "nro_linea": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "unidad": forms.TextInput(attrs={"class": "form-control"}),
            "inventario": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n in ("descripcion", "cantidad", "unidad", "inventario"):
            if n in self.fields:
                self.fields[n].required = False
        sol = getattr(self.instance, "solicitud", None)
        emp = getattr(sol, "empresa", None) if sol else None
        if emp and "inventario" in self.fields:
            self.fields["inventario"].queryset = (
                Inventario.objects.filter(empresa=emp, is_active=True)
                .select_related("tipo_inventario")
                .order_by("tipo_inventario__orden", "tipo_inventario__nombre", "codigo")
            )

    def clean(self):
        data = super().clean()
        desc = (data.get("descripcion") or "").strip()
        cant = data.get("cantidad")
        if not desc and (cant is None or cant == ""):
            return data
        if not desc:
            raise forms.ValidationError("Indique descripción.")
        if cant is None or cant <= 0:
            raise forms.ValidationError("Indique cantidad mayor a cero.")
        if not (data.get("unidad") or "").strip():
            data["unidad"] = "UND"
        return data


class SolicitudCotizacionDetalleInlineFormSet(BaseInlineFormSet):
    def save(self, commit=True):
        saved = []
        for form in self.forms:
            if not form.is_bound or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                if form.instance.pk:
                    form.instance.delete()
                continue
            desc = (form.cleaned_data.get("descripcion") or "").strip()
            if not desc:
                if form.instance.pk:
                    form.instance.delete()
                continue
            saved.append(form.save(commit=commit))
        return saved


SolicitudCotizacionDetalleFormSet = inlineformset_factory(
    SolicitudCotizacion,
    SolicitudCotizacionDetalle,
    form=SolicitudCotizacionDetalleForm,
    formset=SolicitudCotizacionDetalleInlineFormSet,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class InvitacionCotizacionForm(forms.ModelForm):
    class Meta:
        model = InvitacionCotizacion
        fields = ("proveedor", "fecha_invitacion")
        widgets = {
            "proveedor": forms.Select(attrs={"class": "form-control"}),
            "fecha_invitacion": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sol = getattr(self.instance, "solicitud", None)
        emp = getattr(sol, "empresa", None) if sol else None
        if emp:
            self.fields["proveedor"].queryset = Proveedor.objects.filter(
                empresa=emp, activo=True
            ).order_by("razon_social")
        self.fields["proveedor"].required = False
        self.fields["fecha_invitacion"].required = False

    def clean(self):
        data = super().clean()
        prov = data.get("proveedor")
        fi = data.get("fecha_invitacion")
        if not prov and not fi:
            return data
        if not prov:
            raise forms.ValidationError("Indique proveedor o deje la fila vacía.")
        return data


class InvitacionCotizacionInlineFormSet(BaseInlineFormSet):
    def save(self, commit=True):
        saved = []
        for form in self.forms:
            if not form.is_bound or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                if form.instance.pk:
                    form.instance.delete()
                continue
            if not form.cleaned_data.get("proveedor"):
                continue
            obj = form.save(commit=False)
            if not obj.fecha_invitacion:
                obj.fecha_invitacion = date.today()
            if commit:
                obj.save()
            saved.append(obj)
        return saved


InvitacionCotizacionFormSet = inlineformset_factory(
    SolicitudCotizacion,
    InvitacionCotizacion,
    form=InvitacionCotizacionForm,
    formset=InvitacionCotizacionInlineFormSet,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class OfertaProveedorForm(forms.ModelForm):
    class Meta:
        model = OfertaProveedor
        fields = ("fecha_recepcion", "monto_total", "notas", "es_seleccionada")
        widgets = {
            "fecha_recepcion": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "monto_total": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "es_seleccionada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MovimientoBodegaEntradaForm(forms.ModelForm):
    class Meta:
        model = MovimientoBodega
        fields = (
            "fecha_compra",
            "fecha",
            "inventario",
            "cantidad",
            "costo_unitario",
            "orden_detalle",
            "referencia",
            "notas",
        )
        widgets = {
            "fecha_compra": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "inventario": forms.Select(attrs={"class": "form-control js-select2-inv-entrada"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "costo_unitario": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "orden_detalle": forms.Select(attrs={"class": "form-control js-select2-oc-entrada"}),
            "referencia": forms.TextInput(attrs={"class": "form-control"}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["orden_detalle"].required = False
        self.fields["fecha_compra"].required = False
        self.fields["fecha_compra"].help_text = (
            "Fecha en que se realizó la compra (factura/proveedor). Si la deja vacía, se usará la misma fecha de registro en bodega."
        )
        if empresa:
            self.fields["inventario"].queryset = (
                Inventario.objects.filter(empresa=empresa, is_active=True)
                .select_related("tipo_inventario")
                .order_by("tipo_inventario__orden", "tipo_inventario__nombre", "codigo")
            )
            self.fields["inventario"].label_from_instance = label_inventario_catalogo
            od_qs = OrdenCompraDetalle.objects.filter(orden__empresa=empresa).select_related(
                "orden", "inventario"
            )
            self.fields["orden_detalle"].queryset = od_qs.order_by("-orden__fecha", "orden_id", "nro_linea")

            def _lbl(od):
                num = od.orden.numero if od.orden_id else ""
                return f"{num} L{od.nro_linea} — {(od.descripcion or '')[:50]}"

            self.fields["orden_detalle"].label_from_instance = _lbl
        self.fields["orden_detalle"].label = "Línea OC origen (opcional)"

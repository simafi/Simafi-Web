"""
Registro de modelos en Django Admin para el módulo Contabilidad
"""
from django.contrib import admin
from .models import (
    EjercicioFiscal, PeriodoContable, GrupoCuenta, CuentaContable,
    CentroCosto, Moneda, TipoCambio, TipoAsiento, AsientoContable,
    DetalleAsiento, LibroMayor, ActivoFijo, Depreciacion, Inventario,
    TipoInventario,
    Provision, ActivoIntangible, InstrumentoFinanciero, ImpuestoDiferido,
    BeneficioEmpleado, PropiedadInversion, ActivoBiologico, CostoPrestamo,
    PoliticaContable, HechoPosterior, DeterioroActivo, FlujoEfectivo
)


class DetalleAsientoInline(admin.TabularInline):
    model = DetalleAsiento
    extra = 2
    fields = ['linea', 'cuenta', 'concepto', 'debe', 'haber', 'centro_costo']


@admin.register(EjercicioFiscal)
class EjercicioFiscalAdmin(admin.ModelAdmin):
    list_display = ['anio', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado', 'empresa']
    list_filter = ['estado', 'empresa']
    search_fields = ['anio', 'descripcion']


@admin.register(PeriodoContable)
class PeriodoContableAdmin(admin.ModelAdmin):
    list_display = ['ejercicio', 'numero', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado']
    list_filter = ['estado', 'ejercicio']


@admin.register(GrupoCuenta)
class GrupoCuentaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'naturaleza', 'orden']
    ordering = ['codigo']


@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'grupo', 'nivel', 'tipo', 'naturaleza', 'acepta_movimiento']
    list_filter = ['grupo', 'tipo', 'naturaleza', 'nivel', 'empresa']
    search_fields = ['codigo', 'nombre']
    ordering = ['codigo']


@admin.register(CentroCosto)
class CentroCostoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'responsable', 'empresa']
    search_fields = ['codigo', 'nombre']


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'simbolo', 'es_local']


@admin.register(TipoCambio)
class TipoCambioAdmin(admin.ModelAdmin):
    list_display = ['moneda', 'fecha', 'tasa_compra', 'tasa_venta', 'tasa_promedio']
    list_filter = ['moneda']


@admin.register(TipoAsiento)
class TipoAsientoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'prefijo', 'es_automatico']


@admin.register(AsientoContable)
class AsientoContableAdmin(admin.ModelAdmin):
    list_display = ['numero', 'tipo', 'fecha', 'concepto', 'total_debe', 'total_haber', 'estado']
    list_filter = ['estado', 'tipo', 'periodo']
    search_fields = ['numero', 'concepto']
    inlines = [DetalleAsientoInline]


@admin.register(LibroMayor)
class LibroMayorAdmin(admin.ModelAdmin):
    list_display = ['cuenta', 'periodo', 'saldo_anterior', 'debitos', 'creditos', 'saldo_final']
    list_filter = ['periodo', 'empresa']
    search_fields = ['cuenta__codigo', 'cuenta__nombre']


@admin.register(ActivoFijo)
class ActivoFijoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'costo_adquisicion', 'depreciacion_acumulada', 'valor_en_libros', 'estado']
    list_filter = ['estado', 'metodo_depreciacion']
    search_fields = ['codigo', 'descripcion']


@admin.register(TipoInventario)
class TipoInventarioAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'orden', 'nombre', 'codigo_legacy', 'is_active']
    list_filter = ['empresa', 'is_active']
    search_fields = ['nombre', 'codigo_legacy']


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'tipo_inventario', 'nomenclatura', 'descripcion',
        'cantidad', 'costo_unitario', 'costo_total', 'metodo_valoracion',
    ]
    list_filter = ['metodo_valoracion']
    search_fields = ['codigo', 'descripcion', 'nomenclatura']


@admin.register(Provision)
class ProvisionAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'tipo', 'monto_estimado', 'probabilidad', 'fecha_origen']
    list_filter = ['tipo', 'probabilidad']


@admin.register(ActivoIntangible)
class ActivoIntangibleAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'costo_adquisicion', 'amortizacion_acumulada', 'tipo_vida']
    search_fields = ['codigo', 'descripcion']


@admin.register(InstrumentoFinanciero)
class InstrumentoFinancieroAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'tipo', 'clasificacion', 'valor_nominal']
    list_filter = ['tipo', 'clasificacion']


@admin.register(ImpuestoDiferido)
class ImpuestoDiferidoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'tipo', 'base_contable', 'base_fiscal', 'impuesto_diferido']
    list_filter = ['tipo']


@admin.register(BeneficioEmpleado)
class BeneficioEmpleadoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'tipo', 'monto_mensual', 'provision_acumulada']
    list_filter = ['tipo']


@admin.register(PropiedadInversion)
class PropiedadInversionAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'costo_adquisicion', 'valor_razonable', 'modelo_medicion']
    search_fields = ['codigo', 'descripcion']


@admin.register(ActivoBiologico)
class ActivoBiologicoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'tipo', 'cantidad', 'valor_razonable']
    list_filter = ['tipo']


@admin.register(CostoPrestamo)
class CostoPrestamoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'monto_principal', 'tasa_interes_anual', 'capitalizable']
    list_filter = ['capitalizable']


@admin.register(PoliticaContable)
class PoliticaContableAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_vigencia', 'nic_relacionada']


@admin.register(HechoPosterior)
class HechoPosteriorAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'descripcion', 'fecha_hecho', 'impacto_financiero']
    list_filter = ['tipo']


@admin.register(DeterioroActivo)
class DeterioroActivoAdmin(admin.ModelAdmin):
    list_display = ['tipo_activo', 'valor_en_libros', 'importe_recuperable', 'perdida_deterioro']
    list_filter = ['tipo_activo']


@admin.register(FlujoEfectivo)
class FlujoEfectivoAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'concepto', 'entrada', 'salida', 'neto']
    list_filter = ['categoria', 'periodo']

from django.contrib import admin
from .models import Contribuyente, TarifasPersonal, DeclaracionPersonal, PlanillaEmpresa, DetallePlanilla

@admin.register(Contribuyente)
class ContribuyenteAdmin(admin.ModelAdmin):
    list_display = ('persona', 'rtn', 'telefono', 'correo')
    search_fields = ('persona__identidad', 'persona__nombres', 'persona__apellidos', 'rtn')

@admin.register(TarifasPersonal)
class TarifasPersonalAdmin(admin.ModelAdmin):
    list_display = ('ano', 'desde', 'hasta', 'tasa', 'valor_fijo')
    list_filter = ('ano',)

@admin.register(DeclaracionPersonal)
class DeclaracionPersonalAdmin(admin.ModelAdmin):
    list_display = ('contribuyente', 'ano_fiscal', 'renta_bruta', 'impuesto_calculado', 'total_pagar', 'estado')
    list_filter = ('ano_fiscal', 'estado')
    search_fields = ('contribuyente__persona__identidad', 'contribuyente__persona__nombres')

class DetallePlanillaInline(admin.TabularInline):
    model = DetallePlanilla
    extra = 0

@admin.register(PlanillaEmpresa)
class PlanillaEmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'ano', 'mes', 'fecha_carga', 'procesado')
    list_filter = ('ano', 'mes', 'procesado')
    inlines = [DetallePlanillaInline]

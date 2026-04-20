"""
Signals para el módulo presupuestos
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PresupuestoIngresos, PresupuestoGastos, EjecucionPresupuestaria


@receiver(post_save, sender=EjecucionPresupuestaria)
def actualizar_montos_ejecutados(sender, instance, created, **kwargs):
    """
    Actualiza los montos ejecutados en los presupuestos cuando se registra una ejecución
    """
    if created:
        if instance.tipo == 'ingreso' and instance.presupuesto_ingreso:
            presupuesto = instance.presupuesto_ingreso
            presupuesto.monto_ejecutado += instance.monto
            presupuesto.save()
        elif instance.tipo == 'gasto' and instance.presupuesto_gasto:
            presupuesto = instance.presupuesto_gasto
            presupuesto.monto_ejecutado += instance.monto
            presupuesto.save()


@receiver(post_delete, sender=EjecucionPresupuestaria)
def revertir_montos_ejecutados(sender, instance, **kwargs):
    """
    Revierte los montos ejecutados cuando se elimina una ejecución
    """
    if instance.tipo == 'ingreso' and instance.presupuesto_ingreso:
        presupuesto = instance.presupuesto_ingreso
        presupuesto.monto_ejecutado -= instance.monto
        presupuesto.save()
    elif instance.tipo == 'gasto' and instance.presupuesto_gasto:
        presupuesto = instance.presupuesto_gasto
        presupuesto.monto_ejecutado -= instance.monto
        presupuesto.save()


@receiver(post_save, sender=PresupuestoIngresos)
def auditoria_presupuesto_ingresos(sender, instance, created, **kwargs):
    """
    Registra cambios en presupuestos de ingresos para auditoría
    """
    # TODO: Implementar logging de auditoría
    pass


@receiver(post_save, sender=PresupuestoGastos)
def auditoria_presupuesto_gastos(sender, instance, created, **kwargs):
    """
    Registra cambios en presupuestos de gastos para auditoría
    """
    # TODO: Implementar logging de auditoría
    pass
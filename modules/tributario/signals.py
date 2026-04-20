"""
Signals de Django para el módulo tributario.
Protege que el campo tasa siempre sea 0.00 en TransaccionesIcs.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from decimal import Decimal


def register_signals():
    """
    Registra los signals para TransaccionesIcs.
    Se llama desde apps.py o __init__.py cuando Django está listo.
    """
    try:
        from tributario.models import TransaccionesIcs
    except ImportError:
        try:
            from tributario_app.models import TransaccionesIcs
        except ImportError:
            # No se puede importar el modelo, no registrar signals
            return
    
    # Registrar signals con el sender específico
    pre_save.connect(forzar_tasa_cero_signal, sender=TransaccionesIcs, weak=False)
    post_save.connect(verificar_tasa_cero_despues_guardar, sender=TransaccionesIcs, weak=False)


def forzar_tasa_cero_signal(sender, instance, **kwargs):
    """
    Signal que fuerza el campo tasa a 0.00 antes de guardar TransaccionesIcs.
    Esta protección asegura que tasa nunca reciba valores incorrectos.
    IMPORTANTE: Se ejecuta ANTES de save(), así que cualquier valor incorrecto será sobrescrito.
    """
    if instance and hasattr(instance, 'tasa'):
        # FORZAR tasa a 0.00 siempre, sin importar qué valor tenga
        # Esto previene que se guarde con un valor incorrecto desde el inicio
        valor_anterior = instance.tasa
        instance.tasa = Decimal('0.00')
        # Log para debugging (solo si había un valor diferente)
        if valor_anterior != Decimal('0.00') and valor_anterior is not None:
            print(f"[SIGNAL PRE_SAVE] Corrigiendo tasa de {valor_anterior} a 0.00 para TransaccionesIcs")


def verificar_tasa_cero_despues_guardar(sender, instance, **kwargs):
    """
    Signal que verifica y corrige tasa después de guardar TransaccionesIcs.
    Protección adicional usando update directo en BD.
    IMPORTANTE: SIEMPRE fuerza tasa a 0.00, incluso si ya es 0.00, 
    para sobreescribir cualquier trigger de BD que lo haya modificado.
    """
    if instance and hasattr(instance, 'tasa') and hasattr(instance, 'id'):
        # SIEMPRE forzar a 0.00 usando update directo en BD
        # Esto sobrescribe cualquier trigger o proceso que haya modificado tasa
        try:
            sender.objects.filter(id=instance.id).update(tasa=Decimal('0.00'))
            # Recargar el instance desde BD para reflejar el cambio
            instance.refresh_from_db()
            # Verificar que se guardó correctamente
            if instance.tasa != Decimal('0.00'):
                print(f"[SIGNAL WARNING] tasa no es 0 después de update (id={instance.id}, tasa={instance.tasa})")
        except Exception as e:
            print(f"[SIGNAL] Error forzando tasa a 0 después de guardar (id={instance.id}): {e}")
            import traceback
            traceback.print_exc()


# Registrar signals automáticamente cuando se importa el módulo
# Esto funcionará cuando Django esté completamente cargado
try:
    import django
    django.setup()
    if django.apps.apps.ready:
        register_signals()
    else:
        # Si Django no está listo, intentar registrar de todas formas
        try:
            register_signals()
        except:
            pass
except:
    # Si Django no está listo, los signals se registrarán cuando se importe apps.py
    try:
        register_signals()
    except:
        pass

# Importar signals para que se registren automáticamente
default_app_config = None

# Registrar signals automáticamente cuando Django esté listo
def ready():
    """Función para registrar signals cuando Django esté listo"""
    try:
        from . import signals
        signals.register_signals()
    except ImportError:
        pass
    except Exception as e:
        print(f"[TRIBUTARIO __INIT__] Error registrando signals en ready(): {e}")

# Intentar registrar signals inmediatamente
try:
    # Forzar registro de signals
    from . import signals
    # Dar tiempo para que Django esté listo
    import time
    time.sleep(0.1)  # Pequeña pausa para que Django termine de cargar
    signals.register_signals()
    print("[TRIBUTARIO] Signals registrados exitosamente")
except (ImportError, AttributeError) as e:
    print(f"[TRIBUTARIO __INIT__] Error registrando signals (será intentado nuevamente): {e}")
except Exception as e:
    print(f"[TRIBUTARIO __INIT__] Error inesperado registrando signals: {e}")

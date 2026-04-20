# 🔧 CORRECCIÓN DEL CAMPO `tasa` EN TransaccionesIcs

## 📋 PROBLEMA IDENTIFICADO

El campo `tasa` en la tabla `transaccionesics` está recibiendo el mismo valor que `saldoact` o el campo `valor` durante el proceso de generación de transacciones desde el formulario `declaracion_volumen`.

**Ejemplo del problema:**
- `saldoact = 17127.77`, `tasa = 17127.77` ❌ (incorrecto)
- `saldoact = 8000`, `tasa = 8000` ❌ (incorrecto)
- `saldoact = 500`, `tasa = 500` ❌ (incorrecto)

**Comportamiento esperado:**
- `saldoact = 17127.77`, `tasa = 0.00` ✅ (correcto)
- `saldoact = 8000`, `tasa = 0.00` ✅ (correcto)
- `saldoact = 500`, `tasa = 0.00` ✅ (correcto)

## 🔍 CAUSA PROBABLE

El campo `tasa` puede estar recibiendo valores incorrectos en cualquiera de estos escenarios:

1. **Asignación directa incorrecta:** `tasa = valor_tasa` o `tasa = saldoact`
2. **Método `save()` personalizado:** Un método `save()` en el modelo que asigna `tasa = saldoact` o `tasa = valor`
3. **Signal de Django:** Un signal `pre_save` o `post_save` que modifica el campo `tasa`
4. **Trigger en la base de datos:** Un trigger SQL que actualiza `tasa` después de insertar

## ✅ SOLUCIONES IMPLEMENTADAS

### 1. Signal de Django - `pre_save` y `post_save` ✅ **IMPLEMENTADO**

**Ubicación:** `modules/tributario/signals.py`

```python
def forzar_tasa_cero_signal(sender, instance, **kwargs):
    """
    Signal que fuerza el campo tasa a 0.00 antes de guardar TransaccionesIcs.
    Esta protección asegura que tasa nunca reciba valores incorrectos.
    """
    if instance and hasattr(instance, 'tasa'):
        # FORZAR tasa a 0.00 siempre, sin importar qué valor tenga
        instance.tasa = Decimal('0.00')

def verificar_tasa_cero_despues_guardar(sender, instance, **kwargs):
    """
    Signal que verifica y corrige tasa después de guardar TransaccionesIcs.
    Protección adicional usando update directo en BD.
    """
    if instance and hasattr(instance, 'tasa') and hasattr(instance, 'id'):
        if instance.tasa != Decimal('0.00'):
            sender.objects.filter(id=instance.id).update(tasa=Decimal('0.00'))
            instance.refresh_from_db()
```

**Registrado en:** `modules/tributario/__init__.py`

### 2. Función Helper `forzar_tasa_cero()`

**Ubicación:** `modules/tributario/simple_views.py`

```python
def forzar_tasa_cero(transaccion_id):
    """
    Fuerza el campo tasa a 0.00 usando update directo en BD.
    Se usa después de cualquier operación que modifique transacciones,
    especialmente cuando se calculan recargos moratorios.
    """
    from tributario.models import TransaccionesIcs
    from decimal import Decimal
    try:
        TransaccionesIcs.objects.filter(id=transaccion_id).update(tasa=Decimal('0.00'))
        return True
    except Exception as e:
        print(f"[FORZAR_TASA_CERO] Error forzando tasa a 0 para transacción {transaccion_id}: {e}")
        return False
```

### 3. Protección en `guardar_transaccion_pago()`

**Ubicación:** `modules/tributario/views.py`

```python
transaccion_pago = TransaccionesIcs(
    # ... otros campos ...
    tasa=Decimal('0'),  # ✅ Asignación correcta
    # ... otros campos ...
)
transaccion_pago.save()
# ✅ Protección adicional después de guardar
TransaccionesIcs.objects.filter(id=transaccion_pago.id).update(tasa=Decimal('0.00'))
```

## 🔍 PUNTOS A REVISAR

### 1. Buscar función de generación de transacciones

**Buscar en:**
- `modules/tributario/simple_views.py` - Función que maneja `accion == 'generar_transacciones'`
- `modules/tributario/ajax_views.py` - Funciones AJAX relacionadas
- Templates HTML - JavaScript que genere transacciones

**Buscar patrón:**
```python
if accion == 'generar_transacciones':
    # Aquí debería estar el código que crea TransaccionesIcs
    nueva_transaccion = TransaccionesIcs(
        tasa=Decimal('0.00'),  # ✅ Debe ser así
    )
```

### 2. Revisar modelo TransaccionesIcs

**Buscar método `save()` personalizado:**
```python
class TransaccionesIcs(models.Model):
    # ... campos ...
    
    def save(self, *args, **kwargs):
        # ❌ PROBLEMA: Si hay algo como esto:
        # if not self.tasa:
        #     self.tasa = self.saldoact  # ❌ INCORRECTO
        
        # ✅ SOLUCIÓN: Debe forzar tasa a 0
        self.tasa = Decimal('0.00')
        super().save(*args, **kwargs)
```

### 3. Revisar signals de Django

**Buscar en:** `modules/tributario/signals.py` o en el `apps.py`

```python
# ❌ PROBLEMA: Signal que modifica tasa
@receiver(pre_save, sender=TransaccionesIcs)
def asignar_tasa_antes_guardar(sender, instance, **kwargs):
    if not instance.tasa:
        instance.tasa = instance.saldoact  # ❌ INCORRECTO

# ✅ SOLUCIÓN: Signal que fuerza tasa a 0
@receiver(pre_save, sender=TransaccionesIcs)
def forzar_tasa_cero(sender, instance, **kwargs):
    instance.tasa = Decimal('0.00')  # ✅ CORRECTO
```

### 4. Revisar triggers en la base de datos

**Comando SQL para verificar:**
```sql
SHOW TRIGGERS WHERE `Table` = 'transaccionesics';
```

Si existe un trigger que modifica `tasa`, debería:
- Eliminarlo, O
- Modificarlo para que siempre asigne `tasa = 0.00`

## 🛠️ ACCIONES RECOMENDADAS

### 1. Crear script de testeo

Ejecutar `test_tasa_campo.py` para encontrar todas las asignaciones problemáticas:
```bash
python test_tasa_campo.py
```

### 2. Agregar protección en el modelo

Si se encuentra el modelo `TransaccionesIcs`, agregar método `save()`:
```python
def save(self, *args, **kwargs):
    # FORZAR tasa a 0 siempre
    self.tasa = Decimal('0.00')
    super().save(*args, **kwargs)
```

### 3. Agregar signal de protección

Crear signal global en `signals.py`:
```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from tributario.models import TransaccionesIcs
from decimal import Decimal

@receiver(pre_save, sender=TransaccionesIcs)
def forzar_tasa_cero_signal(sender, instance, **kwargs):
    """Signal que fuerza tasa a 0 antes de guardar"""
    instance.tasa = Decimal('0.00')
```

## 📝 NOTAS IMPORTANTES

1. **Cuando se calculan recargos moratorios:** El campo `tasa` debe permanecer en `0.00`, incluso durante el cálculo de recargos e intereses moratorios.

2. **Operación 'F':** Las transacciones con `operacion='F'` también deben tener `tasa=0.00`.

3. **Protección múltiple:** Se recomienda tener múltiples capas de protección:
   - Asignación correcta al crear
   - Método `save()` en el modelo
   - Signal de Django
   - Update directo después de guardar

## ✅ VERIFICACIÓN

Después de implementar las correcciones, verificar:
1. Generar nuevas transacciones desde `declaracion_volumen`
2. Verificar en la base de datos que `tasa = 0.00` para todas las transacciones nuevas
3. Verificar que al calcular recargos moratorios, `tasa` permanece en `0.00`

# ESTRUCTURA DE MODELOS - SISTEMA TRIBUTARIO

## ARCHIVOS DE MODELOS

### 1. ARCHIVO PRINCIPAL: `venv/Scripts/tributario/models.py`
**Este es el archivo principal que contiene todos los modelos del sistema.**

**Modelos definidos:**
- `Identificacion` - Identificaciones de contribuyentes
- `Actividad` - Actividades económicas
- `Oficina` - Oficinas municipales
- `Negocio` - Negocios registrados
- `PagoVariosTemp` - Pagos varios temporales
- `NoRecibos` - Números de recibos
- `Rubro` - Rubros tributarios
- `PlanArbitrio` - Planes de arbitrio
- `Tarifas` - Tarifas municipales

### 2. ARCHIVO SECUNDARIO: `venv/Scripts/tributario/tributario_app/models.py`
**Este archivo solo contiene modelos específicos de la aplicación tributario_app.**

**Modelos definidos:**
- `TarifasICS` - Tarifas específicas para ICS (Impuesto sobre Circulación y Servicios)

## REGLAS DE IMPORTACIÓN

### ✅ CORRECTO - Importar desde archivo principal:
```python
from tributario.models import Rubro, Tarifas, PlanArbitrio
```

### ✅ CORRECTO - Importar modelos específicos:
```python
from tributario_app.models import TarifasICS
```

### ❌ INCORRECTO - No duplicar modelos:
```python
# NO hacer esto - causa conflictos
from .tributario_app.models import Rubro  # ❌
```

## CONFLICTOS RESUELTOS

### Problema anterior:
- Modelos duplicados en ambos archivos
- Conflictos de importación
- Errores de `Conflicting models`

### Solución implementada:
1. **Centralización**: Todos los modelos principales en `tributario/models.py`
2. **Especialización**: Solo modelos específicos en `tributario_app/models.py`
3. **Importaciones claras**: Reglas estrictas de importación
4. **Documentación**: Este archivo como referencia

## MIGRACIONES

Las migraciones de Django están en:
- `venv/Scripts/tributario/tributario_app/migrations/`

## APLICACIÓN DE ESTAS REGLAS

### En views.py:
```python
# ✅ CORRECTO
from tributario.models import Rubro, Tarifas, PlanArbitrio
from tributario_app.models import TarifasICS
```

### En forms.py:
```python
# ✅ CORRECTO
from tributario.models import Rubro, Tarifas
from tributario_app.models import TarifasICS
```

### En simple_views.py:
```python
# ✅ CORRECTO
from tributario.models import Rubro, Tarifas, PlanArbitrio
from tributario_app.models import TarifasICS
```

## MANTENIMIENTO FUTURO

1. **Nuevos modelos principales**: Agregar a `tributario/models.py`
2. **Nuevos modelos específicos**: Agregar a `tributario_app/models.py`
3. **Nunca duplicar**: Un modelo solo debe existir en un archivo
4. **Actualizar importaciones**: Seguir las reglas establecidas
5. **Documentar cambios**: Actualizar este archivo si es necesario

## VERIFICACIÓN

Para verificar que no hay conflictos:
```bash
cd venv/Scripts
python manage.py check
```

Si no hay errores, la estructura está correcta.

---
**Fecha de creación**: 06/10/2025
**Última actualización**: 06/10/2025
**Estado**: ✅ CONFLICTOS RESUELTOS



























































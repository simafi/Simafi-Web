# 🚨 IMPLEMENTACIÓN: Botón Temporal para Calcular Tasas según Plan de Arbitrios

## 📋 Resumen

Se ha implementado exitosamente un **botón temporal** en el formulario de declaración de volumen que permite calcular las tasas según el plan de arbitrios. Esta funcionalidad será temporal hasta que se integre en el botón "Guardar Declaración".

## 🎯 Funcionalidad Implementada

### Proceso de Cálculo

El botón ejecuta el siguiente proceso:

1. **Selección de Tasas**: Se obtienen las tasas de la tabla `tasasdecla` según:
   - `empresa`
   - `rtm`
   - `expe`
   - `ano`
   - `rubro`
   - `tipota`

2. **Validación Tipo "F" (Fija)**:
   - Busca el valor en la tabla `tarifas` por `empresa`, `rubro`, `ano`
   - Actualiza el campo `valor` en `tasasdecla` según `empresa`, `rtm`, `expe`, `rubro`, `ano`

3. **Validación Tipo "V" (Variable)**:
   - Busca en la tabla `planarbitrio` por `empresa`, `rubro`, `ano`
   - Ordena por `codigo`
   - Valida si existe un registro donde `valorbase > minimo` y `valorbase < maximo`
   - Si no encuentra, busca con `>=` y `<=`
   - Toma el `valor` del registro encontrado
   - Actualiza el campo `valor` en `tasasdecla` según `empresa`, `rtm`, `expe`, `rubro`, `ano`

4. **ValorBase**: Se calcula automáticamente desde la declaración de volumen:
   - `valorbase = ventai + ventac + ventas + valorexcento + controlado`

## 📁 Archivos Modificados

### 1. `modules/tributario/ajax_views.py`

Se agregó la función `calcular_tasas_plan_arbitrio`:

```python
@csrf_exempt
def calcular_tasas_plan_arbitrio(request):
    """
    Vista AJAX TEMPORAL para calcular tasas según el plan de arbitrios.
    """
    # Proceso completo implementado
```

**Funcionalidades**:
- Valida parámetros obligatorios (empresa, rtm, expe)
- Obtiene valorbase de la declaración de volumen
- Procesa todas las tasas encontradas
- Maneja tasas Fijas (F) y Variables (V)
- Retorna detalle de tasas actualizadas y errores

### 2. `modules/tributario/urls.py`

Se agregó la ruta para el endpoint AJAX:

```python
# URL para cálculo temporal de tasas según plan de arbitrios
path('ajax/calcular-tasas-plan-arbitrio/', ajax_views.calcular_tasas_plan_arbitrio, name='calcular_tasas_plan_arbitrio'),
```

### 3. `venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html`

**Cambio 1**: Se agregó el botón temporal:

```html
<button type="button" onclick="calcularTasasPlanArbitrio()" class="btn" style="background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%); color: white;">
    <i class="fas fa-sliders-h"></i> 🚨 TEMPORAL: Calcular Tasas Plan Arbitrio
</button>
```

**Cambio 2**: Se agregó la función JavaScript:

```javascript
function calcularTasasPlanArbitrio() {
    // Obtiene parámetros de URL y formulario
    // Realiza petición AJAX al servidor
    // Muestra resultados detallados
    // Opción de recargar página
}
```

**Características del botón**:
- Confirmación antes de ejecutar
- Indicador de carga durante el proceso
- Mensajes detallados de resultados
- Lista de tasas actualizadas y errores
- Opción de recargar página para ver cambios

## 🔧 Tablas Utilizadas

### 1. `tasasdecla`
Campos utilizados:
- `empresa`: Filtro principal
- `rtm`: Filtro principal
- `expe`: Filtro principal
- `ano`: Filtro opcional
- `rubro`: Identificador de tasa
- `tipota`: Tipo de tasa (F=Fija, V=Variable)
- `valor`: Campo actualizado

### 2. `tarifas` (para tipo F)
Campos utilizados:
- `empresa`: Filtro
- `rubro`: Filtro
- `ano`: Filtro
- `valor`: Valor a asignar

### 3. `planarbitrio` (para tipo V)
Campos utilizados:
- `empresa`: Filtro
- `rubro`: Filtro
- `ano`: Filtro
- `codigo`: Ordenamiento
- `minimo`: Validación de rango
- `maximo`: Validación de rango
- `valor`: Valor a asignar según valorbase

### 4. `declara` (DeclaracionVolumen)
Campos utilizados para valorbase:
- `ventai`: Ventas Industria
- `ventac`: Ventas Comercio
- `ventas`: Ventas Servicios
- `valorexcento`: Valores Exentos
- `controlado`: Productos Controlados

## 🎨 Interfaz de Usuario

### Botón
- **Color**: Rosa/Magenta (gradiente #e91e63 a #ad1457)
- **Icono**: `fas fa-sliders-h`
- **Texto**: "🚨 TEMPORAL: Calcular Tasas Plan Arbitrio"
- **Posición**: En la sección de botones de acción

### Confirmación
Antes de ejecutar, se muestra:
```
🚨 FUNCIÓN TEMPORAL

¿Desea calcular las tasas según el plan de arbitrios?

Esta acción:
- Actualizará tasas de tipo F (Fijas) desde tabla tarifas
- Actualizará tasas de tipo V (Variables) según plan de arbitrio
```

### Resultados
Después de ejecutar, se muestra:
```
✅ [Mensaje general]

📊 TASAS ACTUALIZADAS:
1. Rubro: [rubro], Año: [año], Tipo: [tipo]
   Nuevo Valor: [valor]
   [mensaje descriptivo]

⚠️ TASAS CON ERRORES:
1. Rubro: [rubro], Año: [año], Tipo: [tipo]
   Error: [descripción del error]

Total procesadas: [número]
```

## 📊 Logs del Servidor

El servidor imprime logs detallados durante el proceso:

```
🔧 [CALCULAR TASAS] Parámetros: empresa=0301, rtm=..., expe=..., ano=..., rubro=...
💰 [VALORBASE] Valorbase calculado: ...
📊 [TASAS ENCONTRADAS] Total: ...
🔄 [PROCESANDO TASA] Rubro: ..., Año: ..., Tipo: F/V
✅ [TASA FIJA] Buscando en tabla tarifas...
✅ [ACTUALIZADA] Tasa Fija: ...
```

## 🚀 Uso

1. Acceder al formulario de declaración de volumen con parámetros `rtm` y `expe`
2. Hacer clic en el botón **"🚨 TEMPORAL: Calcular Tasas Plan Arbitrio"**
3. Confirmar la acción
4. Esperar el procesamiento (el botón mostrará "Procesando...")
5. Revisar los resultados en el diálogo
6. Decidir si recargar la página para ver los cambios

## ⚠️ Notas Importantes

### Temporal
Esta funcionalidad es **temporal** y debe integrarse posteriormente en el botón "Guardar Declaración".

### Valorbase
- Se calcula automáticamente desde los campos de la declaración de volumen
- Si no hay declaración guardada, se usa 0.00
- Se usa tanto para la validación inicial como para cada tasa variable

### Ordenamiento
Para tasas variables, el ordenamiento por `codigo` es importante para asegurar consistencia en la selección del plan de arbitrio.

### Validación de Rangos
Se intenta primero con operadores estrictos (`>` y `<`), y si no encuentra, se usa con inclusivos (`>=` y `<=`).

## 🔄 Próximos Pasos

1. **Probar** la funcionalidad con datos reales
2. **Validar** que las tasas se actualizan correctamente
3. **Integrar** el código en el botón "Guardar Declaración"
4. **Remover** el botón temporal una vez integrado

## ✅ Estado

- ✅ Función backend implementada
- ✅ Endpoint AJAX configurado
- ✅ Botón temporal agregado al template
- ✅ Función JavaScript implementada
- ✅ Manejo de errores completo
- ✅ Logs detallados para debugging
- ✅ Interfaz de usuario pulida

---

**Fecha de Implementación**: [Fecha actual]
**Versión**: 1.0
**Estado**: ✅ Completado































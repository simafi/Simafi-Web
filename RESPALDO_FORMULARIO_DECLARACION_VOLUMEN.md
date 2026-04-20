# 📋 RESPALDO: Formulario de Declaración de Volumen

## 📅 Fecha de Respaldo
**Fecha:** 29 de octubre de 2025, 22:41:07
**Estado:** Formulario funcional con botón temporal de cálculo de tasas

---

## ✅ Estado del Formulario

El formulario de **Declaración de Volumen** está funcionando correctamente con las siguientes funcionalidades:

### Funcionalidades Implementadas
- ✅ Carga automática de datos del negocio
- ✅ Guardado de declaraciones de volumen
- ✅ Cálculo de valor base (suma de ventas)
- ✅ Calculo de impuestos ICS
- ✅ Sistema de autoguardado
- ✅ Validación de campos
- ✅ Formato de separadores de miles
- ✅ Cálculo de multas por declaración tardía

### 🚨 Funcionalidad Nueva (Temporal)
- **Botón Temporal:** "🚨 TEMPORAL: Calcular Tasas Plan Arbitrio"
- **Ubicación:** Sección de botones de acción
- **Funcionalidad:** Calcula y actualiza tasas según el plan de arbitrios automáticamente

---

## 📁 Archivos Respaldados

### 1. Formulario Principal
**Archivo:** `declaracion_volumen_BACKUP_20251029_224107.html`
- **Ubicación:** `venv/Scripts/tributario/tributario_app/templates/`
- **Tamaño:** 192,551 bytes (188 KB)
- **Líneas:** ~3,949 líneas
- **Estado:** Funcional completo

### 2. Backend - Vista AJAX
**Archivo:** `ajax_views_BACKUP_20251029_224116.py`
- **Ubicación:** `venv/Scripts/tributario/`
- **Tamaño:** 18,940 bytes (18.5 KB)
- **Funcionalidad:** Función `calcular_tasas_plan_arbitrio` implementada

### 3. Configuración de URLs
**Archivo:** `tributario_urls_BACKUP_20251029_224116.py`
- **Ubicación:** `venv/Scripts/tributario/`
- **Tamaño:** 5,119 bytes (5 KB)
- **Funcionalidad:** URL del endpoint AJAX configurada

### 4. Backup Anterior
**Archivo:** `declaracion_volumen_backup_antes_limpiar_multa.html`
- **Fecha:** 29/10/2025 21:49:36
- **Tamaño:** 126,607 bytes (123.5 KB)
- **Nota:** Versión anterior antes de limpiar lógica de multa

---

## 🎯 Funcionalidad del Botón Temporal

### Descripción
El botón temporal permite calcular las tasas según el plan de arbitrios **sin confirmación** y guardando automáticamente.

### Proceso de Cálculo

#### 1. Tasas Fijas (Tipo "F")
- Busca el valor en la tabla `tarifas` por:
  - `empresa`
  - `rubro`
  - `ano`
- Actualiza el campo `valor` en `tasasdecla`

#### 2. Tasas Variables (Tipo "V")
- Busca en la tabla `planarbitrio` por:
  - `empresa`
  - `rubro`
  - `ano`
- Ordena por `codigo`
- Valida rangos: `valorbase > minimo AND valorbase < maximo`
- Actualiza el campo `valor` en `tasasdecla`

#### 3. ValorBase
- Calculado automáticamente desde la declaración:
  ```
  valorbase = ventai + ventac + ventas + valorexcento + controlado
  ```

### Comportamiento del Botón
1. **Sin confirmación** - Ejecuta inmediatamente
2. **Muestra indicador de carga** - "Procesando..."
3. **Mensaje de resultado** - Simple y directo
4. **Recarga automática** - Página se recarga para mostrar cambios
5. **Sin pasos adicionales** - Todo automático

---

## 📍 Ubicación del Botón

### En el Template HTML
**Líneas:** 1254-1256

```html
<button type="button" onclick="calcularTasasPlanArbitrio()" class="btn" style="background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%); color: white;">
    <i class="fas fa-sliders-h"></i> 🚨 TEMPORAL: Calcular Tasas Plan Arbitrio
</button>
```

### Función JavaScript
**Líneas:** 3823-3921

```javascript
function calcularTasasPlanArbitrio() {
    // Función completa implementada
    // - Sin confirmación
    // - Guarda automáticamente
    // - Recarga la página
}
```

### Endpoint Backend
**URL:** `/tributario/ajax/calcular-tasas-plan-arbitrio/`
**Método:** POST
**Ubicación:** `venv/Scripts/tributario/ajax_views.py`

---

## 🔧 Tablas Involucradas

### 1. `tasasdecla`
- Campo actualizado: `valor`
- Filtros: empresa, rtm, expe, ano, rubro, tipota

### 2. `tarifas` (para tipo F)
- Campos usados: empresa, rubro, ano, valor

### 3. `planarbitrio` (para tipo V)
- Campos usados: empresa, rubro, ano, codigo, minimo, maximo, valor

### 4. `declara` (DeclaracionVolumen)
- Campos para valorbase: ventai, ventac, ventas, valorexcento, controlado

---

## 🎨 Estilo del Botón

- **Color:** Rosa/Magenta (gradiente #e91e63 a #ad1457)
- **Icono:** `fas fa-sliders-h`
- **Texto:** "🚨 TEMPORAL: Calcular Tasas Plan Arbitrio"
- **Posición:** Entre "Calcular Valor Base" y "Volver a Negocios"

---

## ⚠️ Nota Importante

### Temporalidad
Esta funcionalidad es **TEMPORAL** hasta que se integre en el botón "Guardar Declaración".

### Después de Integrar
Una vez que la funcionalidad esté integrada en el botón principal:
1. Remover el botón temporal del template
2. Remover la función JavaScript
3. Integrar la lógica en el botón "Guardar Declaración"

---

## 🔄 Cómo Restaurar

### Si necesitas restaurar el archivo:

```powershell
# Restaurar formulario
Copy-Item "C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen_BACKUP_20251029_224107.html" -Destination "C:\simafiweb\venv\Scripts\tributario\tributario_app\templates\declaracion_volumen.html"

# Restaurar ajax_views
Copy-Item "C:\simafiweb\venv\Scripts\tributario\ajax_views_BACKUP_20251029_224116.py" -Destination "C:\simafiweb\venv\Scripts\tributario\ajax_views.py"

# Restaurar urls
Copy-Item "C:\simafiweb\venv\Scripts\tributario\tributario_urls_BACKUP_20251029_224116.py" -Destination "C:\simafiweb\venv\Scripts\tributario\tributario_urls.py"
```

---

## 📊 Logs del Servidor

El servidor registra logs detallados durante la ejecución:

```
🔧 [CALCULAR TASAS] Parámetros: empresa=0301, rtm=..., expe=..., ano=..., rubro=...
💰 [VALORBASE] Valorbase calculado: ...
📊 [TASAS ENCONTRADAS] Total: ...
🔄 [PROCESANDO TASA] Rubro: ..., Año: ..., Tipo: F/V
✅ [TASA FIJA/VARIABLE] Buscando en tabla...
✅ [ACTUALIZADA] Tasa: ...
```

---

## ✅ Estado Final

### Archivos Modificados
- ✅ `venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html`
- ✅ `venv/Scripts/tributario/ajax_views.py`
- ✅ `venv/Scripts/tributario/tributario_urls.py`

### Backups Creados
- ✅ `declaracion_volumen_BACKUP_20251029_224107.html`
- ✅ `ajax_views_BACKUP_20251029_224116.py`
- ✅ `tributario_urls_BACKUP_20251029_224116.py`

### Funcionalidad
- ✅ Botón agregado al template
- ✅ Función JavaScript implementada
- ✅ Endpoint backend configurado
- ✅ Guardado automático funcionando

---

## 📝 Notas Adicionales

- El backup fue creado antes de cualquier modificación adicional
- Todos los cambios fueron agregados, no removidos
- El formulario mantiene toda su funcionalidad original
- El botón temporal es la única adición
- La funcionalidad guarda automáticamente sin confirmación según la preferencia del usuario

---

**Generado automáticamente el:** 29 de octubre de 2025  
**Sistema:** Simafiweb - Módulo Tributario  
**Estado:** ✅ Respaldo completo exitoso































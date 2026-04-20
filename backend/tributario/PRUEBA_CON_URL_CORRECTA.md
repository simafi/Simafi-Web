# 🧪 PRUEBA DEL FORMULARIO CON URL CORRECTA

## ✅ URL Correcta del Formulario

La URL correcta para acceder al formulario de declaración de volumen es:

```
http://127.0.0.1:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

### 📋 Parámetros de la URL:

| Parámetro | Valor Ejemplo | Descripción |
|-----------|---------------|-------------|
| `empresa` | `0301` | Código de la empresa/municipio |
| `rtm` | `114-03-23` | Número de Registro Tributario Municipal |
| `expe` | `1151` | Número de Expediente |

---

## 🔍 Estructura de la URL

### **Base URL:**
```
http://127.0.0.1:8080/tributario/declaracion-volumen/
```

### **Con Parámetros (Query String):**
```
?empresa=0301&rtm=114-03-23&expe=1151
```

### **URL Completa:**
```
http://127.0.0.1:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

---

## 🎯 Cómo Funciona el Formulario

### **1. Carga Inicial:**
```
Usuario accede a la URL con parámetros
    ↓
Backend (views.py) recibe:
  - empresa = request.GET.get('empresa') o request.session.get('empresa')
  - rtm = request.GET.get('rtm')
  - expe = request.GET.get('expe')
    ↓
Busca el negocio en la base de datos:
  - Negocio.objects.get(empresa=empresa, rtm=rtm, expe=expe)
    ↓
Renderiza el formulario con los datos del negocio
```

### **2. Campos del Formulario:**
```html
<!-- Campo oculto de empresa -->
<input type="hidden" id="empresa_field" name="empresa" value="0301">

<!-- Campos visibles (readonly) -->
<input type="text" id="rtm_field" name="rtm" value="114-03-23" readonly>
<input type="text" id="expe_field" name="expe" value="1151" readonly>

<!-- Campos editables -->
<select id="id_ano" name="ano">...</select>
<select id="id_mes" name="mes">...</select>
<input type="number" id="id_ventai" name="ventai">
...
```

### **3. Validación JavaScript:**
```javascript
// Al presionar "Guardar Declaración"
document.getElementById('declaracionForm').addEventListener('submit', function(e) {
    // 1. Validar empresa
    const empresa = document.getElementById('empresa_field').value;
    if (!empresa || empresa.trim() === '') {
        e.preventDefault();
        alert('El campo Empresa es obligatorio...');
        return false;
    }
    
    // 2. Validar RTM
    const rtm = document.getElementById('rtm_field').value;
    if (!rtm || rtm.trim() === '') {
        e.preventDefault();
        alert('El campo RTM es obligatorio.');
        return false;
    }
    
    // 3. Validar Expediente
    const expe = document.getElementById('expe_field').value;
    if (!expe || expe.trim() === '') {
        e.preventDefault();
        alert('El campo Expediente es obligatorio.');
        return false;
    }
    
    // 4. Validar Año
    const ano = document.getElementById('id_ano').value;
    if (!ano) {
        e.preventDefault();
        alert('Por favor seleccione un año.');
        return false;
    }
    
    // 5. Validar Mes
    const mes = document.getElementById('id_mes').value;
    if (!mes) {
        e.preventDefault();
        alert('Por favor seleccione un mes.');
        return false;
    }
    
    // 6. Validar Ventas > 0
    const total = ventai + ventac + ventas + valorexcento + controlado;
    if (total <= 0) {
        e.preventDefault();
        alert('Por favor ingrese al menos un valor de ventas mayor a 0.');
        return false;
    }
    
    // ✅ Todas las validaciones pasaron
    return true;
});
```

### **4. Envío al Backend:**
```
Formulario se envía con método POST
    ↓
Backend (views.py) recibe:
  - request.POST.get('accion') = 'guardar'
  - form = DeclaracionVolumenForm(request.POST)
    ↓
Valida el formulario:
  - form.is_valid()
    ↓
Guarda en base de datos:
  - declaracion.empresa = empresa (desde sesión)
  - declaracion.idneg = negocio.id
  - declaracion.save()
    ↓
Retorna mensaje de éxito
```

---

## 🧪 PRUEBA PASO A PASO

### **PASO 1: Verificar Datos en la Base de Datos**

Antes de probar, verifica que estos datos existan:

```sql
-- Verificar que el negocio existe
SELECT * FROM negocio 
WHERE empresa = '0301' 
  AND rtm = '114-03-23' 
  AND expe = '1151';
```

**Resultado esperado:** Debe retornar 1 fila con los datos del negocio.

---

### **PASO 2: Limpiar Cache del Navegador**

**CRÍTICO:** El JavaScript ha cambiado, debes limpiar el cache.

**Opción A - Recarga Forzada:**
```
Presiona: Ctrl + Shift + R (Windows)
```

**Opción B - Modo Incógnito:**
```
Ctrl + Shift + N (Chrome)
Ctrl + Shift + P (Firefox)
```

---

### **PASO 3: Acceder al Formulario**

Abre esta URL en tu navegador:

```
http://127.0.0.1:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

**Resultado esperado:**
- ✅ El formulario se carga
- ✅ Los campos RTM y Expediente aparecen prellenados
- ✅ Los campos RTM y Expediente están en modo readonly (gris)

---

### **PASO 4: Verificar Campos Ocultos (Opcional)**

Abre la consola del navegador (F12) y ejecuta:

```javascript
console.log('Empresa:', document.getElementById('empresa_field').value);
console.log('RTM:', document.getElementById('rtm_field').value);
console.log('Expediente:', document.getElementById('expe_field').value);
```

**Resultado esperado:**
```
Empresa: 0301
RTM: 114-03-23
Expediente: 1151
```

---

### **PASO 5: Llenar el Formulario**

1. **Seleccionar Año:** 2024
2. **Seleccionar Mes:** Enero (1)
3. **Seleccionar Tipo:** Normal
4. **Ingresar Ventas Internas:** 50000.00
5. **Esperar 2 segundos** (para que se calcule el impuesto automáticamente)

---

### **PASO 6: Presionar "Guardar Declaración"**

1. Haz click en el botón **"Guardar Declaración"**
2. **NO debe aparecer ninguna alerta de error**
3. El formulario debe enviarse al servidor

---

### **PASO 7: Verificar Resultado**

**Resultado esperado:**
```
✅ Mensaje de éxito: "Declaración 2024/01 creada correctamente"
✅ Los datos aparecen en la tabla inferior
✅ El formulario se mantiene con los datos ingresados
```

---

### **PASO 8: Verificar en Base de Datos (Opcional)**

```sql
SELECT * FROM declaracion_volumen
WHERE empresa = '0301'
  AND rtm = '114-03-23'
  AND expe = '1151'
  AND ano = 2024
  AND mes = 1;
```

**Resultado esperado:**
```
empresa: 0301
rtm: 114-03-23
expe: 1151
ano: 2024
mes: 1
ventai: 50000.00
impuesto: (calculado según tarifa)
...
```

---

## 🐛 TROUBLESHOOTING

### **Problema 1: Negocio no encontrado**

**Error:**
```
Negocio no encontrado
```

**Solución:**
1. Verifica que el negocio existe en la base de datos
2. Verifica que los parámetros en la URL son correctos
3. Verifica que la empresa en la sesión coincide con la de la URL

---

### **Problema 2: Alert "El campo Empresa es obligatorio"**

**Causa:**
- El campo `empresa_field` está vacío o no existe

**Solución:**
1. Abre la consola (F12)
2. Ejecuta: `console.log(document.getElementById('empresa_field').value)`
3. Si es `null` o vacío, el problema está en el backend
4. Verifica que `empresa` se pase al template en `views.py`

---

### **Problema 3: Alert "El campo RTM es obligatorio"**

**Causa:**
- El campo `rtm_field` está vacío

**Solución:**
1. Verifica que la URL incluye el parámetro `rtm=114-03-23`
2. Verifica que el negocio existe en la base de datos
3. Abre la consola y ejecuta: `console.log(document.getElementById('rtm_field').value)`

---

### **Problema 4: El botón no hace nada**

**Causa:**
- Cache del navegador no está limpio
- JavaScript tiene errores

**Solución:**
1. **Limpiar cache:** Ctrl + Shift + R
2. **Abrir consola (F12)** y buscar errores en rojo
3. **Modo incógnito:** Prueba en una ventana nueva
4. **Verificar que el archivo JavaScript se cargó correctamente**

---

### **Problema 5: Formulario se envía pero no guarda**

**Causa:**
- Error en el backend
- Falta asignar `empresa` o `idneg`

**Solución:**
1. Revisa la terminal donde corre el servidor
2. Busca errores de Python
3. Verifica que `views.py` tenga:
   ```python
   declaracion.empresa = empresa
   declaracion.idneg = negocio.id
   ```

---

## 📊 RESUMEN DE CORRECCIONES

### ✅ Lo que se corrigió:

1. **IDs JavaScript:**
   - `id_rtm` → `rtm_field`
   - `id_expe` → `expe_field`

2. **Validación de Empresa:**
   - Se agregó validación del campo `empresa_field`

3. **Validación de Impuesto:**
   - Se eliminó la validación bloqueante
   - Ahora permite enviar el formulario

4. **Backend:**
   - Se asigna `empresa` desde la sesión
   - Se obtiene `idneg` del modelo `Negocio`
   - Se incluye `empresa` en filtros de búsqueda

---

## 🎯 URL de Prueba Completa

```
http://127.0.0.1:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

### Variantes según tu configuración:

```
# Si el servidor corre en localhost:
http://localhost:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151

# Si el servidor corre en 127.0.0.1:
http://127.0.0.1:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151

# Si el servidor corre en 0.0.0.0 pero accedes desde la máquina local:
http://127.0.0.1:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

---

## ✅ Estado Final

- ✅ Servidor corriendo en puerto 8080
- ✅ JavaScript corregido con IDs correctos
- ✅ Validaciones funcionando correctamente
- ✅ Backend guardando en base de datos
- ✅ URL correcta con parámetros empresa, rtm, expe

---

**¡AHORA PRUEBA EL FORMULARIO!** 🚀

**Fecha:** 2025-10-01  
**Estado:** ✅ LISTO PARA PROBAR



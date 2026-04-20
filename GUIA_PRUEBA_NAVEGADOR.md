# 🧪 GUÍA DE PRUEBA EN NAVEGADOR - PASO A PASO

## ✅ ESTADO DEL CÓDIGO

**Verificación del código en disco:**
- ✅ Template: 2927 líneas
- ✅ función sincronizarCamposHidden() existe
- ✅ Se llama automáticamente
- ✅ Campo hidden_unidadFactor_impuesto existe
- ✅ Importaciones correctas en views.py
- ✅ Modelos agregados correctamente

---

## 🌐 PASO 1: ABRIR EL FORMULARIO

**URL:**
```
http://127.0.0.1:8080/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151
```

**IMPORTANTE:** 
- Si ya lo tenías abierto: **Ctrl+F5** (limpiar caché del navegador)
- Espera a que cargue completamente

---

## 🔍 PASO 2: ABRIR DEVELOPER TOOLS

1. Presionar **F12**
2. Ir a la pestaña **Console**
3. Dejar abierta para ver los mensajes

---

## 🧪 PASO 3: VERIFICAR INICIALIZACIÓN

**Ejecuta en Console (copiar y pegar):**

### **A. Verificar que el sistema está cargado:**
```javascript
window.declaracionVolumenInteractivo
```
**Debe retornar:** Un objeto (no `undefined`)

### **B. Verificar variables ocultas:**
```javascript
window.declaracionVolumenInteractivo.variablesOcultas
```
**Debe mostrar:**
```javascript
{
    ventai_base: 0,
    ventai_impuesto: 0,
    ...
    unidadFactor_impuesto: 0  ← DEBE ESTAR AQUÍ
}
```

### **C. Verificar que los campos existen:**
```javascript
document.getElementById('id_unidad')
document.getElementById('id_factor')
document.getElementById('id_impuesto')
document.getElementById('hidden_unidadFactor_impuesto')
```
**Cada uno debe retornar:** Un elemento HTML (no `null`)

---

## 📝 PASO 4: INGRESAR VALORES

1. En el formulario, buscar el campo **"Unidad"**
2. Ingresar: `1000`
3. Presionar **Tab**
4. Buscar el campo **"Factor"**
5. Ingresar: `5.50`
6. Presionar **Tab**

---

## ✅ PASO 5: VERIFICAR EN CONSOLE

**Deberías ver estos mensajes:**

```
📝 EVENT INPUT DISPARADO PARA: unidad con valor: "1000"
🔢 CALCULANDO IMPUESTOS PARA CAMPO: unidad
🧮 Cálculo Factor × Unidad:
   Factor: 5.5
   Unidad: 1000
   Resultado: 5.5 × 1000 = 5500
📊 Unidad × Factor: 1000 × 5.5 = L. 5500.00  ← CÁLCULO
💰 TOTAL IMPUESTO FINAL: L. 5500.00
✅ Campo impuesto actualizado: ... L. 5500.00
🔄 Sincronizando variables ocultas con campos hidden...  ← SINCRONIZACIÓN
   ✅ unidadFactor_impuesto: 5500  ← VALOR ACTUALIZADO
✅ Campos hidden sincronizados correctamente
```

**Si NO ves estos mensajes:**
- ❌ El navegador está usando caché viejo
- ✅ Solución: Ctrl+F5 para recargar

---

## 🔎 PASO 6: VERIFICAR CAMPOS HIDDEN

**Ejecuta en Console:**

```javascript
// Verificar que el campo hidden se actualizó
document.getElementById('hidden_unidadFactor_impuesto').value
```

**Debe retornar:** `"5500"` (o el valor calculado)

**Si retorna "0":**
- ❌ La función sincronizarCamposHidden() NO se ejecutó
- ❌ O el navegador usa versión vieja

---

## 💾 PASO 7: PROBAR GUARDADO

1. **Presionar botón "Guardar"**
2. **Esperar confirmación**
3. **Recargar la página** (F5)
4. **Verificar que los valores persisten:**
   - Campo Unidad debe mostrar: 1000
   - Campo Factor debe mostrar: 5.50
   - Campo Impuesto debe mostrar: L. 5,500.00

**Si los valores NO persisten:**
- ❌ Los campos hidden NO se actualizaron antes de guardar
- ❌ O hay error en el backend

---

## 🐛 DIAGNÓSTICO DE PROBLEMAS

### **Problema A: NO aparecen mensajes en console**

**Síntomas:**
- Console está vacía
- No hay ningún mensaje del sistema

**Causa:**
- Navegador usando caché viejo
- JavaScript tiene errores

**Solución:**
```
1. Ctrl+F5 (limpiar caché)
2. Buscar errores rojos en console
3. Verificar que no haya "Uncaught" o "TypeError"
```

---

### **Problema B: Mensajes aparecen PERO campo NO se actualiza**

**Síntomas:**
- Ves "📊 Unidad × Factor: 1000 × 5.5 = L. 5500.00"
- Pero campo "Impuesto" sigue en 0

**Verificar en Console:**
```javascript
// Ver si el campo existe
document.getElementById('id_impuesto')

// Ver su valor
document.getElementById('id_impuesto').value

// Intentar actualizar manualmente
document.getElementById('id_impuesto').value = '5500.00'
```

**Causa posible:**
- Campo está en `readonly`
- Hay otro script que sobreescribe el valor
- ID del campo es diferente

---

### **Problema C: Campo se actualiza PERO NO se guarda**

**Síntomas:**
- Campo muestra L. 5,500.00
- Al guardar y recargar, vuelve a 0

**Verificar en Console ANTES de guardar:**
```javascript
// Ver valor del campo hidden
document.getElementById('hidden_unidadFactor_impuesto').value
// DEBE ser "5500", NO "0"
```

**Si es "0":**
- ❌ La función `sincronizarCamposHidden()` NO se ejecutó
- ❌ O el navegador usa versión vieja del código

**Solución:**
```
1. Ctrl+F5 (recargar COMPLETO)
2. Verificar en console que aparezca:
   "🔄 Sincronizando variables ocultas..."
   "✅ unidadFactor_impuesto: 5500"
```

---

## 📊 COMANDOS DE VERIFICACIÓN RÁPIDA

**Copia y pega TODOS estos comandos en Console:**

```javascript
console.log('=== VERIFICACIÓN COMPLETA ===');

// 1. Sistema
console.log('1. Sistema:', window.declaracionVolumenInteractivo ? '✅ Cargado' : '❌ No cargado');

// 2. Variables ocultas
if (window.declaracionVolumenInteractivo) {
    console.log('2. unidadFactor_impuesto en variablesOcultas:', 
        'unidadFactor_impuesto' in window.declaracionVolumenInteractivo.variablesOcultas ? '✅ Sí' : '❌ No');
}

// 3. Campos del formulario
console.log('3. Campo id_unidad:', document.getElementById('id_unidad') ? '✅ Existe' : '❌ No existe');
console.log('4. Campo id_factor:', document.getElementById('id_factor') ? '✅ Existe' : '❌ No existe');
console.log('5. Campo id_impuesto:', document.getElementById('id_impuesto') ? '✅ Existe' : '❌ No existe');
console.log('6. Campo hidden_unidadFactor_impuesto:', document.getElementById('hidden_unidadFactor_impuesto') ? '✅ Existe' : '❌ No existe');

// 4. Valores actuales
console.log('7. Valor Unidad:', document.getElementById('id_unidad')?.value);
console.log('8. Valor Factor:', document.getElementById('id_factor')?.value);
console.log('9. Valor Impuesto:', document.getElementById('id_impuesto')?.value);
console.log('10. Valor hidden:', document.getElementById('hidden_unidadFactor_impuesto')?.value);

console.log('=== FIN VERIFICACIÓN ===');
```

**Interpretación:**
- Si TODOS muestran ✅: El código está correcto
- Si alguno muestra ❌: Identifica cuál falla

---

## 🎯 PRUEBA FINAL

**Ejecuta en Console para forzar el cálculo:**

```javascript
// Simular que el usuario ingresó valores
document.getElementById('id_unidad').value = '1000';
document.getElementById('id_factor').value = '5.50';

// Forzar el cálculo
window.declaracionVolumenInteractivo.calcularEnTiempoReal('unidad');

// Esperar 1 segundo y verificar
setTimeout(() => {
    console.log('Valor del campo impuesto:', document.getElementById('id_impuesto').value);
    console.log('Valor del campo hidden:', document.getElementById('hidden_unidadFactor_impuesto').value);
}, 1000);
```

**Resultado esperado:**
```
Valor del campo impuesto: 5500.00
Valor del campo hidden: 5500
```

**Si el hidden es "0":**
- La función `sincronizarCamposHidden()` NO se está ejecutando
- Necesitas recargar con Ctrl+F5

---

## ✅ CRITERIOS DE ÉXITO

| Verificación | Estado Esperado |
|--------------|-----------------|
| Sistema cargado | ✅ window.declaracionVolumenInteractivo existe |
| Variable existe | ✅ unidadFactor_impuesto en variablesOcultas |
| Campos existen | ✅ id_unidad, id_factor, id_impuesto, hidden_unidadFactor_impuesto |
| Al ingresar valores | ✅ Console muestra "📊 Unidad × Factor..." |
| Campo impuesto | ✅ Se actualiza visualmente |
| Sincronización | ✅ Console muestra "🔄 Sincronizando..." |
| Campo hidden | ✅ hidden_unidadFactor_impuesto.value = "5500" |
| Al guardar | ✅ Valores persisten al recargar |

---

**Si TODOS los criterios se cumplen: ✅ El sistema funciona correctamente**

**Si alguno falla: Identifica cuál y revisa la sección de diagnóstico correspondiente**

























































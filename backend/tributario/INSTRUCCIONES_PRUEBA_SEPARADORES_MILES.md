# 🔍 INSTRUCCIONES: PRUEBA MANUAL CON SEPARADORES DE MILES

## ✅ CORRECCIONES APLICADAS

Se han aplicado las siguientes correcciones para **PERMITIR valores con separadores de miles (comas)**:

### **1. Formulario Django (forms.py)**
- ✅ Cambiado `inputmode='decimal'` → `inputmode='text'` 
- ✅ Aumentado `maxlength` de 17 a 20 caracteres
- ✅ Removido atributo `pattern` restrictivo
- ✅ Agregados métodos `clean_` para limpiar comas antes de validar

### **2. Template HTML (declaracion_volumen.html)**
- ✅ Event listeners modificados para **PERMITIR** comas
- ✅ Función `limpiarYParsearNumero()` para parsear correctamente valores con comas
- ✅ Validación de formulario actualizada para manejar comas

### **3. Vista Backend (views.py)**
- ✅ Limpieza de valores con comas antes de guardar en BD

---

## 📋 PRUEBA MANUAL EN EL NAVEGADOR

### **Paso 1: Limpiar Cache del Navegador**

**IMPORTANTE:** Debes limpiar el cache para cargar los cambios:

```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

O en el navegador:
- Chrome/Edge: F12 → Network → Disable cache
- Luego recargar la página

---

### **Paso 2: Acceder al Formulario**

Abre tu navegador y ve a:

```
http://127.0.0.1:8080/tributario/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

---

### **Paso 3: Abrir la Consola del Navegador**

Presiona **F12** para abrir las herramientas de desarrollo y ve a la pestaña **Console**.

Esto te permitirá ver los mensajes de depuración:
- ✅ Mensajes de validación
- ✅ Valores con comas siendo parseados
- ❌ Errores si los hay

---

### **Paso 4: Ingresar Valores CON SEPARADORES DE MILES**

Completa el formulario con estos valores de prueba:

| Campo | Valor a Ingresar |
|-------|------------------|
| **Año** | 2024 |
| **Mes** | Marzo (3) |
| **Tipo** | Normal |
| **Ventas Rubro Producción** | `555,555` |
| **Ventas Mercadería** | `1,000,000.50` |
| **Ventas por Servicios** | `250,000.25` |
| **Valores Exentos** | `100,000` |
| **Productos Controlados** | `50,000.00` |
| **Unidad** | 1000 |
| **Factor** | `1,500.50` |
| **Ajuste** | `10,000.00` |

---

### **Paso 5: Verificar en la Consola**

**ANTES de presionar "Guardar Declaración"**, verifica en la consola que veas mensajes como:

```javascript
✅ Campo id_ventai permite comas: 555,555 (longitud: 7)
✅ Campo id_ventac permite comas: 1,000,000.50 (longitud: 12)
✅ Campo id_ventas permite comas: 250,000.25 (longitud: 10)
```

Esto confirma que los campos **ESTÁN ACEPTANDO** las comas.

---

### **Paso 6: Presionar "Guardar Declaración"**

1. **Presiona el botón "Guardar Declaración"**
2. **Observa la consola del navegador**

**Deberías ver:**

```javascript
Acción detectada: guardar
Validando formulario para guardar...
Empresa OK: 0301
RTM OK: 114-03-23
Expediente OK: 1151
Año OK: 2024
Campo ventai: "555,555" → 555555
Campo ventac: "1,000,000.50" → 1000000.50
Campo ventas: "250,000.25" → 250000.25
Ventas OK: 1905555.75 Campos con valor: 7
Todas las validaciones pasaron. Enviando formulario...
```

---

### **Paso 7: Verificar Respuesta del Servidor**

**En la terminal del servidor** (donde corre `python manage.py runserver`), deberías ver:

```
================================================================================
BACKEND - Limpiando valores con separadores de miles:
  ventai: '555,555' → '555555'
  ventac: '1,000,000.50' → '1000000.50'
  ventas: '250,000.25' → '250000.25'
  valorexcento: '100,000' → '100000'
  controlado: '50,000.00' → '50000.00'
  factor: '1,500.50' → '1500.50'
  ajuste: '10,000.00' → '10000.00'
✅ Declaración guardada correctamente: Declaración 2024/03 creada correctamente
================================================================================
```

---

### **Paso 8: Verificar en la Base de Datos**

Puedes verificar que se guardó correctamente consultando la BD:

```sql
SELECT 
    empresa, rtm, expe, ano, mes,
    ventai, ventac, ventas, valorexcento, controlado,
    factor, ajuste
FROM declaracion_volumen
WHERE empresa = '0301' 
  AND rtm = '114-03-23' 
  AND expe = '1151'
  AND ano = 2024
  AND mes = 3
ORDER BY ano DESC, mes DESC
LIMIT 1;
```

**Valores Esperados:**

| Campo | Valor Guardado |
|-------|----------------|
| ventai | 555555.00 |
| ventac | 1000000.50 |
| ventas | 250000.25 |
| valorexcento | 100000.00 |
| controlado | 50000.00 |
| factor | 1500.50 |
| ajuste | 10000.00 |

---

## 🐛 TROUBLESHOOTING

### **Problema 1: Los campos NO aceptan comas al escribir**

**Síntoma:** Al intentar escribir una coma, el campo la rechaza o la elimina inmediatamente.

**Causa Probable:**
- Cache del navegador no limpiado
- Atributo `inputmode='decimal'` aún presente en el HTML renderizado

**Solución:**
1. Limpiar cache con **Ctrl + Shift + R**
2. Verificar en el inspector de elementos (F12 → Elements) que el campo tenga:
   ```html
   <input inputmode="text" maxlength="20" ...>
   ```
3. Si sigue mostrando `inputmode="decimal"`, reinicia el servidor

---

### **Problema 2: Error al presionar "Guardar Declaración"**

**Síntoma:** Aparece un alert con mensaje de error.

**Diagnóstico:**
1. Abre la **Consola** (F12 → Console)
2. Busca mensajes de error **ANTES** del alert
3. Verifica qué validación está fallando

**Posibles Errores:**

#### **Error:** "El campo Empresa es obligatorio"
```javascript
alert('El campo Empresa es obligatorio. Por favor inicie sesión nuevamente.');
```
**Solución:** Reinicia sesión o verifica que el campo `empresa_field` esté en el HTML

#### **Error:** "El campo RTM es obligatorio"
```javascript
alert('El campo RTM es obligatorio.');
```
**Solución:** Verifica que el campo `rtm_field` tenga valor

#### **Error:** "Por favor ingrese al menos un valor de ventas mayor a 0"
```javascript
alert('Por favor ingrese al menos un valor de ventas mayor a 0 en cualquier campo de ventas.');
```
**Solución:** Asegúrate de que **al menos un campo** de ventas tenga un valor > 0

---

### **Problema 3: Formulario se envía pero NO guarda en BD**

**Síntoma:** 
- La consola del navegador muestra "Todas las validaciones pasaron"
- La página recarga
- Pero en la terminal del servidor NO aparece el mensaje de guardado

**Diagnóstico:**
1. Verifica la **terminal del servidor**
2. Busca mensajes de error de Django
3. Busca si aparece el mensaje:
   ```
   ❌ Errores en el formulario:
   ```

**Posibles Causas:**

#### **Causa 1:** Validación de Django rechaza el valor
**Mensaje en terminal:**
```
❌ Errores en el formulario:
  ventai: ['Enter a number.']
```
**Solución:** Los métodos `clean_` no están funcionando. Verifica que los cambios en `forms.py` se aplicaron correctamente.

#### **Causa 2:** Error en la limpieza del backend
**Mensaje en terminal:**
```
Traceback...
ValueError: could not convert string to float: '555,555'
```
**Solución:** La limpieza en `views.py` no está funcionando. Verifica el código de limpieza.

---

### **Problema 4: Servidor no inicia**

**Síntoma:**
```
ConnectionRefusedError: [WinError 10061]
```

**Solución:**
1. Verifica que el servidor esté corriendo:
   ```powershell
   tasklist | findstr python
   ```
2. Si no hay procesos, inicia el servidor:
   ```powershell
   cd venv\Scripts
   python manage.py runserver 0.0.0.0:8080
   ```

---

## 📊 CASOS DE PRUEBA RECOMENDADOS

### **Test 1: Valor simple con coma**
```
INPUT: 555,555
ESPERADO: 555555.00 en BD
```

### **Test 2: Valor con coma y decimales**
```
INPUT: 555,555.50
ESPERADO: 555555.50 en BD
```

### **Test 3: Valor con múltiples comas**
```
INPUT: 1,234,567.89
ESPERADO: 1234567.89 en BD
```

### **Test 4: Todos los campos con comas**
```
Ventas Rubro Producción: 1,000,000.00
Ventas Mercadería: 500,000.50
Ventas por Servicios: 250,000.25
Valores Exentos: 100,000.00
Productos Controlados: 50,000.00
Factor: 1,500.50
Ajuste: 10,000.00

ESPERADO: Todos guardados correctamente
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de hacer la prueba, verifica:

- [ ] **Servidor Django corriendo** en http://127.0.0.1:8080
- [ ] **Cache del navegador limpiado** (Ctrl + Shift + R)
- [ ] **Consola del navegador abierta** (F12 → Console)
- [ ] **Terminal del servidor visible** para ver los logs
- [ ] **Sesión iniciada** con empresa 0301

---

## 🎯 RESULTADO ESPERADO

**ÉXITO TOTAL se confirma cuando:**

1. ✅ Puedes **ESCRIBIR** comas en los campos sin que se eliminen
2. ✅ La **CONSOLA** muestra mensajes de que los campos permiten comas
3. ✅ Al presionar **"Guardar Declaración"** NO aparecen alerts de error
4. ✅ La **TERMINAL DEL SERVIDOR** muestra el mensaje de guardado exitoso
5. ✅ Los valores en la **BASE DE DATOS** coinciden con lo esperado (sin comas)

---

**¡PRUEBA AHORA CON EL VALOR ESPECÍFICO: 555,555!** 🚀

**Fecha:** 2025-10-01  
**Estado:** ✅ CONFIGURACIÓN COMPLETA APLICADA  
**Servidor:** http://127.0.0.1:8080  
**Formulario:** /tributario/declaracion-volumen/



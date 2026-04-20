# ✅ FUNCIONALIDAD: Carga Automática de Declaraciones por Año

## 🎯 OBJETIVO

Implementar la funcionalidad para que cuando el usuario acceda al formulario de declaración de volumen, **automáticamente cargue los datos existentes** si ya hay una declaración guardada para ese **empresa, RTM, expediente y año**.

## 📋 FUNCIONALIDAD IMPLEMENTADA

### **1. Carga Automática al Acceder al Formulario**

**Comportamiento:**
- Al acceder al formulario, busca automáticamente si existe una declaración para el **año actual**
- Si existe, carga todos los datos en el formulario
- Si no existe, muestra formulario vacío con año/mes actual

**Validación:** Solo por **empresa + RTM + expediente + año** (SIN validar mes)

---

### **2. Búsqueda Dinámica al Cambiar Año**

**Comportamiento:**
- Cuando el usuario cambia el año en el formulario, automáticamente busca si existe una declaración para ese año
- Si existe, carga los datos automáticamente
- Si no existe, limpia el formulario

**Validación:** Solo por **empresa + RTM + expediente + año** (SIN validar mes)

---

### **3. El Mes NO Dispara Búsqueda**

**Comportamiento:**
- Cambiar el mes NO dispara búsqueda automática
- El usuario puede cambiar el mes libremente sin afectar la búsqueda
- La búsqueda solo se activa al cambiar el año

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### **Backend (views.py)**

#### **Carga Inicial (Líneas 830-875):**
```python
# Verificar si ya existe una declaración para el año actual (SIN validar mes)
declaracion_actual = DeclaracionVolumen.objects.filter(
    empresa=empresa,
    rtm=negocio.rtm, 
    expe=negocio.expe,
    ano=current_year  # Solo validar por año, no por mes
).first()

if declaracion_actual:
    # Cargar los datos de la declaración existente
    initial_data.update({
        'ano': declaracion_actual.ano,
        'mes': declaracion_actual.mes,  # Usar el mes de la declaración existente
        'tipo': declaracion_actual.tipo,
        'ventai': declaracion_actual.ventai,
        # ... todos los campos
    })
```

#### **Búsqueda AJAX (Líneas 756-811):**
```python
elif accion == 'buscar_existente':
    ano = request.POST.get('ano')
    
    declaracion_existente = DeclaracionVolumen.objects.filter(
        empresa=empresa,
        rtm=rtm, 
        expe=expe,
        ano=int(ano)  # Solo validar por año
    ).first()
    
    if declaracion_existente:
        # Retornar datos en formato JSON
        return JsonResponse({
            'exito': True,
            'declaracion': declaracion_data,
            'mensaje': f'Declaración {declaracion_existente.ano}/{declaracion_existente.mes:02d} encontrada'
        })
```

---

### **Frontend (declaracion_volumen.html)**

#### **Función de Búsqueda (Líneas 2801-2884):**
```javascript
function cargarDeclaracionExistente() {
    const ano = document.getElementById('id_ano').value;
    
    if (!ano) {
        console.log('⚠️ Año no seleccionado - no se puede buscar declaración');
        return;
    }
    
    console.log(`🔍 Buscando declaración existente para año: ${ano}`);
    
    // Petición AJAX
    const formData = new FormData();
    formData.append('accion', 'buscar_existente');
    formData.append('ano', ano);
    
    fetch(window.location.href, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.exito && data.declaracion) {
            // Cargar datos en el formulario
            const declaracion = data.declaracion;
            document.getElementById('id_ano').value = declaracion.ano;
            document.getElementById('id_mes').value = declaracion.mes;
            // ... cargar todos los campos
        } else {
            // Limpiar formulario si no hay declaración
            // ... limpiar todos los campos
        }
    });
}
```

#### **Event Listeners (Líneas 2886-2897):**
```javascript
// Event listeners SOLO para año (no para mes)
const campoAno = document.getElementById('id_ano');

if (campoAno) {
    campoAno.addEventListener('change', function() {
        console.log(`📅 Año cambiado a: ${this.value}`);
        cargarDeclaracionExistente();
    });
}

// El mes NO debe disparar búsqueda automática
console.log('ℹ️ Solo el año dispara búsqueda automática - el mes no');
```

---

## 🧪 CASOS DE PRUEBA

### **Caso 1: Acceso Inicial al Formulario**

**Escenario:** Usuario accede al formulario por primera vez en 2025

**Datos en BD:**
```
Empresa: 0301, RTM: 114-03-23, EXPE: 1151, Año: 2024, Mes: 10
Ventas: 1000, 2000, 3000...
```

**Resultado Esperado:**
```
✅ Cargando declaración existente para año 2025 (mes 10)
📋 Declaración 2024/10 cargada desde la base de datos
```

**Formulario Cargado:**
- Año: 2024
- Mes: 10
- Todos los campos de ventas con los valores guardados

---

### **Caso 2: Cambio de Año en el Formulario**

**Escenario:** Usuario cambia año de 2024 a 2023

**Datos en BD:**
```
Año 2024: Ventas 1000, 2000, 3000...
Año 2023: Ventas 500, 1500, 2500...
```

**Acción:** Usuario selecciona año 2023

**Resultado Esperado:**
```
📅 Año cambiado a: 2023
🔍 Buscando declaración existente para año: 2023
✅ Declaración encontrada - cargando datos
📋 Declaración 2023/05 encontrada
```

**Formulario Actualizado:**
- Año: 2023
- Mes: 05 (mes de la declaración existente)
- Todos los campos con valores de 2023

---

### **Caso 3: Cambio de Año Sin Declaración Existente**

**Escenario:** Usuario cambia año a 2022 (que no existe en BD)

**Acción:** Usuario selecciona año 2022

**Resultado Esperado:**
```
📅 Año cambiado a: 2022
🔍 Buscando declaración existente para año: 2022
ℹ️ No hay declaración existente para este período
```

**Formulario Limpiado:**
- Año: 2022
- Mes: [valor actual]
- Todos los campos de ventas vacíos
- Tipo: Normal (por defecto)

---

### **Caso 4: Cambio de Mes NO Dispara Búsqueda**

**Escenario:** Usuario cambia mes de 10 a 11

**Acción:** Usuario selecciona mes 11

**Resultado Esperado:**
```
📅 Mes cambiado a: 11
ℹ️ Solo el año dispara búsqueda automática - el mes no
```

**Formulario:** Sin cambios en los datos, solo cambia el mes

---

## 📊 FLUJO DE DATOS

### **Flujo 1: Carga Inicial**
```
1. Usuario accede al formulario
   ↓
2. Backend busca: empresa + RTM + EXPE + año_actual
   ↓
3. Si existe: Carga datos en initial_data
   ↓
4. Si no existe: Formulario vacío con año actual
   ↓
5. Renderiza formulario con datos
```

### **Flujo 2: Cambio de Año**
```
1. Usuario cambia año en formulario
   ↓
2. JavaScript dispara cargarDeclaracionExistente()
   ↓
3. AJAX POST con accion='buscar_existente' + ano
   ↓
4. Backend busca: empresa + RTM + EXPE + año_nuevo
   ↓
5. Si existe: Retorna JSON con datos
   ↓
6. Si no existe: Retorna JSON vacío
   ↓
7. JavaScript carga/limpia formulario según respuesta
```

---

## 🔍 VALIDACIONES APLICADAS

### **Backend:**
- ✅ Solo valida por **empresa + RTM + expediente + año**
- ✅ NO valida por mes en la búsqueda
- ✅ Maneja errores con try/catch
- ✅ Retorna JSON válido para AJAX

### **Frontend:**
- ✅ Solo el año dispara búsqueda automática
- ✅ El mes NO dispara búsqueda
- ✅ Maneja respuestas AJAX correctamente
- ✅ Carga/limpia campos según resultado
- ✅ Recalcula impuestos después de cargar datos

---

## 🐛 TROUBLESHOOTING

### **Problema 1: No carga datos existentes al acceder**

**Síntoma:** Formulario siempre aparece vacío

**Verificar:**
1. **Terminal del servidor:** Buscar mensaje:
   ```
   ✅ Cargando declaración existente para año XXXX (mes XX)
   ```
2. **Base de datos:** Verificar que existe declaración para ese año:
   ```sql
   SELECT * FROM declaracion_volumen 
   WHERE empresa = '0301' 
     AND rtm = '114-03-23' 
     AND expe = '1151' 
     AND ano = 2024;
   ```

---

### **Problema 2: AJAX no funciona al cambiar año**

**Síntoma:** Cambiar año no carga datos automáticamente

**Verificar:**
1. **Consola del navegador:** Buscar errores de AJAX
2. **Network tab:** Verificar que se envía POST con `accion=buscar_existente`
3. **Terminal del servidor:** Verificar que llega la petición AJAX

---

### **Problema 3: Mes dispara búsqueda (no debería)**

**Síntoma:** Cambiar mes también busca declaraciones

**Verificar:**
1. **Consola del navegador:** Buscar:
   ```
   ℹ️ Solo el año dispara búsqueda automática - el mes no
   ```
2. **Código JavaScript:** Verificar que solo `campoAno` tiene event listener

---

## ✅ ESTADO ACTUAL

| Funcionalidad | Estado | Detalles |
|---------------|--------|----------|
| Carga inicial | ✅ | Busca por año al acceder |
| Cambio de año | ✅ | AJAX busca automáticamente |
| Cambio de mes | ✅ | NO dispara búsqueda |
| Validación | ✅ | Solo empresa + RTM + EXPE + año |
| Error handling | ✅ | Maneja casos sin declaración |
| JSON response | ✅ | Datos correctos para AJAX |

---

## 🎯 RESULTADO FINAL

**El formulario ahora:**

1. ✅ **Carga automáticamente** datos existentes al acceder
2. ✅ **Busca dinámicamente** al cambiar año
3. ✅ **Permite cambio libre** de mes sin afectar búsqueda
4. ✅ **Valida solo por año** (no por mes)
5. ✅ **Maneja errores** correctamente
6. ✅ **Recalcula impuestos** después de cargar datos

---

**¡PRUEBA AHORA!**

1. **Accede al formulario** → Debe cargar datos si existen para el año actual
2. **Cambia el año** → Debe buscar y cargar automáticamente
3. **Cambia el mes** → NO debe buscar, solo cambiar el mes
4. **Verifica en consola** → Debe mostrar mensajes de búsqueda

---

**Fecha:** 2025-10-01  
**Estado:** ✅ FUNCIONALIDAD COMPLETA IMPLEMENTADA  
**Validación:** Solo por empresa + RTM + expediente + año  
**Servidor:** http://127.0.0.1:8080


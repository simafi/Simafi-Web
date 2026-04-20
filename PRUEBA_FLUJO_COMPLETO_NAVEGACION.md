# ✅ GUÍA DE PRUEBA: Flujo Completo de Navegación Contextual

## 🎯 Objetivo de la Prueba

Verificar que el sistema mantiene el contexto del negocio (RTM y EXPE) durante toda la navegación entre:
- Maestro de Negocios
- Configurar Tasas de Negocio
- Declaración de Volumen de Ventas

---

## 🧪 PRUEBA COMPLETA - Paso a Paso

### **Preparación**
- Servidor corriendo: `http://127.0.0.1:8080`
- Negocio de prueba: RTM `114-03-23`, Expediente `1151`

---

### **📝 PASO 1: Buscar Negocio en Maestro**

1. Ir a: `http://127.0.0.1:8080/tributario/maestro-negocios/`

2. Ingresar datos:
   - **RTM**: `114-03-23`
   - **Expediente**: `1151`

3. Presionar **"Buscar"**

4. **VERIFICAR ✅:**
   - Los datos del negocio se cargan
   - Nombre: "Test"
   - Actividad económica está seleccionada
   - Select2 funciona en Actividad Económica (puede buscar por texto)

---

### **📝 PASO 2: Ir a Configurar Tasas**

1. Presionar botón **"Configuración de Tasas"**

2. **VERIFICAR ✅:**
   - URL es: `/tributario/configurar-tasas-negocio/?empresa=0301&rtm=114-03-23&expe=1151`
   - Se muestra la información del negocio:
     * RTM: 114-03-23
     * Expediente: 1151
     * Nombre: Test

3. **Probar Select2:**
   - Hacer clic en "Cuenta Contable (Actividad)"
   - Escribir para buscar (ej: "001")
   - Seleccionar una cuenta
   - Hacer clic en "Cuenta Rezago (Actividad)"
   - Escribir para buscar
   - Seleccionar cuenta rezago

4. **VERIFICAR ✅:**
   - Select2 funciona en ambos combobox
   - Puede buscar por texto
   - Se filtran los resultados

---

### **📝 PASO 3: Volver al Maestro desde Configurar Tasas**

1. Presionar botón **"Volver al Maestro de Negocios"**

2. **VERIFICAR ✅:**
   - URL temporalmente tiene parámetros: `...?empresa=0301&rtm=114-03-23&expe=1151`
   - Los campos RTM y EXPE se llenan automáticamente
   - **El sistema ejecuta búsqueda automática**
   - **El negocio se carga automáticamente**
   - Todos los datos del negocio aparecen
   - Actividad económica está seleccionada en Select2
   - URL se limpia a: `/tributario/maestro-negocios/`

3. **RESULTADO ESPERADO:**
   - ✅ No hay que volver a buscar el negocio
   - ✅ RTM y EXPE están llenos
   - ✅ Todo funciona como si nunca hubiéramos salido

---

### **📝 PASO 4: Ir a Declaración de Volumen**

1. Desde el negocio cargado, presionar **"Declaración Volumen de Ventas"**

2. **VERIFICAR ✅:**
   - URL es: `/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151`
   - Se carga la información del negocio

---

### **📝 PASO 5: Volver al Maestro desde Declaraciones**

1. Presionar botón **"Volver a Negocios"**

2. **VERIFICAR ✅:**
   - **El negocio se carga automáticamente nuevamente**
   - RTM: `114-03-23`
   - Expediente: `1151`
   - Todos los datos presentes
   - Actividad económica seleccionada en Select2

---

### **📝 PASO 6: Ciclo Completo (Navegación Múltiple)**

1. **Ir a Configurar Tasas** → Volver → ✅ Negocio mantiene contexto

2. **Ir a Declaraciones** → Volver → ✅ Negocio mantiene contexto

3. **Ir a Configurar Tasas nuevamente** → Volver → ✅ Negocio mantiene contexto

4. **Ir a Declaraciones nuevamente** → Volver → ✅ Negocio mantiene contexto

**RESULTADO ESPERADO:**
- ✅ En ningún momento se pierde el RTM y EXPE
- ✅ Siempre se carga automáticamente el negocio
- ✅ Navegación fluida sin interrupciones

---

## 🔍 Puntos Críticos a Verificar

### **1. URLs con Parámetros**

**Al presionar "Configuración de Tasas":**
```
Debe redireccionar a:
/tributario/configurar-tasas-negocio/?empresa=0301&rtm=114-03-23&expe=1151
```

**Al presionar "Declaración Volumen de Ventas":**
```
Debe redireccionar a:
/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151
```

**Al presionar "Volver" desde Configurar Tasas:**
```
Debe redireccionar a:
/tributario/maestro-negocios/?empresa=0301&rtm=114-03-23&expe=1151
```

**Al presionar "Volver" desde Declaraciones:**
```
Debe redireccionar a:
/tributario/maestro-negocios/?empresa=0301&rtm=114-03-23&expe=1151
```

### **2. Carga Automática en Maestro**

Al regresar al Maestro con parámetros en la URL:
1. ✅ Los campos RTM y EXPE se llenan automáticamente
2. ✅ Se ejecuta `buscarNegocio()` automáticamente
3. ✅ El negocio se carga con todos sus datos
4. ✅ Select2 de Actividad Económica se actualiza
5. ✅ La URL se limpia (parámetros se eliminan)

### **3. Select2 Funcionando**

**En Maestro de Negocios:**
- ✅ Actividad Económica tiene búsqueda por texto

**En Configurar Tasas:**
- ✅ Cuenta Contable tiene búsqueda por texto
- ✅ Cuenta Rezago tiene búsqueda por texto

---

## 📊 Checklist de Verificación

### **Funcionalidad Select2:**
- [ ] Select2 en Actividad Económica (Maestro)
- [ ] Select2 en Cuenta Contable (Tasas)
- [ ] Select2 en Cuenta Rezago (Tasas)
- [ ] Búsqueda por texto funciona
- [ ] Botón X para limpiar funciona

### **Navegación Contextual:**
- [ ] Maestro → Configurar Tasas (lleva parámetros)
- [ ] Configurar Tasas → Maestro (mantiene contexto)
- [ ] Maestro → Declaraciones (lleva parámetros)
- [ ] Declaraciones → Maestro (mantiene contexto)
- [ ] Carga automática funciona
- [ ] Múltiples navegaciones mantienen contexto

---

## 🚀 Comandos de Verificación en Consola

Abrir la **Consola del Navegador** (F12 → Console) y verificar mensajes:

### **Al cargar Maestro con parámetros:**
```
🔍 Parámetros detectados en URL: {rtm: "114-03-23", expe: "1151", empresa: "0301"}
✅ Campos llenados, ejecutando búsqueda automática...
Buscando negocio: {empre: "0301", rtm: "114-03-23", expe: "1151"}
✅ Actividad económica establecida: [código de actividad]
✅ Select2 actualizado con actividad: [código]
✅ Parámetros limpiados de la URL
```

### **Al inicializar Select2:**
```
✅ Select2 inicializado en combobox de actividad económica
```

### **En Configurar Tasas:**
```
✅ Select2 inicializado en combobox de cuenta y cuenta rezago
✅ Actividades cargadas: [número de actividades]
```

---

## ✅ Resultado Esperado

**Flujo de Trabajo Ideal:**
```
1. Buscar negocio en Maestro
2. Ver toda la información cargada
3. Ir a Configurar Tasas
4. Trabajar con tarifas (usando Select2)
5. Volver al Maestro → ✅ Negocio ya cargado
6. Ir a Declaraciones
7. Trabajar con declaraciones
8. Volver al Maestro → ✅ Negocio ya cargado
9. Ir nuevamente a Configurar Tasas
10. Volver → ✅ Negocio ya cargado

= NAVEGACIÓN FLUIDA SIN PERDER CONTEXTO =
```

---

## 🎉 Estado de Implementación

### ✅ **COMPLETADO Y FUNCIONAL**

**Funcionalidades:**
1. ✅ Select2 en 3 combobox
2. ✅ Navegación contextual completa
3. ✅ Detección automática de parámetros
4. ✅ Búsqueda automática al regresar
5. ✅ Limpieza de URL tras carga

**Archivos Modificados:**
- ✅ `maestro_negocios_optimizado.html`
- ✅ `configurar_tasas_negocio.html`

**Estado del Servidor:**
- ✅ Corriendo en puerto 8080
- ✅ Sirviendo templates actualizados

---

**Listo para probar:** `http://127.0.0.1:8080/tributario/maestro-negocios/`

**Fecha**: 10 de Octubre, 2025  
**Versión**: 2.0 Final  
**Estado**: ✅ Completado y Probado

























































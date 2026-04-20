# 🧪 GUÍA DE PRUEBA: Cálculo Unidad × Factor

## ✅ Corrección Aplicada

**Problema identificado y corregido:**
```
Error: cannot import name 'TarifasICS' from 'tributario.models'
```

**Causa:** Importaciones incorrectas en `views.py`

**Solución:** Corregidas 7 importaciones:
- ❌ `from tributario.models import TarifasICS`
- ✅ `from tributario_app.models import TarifasICS`

---

## 🎯 Estructura Correcta de Modelos

### **tributario.models (PRINCIPAL)**
```python
- TarifasImptoics  (tabla: tarifasimptoics)  ← Para productos controlados
- DeclaracionVolumen (tabla: declara)        ← Declaraciones
- Negocio, Actividad, Oficina, etc.
```

### **tributario_app.models (SECUNDARIO)**
```python
- TarifasICS  (tabla: tarifasics)  ← Específico del negocio
- Re-exporta todos de tributario.models
```

---

## 🧪 PASO A PASO: Probar Unidad × Factor

### **1. Abrir el Formulario**
```
URL: http://127.0.0.1:8080/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151
```

### **2. Abrir Consola del Navegador**
- Presionar **F12**
- Ir a la pestaña **Console**
- Dejar abierta para ver los mensajes

### **3. Ingresar Valores de Prueba**

#### **Campo Unidad:**
- Hacer clic en el campo "Unidad"
- Ingresar: `1000`
- Presionar Tab o hacer clic fuera

#### **Campo Factor:**
- Hacer clic en el campo "Factor"  
- Ingresar: `5.50`
- Presionar Tab o hacer clic fuera

### **4. Verificar en Consola**

**Mensajes esperados:**
```javascript
📝 EVENT INPUT DISPARADO PARA: unidad con valor: "1000"
🔢 CALCULANDO IMPUESTOS PARA CAMPO: unidad
📊 Valores obtenidos: {unidad: 1000, factor: 5.5, ...}

🧮 Cálculo Factor × Unidad:
   Factor: 5.5
   Unidad: 1000
   Resultado: 5.5 × 1000 = 5500

📊 Unidad × Factor: 1000 × 5.5 = L. 5500.00
✅ Variables ocultas actualizadas: {unidadFactor_impuesto: 5500, ...}

🎯 SUMANDO IMPUESTOS DESDE VARIABLES OCULTAS:
🔢 IMPUESTOS INDIVIDUALES (convertidos a números):
   • Ventas Rubro Producción: L. X.XX
   • Ventas Mercadería: L. X.XX
   • Ventas por Servicios: L. X.XX
   • Productos Controlados: L. X.XX
   • Unidad × Factor: L. 5500.00

💰 TOTAL IMPUESTO FINAL: L. [suma incluyendo 5500.00]
```

### **5. Verificar en el Formulario**

**Campo "Impuesto Total" debe mostrar:**
- ✅ Suma de todos los impuestos
- ✅ Incluye el cálculo de Unidad × Factor (L. 5,500.00)

**Campo "Multa" debe:**
- ✅ Calcularse automáticamente basado en el impuesto
- ✅ Actualizarse al cambiar Mes o Tipo

---

## 🔍 Verificación de Errores

### **✅ Sin Errores (Correcto):**
```
[10/Oct/2025 13:XX:XX] "GET /tributario/declaraciones/..." 200 121025
```

### **❌ Con Errores (Incorrecto - ya corregido):**
```
Error al cargar declaraciones: cannot import name 'TarifasICS' from 'tributario.models'
```

---

## 📊 Casos de Prueba

### **Caso 1: Cálculo Simple**
```
Entrada:
  Unidad: 100
  Factor: 2.00
  
Resultado esperado:
  100 × 2.00 = L. 200.00
  
Consola:
  📊 Unidad × Factor: 100 × 2 = L. 200.00
```

### **Caso 2: Cálculo con Decimales**
```
Entrada:
  Unidad: 1500
  Factor: 3.75
  
Resultado esperado:
  1500 × 3.75 = L. 5,625.00
  
Consola:
  📊 Unidad × Factor: 1500 × 3.75 = L. 5625.00
```

### **Caso 3: Valor Cero (No Calcula)**
```
Entrada:
  Unidad: 0
  Factor: 5.00
  
Resultado esperado:
  No se calcula (valor 0)
  
Consola:
  ⚠️ Unidad o Factor no válidos - Unidad: 0 Factor: 5
```

### **Caso 4: Con Otros Impuestos**
```
Entrada:
  Ventas Producción: 10,000
  Unidad: 500
  Factor: 4.50
  
Cálculo esperado:
  - Ventas Producción: ~L. 3.00 (tarifa ICS)
  - Unidad × Factor: L. 2,250.00
  - Total: ~L. 2,253.00
```

---

## 🎯 Funcionalidad Completa

### **Campos que Calculan Automáticamente:**

1. **Ventas Rubro Producción** → Tarifas ICS escalonadas
2. **Ventas Mercadería** → Tarifas ICS escalonadas  
3. **Ventas por Servicios** → Tarifas ICS escalonadas
4. **Productos Controlados** → Tarifas específicas categoría 2
5. **Unidad × Factor** → Multiplicación simple ✅

### **Proceso Automático:**
```
Ingresar valor → Detectar cambio → Calcular → Actualizar variables ocultas 
→ Sumar total → Actualizar impuesto → Calcular multa
```

---

## 📋 Checklist de Verificación

- [ ] Servidor corriendo sin errores
- [ ] Error de importación corregido
- [ ] Campo Unidad acepta valores enteros
- [ ] Campo Factor acepta decimales (2 decimales)
- [ ] Cálculo se dispara al cambiar Unidad
- [ ] Cálculo se dispara al cambiar Factor
- [ ] Resultado correcto: Factor × Unidad
- [ ] Se suma al total de impuestos
- [ ] Mensajes en consola aparecen correctamente
- [ ] Multa se calcula automáticamente

---

## 🌐 URLs de Prueba

**Formulario Principal:**
```
http://127.0.0.1:8080/tributario/declaraciones/?empresa=0301&rtm=114-03-23&expe=1151
```

**API de Tarifas (verificación):**
```
http://127.0.0.1:8080/tributario/api-tarifas-ics/?categoria=1
http://127.0.0.1:8080/tributario/api-tarifas-ics/?categoria=2
```

---

## ✅ Estado Final

**Servidor:** ✅ Funcionando  
**Importaciones:** ✅ Corregidas  
**Cálculo Unidad × Factor:** ✅ Implementado  
**Cálculo Productos Controlados:** ✅ Implementado  
**Sistema Completo:** ✅ Operativo

---

**Fecha:** 10 de Octubre, 2025  
**Problema:** Importaciones incorrectas causaban error  
**Solución:** Corregidas 7 referencias de TarifasICS  
**Estado:** ✅ Listo para Pruebas

























































# Análisis del Esquema de la Tabla `declara`

## 📊 Campos y Formatos de la Base de Datos

### Campos de Ventas - DECIMAL(16,2)
- `ventai` DECIMAL(16,2) - Ventas Industria
- `ventac` DECIMAL(16,2) - Ventas Comercio  
- `ventas` DECIMAL(16,2) - Ventas Servicios
- **FALTA:** `ventap` - No existe en la tabla (Ventas Producción)

### Campo de Impuesto - DECIMAL(12,2) ⚠️
- `impuesto` DECIMAL(12,2) - **DISCREPANCIA CRÍTICA**

### Otros Campos Relevantes
- `ano` DECIMAL(12,2) - Año
- `factor` DECIMAL(12,2) - Factor de cálculo
- `valorexcento` DECIMAL(16,2) - Valor exento
- `cocontrolado` DECIMAL(16,2) - Controlado

## 🚨 PROBLEMAS IDENTIFICADOS

### 1. Campo `ventap` Faltante
- El formulario usa `ventap` (Ventas Producción)
- **NO EXISTE** en la tabla `declara`
- Esto explica por qué los valores no se guardan

### 2. Discrepancia en Campo `impuesto`
- **Formulario espera:** DECIMAL(16,2) 
- **Base de datos tiene:** DECIMAL(12,2)
- **Máximo BD:** 9,999,999,999.99 (10 enteros + 2 decimales)
- **JavaScript valida:** 99,999,999,999,999.99 (14 enteros + 2 decimales)

### 3. Validaciones Incorrectas
- JavaScript valida DECIMAL(16,2) para impuesto
- Base de datos solo acepta DECIMAL(12,2)
- Valores grandes causan overflow o truncamiento

## 🔧 CORRECCIONES NECESARIAS

### Opción A: Actualizar Base de Datos
```sql
ALTER TABLE declara 
ADD COLUMN ventap DECIMAL(16,2) DEFAULT 0.00 AFTER ventas;

ALTER TABLE declara 
MODIFY COLUMN impuesto DECIMAL(16,2) DEFAULT 0.00;
```

### Opción B: Ajustar Formulario
- Remover campo `ventap` del formulario
- Limitar validación de `impuesto` a DECIMAL(12,2)
- Actualizar JavaScript para máximos correctos

## 📋 Mapeo de Campos Correcto

| Campo Formulario | Campo BD | Formato BD | Máximo BD |
|------------------|----------|------------|-----------|
| `ventai` | `ventai` | DECIMAL(16,2) | 99,999,999,999,999.99 |
| `ventac` | `ventac` | DECIMAL(16,2) | 99,999,999,999,999.99 |
| `ventas` | `ventas` | DECIMAL(16,2) | 99,999,999,999,999.99 |
| `ventap` | **❌ NO EXISTE** | - | - |
| `impuesto` | `impuesto` | DECIMAL(12,2) | 9,999,999,999.99 |

## 🎯 RECOMENDACIÓN

**Opción A (Recomendada):** Actualizar la base de datos para que coincida con el formulario:
1. Agregar campo `ventap DECIMAL(16,2)`
2. Cambiar `impuesto` a `DECIMAL(16,2)`
3. Mantener validaciones JavaScript actuales

**Opción B (Alternativa):** Ajustar formulario a la base de datos existente:
1. Remover campo `ventap` 
2. Limitar `impuesto` a DECIMAL(12,2)
3. Actualizar validaciones JavaScript

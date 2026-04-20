# Esquema CORRECTO de la Tabla `declara`

## 📊 Estructura Real de la Base de Datos

### Campos de Ventas - DECIMAL(16,2) ✅
- `ventai` DECIMAL(16,2) - Ventas Industria
- `ventac` DECIMAL(16,2) - Ventas Comercio  
- `ventas` DECIMAL(16,2) - Ventas Servicios
- `valorexcento` DECIMAL(16,2) - Valor exento
- `controlado` DECIMAL(16,2) - Valor controlado ✅ CORRECTO

### Campo de Impuesto - DECIMAL(12,2)
- `impuesto` DECIMAL(12,2) - Máximo: 9,999,999,999.99

### Otros Campos
- `id` INTEGER AUTO_INCREMENT
- `idneg` INTEGER DEFAULT 0
- `rtm` CHAR(20) 
- `expe` CHAR(10)
- `ano` DECIMAL(12,2) DEFAULT 0.00
- `tipo` DECIMAL(1,0) DEFAULT 0
- `mes` DECIMAL(4,0) DEFAULT 0
- `unidad` DECIMAL(11,0) DEFAULT 0
- `factor` DECIMAL(12,2) DEFAULT 0.00
- `fechssys` DATETIME
- `usuario` CHAR(50)

## ✅ CORRECCIÓN APLICADA

### Problema Original:
- ❌ Código buscaba: `cocontrolado`
- ✅ Campo real es: `controlado`

### Campos Faltantes:
- ❌ `ventap` - No existe en la tabla
- ✅ Solo usar: `ventai`, `ventac`, `ventas`, `controlado`

## 📋 Mapeo Correcto

| Campo Formulario | Campo BD | Formato BD | Estado |
|------------------|----------|------------|--------|
| `ventai` | `ventai` | DECIMAL(16,2) | ✅ Existe |
| `ventac` | `ventac` | DECIMAL(16,2) | ✅ Existe |
| `ventas` | `ventas` | DECIMAL(16,2) | ✅ Existe |
| `controlado` | `controlado` | DECIMAL(16,2) | ✅ Existe |
| `ventap` | ❌ NO EXISTE | - | ❌ Falta |
| `impuesto` | `impuesto` | DECIMAL(12,2) | ✅ Existe |

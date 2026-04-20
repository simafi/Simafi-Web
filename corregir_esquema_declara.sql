-- Script SQL para corregir discrepancias en la tabla 'declara'
-- Basado en el análisis del esquema actual vs formulario

-- =====================================================
-- CORRECCIÓN 1: Agregar campo ventap faltante
-- =====================================================
-- El formulario usa 'ventap' (Ventas Producción) pero no existe en la tabla

ALTER TABLE `declara` 
ADD COLUMN `ventap` DECIMAL(16,2) DEFAULT 0.00 
AFTER `ventas`;

-- =====================================================
-- CORRECCIÓN 2: Actualizar campo impuesto a DECIMAL(16,2)
-- =====================================================
-- Cambiar de DECIMAL(12,2) a DECIMAL(16,2) para consistencia

ALTER TABLE `declara` 
MODIFY COLUMN `impuesto` DECIMAL(16,2) DEFAULT 0.00;

-- =====================================================
-- CORRECCIÓN 3: Corregir campo controlado (cocontrolado)
-- =====================================================
-- El campo se llama 'cocontrolado' en la BD, verificar que sea DECIMAL(16,2)

ALTER TABLE `declara` 
MODIFY COLUMN `cocontrolado` DECIMAL(16,2) DEFAULT 0.00;

-- =====================================================
-- VERIFICACIÓN: Consultar estructura actualizada
-- =====================================================
DESCRIBE `declara`;

-- =====================================================
-- ÍNDICES ADICIONALES (Opcional)
-- =====================================================
-- Agregar índice para el nuevo campo ventap si es necesario
-- ALTER TABLE `declara` ADD INDEX `declara_idx_ventap` (`ventap`);

-- =====================================================
-- VERIFICACIÓN DE DATOS EXISTENTES
-- =====================================================
-- Verificar que no hay datos que excedan los nuevos límites
SELECT 
    COUNT(*) as total_registros,
    MAX(impuesto) as max_impuesto_actual,
    MAX(ventai) as max_ventai,
    MAX(ventac) as max_ventac,
    MAX(ventas) as max_ventas
FROM `declara`;

-- =====================================================
-- COMENTARIOS SOBRE LOS CAMBIOS
-- =====================================================
/*
ANTES:
- ventai: DECIMAL(16,2) ✓
- ventac: DECIMAL(16,2) ✓  
- ventas: DECIMAL(16,2) ✓
- ventap: NO EXISTÍA ❌
- impuesto: DECIMAL(12,2) ❌ (máx: 9,999,999,999.99)

DESPUÉS:
- ventai: DECIMAL(16,2) ✓
- ventac: DECIMAL(16,2) ✓
- ventas: DECIMAL(16,2) ✓
- ventap: DECIMAL(16,2) ✓ (NUEVO)
- impuesto: DECIMAL(16,2) ✓ (máx: 99,999,999,999,999.99)

BENEFICIOS:
1. El campo ventap ahora existe y puede almacenar datos
2. El campo impuesto puede manejar valores calculados grandes
3. Consistencia entre formulario y base de datos
4. Soporte completo para negocios con ingresos altos
*/

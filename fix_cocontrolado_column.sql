-- SOLUCIÓN 1: Agregar columna faltante
-- Ejecutar en la base de datos MySQL

USE tributario_db;  -- Cambiar por el nombre real de la BD

-- Verificar si la columna existe
SHOW COLUMNS FROM declara LIKE 'cocontrolado';

-- Si no existe, agregarla
ALTER TABLE declara 
ADD COLUMN cocontrolado DECIMAL(16,2) DEFAULT 0.00 
AFTER valorexcento;

-- Verificar que se agregó correctamente
DESCRIBE declara;

-- Opcional: Actualizar registros existentes
UPDATE declara SET cocontrolado = 0.00 WHERE cocontrolado IS NULL;

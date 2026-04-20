-- Migración manual para actualizar la longitud del campo codigo en la tabla rubros
-- De CHAR(4) a CHAR(6)
-- Fecha: 2025-10-08

-- Actualizar la estructura de la tabla rubros
ALTER TABLE `rubros` 
MODIFY COLUMN `codigo` CHAR(6) COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '';

-- Verificar que la estructura sea correcta
-- DESCRIBE rubros;


























































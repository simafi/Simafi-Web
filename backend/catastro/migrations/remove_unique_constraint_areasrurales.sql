-- Script SQL para eliminar el UniqueConstraint de la tabla areasrurales
-- Esto permite múltiples registros por cocata1

-- Eliminar el índice único si existe
ALTER TABLE `areasrurales` DROP INDEX IF EXISTS `areasrurales_idx1`;

-- Verificar que el índice fue eliminado
-- SELECT * FROM INFORMATION_SCHEMA.STATISTICS 
-- WHERE TABLE_SCHEMA = DATABASE() 
-- AND TABLE_NAME = 'areasrurales' 
-- AND INDEX_NAME = 'areasrurales_idx1';









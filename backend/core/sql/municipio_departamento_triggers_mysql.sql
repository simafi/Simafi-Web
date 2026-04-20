-- Refuerzo opcional en MySQL: la regla ya se aplica en Django (modelo Municipio.clean / save).
-- Ejecutar manualmente en el servidor si se desea impedir INSERT/UPDATE inválidos desde otros clientes.
-- Revisar nombres de esquema/tablas según su instalación.

DROP TRIGGER IF EXISTS municipio_bi_valida_depto;
DROP TRIGGER IF EXISTS municipio_bu_valida_depto;

DELIMITER //

CREATE TRIGGER municipio_bi_valida_depto
BEFORE INSERT ON municipio
FOR EACH ROW
BEGIN
  DECLARE v_ok INT DEFAULT 0;
  IF NEW.codigo IS NULL OR CHAR_LENGTH(TRIM(NEW.codigo)) < 2 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'municipio.codigo debe tener al menos 2 caracteres (prefijo departamento)';
  END IF;
  SELECT COUNT(*) INTO v_ok
  FROM departamento d
  WHERE LEFT(TRIM(NEW.codigo), 2) = CASE
    WHEN CHAR_LENGTH(TRIM(d.depto)) >= 2 THEN LEFT(TRIM(d.depto), 2)
    ELSE LPAD(TRIM(d.depto), 2, '0')
  END
  LIMIT 1;
  IF v_ok = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Prefijo de municipio sin fila correspondiente en departamento';
  END IF;
END//

CREATE TRIGGER municipio_bu_valida_depto
BEFORE UPDATE ON municipio
FOR EACH ROW
BEGIN
  DECLARE v_ok INT DEFAULT 0;
  IF NEW.codigo IS NULL OR CHAR_LENGTH(TRIM(NEW.codigo)) < 2 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'municipio.codigo debe tener al menos 2 caracteres (prefijo departamento)';
  END IF;
  SELECT COUNT(*) INTO v_ok
  FROM departamento d
  WHERE LEFT(TRIM(NEW.codigo), 2) = CASE
    WHEN CHAR_LENGTH(TRIM(d.depto)) >= 2 THEN LEFT(TRIM(d.depto), 2)
    ELSE LPAD(TRIM(d.depto), 2, '0')
  END
  LIMIT 1;
  IF v_ok = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Prefijo de municipio sin fila correspondiente en departamento';
  END IF;
END//

DELIMITER ;

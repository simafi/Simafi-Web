-- Script SQL para crear las tablas de facturación municipal
-- Ejecutar este script en la base de datos MySQL

-- Tabla de conceptos de facturación
CREATE TABLE IF NOT EXISTS conceptos_facturacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(10) DEFAULT 'TASA',
    descripcion TEXT,
    valor_base DECIMAL(12,2) DEFAULT 0.00,
    porcentaje DECIMAL(5,2) DEFAULT 0.00,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de períodos de facturación
CREATE TABLE IF NOT EXISTS periodos_facturacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    tipo_periodo VARCHAR(10) DEFAULT 'MENSUAL',
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de facturas
CREATE TABLE IF NOT EXISTS facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_factura VARCHAR(20) UNIQUE NOT NULL,
    negocio_id INT NOT NULL,
    periodo_id INT NOT NULL,
    fecha_emision DATE DEFAULT CURRENT_DATE,
    fecha_vencimiento DATE NOT NULL,
    subtotal DECIMAL(12,2) DEFAULT 0.00,
    impuestos DECIMAL(12,2) DEFAULT 0.00,
    total DECIMAL(12,2) DEFAULT 0.00,
    estado VARCHAR(10) DEFAULT 'PENDIENTE',
    observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (negocio_id) REFERENCES negocios(id),
    FOREIGN KEY (periodo_id) REFERENCES periodos_facturacion(id),
    INDEX idx_numero_factura (numero_factura),
    INDEX idx_negocio (negocio_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha_vencimiento (fecha_vencimiento)
);

-- Tabla de detalles de factura
CREATE TABLE IF NOT EXISTS detalles_factura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    concepto_id INT NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    cantidad DECIMAL(10,2) DEFAULT 1.00,
    valor_unitario DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    impuestos DECIMAL(12,2) DEFAULT 0.00,
    total DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    FOREIGN KEY (concepto_id) REFERENCES conceptos_facturacion(id)
);

-- Tabla de pagos de factura
CREATE TABLE IF NOT EXISTS pagos_factura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    numero_recibo VARCHAR(20) UNIQUE NOT NULL,
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(12,2) NOT NULL,
    forma_pago VARCHAR(15) DEFAULT 'EFECTIVO',
    referencia VARCHAR(50),
    observaciones TEXT,
    usuario_pago VARCHAR(50),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    INDEX idx_numero_recibo (numero_recibo),
    INDEX idx_factura (factura_id),
    INDEX idx_fecha_pago (fecha_pago)
);

-- Tabla de configuración de facturación
CREATE TABLE IF NOT EXISTS configuracion_facturacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa VARCHAR(4) NOT NULL,
    prefijo_factura VARCHAR(10) DEFAULT 'FAC',
    secuencia_factura INT DEFAULT 1,
    dias_vencimiento INT DEFAULT 30,
    aplicar_intereses BOOLEAN DEFAULT TRUE,
    porcentaje_interes DECIMAL(5,2) DEFAULT 2.00,
    aplicar_multas BOOLEAN DEFAULT TRUE,
    monto_multas DECIMAL(12,2) DEFAULT 50.00,
    activo BOOLEAN DEFAULT TRUE,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_empresa (empresa)
);

-- Tabla de historial de facturación
CREATE TABLE IF NOT EXISTS historial_facturacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    tipo_cambio VARCHAR(15) NOT NULL,
    descripcion TEXT NOT NULL,
    valor_anterior TEXT,
    valor_nuevo TEXT,
    usuario VARCHAR(50) NOT NULL,
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    INDEX idx_fecha_cambio (fecha_cambio)
);

-- Insertar datos de ejemplo para conceptos de facturación
INSERT INTO conceptos_facturacion (codigo, nombre, tipo, descripcion, valor_base, porcentaje) VALUES
('TASA-001', 'Tasa Municipal Básica', 'TASA', 'Tasa municipal básica para comercios', 100.00, 0.00),
('IMPUESTO-001', 'Impuesto sobre Ventas', 'IMPUESTO', 'Impuesto sobre ventas municipales', 0.00, 15.00),
('SERVICIO-001', 'Servicio de Recolección', 'SERVICIO', 'Servicio de recolección de basura', 50.00, 0.00),
('MULTA-001', 'Multa por Retraso', 'MULTA', 'Multa por pago fuera de término', 25.00, 0.00);

-- Insertar datos de ejemplo para períodos
INSERT INTO periodos_facturacion (codigo, nombre, tipo_periodo, fecha_inicio, fecha_fin) VALUES
('2025-01', 'Enero 2025', 'MENSUAL', '2025-01-01', '2025-01-31'),
('2025-02', 'Febrero 2025', 'MENSUAL', '2025-02-01', '2025-02-28'),
('2025-03', 'Marzo 2025', 'MENSUAL', '2025-03-01', '2025-03-31'),
('2025-Q1', 'Primer Trimestre 2025', 'TRIMESTRAL', '2025-01-01', '2025-03-31');

-- Insertar configuración por defecto
INSERT INTO configuracion_facturacion (empresa, prefijo_factura, secuencia_factura) VALUES
('0301', 'FAC', 1);

-- Crear índices adicionales para optimización
CREATE INDEX idx_conceptos_activo ON conceptos_facturacion(activo);
CREATE INDEX idx_periodos_activo ON periodos_facturacion(activo);
CREATE INDEX idx_facturas_fecha_emision ON facturas(fecha_emision); 
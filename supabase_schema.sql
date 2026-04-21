-- Supabase (PostgreSQL) Schema for SIMAFI Web
-- Generated based on Django models (Core, Tributario, Catastro)

-- =====================================================
-- 1. EXTENSIONS & UTILS
-- =====================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 2. CORE MODULE
-- =====================================================

-- Table: municipio
CREATE TABLE IF NOT EXISTS "municipio" (
    "id" SERIAL PRIMARY KEY,
    "codigo" VARCHAR(4) UNIQUE NOT NULL DEFAULT '',
    "descripcion" VARCHAR(29) NOT NULL,
    "fesqui" DECIMAL(5,2) DEFAULT 0.00,
    "por_concer" DECIMAL(7,2) DEFAULT 0.00,
    "vl_exento" DECIMAL(12,2) DEFAULT 0.00,
    "tasau" DECIMAL(7,2) DEFAULT 0.00,
    "tasar" DECIMAL(7,2) DEFAULT 0.00,
    "alcalde" VARCHAR(50),
    "auditor" VARCHAR(50),
    "presupuestos" VARCHAR(50),
    "contador" VARCHAR(50),
    "tesorero" VARCHAR(50),
    "secretario" VARCHAR(50),
    "proyecto" VARCHAR(50),
    "activo" VARCHAR(7),
    "financiero" VARCHAR(50),
    "tesorera" VARCHAR(50),
    "tributacion" VARCHAR(100) DEFAULT '',
    "gerentefin" VARCHAR(100),
    "gerentegeneral" VARCHAR(100),
    "porce_condo1" DECIMAL(7,2) DEFAULT 0.00,
    "porce_condo2" DECIMAL(12,2) DEFAULT 0.00,
    "fecondona1" DATE,
    "fecondona2" DATE,
    "interes" DECIMAL(7,2) DEFAULT 0.00,
    "desc_tercera" DECIMAL(12,2) DEFAULT 0.00
);

-- Table: departamento
CREATE TABLE IF NOT EXISTS "departamento" (
    "id" SERIAL PRIMARY KEY,
    "depto" VARCHAR(3) UNIQUE NOT NULL,
    "descripcion" VARCHAR(29) NOT NULL
);

-- =====================================================
-- 3. TRIBUTARIO MODULE
-- =====================================================

-- Table: identificacion (Contribuyentes)
CREATE TABLE IF NOT EXISTS "identificacion" (
    "id" SERIAL PRIMARY KEY,
    "identidad" VARCHAR(18) UNIQUE NOT NULL,
    "nombres" VARCHAR(30),
    "apellidos" VARCHAR(30),
    "fechanac" DATE
);

-- Table: actividad (Rubros)
CREATE TABLE IF NOT EXISTS "actividad" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4) NOT NULL DEFAULT '',
    "codigo" VARCHAR(20) NOT NULL DEFAULT '',
    "cuentarez" VARCHAR(20) NOT NULL DEFAULT '',
    "cuentarec" VARCHAR(20) DEFAULT '',
    "cuentaint" VARCHAR(20) DEFAULT '',
    "descripcion" VARCHAR(200) DEFAULT '',
    UNIQUE ("empresa", "codigo")
);

-- Table: oficina
CREATE TABLE IF NOT EXISTS "oficina" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4) NOT NULL,
    "codigo" VARCHAR(20) NOT NULL,
    "descripcion" VARCHAR(200),
    UNIQUE ("empresa", "codigo")
);

-- Table: negocios
CREATE TABLE IF NOT EXISTS "negocios" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4) NOT NULL,
    "rtm" VARCHAR(16) NOT NULL,
    "expe" VARCHAR(12) NOT NULL,
    "nombrenego" VARCHAR(100) DEFAULT ' ',
    "comerciante" VARCHAR(100) DEFAULT ' ',
    "identidad" VARCHAR(20) NOT NULL,
    "rtnpersonal" VARCHAR(20) DEFAULT ' ',
    "rtnnego" VARCHAR(19) DEFAULT ' ',
    "catastral" VARCHAR(17) NOT NULL,
    "identidadrep" VARCHAR(20) DEFAULT ' ',
    "representante" VARCHAR(100) DEFAULT ' ',
    "direccion" VARCHAR(100) DEFAULT ' ',
    "actividad" VARCHAR(20) DEFAULT ' ',
    "estatus" VARCHAR(1) NOT NULL,
    "descriestatus" VARCHAR(50) DEFAULT ' ',
    "fecha_ini" DATE,
    "fecha_can" DATE,
    "fecha_nacimiento" DATE,
    "telefono" VARCHAR(20) DEFAULT ' ',
    "celular" VARCHAR(20) DEFAULT ' ',
    "socios" VARCHAR(250) NOT NULL,
    "correo" VARCHAR(35) DEFAULT ' ',
    "pagweb" VARCHAR(40) DEFAULT ' ',
    "comentario" TEXT,
    "descriactividad" VARCHAR(100) DEFAULT ' ',
    "usuario" VARCHAR(10) DEFAULT ' ',
    "fechasys" TIMESTAMP WITH TIME ZONE,
    "cx" DECIMAL(12,2) DEFAULT 0.00,
    "cy" DECIMAL(12,2) DEFAULT 0.00,
    UNIQUE ("empresa", "rtm", "expe")
);

-- Table: pagovariostemp (Liquidaciones Temporales para Caja)
CREATE TABLE IF NOT EXISTS "pagovariostemp" (
    "id" BIGSERIAL PRIMARY KEY,
    "empresa" VARCHAR(6),
    "recibo" DECIMAL(12,0) NOT NULL,
    "rubro" VARCHAR(6) DEFAULT '',
    "codigo" VARCHAR(16) NOT NULL,
    "fecha" DATE,
    "identidad" VARCHAR(31),
    "nombre" VARCHAR(150),
    "descripcion" VARCHAR(200),
    "valor" DECIMAL(16,2) NOT NULL, -- Ampliado según corregir_esquema_declara
    "comentario" VARCHAR(500),
    "oficina" VARCHAR(20),
    "facturadora" VARCHAR(45),
    "aplicado" VARCHAR(1) DEFAULT '0',
    "traslado" VARCHAR(1) DEFAULT '0',
    "solvencia" DECIMAL(15,0) DEFAULT 0,
    "fecha_solv" DATE,
    "cantidad" DECIMAL(12,2) DEFAULT 0.00,
    "vl_unit" DECIMAL(12,2) DEFAULT 0.00,
    "deposito" DECIMAL(1,0) DEFAULT 0,
    "cajero" VARCHAR(20),
    "usuario" VARCHAR(30),
    "referencia" VARCHAR(20),
    "banco" VARCHAR(3),
    "Tipofa" VARCHAR(1) DEFAULT ' ',
    "Rtm" VARCHAR(20) DEFAULT ' ',
    "expe" VARCHAR(12) DEFAULT '0',
    "pagodia" DECIMAL(12,0) DEFAULT 0,
    "rcaja" DECIMAL(12,2) DEFAULT 0.00,
    "Rfechapag" DATE,
    "permiso" DECIMAL(12,0) DEFAULT 0,
    "Fechavence" DATE,
    "direccion" VARCHAR(100) DEFAULT ' ',
    "prima" VARCHAR(1) DEFAULT '',
    "categoria" VARCHAR(2) DEFAULT '',
    "sexo" VARCHAR(1) DEFAULT '',
    "rtn" VARCHAR(20)
);

-- Table: norecibos (Control de correlativos)
CREATE TABLE IF NOT EXISTS "norecibos" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(6),
    "numero" DECIMAL(12,0),
    "solvencia" DECIMAL(12,0) DEFAULT 0
);

-- =====================================================
-- 4. CATASTRO MODULE - Core Tables
-- =====================================================

-- Table: bdcata1 (Maestro de Catastro)
CREATE TABLE IF NOT EXISTS "bdcata1" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4),
    "cocata1" VARCHAR(20) NOT NULL,
    "ficha" DECIMAL(1,0) DEFAULT 1,
    "claveant" VARCHAR(15),
    "mapa" VARCHAR(7),
    "bloque" VARCHAR(3),
    "predio" VARCHAR(4) DEFAULT ' ',
    "depto" VARCHAR(3),
    "municipio" VARCHAR(2),
    "barrio" VARCHAR(8),
    "caserio" VARCHAR(3),
    "sitio" VARCHAR(3),
    "nombres" VARCHAR(100),
    "apellidos" VARCHAR(100),
    "identidad" VARCHAR(20),
    "rtn" VARCHAR(20),
    "ubicacion" VARCHAR(80),
    "nacionalidad" VARCHAR(3),
    "uso" VARCHAR(3) DEFAULT '0',
    "subuso" VARCHAR(3),
    "constru" DECIMAL(10,0) DEFAULT 0,
    "nofichas" DECIMAL(5,0) DEFAULT 0,
    "bvl2tie" DECIMAL(12,2) DEFAULT 0.00,
    "conedi" DECIMAL(5,0) DEFAULT 0,
    "mejoras" DECIMAL(12,2) DEFAULT 0.00,
    "cedif" DECIMAL(5,0) DEFAULT 0,
    "detalle" DECIMAL(12,2) DEFAULT 0.00,
    "impuesto" DECIMAL(12,2) DEFAULT 0.00,
    "grabable" DECIMAL(12,2) DEFAULT 0.00,
    "cultivo" DECIMAL(14,4) DEFAULT 0.0000,
    "declarado" DECIMAL(12,2) DEFAULT 0.00,
    "condetalle" DECIMAL(5,0) DEFAULT 0,
    "exencion" DECIMAL(12,2) DEFAULT 0.00,
    "usuario" VARCHAR(50),
    "fechasys" TIMESTAMP WITH TIME ZONE,
    "st" VARCHAR(3),
    "codhab" VARCHAR(3),
    "codprop" VARCHAR(3),
    "tasaimpositiva" DECIMAL(7,2) DEFAULT 0.00,
    "declaimpto" DECIMAL(1,0) DEFAULT 0,
    "sexo" VARCHAR(1),
    "telefono" VARCHAR(40) DEFAULT '0',
    "tipopropiedad" DECIMAL(12,2) DEFAULT 1.00,
    "estado" VARCHAR(1) DEFAULT 'A',
    "clavesure" VARCHAR(18),
    "cx" DECIMAL(12,2) DEFAULT 0.00,
    "cy" DECIMAL(12,2) DEFAULT 0.00,
    "zonificacion" VARCHAR(5),
    "bexenc" DECIMAL(7,2) DEFAULT 0.00,
    "vivienda" DECIMAL(3,0) DEFAULT 0,
    "apartamentos" DECIMAL(1,0) DEFAULT 0,
    "cuartos" DECIMAL(12,0) DEFAULT 0,
    "lote" VARCHAR(10) DEFAULT '',
    "bloquecol" VARCHAR(20) DEFAULT '',
    "terceraedad" VARCHAR(1) DEFAULT '',
    "foto" VARCHAR(200) DEFAULT '',
    "croquis" VARCHAR(200) DEFAULT '',
    UNIQUE ("empresa", "cocata1")
);

-- Table: bdterreno (Avalúos)
CREATE TABLE IF NOT EXISTS "bdterreno" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4),
    "cocata1" VARCHAR(20) UNIQUE NOT NULL,
    "bvlbas1" DECIMAL(12,2) DEFAULT 0.00,
    "baream21" DECIMAL(12,2) DEFAULT 0.00,
    "tipica1" DECIMAL(12,2) DEFAULT 0.00,
    "bfacmodi" DECIMAL(7,3) DEFAULT 0.000,
    "bfrente" DECIMAL(12,2) DEFAULT 0.00,
    "besqui" DECIMAL(1,0) DEFAULT 0,
    "esquina" DECIMAL(5,2) DEFAULT 0.00,
    "bvlbas2" DECIMAL(12,2) DEFAULT 0.00,
    "baream22" DECIMAL(12,2) DEFAULT 0.00,
    "tipica2" DECIMAL(12,2) DEFAULT 0.00,
    "bfacmod2" DECIMAL(7,3) DEFAULT 0.000,
    "bfrente2" DECIMAL(12,2) DEFAULT 0.00,
    "btopogra" VARCHAR(3) DEFAULT '0',
    "bfactopo" DECIMAL(7,2) DEFAULT 0.00,
    "fac1" DECIMAL(6,3) DEFAULT 0.000, "codfac1" VARCHAR(3), "facarea1" DECIMAL(12,2), "monto1" DECIMAL(12,2),
    "fac2" DECIMAL(6,3) DEFAULT 0.000, "codfac2" VARCHAR(3), "facarea2" DECIMAL(12,2), "monto2" DECIMAL(12,2),
    "fac3" DECIMAL(6,3) DEFAULT 0.000, "codfac3" VARCHAR(3), "facarea3" DECIMAL(12,2), "monto3" DECIMAL(12,2),
    "fac4" DECIMAL(6,3) DEFAULT 0.000, "codfac4" VARCHAR(3), "facarea4" DECIMAL(12,2), "monto4" DECIMAL(12,2),
    "fac5" DECIMAL(6,3) DEFAULT 0.000, "codfac5" VARCHAR(3), "facarea5" DECIMAL(12,2), "monto5" DECIMAL(12,2),
    "fac6" DECIMAL(6,3) DEFAULT 0.000, "codfac6" VARCHAR(3), "facarea6" DECIMAL(12,2), "monto6" DECIMAL(12,2),
    "fac7" DECIMAL(12,2) DEFAULT 0.00, "codfac7" VARCHAR(3), "facarea7" DECIMAL(12,2), "monto7" DECIMAL(12,2),
    "fac8" DECIMAL(6,3) DEFAULT 0.000, "codfac8" VARCHAR(3), "facarea8" DECIMAL(12,2), "monto8" DECIMAL(12,2),
    "fac9" DECIMAL(6,3) DEFAULT 0.000, "codfac9" VARCHAR(3), "facarea9" DECIMAL(12,2), "monto9" DECIMAL(12,2),
    "fac10" DECIMAL(6,3) DEFAULT 0.000, "codfac10" VARCHAR(3), "facarea10" DECIMAL(12,2), "monto10" DECIMAL(12,2),
    "fcarea" DECIMAL(6,3) DEFAULT 0.000,
    "fcubic" DECIMAL(6,3) DEFAULT 0.000,
    "fcservi" DECIMAL(6,3) DEFAULT 0.000,
    "fcacceso" DECIMAL(6,3) DEFAULT 0.000,
    "fcagua" DECIMAL(6,3) DEFAULT 0.000,
    "fcarea2" DECIMAL(6,3) DEFAULT 0.000,
    "fcservi2" DECIMAL(6,3) DEFAULT 0.000,
    "fctopo" DECIMAL(6,3) DEFAULT 0.000,
    "fcconfi" DECIMAL(6,3) DEFAULT 0.000,
    "usuario" VARCHAR(50) DEFAULT '',
    "fechasys" TIMESTAMP WITH TIME ZONE
);

-- Table: edificacion
CREATE TABLE IF NOT EXISTS "edificacion" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4) DEFAULT '',
    "clave" VARCHAR(14) NOT NULL DEFAULT '0',
    "edifino" DECIMAL(3,0) DEFAULT 0,
    "piso" DECIMAL(2,0),
    "area" DECIMAL(12,2) DEFAULT 0.00,
    "uso" VARCHAR(1),
    "clase" VARCHAR(2),
    "calidad" VARCHAR(2),
    "costo" DECIMAL(12,2) DEFAULT 0.00,
    "bueno" DECIMAL(3,0) DEFAULT 0,
    "totedi" DECIMAL(14,2) DEFAULT 0.00,
    "descripcion" VARCHAR(100) DEFAULT '',
    "usuario" VARCHAR(50) DEFAULT '',
    "fechasys" TIMESTAMP WITH TIME ZONE
);

-- =====================================================
-- 5. INDEXES for Performance
-- =====================================================
CREATE INDEX IF NOT EXISTS "idx_negocios_identidad" ON "negocios" ("identidad");
CREATE INDEX IF NOT EXISTS "idx_negocios_rtm_expe" ON "negocios" ("rtm", "expe");
CREATE INDEX IF NOT EXISTS "idx_bdcata1_cocata1" ON "bdcata1" ("cocata1");
CREATE INDEX IF NOT EXISTS "idx_pagovariostemp_recibo" ON "pagovariostemp" ("recibo");
CREATE INDEX IF NOT EXISTS "idx_pagovariostemp_fecha" ON "pagovariostemp" ("fecha");

-- =====================================================
-- 6. CATASTRO & SUPPORTING CATALOGS
-- =====================================================

-- Table: barrios (Aldeas y Colonias)
CREATE TABLE IF NOT EXISTS "barrios" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4) DEFAULT '',
    "depto" VARCHAR(2) DEFAULT '',
    "codmuni" VARCHAR(2) DEFAULT '',
    "codbarrio" VARCHAR(8) DEFAULT '',
    "descripcion" VARCHAR(29),
    "tipica" DECIMAL(12,2) DEFAULT 0.00,
    UNIQUE ("empresa", "depto", "codmuni", "codbarrio")
);

-- Table: caserio
CREATE TABLE IF NOT EXISTS "caserio" (
    "id" SERIAL PRIMARY KEY,
    "depto" VARCHAR(3),
    "codmuni" VARCHAR(3),
    "codbarrio" VARCHAR(3) DEFAULT '',
    "codigo" VARCHAR(3) DEFAULT '',
    "descripcion" VARCHAR(50),
    UNIQUE ("depto", "codmuni", "codbarrio", "codigo")
);

-- Table: factoresriego
CREATE TABLE IF NOT EXISTS "factoresriego" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4),
    "codigo" VARCHAR(3) NOT NULL DEFAULT '0',
    "descripcion" VARCHAR(45) NOT NULL DEFAULT '0',
    "valor" DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    UNIQUE ("empresa", "codigo")
);

-- Table: areasrurales
CREATE TABLE IF NOT EXISTS "areasrurales" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4),
    "cocata1" VARCHAR(20) NOT NULL,
    "fac" DECIMAL(6,3) DEFAULT 0.000,
    "codfac" VARCHAR(3),
    "facarea" DECIMAL(12,2) DEFAULT 0.00,
    "monto" DECIMAL(12,2) DEFAULT 0.00,
    "usuario" VARCHAR(50),
    "fechasys" TIMESTAMP WITH TIME ZONE
);

-- Table: colindantes
CREATE TABLE IF NOT EXISTS "colindantes" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4),
    "cocata1" VARCHAR(20) NOT NULL,
    "tipo" VARCHAR(1) NOT NULL,
    "colindante" VARCHAR(200),
    "codcolinda" VARCHAR(2),
    "usuario" VARCHAR(50),
    "fechasys" TIMESTAMP WITH TIME ZONE
);

-- Table: copropietarios
CREATE TABLE IF NOT EXISTS "copropietarios" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4),
    "cocata1" VARCHAR(20) DEFAULT '',
    "identidad" VARCHAR(18) DEFAULT '',
    "nombre" VARCHAR(100) DEFAULT '',
    "porcentaje" DECIMAL(7,2) DEFAULT NULL,
    UNIQUE ("empresa", "cocata1", "identidad")
);

-- Table: costos (Avalúo de edificios)
CREATE TABLE IF NOT EXISTS "costos" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4) DEFAULT '',
    "uso" VARCHAR(2) NOT NULL DEFAULT '',
    "clase" VARCHAR(1) NOT NULL DEFAULT '',
    "calidad" VARCHAR(3) NOT NULL DEFAULT '',
    "costo" DECIMAL(13,2) NOT NULL DEFAULT 0.00,
    "rango1" DECIMAL(11,0) DEFAULT 0,
    "rango2" DECIMAL(11,0) DEFAULT 0,
    UNIQUE ("empresa", "uso", "clase", "calidad")
);

-- Table: tipodetalle
CREATE TABLE IF NOT EXISTS "tipodetalle" (
    "id" SERIAL PRIMARY KEY,
    "empresa" VARCHAR(4),
    "codigo" VARCHAR(4) DEFAULT '0',
    "descripcion" VARCHAR(30) DEFAULT '0',
    "costo" DECIMAL(12,3) NOT NULL DEFAULT 0.000,
    UNIQUE ("empresa", "codigo")
);

-- Table: usos
CREATE TABLE IF NOT EXISTS "usos" (
    "id" SERIAL PRIMARY KEY,
    "uso" VARCHAR(3) UNIQUE NOT NULL,
    "desuso" VARCHAR(34) NOT NULL
);

-- Table: subuso
CREATE TABLE IF NOT EXISTS "subuso" (
    "id" SERIAL PRIMARY KEY,
    "uso" VARCHAR(3) NOT NULL,
    "codsubuso" VARCHAR(5) DEFAULT ' ',
    "des_subuso" VARCHAR(34) NOT NULL
);

-- Table: nacionalidad
CREATE TABLE IF NOT EXISTS "nacionalidad" (
    "id" SERIAL PRIMARY KEY,
    "codigo" VARCHAR(3) UNIQUE NOT NULL,
    "descripcion" VARCHAR(45) NOT NULL
);

-- Table: tiposexo
CREATE TABLE IF NOT EXISTS "tiposexo" (
    "id" SERIAL PRIMARY KEY,
    "codigo" VARCHAR(1) UNIQUE NOT NULL,
    "descripcion" VARCHAR(30)
);

-- =====================================================
-- 7. AUDIT TABLES
-- =====================================================

-- Table: bitacoracatastro
CREATE TABLE IF NOT EXISTS "bitacoracatastro" (
    "id" BIGSERIAL PRIMARY KEY,
    "clave" VARCHAR(20) NOT NULL,
    "fecha" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "usuario_id" INTEGER,
    "propietarioantes" VARCHAR(200),
    "propietarioactual" VARCHAR(200),
    "concepto" TEXT,
    "valorantes" DECIMAL(20,4),
    "valoractual" DECIMAL(20,4)
);

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

-- =====================================================
-- 8. PRESUPUESTOS MODULE
-- =====================================================

CREATE TABLE IF NOT EXISTS "mod_presupuestos_partida" (
    "id" SERIAL PRIMARY KEY,
    "codigo" VARCHAR(20) NOT NULL,
    "nombre" VARCHAR(200) NOT NULL,
    "presupuesto_inicial" DECIMAL(18,2) DEFAULT 0.00,
    "modificaciones" DECIMAL(18,2) DEFAULT 0.00,
    "presupuesto_vigente" DECIMAL(18,2) DEFAULT 0.00,
    "ejecutado" DECIMAL(18,2) DEFAULT 0.00,
    "disponible" DECIMAL(18,2) DEFAULT 0.00
);

-- =====================================================
-- 9. TESORERIA MODULE
-- =====================================================

CREATE TABLE IF NOT EXISTS "mod_tesoreria_caja" (
    "id" SERIAL PRIMARY KEY,
    "cod_caja" VARCHAR(10) NOT NULL,
    "nombre" VARCHAR(100) NOT NULL,
    "responsable" VARCHAR(100),
    "estado" VARCHAR(1) DEFAULT 'A'
);
- -   M I G R A T I O N   0 0 0 1  
 B E G I N ;  
 - -  
 - -   C r e a t e   m o d e l   A c t i v o F i j o  
 - -  
 C R E A T E   T A B L E   " c o n t _ a c t i v o _ f i j o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " f e c h a _ a d q u i s i c i o n "   d a t e   N O T   N U L L ,   " c o s t o _ a d q u i s i c i o n "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v a l o r _ r e s i d u a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v i d a _ u t i l _ m e s e s "   i n t e g e r   N O T   N U L L ,   " m e t o d o _ d e p r e c i a c i o n "   v a r c h a r ( 3 0 )   N O T   N U L L ,   " d e p r e c i a c i o n _ a c u m u l a d a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v a l o r _ e n _ l i b r o s "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " u b i c a c i o n "   v a r c h a r ( 2 0 0 )   N U L L ,   " r e s p o n s a b l e "   v a r c h a r ( 2 0 0 )   N U L L ,   " n u m e r o _ s e r i e "   v a r c h a r ( 1 0 0 )   N U L L ,   " e s t a d o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   A c t i v o I n t a n g i b l e  
 - -  
 C R E A T E   T A B L E   " c o n t _ a c t i v o _ i n t a n g i b l e "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " t i p o _ v i d a "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " c o s t o _ a d q u i s i c i o n "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " a m o r t i z a c i o n _ a c u m u l a d a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v i d a _ u t i l _ m e s e s "   i n t e g e r   N U L L ,   " f e c h a _ a d q u i s i c i o n "   d a t e   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   A s i e n t o C o n t a b l e  
 - -  
 C R E A T E   T A B L E   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " n u m e r o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " f e c h a "   d a t e   N O T   N U L L ,   " c o n c e p t o "   t e x t   N O T   N U L L ,   " r e f e r e n c i a "   v a r c h a r ( 1 0 0 )   N U L L ,   " d o c u m e n t o "   v a r c h a r ( 5 0 )   N U L L ,   " t a s a _ c a m b i o "   n u m e r i c ( 1 8 ,   6 )   N O T   N U L L ,   " t o t a l _ d e b e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " t o t a l _ h a b e r "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " e s t a d o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " a p r o b a d o _ p o r "   v a r c h a r ( 1 0 0 )   N U L L ,   " f e c h a _ a p r o b a c i o n "   t i m e s t a m p   w i t h   t i m e   z o n e   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   C e n t r o C o s t o  
 - -  
 C R E A T E   T A B L E   " c o n t _ c e n t r o _ c o s t o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " n o m b r e "   v a r c h a r ( 2 0 0 )   N O T   N U L L ,   " r e s p o n s a b l e "   v a r c h a r ( 2 0 0 )   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c e n t r o _ p a d r e _ i d "   b i g i n t   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   C u e n t a C o n t a b l e  
 - -  
 C R E A T E   T A B L E   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " n o m b r e "   v a r c h a r ( 2 0 0 )   N O T   N U L L ,   " n i v e l "   i n t e g e r   N O T   N U L L ,   " t i p o "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " n a t u r a l e z a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   t e x t   N U L L ,   " a c e p t a _ m o v i m i e n t o "   b o o l e a n   N O T   N U L L ,   " r e q u i e r e _ c e n t r o _ c o s t o "   b o o l e a n   N O T   N U L L ,   " r e q u i e r e _ t e r c e r o "   b o o l e a n   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ p a d r e _ i d "   b i g i n t   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   E j e r c i c i o F i s c a l  
 - -  
 C R E A T E   T A B L E   " c o n t _ e j e r c i c i o _ f i s c a l "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " a n i o "   i n t e g e r   N O T   N U L L   U N I Q U E ,   " d e s c r i p c i o n "   v a r c h a r ( 1 0 0 )   N O T   N U L L ,   " f e c h a _ i n i c i o "   d a t e   N O T   N U L L ,   " f e c h a _ f i n "   d a t e   N O T   N U L L ,   " e s t a d o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   G r u p o C u e n t a  
 - -  
 C R E A T E   T A B L E   " c o n t _ g r u p o _ c u e n t a "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 1 )   N O T   N U L L   U N I Q U E ,   " n o m b r e "   v a r c h a r ( 1 0 0 )   N O T   N U L L ,   " n a t u r a l e z a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   t e x t   N U L L ,   " o r d e n "   i n t e g e r   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   M o n e d a  
 - -  
 C R E A T E   T A B L E   " c o n t _ m o n e d a "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 3 )   N O T   N U L L   U N I Q U E ,   " n o m b r e "   v a r c h a r ( 1 0 0 )   N O T   N U L L ,   " s i m b o l o "   v a r c h a r ( 5 )   N O T   N U L L ,   " e s _ l o c a l "   b o o l e a n   N O T   N U L L ,   " d e c i m a l e s "   i n t e g e r   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   P o l i t i c a C o n t a b l e  
 - -  
 C R E A T E   T A B L E   " c o n t _ p o l i t i c a _ c o n t a b l e "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " t i t u l o "   v a r c h a r ( 2 0 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   t e x t   N O T   N U L L ,   " t i p o _ c a m b i o "   v a r c h a r ( 2 0 )   N U L L ,   " f e c h a _ v i g e n c i a "   d a t e   N O T   N U L L ,   " n i c _ r e l a c i o n a d a "   v a r c h a r ( 5 0 )   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   T i p o A s i e n t o  
 - -  
 C R E A T E   T A B L E   " c o n t _ t i p o _ a s i e n t o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 1 0 )   N O T   N U L L   U N I Q U E ,   " n o m b r e "   v a r c h a r ( 1 0 0 )   N O T   N U L L ,   " p r e f i j o "   v a r c h a r ( 5 )   N O T   N U L L ,   " d e s c r i p c i o n "   t e x t   N U L L ,   " e s _ a u t o m a t i c o "   b o o l e a n   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   P r o v i s i o n  
 - -  
 C R E A T E   T A B L E   " c o n t _ p r o v i s i o n "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " t i p o "   v a r c h a r ( 3 0 )   N O T   N U L L ,   " m o n t o _ e s t i m a d o "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " p r o b a b i l i d a d "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " f e c h a _ o r i g e n "   d a t e   N O T   N U L L ,   " f e c h a _ v e n c i m i e n t o "   d a t e   N U L L ,   " n o t a s "   t e x t   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   P e r i o d o C o n t a b l e  
 - -  
 C R E A T E   T A B L E   " c o n t _ p e r i o d o _ c o n t a b l e "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " n u m e r o "   i n t e g e r   N O T   N U L L ,   " n o m b r e "   v a r c h a r ( 5 0 )   N O T   N U L L ,   " f e c h a _ i n i c i o "   d a t e   N O T   N U L L ,   " f e c h a _ f i n "   d a t e   N O T   N U L L ,   " e s t a d o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " e j e r c i c i o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   I n s t r u m e n t o F i n a n c i e r o  
 - -  
 C R E A T E   T A B L E   " c o n t _ i n s t r u m e n t o _ f i n a n c i e r o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " t i p o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " c l a s i f i c a c i o n "   v a r c h a r ( 3 0 )   N O T   N U L L ,   " v a l o r _ n o m i n a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v a l o r _ r a z o n a b l e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " t a s a _ i n t e r e s "   n u m e r i c ( 8 ,   4 )   N O T   N U L L ,   " f e c h a _ e m i s i o n "   d a t e   N O T   N U L L ,   " f e c h a _ v e n c i m i e n t o "   d a t e   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   I m p u e s t o D i f e r i d o  
 - -  
 C R E A T E   T A B L E   " c o n t _ i m p u e s t o _ d i f e r i d o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " t i p o "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " b a s e _ c o n t a b l e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " b a s e _ f i s c a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " d i f e r e n c i a _ t e m p o r a r i a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " t a s a _ i m p u e s t o "   n u m e r i c ( 5 ,   2 )   N O T   N U L L ,   " i m p u e s t o _ d i f e r i d o "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ i d "   b i g i n t   N O T   N U L L ,   " p e r i o d o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   H e c h o P o s t e r i o r  
 - -  
 C R E A T E   T A B L E   " c o n t _ h e c h o _ p o s t e r i o r "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " t i p o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   t e x t   N O T   N U L L ,   " f e c h a _ h e c h o "   d a t e   N O T   N U L L ,   " i m p a c t o _ f i n a n c i e r o "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " a s i e n t o _ a j u s t e _ i d "   b i g i n t   N U L L ,   " e j e r c i c i o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   F l u j o E f e c t i v o  
 - -  
 C R E A T E   T A B L E   " c o n t _ f l u j o _ e f e c t i v o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c a t e g o r i a "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " c o n c e p t o "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " e n t r a d a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " s a l i d a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " n e t o "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ i d "   b i g i n t   N U L L ,   " p e r i o d o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   D e t e r i o r o A c t i v o  
 - -  
 C R E A T E   T A B L E   " c o n t _ d e t e r i o r o _ a c t i v o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " t i p o _ a c t i v o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " v a l o r _ e n _ l i b r o s "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " i m p o r t e _ r e c u p e r a b l e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " p e r d i d a _ d e t e r i o r o "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " f e c h a _ e v a l u a c i o n "   d a t e   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " a c t i v o _ f i j o _ i d "   b i g i n t   N U L L ,   " a c t i v o _ i n t a n g i b l e _ i d "   b i g i n t   N U L L ,   " a s i e n t o _ i d "   b i g i n t   N U L L ,   " c u e n t a _ p e r d i d a _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   A d d   f i e l d   g r u p o   t o   c u e n t a c o n t a b l e  
 - -  
 A L T E R   T A B L E   " c o n t _ c u e n t a _ c o n t a b l e "   A D D   C O L U M N   " g r u p o _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ c u e n t a _ c o n t a b l e _ g r u p o _ i d _ a 0 d 6 0 4 0 4 _ f k _ c o n t _ g r u p o _ c u e n t a _ i d "   R E F E R E N C E S   " c o n t _ g r u p o _ c u e n t a " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ c u e n t a _ c o n t a b l e _ g r u p o _ i d _ a 0 d 6 0 4 0 4 _ f k _ c o n t _ g r u p o _ c u e n t a _ i d "   I M M E D I A T E ;  
 - -  
 - -   C r e a t e   m o d e l   C o s t o P r e s t a m o  
 - -  
 C R E A T E   T A B L E   " c o n t _ c o s t o _ p r e s t a m o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " m o n t o _ p r i n c i p a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " t a s a _ i n t e r e s _ a n u a l "   n u m e r i c ( 8 ,   4 )   N O T   N U L L ,   " f e c h a _ d e s e m b o l s o "   d a t e   N O T   N U L L ,   " f e c h a _ v e n c i m i e n t o "   d a t e   N O T   N U L L ,   " i n t e r e s _ a c u m u l a d o "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " c a p i t a l i z a b l e "   b o o l e a n   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " a c t i v o _ c a l i f i c a d o _ i d "   b i g i n t   N U L L ,   " c u e n t a _ i n t e r e s _ i d "   b i g i n t   N O T   N U L L ,   " c u e n t a _ p r e s t a m o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   B e n e f i c i o E m p l e a d o  
 - -  
 C R E A T E   T A B L E   " c o n t _ b e n e f i c i o _ e m p l e a d o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " t i p o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " m o n t o _ m e n s u a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " p r o v i s i o n _ a c u m u l a d a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " n u m e r o _ e m p l e a d o s "   i n t e g e r   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ g a s t o _ i d "   b i g i n t   N O T   N U L L ,   " c u e n t a _ p r o v i s i o n _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   A d d   f i e l d   m o n e d a   t o   a s i e n t o c o n t a b l e  
 - -  
 A L T E R   T A B L E   " c o n t _ a s i e n t o _ c o n t a b l e "   A D D   C O L U M N   " m o n e d a _ i d "   b i g i n t   N U L L   C O N S T R A I N T   " c o n t _ a s i e n t o _ c o n t a b l e _ m o n e d a _ i d _ 2 0 5 e 4 b 0 3 _ f k _ c o n t _ m o n e d a _ i d "   R E F E R E N C E S   " c o n t _ m o n e d a " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a s i e n t o _ c o n t a b l e _ m o n e d a _ i d _ 2 0 5 e 4 b 0 3 _ f k _ c o n t _ m o n e d a _ i d "   I M M E D I A T E ;  
 - -  
 - -   A d d   f i e l d   p e r i o d o   t o   a s i e n t o c o n t a b l e  
 - -  
 A L T E R   T A B L E   " c o n t _ a s i e n t o _ c o n t a b l e "   A D D   C O L U M N   " p e r i o d o _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ a s i e n t o _ c o n t a b l _ p e r i o d o _ i d _ e e 8 e 6 2 7 1 _ f k _ c o n t _ p e r i "   R E F E R E N C E S   " c o n t _ p e r i o d o _ c o n t a b l e " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a s i e n t o _ c o n t a b l _ p e r i o d o _ i d _ e e 8 e 6 2 7 1 _ f k _ c o n t _ p e r i "   I M M E D I A T E ;  
 - -  
 - -   A d d   f i e l d   t i p o   t o   a s i e n t o c o n t a b l e  
 - -  
 A L T E R   T A B L E   " c o n t _ a s i e n t o _ c o n t a b l e "   A D D   C O L U M N   " t i p o _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ a s i e n t o _ c o n t a b l e _ t i p o _ i d _ 3 e f 4 e b f a _ f k _ c o n t _ t i p o _ a s i e n t o _ i d "   R E F E R E N C E S   " c o n t _ t i p o _ a s i e n t o " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a s i e n t o _ c o n t a b l e _ t i p o _ i d _ 3 e f 4 e b f a _ f k _ c o n t _ t i p o _ a s i e n t o _ i d "   I M M E D I A T E ;  
 - -  
 - -   A d d   f i e l d   c u e n t a   t o   a c t i v o i n t a n g i b l e  
 - -  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ i n t a n g i b l e "   A D D   C O L U M N   " c u e n t a _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ a c t i v o _ i n t a n g i b _ c u e n t a _ i d _ a 7 5 7 a 0 4 c _ f k _ c o n t _ c u e n "   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a c t i v o _ i n t a n g i b _ c u e n t a _ i d _ a 7 5 7 a 0 4 c _ f k _ c o n t _ c u e n "   I M M E D I A T E ;  
 - -  
 - -   A d d   f i e l d   c u e n t a _ a m o r t i z a c i o n   t o   a c t i v o i n t a n g i b l e  
 - -  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ i n t a n g i b l e "   A D D   C O L U M N   " c u e n t a _ a m o r t i z a c i o n _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ a c t i v o _ i n t a n g i b _ c u e n t a _ a m o r t i z a c i o n _ _ 0 7 c b d 7 4 3 _ f k _ c o n t _ c u e n "   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a c t i v o _ i n t a n g i b _ c u e n t a _ a m o r t i z a c i o n _ _ 0 7 c b d 7 4 3 _ f k _ c o n t _ c u e n "   I M M E D I A T E ;  
 - -  
 - -   A d d   f i e l d   c u e n t a _ a c t i v o   t o   a c t i v o f i j o  
 - -  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ f i j o "   A D D   C O L U M N   " c u e n t a _ a c t i v o _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ a c t i v o _ i d _ 5 9 6 4 0 2 e 8 _ f k _ c o n t _ c u e n "   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ a c t i v o _ i d _ 5 9 6 4 0 2 e 8 _ f k _ c o n t _ c u e n "   I M M E D I A T E ;  
 - -  
 - -   A d d   f i e l d   c u e n t a _ d e p r e c i a c i o n   t o   a c t i v o f i j o  
 - -  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ f i j o "   A D D   C O L U M N   " c u e n t a _ d e p r e c i a c i o n _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ d e p r e c i a c i o n _ _ d 5 0 2 1 6 9 8 _ f k _ c o n t _ c u e n "   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ d e p r e c i a c i o n _ _ d 5 0 2 1 6 9 8 _ f k _ c o n t _ c u e n "   I M M E D I A T E ;  
 - -  
 - -   A d d   f i e l d   c u e n t a _ g a s t o _ d e p r e c i a c i o n   t o   a c t i v o f i j o  
 - -  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ f i j o "   A D D   C O L U M N   " c u e n t a _ g a s t o _ d e p r e c i a c i o n _ i d "   b i g i n t   N O T   N U L L   C O N S T R A I N T   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ g a s t o _ d e p r e c i _ 4 8 d a 5 0 4 9 _ f k _ c o n t _ c u e n "   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ g a s t o _ d e p r e c i _ 4 8 d a 5 0 4 9 _ f k _ c o n t _ c u e n "   I M M E D I A T E ;  
 - -  
 - -   C r e a t e   m o d e l   T i p o C a m b i o  
 - -  
 C R E A T E   T A B L E   " c o n t _ t i p o _ c a m b i o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " f e c h a "   d a t e   N O T   N U L L ,   " t a s a _ c o m p r a "   n u m e r i c ( 1 8 ,   6 )   N O T   N U L L ,   " t a s a _ v e n t a "   n u m e r i c ( 1 8 ,   6 )   N O T   N U L L ,   " t a s a _ p r o m e d i o "   n u m e r i c ( 1 8 ,   6 )   N O T   N U L L ,   " m o n e d a _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   P r o p i e d a d I n v e r s i o n  
 - -  
 C R E A T E   T A B L E   " c o n t _ p r o p i e d a d _ i n v e r s i o n "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " d i r e c c i o n "   t e x t   N U L L ,   " c o s t o _ a d q u i s i c i o n "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v a l o r _ r a z o n a b l e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " m o d e l o _ m e d i c i o n "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " i n g r e s o _ r e n t a _ m e n s u a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " f e c h a _ a d q u i s i c i o n "   d a t e   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   L i b r o M a y o r  
 - -  
 C R E A T E   T A B L E   " c o n t _ l i b r o _ m a y o r "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " s a l d o _ a n t e r i o r "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " d e b i t o s "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " c r e d i t o s "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " s a l d o _ f i n a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ i d "   b i g i n t   N O T   N U L L ,   " p e r i o d o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   I n v e n t a r i o  
 - -  
 C R E A T E   T A B L E   " c o n t _ i n v e n t a r i o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " u n i d a d _ m e d i d a "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " c a n t i d a d "   n u m e r i c ( 1 8 ,   4 )   N O T   N U L L ,   " c o s t o _ u n i t a r i o "   n u m e r i c ( 1 8 ,   4 )   N O T   N U L L ,   " c o s t o _ t o t a l "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v a l o r _ n e t o _ r e a l i z a b l e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " m e t o d o _ v a l o r a c i o n "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " s t o c k _ m i n i m o "   n u m e r i c ( 1 8 ,   4 )   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ c o s t o _ v e n t a _ i d "   b i g i n t   N O T   N U L L ,   " c u e n t a _ i n v e n t a r i o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   D e t a l l e A s i e n t o  
 - -  
 C R E A T E   T A B L E   " c o n t _ d e t a l l e _ a s i e n t o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " l i n e a "   i n t e g e r   N O T   N U L L ,   " c o n c e p t o "   v a r c h a r ( 5 0 0 )   N U L L ,   " d e b e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " h a b e r "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " t e r c e r o "   v a r c h a r ( 2 0 0 )   N U L L ,   " r e f e r e n c i a "   v a r c h a r ( 1 0 0 )   N U L L ,   " a s i e n t o _ i d "   b i g i n t   N O T   N U L L ,   " c e n t r o _ c o s t o _ i d "   b i g i n t   N U L L ,   " c u e n t a _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   C r e a t e   m o d e l   D e p r e c i a c i o n  
 - -  
 C R E A T E   T A B L E   " c o n t _ d e p r e c i a c i o n "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " m o n t o "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " d e p r e c i a c i o n _ a c u m u l a d a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " v a l o r _ e n _ l i b r o s "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " a c t i v o _ i d "   b i g i n t   N O T   N U L L ,   " a s i e n t o _ i d "   b i g i n t   N U L L ,   " p e r i o d o _ i d "   b i g i n t   N O T   N U L L ) ;  
 - -  
 - -   A l t e r   u n i q u e _ t o g e t h e r   f o r   c u e n t a c o n t a b l e   ( 1   c o n s t r a i n t ( s ) )  
 - -  
 A L T E R   T A B L E   " c o n t _ c u e n t a _ c o n t a b l e "   A D D   C O N S T R A I N T   " c o n t _ c u e n t a _ c o n t a b l e _ c o d i g o _ e m p r e s a _ b 4 2 9 d 5 a c _ u n i q "   U N I Q U E   ( " c o d i g o " ,   " e m p r e s a " ) ;  
 - -  
 - -   A l t e r   u n i q u e _ t o g e t h e r   f o r   a s i e n t o c o n t a b l e   ( 1   c o n s t r a i n t ( s ) )  
 - -  
 A L T E R   T A B L E   " c o n t _ a s i e n t o _ c o n t a b l e "   A D D   C O N S T R A I N T   " c o n t _ a s i e n t o _ c o n t a b l e _ n u m e r o _ e m p r e s a _ 3 c c d 4 1 9 d _ u n i q "   U N I Q U E   ( " n u m e r o " ,   " e m p r e s a " ) ;  
 - -  
 - -   A l t e r   u n i q u e _ t o g e t h e r   f o r   a c t i v o i n t a n g i b l e   ( 1   c o n s t r a i n t ( s ) )  
 - -  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ i n t a n g i b l e "   A D D   C O N S T R A I N T   " c o n t _ a c t i v o _ i n t a n g i b l e _ c o d i g o _ e m p r e s a _ 6 0 4 d b c 1 5 _ u n i q "   U N I Q U E   ( " c o d i g o " ,   " e m p r e s a " ) ;  
 - -  
 - -   A l t e r   u n i q u e _ t o g e t h e r   f o r   a c t i v o f i j o   ( 1   c o n s t r a i n t ( s ) )  
 - -  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ f i j o "   A D D   C O N S T R A I N T   " c o n t _ a c t i v o _ f i j o _ c o d i g o _ e m p r e s a _ 8 0 4 f 2 f e 7 _ u n i q "   U N I Q U E   ( " c o d i g o " ,   " e m p r e s a " ) ;  
 - -  
 - -   C r e a t e   m o d e l   A c t i v o B i o l o g i c o  
 - -  
 C R E A T E   T A B L E   " c o n t _ a c t i v o _ b i o l o g i c o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " c o d i g o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " d e s c r i p c i o n "   v a r c h a r ( 5 0 0 )   N O T   N U L L ,   " t i p o "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " c a n t i d a d "   n u m e r i c ( 1 8 ,   4 )   N O T   N U L L ,   " u n i d a d _ m e d i d a "   v a r c h a r ( 2 0 )   N O T   N U L L ,   " v a l o r _ r a z o n a b l e "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " c o s t o s _ v e n t a "   n u m e r i c ( 1 8 ,   2 )   N O T   N U L L ,   " f e c h a _ m e d i c i o n "   d a t e   N O T   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " c u e n t a _ i d "   b i g i n t   N O T   N U L L ) ;  
 A L T E R   T A B L E   " c o n t _ c e n t r o _ c o s t o "   A D D   C O N S T R A I N T   " c o n t _ c e n t r o _ c o s t o _ c o d i g o _ e m p r e s a _ 8 2 f 9 a 5 9 2 _ u n i q "   U N I Q U E   ( " c o d i g o " ,   " e m p r e s a " ) ;  
 A L T E R   T A B L E   " c o n t _ c e n t r o _ c o s t o "   A D D   C O N S T R A I N T   " c o n t _ c e n t r o _ c o s t o _ c e n t r o _ p a d r e _ i d _ 4 d e f a 3 0 4 _ f k _ c o n t _ c e n t "   F O R E I G N   K E Y   ( " c e n t r o _ p a d r e _ i d " )   R E F E R E N C E S   " c o n t _ c e n t r o _ c o s t o "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ c e n t r o _ c o s t o _ c e n t r o _ p a d r e _ i d _ 4 d e f a 3 0 4 "   O N   " c o n t _ c e n t r o _ c o s t o "   ( " c e n t r o _ p a d r e _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ c u e n t a _ c o n t a b l e "   A D D   C O N S T R A I N T   " c o n t _ c u e n t a _ c o n t a b l e _ c u e n t a _ p a d r e _ i d _ 9 f 6 f 4 7 6 c _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ p a d r e _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ c u e n t a _ c o n t a b l e _ c u e n t a _ p a d r e _ i d _ 9 f 6 f 4 7 6 c "   O N   " c o n t _ c u e n t a _ c o n t a b l e "   ( " c u e n t a _ p a d r e _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ g r u p o _ c u e n t a _ c o d i g o _ f e 4 b b 3 b b _ l i k e "   O N   " c o n t _ g r u p o _ c u e n t a "   ( " c o d i g o "   v a r c h a r _ p a t t e r n _ o p s ) ;  
 C R E A T E   I N D E X   " c o n t _ m o n e d a _ c o d i g o _ 2 6 1 7 e 5 f e _ l i k e "   O N   " c o n t _ m o n e d a "   ( " c o d i g o "   v a r c h a r _ p a t t e r n _ o p s ) ;  
 C R E A T E   I N D E X   " c o n t _ t i p o _ a s i e n t o _ c o d i g o _ c 8 b 7 f 7 b 0 _ l i k e "   O N   " c o n t _ t i p o _ a s i e n t o "   ( " c o d i g o "   v a r c h a r _ p a t t e r n _ o p s ) ;  
 A L T E R   T A B L E   " c o n t _ p r o v i s i o n "   A D D   C O N S T R A I N T   " c o n t _ p r o v i s i o n _ c u e n t a _ i d _ e d b 9 5 8 3 5 _ f k _ c o n t _ c u e n t a _ c o n t a b l e _ i d "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ p r o v i s i o n _ c u e n t a _ i d _ e d b 9 5 8 3 5 "   O N   " c o n t _ p r o v i s i o n "   ( " c u e n t a _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ p e r i o d o _ c o n t a b l e "   A D D   C O N S T R A I N T   " c o n t _ p e r i o d o _ c o n t a b l e _ e j e r c i c i o _ i d _ n u m e r o _ 5 0 e e 8 3 e 2 _ u n i q "   U N I Q U E   ( " e j e r c i c i o _ i d " ,   " n u m e r o " ) ;  
 A L T E R   T A B L E   " c o n t _ p e r i o d o _ c o n t a b l e "   A D D   C O N S T R A I N T   " c o n t _ p e r i o d o _ c o n t a b l _ e j e r c i c i o _ i d _ 8 1 4 a 4 f 4 2 _ f k _ c o n t _ e j e r "   F O R E I G N   K E Y   ( " e j e r c i c i o _ i d " )   R E F E R E N C E S   " c o n t _ e j e r c i c i o _ f i s c a l "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ p e r i o d o _ c o n t a b l e _ e j e r c i c i o _ i d _ 8 1 4 a 4 f 4 2 "   O N   " c o n t _ p e r i o d o _ c o n t a b l e "   ( " e j e r c i c i o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ i n s t r u m e n t o _ f i n a n c i e r o "   A D D   C O N S T R A I N T   " c o n t _ i n s t r u m e n t o _ f i n _ c u e n t a _ i d _ 4 c 8 a 3 0 8 9 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ i n s t r u m e n t o _ f i n a n c i e r o _ c u e n t a _ i d _ 4 c 8 a 3 0 8 9 "   O N   " c o n t _ i n s t r u m e n t o _ f i n a n c i e r o "   ( " c u e n t a _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ i m p u e s t o _ d i f e r i d o "   A D D   C O N S T R A I N T   " c o n t _ i m p u e s t o _ d i f e r i _ c u e n t a _ i d _ b c a 3 7 3 8 1 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ i m p u e s t o _ d i f e r i d o "   A D D   C O N S T R A I N T   " c o n t _ i m p u e s t o _ d i f e r i _ p e r i o d o _ i d _ c 1 5 5 1 2 5 b _ f k _ c o n t _ p e r i "   F O R E I G N   K E Y   ( " p e r i o d o _ i d " )   R E F E R E N C E S   " c o n t _ p e r i o d o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ i m p u e s t o _ d i f e r i d o _ c u e n t a _ i d _ b c a 3 7 3 8 1 "   O N   " c o n t _ i m p u e s t o _ d i f e r i d o "   ( " c u e n t a _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ i m p u e s t o _ d i f e r i d o _ p e r i o d o _ i d _ c 1 5 5 1 2 5 b "   O N   " c o n t _ i m p u e s t o _ d i f e r i d o "   ( " p e r i o d o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ h e c h o _ p o s t e r i o r "   A D D   C O N S T R A I N T   " c o n t _ h e c h o _ p o s t e r i o r _ a s i e n t o _ a j u s t e _ i d _ 6 3 3 3 b 3 a 2 _ f k _ c o n t _ a s i e "   F O R E I G N   K E Y   ( " a s i e n t o _ a j u s t e _ i d " )   R E F E R E N C E S   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ h e c h o _ p o s t e r i o r "   A D D   C O N S T R A I N T   " c o n t _ h e c h o _ p o s t e r i o r _ e j e r c i c i o _ i d _ 2 1 a b b d 8 b _ f k _ c o n t _ e j e r "   F O R E I G N   K E Y   ( " e j e r c i c i o _ i d " )   R E F E R E N C E S   " c o n t _ e j e r c i c i o _ f i s c a l "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ h e c h o _ p o s t e r i o r _ a s i e n t o _ a j u s t e _ i d _ 6 3 3 3 b 3 a 2 "   O N   " c o n t _ h e c h o _ p o s t e r i o r "   ( " a s i e n t o _ a j u s t e _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ h e c h o _ p o s t e r i o r _ e j e r c i c i o _ i d _ 2 1 a b b d 8 b "   O N   " c o n t _ h e c h o _ p o s t e r i o r "   ( " e j e r c i c i o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ f l u j o _ e f e c t i v o "   A D D   C O N S T R A I N T   " c o n t _ f l u j o _ e f e c t i v o _ c u e n t a _ i d _ a 3 e 3 a 2 c b _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ f l u j o _ e f e c t i v o "   A D D   C O N S T R A I N T   " c o n t _ f l u j o _ e f e c t i v o _ p e r i o d o _ i d _ 1 e f a 7 0 f 7 _ f k _ c o n t _ p e r i "   F O R E I G N   K E Y   ( " p e r i o d o _ i d " )   R E F E R E N C E S   " c o n t _ p e r i o d o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ f l u j o _ e f e c t i v o _ c u e n t a _ i d _ a 3 e 3 a 2 c b "   O N   " c o n t _ f l u j o _ e f e c t i v o "   ( " c u e n t a _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ f l u j o _ e f e c t i v o _ p e r i o d o _ i d _ 1 e f a 7 0 f 7 "   O N   " c o n t _ f l u j o _ e f e c t i v o "   ( " p e r i o d o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ d e t e r i o r o _ a c t i v o "   A D D   C O N S T R A I N T   " c o n t _ d e t e r i o r o _ a c t i v _ a c t i v o _ f i j o _ i d _ f c a e 2 5 4 c _ f k _ c o n t _ a c t i "   F O R E I G N   K E Y   ( " a c t i v o _ f i j o _ i d " )   R E F E R E N C E S   " c o n t _ a c t i v o _ f i j o "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ d e t e r i o r o _ a c t i v o "   A D D   C O N S T R A I N T   " c o n t _ d e t e r i o r o _ a c t i v _ a c t i v o _ i n t a n g i b l e _ i d _ c 0 f 2 1 d f b _ f k _ c o n t _ a c t i "   F O R E I G N   K E Y   ( " a c t i v o _ i n t a n g i b l e _ i d " )   R E F E R E N C E S   " c o n t _ a c t i v o _ i n t a n g i b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ d e t e r i o r o _ a c t i v o "   A D D   C O N S T R A I N T   " c o n t _ d e t e r i o r o _ a c t i v _ a s i e n t o _ i d _ 9 e d e b 1 2 7 _ f k _ c o n t _ a s i e "   F O R E I G N   K E Y   ( " a s i e n t o _ i d " )   R E F E R E N C E S   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ d e t e r i o r o _ a c t i v o "   A D D   C O N S T R A I N T   " c o n t _ d e t e r i o r o _ a c t i v _ c u e n t a _ p e r d i d a _ i d _ 3 c 8 1 0 0 3 e _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ p e r d i d a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ d e t e r i o r o _ a c t i v o _ a c t i v o _ f i j o _ i d _ f c a e 2 5 4 c "   O N   " c o n t _ d e t e r i o r o _ a c t i v o "   ( " a c t i v o _ f i j o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ d e t e r i o r o _ a c t i v o _ a c t i v o _ i n t a n g i b l e _ i d _ c 0 f 2 1 d f b "   O N   " c o n t _ d e t e r i o r o _ a c t i v o "   ( " a c t i v o _ i n t a n g i b l e _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ d e t e r i o r o _ a c t i v o _ a s i e n t o _ i d _ 9 e d e b 1 2 7 "   O N   " c o n t _ d e t e r i o r o _ a c t i v o "   ( " a s i e n t o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ d e t e r i o r o _ a c t i v o _ c u e n t a _ p e r d i d a _ i d _ 3 c 8 1 0 0 3 e "   O N   " c o n t _ d e t e r i o r o _ a c t i v o "   ( " c u e n t a _ p e r d i d a _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ c u e n t a _ c o n t a b l e _ g r u p o _ i d _ a 0 d 6 0 4 0 4 "   O N   " c o n t _ c u e n t a _ c o n t a b l e "   ( " g r u p o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ c o s t o _ p r e s t a m o "   A D D   C O N S T R A I N T   " c o n t _ c o s t o _ p r e s t a m o _ a c t i v o _ c a l i f i c a d o _ i d _ 6 6 7 f 0 2 0 0 _ f k _ c o n t _ a c t i "   F O R E I G N   K E Y   ( " a c t i v o _ c a l i f i c a d o _ i d " )   R E F E R E N C E S   " c o n t _ a c t i v o _ f i j o "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ c o s t o _ p r e s t a m o "   A D D   C O N S T R A I N T   " c o n t _ c o s t o _ p r e s t a m o _ c u e n t a _ i n t e r e s _ i d _ 8 4 4 4 6 8 d 0 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i n t e r e s _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ c o s t o _ p r e s t a m o "   A D D   C O N S T R A I N T   " c o n t _ c o s t o _ p r e s t a m o _ c u e n t a _ p r e s t a m o _ i d _ 7 2 0 0 4 9 1 b _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ p r e s t a m o _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ c o s t o _ p r e s t a m o _ a c t i v o _ c a l i f i c a d o _ i d _ 6 6 7 f 0 2 0 0 "   O N   " c o n t _ c o s t o _ p r e s t a m o "   ( " a c t i v o _ c a l i f i c a d o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ c o s t o _ p r e s t a m o _ c u e n t a _ i n t e r e s _ i d _ 8 4 4 4 6 8 d 0 "   O N   " c o n t _ c o s t o _ p r e s t a m o "   ( " c u e n t a _ i n t e r e s _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ c o s t o _ p r e s t a m o _ c u e n t a _ p r e s t a m o _ i d _ 7 2 0 0 4 9 1 b "   O N   " c o n t _ c o s t o _ p r e s t a m o "   ( " c u e n t a _ p r e s t a m o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ b e n e f i c i o _ e m p l e a d o "   A D D   C O N S T R A I N T   " c o n t _ b e n e f i c i o _ e m p l e _ c u e n t a _ g a s t o _ i d _ 4 4 8 5 d f e 3 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ g a s t o _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ b e n e f i c i o _ e m p l e a d o "   A D D   C O N S T R A I N T   " c o n t _ b e n e f i c i o _ e m p l e _ c u e n t a _ p r o v i s i o n _ i d _ 6 1 3 9 7 9 8 c _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ p r o v i s i o n _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ b e n e f i c i o _ e m p l e a d o _ c u e n t a _ g a s t o _ i d _ 4 4 8 5 d f e 3 "   O N   " c o n t _ b e n e f i c i o _ e m p l e a d o "   ( " c u e n t a _ g a s t o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ b e n e f i c i o _ e m p l e a d o _ c u e n t a _ p r o v i s i o n _ i d _ 6 1 3 9 7 9 8 c "   O N   " c o n t _ b e n e f i c i o _ e m p l e a d o "   ( " c u e n t a _ p r o v i s i o n _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a s i e n t o _ c o n t a b l e _ m o n e d a _ i d _ 2 0 5 e 4 b 0 3 "   O N   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " m o n e d a _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a s i e n t o _ c o n t a b l e _ p e r i o d o _ i d _ e e 8 e 6 2 7 1 "   O N   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " p e r i o d o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a s i e n t o _ c o n t a b l e _ t i p o _ i d _ 3 e f 4 e b f a "   O N   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " t i p o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a c t i v o _ i n t a n g i b l e _ c u e n t a _ i d _ a 7 5 7 a 0 4 c "   O N   " c o n t _ a c t i v o _ i n t a n g i b l e "   ( " c u e n t a _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a c t i v o _ i n t a n g i b l e _ c u e n t a _ a m o r t i z a c i o n _ i d _ 0 7 c b d 7 4 3 "   O N   " c o n t _ a c t i v o _ i n t a n g i b l e "   ( " c u e n t a _ a m o r t i z a c i o n _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ a c t i v o _ i d _ 5 9 6 4 0 2 e 8 "   O N   " c o n t _ a c t i v o _ f i j o "   ( " c u e n t a _ a c t i v o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ d e p r e c i a c i o n _ i d _ d 5 0 2 1 6 9 8 "   O N   " c o n t _ a c t i v o _ f i j o "   ( " c u e n t a _ d e p r e c i a c i o n _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ a c t i v o _ f i j o _ c u e n t a _ g a s t o _ d e p r e c i a c i o n _ i d _ 4 8 d a 5 0 4 9 "   O N   " c o n t _ a c t i v o _ f i j o "   ( " c u e n t a _ g a s t o _ d e p r e c i a c i o n _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ t i p o _ c a m b i o "   A D D   C O N S T R A I N T   " c o n t _ t i p o _ c a m b i o _ m o n e d a _ i d _ f e c h a _ 7 f 8 f 2 a 3 4 _ u n i q "   U N I Q U E   ( " m o n e d a _ i d " ,   " f e c h a " ) ;  
 A L T E R   T A B L E   " c o n t _ t i p o _ c a m b i o "   A D D   C O N S T R A I N T   " c o n t _ t i p o _ c a m b i o _ m o n e d a _ i d _ c 1 4 0 2 e c 7 _ f k _ c o n t _ m o n e d a _ i d "   F O R E I G N   K E Y   ( " m o n e d a _ i d " )   R E F E R E N C E S   " c o n t _ m o n e d a "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ t i p o _ c a m b i o _ m o n e d a _ i d _ c 1 4 0 2 e c 7 "   O N   " c o n t _ t i p o _ c a m b i o "   ( " m o n e d a _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ p r o p i e d a d _ i n v e r s i o n "   A D D   C O N S T R A I N T   " c o n t _ p r o p i e d a d _ i n v e r s i o n _ c o d i g o _ e m p r e s a _ d 5 7 6 e 7 2 a _ u n i q "   U N I Q U E   ( " c o d i g o " ,   " e m p r e s a " ) ;  
 A L T E R   T A B L E   " c o n t _ p r o p i e d a d _ i n v e r s i o n "   A D D   C O N S T R A I N T   " c o n t _ p r o p i e d a d _ i n v e r _ c u e n t a _ i d _ 7 e 1 9 0 2 d d _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ p r o p i e d a d _ i n v e r s i o n _ c u e n t a _ i d _ 7 e 1 9 0 2 d d "   O N   " c o n t _ p r o p i e d a d _ i n v e r s i o n "   ( " c u e n t a _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ l i b r o _ m a y o r "   A D D   C O N S T R A I N T   " c o n t _ l i b r o _ m a y o r _ c u e n t a _ i d _ p e r i o d o _ i d _ e m p r e s a _ 5 c 8 9 6 4 d e _ u n i q "   U N I Q U E   ( " c u e n t a _ i d " ,   " p e r i o d o _ i d " ,   " e m p r e s a " ) ;  
 A L T E R   T A B L E   " c o n t _ l i b r o _ m a y o r "   A D D   C O N S T R A I N T   " c o n t _ l i b r o _ m a y o r _ c u e n t a _ i d _ c 7 2 a d 3 b a _ f k _ c o n t _ c u e n t a _ c o n t a b l e _ i d "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ l i b r o _ m a y o r "   A D D   C O N S T R A I N T   " c o n t _ l i b r o _ m a y o r _ p e r i o d o _ i d _ 1 c a a 7 1 c f _ f k _ c o n t _ p e r i "   F O R E I G N   K E Y   ( " p e r i o d o _ i d " )   R E F E R E N C E S   " c o n t _ p e r i o d o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ l i b r o _ m a y o r _ c u e n t a _ i d _ c 7 2 a d 3 b a "   O N   " c o n t _ l i b r o _ m a y o r "   ( " c u e n t a _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ l i b r o _ m a y o r _ p e r i o d o _ i d _ 1 c a a 7 1 c f "   O N   " c o n t _ l i b r o _ m a y o r "   ( " p e r i o d o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A D D   C O N S T R A I N T   " c o n t _ i n v e n t a r i o _ c o d i g o _ e m p r e s a _ f 8 e 2 7 e 6 5 _ u n i q "   U N I Q U E   ( " c o d i g o " ,   " e m p r e s a " ) ;  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A D D   C O N S T R A I N T   " c o n t _ i n v e n t a r i o _ c u e n t a _ c o s t o _ v e n t a _ i _ 3 e 0 1 e 9 1 8 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ c o s t o _ v e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A D D   C O N S T R A I N T   " c o n t _ i n v e n t a r i o _ c u e n t a _ i n v e n t a r i o _ i d _ d b b 5 b 3 6 5 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i n v e n t a r i o _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ i n v e n t a r i o _ c u e n t a _ c o s t o _ v e n t a _ i d _ 3 e 0 1 e 9 1 8 "   O N   " c o n t _ i n v e n t a r i o "   ( " c u e n t a _ c o s t o _ v e n t a _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ i n v e n t a r i o _ c u e n t a _ i n v e n t a r i o _ i d _ d b b 5 b 3 6 5 "   O N   " c o n t _ i n v e n t a r i o "   ( " c u e n t a _ i n v e n t a r i o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ d e t a l l e _ a s i e n t o "   A D D   C O N S T R A I N T   " c o n t _ d e t a l l e _ a s i e n t o _ a s i e n t o _ i d _ l i n e a _ 6 a c 7 e 2 3 6 _ u n i q "   U N I Q U E   ( " a s i e n t o _ i d " ,   " l i n e a " ) ;  
 A L T E R   T A B L E   " c o n t _ d e t a l l e _ a s i e n t o "   A D D   C O N S T R A I N T   " c o n t _ d e t a l l e _ a s i e n t o _ a s i e n t o _ i d _ 3 3 d 8 c 5 e 5 _ f k _ c o n t _ a s i e "   F O R E I G N   K E Y   ( " a s i e n t o _ i d " )   R E F E R E N C E S   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ d e t a l l e _ a s i e n t o "   A D D   C O N S T R A I N T   " c o n t _ d e t a l l e _ a s i e n t o _ c e n t r o _ c o s t o _ i d _ b 0 e 2 f c 7 e _ f k _ c o n t _ c e n t "   F O R E I G N   K E Y   ( " c e n t r o _ c o s t o _ i d " )   R E F E R E N C E S   " c o n t _ c e n t r o _ c o s t o "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ d e t a l l e _ a s i e n t o "   A D D   C O N S T R A I N T   " c o n t _ d e t a l l e _ a s i e n t o _ c u e n t a _ i d _ e c 8 1 1 6 3 7 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ d e t a l l e _ a s i e n t o _ a s i e n t o _ i d _ 3 3 d 8 c 5 e 5 "   O N   " c o n t _ d e t a l l e _ a s i e n t o "   ( " a s i e n t o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ d e t a l l e _ a s i e n t o _ c e n t r o _ c o s t o _ i d _ b 0 e 2 f c 7 e "   O N   " c o n t _ d e t a l l e _ a s i e n t o "   ( " c e n t r o _ c o s t o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ d e t a l l e _ a s i e n t o _ c u e n t a _ i d _ e c 8 1 1 6 3 7 "   O N   " c o n t _ d e t a l l e _ a s i e n t o "   ( " c u e n t a _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ d e p r e c i a c i o n "   A D D   C O N S T R A I N T   " c o n t _ d e p r e c i a c i o n _ a c t i v o _ i d _ p e r i o d o _ i d _ 5 9 5 6 8 3 9 8 _ u n i q "   U N I Q U E   ( " a c t i v o _ i d " ,   " p e r i o d o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ d e p r e c i a c i o n "   A D D   C O N S T R A I N T   " c o n t _ d e p r e c i a c i o n _ a c t i v o _ i d _ b 6 3 0 2 3 0 b _ f k _ c o n t _ a c t i v o _ f i j o _ i d "   F O R E I G N   K E Y   ( " a c t i v o _ i d " )   R E F E R E N C E S   " c o n t _ a c t i v o _ f i j o "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ d e p r e c i a c i o n "   A D D   C O N S T R A I N T   " c o n t _ d e p r e c i a c i o n _ a s i e n t o _ i d _ a e 6 2 3 3 a b _ f k _ c o n t _ a s i e "   F O R E I G N   K E Y   ( " a s i e n t o _ i d " )   R E F E R E N C E S   " c o n t _ a s i e n t o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 A L T E R   T A B L E   " c o n t _ d e p r e c i a c i o n "   A D D   C O N S T R A I N T   " c o n t _ d e p r e c i a c i o n _ p e r i o d o _ i d _ 2 9 6 b a 8 1 6 _ f k _ c o n t _ p e r i "   F O R E I G N   K E Y   ( " p e r i o d o _ i d " )   R E F E R E N C E S   " c o n t _ p e r i o d o _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ d e p r e c i a c i o n _ a c t i v o _ i d _ b 6 3 0 2 3 0 b "   O N   " c o n t _ d e p r e c i a c i o n "   ( " a c t i v o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ d e p r e c i a c i o n _ a s i e n t o _ i d _ a e 6 2 3 3 a b "   O N   " c o n t _ d e p r e c i a c i o n "   ( " a s i e n t o _ i d " ) ;  
 C R E A T E   I N D E X   " c o n t _ d e p r e c i a c i o n _ p e r i o d o _ i d _ 2 9 6 b a 8 1 6 "   O N   " c o n t _ d e p r e c i a c i o n "   ( " p e r i o d o _ i d " ) ;  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ b i o l o g i c o "   A D D   C O N S T R A I N T   " c o n t _ a c t i v o _ b i o l o g i c o _ c o d i g o _ e m p r e s a _ 5 1 e 7 7 7 b 8 _ u n i q "   U N I Q U E   ( " c o d i g o " ,   " e m p r e s a " ) ;  
 A L T E R   T A B L E   " c o n t _ a c t i v o _ b i o l o g i c o "   A D D   C O N S T R A I N T   " c o n t _ a c t i v o _ b i o l o g i c _ c u e n t a _ i d _ 0 4 d 9 a f 5 0 _ f k _ c o n t _ c u e n "   F O R E I G N   K E Y   ( " c u e n t a _ i d " )   R E F E R E N C E S   " c o n t _ c u e n t a _ c o n t a b l e "   ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;  
 C R E A T E   I N D E X   " c o n t _ a c t i v o _ b i o l o g i c o _ c u e n t a _ i d _ 0 4 d 9 a f 5 0 "   O N   " c o n t _ a c t i v o _ b i o l o g i c o "   ( " c u e n t a _ i d " ) ;  
 C O M M I T ;  
  
 - -   M I G R A T I O N   0 0 0 2  
 B E G I N ;  
 - -  
 - -   A d d   f i e l d   t i p o _ i n v e n t a r i o   t o   i n v e n t a r i o  
 - -  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A D D   C O L U M N   " t i p o _ i n v e n t a r i o "   v a r c h a r ( 3 0 )   D E F A U L T   ' O T R O S '   N O T   N U L L ;  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A L T E R   C O L U M N   " t i p o _ i n v e n t a r i o "   D R O P   D E F A U L T ;  
 - -  
 - -   A d d   f i e l d   n o m e n c l a t u r a   t o   i n v e n t a r i o  
 - -  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A D D   C O L U M N   " n o m e n c l a t u r a "   v a r c h a r ( 1 2 0 )   D E F A U L T   ' '   N O T   N U L L ;  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A L T E R   C O L U M N   " n o m e n c l a t u r a "   D R O P   D E F A U L T ;  
 C O M M I T ;  
  
 - -   M I G R A T I O N   0 0 0 3  
 B E G I N ;  
 - -  
 - -   C r e a t e   m o d e l   T i p o I n v e n t a r i o  
 - -  
 C R E A T E   T A B L E   " c o n t _ t i p o _ i n v e n t a r i o "   ( " i d "   b i g i n t   N O T   N U L L   P R I M A R Y   K E Y   G E N E R A T E D   B Y   D E F A U L T   A S   I D E N T I T Y ,   " c r e a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " u p d a t e d _ a t "   t i m e s t a m p   w i t h   t i m e   z o n e   N O T   N U L L ,   " i s _ a c t i v e "   b o o l e a n   N O T   N U L L ,   " c r e a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " u p d a t e d _ b y "   v a r c h a r ( 1 0 0 )   N U L L ,   " e m p r e s a "   v a r c h a r ( 1 0 )   N O T   N U L L ,   " n o m b r e "   v a r c h a r ( 1 2 0 )   N O T   N U L L ,   " o r d e n "   s m a l l i n t   N O T   N U L L   C H E C K   ( " o r d e n "   > =   0 ) ,   " n o t a s "   t e x t   N O T   N U L L ,   " c o d i g o _ l e g a c y "   v a r c h a r ( 3 0 )   N O T   N U L L ) ;  
 - -  
 - -   A d d   f i e l d   t i p o _ c a t a l o g o   t o   i n v e n t a r i o  
 - -  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   A D D   C O L U M N   " t i p o _ c a t a l o g o _ i d "   b i g i n t   N U L L   C O N S T R A I N T   " c o n t _ i n v e n t a r i o _ t i p o _ c a t a l o g o _ i d _ 2 9 f 2 e a e 0 _ f k _ c o n t _ t i p o "   R E F E R E N C E S   " c o n t _ t i p o _ i n v e n t a r i o " ( " i d " )   D E F E R R A B L E   I N I T I A L L Y   D E F E R R E D ;   S E T   C O N S T R A I N T S   " c o n t _ i n v e n t a r i o _ t i p o _ c a t a l o g o _ i d _ 2 9 f 2 e a e 0 _ f k _ c o n t _ t i p o "   I M M E D I A T E ;  
 - -  
 - -   R a w   P y t h o n   o p e r a t i o n  
 - -  
 - -   T H I S   O P E R A T I O N   C A N N O T   B E   W R I T T E N   A S   S Q L  
 - -  
 - -   R e m o v e   f i e l d   t i p o _ i n v e n t a r i o   f r o m   i n v e n t a r i o  
 - -  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   D R O P   C O L U M N   " t i p o _ i n v e n t a r i o "   C A S C A D E ;  
 - -  
 - -   R e n a m e   f i e l d   t i p o _ c a t a l o g o   o n   i n v e n t a r i o   t o   t i p o _ i n v e n t a r i o  
 - -  
 A L T E R   T A B L E   " c o n t _ i n v e n t a r i o "   R E N A M E   C O L U M N   " t i p o _ c a t a l o g o _ i d "   T O   " t i p o _ i n v e n t a r i o _ i d " ;  
 A L T E R   T A B L E   " c o n t _ t i p o _ i n v e n t a r i o "   A D D   C O N S T R A I N T   " c o n t _ t i p o _ i n v e n t a r i o _ e m p r e s a _ n o m b r e _ 7 3 1 1 e d a 1 _ u n i q "   U N I Q U E   ( " e m p r e s a " ,   " n o m b r e " ) ;  
 C R E A T E   I N D E X   " c o n t _ t i p o _ i n v e n t a r i o _ e m p r e s a _ a 1 d 3 d 5 2 3 "   O N   " c o n t _ t i p o _ i n v e n t a r i o "   ( " e m p r e s a " ) ;  
 C R E A T E   I N D E X   " c o n t _ t i p o _ i n v e n t a r i o _ e m p r e s a _ a 1 d 3 d 5 2 3 _ l i k e "   O N   " c o n t _ t i p o _ i n v e n t a r i o "   ( " e m p r e s a "   v a r c h a r _ p a t t e r n _ o p s ) ;  
 C R E A T E   I N D E X   " c o n t _ i n v e n t a r i o _ t i p o _ i n v e n t a r i o _ i d _ 8 0 a 9 6 e 3 6 "   O N   " c o n t _ i n v e n t a r i o "   ( " t i p o _ i n v e n t a r i o _ i d " ) ;  
 C O M M I T ;  
 
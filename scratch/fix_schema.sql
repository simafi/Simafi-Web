-- SQL Script to fix defaults and identities for Contabilidad tables
BEGIN;

-- Fixing table: cont_activo_biologico
CREATE SEQUENCE IF NOT EXISTS "cont_activo_biologico_id_seq";
ALTER TABLE "cont_activo_biologico" ALTER COLUMN "id" SET DEFAULT nextval('"cont_activo_biologico_id_seq"');
ALTER SEQUENCE "cont_activo_biologico_id_seq" OWNED BY "cont_activo_biologico"."id";
SELECT setval('"cont_activo_biologico_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_activo_biologico";
ALTER TABLE "cont_activo_biologico" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_activo_biologico" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_activo_biologico" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_activo_fijo
CREATE SEQUENCE IF NOT EXISTS "cont_activo_fijo_id_seq";
ALTER TABLE "cont_activo_fijo" ALTER COLUMN "id" SET DEFAULT nextval('"cont_activo_fijo_id_seq"');
ALTER SEQUENCE "cont_activo_fijo_id_seq" OWNED BY "cont_activo_fijo"."id";
SELECT setval('"cont_activo_fijo_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_activo_fijo";
ALTER TABLE "cont_activo_fijo" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_activo_fijo" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_activo_fijo" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_activo_intangible
CREATE SEQUENCE IF NOT EXISTS "cont_activo_intangible_id_seq";
ALTER TABLE "cont_activo_intangible" ALTER COLUMN "id" SET DEFAULT nextval('"cont_activo_intangible_id_seq"');
ALTER SEQUENCE "cont_activo_intangible_id_seq" OWNED BY "cont_activo_intangible"."id";
SELECT setval('"cont_activo_intangible_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_activo_intangible";
ALTER TABLE "cont_activo_intangible" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_activo_intangible" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_activo_intangible" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_asiento_contable
CREATE SEQUENCE IF NOT EXISTS "cont_asiento_contable_id_seq";
ALTER TABLE "cont_asiento_contable" ALTER COLUMN "id" SET DEFAULT nextval('"cont_asiento_contable_id_seq"');
ALTER SEQUENCE "cont_asiento_contable_id_seq" OWNED BY "cont_asiento_contable"."id";
SELECT setval('"cont_asiento_contable_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_asiento_contable";
ALTER TABLE "cont_asiento_contable" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_asiento_contable" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_asiento_contable" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_beneficio_empleado
CREATE SEQUENCE IF NOT EXISTS "cont_beneficio_empleado_id_seq";
ALTER TABLE "cont_beneficio_empleado" ALTER COLUMN "id" SET DEFAULT nextval('"cont_beneficio_empleado_id_seq"');
ALTER SEQUENCE "cont_beneficio_empleado_id_seq" OWNED BY "cont_beneficio_empleado"."id";
SELECT setval('"cont_beneficio_empleado_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_beneficio_empleado";
ALTER TABLE "cont_beneficio_empleado" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_beneficio_empleado" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_beneficio_empleado" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_centro_costo
CREATE SEQUENCE IF NOT EXISTS "cont_centro_costo_id_seq";
ALTER TABLE "cont_centro_costo" ALTER COLUMN "id" SET DEFAULT nextval('"cont_centro_costo_id_seq"');
ALTER SEQUENCE "cont_centro_costo_id_seq" OWNED BY "cont_centro_costo"."id";
SELECT setval('"cont_centro_costo_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_centro_costo";
ALTER TABLE "cont_centro_costo" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_centro_costo" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_centro_costo" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_costo_prestamo
CREATE SEQUENCE IF NOT EXISTS "cont_costo_prestamo_id_seq";
ALTER TABLE "cont_costo_prestamo" ALTER COLUMN "id" SET DEFAULT nextval('"cont_costo_prestamo_id_seq"');
ALTER SEQUENCE "cont_costo_prestamo_id_seq" OWNED BY "cont_costo_prestamo"."id";
SELECT setval('"cont_costo_prestamo_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_costo_prestamo";
ALTER TABLE "cont_costo_prestamo" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_costo_prestamo" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_costo_prestamo" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_cuenta_contable
CREATE SEQUENCE IF NOT EXISTS "cont_cuenta_contable_id_seq";
ALTER TABLE "cont_cuenta_contable" ALTER COLUMN "id" SET DEFAULT nextval('"cont_cuenta_contable_id_seq"');
ALTER SEQUENCE "cont_cuenta_contable_id_seq" OWNED BY "cont_cuenta_contable"."id";
SELECT setval('"cont_cuenta_contable_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_cuenta_contable";
ALTER TABLE "cont_cuenta_contable" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_cuenta_contable" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_cuenta_contable" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_depreciacion
CREATE SEQUENCE IF NOT EXISTS "cont_depreciacion_id_seq";
ALTER TABLE "cont_depreciacion" ALTER COLUMN "id" SET DEFAULT nextval('"cont_depreciacion_id_seq"');
ALTER SEQUENCE "cont_depreciacion_id_seq" OWNED BY "cont_depreciacion"."id";
SELECT setval('"cont_depreciacion_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_depreciacion";
ALTER TABLE "cont_depreciacion" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_depreciacion" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_depreciacion" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_detalle_asiento
CREATE SEQUENCE IF NOT EXISTS "cont_detalle_asiento_id_seq";
ALTER TABLE "cont_detalle_asiento" ALTER COLUMN "id" SET DEFAULT nextval('"cont_detalle_asiento_id_seq"');
ALTER SEQUENCE "cont_detalle_asiento_id_seq" OWNED BY "cont_detalle_asiento"."id";
SELECT setval('"cont_detalle_asiento_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_detalle_asiento";
ALTER TABLE "cont_detalle_asiento" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_detalle_asiento" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_detalle_asiento" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_deterioro_activo
CREATE SEQUENCE IF NOT EXISTS "cont_deterioro_activo_id_seq";
ALTER TABLE "cont_deterioro_activo" ALTER COLUMN "id" SET DEFAULT nextval('"cont_deterioro_activo_id_seq"');
ALTER SEQUENCE "cont_deterioro_activo_id_seq" OWNED BY "cont_deterioro_activo"."id";
SELECT setval('"cont_deterioro_activo_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_deterioro_activo";
ALTER TABLE "cont_deterioro_activo" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_deterioro_activo" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_deterioro_activo" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_ejercicio_fiscal
CREATE SEQUENCE IF NOT EXISTS "cont_ejercicio_fiscal_id_seq";
ALTER TABLE "cont_ejercicio_fiscal" ALTER COLUMN "id" SET DEFAULT nextval('"cont_ejercicio_fiscal_id_seq"');
ALTER SEQUENCE "cont_ejercicio_fiscal_id_seq" OWNED BY "cont_ejercicio_fiscal"."id";
SELECT setval('"cont_ejercicio_fiscal_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_ejercicio_fiscal";
ALTER TABLE "cont_ejercicio_fiscal" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_ejercicio_fiscal" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_ejercicio_fiscal" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_flujo_efectivo
CREATE SEQUENCE IF NOT EXISTS "cont_flujo_efectivo_id_seq";
ALTER TABLE "cont_flujo_efectivo" ALTER COLUMN "id" SET DEFAULT nextval('"cont_flujo_efectivo_id_seq"');
ALTER SEQUENCE "cont_flujo_efectivo_id_seq" OWNED BY "cont_flujo_efectivo"."id";
SELECT setval('"cont_flujo_efectivo_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_flujo_efectivo";
ALTER TABLE "cont_flujo_efectivo" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_flujo_efectivo" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_flujo_efectivo" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_grupo_cuenta
CREATE SEQUENCE IF NOT EXISTS "cont_grupo_cuenta_id_seq";
ALTER TABLE "cont_grupo_cuenta" ALTER COLUMN "id" SET DEFAULT nextval('"cont_grupo_cuenta_id_seq"');
ALTER SEQUENCE "cont_grupo_cuenta_id_seq" OWNED BY "cont_grupo_cuenta"."id";
SELECT setval('"cont_grupo_cuenta_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_grupo_cuenta";
ALTER TABLE "cont_grupo_cuenta" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_grupo_cuenta" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_grupo_cuenta" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_hecho_posterior
CREATE SEQUENCE IF NOT EXISTS "cont_hecho_posterior_id_seq";
ALTER TABLE "cont_hecho_posterior" ALTER COLUMN "id" SET DEFAULT nextval('"cont_hecho_posterior_id_seq"');
ALTER SEQUENCE "cont_hecho_posterior_id_seq" OWNED BY "cont_hecho_posterior"."id";
SELECT setval('"cont_hecho_posterior_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_hecho_posterior";
ALTER TABLE "cont_hecho_posterior" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_hecho_posterior" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_hecho_posterior" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_impuesto_diferido
CREATE SEQUENCE IF NOT EXISTS "cont_impuesto_diferido_id_seq";
ALTER TABLE "cont_impuesto_diferido" ALTER COLUMN "id" SET DEFAULT nextval('"cont_impuesto_diferido_id_seq"');
ALTER SEQUENCE "cont_impuesto_diferido_id_seq" OWNED BY "cont_impuesto_diferido"."id";
SELECT setval('"cont_impuesto_diferido_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_impuesto_diferido";
ALTER TABLE "cont_impuesto_diferido" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_impuesto_diferido" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_impuesto_diferido" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_instrumento_financiero
CREATE SEQUENCE IF NOT EXISTS "cont_instrumento_financiero_id_seq";
ALTER TABLE "cont_instrumento_financiero" ALTER COLUMN "id" SET DEFAULT nextval('"cont_instrumento_financiero_id_seq"');
ALTER SEQUENCE "cont_instrumento_financiero_id_seq" OWNED BY "cont_instrumento_financiero"."id";
SELECT setval('"cont_instrumento_financiero_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_instrumento_financiero";
ALTER TABLE "cont_instrumento_financiero" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_instrumento_financiero" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_instrumento_financiero" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_inventario
CREATE SEQUENCE IF NOT EXISTS "cont_inventario_id_seq";
ALTER TABLE "cont_inventario" ALTER COLUMN "id" SET DEFAULT nextval('"cont_inventario_id_seq"');
ALTER SEQUENCE "cont_inventario_id_seq" OWNED BY "cont_inventario"."id";
SELECT setval('"cont_inventario_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_inventario";
ALTER TABLE "cont_inventario" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_inventario" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_inventario" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_libro_mayor
CREATE SEQUENCE IF NOT EXISTS "cont_libro_mayor_id_seq";
ALTER TABLE "cont_libro_mayor" ALTER COLUMN "id" SET DEFAULT nextval('"cont_libro_mayor_id_seq"');
ALTER SEQUENCE "cont_libro_mayor_id_seq" OWNED BY "cont_libro_mayor"."id";
SELECT setval('"cont_libro_mayor_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_libro_mayor";
ALTER TABLE "cont_libro_mayor" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_libro_mayor" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_libro_mayor" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_moneda
CREATE SEQUENCE IF NOT EXISTS "cont_moneda_id_seq";
ALTER TABLE "cont_moneda" ALTER COLUMN "id" SET DEFAULT nextval('"cont_moneda_id_seq"');
ALTER SEQUENCE "cont_moneda_id_seq" OWNED BY "cont_moneda"."id";
SELECT setval('"cont_moneda_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_moneda";
ALTER TABLE "cont_moneda" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_moneda" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_moneda" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_periodo_contable
CREATE SEQUENCE IF NOT EXISTS "cont_periodo_contable_id_seq";
ALTER TABLE "cont_periodo_contable" ALTER COLUMN "id" SET DEFAULT nextval('"cont_periodo_contable_id_seq"');
ALTER SEQUENCE "cont_periodo_contable_id_seq" OWNED BY "cont_periodo_contable"."id";
SELECT setval('"cont_periodo_contable_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_periodo_contable";
ALTER TABLE "cont_periodo_contable" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_periodo_contable" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_periodo_contable" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_politica_contable
CREATE SEQUENCE IF NOT EXISTS "cont_politica_contable_id_seq";
ALTER TABLE "cont_politica_contable" ALTER COLUMN "id" SET DEFAULT nextval('"cont_politica_contable_id_seq"');
ALTER SEQUENCE "cont_politica_contable_id_seq" OWNED BY "cont_politica_contable"."id";
SELECT setval('"cont_politica_contable_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_politica_contable";
ALTER TABLE "cont_politica_contable" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_politica_contable" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_politica_contable" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_propiedad_inversion
CREATE SEQUENCE IF NOT EXISTS "cont_propiedad_inversion_id_seq";
ALTER TABLE "cont_propiedad_inversion" ALTER COLUMN "id" SET DEFAULT nextval('"cont_propiedad_inversion_id_seq"');
ALTER SEQUENCE "cont_propiedad_inversion_id_seq" OWNED BY "cont_propiedad_inversion"."id";
SELECT setval('"cont_propiedad_inversion_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_propiedad_inversion";
ALTER TABLE "cont_propiedad_inversion" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_propiedad_inversion" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_propiedad_inversion" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_provision
CREATE SEQUENCE IF NOT EXISTS "cont_provision_id_seq";
ALTER TABLE "cont_provision" ALTER COLUMN "id" SET DEFAULT nextval('"cont_provision_id_seq"');
ALTER SEQUENCE "cont_provision_id_seq" OWNED BY "cont_provision"."id";
SELECT setval('"cont_provision_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_provision";
ALTER TABLE "cont_provision" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_provision" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_provision" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_tipo_asiento
CREATE SEQUENCE IF NOT EXISTS "cont_tipo_asiento_id_seq";
ALTER TABLE "cont_tipo_asiento" ALTER COLUMN "id" SET DEFAULT nextval('"cont_tipo_asiento_id_seq"');
ALTER SEQUENCE "cont_tipo_asiento_id_seq" OWNED BY "cont_tipo_asiento"."id";
SELECT setval('"cont_tipo_asiento_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_tipo_asiento";
ALTER TABLE "cont_tipo_asiento" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_tipo_asiento" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_tipo_asiento" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_tipo_cambio
CREATE SEQUENCE IF NOT EXISTS "cont_tipo_cambio_id_seq";
ALTER TABLE "cont_tipo_cambio" ALTER COLUMN "id" SET DEFAULT nextval('"cont_tipo_cambio_id_seq"');
ALTER SEQUENCE "cont_tipo_cambio_id_seq" OWNED BY "cont_tipo_cambio"."id";
SELECT setval('"cont_tipo_cambio_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_tipo_cambio";
ALTER TABLE "cont_tipo_cambio" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_tipo_cambio" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_tipo_cambio" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing table: cont_tipo_inventario
CREATE SEQUENCE IF NOT EXISTS "cont_tipo_inventario_id_seq";
ALTER TABLE "cont_tipo_inventario" ALTER COLUMN "id" SET DEFAULT nextval('"cont_tipo_inventario_id_seq"');
ALTER SEQUENCE "cont_tipo_inventario_id_seq" OWNED BY "cont_tipo_inventario"."id";
SELECT setval('"cont_tipo_inventario_id_seq"', COALESCE(max("id"), 0) + 1, false) FROM "cont_tipo_inventario";
ALTER TABLE "cont_tipo_inventario" ALTER COLUMN "created_at" SET DEFAULT now();
ALTER TABLE "cont_tipo_inventario" ALTER COLUMN "updated_at" SET DEFAULT now();
ALTER TABLE "cont_tipo_inventario" ALTER COLUMN "is_active" SET DEFAULT true;

-- Fixing EjercicioFiscal uniqueness (Idempotent)
ALTER TABLE "cont_ejercicio_fiscal" DROP CONSTRAINT IF EXISTS "cont_ejercicio_fiscal_anio_key";
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cont_ejercicio_fiscal_anio_empresa_uniq') THEN
        ALTER TABLE "cont_ejercicio_fiscal" ADD CONSTRAINT "cont_ejercicio_fiscal_anio_empresa_uniq" UNIQUE ("anio", "empresa");
    END IF;
END $$;

COMMIT;
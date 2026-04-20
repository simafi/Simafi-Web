# Catálogo de Rubros Reservados (NO MODIFICAR)

Este documento define **códigos de rubro reservados** por funcionalidad dentro del **Módulo Tributario**.  
Estos códigos se consideran **estándar del sistema**: su significado y uso **no debe cambiar**, aunque la descripción visible pueda variar por municipio.

## Reglas generales

- **No reutilizar** un rubro reservado para otro fin.
- **No renombrar** el código (ej. `B0001`) ni cambiar su naturaleza (impuesto/tasa/recargo).
- Si un municipio necesita un concepto nuevo, **crear un rubro nuevo** (no usar uno reservado).

## Convención de mora (prefijos obligatorios)

Esta convención es **estándar del sistema** y se usa para reportes/desgloses (por ejemplo `desglose_mora` en BI/ICS):

- **`R*`**: **Recargos moratorios** (mora por recargo)
- **`I*`**: **Intereses** (mora por interés)

Todo lo que **no** inicie con `R` o `I` se considera **cargo base** (impuesto/tasa u otros conceptos), y su clasificación “año actual vs años anteriores” se hace por el **año del periodo** del cargo (`ano` / periodo contable), no por la fecha en que el contribuyente paga.

## Bienes Inmuebles (Catastro / BI)

Estos rubros se usan en **Bienes Inmuebles** y en reglas de descuentos (Adulto Mayor) y cálculo de recibos.

| Código | Nombre funcional (reservado) | Notas |
|---|---|---|
| `B0001` | Impuesto de Bienes Inmuebles **Urbano** | **Siempre** representa BI Urbano. |
| `B0002` | Impuesto de Bienes Inmuebles **Rural** | **Siempre** representa BI Rural. |
| `T0001` | Tasa de servicio público asociada a BI (ej. agua/alcantarillado) | Se trata como tasa “especial” en descuentos de Adulto Mayor; el rótulo puede variar según el municipio. |

## Negocios (ICS)

Estos rubros se usan en **declaración/estado de cuenta** y generación de transacciones de Negocios.

| Código | Nombre funcional (reservado) | Frecuencia típica | Notas |
|---|---|---|---|
| `C0001` | Impuesto Industria, Comercio y Servicios (ICS) | Mensual | Rubro base principal de ICS. |
| `C0002` | Permiso de Operación | Anual | Cobro anual del negocio. |
| `C0003` | Multa Declaración de Negocios | Anual (según parametrización) | Multa asociada a declaraciones. |
| `T0001` | Tasa de servicio público (ej. alcantarillado/agua) | Mensual | Rubro reservado usado también en BI (tasa pública). |
| `T0002` | Tren de Aseo | Mensual | Tasa municipal (aseo). |

## Códigos “concepto” (internos de recibo / descuentos)

Adicionalmente, el sistema puede generar **conceptos internos** para detallar descuentos en recibos (no son rubros nuevos del catálogo, pero deben mantenerse estables en la lógica).

- **`DPA`**: Descuento Pago Anual (ítem negativo)
- **`DTE`**: Descuento Tercera Edad (ítem negativo)
- **`DCE`**: Descuento Cuarta Edad (ítem negativo)
- **`AMR` / `AMI` / `DAM`**: Amnistía (recargos/intereses/saldo) (ítems negativos)

## Trazabilidad (dónde se usan)

- **Bienes Inmuebles**: reglas de descuentos y recibos en `tributario_app/views.py` (`enviar_a_caja_bienes`)
- **Negocios (ICS)**: listado/descripcion de rubros en `tributario_app/templates/declaracion_volumen.html` y generación de pagos en `tributario/views.py` (`calcular_transaccion_pago`, `guardar_transaccion_pago`)


# Guía de Usuario – Módulo de Contabilidad SIMAFI Web

Esta guía explica cómo operar el módulo de contabilidad **sin necesidad de experiencia previa**. Siga los pasos en orden para dejar el sistema listo para registrar asientos y generar reportes.

---

## 1. ¿Qué hace este módulo?

El módulo de contabilidad permite:

- **Configurar el plan de cuentas** (Activo, Pasivo, Capital, Ingresos y Egresos).
- **Registrar asientos contables** (libro diario) con partida doble.
- **Consultar saldos** por cuenta (libro mayor) y **generar estados financieros** (Balance General, Estado de Resultados).
- Gestionar **activos fijos**, **inventarios**, **ejercicios fiscales** y **centros de costo**.

Todo está basado en Normas Internacionales de Contabilidad (NIC/IAS).

---

## 2. Los cinco elementos contables (Activo, Pasivo, Capital, Ingresos, Egresos)

En contabilidad, las cuentas se agrupan en **cinco grandes categorías**. En este sistema cada una tiene un **código de grupo** (número del 1 al 7):

| Código | Nombre en el sistema        | Qué representa | Naturaleza  | Ejemplos |
|--------|-----------------------------|----------------|-------------|----------|
| **1**  | **Activo**                  | Recursos y derechos que tiene la entidad | Deudora  | Caja, bancos, cuentas por cobrar, inventarios, activos fijos |
| **2**  | **Pasivo**                  | Obligaciones con terceros                 | Acreedora | Proveedores, préstamos, impuestos por pagar, sueldos por pagar |
| **3**  | **Patrimonio (Capital)**    | Lo que queda: Activos − Pasivos           | Acreedora | Capital social, reservas, resultados acumulados |
| **4**  | **Cuentas de Orden**        | Control y revelación (avales, garantías) | Acreedora | Avales, fianzas |
| **5**  | **Ingresos**                | Entradas de recursos que generan beneficio | Acreedora | Ventas, servicios, intereses ganados |
| **6**  | **Gastos**                  | Salidas de recursos (operación)          | Deudora   | Sueldos, servicios, depreciación |
| **7**  | **Gastos administrativos y otros** | Otros gastos no operativos          | Deudora   | Gastos administrativos, financieros |

- **Naturaleza Deudora**: aumentan con débitos (debe) y disminuyen con créditos (haber). Ej.: Activo, Gastos.
- **Naturaleza Acreedora**: aumentan con créditos (haber) y disminuyen con débitos (debe). Ej.: Pasivo, Capital, Ingresos.

Para **configurar correctamente** el plan de cuentas, asigne cada cuenta al **grupo** que corresponda (1=Activo, 2=Pasivo, 3=Patrimonio, 5=Ingresos, 6 o 7=Gastos/Egresos).

---

## 3. Configuración inicial (paso a paso)

### Paso 1: Ejercicio fiscal

Antes de registrar asientos debe existir un **año contable** (ejercicio fiscal) **abierto**.

1. Menú Contabilidad → **Ejercicios Fiscales**.
2. Clic en **Nuevo** (o "Crear ejercicio").
3. Complete:
   - **Año** (ej.: 2025).
   - **Descripción** (ej.: "Ejercicio 2025").
   - **Fecha inicio** y **Fecha fin** (ej.: 01/01/2025 y 31/12/2025).
   - **Estado**: Abierto.
   - **Empresa**: código de su municipio/entidad (ej.: 0301).
4. Guarde. El sistema creará automáticamente los períodos mensuales (1 a 12).

Sin ejercicio abierto no se pueden cargar asientos.

---

### Paso 2: Grupos de cuentas (Activo, Pasivo, Capital, Ingresos, Egresos)

Los **grupos** (1=Activo, 2=Pasivo, 3=Patrimonio, 4=Cuentas de Orden, 5=Ingresos, 6 y 7=Gastos) suelen crearse automáticamente la primera vez que se usa el plan de cuentas o al cargar un catálogo. Si no existen:

- El sistema los crea al cargar el catálogo con el comando `load_catalogo_contable`.
- O puede verificar en **Plan de Cuentas** que al filtrar por "Grupo" aparezcan las opciones 1, 2, 3, 5, 6, 7.

No es necesario que un usuario sin experiencia cree grupos a mano; basta con **cargar el plan de cuentas** (paso 3).

---

### Paso 3: Plan de cuentas (Activo, Pasivo, Capital, Ingresos, Egresos)

El **plan de cuentas** es el catálogo donde se definen todas las cuentas (con su código, nombre y grupo).

**Opción A – Cargar catálogo desde archivo (recomendado)**

1. Prepare un archivo **TSV** (columnas separadas por tabulador) con al menos:
   - **codgrupo**: 1=Activo, 2=Pasivo, 3=Patrimonio, 5=Ingresos, 6 o 7=Egresos.
   - **cuenta**: código de la cuenta (ej.: 111-01-01-00-00).
   - **descrip**: nombre de la cuenta (ej.: Caja Chica).
2. Desde la carpeta del proyecto (donde está `manage.py` del módulo tributario):

   ```bash
   python manage.py load_catalogo_contable ruta/al/archivo.tsv --empresa=0301
   ```

   Use `--dry-run` para ver qué se cargaría sin guardar. Use `--replace` si quiere reemplazar todo el plan de esa empresa.

3. Después de cargar, vaya a **Plan de Cuentas** en el menú y verifique que ve las cuentas por grupo (Activo, Pasivo, etc.).

**Opción B – Crear cuentas manualmente**

1. Menú Contabilidad → **Plan de Cuentas**.
2. Clic en **Nueva Cuenta**.
3. Complete:
   - **Código**: único (ej.: 1110, 111-01-01-00-00).
   - **Nombre**: descripción clara.
   - **Grupo**: seleccione **1=Activo**, **2=Pasivo**, **3=Patrimonio**, **5=Ingresos** o **6/7=Gastos** según corresponda.
   - **Cuenta padre**: si es una subcuenta, elija la cuenta que la agrupa.
   - **Naturaleza**: normalmente se asigna según el grupo (Activo/Gastos = Deudora; Pasivo/Capital/Ingresos = Acreedora).
   - **Tipo**: Título (solo agrupa) o Detalle (acepta movimientos).
4. Guarde. Repita para todas las cuentas que necesite.

**Resumen de a qué grupo va cada tipo de cuenta:**

- **Activo (1)**: Caja, bancos, cuentas por cobrar, inventarios, activos fijos, gastos pagados por anticipado.
- **Pasivo (2)**: Proveedores, préstamos, impuestos por pagar, sueldos por pagar, anticipos de clientes.
- **Patrimonio / Capital (3)**: Capital social, reservas, resultados acumulados, resultado del ejercicio.
- **Ingresos (5)**: Ventas, servicios, intereses ganados, otros ingresos.
- **Egresos / Gastos (6 o 7)**: Sueldos, servicios básicos, depreciación, gastos administrativos, financieros, etc.

---

### Paso 4: Centros de costo (opcional)

Si desea distribuir gastos o ingresos por área o proyecto:

1. Menú → **Centros de Costo**.
2. Cree los centros (código, nombre, responsable, empresa).
3. Al registrar asientos, podrá asociar líneas a un centro de costo si la cuenta lo requiere.

---

### Paso 5: Registrar asientos

Cuando tenga **ejercicio abierto** y **plan de cuentas** con al menos las cuentas básicas:

1. Menú → **Asientos Contables** → **Nuevo asiento**.
2. Elija **tipo de asiento**, **período** y **fecha**.
3. Escriba el **concepto** y en las líneas:
   - **Cuenta**: seleccione una cuenta del plan (del grupo que corresponda: Activo, Pasivo, etc.).
   - **Debe** o **Haber**: solo uno por línea; el total Debe debe ser igual al total Haber (partida doble).
4. Guarde como borrador. Luego puede **Aprobar** y **Contabilizar**.

Para no equivocarse con la naturaleza:

- Si la cuenta es **Activo** o **Gasto**: aumentar = Débito; disminuir = Crédito.
- Si la cuenta es **Pasivo**, **Capital** o **Ingreso**: aumentar = Crédito; disminuir = Débito.

---

### Paso 6: Consultar saldos y reportes

- **Libro Mayor**: saldos por cuenta y período.
- **Estados Financieros**: Balance General (Activo, Pasivo, Capital) y Estado de Resultados (Ingresos y Egresos).

---

## 4. Resumen rápido: configurar Activo, Pasivo, Capital, Ingresos y Egresos

| Elemento        | Código grupo | Dónde se configura        | Qué hacer |
|-----------------|-------------|---------------------------|-----------|
| **Activo**      | 1           | Plan de Cuentas (Grupo 1) | Crear o cargar cuentas con codgrupo 1 (caja, bancos, inventarios, activos fijos, etc.). |
| **Pasivo**      | 2           | Plan de Cuentas (Grupo 2) | Crear o cargar cuentas con codgrupo 2 (proveedores, préstamos, impuestos por pagar, etc.). |
| **Capital**     | 3           | Plan de Cuentas (Grupo 3) | Crear o cargar cuentas con codgrupo 3 (capital social, reservas, resultados). |
| **Ingresos**    | 5           | Plan de Cuentas (Grupo 5) | Crear o cargar cuentas con codgrupo 5 (ventas, servicios, otros ingresos). |
| **Egresos**     | 6 y 7       | Plan de Cuentas (Grupos 6 y 7) | Crear o cargar cuentas con codgrupo 6 o 7 (gastos operativos y administrativos). |

Todo se configura desde **Plan de Cuentas** (y, si aplica, desde la carga del archivo TSV). Los **grupos** definen si la cuenta es Activo, Pasivo, Capital, Ingresos o Egresos.

---

## 5. Comando de carga del catálogo (referencia)

```bash
# Desde la carpeta donde está manage.py (por ejemplo venv\Scripts\tributario)
python manage.py load_catalogo_contable archivo.tsv --empresa=0301

# Solo simular (no guarda)
python manage.py load_catalogo_contable archivo.tsv --empresa=0301 --dry-run

# Reemplazar todo el plan de la empresa
python manage.py load_catalogo_contable archivo.tsv --empresa=0301 --replace
```

Columnas mínimas del TSV: **codgrupo**, **cuenta**, **descrip** (las demás son opcionales).

---

## 6. Dónde encontrar cada cosa en el menú

| Tarea                     | Menú / Opción          |
|---------------------------|-------------------------|
| Ver/editar plan de cuentas | Plan de Cuentas        |
| Crear ejercicio fiscal    | Ejercicios Fiscales    |
| Registrar asientos       | Asientos Contables     |
| Ver saldos por cuenta    | Libro Mayor            |
| Balance y resultados      | Estados Financieros    |
| Activos fijos             | Activos Fijos          |
| Inventarios               | Inventarios            |
| Centros de costo          | Centros de Costo       |

---

Si sigue esta guía en orden (ejercicio → plan de cuentas con Activo, Pasivo, Capital, Ingresos y Egresos → asientos), podrá operar el módulo de contabilidad aunque no tenga experiencia previa. Para dudas sobre un pantalla concreta, use la opción **Configuración inicial** en el menú de Contabilidad.

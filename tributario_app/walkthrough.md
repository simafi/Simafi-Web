# Walkthrough - Sub-módulo de Impuesto Personal

Hemos completado la integración del sub-módulo de Impuesto Personal en SimafiWeb, cumpliendo con los requisitos fiscales hondureños y las directrices de diseño del proyecto.

## Cambios Realizados

### 1. Modelado de Datos y Base de Datos
- Se creó la aplicación `impuesto_personal`.
- Modelos implementados:
    - `Contribuyente`: Vinculación con la identidad del ciudadano.
    - `DeclaracionPersonal`: Almacena ingresos, deducciones e impuestos calculados.
    - `PlanillaEmpresa` y `DetallePlanilla`: Gestión de retenciones masivas por parte de empresas.
    - `TarifasPersonal`: Escalas progresivas para el cálculo del impuesto.

### 2. Lógica de Negocio (Servicios)
- **Cálculo de Impuestos**: Lógica progresiva basada en la renta neta gravable.
- **Multas y Recargos**: Aplicación automática del 5% por declaración tardía y 1% mensual por mora en el pago.
- **Procesamiento de Planillas**: Importación automatizada desde archivos **Excel (.xlsx)** y **CSV**, vinculando empleados mediante su DNI.

### 3. Interfaz de Usuario (UI/UX)
- **Glassmorphism**: Aplicación de estilos modernos con transparencias, desenfoques y gradientes.
- **Dashboard**: Integración de un nuevo módulo en el menú principal tributario.
- **Formularios Reactivos**: Los cálculos de impuestos se visualizan en tiempo real en la pantalla de declaración.

### 4. Solvencia Municipal
- **Bloqueo por Mora**: El sistema verifica automáticamente si el ciudadano tiene deudas en Bienes Inmuebles o Negocios (ICS) antes de permitir la emisión del documento.
- **Generación de PDF**: Implementación de constancias oficiales usando `ReportLab`, con validación de seguridad y fecha de vigencia.

## Verificación

- [x] **Cálculos**: Validados en `services.py` con lógica de redondeo decimal.
- [x] **Seguridad**: Los accesos a las vistas están protegidos por el sistema de autenticación de Django.
- [x] **Integridad**: Relaciones sólidas con los modelos existentes de `catastro` y `tributario`.

## Próximos Pasos Recomendados
- **Pruebas de Campo**: Cargar una planilla real de una empresa con más de 100 empleados para validar rendimiento.
- **Personalización de PDF**: Ajustar el diseño del certificado si el municipio requiere logos específicos o sellos de agua.

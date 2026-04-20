# FUNCIONALIDAD FINAL - Carga Automática de Declaraciones

## ✅ Funcionamiento Correcto Implementado

### Flujo de Usuario

#### 1. Usuario cambia el año en el combo
- Selecciona un año diferente en el dropdown

#### 2. Aparece mensaje de confirmación
```
¿Desea cargar los datos del año XXXX?

Si existe una declaración para este año (Empresa: 0301, RTM: xxx, Expediente: xxx), 
se cargarán automáticamente los datos registrados.
```

#### 3. Usuario presiona "Aceptar" (OK)
- ✅ La página se recarga con la URL: 
  ```
  /declaracion-volumen/?empresa=0301&rtm=xxx&expe=xxx&ano_cargar=XXXX
  ```
- ✅ El backend busca declaración por: **empresa + RTM + expediente + año** (SIN mes)
- ✅ **Si existe declaración:**
  - Se cargan TODOS los datos de la tabla `declara`
  - Año queda seleccionado en el combo
  - Mes se actualiza al de la declaración
  - Ventas, impuestos, etc. se cargan
  - Mensaje: "Declaracion XXXX/XX cargada desde la base de datos"

- ✅ **Si NO existe declaración:**
  - Formulario nuevo (campos vacíos)
  - Año queda seleccionado en el combo
  - Mes es el actual
  - Listo para crear nueva declaración

#### 4. Usuario presiona "Cancelar"
- ✅ El combo vuelve al año anterior
- ✅ NO se recarga la página
- ✅ Los datos permanecen sin cambios

## Validación Implementada

### Backend busca declaración por:
```sql
SELECT * FROM declara 
WHERE empresa = '0301' 
  AND rtm = '114-03-23' 
  AND expe = '1151' 
  AND ano = 2024
LIMIT 1;
```

**NO** se valida por mes, como solicitaste.

## Ejemplos de Uso

### Caso 1: Cambiar a año 2024 (con declaración existente)

**URL inicial:**
```
http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

**Acción:** Usuario selecciona año 2024 → Confirma

**URL después de recargar:**
```
http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2024
```

**Resultado:**
- Año 2024 seleccionado en combo
- Mes: 01 (Enero)
- Ventas Industria: 1,000,000.00
- Todos los datos de la declaración 2024/01 cargados

### Caso 2: Cambiar a año 2023 (sin declaración)

**Acción:** Usuario selecciona año 2023 → Confirma

**URL después de recargar:**
```
http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2023
```

**Resultado:**
- Año 2023 seleccionado en combo
- Mes: 10 (Octubre - mes actual)
- Campos de ventas vacíos
- Formulario nuevo listo para crear declaración 2023

### Caso 3: Usuario cancela

**Acción:** Usuario selecciona año 2024 → Cancela

**Resultado:**
- Combo vuelve al año anterior (2025)
- Página NO se recarga
- Datos actuales permanecen sin cambios

## Logs del Sistema

### Logs en Consola del Navegador (F12)
```javascript
[CARGA AUTO] Año cambiado de 2025 a 2024
[CARGA AUTO] Usuario confirmó. Cargando datos del año 2024
[CARGA AUTO] Recargando con URL: /declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2024
```

### Logs en Terminal del Servidor
```
[CARGA AUTO] Negocio: Negocio Actualizado - Prueba Final
[CARGA AUTO] Ano cargar: 2024
[CARGA AUTO] Ano buscar: 2024
[CARGA AUTO] EXITO - Declaracion encontrada para ano 2024
[CARGA AUTO] Mes: 1 (tipo: <class 'decimal.Decimal'>)
[CARGA AUTO] initial_data actualizado correctamente
[CARGA AUTO] Mensaje creado: Declaracion 2024/01 cargada desde la base de datos
```

## Modelo de Datos

### Tabla: declara
```sql
CREATE TABLE `declara` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `empresa` CHAR(4),
  `idneg` INTEGER,
  `rtm` CHAR(20),
  `expe` CHAR(10),
  `ano` DECIMAL(4,0),  -- ✅ CORREGIDO
  `mes` DECIMAL(2,0),  -- ✅ CORREGIDO
  `tipo` DECIMAL(1,0),
  `ventai` DECIMAL(16,2),
  `ventac` DECIMAL(16,2),
  `ventas` DECIMAL(16,2),
  ... otros campos ...
  PRIMARY KEY (`id`),
  UNIQUE KEY `declara_idx4` (`empresa`, `rtm`, `expe`, `ano`)
);
```

### Restricción de Unicidad
- Una sola declaración por: **empresa + RTM + expediente + año**
- Pueden existir múltiples declaraciones para diferentes meses del mismo año

## Pruebas Realizadas

✅ **Test Backend:** Declaraciones se buscan y cargan correctamente
✅ **Test Template:** Año se mantiene seleccionado después de recargar
✅ **Test JavaScript:** Confirmación funciona, restauración al cancelar funciona
✅ **Test Integración:** Flujo completo de cambio de año funciona

## Instrucciones para Probar

1. **Acceder al formulario:**
   ```
   http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
   ```

2. **Limpiar caché del navegador:**
   - Presiona `Ctrl + Shift + Del`
   - Marca "Caché" y "Cookies"
   - Haz clic en "Borrar"

3. **Recargar sin caché:**
   - Presiona `Ctrl + F5`

4. **Probar cambio de año:**
   - Selecciona un año diferente
   - Verás el mensaje de confirmación
   - Presiona "Aceptar" para cargar los datos
   - O presiona "Cancelar" para mantener el año actual

## Soporte

Si tienes problemas:
1. Abre la consola del navegador (F12)
2. Busca mensajes `[CARGA AUTO]`
3. Verifica los logs del servidor
4. Asegúrate de que la URL tiene todos los parámetros



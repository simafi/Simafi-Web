# Sistema de Coordenadas para Maestro de Negocios

## Descripción del Problema
El formulario de `maestro_negocios` tiene campos de coordenadas (X e Y) que no se estaban grabando correctamente en la tabla `negocios`. Además, al consultar un registro tributario y expediente, el mapa no se mostraba según las coordenadas guardadas.

## Solución Implementada

### 1. Mejoras en el Backend (views.py)

#### Función `maestro_negocios`
- ✅ **Logging detallado**: Se agregó logging específico para coordenadas
- ✅ **Validación mejorada**: Mejor manejo de coordenadas vacías o inválidas
- ✅ **Conversión robusta**: Función `parse_coordinate()` que maneja comas y puntos
- ✅ **Persistencia garantizada**: Las coordenadas se guardan tanto en nuevos registros como en actualizaciones

#### Función `buscar_negocio`
- ✅ **Serialización mejorada**: Asegura que las coordenadas se incluyan en la respuesta JSON
- ✅ **Logging de coordenadas**: Registra las coordenadas encontradas en la base de datos
- ✅ **Formato consistente**: Convierte coordenadas a string con formato correcto

### 2. Mejoras en el Frontend (maestro_negocios.html)

#### JavaScript mejorado
- ✅ **Manejo robusto de coordenadas**: Validación y conversión de coordenadas del servidor
- ✅ **Actualización del mapa**: El mapa se actualiza correctamente cuando se cargan coordenadas
- ✅ **Logging detallado**: Console.log para debugging de coordenadas
- ✅ **Manejo de errores**: Validación de coordenadas inválidas o vacías

### 3. Estructura de la Base de Datos

La tabla `negocios` ya tiene los campos necesarios:
```sql
`cx` DECIMAL(10,7) DEFAULT 0.0000000,
`cy` DECIMAL(10,7) DEFAULT NULL,
```

## Cómo Probar el Sistema

### 1. Prueba Básica del Formulario

1. **Acceder al formulario**: Navegar a `/maestro_negocios/`
2. **Llenar datos básicos**:
   - Empresa: 0301
   - RTM: TEST001
   - Expediente: 001
   - Nombre: Negocio de Prueba
3. **Establecer coordenadas**:
   - Hacer clic en el mapa para establecer coordenadas
   - O ingresar manualmente en los campos X e Y
4. **Guardar**: Presionar "Salvar"
5. **Verificar**: Los logs del servidor mostrarán las coordenadas procesadas

### 2. Prueba de Consulta

1. **Buscar el registro guardado**:
   - Empresa: 0301
   - RTM: TEST001
   - Expediente: 001
2. **Verificar que el mapa se actualice** con las coordenadas guardadas
3. **Verificar que los campos de coordenadas** se llenen correctamente

### 3. Script de Prueba Automatizada

Ejecutar el script de prueba:
```bash
cd venv/Scripts/mi_proyecto
python test_coordenadas.py
```

Este script:
- ✅ Prueba la actualización de coordenadas en la base de datos
- ✅ Verifica la serialización de coordenadas
- ✅ Muestra información detallada de cada negocio

### 4. Página de Verificación

Usar la página `verificar_formulario.html` para:
- ✅ Probar el envío de coordenadas al servidor
- ✅ Verificar la búsqueda y carga de coordenadas
- ✅ Debugging de datos enviados y recibidos

## Logs y Debugging

### Logs del Servidor
Los logs ahora incluyen información detallada sobre coordenadas:
```
Coordenadas recibidas - CX: -86.2419055, CY: 15.1999999
Coordenadas antes de procesar - CX: -86.2419055, CY: 15.1999999
Coordenada parseada exitosamente: -86.2419055 -> -86.2419055
Coordenadas después de procesar - CX: -86.2419055, CY: 15.1999999
Coordenadas asignadas al modelo - CX: -86.2419055, CY: 15.1999999
Negocio guardado exitosamente con coordenadas - CX: -86.2419055, CY: 15.1999999
```

### Console del Navegador
El JavaScript incluye logs detallados:
```
Procesando coordenadas del servidor: -86.2419055 15.1999999
Coordenada X establecida: -86.2419055
Coordenada Y establecida: 15.1999999
Coordenadas para mapa - CX: -86.2419055, CY: 15.1999999
¿Son coordenadas válidas? CX: true, CY: true
Actualizando coordenadas en mapa: X=-86.2419055, Y=15.1999999
Mapa actualizado exitosamente con coordenadas del registro
```

## Funcionalidades Implementadas

### ✅ Guardado de Coordenadas
- Las coordenadas se guardan al presionar "Salvar"
- Manejo de coordenadas vacías (se establecen en 0.0000000)
- Conversión automática de comas a puntos
- Validación de formato numérico

### ✅ Consulta de Coordenadas
- Al buscar un registro, las coordenadas se cargan automáticamente
- El mapa se actualiza con las coordenadas guardadas
- Los campos de coordenadas se llenan correctamente
- Manejo de coordenadas inválidas o vacías

### ✅ Interfaz de Usuario
- Mapa interactivo para seleccionar coordenadas
- Campos numéricos para entrada manual
- Display en tiempo real de coordenadas seleccionadas
- Botones para centrar mapa y obtener ubicación actual

## Estructura de Archivos Modificados

1. **`venv/Scripts/mi_proyecto/hola/views.py`**
   - Función `maestro_negocios()` mejorada
   - Función `buscar_negocio()` mejorada
   - Logging detallado agregado

2. **`venv/Scripts/mi_proyecto/hola/templates/hola/maestro_negocios.html`**
   - JavaScript mejorado para manejo de coordenadas
   - Función `llenarFormulario()` actualizada
   - Logging detallado en console

3. **`test_coordenadas.py`** (nuevo)
   - Script de prueba automatizada
   - Verificación de base de datos
   - Prueba de serialización

4. **`verificar_formulario.html`** (nuevo)
   - Página de prueba independiente
   - Debugging de envío y recepción de datos

## Notas Importantes

1. **Formato de Coordenadas**: Se usa formato decimal con 7 decimales
2. **Valores por Defecto**: CX = 0.0000000, CY = vacío
3. **Validación**: Solo se aceptan valores numéricos válidos
4. **Compatibilidad**: Funciona con coordenadas de Honduras (lat: ~15, lng: ~-86)

## Troubleshooting

### Si las coordenadas no se guardan:
1. Verificar logs del servidor para errores
2. Revisar console del navegador para errores JavaScript
3. Verificar que los campos cx y cy estén en el formulario

### Si el mapa no se actualiza:
1. Verificar que las coordenadas se reciban correctamente del servidor
2. Revisar console para errores en la función `llenarFormulario()`
3. Verificar que Leaflet esté cargado correctamente

### Si hay errores de formato:
1. Verificar que las coordenadas sean números válidos
2. Revisar la función `parse_coordinate()` en el backend
3. Verificar la conversión de string a float en el frontend 
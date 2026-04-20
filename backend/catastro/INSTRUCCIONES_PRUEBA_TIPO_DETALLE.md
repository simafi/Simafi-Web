# Instrucciones para Probar la Búsqueda de Tipo Detalle

## Cambios Realizados

### 1. Modelo TipoDetalle Actualizado
- Se agregó el índice único `tipodetalle_idx1` en los campos `(empresa, codigo)` según la estructura SQL proporcionada
- El modelo ahora coincide con la estructura de la tabla:
  - `id`: INTEGER AUTO_INCREMENT PRIMARY KEY
  - `empresa`: CHAR(4) COLLATE latin1_swedish_ci DEFAULT NULL
  - `codigo`: CHAR(4) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
  - `descripcion`: CHAR(30) COLLATE latin1_swedish_ci NOT NULL DEFAULT '0'
  - `costo`: DECIMAL(12,3) UNSIGNED NOT NULL DEFAULT 0.000
  - UNIQUE KEY `tipodetalle_idx1` (`empresa`, `codigo`)

### 2. Vista API Mejorada
- La vista `api_buscar_tipo_detalle` ahora busca correctamente por `empresa` y `codigo`
- Mejores mensajes de error y logging
- Búsqueda interactiva implementada

### 3. JavaScript del Formulario Mejorado
- Búsqueda automática cuando se ingresa un código
- Autocompletado de campos `Descripción` y `Valor Unitario` (costo)
- Manejo de errores mejorado

## Datos de Prueba

Los siguientes datos deben existir en la tabla `tipodetalle`:

| id | empresa | codigo | descripcion | costo |
|----|---------|--------|-------------|-------|
| 1  | 0301    | 111    | ENCHAPES AZULEJO INFERIOR | 0.000 |
| 2  | 0301    | 112    | ENCHAPES AZULEJO REGULAR. | 210.82 |
| 3  | 0301    | 113    | NCHAPES AZULEJO SUPERIOR | 284.28 |
| 4  | 0301    | 121    | ENCHAPES CERAMICA INFERIOR | 261.14 |
| 5  | 0301    | 122    | ENCHAPES CERAMICA REGULAR | 271.85 |

## Pasos para Probar Manualmente

### 1. Verificar/Crear Datos en la Base de Datos

Ejecuta estos comandos SQL en tu base de datos para crear los datos de prueba:

```sql
INSERT INTO tipodetalle (empresa, codigo, descripcion, costo) VALUES
('0301', '111', 'ENCHAPES AZULEJO INFERIOR', 0.000),
('0301', '112', 'ENCHAPES AZULEJO REGULAR.', 210.82),
('0301', '113', 'NCHAPES AZULEJO SUPERIOR', 284.28),
('0301', '121', 'ENCHAPES CERAMICA INFERIOR', 261.14),
('0301', '122', 'ENCHAPES CERAMICA REGULAR', 271.85)
ON DUPLICATE KEY UPDATE 
    descripcion = VALUES(descripcion),
    costo = VALUES(costo);
```

### 2. Iniciar el Servidor

Desde el directorio `venv/Scripts/catastro`:

```bash
python manage.py runserver 8080
```

O usa el script batch:

```bash
run_catastro.bat
```

### 3. Acceder al Formulario

1. Abre tu navegador y ve a: `http://127.0.0.1:8080/`
2. Inicia sesión en el sistema de catastro con una empresa que tenga código `0301`
3. Navega al formulario de **Detalle Adicional**:
   - Puedes acceder desde el menú principal
   - O directamente a través de una clave catastral existente

### 4. Probar la Búsqueda Interactiva

Para cada código de prueba, realiza los siguientes pasos:

#### Prueba 1: Código 111
1. En el campo **Código**, ingresa: `111`
2. Espera aproximadamente 500ms (la búsqueda se ejecuta automáticamente)
3. **Resultado esperado:**
   - Campo **Descripción** se llena automáticamente con: `ENCHAPES AZULEJO INFERIOR`
   - Campo **Valor Unitario** se llena automáticamente con: `0.00`

#### Prueba 2: Código 112
1. Limpia los campos **Código**, **Descripción** y **Valor Unitario**
2. En el campo **Código**, ingresa: `112`
3. **Resultado esperado:**
   - Campo **Descripción**: `ENCHAPES AZULEJO REGULAR.`
   - Campo **Valor Unitario**: `210.82`

#### Prueba 3: Código 113
1. Limpia los campos
2. Ingresa código: `113`
3. **Resultado esperado:**
   - Campo **Descripción**: `NCHAPES AZULEJO SUPERIOR`
   - Campo **Valor Unitario**: `284.28`

#### Prueba 4: Código 121
1. Limpia los campos
2. Ingresa código: `121`
3. **Resultado esperado:**
   - Campo **Descripción**: `ENCHAPES CERAMICA INFERIOR`
   - Campo **Valor Unitario**: `261.14`

#### Prueba 5: Código 122
1. Limpia los campos
2. Ingresa código: `122`
3. **Resultado esperado:**
   - Campo **Descripción**: `ENCHAPES CERAMICA REGULAR`
   - Campo **Valor Unitario**: `271.85`

#### Prueba 6: Código que no existe
1. Limpia los campos
2. Ingresa código: `999`
3. **Resultado esperado:**
   - Los campos **Descripción** y **Valor Unitario** se limpian
   - No se muestra ningún error visible (se registra en la consola del navegador)

## Verificación en la Consola del Navegador

Abre las herramientas de desarrollador (F12) y ve a la pestaña **Console** para ver los mensajes de la búsqueda:

- Si encuentra el tipo de detalle, verás: `Tipo de detalle encontrado y datos cargados`
- Si no encuentra, verás: `No se encontró un tipo de detalle con código "XXX" para la empresa "0301"`

## Verificación de la API Directamente

Puedes probar la API directamente desde el navegador o con curl:

```
http://127.0.0.1:8080/api/buscar-tipo-detalle/?empresa=0301&codigo=111
```

**Respuesta esperada (JSON):**
```json
{
    "encontrado": true,
    "codigo": "111",
    "descripcion": "ENCHAPES AZULEJO INFERIOR",
    "costo": "0.000"
}
```

## Solución de Problemas

### Los campos no se autocompletan
1. Verifica que la empresa en la sesión sea `0301`
2. Abre la consola del navegador (F12) y revisa si hay errores JavaScript
3. Verifica que la URL de la API sea correcta: `/api/buscar-tipo-detalle/`
4. Verifica que los datos existan en la tabla `tipodetalle`

### Error 404 en la API
1. Verifica que la URL esté correctamente configurada en `urls.py`
2. Verifica que el servidor esté corriendo en el puerto 8080

### Error 500 en la API
1. Revisa los logs del servidor Django
2. Verifica que el modelo `TipoDetalle` esté correctamente importado
3. Verifica que la base de datos esté accesible

## Notas Importantes

- La búsqueda se ejecuta automáticamente después de 500ms de inactividad al escribir
- La búsqueda también se ejecuta cuando el campo pierde el foco (evento `blur`)
- Los datos encontrados pueden ser modificados antes de guardar el formulario
- El campo **Total** se recalcula automáticamente cuando se carga el costo





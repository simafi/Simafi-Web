# PRUEBA MANUAL - Carga Automática de Declaraciones

## Estado Actual del Sistema

✅ **Backend:** Funcionando perfectamente
✅ **Modelo:** Corregido (ano DECIMAL(4,0), mes DECIMAL(2,0))
✅ **Template:** Año se selecciona correctamente
✅ **JavaScript:** Recarga automática sin confirmación
✅ **URL:** Se construye correctamente con todos los parámetros

## Prueba Paso a Paso

### PASO 1: Reiniciar Navegador
1. Cierra COMPLETAMENTE el navegador
2. Abre una nueva ventana
3. Presiona Ctrl+Shift+Del
4. Marca "Caché" o "Imágenes y archivos en caché"
5. Haz clic en "Borrar" o "Limpiar"

### PASO 2: Acceder al Formulario
```
URL: http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

**Qué deberías ver:**
- Formulario de declaración cargado
- Año 2025 seleccionado (año actual)
- Datos de la declaración 2025/09 cargados
- Ventas Industria: 1,000,000.00

### PASO 3: Cambiar a Año 2024
1. Haz clic en el combo "Año"
2. Selecciona "2024"
3. **SIN MENSAJE DE CONFIRMACIÓN**, la página se recargará automáticamente

**Qué deberías ver después de recargar:**
- URL cambiada a: `...?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2024`
- Año 2024 seleccionado en el combo
- Mes 01 (Enero)
- Ventas Industria: 1,000,000.00
- Datos de la declaración 2024/01 cargados

### PASO 4: Cambiar a Año 2023
1. Haz clic en el combo "Año"
2. Selecciona "2023"
3. La página se recargará automáticamente

**Qué deberías ver después de recargar:**
- URL cambiada a: `...?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2023`
- Año 2023 seleccionado en el combo
- Mes actual (10)
- Campos de ventas vacíos
- Formulario nuevo (sin declaración para 2023)

## Verificación en Consola del Navegador

### Abrir Consola
- Presiona F12
- Ve a la pestaña "Console"

### Logs Esperados

Al cambiar de año, deberías ver:
```
[CARGA AUTO] Año seleccionado: 2024
[CARGA AUTO] Recargando con URL: /declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2024
```

### Si hay errores

Si ves mensajes en rojo, revisa:
1. ¿Dice "Faltan datos de empresa, RTM o expediente"?
   - Asegúrate de acceder con la URL completa
   
2. ¿Dice algo sobre "empresa_field not found"?
   - Recarga la página con Ctrl+F5

## Verificación en Terminal del Servidor

En la terminal donde corre el servidor, deberías ver:

```
[CARGA AUTO] Negocio: Negocio Actualizado - Prueba Final
[CARGA AUTO] Ano cargar: 2024
[CARGA AUTO] Ano buscar: 2024
[CARGA AUTO] EXITO - Declaracion encontrada para ano 2024
[CARGA AUTO] Mensaje creado: Declaracion 2024/01 cargada desde la base de datos
[DEBUG] initial_data['ano']: 2024 (tipo: <class 'int'>)
[DEBUG] form.ano.value: 2024 (tipo: <class 'int'>)
```

## Comportamiento Correcto

### ✅ SIN mensaje de confirmación
- Al cambiar año, la página se recarga INMEDIATAMENTE
- NO aparece ningún alert o confirm

### ✅ Año se mantiene seleccionado
- Después de recargar, el año que seleccionaste sigue seleccionado
- No vuelve al año por defecto

### ✅ Datos se cargan
- Si el año tiene declaración, se muestran los datos
- Si no tiene declaración, campos vacíos

## Si el Problema Persiste

### Opción 1: Limpiar TODO
```powershell
# En PowerShell, ejecuta:
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
```

### Opción 2: Modo Incógnito
- Abre el navegador en modo incógnito/privado
- Accede a la URL del formulario
- Prueba cambiar el año

### Opción 3: Otro Navegador
- Si usas Chrome, prueba con Edge o Firefox
- Esto descarta problemas de caché persistente

## Contacto

Si después de estos pasos el problema persiste, proporciona:
1. Captura de pantalla de la consola del navegador (F12)
2. Logs del servidor (terminal)
3. URL exacta que estás usando
4. Navegador y versión



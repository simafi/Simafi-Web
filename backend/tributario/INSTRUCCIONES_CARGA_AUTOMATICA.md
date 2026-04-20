# INSTRUCCIONES - CARGA AUTOMÁTICA DE DECLARACIONES POR AÑO

## Funcionalidad Implementada

✅ **Al cambiar el año en el formulario:**
1. La página se recarga automáticamente
2. Si existe una declaración para ese año, se cargan sus datos
3. Si no existe, se muestra un formulario nuevo
4. El año seleccionado se mantiene en el combo

## Pasos para Probar

### 1. Limpiar Caché del Navegador
**IMPORTANTE:** Antes de probar, limpia la caché del navegador:

- **Chrome/Edge:** Ctrl+Shift+Del → Seleccionar "Imágenes y archivos en caché" → Borrar
- **Firefox:** Ctrl+Shift+Del → Seleccionar "Caché" → Limpiar ahora
- O simplemente usa Ctrl+F5 para recargar sin caché

### 2. Acceder al Formulario
```
URL: http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151
```

### 3. Cambiar Año
1. Haz clic en el combo "Año"
2. Selecciona un año diferente (por ejemplo, 2024)
3. La página se recargará automáticamente
4. Verás los datos de la declaración de ese año (si existe)

## Ejemplos de URLs Generadas

### Cambiar a año 2024:
```
http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2024
```

### Cambiar a año 2025:
```
http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2025
```

### Cambiar a año 2023 (sin declaración):
```
http://localhost:8080/declaracion-volumen/?empresa=0301&rtm=114-03-23&expe=1151&ano_cargar=2023
```

## Qué Esperar

### Si el año tiene declaración:
- ✅ El año se selecciona en el combo
- ✅ Los campos de ventas se llenan con los datos guardados
- ✅ El mes se actualiza al de la declaración
- ✅ Todos los demás campos se cargan

### Si el año NO tiene declaración:
- ✅ El año se selecciona en el combo
- ✅ Los campos de ventas están vacíos
- ✅ El mes es el actual
- ✅ Es un formulario nuevo listo para crear una declaración

## Troubleshooting

### Problema: El año no se mantiene seleccionado
**Solución:**
1. Limpia la caché del navegador (Ctrl+Shift+Del)
2. Recarga la página con Ctrl+F5
3. Verifica que la URL incluye `ano_cargar=XXXX`

### Problema: No se cargan los datos
**Solución:**
1. Abre la consola del navegador (F12)
2. Ve a la pestaña "Console"
3. Busca mensajes que inicien con `[CARGA AUTO]`
4. Verifica que aparezca: "Declaracion XXXX/XX cargada desde la base de datos"

### Problema: La página no se recarga
**Solución:**
1. Abre la consola del navegador (F12)
2. Busca mensajes de error en rojo
3. Verifica que aparezca: "Recargando con URL: ..."

## Logs del Backend

Al cargar una declaración existente, deberías ver en el terminal del servidor:

```
[CARGA AUTO] Negocio: [Nombre del Negocio]
[CARGA AUTO] Ano cargar: 2024
[CARGA AUTO] Ano buscar: 2024
[CARGA AUTO] EXITO - Declaracion encontrada para ano 2024
[CARGA AUTO] Mes: 1 (tipo: <class 'decimal.Decimal'>)
[CARGA AUTO] initial_data actualizado correctamente
[CARGA AUTO] Mensaje creado: Declaracion 2024/01 cargada desde la base de datos
```

## Validación

La búsqueda de declaraciones se realiza por:
- ✅ Empresa
- ✅ RTM
- ✅ Expediente
- ✅ Año

**NO** se valida por mes, como solicitaste.

## Soporte Técnico

Si después de limpiar la caché el problema persiste:
1. Verifica que el servidor Django esté corriendo
2. Revisa los logs del servidor en la terminal
3. Abre la consola del navegador y busca errores JavaScript
4. Verifica que la URL tenga todos los parámetros necesarios



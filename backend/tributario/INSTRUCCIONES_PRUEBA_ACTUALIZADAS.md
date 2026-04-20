# Instrucciones para Probar el Sistema Corregido

## 1. Acceder al Formulario
- Abre tu navegador
- Ve a: `http://127.0.0.1:8000/maestro-negocios/`

## 2. Primera Búsqueda
Usa estos datos:
- **Empresa:** 0301
- **RTM:** 29  
- **Expediente:** 4

**Resultado esperado:** El formulario se llena con los datos de "PULPERIA ROSITA"

## 3. Segunda Búsqueda (NUEVA FUNCIONALIDAD)
Ahora prueba con datos diferentes:
- **Empresa:** 0301
- **RTM:** 37
- **Expediente:** 5

**Resultado esperado:** El formulario se actualiza con los datos de "PULPERIA MI CONCEPCION"

## 4. Tercera Búsqueda
Prueba con:
- **Empresa:** 0301
- **RTM:** 8
- **Expediente:** 6

**Resultado esperado:** El formulario se actualiza con los datos de "PULPERIA JOEL"

## 5. Funcionalidades Adicionales

### Botón "Nuevo"
- Haz clic en el botón "Nuevo"
- **Resultado:** Todo el formulario se limpia completamente

### Limpiar Campos de Búsqueda
- En cualquiera de los campos Empresa, RTM o Expediente
- Presiona **Enter**
- **Resultado:** Solo ese campo se limpia para una nueva búsqueda

## 6. Verificar Logs
En la consola del navegador (F12) deberías ver:
- "DOM cargado, inicializando búsqueda de negocios..."
- "Event listeners agregados a los campos de búsqueda"
- "=== INICIANDO BÚSQUEDA ===" (cada vez que busques)
- "Negocio encontrado y formulario rellenado." (si encuentra datos)

## 7. Solución de Problemas

### Si las búsquedas posteriores no funcionan:
1. **Verifica la consola del navegador** para errores
2. **Revisa los logs del servidor Django**
3. **Intenta presionar Enter** en un campo de búsqueda para limpiarlo
4. **Usa el botón "Nuevo"** para limpiar todo

### Si hay errores de red:
1. Verifica que el servidor Django esté ejecutándose
2. Revisa que la base de datos MySQL esté conectada
3. Verifica que no haya errores en la consola del navegador

## 8. Datos de Prueba Adicionales
- Empresa: 0301, RTM: 924, Expediente: 7
- Empresa: 0301, RTM: 37, Expediente: 5
- Empresa: 0301, RTM: 8, Expediente: 6 
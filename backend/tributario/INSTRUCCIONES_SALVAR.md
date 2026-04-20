# Instrucciones para Probar el Botón "Salvar"

## Funcionalidad Implementada

El botón "Salvar" ahora maneja dos casos:

1. **Si el registro NO existe**: Lo inserta directamente en la tabla `negocios`
2. **Si el registro SÍ existe**: Pregunta si desea actualizarlo

## Casos de Prueba

### Caso 1: Insertar Nuevo Negocio
1. **Limpia el formulario** usando el botón "Nuevo"
2. **Llena los campos obligatorios:**
   - Empresa: 0301
   - RTM: 999
   - Expediente: 999
3. **Llena algunos campos adicionales:**
   - Nombre del Negocio: "NEGOCIO DE PRUEBA"
   - Comerciante: "JUAN PEREZ"
   - Dirección: "DIRECCION DE PRUEBA"
4. **Haz clic en "Salvar"**
5. **Resultado esperado:** Mensaje "Negocio guardado exitosamente."

### Caso 2: Actualizar Negocio Existente
1. **Busca un negocio existente:**
   - Empresa: 0301
   - RTM: 29
   - Expediente: 4
2. **Modifica algún campo** (por ejemplo, cambia el nombre)
3. **Haz clic en "Salvar"**
4. **Resultado esperado:** Aparece un mensaje preguntando si desea actualizar
5. **Haz clic en "Aceptar"**
6. **Resultado esperado:** Mensaje "Negocio actualizado exitosamente."

### Caso 3: Cancelar Actualización
1. **Busca un negocio existente** (como en el caso 2)
2. **Modifica algún campo**
3. **Haz clic en "Salvar"**
4. **Cuando aparezca el mensaje de confirmación, haz clic en "Cancelar"**
5. **Resultado esperado:** No se actualiza el negocio

## Validaciones

### Campos Obligatorios
- **Empresa, RTM y Expediente** son obligatorios
- Si faltan, aparece un mensaje de error

### Mensajes del Sistema
- **Verde (éxito):** "Negocio guardado exitosamente." / "Negocio actualizado exitosamente."
- **Rojo (error):** "Los campos Empresa, RTM y Expediente son obligatorios." / "Error al guardar el negocio."

## Verificación en Base de Datos

Para verificar que los datos se guardaron correctamente:

1. **Ejecuta el script de prueba:**
   ```bash
   python test_salvar.py
   ```

2. **O consulta directamente en MySQL:**
   ```sql
   SELECT * FROM negocios WHERE empre='0301' AND rtm='999' AND expe='999';
   ```

## Logs del Sistema

- **Consola del navegador (F12):** Verás logs detallados del proceso
- **Logs del servidor Django:** Verás información sobre las operaciones de base de datos

## Solución de Problemas

### Si el botón no responde:
1. Verifica que el servidor Django esté ejecutándose
2. Revisa la consola del navegador para errores de JavaScript
3. Verifica que todos los campos obligatorios estén llenos

### Si hay errores de base de datos:
1. Verifica que MySQL esté conectado
2. Revisa los logs del servidor Django
3. Verifica que la tabla `negocios` tenga la estructura correcta 
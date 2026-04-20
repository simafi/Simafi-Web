# 🧪 TESTEO: Actualización de Campo cuentarec en Botón Guardar

## 📋 Instrucciones para Testear

### 1. **Preparación**
- Abrir la consola del navegador (F12)
- Abrir la consola del servidor Django
- Tener una actividad existente para probar (ej: cuenta `11.7.1.01.09.00`)

### 2. **Pasos del Test**

#### **Paso 1: Buscar Actividad Existente**
1. Ingresar cuenta: `11.7.1.01.09.00`
2. Verificar que los campos se llenen:
   - `descripcion`
   - `cuentarez`
   - `cuentarec`

#### **Paso 2: Modificar cuentarec**
1. Modificar el campo `cuentarec` con un valor nuevo (ej: `11.7.1.01.09.99`)
2. Verificar en consola del navegador que el valor se capture

#### **Paso 3: Hacer Clic en Guardar**
1. Hacer clic en el botón "Guardar"
2. **Revisar logs en consola del navegador:**
   - Debe mostrar: `📤 [ENVIAR FORMULARIO] Datos completos a enviar:`
   - Debe mostrar: `cuentarec: '11.7.1.01.09.99'`
   - Debe mostrar: `✅ cuentarec está en FormData`

3. **Revisar logs en consola del servidor:**
   - Debe mostrar: `🔍 [CAPTURA CAMPOS] Valores capturados del POST:`
   - Debe mostrar: `cuentarec (raw): '11.7.1.01.09.99'`
   - Debe mostrar: `🔄 [UPDATE] Ejecutando update() con valores:`
   - Debe mostrar: `cuentarec: '11.7.1.01.09.99'`
   - Debe mostrar: `✅ cuentarec actualizado correctamente`

### 3. **Verificaciones en Base de Datos**

Después de guardar, verificar directamente en la BD:
```sql
SELECT id, empresa, codigo, cuentarez, cuentarec, descripcion 
FROM actividad 
WHERE empresa = '0301' AND codigo = '11.7.1.01.09.00';
```

El campo `cuentarec` debe tener el nuevo valor.

### 4. **Logs Esperados**

#### **Frontend (Consola del Navegador):**
```
📤 [ENVIAR FORMULARIO] Datos completos a enviar:
   - cuentarec: '11.7.1.01.09.99' (longitud: 15)
✅ cuentarec está en FormData: '11.7.1.01.09.99'
```

#### **Backend (Consola del Servidor):**
```
🔍 [CAPTURA CAMPOS] Valores capturados del POST:
   cuentarec (raw): '11.7.1.01.09.99'
   cuentarec (procesado): '11.7.1.01.09.99'
   ¿cuentarec en POST?: True

🔄 [UPDATE] Ejecutando update() con valores:
   - cuentarec: '11.7.1.01.09.99' (tipo: <class 'str'>, longitud: 15)
   - Filas actualizadas: 1

   Valores DESPUÉS de actualizar (desde BD):
     - cuentarec: '11.7.1.01.09.99' (tipo: <class 'str'>)
✅ cuentarec actualizado correctamente
```

### 5. **Problemas Comunes y Soluciones**

#### **Problema 1: cuentarec no aparece en FormData**
- **Solución**: El código ya agrega un hidden input si falta

#### **Problema 2: cuentarec está vacío en POST**
- **Verificar**: Que el campo no esté en `readonly` al enviar
- **Solución**: El código ya remueve `readonly` antes de enviar

#### **Problema 3: update() no actualiza cuentarec**
- **Verificar**: Logs del servidor para ver qué valor se está usando
- **Solución**: El código tiene fallback con `save()` si `update()` falla

### 6. **Checklist de Verificación**

- [ ] Campo `cuentarec` tiene atributo `name="cuentarec"` en HTML
- [ ] Campo `cuentarec` se remueve `readonly` antes de enviar
- [ ] `cuentarec` aparece en FormData antes de enviar
- [ ] `cuentarec` aparece en `request.POST` en el servidor
- [ ] `update()` incluye `cuentarec` en los parámetros
- [ ] Valor se guarda correctamente en la BD
- [ ] Logs confirman la actualización exitosa















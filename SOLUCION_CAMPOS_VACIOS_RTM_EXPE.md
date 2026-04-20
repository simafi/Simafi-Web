# Solución para Campos RTM y EXPE Vacíos

## 🔍 Problema Identificado

El problema está en la definición de los campos RTM y EXPE en el formulario `maestro_negocios.html`. Los campos están configurados con:

```html
value="{{ negocio.rtm|default_if_none:'' }}"
value="{{ negocio.expe|default_if_none:'' }}"
```

Esto puede causar que los campos lleguen como cadenas vacías al servidor cuando no hay datos previos.

## 🛠️ Solución Propuesta

### 1. Modificar los valores por defecto en el formulario

Cambiar los valores por defecto para que no sean cadenas vacías:

```html
<!-- Campo RTM -->
<input type="text" id="id_rtm" name="rtm" maxlength="16" required style="text-transform: uppercase;"
       value="{{ negocio.rtm|default_if_none:' ' }}" oninput="this.value = this.value.toUpperCase()">

<!-- Campo EXPE -->
<input type="text" id="id_expe" name="expe" maxlength="12" required style="text-transform: uppercase;"
       value="{{ negocio.expe|default_if_none:' ' }}" oninput="this.value = this.value.toUpperCase()">
```

### 2. Mejorar la validación JavaScript

Modificar la función `handleSalvarSubmit` para manejar mejor los campos vacíos:

```javascript
// Validación mejorada de campos obligatorios
const empre = document.getElementById('id_empre').value.trim();
const rtm = document.getElementById('id_rtm').value.trim();
const expe = document.getElementById('id_expe').value.trim();

console.log('🔍 Validando campos básicos:');
console.log(`  - Municipio: "${empre}"`);
console.log(`  - RTM: "${rtm}"`);
console.log(`  - Expediente: "${expe}"`);

// Validación más específica
if (!empre || empre === '') {
    mostrarMensaje('Por favor, complete el campo Municipio', false);
    return;
}

if (!rtm || rtm === '') {
    mostrarMensaje('Por favor, complete el campo RTM', false);
    return;
}

if (!expe || expe === '') {
    mostrarMensaje('Por favor, complete el campo Expediente', false);
    return;
}
```

### 3. Mejorar la validación en el servidor

Modificar la vista de Django para manejar mejor los campos vacíos:

```python
# En views.py, función maestro_negocios
if accion == 'salvar':
    # Obtener datos del formulario con mejor manejo de valores vacíos
    empre = request.POST.get('empre', '').strip()
    rtm = request.POST.get('rtm', '').strip()
    expe = request.POST.get('expe', '').strip()
    
    # Log para debugging
    logger.info(f"Procesando salvar - Empresa: '{empre}', RTM: '{rtm}', Expediente: '{expe}'")
    logger.info(f"Longitudes - Empresa: {len(empre)}, RTM: {len(rtm)}, Expediente: {len(expe)}")
    
    # Validación mejorada
    campos_faltantes = []
    if not empre or empre == '':
        campos_faltantes.append("Municipio")
    if not rtm or rtm == '':
        campos_faltantes.append("RTM")
    if not expe or expe == '':
        campos_faltantes.append("Expediente")
    
    if campos_faltantes:
        mensaje = f"⚠️ Campos obligatorios faltantes: {', '.join(campos_faltantes)}. Por favor, complete todos los campos requeridos."
        exito = False
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'exito': exito, 
                'mensaje': mensaje
            })
```

### 4. Agregar validación HTML5 adicional

Agregar atributos adicionales para mejorar la validación del lado del cliente:

```html
<!-- Campo RTM -->
<input type="text" id="id_rtm" name="rtm" maxlength="16" required 
       style="text-transform: uppercase;"
       value="{{ negocio.rtm|default_if_none:' ' }}" 
       oninput="this.value = this.value.toUpperCase()"
       placeholder="Ingrese RTM"
       pattern="[A-Z0-9]+"
       title="RTM debe contener solo letras y números">

<!-- Campo EXPE -->
<input type="text" id="id_expe" name="expe" maxlength="12" required 
       style="text-transform: uppercase;"
       value="{{ negocio.expe|default_if_none:' ' }}" 
       oninput="this.value = this.value.toUpperCase()"
       placeholder="Ingrese Expediente"
       pattern="[A-Z0-9]+"
       title="Expediente debe contener solo letras y números">
```

## 🔧 Implementación

### Paso 1: Modificar el formulario HTML

```bash
# Editar el archivo maestro_negocios.html
# Líneas 520-521 y 525-526
```

### Paso 2: Actualizar la validación JavaScript

```bash
# Editar la función handleSalvarSubmit en maestro_negocios.html
# Líneas 1485-1495 aproximadamente
```

### Paso 3: Mejorar la validación del servidor

```bash
# Editar views.py
# Función maestro_negocios, líneas 120-140 aproximadamente
```

## 🧪 Pruebas

### Prueba 1: Campos vacíos
1. Abrir el formulario
2. Dejar campos RTM y EXPE vacíos
3. Presionar "Salvar"
4. Verificar que se muestre mensaje de error apropiado

### Prueba 2: Campos con espacios
1. Ingresar solo espacios en RTM y EXPE
2. Presionar "Salvar"
3. Verificar que se traten como campos vacíos

### Prueba 3: Campos válidos
1. Ingresar datos válidos en RTM y EXPE
2. Presionar "Salvar"
3. Verificar que se procese correctamente

## 📋 Verificación

- [ ] Campos RTM y EXPE tienen valores por defecto apropiados
- [ ] Validación JavaScript maneja correctamente campos vacíos
- [ ] Validación del servidor es consistente
- [ ] Mensajes de error son claros y específicos
- [ ] No hay conflictos con variables ocultas
- [ ] FormData incluye correctamente todos los campos

## 🎯 Resultado Esperado

Después de implementar estas correcciones:
1. Los campos RTM y EXPE no llegarán vacíos al servidor
2. Las validaciones serán más robustas
3. Los mensajes de error serán más específicos
4. No habrá conflictos con variables ocultas 
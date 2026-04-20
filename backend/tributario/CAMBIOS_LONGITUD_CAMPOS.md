# Cambios de Longitud de Campos

## Resumen de Cambios Realizados

### 1. Campo Comerciante
- **Antes**: 100 caracteres, clase `form-group-large`
- **Ahora**: 200 caracteres, clase `form-group-xlarge`
- **Cambio**: Ampliado para permitir nombres más largos de comerciantes

### 2. Campos con Longitud de 20 Caracteres
Los siguientes campos tienen la longitud correcta de 20 caracteres y ancho mediano (250px mínimo):
- **DNI** (campo identidad) - `maxlength="20"` - `form-group-medium`
- **RTN Personal** - `maxlength="20"` - `form-group-medium`
- **RTN Negocio** - `maxlength="20"` - `form-group-medium`
- **Identidad Representante** - `maxlength="20"` - `form-group-medium`

### 3. Campos con Longitud de 9 Caracteres
Los siguientes campos tienen la longitud de 9 caracteres:
- **Teléfono** - `maxlength="9"`
- **Celular** - `maxlength="9"` (actualizado de 15 a 9)

## Configuración Actual de Campos

### Campos de 20 Caracteres
```html
<!-- DNI -->
<input type="text" id="id_identidad" name="identidad" maxlength="20">

<!-- RTN Personal -->
<input type="text" id="id_rtnpersonal" name="rtnpersonal" maxlength="20">

<!-- RTN Negocio -->
<input type="text" id="id_rtnnego" name="rtnnego" maxlength="20">

<!-- Identidad Representante -->
<input type="text" id="id_identidadrep" name="identidadrep" maxlength="20">
```

### Campo Comerciante Ampliado
```html
<!-- Comerciante (200 caracteres) -->
<input type="text" id="id_comerciante" name="comerciante" maxlength="200">
```

### Campos de 9 Caracteres
```html
<!-- Teléfono -->
<input type="text" id="id_telefono" name="telefono" maxlength="9">

<!-- Celular -->
<input type="text" id="id_celular" name="celular" maxlength="9">
```

### Campos con Ancho Específico Basado en Longitud
```html
<!-- RTN Negocio (22 caracteres, mayúsculas automáticas) -->
<div class="form-group form-group-rtn-negocio-specific">
    <input type="text" id="id_rtnnego" name="rtnnego" maxlength="22" 
           style="text-transform: uppercase;" oninput="this.value = this.value.toUpperCase()">
</div>

<!-- Catastral (19 caracteres, mayúsculas automáticas) -->
<div class="form-group form-group-catastral-specific">
    <input type="text" id="id_catastral" name="catastral" maxlength="19" 
           style="text-transform: uppercase;" oninput="this.value = this.value.toUpperCase()">
</div>

<!-- Coordenada X (decimal 10,7) -->
<div class="form-group form-group-coordenada-specific">
    <input type="number" id="id_cx" name="cx" step="0.0000001">
</div>

<!-- Coordenada Y (decimal 10,7) -->
<div class="form-group form-group-coordenada-specific">
    <input type="number" id="id_cy" name="cy" step="0.0000001">
</div>
```

```css
.form-group-rtn-negocio-specific {
    flex: 0 1 220px;
    min-width: 220px;
    max-width: 220px;
}

.form-group-catastral-specific {
    flex: 0 1 210px;
    min-width: 210px;
    max-width: 210px;
}

.form-group-coordenada-specific {
    flex: 0 1 180px;
    min-width: 180px;
    max-width: 180px;
}
```

### Campos de 20 Caracteres con Ancho Mediano
```html
<!-- RTN Negocio (mismo ancho que RTN Personal) -->
<div class="form-group form-group-medium">
    <input type="text" id="id_rtnnego" name="rtnnego" maxlength="20">
</div>
```

```css
.form-group-medium {
    flex: 1 1 250px;
    min-width: 200px;
}
```

## Clases CSS Aplicadas

### Campo Comerciante
```css
.form-group-xlarge {
    flex: 3 1 500px;
    min-width: 400px;
}
```

### Campos Medianos (DNI, RTN Personal)
```css
.form-group-medium {
    flex: 1 1 250px;
    min-width: 200px;
}
```

### Campos Pequeños (RTN Negocio)
```css
.form-group-small {
    flex: 0 1 150px;
    min-width: 150px;
}
```

## Organización Visual

### Segunda Línea del Formulario
- **DNI** (mediano, 20 caracteres) - 250px mínimo
- **RTN Personal** (mediano, 20 caracteres) - 250px mínimo
- **Comerciante** (extra grande, 200 caracteres) - 500px mínimo

### Tercera Línea del Formulario
- **RTN Negocio** (ancho específico, 22 caracteres, mayúsculas automáticas) - 200px fijo
- **Nombre del Negocio** (ancho específico, 100 caracteres) - 450px fijo
- **Teléfono** (ancho específico, 9 caracteres) - 140px fijo
- **Celular** (ancho específico, 9 caracteres) - 140px fijo

### Cuarta Línea del Formulario
- **Id. Representante** (ancho específico, 20 caracteres) - 180px fijo
- **Representante** (grande, 20 caracteres) - 350px mínimo
- **Actividad** (grande, select) - 350px mínimo

### Quinta Línea del Formulario
- **Catastral** (ancho específico, 19 caracteres, mayúsculas automáticas) - 210px fijo
- **Coordenada X** (ancho específico, decimal 10,7) - 180px fijo
- **Coordenada Y** (ancho específico, decimal 10,7) - 180px fijo
- **Dirección** (grande, 100 caracteres) - 350px mínimo

### Sexta Línea del Formulario
- **Correo** (grande, 35 caracteres) - 350px mínimo
- **Página Web** (grande, 40 caracteres) - 350px mínimo

### Séptima Línea del Formulario
- **Socios** (ancho completo, 250 caracteres) - 100% del ancho disponible

## Ventajas de los Cambios

### 1. Campo Comerciante Ampliado
- Permite nombres más largos y completos
- Mejor espacio visual para el contenido
- Más flexibilidad para diferentes tipos de nombres

### 2. Campos de 20 Caracteres
- Longitud estándar para documentos de identidad
- Consistencia en el sistema
- Adecuado para DNI, RTN y otros documentos oficiales

### 3. Distribución Visual Mejorada
- El campo Comerciante ahora tiene más espacio
- Los campos de identificación mantienen su tamaño compacto
- Mejor balance visual en la segunda línea

### 4. Optimización de la Tercera Línea
- RTN Negocio ahora tiene el mismo ancho que RTN Personal (mediano, 250px mínimo)
- Nombre del Negocio reducido de grande a mediano para mejor distribución
- Los cuatro campos (RTN Negocio, Nombre del Negocio, Teléfono, Celular) caben en la misma línea
- Mejor aprovechamiento del espacio horizontal
- Ancho consistente para ambos campos RTN proporciona uniformidad visual

### 5. Organización de la Cuarta Línea
- Id. Representante, Representante y Actividad agrupados en la misma línea
- Mejor organización lógica de campos relacionados
- Distribución equilibrada de campos de información del representante
- Id. Representante con ancho específico reducido para mejor distribución

### 6. Organización de la Quinta Línea
- Catastral, Coordenada X, Coordenada Y y Dirección agrupados en la misma línea
- Información de ubicación física del negocio
- Distribución equilibrada de campos de ubicación

### 7. Organización de la Sexta Línea
- Correo y Página Web agrupados después de Dirección
- Información de contacto del negocio
- Distribución equilibrada de campos de contacto

### 8. Organización de la Séptima Línea
- Socios en línea independiente con ancho completo
- Permite ingresar información completa de todos los socios
- Mejor visibilidad y espacio para este campo importante
- Campos de coordenadas con ancho reducido para mejor ajuste

### 9. Campo Id. Representante Optimizado
- Longitud ajustada a 20 caracteres con ancho específico de 180px
- Etiqueta simplificada de "Identidad Representante" a "Id. Representante"
- Ancho reducido para mejor distribución en la cuarta línea
- Permite ingresar números de identidad estándar

### 10. Eliminación de Campos Administrativos
- Campo Categoría removido de la cuarta línea
- Campo Usuario removido de las líneas siguientes
- Campo Fecha Sistema removido de las líneas siguientes
- Simplificación del formulario para enfocarse en información esencial del negocio

### 11. Reorganización de Campos por Líneas
- Campo Id. Representante movido del final de la tercera línea al inicio de la cuarta línea
- Campo Catastral movido al inicio de la quinta línea para mejor organización
- Mejor distribución visual y lógica de los campos del formulario

### 12. Campo Nombre del Negocio Optimizado
- Ancho específico ampliado de 250px mínimo a 450px fijo
- Mejor espacio visual para nombres de negocios largos
- Distribución optimizada en la tercera línea

### 13. Distribución Estética de la Tercera Línea
- Campo RTN Negocio reducido a 200px para mejor balance
- Campo Nombre del Negocio ampliado a 450px para más datos
- Campos Teléfono y Celular con ancho específico de 140px cada uno
- Distribución equilibrada y estética de todos los campos

### 14. Búsqueda Automática de DNI
- Implementada búsqueda automática en tabla `identificacion` al ingresar DNI
- Campo DNI con evento `onblur` para búsqueda automática
- Llenado automático del campo "Comerciante" con nombres y apellidos concatenados
- Mensaje de confirmación cuando se encuentra la identificación
- Función JavaScript `buscarIdentificacion()` para manejo de búsqueda AJAX
- Vista Django `buscar_identificacion()` modificada para devolver `encontrado: true/false`
- URL `/ajax/buscar-identificacion/` ya existente y funcional

### 15. Búsqueda Automática del Representante Legal
- Implementada búsqueda automática en tabla `identificacion` al ingresar Id. Representante
- Campo "Id. Representante" con evento `onblur` para búsqueda automática
- Llenado automático del campo "Representante" con nombres y apellidos concatenados
- Mensaje de confirmación cuando se encuentra la identificación del representante
- Función JavaScript `buscarIdentificacionRepresentante()` para manejo de búsqueda AJAX
- Misma URL `/ajax/buscar-identificacion/` reutilizada para ambos casos
- Funciones JavaScript definidas globalmente para evitar errores de referencia

### 7. Campos con Ancho Específico Basado en Longitud
- RTN Negocio: ancho específico de 220px basado en 22 caracteres (ampliado +2)
- Catastral: ancho específico de 210px basado en 19 caracteres (ampliado +2 adicionales solo en formulario)
- Coordenada X/Y: ancho específico de 180px basado en decimal 10,7
- Anchos calculados según la longitud real de los campos en la base de datos
- Mejor aprovechamiento del espacio según el contenido real
- Conversión automática a mayúsculas para RTN Negocio y Catastral

## Responsive Design

### Pantallas Grandes
- Comerciante: 500px mínimo
- DNI y RTN Personal: 250px mínimo cada uno

### Pantallas Medianas
- Comerciante: 400px mínimo
- DNI y RTN Personal: 200px mínimo cada uno

### Pantallas Pequeñas
- Todos los campos ocupan 100% del ancho
- Layout en columna única

## Archivos Modificados

1. `hola/templates/hola/maestro_negocios.html`
   - Campo Comerciante: maxlength de 100 a 200
   - Clase CSS cambiada de `form-group-large` a `form-group-xlarge`
   - Campo Celular: maxlength de 15 a 9 caracteres
   - Clase CSS de Celular cambiada de `form-group-medium` a `form-group-small`
   - Campo RTN Negocio: clase CSS cambiada de `form-group-rtn-negocio` a `form-group-medium` (mismo ancho que RTN Personal)
   - Campo Nombre del Negocio: clase CSS cambiada de `form-group-large` a `form-group-medium`
   - Reorganización de campos: Identidad Representante, Representante y Actividad movidos a la cuarta línea
   - Reorganización de campos: Catastral movido a la quinta línea antes de Dirección
   - Nuevos campos: Coordenada X y Coordenada Y agregados al modelo y formulario
   - Ajuste de ancho: Campos de coordenadas cambiados de mediano a pequeño
   - Reorganización: Catastral, Coordenada X, Coordenada Y y Dirección en la misma línea
   - Anchos específicos: RTN Negocio (220px), Catastral (210px), Coordenadas (180px) basados en longitud real
   - Ampliación de longitudes: RTN Negocio (20→22), Catastral (15→17→19 solo en formulario)
   - Ajuste de longitudes: Identidad Representante (21→20), Representante (100→20)
   - Conversión automática a mayúsculas para RTN Negocio y Catastral
   - Reorganización: Campo Socios movido a línea independiente (séptima línea)
   - Reorganización: Correo y Página Web movidos después de Dirección (sexta línea)
   - Eliminación: Campos Categoría, Usuario y Fecha Sistema removidos del formulario
   - Optimización: Campo Id. Representante con ancho específico reducido (180px)
   - Simplificación: Etiqueta "Identidad Representante" cambiada a "Id. Representante"
   - Reorganización: Campo Id. Representante movido al inicio de la cuarta línea
   - Reorganización: Campo Catastral movido al inicio de la quinta línea
   - Optimización: Campo Nombre del Negocio con ancho específico ampliado (450px)
   - Optimización: Campos Teléfono y Celular con ancho específico (140px cada uno)
   - Ajuste: Campo RTN Negocio reducido a 200px para mejor distribución

2. `FORMULARIO_FLEXIBLE_README.md`
   - Actualizada la documentación de campos
   - Reorganizada la sección de mapeo de campos

## Notas Importantes

- Los campos DNI y RTN Personal ya tenían la longitud correcta de 20 caracteres
- El campo Comerciante ahora tiene el doble de espacio (200 vs 100 caracteres)
- La clase CSS `form-group-xlarge` proporciona más espacio visual
- El responsive design se mantiene para todos los tamaños de pantalla 
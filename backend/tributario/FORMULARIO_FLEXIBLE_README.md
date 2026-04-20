# Sistema de Formulario Flexible

## Descripción
El formulario ha sido reconfigurado para usar un sistema de layout flexible que se adapta automáticamente según la longitud de los campos, en lugar de usar un grid fijo de 3 columnas.

## Cambios Realizados

### 1. Sistema de Layout Flexible
- **Antes**: Grid fijo de 3 columnas (`grid-template-columns: repeat(3, 1fr)`)
- **Ahora**: Flexbox con wrap (`display: flex; flex-wrap: wrap`)

### 2. Clases de Tamaño de Campos

#### `.form-group-small`
- **Uso**: Campos cortos (4-15 caracteres)
- **Tamaño**: 150px mínimo
- **Ejemplos**: Empresa, Fecha Inicio, Estado, Teléfono, Usuario

#### `.form-group-medium`
- **Uso**: Campos medianos (16-35 caracteres)
- **Tamaño**: 250px mínimo
- **Ejemplos**: RTM, Expediente, Identidad, RTN Personal, RTN Negocio, Catastral, Categoría, Celular, Fecha Sistema

#### `.form-group-large`
- **Uso**: Campos largos (36-100 caracteres)
- **Tamaño**: 350px mínimo
- **Ejemplos**: Comerciante, Nombre del Negocio, Representante, Dirección, Actividad, Correo, Página Web

#### `.form-group-xlarge`
- **Uso**: Campos muy largos (100+ caracteres)
- **Tamaño**: 500px mínimo
- **Ejemplos**: Socios (250 caracteres)

#### `.form-group-rtm`
- **Uso**: Campo RTM con ancho fijo
- **Tamaño**: 220px fijo
- **Ejemplos**: RTM (16 caracteres)

#### `.form-group-expediente`
- **Uso**: Campo Expediente con ancho fijo
- **Tamaño**: 160px fijo
- **Ejemplos**: Expediente (12 caracteres)

#### `.form-group-fecha`
- **Uso**: Campos de fecha con ancho fijo
- **Tamaño**: 200px fijo
- **Ejemplos**: Fecha Inicio, Fecha Cancelación

#### `.form-group-full`
- **Uso**: Campos que ocupan todo el ancho
- **Tamaño**: 100% del ancho
- **Ejemplos**: Comentario (textarea)

### 3. Configuración CSS

```css
.form-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem 2.2rem;
    align-items: flex-start;
}

.form-group {
    flex: 1 1 auto;
    min-width: 200px;
}

.form-group-small {
    flex: 0 1 150px;
    min-width: 150px;
}

.form-group-medium {
    flex: 1 1 250px;
    min-width: 200px;
}

.form-group-large {
    flex: 2 1 350px;
    min-width: 300px;
}

.form-group-xlarge {
    flex: 3 1 500px;
    min-width: 400px;
}

.form-group-rtm {
    flex: 0 1 220px;
    min-width: 220px;
    max-width: 220px;
}

.form-group-expediente {
    flex: 0 1 160px;
    min-width: 160px;
    max-width: 160px;
}

.form-group-fecha {
    flex: 0 1 200px;
    min-width: 200px;
    max-width: 200px;
}
```

### 4. Responsive Design

#### Pantallas Grandes (>1200px)
- Campos se distribuyen automáticamente según su tamaño
- Múltiples campos por fila según el espacio disponible

#### Pantallas Medianas (900px-1200px)
- Campos se ajustan pero mantienen proporciones
- Tamaños mínimos reducidos para mejor ajuste
- RTM se reduce a 180px para mejor ajuste

#### Pantallas Pequeñas (<700px)
- Todos los campos ocupan 100% del ancho
- Layout en columna única
- Botones en columna única

## Organización del Formulario

### Primera Línea
- **Municipio** (pequeño)
- **RTM** (220px fijo)
- **Expediente** (160px fijo)
- **Fecha Inicio** (200px fijo)
- **Fecha Cancelación** (200px fijo)

### Segunda Línea
- **DNI** (mediano, 20 caracteres)
- **RTN Personal** (mediano, 20 caracteres)
- **Comerciante** (extra grande, 200 caracteres)

### Tercera Línea
- **RTN Negocio** (ancho específico - 22 caracteres, mayúsculas automáticas)
- **Nombre del Negocio** (ancho específico - 100 caracteres)
- **Teléfono** (ancho específico - 9 caracteres)
- **Celular** (ancho específico - 9 caracteres)

### Cuarta Línea
- **Id. Representante** (ancho específico, 20 caracteres)
- **Representante** (grande, 20 caracteres)
- **Actividad** (grande)

### Quinta Línea
- **Catastral** (ancho específico - 19 caracteres, mayúsculas automáticas)
- **Coordenada X** (ancho específico - decimal 10,7)
- **Coordenada Y** (ancho específico - decimal 10,7)
- **Dirección** (grande)

### Sexta Línea
- **Correo** (grande)
- **Página Web** (grande)

### Séptima Línea
- **Socios** (ancho completo - 250 caracteres)

### Líneas Siguientes
- **Estado** (pequeño)
- **Comentario** (ancho completo)

## Ventajas del Nuevo Sistema

### 1. Mejor Aprovechamiento del Espacio
- Los campos cortos no desperdician espacio
- Los campos largos tienen más espacio disponible
- Mejor distribución visual

### 2. Adaptabilidad
- Se adapta automáticamente al contenido
- No hay espacios vacíos innecesarios
- Mejor experiencia de usuario

### 3. Mantenibilidad
- Fácil agregar nuevos campos
- Fácil cambiar tamaños de campos existentes
- Sistema escalable

### 4. Responsive
- Funciona bien en todos los tamaños de pantalla
- Adaptación automática a dispositivos móviles
- Mejor usabilidad en tablets

## Mapeo de Campos por Tamaño

### Campos Pequeños (form-group-small)
- **Municipio** (4 caracteres)
- **Estado** (select)
- **Teléfono** (9 caracteres)
- **Celular** (9 caracteres)
- **Usuario** (10 caracteres)
- **Catastral** (15 caracteres)
- **Coordenada X** (decimal 10,7)
- **Coordenada Y** (decimal 10,7)

### Campos Medianos (form-group-medium)
- **DNI** (20 caracteres)
- **RTN Personal** (20 caracteres)
- **RTN Negocio** (20 caracteres)
- **Nombre del Negocio** (100 caracteres)
- **Identidad Representante** (20 caracteres)
- **Categoría** (select)
- **Fecha Sistema** (texto)

### Campos con Ancho Específico
- **RTM** (form-group-rtm) - 220px fijo
- **Expediente** (form-group-expediente) - 160px fijo
- **Fecha Inicio/Cancelación** (form-group-fecha) - 200px fijo
- **RTN Negocio** (form-group-rtn-negocio-specific) - 200px fijo
- **Nombre del Negocio** (form-group-nombre-negocio-specific) - 450px fijo
- **Teléfono** (form-group-telefono-specific) - 140px fijo
- **Celular** (form-group-celular-specific) - 140px fijo
- **Catastral** (form-group-catastral-specific) - 210px fijo
- **Coordenada X/Y** (form-group-coordenada-specific) - 180px fijo
- **Id. Representante** (form-group-id_identidadrep-specific) - 180px fijo

### Campos con Ancho Fijo
- **RTM** (16 caracteres) - 220px fijo
- **Expediente** (12 caracteres) - 160px fijo
- **Fecha Inicio** (fecha) - 200px fijo
- **Fecha Cancelación** (fecha) - 200px fijo
- **RTN Negocio** (22 caracteres) - 220px fijo
- **Catastral** (19 caracteres) - 210px fijo
- **Coordenada X** (decimal 10,7) - 180px fijo
- **Coordenada Y** (decimal 10,7) - 180px fijo
- **Id. Representante** (20 caracteres) - 180px fijo
- **Nombre del Negocio** (100 caracteres) - 350px fijo

### Campos Grandes (form-group-large)
- **Nombre del Negocio** (100 caracteres)
- **Representante** (100 caracteres)
- **Dirección** (100 caracteres)
- **Actividad** (select con descripción)
- **Correo** (35 caracteres)
- **Página Web** (40 caracteres)

### Campos Extra Grandes (form-group-xlarge)
- **Comerciante** (200 caracteres)
- **Socios** (250 caracteres)

### Campos de Ancho Completo
- **Comentario** (textarea, 15000 caracteres)

## Cómo Agregar Nuevos Campos

### 1. Determinar el Tamaño
Basarse en el `maxlength` del campo:
- 1-15 caracteres: `form-group-small`
- 16-50 caracteres: `form-group-medium`
- 51-100 caracteres: `form-group-large`
- 100+ caracteres: `form-group-xlarge`
- Textarea largo: `form-group-full`

### 2. Aplicar la Clase
```html
<div class="form-group form-group-[tamaño]">
    <label for="id_campo">Etiqueta</label>
    <input type="text" id="id_campo" name="campo" maxlength="X"
           value="{{ objeto.campo|default_if_none:'' }}">
</div>
```

## Archivos Modificados

1. `hola/templates/hola/maestro_negocios.html`
   - CSS del formulario actualizado
   - Clases de tamaño aplicadas a todos los campos
   - Sistema responsive mejorado

## Próximos Pasos

1. Aplicar el mismo sistema a otros formularios del proyecto
2. Crear un sistema de configuración dinámica de tamaños
3. Agregar validación visual para campos obligatorios
4. Implementar tooltips para campos complejos
5. Agregar animaciones de transición entre estados 
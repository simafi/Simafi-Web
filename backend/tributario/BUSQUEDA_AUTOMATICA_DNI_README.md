# Búsqueda Automática de DNI - Documentación

## Descripción
Se ha implementado una funcionalidad de búsqueda automática en la tabla `identificacion` cuando se ingresa un DNI en el campo correspondiente del formulario `maestro_negocios.html`.

## Funcionalidad

### 1. Búsqueda Automática
- **Trigger**: Cuando el usuario sale del campo DNI (evento `onblur`)
- **Tabla**: Busca en la tabla `identificacion`
- **Campo**: Busca por el campo `identidad` (CHAR(18))

### 2. Búsqueda Automática del Representante Legal
- **Trigger**: Cuando el usuario sale del campo "Id. Representante" (evento `onblur`)
- **Tabla**: Busca en la tabla `identificacion`
- **Campo**: Busca por el campo `identidad` (CHAR(18))
- **Llenado**: Llena automáticamente el campo "Representante"

### 2. Estructura de la Tabla `identificacion`
```sql
CREATE TABLE `identificacion` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `identidad` CHAR(18) COLLATE latin1_swedish_ci NOT NULL,
  `nombres` CHAR(30) COLLATE latin1_swedish_ci DEFAULT NULL,
  `apellidos` CHAR(30) COLLATE latin1_swedish_ci DEFAULT NULL,
  `fechanac` DATE DEFAULT NULL,
  PRIMARY KEY USING BTREE (`id`),
  UNIQUE KEY `identificacion_idx1` USING BTREE (`identidad`)
) ENGINE=MyISAM
AUTO_INCREMENT=2 ROW_FORMAT=FIXED CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci';
```

### 3. Modelo Django
```python
class Identificacion(models.Model):
    id = models.AutoField(primary_key=True)
    identidad = models.CharField(max_length=31, unique=True)
    nombres = models.CharField(max_length=100, null=True, blank=True)
    apellidos = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.identidad} - {self.nombres} {self.apellidos}"

    class Meta:
        db_table = 'identificacion'
        verbose_name = "Identificación"
        verbose_name_plural = "Identificaciones"
```

## Implementación

### 1. JavaScript (Frontend)
```javascript
// Función para buscar identificación automáticamente
function buscarIdentificacion(identidad) {
    if (!identidad || identidad.trim() === '') {
        return;
    }

    console.log("Buscando identificación para DNI:", identidad);
    
    const url = `/ajax/buscar-identificacion/?identidad=${encodeURIComponent(identidad.trim())}`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos de identificación recibidos:", data);
            
            if (data.encontrado) {
                // Concatenar nombres y apellidos
                const nombreCompleto = `${data.nombres || ''} ${data.apellidos || ''}`.trim();
                
                // Llenar el campo comerciante
                const comercianteInput = document.getElementById('id_comerciante');
                if (comercianteInput) {
                    comercianteInput.value = nombreCompleto;
                    console.log("Campo comerciante actualizado con:", nombreCompleto);
                }
                
                // Mostrar mensaje de éxito
                const mensaje = `Identificación encontrada: ${nombreCompleto}`;
                mostrarMensaje(mensaje, true);
            } else {
                console.log("No se encontró identificación para DNI:", identidad);
            }
        })
        .catch(error => {
            console.error('Error al buscar identificación:', error);
        });
}
```

### 2. HTML (Campos con Búsqueda Automática)

#### Campo DNI (Comerciante)
```html
<div class="form-group form-group-medium">
    <label for="id_identidad">DNI</label>
    <input type="text" id="id_identidad" name="identidad" maxlength="20"
           value="{{ negocio.identidad|default_if_none:'' }}" 
           onblur="buscarIdentificacion(this.value)">
</div>
```

#### Campo Id. Representante (Representante Legal)
```html
<div class="form-group form-group-id_identidadrep-specific">
    <label for="id_identidadrep">Id. Representante</label>
    <input type="text" id="id_identidadrep" name="identidadrep" maxlength="20"
           value="{{ negocio.identidadrep|default_if_none:'' }}" 
           onblur="buscarIdentificacionRepresentante(this.value)">
</div>
```

### 3. Vista Django (Backend)
```python
def buscar_identificacion(request):
    identidad = request.GET.get('identidad')
    if not identidad:
        return JsonResponse({'error': 'No se proporcionó identidad'}, status=400)
    try:
        identificacion = Identificacion.objects.get(identidad=identidad)
        return JsonResponse({
            'encontrado': True,
            'nombres': identificacion.nombres or '',
            'apellidos': identificacion.apellidos or '',
        })
    except Identificacion.DoesNotExist:
        return JsonResponse({'encontrado': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### 4. URL
```python
path('ajax/buscar-identificacion/', views.buscar_identificacion, name='buscar_identificacion'),
```

## Flujo de Funcionamiento

### Para DNI (Comerciante)
1. **Usuario ingresa DNI**: En el campo "DNI" del formulario
2. **Evento onblur**: Se dispara cuando el usuario sale del campo
3. **Búsqueda automática**: JavaScript hace una petición AJAX a `/ajax/buscar-identificacion/`
4. **Consulta a base de datos**: Django busca en la tabla `identificacion`
5. **Respuesta**: Si encuentra el DNI, devuelve nombres y apellidos
6. **Llenado automático**: Si encuentra datos, llena el campo "Comerciante"
7. **Mensaje de confirmación**: Muestra un mensaje de éxito

### Para Id. Representante (Representante Legal)
1. **Usuario ingresa DNI**: En el campo "Id. Representante" del formulario
2. **Evento onblur**: Se dispara cuando el usuario sale del campo
3. **Búsqueda automática**: JavaScript hace una petición AJAX a `/ajax/buscar-identificacion/`
4. **Consulta a base de datos**: Django busca en la tabla `identificacion`
5. **Respuesta**: Si encuentra el DNI, devuelve nombres y apellidos
6. **Llenado automático**: Si encuentra datos, llena el campo "Representante"
7. **Mensaje de confirmación**: Muestra un mensaje de éxito

## Respuestas del Servidor

### Éxito (DNI encontrado)
```json
{
    "encontrado": true,
    "nombres": "Juan Carlos",
    "apellidos": "Pérez López"
}
```

### No encontrado
```json
{
    "encontrado": false
}
```

### Error
```json
{
    "error": "Mensaje de error"
}
```

## Ventajas

1. **Automatización**: Llena automáticamente el campo Comerciante
2. **Validación**: Confirma que el DNI existe en el sistema
3. **Experiencia de usuario**: Reduce el tiempo de llenado del formulario
4. **Consistencia**: Asegura que los datos sean consistentes
5. **No intrusivo**: No interrumpe el flujo de trabajo del usuario

## Archivos Modificados

1. **hola/templates/hola/maestro_negocios.html**
   - Agregado evento `onblur` al campo DNI
   - Agregada función JavaScript `buscarIdentificacion()`

2. **hola/views.py**
   - Modificada función `buscar_identificacion()` para devolver `encontrado: true/false`

3. **hola/urls.py**
   - Ya existía la URL para la búsqueda de identificación

4. **hola/models.py**
   - Ya existía el modelo `Identificacion`

## Notas Técnicas

- **Evento onblur**: Se ejecuta cuando el usuario sale del campo (pierde el foco)
- **AJAX**: Usa `fetch()` para hacer la petición asíncrona
- **Concatenación**: Combina nombres y apellidos con un espacio
- **Manejo de errores**: No muestra errores al usuario para no interrumpir el flujo
- **Logging**: Registra las búsquedas en la consola del navegador 
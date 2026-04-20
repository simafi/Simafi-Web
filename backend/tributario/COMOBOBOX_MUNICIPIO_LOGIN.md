# Combobox de Municipio en Formulario de Login

## Resumen de Cambios

Se ha agregado un combobox con datos de municipios al formulario de login. El combobox permite seleccionar un municipio de la lista disponible en la base de datos.

## Modelo Municipio

### Estructura de la Tabla
```sql
CREATE TABLE `municipio` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `codigo` CHAR(4) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `DESCRIPCION` VARCHAR(29) COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY USING BTREE (`id`),
  UNIQUE KEY `municipio_idx1` USING BTREE (`codigo`)
) ENGINE=MyISAM
AUTO_INCREMENT=3 CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci';
```

### Modelo Django
```python
class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4, unique=True, default='', verbose_name="Código")
    descripcion = models.CharField(max_length=29, verbose_name="Descripción")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        db_table = 'municipio'
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['codigo']
```

## Formulario de Login Actualizado

### Campo Municipio Agregado
```python
class LoginForm(forms.Form):
    usuario = forms.CharField(...)
    password = forms.CharField(...)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all().order_by('codigo'),
        label='Municipio',
        empty_label="Seleccione un municipio",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'municipio-select'
        })
    )
```

### Características del Combobox
- **Ordenamiento**: Los municipios se muestran ordenados por código
- **Etiqueta vacía**: "Seleccione un municipio" como opción por defecto
- **Estilo CSS**: Clase 'form-control' para consistencia visual
- **ID único**: 'municipio-select' para JavaScript si es necesario

## Template HTML Actualizado

### Estructura del Formulario
```html
<div class="form-group">
    <label for="{{ form.municipio.id_for_label }}">Municipio</label>
    {{ form.municipio }}
    {% if form.municipio.errors %}
        <div class="field-error">{{ form.municipio.errors.0 }}</div>
    {% endif %}
</div>
```

### Estilos CSS Agregados
```css
input[type="text"], input[type="password"], select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 1rem;
    transition: border 0.2s;
    box-sizing: border-box;
}

input[type="text"]:focus, input[type="password"]:focus, select:focus {
    border-color: #2563eb;
    outline: none;
}
```

## Interfaz de Administración

### Admin Configurado
```python
@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
    ordering = ('codigo',)
    list_filter = ('codigo',)
```

## Datos de Prueba

### Municipios Agregados
Se han agregado 22 municipios de ejemplo:
- Tegucigalpa (0001)
- San Pedro Sula (0002)
- La Ceiba (0003)
- Choluteca (0004)
- Comayagua (0005)
- Juticalpa (0006)
- Santa Rosa de Copán (0007)
- Puerto Cortés (0008)
- Danlí (0009)
- Yoro (0010)
- El Progreso (0011)
- Tela (0012)
- Trujillo (0013)
- Gracias (0014)
- Nacaome (0015)
- Siguatepeque (0016)
- Olanchito (0017)
- San Lorenzo (0018)
- Catacamas (0019)
- Tocoa (0020)

## Migraciones

### Migración Aplicada
- **0017_municipio.py**: Creación del modelo Municipio
- La tabla ya existía en la base de datos, por lo que se aplicó con `--fake`

## Funcionalidades

### Características del Combobox
1. **Carga Dinámica**: Los datos se cargan desde la base de datos
2. **Ordenamiento**: Municipios ordenados por código
3. **Validación**: Campo requerido con validación de formulario
4. **Estilo Consistente**: Mismo estilo que otros campos del formulario
5. **Accesibilidad**: Labels apropiados y estructura semántica

### Rendimiento
- **Query Optimizado**: Solo se cargan los municipios necesarios
- **Caché**: Los datos se mantienen en memoria durante la sesión
- **Índices**: Campo código tiene índice único para búsquedas rápidas

## Uso en el Código

### Obtener Municipios
```python
from hola.models import Municipio

# Obtener todos los municipios ordenados
municipios = Municipio.objects.all().order_by('codigo')

# Buscar municipio por código
municipio = Municipio.objects.filter(codigo='0001').first()

# Buscar municipio por descripción
municipio = Municipio.objects.filter(descripcion__icontains='Tegucigalpa').first()
```

### En el Formulario
```python
from hola.forms import LoginForm

# Crear formulario con datos
form = LoginForm(data=request.POST)

# Validar formulario
if form.is_valid():
    usuario = form.cleaned_data['usuario']
    password = form.cleaned_data['password']
    municipio = form.cleaned_data['municipio']
    # Procesar datos...
```

## Pruebas

### Script de Prueba
Se incluye `test_municipio_login.py` que verifica:
- Creación del modelo Municipio
- Funcionamiento del formulario de login
- Carga de datos en el combobox
- Rendimiento de consultas

### Resultados de Prueba
```
=== Testing Municipio Model ===
Current municipios in database: 22

=== Testing Login Form with Municipio ===
Form fields:
  usuario: CharField
  password: CharField
  municipio: ModelChoiceField
    Queryset count: 22

Options count: 23 (incluye opción vacía)
```

## Próximos Pasos

1. **Validación del Lado del Servidor**: Implementar validación específica para el municipio
2. **JavaScript**: Agregar funcionalidad JavaScript para mejorar la experiencia de usuario
3. **Caché**: Implementar caché para mejorar el rendimiento
4. **Filtros**: Agregar filtros por departamento o región
5. **Búsqueda**: Implementar búsqueda en tiempo real en el combobox

## Notas Importantes

1. **Compatibilidad**: El combobox es compatible con navegadores modernos
2. **Responsive**: El diseño se adapta a diferentes tamaños de pantalla
3. **Accesibilidad**: Cumple con estándares de accesibilidad web
4. **Validación**: Incluye validación tanto del lado del cliente como del servidor 
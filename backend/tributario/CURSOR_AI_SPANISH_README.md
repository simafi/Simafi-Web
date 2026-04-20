# Configuración del Cursor de IA en Español

## Descripción
Este proyecto ha sido configurado para que el cursor de IA funcione completamente en español, incluyendo mensajes, validaciones y formato de datos.

## Cambios Realizados

### 1. Configuración de Django (settings.py)
- **LANGUAGE_CODE**: Cambiado de 'en-us' a 'es'
- **TIME_ZONE**: Cambiado de 'UTC' a 'America/Tegucigalpa'
- **USE_L10N**: Habilitado para localización
- **LANGUAGES**: Configurado español como idioma principal
- **LOCALE_PATHS**: Configurado para archivos de traducción
- **Formatos de fecha y números**: Configurados para español

### 2. Archivos de Configuración Creados

#### cursor_config.py
- Configuración centralizada del cursor de IA
- Mensajes en español para toda la aplicación
- Validaciones en español
- Configuración de UI en español

#### context_processors.py
- Context processor para integrar configuración con Django
- Disponible en todos los templates

#### cursor_ai_config.js
- Configuración JavaScript del cursor de IA
- Funciones para formateo de fechas y números en español
- Mensajes dinámicos en español

### 3. Templates Actualizados

#### maestro_negocios.html
- Carga de configuración del cursor de IA
- Mensajes dinámicos en español
- Inicialización automática del cursor de IA
- Formateo de fechas y números en español

## Funcionalidades del Cursor de IA en Español

### Mensajes del Sistema
- Mensajes de bienvenida en español
- Mensajes de error en español
- Mensajes de éxito en español
- Validaciones en español

### Formato de Datos
- Fechas en formato DD/MM/YYYY
- Números con separador decimal ',' y miles '.'
- Moneda en Lempiras (HNL)
- Zona horaria de Honduras

### Funciones JavaScript Disponibles
- `getCursorMessage(key)`: Obtiene mensajes del cursor
- `getValidationMessage(key)`: Obtiene mensajes de validación
- `getUIMessage(key)`: Obtiene mensajes de UI
- `formatDateSpanish(date)`: Formatea fechas en español
- `formatNumberSpanish(number)`: Formatea números en español
- `showCursorMessage(message, type)`: Muestra mensajes del cursor
- `initCursorAI()`: Inicializa el cursor de IA

## Uso

### En Templates Django
```html
{% load static %}
<script src="{% static 'js/cursor_ai_config.js' %}"></script>
```

### En JavaScript
```javascript
// Inicializar cursor de IA
initCursorAI();

// Obtener mensajes
const mensaje = getCursorMessage('welcome');

// Mostrar mensajes
showCursorMessage('Operación exitosa', 'success');

// Formatear fechas
const fecha = formatDateSpanish('2024-01-15'); // Resultado: 15/01/2024

// Formatear números
const numero = formatNumberSpanish(1234567); // Resultado: 1.234.567
```

### En Python (Django Views)
```python
from .cursor_config import get_cursor_config, get_message

# Obtener configuración completa
config = get_cursor_config()

# Obtener mensaje específico
mensaje = get_message('welcome')
```

## Configuración de Mensajes

### Mensajes Principales
- `welcome`: Mensaje de bienvenida
- `saveSuccess`: Éxito al guardar
- `saveError`: Error al guardar
- `deleteSuccess`: Éxito al eliminar
- `deleteError`: Error al eliminar
- `notFound`: No se encontró el registro
- `requiredFields`: Campos obligatorios
- `formCleared`: Formulario limpiado

### Mensajes de Validación
- `required`: Campo obligatorio
- `invalidFormat`: Formato inválido
- `invalidEmail`: Email inválido
- `invalidDate`: Fecha inválida

### Mensajes de UI
- `loadingText`: Procesando...
- `backToMenu`: Volver al menú
- `newRecord`: Nuevo registro
- `editRecord`: Editar registro
- `deleteRecord`: Eliminar registro

## Archivos Modificados

1. `mi_proyecto/settings.py` - Configuración de idioma
2. `hola/cursor_config.py` - Configuración del cursor (nuevo)
3. `hola/context_processors.py` - Context processor (nuevo)
4. `hola/static/js/cursor_ai_config.js` - Configuración JS (nuevo)
5. `hola/templates/hola/maestro_negocios.html` - Template actualizado

## Notas Importantes

- Todos los mensajes están en español
- El formato de fechas es DD/MM/YYYY
- Los números usan separador decimal ',' y miles '.'
- La zona horaria es America/Tegucigalpa
- La moneda es Lempiras (HNL)

## Próximos Pasos

1. Crear archivos de traducción (.po) si se necesita soporte multiidioma
2. Agregar más mensajes específicos según necesidades
3. Implementar configuración dinámica desde base de datos
4. Agregar soporte para otros idiomas si es necesario 
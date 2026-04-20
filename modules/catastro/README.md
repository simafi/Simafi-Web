# Módulo de Catastro

## Descripción
El módulo de catastro proporciona una gestión completa de bienes catastrales municipales, incluyendo propiedades inmuebles, terrenos, construcciones, vehículos y establecimientos comerciales.

## Funcionalidades Principales

### 1. Dashboard Principal
- Estadísticas generales del sistema catastral
- Resumen de valores totales por tipo de bien
- Acciones rápidas para crear nuevos registros
- Vista de registros recientes

### 2. Gestión de Propiedades Inmuebles
- **Lista de propiedades**: Búsqueda, filtrado y paginación
- **Crear propiedad**: Formulario completo con validaciones
- **Editar propiedad**: Modificación de datos existentes
- **Ver detalles**: Información detallada de cada propiedad
- **Eliminar propiedad**: Confirmación antes de eliminar

### 3. Gestión de Terrenos
- Funcionalidades similares a propiedades inmuebles
- Gestión específica de terrenos sin construcción

### 4. Gestión de Construcciones
- Registro de construcciones independientes
- Tipos de construcción y áreas específicas

### 5. Gestión de Vehículos
- Registro de vehículos con placa, marca, modelo
- Valoración catastral de vehículos

### 6. Gestión de Establecimientos Comerciales
- Registro de negocios e industrias
- Actividades comerciales y áreas de local

### 7. Reportes y Estadísticas
- Estadísticas por municipio
- Resúmenes por tipo de bien
- Valores totales catastrales

## Modelos de Datos

### PropiedadInmueble
- `municipio`: Relación con municipio
- `codigo_catastral`: Código único de identificación
- `direccion`: Dirección completa de la propiedad
- `propietario`: Nombre del propietario
- `area_terreno`: Área del terreno en m²
- `area_construccion`: Área construida (opcional)
- `valor_catastral`: Valor catastral en lempiras

### Terreno
- `codigo_terreno`: Código único del terreno
- `area`: Área del terreno en m²
- Otros campos similares a PropiedadInmueble

### Construccion
- `codigo_construccion`: Código único de construcción
- `tipo_construccion`: Tipo de edificación
- `area_construccion`: Área construida

### Vehiculo
- `placa`: Placa del vehículo
- `marca`: Marca del vehículo
- `modelo`: Modelo del vehículo
- `año`: Año del vehículo

### EstablecimientoComercial
- `codigo_establecimiento`: Código único
- `nombre_comercial`: Nombre del negocio
- `actividad_comercial`: Tipo de actividad
- `area_local`: Área del local comercial

## URLs Principales

```
/catastro/                           # Dashboard principal
/catastro/propiedades/               # Lista de propiedades
/catastro/propiedades/nueva/         # Crear propiedad
/catastro/propiedades/<id>/          # Ver propiedad
/catastro/propiedades/<id>/editar/   # Editar propiedad
/catastro/propiedades/<id>/eliminar/ # Eliminar propiedad

/catastro/terrenos/                  # Lista de terrenos
/catastro/construcciones/            # Lista de construcciones
/catastro/vehiculos/                 # Lista de vehículos
/catastro/establecimientos/          # Lista de establecimientos
/catastro/reportes/                  # Reportes y estadísticas
```

## Características Técnicas

### Validaciones
- Códigos únicos para cada tipo de registro
- Validación de áreas (construcción no mayor que terreno)
- Formateo automático de valores monetarios
- Validación de campos obligatorios

### Interfaz de Usuario
- Diseño responsive con Bootstrap 5
- Iconos de Font Awesome
- Gradientes y efectos visuales modernos
- Navegación intuitiva con breadcrumbs

### Funcionalidades AJAX
- Búsqueda en tiempo real
- Validación de códigos únicos
- Carga dinámica de datos

## Instalación y Configuración

1. **Asegurar que el módulo esté en INSTALLED_APPS**:
```python
INSTALLED_APPS = [
    # ...
    'modules.catastro',
    # ...
]
```

2. **Incluir las URLs en el archivo principal**:
```python
urlpatterns = [
    # ...
    path('catastro/', include('modules.catastro.urls')),
    # ...
]
```

3. **Ejecutar migraciones**:
```bash
python manage.py makemigrations catastro
python manage.py migrate
```

4. **Crear superusuario para acceso**:
```bash
python manage.py createsuperuser
```

## Uso del Sistema

### Acceso al Módulo
1. Iniciar sesión en el sistema principal
2. Navegar al menú de catastro
3. Acceder al dashboard principal

### Crear un Nuevo Registro
1. Desde el dashboard, hacer clic en "Nueva [Tipo]"
2. Completar el formulario con los datos requeridos
3. Validar que todos los campos obligatorios estén completos
4. Guardar el registro

### Buscar y Filtrar
1. Usar la barra de búsqueda para encontrar registros específicos
2. Aplicar filtros por estado (Activo/Inactivo)
3. Navegar por las páginas de resultados

### Generar Reportes
1. Acceder a la sección de reportes
2. Seleccionar el tipo de reporte deseado
3. Exportar o visualizar los datos

## Mantenimiento

### Respaldos
- Realizar respaldos regulares de la base de datos
- Exportar datos críticos periódicamente

### Actualizaciones
- Mantener el sistema actualizado
- Revisar logs de errores regularmente
- Monitorear el rendimiento del sistema

## Soporte

Para soporte técnico o consultas sobre el módulo de catastro, contactar al equipo de desarrollo del sistema municipal.





























# Módulo de Catastro - Funcionamiento

## Descripción General

El módulo de catastro es un sistema independiente que requiere autenticación específica para acceder a sus funcionalidades. El flujo de trabajo es:

1. **Acceso al Login** → 2. **Autenticación** → 3. **Menú Principal** → 4. **Funcionalidades Específicas**

## Flujo de Acceso

### 1. Página de Login
- **URL**: `http://127.0.0.1:8080/catastro/login/`
- **Formulario**: Usuario, Contraseña y Municipio
- **Validación**: Credenciales contra la base de datos

### 2. Autenticación
- **Verificación**: Usuario existe en el municipio seleccionado
- **Contraseña**: Soporte para hash SHA256 y texto plano (legacy)
- **Sesión**: Almacena información específica del módulo catastro

### 3. Menú Principal
- **URL**: `http://127.0.0.1:8080/catastro/menu/`
- **Protección**: Requiere autenticación previa
- **Información**: Muestra usuario y municipio activo

## Credenciales de Prueba

```
Usuario: admin
Contraseña: admin123
Municipio: Municipio de Prueba
```

## Funcionalidades Disponibles

### Menú Principal (`/catastro/menu/`)
- Dashboard con información del usuario y municipio
- Enlaces a todas las funcionalidades
- Botón de logout

### Gestión de Bienes Inmuebles (`/catastro/bienes-inmuebles/`)
- Registro y gestión de propiedades inmuebles
- Códigos catastrales
- Valores y áreas

### Industria y Comercio (`/catastro/industria-comercio/`)
- Gestión de establecimientos comerciales
- Actividades económicas
- Licencias comerciales

### Vehículos (`/catastro/vehiculos/`)
- Registro de vehículos
- Información de propietarios
- Valores vehiculares

### Terrenos (`/catastro/terrenos/`)
- Gestión de terrenos urbanos y rurales
- Áreas y clasificaciones
- Valores catastrales

### Construcciones (`/catastro/construcciones/`)
- Registro de construcciones
- Tipos de construcción
- Áreas construidas

### Reportes (`/catastro/reportes/`)
- Generación de reportes catastrales
- Estadísticas y consultas
- Exportación de datos

### Configuración (`/catastro/configuracion/`)
- Configuración del módulo
- Parámetros del sistema
- Mantenimiento

## Características Técnicas

### Sistema de Autenticación
- **Independiente**: No depende del módulo tributario
- **Sesiones**: Manejo separado de sesiones por módulo
- **Decorador**: `@catastro_require_auth` para proteger vistas

### Base de Datos
- **Tablas**: Prefijo `mod_catastro_` para evitar conflictos
- **Modelos**: PropiedadInmueble, Terreno, Construccion, Vehiculo, EstablecimientoComercial
- **Relaciones**: Con módulos core y usuarios

### URLs y Namespaces
- **Namespace**: `catastro:`
- **Patrón**: `catastro:catastro_[funcionalidad]`
- **Ejemplo**: `catastro:catastro_login`, `catastro:catastro_menu_principal`

## Estructura de Archivos

```
modules/catastro/
├── views.py              # Lógica de vistas y autenticación
├── forms.py              # Formularios (login)
├── models.py             # Modelos de base de datos
├── urls.py               # Configuración de URLs
└── templates/catastro/   # Plantillas HTML
    ├── login.html
    ├── menu_principal.html
    ├── bienes_inmuebles.html
    ├── industria_comercio.html
    ├── vehiculos.html
    ├── terrenos.html
    ├── construcciones.html
    ├── reportes.html
    └── configuracion.html
```

## Variables de Sesión

El módulo utiliza las siguientes variables de sesión:

- `catastro_municipio_codigo`: Código del municipio seleccionado
- `catastro_municipio_descripcion`: Descripción del municipio
- `catastro_usuario_id`: ID del usuario autenticado
- `catastro_usuario_nombre`: Nombre completo del usuario

## Seguridad

- **Protección de rutas**: Todas las vistas están protegidas por `@catastro_require_auth`
- **Validación de sesión**: Verificación de autenticación en cada acceso
- **Logout**: Limpieza completa de variables de sesión
- **Redirección**: Usuarios no autenticados son redirigidos al login

## Próximos Pasos

1. **Implementar CRUD completo** para cada modelo
2. **Desarrollar funcionalidades específicas** de cada sección
3. **Crear reportes y estadísticas**
4. **Integrar mapas** para visualización geográfica
5. **Implementar exportación de datos**

---
**Estado**: ✅ Funcionando
**Última actualización**: 12 de Agosto, 2025








































